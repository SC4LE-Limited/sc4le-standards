#!/usr/bin/env python3
"""
Concatenate text files from a repo into a single Markdown export.

Usage:
  python tools/export_repo.py --root . --output export.md
"""
import argparse
import os
from pathlib import Path
import subprocess

# Extensions -> language hint for fenced code blocks
EXT_LANG = {
    '.py': 'python', '.md': 'markdown', '.js': 'javascript', '.ts': 'typescript',
    '.java': 'java', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.html': 'html',
    '.css': 'css', '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml',
    '.sh': 'bash', '.ps1': 'powershell', '.rb': 'ruby', '.go': 'go',
    '.rs': 'rust', '.pyi': 'python'
}

DEFAULT_EXCLUDES = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.gradle'}


def is_binary(path: Path, max_bytes=1024):
    try:
        with path.open('rb') as f:
            chunk = f.read(max_bytes)
            if b'\0' in chunk:
                return True
            # Heuristic: high non-text bytes
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)))
            if bool(chunk) and sum(b not in text_chars for b in chunk) / max(1, len(chunk)) > 0.30:
                return True
    except Exception:
        return True
    return False


def git_head_sha(root: Path):
    try:
        out = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        return out
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.', help='Repo root to export')
    p.add_argument('--output', default='export.md', help='Output Markdown file')
    p.add_argument('--max-size', type=int, default=2_000_000, help='Skip files > bytes (default 2MB)')
    p.add_argument('--exclude', nargs='*', default=[], help='Additional paths to exclude')
    args = p.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.output).resolve()
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)

    head = git_head_sha(root)

    with out_path.open('w', encoding='utf-8') as out:
        out.write(f"# Repository export: {root.name}\n\n")
        if head:
            out.write(f"- commit: `{head}`\n\n")
        out.write(f"- generated_by: tools/export_repo.py\n\n")
        out.write("---\n\n")

        for dirpath, dirnames, filenames in os.walk(root):
            # relative path from root
            rel_dir = Path(dirpath).relative_to(root)
            # Skip excluded dirs
            parts = set(rel_dir.parts)
            if parts & excludes:
                # prune by clearing filenames/dirnames to avoid walking deeper
                dirnames[:] = []
                continue

            # remove excluded subdirs from traversal
            dirnames[:] = [d for d in dirnames if d not in excludes and not d.startswith('.git')]

            for fname in filenames:
                fpath = Path(dirpath) / fname
                # Skip files in excluded folders or exact matches
                if any(p in fpath.parts for p in excludes):
                    continue
                # skip .git internals
                if '.git' in fpath.parts:
                    continue
                # file size guard
                try:
                    size = fpath.stat().st_size
                except Exception:
                    continue
                if size > args.max_size:
                    out.write(f"<!-- SKIP {fpath} (size {size} bytes) -->\n\n")
                    continue
                # skip binary
                if is_binary(fpath):
                    out.write(f"<!-- SKIP BINARY {fpath} -->\n\n")
                    continue

                # read text with fallback
                try:
                    text = fpath.read_text(encoding='utf-8')
                except Exception:
                    try:
                        text = fpath.read_text(encoding='latin-1')
                    except Exception:
                        text = ''

                rel = fpath.relative_to(root)
                ext = fpath.suffix.lower()
                lang = EXT_LANG.get(ext, '')
                out.write(f"## {rel}\n\n")
                out.write(f"<!-- size: {size} bytes -->\n\n")
                if lang:
                    out.write(f"```{lang}\n")
                    out.write(text.rstrip() + "\n")
                    out.write("```\n\n")
                else:
                    # put as plain text block
                    out.write("```\n")
                    out.write(text.rstrip() + "\n")
                    out.write("```\n\n")
    print(f"Export written to {out_path}")


if __name__ == '__main__':
    main()
