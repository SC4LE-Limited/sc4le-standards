#!/usr/bin/env python3
"""
Concatenate text files from a repo into multiple Markdown export parts.

Produces export_001.md, export_002.md, ... and export-manifest.json.

Key behavior:
- Excludes common build/vendor dirs.
- Skips binary files and files larger than --max-size.
- Writes Markdown file contents verbatim (no triple-backtick fencing).
- Writes non-markdown code files inside fenced blocks with a language hint.
- Optional light sanitization with --sanitize to neutralize obvious active signals.

Usage:
  python3 tools/export_repo.py --root . --output export.md --manifest-file export-manifest.json
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Extensions -> language hint for fenced code blocks
EXT_LANG: Dict[str, str] = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
    '.java': 'java', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.html': 'html',
    '.css': 'css', '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml',
    '.sh': 'bash', '.ps1': 'powershell', '.rb': 'ruby', '.go': 'go',
    '.rs': 'rust', '.pyi': 'python', '.txt': 'text', '.svg': 'xml',
    '.md': 'markdown', '.markdown': 'markdown'
}

DEFAULT_EXCLUDES = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.gradle'}


def slugify_anchor(path_str: str) -> str:
    s = path_str.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s or 'file'


def is_binary(path: Path, max_bytes: int = 1024) -> bool:
    try:
        with path.open('rb') as f:
            chunk = f.read(max_bytes)
            if b'\0' in chunk:
                return True
            # heuristic: if >30% of bytes are non-text-like, treat as binary
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
            if chunk and sum(b not in text_chars for b in chunk) / max(1, len(chunk)) > 0.30:
                return True
    except Exception:
        # on error, be conservative and treat as binary
        return True
    return False


def run_git(args: List[str], cwd: Path, silent: bool = False) -> Optional[str]:
    try:
        out = subprocess.check_output(['git'] + args, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
        return out
    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None


def git_head_sha(root: Path) -> Optional[str]:
    return run_git(['rev-parse', 'HEAD'], root, silent=True)


def git_branch(root: Path) -> Optional[str]:
    return run_git(['rev-parse', '--abbrev-ref', 'HEAD'], root, silent=True)


def git_remote_url(root: Path) -> Optional[str]:
    return run_git(['remote', 'get-url', 'origin'], root, silent=True)


def git_describe_tag(root: Path) -> Optional[str]:
    tag = run_git(['describe', '--tags', '--exact-match', 'HEAD'], root, silent=True)
    if tag:
        return tag
    return run_git(['describe', '--tags', '--always'], root, silent=True)


def git_last_commit_for_file(root: Path, relpath: Path) -> Optional[Dict[str, str]]:
    out = run_git(['log', '-n', '1', '--pretty=format:%H|%cI|%an', '--', str(relpath)], root, silent=True)
    if out:
        parts = out.split('|', 2)
        if len(parts) == 3:
            sha, date_iso, author = parts
            return {'sha': sha, 'date': date_iso, 'author': author}
    return None


def git_ls_tree_blob_map(root: Path) -> Dict[str, str]:
    out = run_git(['ls-tree', '-r', 'HEAD'], root, silent=True)
    mapping: Dict[str, str] = {}
    if not out:
        return mapping
    for line in out.splitlines():
        try:
            left, path = line.split('\t', 1)
            parts = left.split()
            if len(parts) >= 3:
                sha = parts[2]
                mapping[path] = sha
        except Exception:
            continue
    return mapping


def build_file_list(root: Path, excludes: set, max_size: int) -> List[Tuple[Path, int]]:
    files: List[Tuple[Path, int]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip excluded directories early
        rel_dir = Path(dirpath).relative_to(root)
        parts = set(rel_dir.parts) if rel_dir.parts else set()
        if parts & excludes:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in excludes and not d.startswith('.git')]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if any(p in fpath.parts for p in excludes):
                continue
            if '.git' in fpath.parts:
                continue
            try:
                size = fpath.stat().st_size
            except Exception:
                continue
            if size > max_size:
                # skip overly large files (keeps exports manageable)
                continue
            if is_binary(fpath):
                continue
            files.append((fpath, size))
    files.sort(key=lambda t: str(t[0].relative_to(root)))
    return files


def build_tree_lines(paths: List[Tuple[Path, int]], root: Path) -> List[str]:
    tree = {}
    for p, _ in paths:
        rel = p.relative_to(root)
        parts = rel.parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault(parts[-1], None)
    lines: List[str] = []

    def walk(node, prefix=''):
        entries = sorted(node.items(), key=lambda kv: (kv[1] is None, kv[0]))
        for i, (name, child) in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = '└─ ' if is_last else '├─ '
            lines.append(prefix + connector + name)
            if child is not None:
                new_prefix = prefix + ('   ' if is_last else '│  ')
                walk(child, new_prefix)

    walk(tree)
    return lines or ["(empty)"]


def safe_read_text(fpath: Path) -> str:
    try:
        return fpath.read_text(encoding='utf-8')
    except Exception:
        try:
            return fpath.read_text(encoding='latin-1')
        except Exception:
            return ''


def sanitize_content(text: str, relpath: str) -> str:
    """
    Light sanitization used only if --sanitize is passed.
    This should not remove prose. It neutralizes risky signals that commonly trigger filters.
    """
    # Redact workflow files outright if they live under .github/workflows
    if relpath.startswith('.github/workflows') or relpath.endswith('.workflow') or (relpath.lower().endswith(('.yml', '.yaml')) and '.github/workflows' in relpath):
        return '[REDACTED: workflow file removed for upload safety]\n'

    # Remove YAML frontmatter at top (--- ... ---)
    text = re.sub(r'(?s)^\s*---\s*\n.*?\n---\s*\n', '[REDACTED YAML FRONTMATTER]\n', text)

    # Escape angle brackets to avoid embedded HTML/SVG being seen as active
    text = text.replace('<', '&lt;').replace('>', '&gt;')

    # Replace triple-backtick code fences with a neutral token to reduce "executable" signal
    text = text.replace('```', '[[CODE_BLOCK]]')

    # Replace suspicious shell lines ($ prompt, sudo)
    text = re.sub(r'(?m)^[ \t]*\$.*$', '[REDACTED COMMAND]\n', text)
    text = re.sub(r'(?m)^[ \t]*sudo\b.*$', '[REDACTED COMMAND]\n', text)

    # Replace common automation shebangs
    text = re.sub(r'(?m)^#!\/.*\b(sh|bash|python|env)\b.*$', '[REDACTED SHEBANG]\n', text)

    # Redact long hex/base64 tokens inline
    text = re.sub(r'\b[0-9a-fA-F]{16,}\b', '[REDACTED_HEX]', text)
    text = re.sub(r'\b[A-Za-z0-9+/]{40,}={0,2}\b', '[REDACTED_BLOB]', text)

    return text


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.', help='Repo root to export')
    p.add_argument('--output', default='export.md', help='Output base Markdown file')
    p.add_argument('--part-size', type=int, default=1_000_000, help='Max bytes per export part')
    p.add_argument('--max-size', type=int, default=2_000_000, help='Skip files > bytes (default 2MB)')
    p.add_argument('--exclude', nargs='*', default=[], help='Additional paths to exclude')
    p.add_argument('--manifest-file', default='export-manifest.json', help='Write manifest JSON to this path')
    p.add_argument('--sanitize', action='store_true', help='Sanitize file contents for upload (light)')
    args = p.parse_args()

    root = Path(args.root).resolve()
    output_base = Path(args.output).resolve()
    manifest_path = Path(args.manifest_file).resolve()
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)
    part_size = args.part_size
    max_size = args.max_size

    head = git_head_sha(root)
    branch = git_branch(root)
    remote = git_remote_url(root)
    head_tag = git_describe_tag(root)
    blob_map = git_ls_tree_blob_map(root)

    files = build_file_list(root, excludes, max_size)
    tree_lines = build_tree_lines(files, root)

    file_infos: List[Dict] = []
    for pth, size in files:
        rel = pth.relative_to(root)
        rel_str = str(rel)
        anchor = slugify_anchor(rel_str)
        ext = pth.suffix.lower()
        lang = EXT_LANG.get(ext, '')
        meta = git_last_commit_for_file(root, rel)
        blob_sha = blob_map.get(rel_str)
        file_infos.append({
            "path": rel_str,
            "size": size,
            "language": lang or None,
            "anchor": anchor,
            "last_commit": meta['sha'] if meta else None,
            "last_commit_date": meta['date'] if meta else None,
            "last_commit_author": meta['author'] if meta else None,
            "blob_sha": blob_sha,
            "export_file": None,
            "sanitized": False
        })

    toc_lines = [f"- [{fi['path']}](#{fi['anchor']})" for fi in file_infos]

    def write_and_count(fhandle, s: str, counter: int) -> int:
        b = s.encode('utf-8')
        fhandle.write(s)
        return counter + len(b)

    base_stem = output_base.stem
    base_suffix = output_base.suffix or '.md'

    def part_filename_for(index: int) -> str:
        return f"{base_stem}_{index:03}{base_suffix}"

    part_index = 1
    part_path = root / part_filename_for(part_index)
    out = part_path.open('w', encoding='utf-8')
    current_bytes = 0
    parts_meta: List[Dict] = []

    def write_part_header(f, idx: int, counter: int) -> int:
        header = f"# Repository export: {root.name} (part {idx})\n\n"
        if head:
            header += f"- commit: `{head}`\n\n"
        if branch:
            header += f"- branch: `{branch}`\n\n"
        if head_tag:
            header += f"- tag: `{head_tag}`\n\n"
        if remote:
            header += f"- remote: `{remote}`\n\n"
        header += f"- generated_by: tools/export_repo.py\n"
        header += f"- generated_at: {datetime.utcnow().isoformat()}Z\n\n"
        header += "---\n\n"
        counter = write_and_count(f, header, counter)
        if idx == 1:
            tree_block = "## Directory tree\n\n```\n"
            for l in tree_lines:
                tree_block += l + "\n"
            tree_block += "```\n\n"
            counter = write_and_count(f, tree_block, counter)

            toc_block = "## Table of contents\n\n"
            if toc_lines:
                toc_block += "\n".join(toc_lines) + "\n\n"
            else:
                toc_block += "_No exported files_\n\n"
            counter = write_and_count(f, toc_block, counter)
            counter = write_and_count(f, "---\n\n", counter)
            counter = write_and_count(f, "## Files\n\n", counter)
        return counter

    current_bytes = write_part_header(out, part_index, current_bytes)

    for fi in file_infos:
        rel = fi['path']
        anchor = fi['anchor']
        fpath = root / rel

        meta_lines: List[str] = []
        meta_lines.append(f"<a name=\"{anchor}\"></a>\n\n")
        meta_lines.append(f"### {rel}\n\n")
        meta_lines.append(f"- size: {fi['size']} bytes\n")
        if fi['last_commit']:
            meta_lines.append(f"- last_commit: `{fi['last_commit']}` ({fi['last_commit_date']}) by {fi['last_commit_author']}\n")
        if fi['blob_sha']:
            meta_lines.append(f"- blob_sha: `{fi['blob_sha']}`\n")
        if fi['language']:
            meta_lines.append(f"- language: {fi['language']}\n")
        meta_lines.append("\n")

        text = safe_read_text(fpath)
        if args.sanitize:
            text_to_write = sanitize_content(text, rel)
            fi['sanitized'] = True
        else:
            text_to_write = text
            fi['sanitized'] = False

        text_bytes_len = len(text_to_write.encode('utf-8'))
        ext = fpath.suffix.lower()
        lang = fi['language'] or ''

        # For Markdown files we do NOT wrap the content in fenced code blocks.
        # For other languages we keep fenced blocks (so code remains distinguishable).
        is_markdown = (lang == 'markdown' or ext in ('.md', '.markdown'))

        if not is_markdown and lang:
            fence_start = f"```{lang}\n"
            fence_end = "```\n\n"
        else:
            # No fences for markdown / plain-text - write raw text (with two newlines after)
            fence_start = ""
            fence_end = "\n\n"

        meta_bytes = sum(len(s.encode('utf-8')) for s in meta_lines)
        fence_start_bytes = len(fence_start.encode('utf-8'))
        fence_end_bytes = len(fence_end.encode('utf-8'))
        section_bytes = meta_bytes + fence_start_bytes + text_bytes_len + fence_end_bytes

        # If adding this file would exceed current part size, rotate to next part
        if current_bytes + section_bytes > part_size and current_bytes > 0:
            out.close()
            parts_meta.append({
                "filename": str(part_path.relative_to(root)),
                "size": current_bytes
            })
            part_index += 1
            part_path = root / part_filename_for(part_index)
            out = part_path.open('w', encoding='utf-8')
            current_bytes = 0
            current_bytes = write_part_header(out, part_index, current_bytes)

        # Write metadata lines
        for s in meta_lines:
            current_bytes = write_and_count(out, s, current_bytes)

        # Write either fenced code block (for code files) or raw markdown text
        if fence_start:
            current_bytes = write_and_count(out, fence_start, current_bytes)
            current_bytes = write_and_count(out, text_to_write.rstrip() + "\n", current_bytes)
            current_bytes = write_and_count(out, fence_end, current_bytes)
        else:
            # markdown/plain text: write as-is (escaped/sanitized earlier if requested)
            # ensure there is a blank line after the file content
            current_bytes = write_and_count(out, text_to_write.rstrip() + "\n\n", current_bytes)

        fi['export_file'] = str(part_path.relative_to(root))

    out.close()
    parts_meta.append({
        "filename": str(part_path.relative_to(root)),
        "size": current_bytes
    })

    manifest = {
        "repo": root.name,
        "head": head,
        "branch": branch,
        "head_tag": head_tag,
        "remote": remote,
        "generated_at": datetime.utcnow().isoformat() + 'Z',
        "generated_by": 'tools/export_repo.py',
        "part_size": part_size,
        "parts": parts_meta,
        "files": []
    }

    for fi in file_infos:
        entry = {
            "path": fi['path'],
            "size": fi['size'],
            "language": fi['language'],
            "anchor": fi['anchor'],
            "last_commit': fi.get('last_commit') if isinstance(fi.get('last_commit'), str) else fi.get('last_commit'),
            "last_commit_date": fi.get('last_commit_date'),
            "last_commit_author": fi.get('last_commit_author'),
            "blob_sha": fi['blob_sha'],
            "export_file": fi['export_file'],
            "sanitized": fi.get('sanitized', False)
        }
        manifest["files"].append(entry)

    try:
        with manifest_path.open('w', encoding='utf-8') as mf:
            json.dump(manifest, mf, indent=2)
    except Exception:
        pass

    print("Export parts written:")
    for pm in parts_meta:
        print(f" - {pm['filename']} ({pm['size']} bytes)")
    print(f"Manifest written to {manifest_path}")


if __name__ == '__main__':
    main()
