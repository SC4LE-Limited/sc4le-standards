#!/usr/bin/env python3
"""
Reliable Markdown exporter for SC4LE-Limited/sc4le-standards.

Fixes included:
- Always walk the actual repo root (not workflow CWD)
- Track skipped files (oversized or unreadable)
- Deterministic anchors
- Robust part splitting (no header-only parts)
- Debug logging for completeness verification
- Manifest includes skipped files
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

MAX_PART_SIZE_DEFAULT = 1_000_000  # bytes
EXPORT_PREFIX = "export_"
EXPORT_MANIFEST = "export-manifest.json"


# -----------------------------
# Git helpers
# -----------------------------

def run_git(args: List[str]) -> str:
    result = subprocess.run(
        ["git"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_repo_root() -> str:
    return run_git(["rev-parse", "--show-toplevel"])


def get_head_commit(branch: str) -> str:
    return run_git(["rev-parse", branch])


def get_last_commit_info(path: str) -> Dict[str, str]:
    fmt = "%H|%cI|%an"
    try:
        out = run_git(["log", "-1", f"--format={fmt}", "--", path])
    except subprocess.CalledProcessError:
        return {"sha": "", "date": "", "author": ""}
    parts = out.split("|")
    if len(parts) != 3:
        return {"sha": "", "date": "", "author": ""}
    return {"sha": parts[0], "date": parts[1], "author": parts[2]}


def get_blob_sha(path: str) -> str:
    try:
        out = run_git(["ls-tree", "HEAD", path])
    except subprocess.CalledProcessError:
        return ""
    if not out:
        return ""
    fields = out.split()
    if len(fields) >= 3 and fields[1] == "blob":
        return fields[2]
    return ""


# -----------------------------
# Data structures
# -----------------------------

class FileInfo:
    def __init__(
        self,
        path: str,
        size: int,
        anchor: str,
        last_commit_sha: str,
        last_commit_date: str,
        last_commit_author: str,
        blob_sha: str,
    ):
        self.path = path
        self.size = size
        self.anchor = anchor
        self.last_commit_sha = last_commit_sha
        self.last_commit_date = last_commit_date
        self.last_commit_author = last_commit_author
        self.blob_sha = blob_sha
        self.export_file: Optional[str] = None


# -----------------------------
# Collection
# -----------------------------

def make_anchor(path: str) -> str:
    return path.lower().replace(" ", "-").replace("/", "-")


def collect_markdown_files(max_size_bytes: int, only_path: Optional[str] = None):
    repo_root = get_repo_root()
    files: List[FileInfo] = []
    skipped_files: List[Dict[str, Any]] = []

    for root, dirs, filenames in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d != ".git"]

        for name in filenames:
            rel_path = os.path.relpath(os.path.join(root, name), repo_root)

            if only_path and rel_path != only_path:
                continue

            if not rel_path.lower().endswith(".md"):
                continue

            full_path = os.path.join(root, name)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                skipped_files.append({
                    "path": rel_path,
                    "reason": "unreadable file"
                })
                continue

            if size > max_size_bytes:
                skipped_files.append({
                    "path": rel_path,
                    "size": size,
                    "reason": "file exceeds max-size-bytes"
                })
                continue

            info = get_last_commit_info(rel_path)
            blob_sha = get_blob_sha(rel_path)
            anchor = make_anchor(rel_path)

            print(f"[exporter] Including: {rel_path} ({size} bytes)")

            files.append(
                FileInfo(
                    path=rel_path,
                    size=size,
                    anchor=anchor,
                    last_commit_sha=info["sha"],
                    last_commit_date=info["date"],
                    last_commit_author=info["author"],
                    blob_sha=blob_sha,
                )
            )

    files.sort(key=lambda f: f.path)
    return files, skipped_files


# -----------------------------
# Directory tree + TOC
# -----------------------------

def build_directory_tree(files: List[FileInfo]) -> str:
    tree: Dict[str, Any] = {}

    for fi in files:
        parts = fi.path.split(os.sep)
        node = tree
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                node.setdefault("__files__", []).append(part)
            else:
                node = node.setdefault(part, {})

    lines: List[str] = []

    def walk(node: Dict[str, Any], prefix: str = ""):
        for key in sorted(k for k in node.keys() if k != "__files__"):
            lines.append(f"{prefix}{key}/")
            walk(node[key], prefix + "    ")
        for fname in sorted(node.get("__files__", [])):
            lines.append(f"{prefix}{fname}")

    walk(tree)
    return "```text\n" + "\n".join(lines) + "\n```"


def build_toc(files: List[FileInfo]) -> str:
    lines = ["## Table of Contents", ""]
    for fi in files:
        lines.append(f"- [{fi.path}](#{fi.anchor})")
    lines.append("")
    return "\n".join(lines)


# -----------------------------
# File section builder
# -----------------------------

def build_file_section(fi: FileInfo, content: str) -> str:
    meta = [
        f'<a name="{fi.anchor}"></a>',
        f"## {fi.path}",
        "",
        f"- **Size:** {fi.size} bytes",
        f"- **Language:** markdown",
        f"- **Last commit SHA:** {fi.last_commit_sha}",
        f"- **Last commit date:** {fi.last_commit_date}",
        f"- **Last commit author:** {fi.last_commit_author}",
        f"- **Blob SHA:** {fi.blob_sha}",
        "",
    ]
    return "\n".join(meta) + content + ("\n" if not content.endswith("\n") else "")


# -----------------------------
# Export parts
# -----------------------------

def write_export_parts(files: List[FileInfo], max_part_size: int, branch: str):
    parts_meta: List[Dict[str, Any]] = []
    if not files:
        return parts_meta

    head_commit = get_head_commit(branch)
    part_index = 1
    current_content = []
    current_size = 0

    # First part header
    header_lines = [
        f"# Repository export: sc4le-standards (part {part_index})",
        "",
        f"- commit: `{head_commit}`",
        f"- branch: `{branch}`",
        f"- generated_by: tools/export_repo.py",
        f"- generated_at: {datetime.utcnow().isoformat()}Z",
        "",
        "---",
        "",
        "## Directory tree (Markdown files)",
        "",
        build_directory_tree(files),
        "",
        build_toc(files),
        "---",
        "",
    ]
    header = "\n".join(header_lines)
    header_bytes = len(header.encode("utf-8"))

    if header_bytes > max_part_size:
        raise RuntimeError("Header exceeds max part size — increase --max-size-bytes.")

    current_content.append(header)
    current_size += header_bytes

    repo_root = get_repo_root()

    for fi in files:
        full_path = os.path.join(repo_root, fi.path)
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()

        section = build_file_section(fi, raw)
        section_bytes = len(section.encode("utf-8"))

        if current_size + section_bytes > max_part_size:
            filename = f"{EXPORT_PREFIX}{part_index:03d}.md"
            content_str = "\n".join(current_content)
            with open(filename, "w", encoding="utf-8") as out_f:
                out_f.write(content_str)
            parts_meta.append({"filename": filename, "size": len(content_str.encode("utf-8"))})

            part_index += 1
            current_content = [
                f"# Repository export: sc4le-standards (part {part_index})",
                "",
                f"- commit: `{head_commit}`",
                f"- branch: `{branch}`",
                f"- generated_by: tools/export_repo.py",
                f"- generated_at: {datetime.utcnow().isoformat()}Z",
                "",
                "---",
                "",
            ]
            current_size = len("\n".join(current_content).encode("utf-8"))

        current_content.append(section)
        current_size += section_bytes
        fi.export_file = f"{EXPORT_PREFIX}{part_index:03d}.md"

    filename = f"{EXPORT_PREFIX}{part_index:03d}.md"
    content_str = "\n".join(current_content)
    with open(filename, "w", encoding="utf-8") as out_f:
        out_f.write(content_str)
    parts_meta.append({"filename": filename, "size": len(content_str.encode("utf-8"))})

    return parts_meta


# -----------------------------
# Manifest
# -----------------------------

def write_manifest(files, parts_meta, skipped_files):
    manifest = {
        "repo": "sc4le-standards",
        "branch": run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": [],
        "parts": parts_meta,
        "skipped_files": skipped_files,
    }

    for fi in files:
        manifest["files"].append({
            "path": fi.path,
            "size": fi.size,
            "language": "markdown",
            "anchor": fi.anchor,
            "last_commit": fi.last_commit_sha,
            "last_commit_date": fi.last_commit_date,
            "last_commit_author": fi.last_commit_author,
            "blob_sha": fi.blob_sha,
            "export_file": fi.export_file,
        })

    with open(EXPORT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


# -----------------------------
# CLI
# -----------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Export markdown files into <=1MB parts with manifest.")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--max-size-bytes", type=int, default=MAX_PART_SIZE_DEFAULT)
    parser.add_argument("--only", default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    files, skipped_files = collect_markdown_files(
        max_size_bytes=args.max_size_bytes,
        only_path=args.only,
    )

    if not files:
        print("No markdown files found within size limit.")
        write_manifest([], [], skipped_files)
        return 0

    parts_meta = write_export_parts(files, args.max_size_bytes, args.branch)
    write_manifest(files, parts_meta, skipped_files)

    print("[exporter] Completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
