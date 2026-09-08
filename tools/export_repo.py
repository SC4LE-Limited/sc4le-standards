#!/usr/bin/env python3
"""
Concatenate text files from a repo into a single Markdown export with:
  - a directory tree
  - a table-of-contents with stable anchors
  - an inline JSON manifest (export-manifest.json) and a separate file export-manifest.json
  - per-file git blob SHA, last commit SHA/date/author
Usage:
  python tools/export_repo.py --root . --output export.md
"""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Extensions -> language hint for fenced code blocks
EXT_LANG = {
    '.py': 'python', '.md': 'markdown', '.js': 'javascript', '.ts': 'typescript',
    '.java': 'java', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.html': 'html',
    '.css': 'css', '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml',
    '.sh': 'bash', '.ps1': 'powershell', '.rb': 'ruby', '.go': 'go',
    '.rs': 'rust', '.pyi': 'python', '.txt': 'text'
}

DEFAULT_EXCLUDES = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.gradle'}


def slugify_anchor(path_str: str) -> str:
    # produce a stable anchor name for a path: lowercase, replace non-alnum with '-'
    s = path_str.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    if not s:
        s = 'file'
    return s


def is_binary(path: Path, max_bytes=1024):
    try:
        with path.open('rb') as f:
            chunk = f.read(max_bytes)
            if b'\0' in chunk:
                return True
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)))
            if bool(chunk) and sum(b not in text_chars for b in chunk) / max(1, len(chunk)) > 0.30:
                return True
    except Exception:
        return True
    return False


def run_git(args, cwd, silent=False):
    try:
        out = subprocess.check_output(['git'] + args, cwd=cwd, text=True).strip()
        return out
    except subprocess.CalledProcessError:
        if not silent:
            return None
        return None
    except Exception:
        return None


def git_head_sha(root: Path):
    return run_git(['rev-parse', 'HEAD'], root, silent=True)


def git_branch(root: Path):
    return run_git(['rev-parse', '--abbrev-ref', 'HEAD'], root, silent=True)


def git_remote_url(root: Path):
    return run_git(['remote', 'get-url', 'origin'], root, silent=True)


def git_describe_tag(root: Path):
    # try exact match then fallback
    tag = run_git(['describe', '--tags', '--exact-match', 'HEAD'], root, silent=True)
    if tag:
        return tag
    return run_git(['describe', '--tags', '--always'], root, silent=True)


def git_last_commit_for_file(root: Path, relpath: Path):
    out = run_git(['log', '-n', '1', '--pretty=format:%H|%cI|%an', '--', str(relpath)], root, silent=True)
    if out:
        parts = out.split('|', 2)
        if len(parts) == 3:
            sha, date_iso, author = parts
            return {'sha': sha, 'date': date_iso, 'author': author}
    return None


def git_ls_tree_blob_map(root: Path):
    # returns dict path -> blob_sha for HEAD
    out = run_git(['ls-tree', '-r', 'HEAD'], root, silent=True)
    mapping = {}
    if not out:
        return mapping
    for line in out.splitlines():
        # format: '<mode> <type> <sha>\t<path>'
        try:
            left, path = line.split('\t', 1)
            parts = left.split()
            if len(parts) >= 3:
                sha = parts[2]
                mapping[path] = sha
        except Exception:
            continue
    return mapping


def build_file_list(root: Path, excludes, max_size):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
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
                continue
            if is_binary(fpath):
                continue
            files.append((fpath, size))
    files.sort(key=lambda t: str(t[0].relative_to(root)))
    return files


def build_tree_lines(paths, root: Path):
    # Simple ASCII tree-like listing grouped by directories
    tree = {}
    for p, _ in paths:
        rel = p.relative_to(root)
        parts = rel.parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault(parts[-1], None)
    lines = []
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
    if not lines:
        return ["(empty)"]
    return lines


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.', help='Repo root to export')
    p.add_argument('--output', default='export.md', help='Output Markdown file')
    p.add_argument('--max-size', type=int, default=2_000_000, help='Skip files > bytes (default 2MB)')
    p.add_argument('--exclude', nargs='*', default=[], help='Additional paths to exclude')
    p.add_argument('--manifest-file', default='export-manifest.json', help='Write manifest JSON to this path')
    args = p.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.output).resolve()
    manifest_path = Path(args.manifest_file).resolve()
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)

    head = git_head_sha(root)
    branch = git_branch(root)
    remote = git_remote_url(root)
    head_tag = git_describe_tag(root)
    blob_map = git_ls_tree_blob_map(root)

    files = build_file_list(root, excludes, args.max_size)
    tree_lines = build_tree_lines(files, root)

    manifest = {
        "repo": root.name,
        "head": head,
        "branch": branch,
        "head_tag": head_tag,
        "remote": remote,
        "generated_at": datetime.utcnow().isoformat() + 'Z',
        "generated_by": 'tools/export_repo.py',
        "files": []
    }

    toc_lines = []
    for pth, size in files:
        rel = pth.relative_to(root)
        rel_str = str(rel)
        anchor = slugify_anchor(rel_str)
        ext = pth.suffix.lower()
        lang = EXT_LANG.get(ext, '')
        meta = git_last_commit_for_file(root, rel)
        blob_sha = blob_map.get(rel_str)
        file_entry = {
            "path": rel_str,
            "size": size,
            "language": lang or None,
            "anchor": anchor,
            "last_commit": meta['sha'] if meta else None,
            "last_commit_date": meta['date'] if meta else None,
            "last_commit_author": meta['author'] if meta else None,
            "blob_sha": blob_sha
        }
        manifest["files"].append(file_entry)
        toc_lines.append(f"- [{rel_str}](#{anchor})")

    # write manifest JSON file separately
    try:
        with manifest_path.open('w', encoding='utf-8') as mf:
            json.dump(manifest, mf, indent=2)
    except Exception:
        # ignore write errors; we'll embed manifest in export.md anyway
        pass

    with out_path.open('w', encoding='utf-8') as out:
        out.write(f"# Repository export: {root.name}\n\n")
        if head:
            out.write(f"- commit: `{head}`\n\n")
        if branch:
            out.write(f"- branch: `{branch}`\n\n")
        if head_tag:
            out.write(f"- tag: `{head_tag}`\n\n")
        if remote:
            out.write(f"- remote: `{remote}`\n\n")
        out.write(f"- generated_by: tools/export_repo.py\n")
        out.write(f"- generated_at: {manifest['generated_at']}\n\n")
        out.write("---\n\n")

        out.write("## Directory tree\n\n")
        out.write("```\n")
        for l in tree_lines:
            out.write(l + "\n")
        out.write("```\n\n")

        out.write("## Table of contents\n\n")
        if toc_lines:
            out.write("\n".join(toc_lines) + "\n\n")
        else:
            out.write("_No exported files_\n\n")

        out.write("---\n\n")
        out.write("## Files\n\n")

        # emit files with stable anchors
        for entry in manifest["files"]:
            rel = entry['path']
            anchor = entry['anchor']
            fpath = root / rel
            out.write(f"<a name=\"{anchor}\"></a>\n\n")
            out.write(f"### {rel}\n\n")
            out.write(f"- size: {entry['size']} bytes\n")
            if entry['last_commit']:
                out.write(f"- last_commit: `{entry['last_commit']}` ({entry['last_commit_date']}) by {entry['last_commit_author']}\n")
            if entry['blob_sha']:
                out.write(f"- blob_sha: `{entry['blob_sha']}`\n")
            if entry['language']:
                out.write(f"- language: {entry['language']}\n")
            out.write("\n")
            try:
                text = fpath.read_text(encoding='utf-8')
            except Exception:
                try:
                    text = fpath.read_text(encoding='latin-1')
                except Exception:
                    text = ''
            ext = fpath.suffix.lower()
            lang = entry['language'] or ''
            if lang:
                out.write(f"```{lang}\n")
                out.write(text.rstrip() + "\n")
                out.write("```\n\n")
            else:
                out.write("```\n")
                out.write(text.rstrip() + "\n")
                out.write("```\n\n")

        out.write("---\n\n")
        out.write("## Manifest (export-manifest.json)\n\n")
        out.write("```json\n")
        out.write(json.dumps(manifest, indent=2) + "\n")
        out.write("```\n\n")
    print(f"Export written to {out_path}")
