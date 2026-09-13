#!/usr/bin/env python3
"""
tools/export_repo.py

Export repository Markdown into parts export_001.md, export_002.md, ... each <= part_size bytes.
Generates export-manifest.json with per-file metadata and part metadata.

Requirements implemented:
- Do not split any original .md file across parts.
- First part includes a directory tree (fenced code block) showing the repo Markdown layout
  and a Table of Contents linking to anchors for each exported file.
- Raw Markdown content is preserved byte-for-byte.
- Skips files flagged binary (null byte in beginning) or larger than --max-size.
- Uses git to retrieve last commit sha/date/author and blob SHA.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple

# Defaults
DEFAULT_PART_SIZE = 1_000_000  # 1 MB
DEFAULT_MAX_SIZE = 1_000_000   # files larger than this are skipped by default
PART_NAME_FMT = "{prefix}{num:03d}.md"

MD_EXTENSIONS = (".md", ".MD", ".markdown", ".mdown", ".mkd")


@dataclass
class FileMeta:
    path: str
    size: int
    language: str
    anchor: str
    last_commit: Optional[str]
    last_commit_date: Optional[str]
    last_commit_author: Optional[str]
    blob_sha: Optional[str]
    export_file: Optional[str]  # which part file contains it (or None if skipped)
    skipped: bool = False
    skipped_reason: Optional[str] = None


def run_git(cmd: List[str], cwd: Optional[str] = None, capture_stdout=True) -> str:
    full = ["git"] + cmd
    try:
        out = subprocess.check_output(full, cwd=cwd, stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError:
        return ""


def list_tracked_markdown_files() -> List[str]:
    # Use git ls-files for tracked files only
    patterns = ["*.md", "*.MD", "*.markdown", "*.mdown", "*.mkd"]
    files = []
    for p in patterns:
        out = run_git(["ls-files", "--", p])
        if out:
            for line in out.splitlines():
                if line.strip():
                    files.append(line.strip())
    # Deduplicate and sort
    files = sorted(dict.fromkeys(files))
    return files


def is_probably_binary(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(4096)
            if b"\x00" in chunk:
                return True
            # heuristic: extremely high non-text byte ratio
            if not chunk:
                return False
            nontext = sum(1 for b in chunk if b < 9 or (13 < b < 32) or b > 126)
            if nontext / len(chunk) > 0.3:
                return True
    except Exception:
        return True
    return False


def slugify_for_anchor(s: str) -> str:
    s = s.strip().lower()
    # replace any run of non-alphanum with single hyphen
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if not s:
        s = "file"
    return s


def get_last_commit_info(path: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    # returns (sha, iso-date, author)
    out = run_git(["log", "-1", "--format=%H%x1f%cI%x1f%an", "--", path])
    if not out:
        return None, None, None
    parts = out.strip().split("\x1f")
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    return None, None, None


def get_blob_sha(path: str) -> Optional[str]:
    # git ls-files -s <path> outputs: mode blob_sha stage\tpath
    out = run_git(["ls-files", "-s", "--", path])
    if not out:
        return None
    parts = out.split()
    if len(parts) >= 2:
        return parts[1]
    return None


def build_md_tree(paths: List[str]) -> str:
    # Build a simple tree showing only directories that contain markdown files.
    # Format like:
    # .
    # ├── docs
    # │   ├── README.md
    # │   └── notes.md
    # └── README.md
    if not paths:
        return ".\n"
    tree = {}
    for p in paths:
        parts = p.split("/")
        node = tree
        for i, part in enumerate(parts):
            node = node.setdefault(part, {})

    def render(node: dict, prefix: str = "") -> List[str]:
        items = sorted(node.items())
        lines = []
        for idx, (name, child) in enumerate(items):
            connector = "└── " if idx == len(items) - 1 else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if child:
                extension = "    " if idx == len(items) - 1 else "│   "
                lines.extend(render(child, prefix + extension))
        return lines

    # top-level: if tree has many roots, show '.' then children
    lines = ["."]
    lines.extend(render(tree, ""))
    return "\n".join(lines) + "\n"


def compute_file_block(path: str, meta: FileMeta) -> bytes:
    # Build the bytes block that will be appended to a part for this file.
    # Anchor, heading, metadata lines, blank line, then raw content bytes.
    heading = f'<a id="{meta.anchor}"></a>\n\n# {meta.path}\n\n'
    meta_lines = [
        f"size: {meta.size} bytes",
        f"language: {meta.language}",
        f"last_commit: {meta.last_commit or ''}",
        f"last_commit_date: {meta.last_commit_date or ''}",
        f"last_commit_author: {meta.last_commit_author or ''}",
        f"blob_sha: {meta.blob_sha or ''}",
    ]
    meta_text = "\n".join(meta_lines) + "\n\n"
    # Read raw bytes
    try:
        with open(path, "rb") as f:
            content_bytes = f.read()
    except Exception:
        content_bytes = b""
    parts = []
    parts.append(heading.encode("utf-8"))
    parts.append(meta_text.encode("utf-8"))
    parts.append(content_bytes)
    parts.append(b"\n\n")  # ensure separation between files
    return b"".join(parts)


def partition_files(file_items: List[Tuple[str, FileMeta, bytes]], part_size: int, prefix: str) -> Tuple[List[Tuple[str, bytes, List[str]]], List[FileMeta]]:
    """
    Partition files into parts. Returns parts: list of (part_filename, bytes_content, [paths_in_part])
    and updated list of FileMeta objects (with export_file set where included).
    """
    parts = []
    current = bytearray()
    current_paths = []
    part_index = 1

    for path, meta, block_bytes in file_items:
        block_len = len(block_bytes)
        # If a block itself exceeds part_size, it must have been skipped earlier via max-size; just skip now.
        if block_len > part_size:
            meta.export_file = None
            meta.skipped = True
            meta.skipped_reason = f"file-block-larger-than-part-size ({block_len} > {part_size})"
            continue
        if len(current) + block_len > part_size:
            # flush current
            if current_paths:
                part_name = PART_NAME_FMT.format(prefix=prefix, num=part_index)
                parts.append((part_name, bytes(current), list(current_paths)))
                part_index += 1
            current = bytearray()
            current_paths = []
        current.extend(block_bytes)
        current_paths.append(path)
        meta.export_file = PART_NAME_FMT.format(prefix=prefix, num=part_index)
    # flush last
    if current_paths:
        part_name = PART_NAME_FMT.format(prefix=prefix, num=part_index)
        parts.append((part_name, bytes(current), list(current_paths)))
    return parts, [meta for (_, meta, _) in file_items]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export repository Markdown into sized parts and manifest.")
    parser.add_argument("--branch", default="main", help="Branch name (informational).")
    parser.add_argument("--output-dir", default="./repo-export-output", help="Output directory for export_*.md and export-manifest.json")
    parser.add_argument("--part-prefix", default="export_", help="Prefix for part files (export_ => export_001.md)")
    parser.add_argument("--part-size", type=int, default=DEFAULT_PART_SIZE, help="Maximum bytes per part (default 1,000,000).")
    parser.add_argument("--max-size", type=int, default=DEFAULT_MAX_SIZE, help="Skip files larger than this (bytes).")
    args = parser.parse_args(argv)

    os.makedirs(args.output_dir, exist_ok=True)

    # Ensure we have full git history (workflow should checkout with fetch-depth: 0)
    head = run_git(["rev-parse", "HEAD"]).strip()
    if not head:
        print("Warning: git HEAD not available. Ensure repository is checked out with history.", file=sys.stderr)

    # List tracked markdown files
    md_files = list_tracked_markdown_files()
    if not md_files:
        print("No tracked Markdown files found.", file=sys.stderr)

    file_metas: List[FileMeta] = []
    file_items: List[Tuple[str, FileMeta, bytes]] = []

    for path in md_files:
        # path is relative
        full_path = os.path.join(os.getcwd(), path)
        if not os.path.exists(full_path):
            # skip
            meta = FileMeta(
                path=path,
                size=0,
                language="markdown",
                anchor="",
                last_commit=None,
                last_commit_date=None,
                last_commit_author=None,
                blob_sha=None,
                export_file=None,
                skipped=True,
                skipped_reason="path-missing",
            )
            file_metas.append(meta)
            continue
        # read raw bytes and size
        try:
            with open(full_path, "rb") as f:
                content_bytes = f.read()
        except Exception as e:
            meta = FileMeta(
                path=path,
                size=0,
                language="markdown",
                anchor="",
                last_commit=None,
                last_commit_date=None,
                last_commit_author=None,
                blob_sha=None,
                export_file=None,
                skipped=True,
                skipped_reason=f"read-error: {e}",
            )
            file_metas.append(meta)
            continue

        size = len(content_bytes)

        # skip large files (> max-size)
        if size > args.max_size:
            meta = FileMeta(
                path=path,
                size=size,
                language="markdown",
                anchor="",
                last_commit=None,
                last_commit_date=None,
                last_commit_author=None,
                blob_sha=None,
                export_file=None,
                skipped=True,
                skipped_reason=f"size>{args.max_size}",
            )
            file_metas.append(meta)
            continue

        # skip binary-like
        if is_probably_binary(full_path):
            meta = FileMeta(
                path=path,
                size=size,
                language="markdown",
                anchor="",
                last_commit=None,
                last_commit_date=None,
                last_commit_author=None,
                blob_sha=None,
                export_file=None,
                skipped=True,
                skipped_reason="binary-detected",
            )
            file_metas.append(meta)
            continue

        # metadata from git
        last_commit, last_commit_date, last_commit_author = get_last_commit_info(path)
        blob_sha = get_blob_sha(path)

        # anchor: slugified path + short sha if present
        slug = slugify_for_anchor(path)
        short = (blob_sha[:8] if blob_sha else (last_commit[:8] if last_commit else ""))
        anchor = f"file-{slug}-{short}" if short else f"file-{slug}"

        meta = FileMeta(
            path=path,
            size=size,
            language="markdown",
            anchor=anchor,
            last_commit=last_commit,
            last_commit_date=last_commit_date,
            last_commit_author=last_commit_author,
            blob_sha=blob_sha,
            export_file=None,
            skipped=False,
            skipped_reason=None,
        )

        block = compute_file_block(path, meta)
        file_items.append((path, meta, block))
        file_metas.append(meta)

    # Prepare directory tree and TOC (first part must include these)
    tree_text = build_md_tree([m.path for m in file_metas if not m.skipped])
    tree_block = b"```\n" + tree_text.encode("utf-8") + b"```\n\n"

    # Table of Contents linking to anchors
    toc_lines = []
    for m in file_metas:
        if m.skipped:
            continue
        toc_lines.append(f"- [{m.path}](#{m.anchor})")
    toc_text = "\n".join(toc_lines) + "\n\n"
    toc_block = toc_text.encode("utf-8")

    # Prepend tree + toc to the first part; we'll model that as an initial header bytes for the first part.
    header_block = tree_block + toc_block
    header_size = len(header_block)

    # Sort file_items in stable order (alphabetical)
    file_items = sorted(file_items, key=lambda t: t[0])

    # Prepend header to the first file when partitioning: we'll simulate by decrementing part_size for the first part
    adjusted_part_size_first = args.part_size - header_size
    if adjusted_part_size_first <= 0:
        print("Error: header (tree+TOC) is larger than part size. Increase --part-size.", file=sys.stderr)
        sys.exit(2)

    # Partition files into parts: handle first part specially
    parts = []
    current = bytearray()
    current_paths: List[str] = []
    part_index = 1
    remaining_capacity = adjusted_part_size_first

    for path, meta, block in file_items:
        blen = len(block)
        if blen > args.part_size:
            # If a single file block is larger than the whole part_size, mark skipped.
            meta.export_file = None
            meta.skipped = True
            meta.skipped_reason = f"file-block-larger-than-part-size ({blen} > {args.part_size})"
            continue
        if blen > remaining_capacity:
            # flush current (first part gets header added later)
            if current_paths:
                part_name = PART_NAME_FMT.format(prefix=args.part_prefix, num=part_index)
                parts.append((part_name, bytes(current), list(current_paths)))
                part_index += 1
            current = bytearray()
            current_paths = []
            remaining_capacity = args.part_size  # subsequent parts have full capacity
        current.extend(block)
        current_paths.append(path)
        meta.export_file = PART_NAME_FMT.format(prefix=args.part_prefix, num=part_index)
        remaining_capacity -= blen

    # flush last
    if current_paths:
        part_name = PART_NAME_FMT.format(prefix=args.part_prefix, num=part_index)
        parts.append((part_name, bytes(current), list(current_paths)))

    # Now add header_block to the first part content
    if parts:
        first_name, first_content, first_paths = parts[0]
        combined = header_block + first_content
        parts[0] = (first_name, combined, first_paths)

    # Write parts to output directory
    part_records = []
    for name, content_bytes, paths_in_part in parts:
        out_path = os.path.join(args.output_dir, name)
        with open(out_path, "wb") as fh:
            fh.write(content_bytes)
        size_written = os.path.getsize(out_path)
        part_records.append({"filename": name, "size": size_written})

    # Build manifest
    manifest = {
        "repo": os.path.basename(os.getcwd()),
        "branch": args.branch,
        "parts": part_records,
        "files": [],
    }
    for m in file_metas:
        manifest["files"].append(
            {
                "path": m.path,
                "size": m.size,
                "language": m.language,
                "anchor": m.anchor,
                "last_commit": m.last_commit,
                "last_commit_date": m.last_commit_date,
                "last_commit_author": m.last_commit_author,
                "blob_sha": m.blob_sha,
                "export_file": m.export_file,
                "skipped": m.skipped,
                "skipped_reason": m.skipped_reason,
            }
        )

    manifest_path = os.path.join(args.output_dir, "export-manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)

    print("Export complete.")
    print(f"Parts written: {len(parts)}")
    for p in part_records:
        print(f" - {p['filename']}: {p['size']} bytes")
    print(f"Manifest: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
