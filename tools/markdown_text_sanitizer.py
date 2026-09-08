#!/usr/bin/env python3
"""
Sanitize markdown exports while preserving human-written text.
- Preserves the "## Directory tree" code block content (escapes <, > and redacts long tokens inside).
- Replaces other fenced code blocks by keeping the first N lines (default 8) and inserting a placeholder.
- Removes YAML frontmatter, HTML comments, data: URIs.
- Replaces <svg>...</svg> with a short preview (keeps textual content if present).
- Redacts long hex/base64 tokens and blob/commit metadata lines.
Outputs: export_<NNN>_sanitized.md and export-manifest-sanitized.json
"""
import re
import sys
import json
import argparse
from pathlib import Path
from html import escape as html_escape

# Config
KEEP_CODE_LINES = 8  # number of lines to keep in non-directory-tree code blocks

# Regexes
YAML_FRONT_RE = re.compile(r'(?s)^\s*---\s*\n.*?\n---\s*\n')
HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
SVG_RE = re.compile(r'(?is)<svg\b.*?>.*?</svg>')
DATA_URI_RE = re.compile(r'data:[A-Za-z0-9\-/\.]+;base64,[A-Za-z0-9+/=]+')
LONG_HEX_RE = re.compile(r'\b[0-9a-fA-F]{16,}\b')
BASE64_LONG_RE = re.compile(r'\b[A-Za-z0-9+/]{40,}={0,2}\b')
BLOB_METADATA_RE = re.compile(r'(?m)^\s*-\s*(blob_sha|last_commit|last_commit_date)\b.*$', re.I)
SHELL_PROMPT_RE = re.compile(r'(?m)^[ \t]*\$.*$')
SUDO_RE = re.compile(r'(?m)^[ \t]*sudo\b.*$')
TAG_RE = re.compile(r'</?[^>]+>')
FENCE_START_RE = re.compile(r'^(```+)(.*)$')  # captures backticks and optional language
SVG_TAG_TEXT_RE = re.compile(r'<[^>]+>')

def redact_long_tokens(s: str) -> str:
    s = LONG_HEX_RE.sub('[REDACTED_HEX]', s)
    s = BASE64_LONG_RE.sub('[REDACTED_BLOB]', s)
    return s

def svg_to_preview(m):
    svg = m.group(0)
    # extract visible text by stripping tags
    inner_text = SVG_TAG_TEXT_RE.sub(' ', svg)
    preview = ' '.join(inner_text.split())[:400]
    if preview:
        preview = html_escape(preview)
        return f"[SVG removed — preview: {preview}]\n"
    snippet = html_escape(svg.strip()[:300])
    return f"[SVG removed — snippet: {snippet}]\n"

def process_file(src: Path, keep_code_lines: int):
    txt = src.read_text(encoding='utf-8', errors='ignore')

    # Remove YAML frontmatter and HTML comments early
    txt = YAML_FRONT_RE.sub('[REDACTED YAML FRONTMATTER]\n', txt)
    txt = HTML_COMMENT_RE.sub('', txt)

    # Replace data URIs and SVGs
    txt = DATA_URI_RE.sub('[REDACTED_DATA_URI]', txt)
    txt = SVG_RE.sub(svg_to_preview, txt)

    # Remove blob metadata lines and redact shell prompts
    txt = BLOB_METADATA_RE.sub('', txt)
    txt = SHELL_PROMPT_RE.sub('[REDACTED COMMAND]', txt)
    txt = SUDO_RE.sub('[REDACTED COMMAND]', txt)

    # Redact very long tokens now to reduce their chance of appearing in preserved blocks
    txt = redact_long_tokens(txt)

    # Now process line-by-line to handle fenced code blocks with contextual preservation
    out_lines = []
    lines = txt.splitlines()
    in_fence = False
    fence_delim = None
    fence_lang = ''
    fence_buffer = []
    last_heading = ''  # most recent heading text (lowercase)
    i = 0
    while i < len(lines):
        line = lines[i]
        # detect headings
        h = re.match(r'^\s{0,3}(#{1,6})\s*(.+?)\s*$', line)
        if not in_fence and h:
            last_heading = h.group(2).strip().lower()
            out_lines.append(line)
            i += 1
            continue

        # detect fence start
        m = FENCE_START_RE.match(line)
        if m and not in_fence:
            in_fence = True
            fence_delim = m.group(1)
            fence_lang = m.group(2).strip()
            fence_buffer = []
            # include the opening fence line (we will re-add or replace later)
            i += 1
            # collect fence body
            while i < len(lines):
                l = lines[i]
                if l.strip().startswith(fence_delim):
                    # fence end found
                    in_fence = False
                    i += 1
                    break
                fence_buffer.append(lines[i])
                i += 1
            # decide how to handle this code block
            # if previous heading is "directory tree" (or contains it), preserve the entire fence buffer
            if 'directory tree' in last_heading:
                # preserve but sanitize inside (escape < > and redact long tokens)
                preserved = []
                for fb in fence_buffer:
                    fb2 = fb.replace('<', '&lt;').replace('>', '&gt;')
                    fb2 = redact_long_tokens(fb2)
                    preserved.append(fb2)
                out_lines.append(fence_delim + (('' + fence_lang) if fence_lang else ''))
                out_lines.extend(preserved)
                out_lines.append(fence_delim)
            else:
                # for other code blocks, keep first N lines (if any) and insert a placeholder
                kept = fence_buffer[:keep_code_lines]
                kept = [redact_long_tokens(l) for l in kept]
                if kept:
                    out_lines.append(fence_delim + (('' + fence_lang) if fence_lang else ''))
                    out_lines.extend(kept)
                    out_lines.append(fence_delim)
                # add a human readable placeholder indicating removal
                removed = max(0, len(fence_buffer) - len(kept))
                if removed > 0:
                    lang_label = fence_lang if fence_lang else 'unknown'
                    out_lines.append(f"[REDACTED CODE BLOCK: language={lang_label}, {removed} lines removed]\n")
            continue

        # normal line outside fences
        # strip any remaining HTML tags but keep inner text
        clean = TAG_RE.sub('', line)
        clean = redact_long_tokens(clean)
        out_lines.append(clean)
        i += 1

    out_text = '\n'.join(out_lines).rstrip() + '\n'

    dst = src.with_name(src.stem + '_sanitized' + src.suffix)
    dst.write_text(out_text, encoding='utf-8')
    print(f"Wrote {dst.name} ({len(out_text.encode('utf-8'))} bytes)")

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
    print(f"Wrote sanitized manifest {out_path.name}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='*', help='Files to sanitize (default: export_*.md)')
    p.add_argument('--keep-code-lines', type=int, default=KEEP_CODE_LINES, help='Keep first N lines of non-directory code blocks')
    args = p.parse_args()

    files = [Path(x) for x in args.files] if args.files else sorted(Path('.').glob('export_*.md'))
    if not files:
        print("No export_*.md files found.")
        sys.exit(0)

    for f in files:
        process_file(f, args.keep_code_lines)

    # sanitize manifest if present
    mpath = Path('export-manifest.json')
    if mpath.exists():
        sanitize_manifest(mpath, Path('export-manifest-sanitized.json'))

if __name__ == '__main__':
    main()
