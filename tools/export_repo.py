```python
#!/usr/bin/env python3
"""
Concatenate text files from a repo into multiple Markdown export parts
with:
 - a directory tree (in the first part)
 - a global table-of-contents (in the first part)
 - a JSON manifest (export-manifest.json) written separately
 - per-file git blob SHA, last commit SHA/date/author
 - split into parts when part bytes exceed --part-size
 - optional sanitization to reduce "active code" signals (use --sanitize)

Usage:
  python tools/export_repo.py --root . --output export.md --part-size 1000000 --sanitize
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
    '.rs': 'rust', '.pyi': 'python', '.txt': 'text', '.svg': 'xml'
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
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
            if bool(chunk) and sum(b not in text_chars for b in chunk) / max(1, len(chunk)) > 0.30:
                return True
    except Exception:
        return True
    return False


def run_git(args, cwd, silent=False):
    try:
        out = subprocess.check_output(['git'] + args, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
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
    # try exact match then fallback, suppress stderr to avoid noisy logs
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


def safe_read_text(fpath: Path):
    try:
        return fpath.read_text(encoding='utf-8')
    except Exception:
        try:
            return fpath.read_text(encoding='latin-1')
        except Exception:
            return ''


def sanitize_content(text: str, relpath: str) -> str:
    """
    Reduce 'active code' signals that might trigger content-type blocking:
    - Remove YAML frontmatter
    - Redact workflow YAML files completely
    - Escape angle brackets to neutralize HTML/SVG
    - Replace code fences with a neutral marker
    - Replace lines that look like shell invocations with a placeholder
    """
    # If this looks like a GitHub workflow path, redact entirely
    if relpath.startswith('.github/workflows') or relpath.endswith('.workflow') or relpath.lower().endswith(('.yml', '.yaml')) and '.github/workflows' in relpath:
        return '[REDACTED: workflow file removed for upload safety]\n'

    # Remove YAML frontmatter at top (--- ... ---)
    text = re.sub(r'(?s)^\s*---\s*\n.*?\n---\s*\n', '[REDACTED YAML FRONTMATTER]\n', text)

    # Escape angle brackets to avoid embedded HTML/SVG being seen as active
    text = text.replace('<', '&lt;').replace('>', '&gt;')

    # Replace triple-backtick code fences with a neutral token
    text = text.replace('```', '[[CODE_BLOCK]]')

    # Replace suspicious shell lines ($ prompt, sudo)
    text = re.sub(r'(?m)^[ \t]*\$.*$', '[REDACTED COMMAND]\n', text)
    text = re.sub(r'(?m)^[ \t]*sudo\b.*$', '[REDACTED COMMAND]\n', text)

    # Replace common automation shebangs to reduce "executable" signal
    text = re.sub(r'(?m)^#!\/.*\b(sh|bash|python|env)\b.*$', '[REDACTED SHEBANG]\n', text)

    return text


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.', help='Repo root to export')
    p.add_argument('--output', default='export.md', help='Output base Markdown file')
    p.add_argument('--part-size', type=int, default=1_000_000, help='Max bytes per export part (default 1_000_000)')
    p.add_argument('--max-size', type=int, default=2_000_000, help='Skip files > bytes (default 2MB)')
    p.add_argument('--exclude', nargs='*', default=[], help='Additional paths to exclude')
    p.add_argument('--manifest-file', default='export-manifest.json', help='Write manifest JSON to this path')
    p.add_argument('--sanitize', action='store_true', help='Sanitize file contents for upload (redact code/HTML/workflows)')
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

    # Precompute file metadata and anchors so we can emit a global TOC (in first part)
    file_infos = []
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
            # will be filled during writing:
            "export_file": None,
            "sanitized": False
        })

    # Prepare TOC lines
    toc_lines = [f"- [{fi['path']}](#{fi['anchor']})" for fi in file_infos]

    # Helper to write text and count bytes (utf-8)
    def write_and_count(fhandle, s, counter):
        b = s.encode('utf-8')
        fhandle.write(s)
        return counter + len(b)

    # Generate part filenames: use output_base.stem and extension
    base_stem = output_base.stem
    base_suffix = output_base.suffix or '.md'

    def part_filename_for(index):
        return f"{base_stem}_{index:03}{base_suffix}"

    # Open first part
    part_index = 1
    part_path = root / part_filename_for(part_index)
    out = part_path.open('w', encoding='utf-8')
    current_bytes = 0
    parts_meta = []

    # write a common header to each part when opened
    def write_part_header(f, idx):
        nonlocal current_bytes
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
        current_bytes = write_and_count(f, header, current_bytes)
        # First part also gets directory tree and global TOC
        if idx == 1:
            tree_block = "## Directory tree\n\n```\n"
            for l in tree_lines:
                tree_block += l + "\n"
            tree_block += "```\n\n"
            current_bytes = write_and_count(f, tree_block, current_bytes)

            toc_block = "## Table of contents\n\n"
            if toc_lines:
                toc_block += "\n".join(toc_lines) + "\n\n"
            else:
                toc_block += "_No exported files_\n\n"
            current_bytes = write_and_count(f, toc_block, current_bytes)
            current_bytes = write_and_count(f, "---\n\n", current_bytes)
            current_bytes = write_and_count(f, "## Files\n\n", current_bytes)

    write_part_header(out, part_index)

    # Iterate entries and write to parts, splitting as needed.
    for fi in file_infos:
        rel = fi['path']
        anchor = fi['anchor']
        fpath = root / rel

        # Prepare the metadata and code fence markers
        meta_lines = []
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
            sanitized_text = sanitize_content(text, rel)
            text_to_write = sanitized_text
            fi['sanitized'] = True
        else:
            text_to_write = text
            fi['sanitized'] = False

        text_bytes_len = len(text_to_write.encode('utf-8'))
        ext = fpath.suffix.lower()
        lang = fi['language'] or ''

        if lang:
            fence_start = f"```{lang}\n"
            fence_end = "```\n\n"
        else:
            fence_start = "```\n"
            fence_end = "```\n\n"

        # Section total size estimate in bytes:
        meta_bytes = sum(len(s.encode('utf-8')) for s in meta_lines)
        fence_start_bytes = len(fence_start.encode('utf-8'))
        fence_end_bytes = len(fence_end.encode('utf-8'))
        section_bytes = meta_bytes + fence_start_bytes + text_bytes_len + fence_end_bytes

        # If adding this section would exceed part_size and current part already has content, rotate to next part
        if current_bytes + section_bytes > part_size and current_bytes > 0:
            # close current part and record meta
            out.close()
            parts_meta.append({
                "filename": str(part_path.relative_to(root)),
                "size": current_bytes
            })
            part_index += 1
            part_path = root / part_filename_for(part_index)
            out = part_path.open('w', encoding='utf-8')
            current_bytes = 0
            write_part_header(out, part_index)

        # Even if section_bytes > part_size and current_bytes == 0, we'll write it into this (new) part oversized.
        # Write meta lines
        for s in meta_lines:
            current_bytes = write_and_count(out, s, current_bytes)
        # Write fence and content
        current_bytes = write_and_count(out, fence_start, current_bytes)
        # write content in one call (text)
        current_bytes = write_and_count(out, text_to_write.rstrip() + "\n", current_bytes)
        current_bytes = write_and_count(out, fence_end, current_bytes)

        # record which export file contains the section
        fi['export_file'] = str(part_path.relative_to(root))

    # finalize last part
    out.close()
    parts_meta.append({
        "filename": str(part_path.relative_to(root)),
        "size": current_bytes
    })

    # Build manifest now that we know export_file for each entry
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
            "last_commit": fi['last_commit'],
            "last_commit_date": fi['last_commit_date'],
            "last_commit_author": fi['last_commit_author'],
            "blob_sha": fi['blob_sha'],
            "export_file": fi['export_file'],
            "sanitized": fi.get('sanitized', False)
        }
        manifest["files"].append(entry)

    # write manifest JSON file separately
    try:
        with manifest_path.open('w', encoding='utf-8') as mf:
            json.dump(manifest, mf, indent=2)
    except Exception:
        # ignore write errors
        pass

    print("Export parts written:")
    for pm in parts_meta:
        print(f" - {pm['filename']} ({pm['size']} bytes)")
    print(f"Manifest written to {manifest_path}")


if __name__ == '__main__':
    main()
```
