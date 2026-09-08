#!/usr/bin/env python3
"""
Preserve and sanitize export parts:
 - keep headings/metadata
 - redact long hex/base64 and blob_sha
 - truncate code block bodies but keep first N lines (default 8)
 - remove/replace raw <svg>...</svg> blocks with a short preview placeholder
 - escape angle brackets outside code blocks
Outputs: export_<NNN>_preserved.md
Usage:
  python3 tools/preserve_and_sanitize.py
  python3 tools/preserve_and_sanitize.py --keep-code-lines 12 export_001.md
"""
import re
import sys
import argparse
from pathlib import Path
from html import escape as html_escape

# Regexes
YAML_FRONT_RE = re.compile(r'(?s)^\s*---\s*\n.*?\n---\s*\n')
BLOB_SHA_LINE_RE = re.compile(r'(?m)^\s*-\s*blob_sha:.*$', re.I)
LONG_HEX_RE = re.compile(r'\b[0-9a-fA-F]{16,}\b')
BASE64_RE = re.compile(r'\b[A-Za-z0-9+/]{40,}={0,2}\b')
FENCE_RE = re.compile(r'(^```[^\n]*\n)(.*?)(^```$)', re.M | re.S)
SVG_RE = re.compile(r'(<svg\b.*?>)(.*?)(</svg>)', re.I | re.S)
ANGLE_RE = re.compile(r'[<>]')

def redact_long_tokens(s: str) -> str:
    s = LONG_HEX_RE.sub('[REDACTED_HEX]', s)
    s = BASE64_RE.sub('[REDACTED_BLOB]', s)
    return s

def process_code_block(m, keep_lines: int):
    start = m.group(1)  # includes opening fence and language, ends with newline
    body = m.group(2)
    # Normalize line endings
    lines = body.splitlines()
    kept = lines[:keep_lines]
    removed = max(0, len(lines) - keep_lines)
    # redact long tokens inside the kept lines
    kept_text = '\n'.join(redact_long_tokens(l) for l in kept)
    if removed:
        kept_text += '\n' + f'[... {removed} lines omitted ...]\n'
    return start + kept_text + '\n```\n'

def replace_svg(m):
    open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
    # extract a small text preview from inside the SVG (strip tags)
    preview = re.sub(r'<[^>]+>', ' ', inner).strip()
    preview = ' '.join(preview.split())[:200]
    if preview:
        preview = html_escape(preview)
        return f'[SVG content omitted for upload safety — preview: {preview}]\n'
    return '[SVG content omitted for upload safety]\n'

def sanitize_text(text: str, keep_code_lines: int) -> str:
    # Remove YAML frontmatter
    text = YAML_FRONT_RE.sub('[REDACTED YAML FRONTMATTER]\n', text)

    # Remove whole blob_sha lines (they're better kept out of uploaded manifest)
    text = BLOB_SHA_LINE_RE.sub('[REDACTED blob_sha]', text)

    # Redact very long tokens anywhere first
    text = redact_long_tokens(text)

    # Replace SVG blocks with short preview placeholders
    text = SVG_RE.sub(replace_svg, text)

    # Process fenced code blocks: keep first N lines only
    def fence_repl(m):
        return process_code_block(m, keep_code_lines)
    text = FENCE_RE.sub(fence_repl, text)

    # Escape any remaining angle brackets to neutralize HTML outside code blocks
    text = ANGLE_RE.sub(lambda m: '&lt;' if m.group(0) == '<' else '&gt;', text)

    # Final pass to ensure no long tokens remain
    text = redact_long_tokens(text)

    return text

def process_file(src: Path, keep_code_lines: int):
    txt = src.read_text(encoding='utf-8', errors='ignore')
    preserved = sanitize_text(txt, keep_code_lines)
    out = src.with_name(src.stem + '_preserved' + src.suffix)
    out.write_text(preserved, encoding='utf-8')
    print(f'Wrote {out.name} ({len(preserved.encode("utf-8"))} bytes)')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='*', help='Files to process (default: export_*.md)')
    p.add_argument('--keep-code-lines', type=int, default=8, help='Keep first N lines of code block bodies')
    args = p.parse_args()

    if args.files:
        files = [Path(f) for f in args.files]
    else:
        files = sorted(Path('.').glob('export_*.md'))

    if not files:
        print('No export_*.md files found.')
        sys.exit(1)

    for f in files:
        process_file(f, args.keep_code_lines)

if __name__ == '__main__':
    main()
