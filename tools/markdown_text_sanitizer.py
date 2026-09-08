#!/usr/bin/env python3
"""
Preserve written text content of export_*.md while removing safety triggers.

Usage:
  python3 tools/markdown_text_sanitizer.py         # sanitizes all export_*.md
  python3 tools/markdown_text_sanitizer.py export_001.md
Outputs:
  export_001_sanitized.md, ... and export-manifest-sanitized.json
"""
import re
import sys
import json
from pathlib import Path
from html import escape as html_escape
import argparse

# Regexes
YAML_FRONT_RE = re.compile(r'(?s)^\s*---\s*\n.*?\n---\s*\n')
HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
SVG_RE = re.compile(r'(?is)<svg\b.*?>.*?</svg>')
FENCE_RE = re.compile(r'(^```[^\n]*\n)(.*?)(^```$)', re.M | re.S)
TAG_RE = re.compile(r'</?[^>]+>')
DATA_URI_RE = re.compile(r'data:[A-Za-z0-9\-/\.]+;base64,[A-Za-z0-9+/=]+')
LONG_HEX_RE = re.compile(r'\b[0-9a-fA-F]{16,}\b')
BASE64_LONG_RE = re.compile(r'\b[A-Za-z0-9+/]{40,}={0,2}\b')
BLOB_METADATA_RE = re.compile(r'(?m)^\s*-\s*(blob_sha|last_commit|last_commit_date)\b.*$', re.I)
SHELL_PROMPT_RE = re.compile(r'(?m)^[ \t]*\$.*$')
SUDO_RE = re.compile(r'(?m)^[ \t]*sudo\b.*$')

def redact_long_tokens(s: str) -> str:
    s = LONG_HEX_RE.sub('[REDACTED_HEX]', s)
    s = BASE64_LONG_RE.sub('[REDACTED_BLOB]', s)
    return s

def svg_to_preview(m):
    svg = m.group(0)
    # strip tags and compress whitespace to make a short preview of any text content
    inner = TAG_RE.sub(' ', svg)
    preview = ' '.join(inner.split())[:400]
    if preview:
        preview = html_escape(preview)
        return f"[SVG removed for safety — preview: {preview}]\n"
    # otherwise show a small escaped raw snippet
    snippet = html_escape(svg.strip()[:300])
    return f"[SVG removed for safety — snippet: {snippet}]\n"

def replace_code_block(m):
    start = m.group(1).rstrip('\n')  # e.g. ```python
    lang = start[3:].strip() if len(start) > 3 else ''
    body = m.group(2)
    line_count = len(body.splitlines())
    lang_label = lang if lang else "unknown"
    return f"[REDACTED CODE BLOCK: language={lang_label}, {line_count} lines removed]\n\n"

def sanitize_text(text: str) -> str:
    # Remove YAML frontmatter
    text = YAML_FRONT_RE.sub('[REDACTED YAML FRONTMATTER]\n', text)

    # Remove HTML comments
    text = HTML_COMMENT_RE.sub('', text)

    # Replace SVG blocks with short preview (keeps readable text if present)
    text = SVG_RE.sub(svg_to_preview, text)

    # Replace fenced code blocks with placeholders (remove code bodies)
    text = FENCE_RE.sub(lambda m: replace_code_block(m), text)

    # Neutralize data URIs (images embedded inline)
    text = DATA_URI_RE.sub('[REDACTED_DATA_URI]', text)

    # Remove blob/commit metadata lines entirely
    text = BLOB_METADATA_RE.sub('', text)

    # Redact shell prompt lines and sudo usages
    text = SHELL_PROMPT_RE.sub('[REDACTED COMMAND]', text)
    text = SUDO_RE.sub('[REDACTED COMMAND]', text)

    # Remove/strip remaining HTML tags but keep inner text
    text = TAG_RE.sub('', text)

    # Redact long hex/base64 tokens
    text = redact_long_tokens(text)

    # Collapse excessive blank lines to keep file size reasonable
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text

def sanitize_file(src: Path, dst: Path):
    txt = src.read_text(encoding='utf-8', errors='ignore')
    sanitized = sanitize_text(txt)
    dst.write_text(sanitized, encoding='utf-8')
    print(f"Wrote {dst} ({len(sanitized.encode('utf-8'))} bytes)")

def sanitize_manifest(manifest_path: Path, out_path: Path):
    try:
        m = json.load(manifest_path.open('r', encoding='utf-8'))
    except Exception as e:
        print("manifest read error:", e, file=sys.stderr)
        return
    for f in m.get('files', []):
        f.pop('blob_sha', None)
        f.pop('last_commit', None)
        f.pop('last_commit_date', None)
    json.dump(m, out_path.open('w', encoding='utf-8'), indent=2)
    print(f"Wrote sanitized manifest {out_path}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='*', help='Files to sanitize (default: export_*.md)')
    args = p.parse_args()

    files = [Path(x) for x in args.files] if args.files else sorted(Path('.').glob('export_*.md'))
    if not files:
        print("No export_*.md files found.")
        sys.exit(1)

    for f in files:
        out = f.with_name(f.stem + '_sanitized' + f.suffix)
        sanitize_file(f, out)

    # sanitize manifest if present
    mpath = Path('export-manifest.json')
    if mpath.exists():
        sanitize_manifest(mpath, Path('export-manifest-sanitized.json'))

if __name__ == '__main__':
    main()
