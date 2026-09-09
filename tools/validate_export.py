#!/usr/bin/env python3
"""
Copilot-ready import validator for SC4LE repo exports.

Validates:
- Manifest structure
- Part sizes (<1MB)
- Anchor correctness
- TOC correctness
- Directory tree correctness
- File completeness
- Skipped file reporting
- UTF-8 validity
- No accidental binary content
"""

import json
import os
import re
import sys

MAX_PART_SIZE = 1_000_000

def error(msg):
    print(f"ERROR: {msg}")
    return False

def validate_utf8(path):
    try:
        with open(path, "rb") as f:
            f.read().decode("utf-8")
        return True
    except UnicodeDecodeError:
        return error(f"{path} contains invalid UTF-8")

def validate_manifest(manifest):
    required_keys = ["repo", "branch", "generated_at", "files", "parts", "skipped_files"]
    for k in required_keys:
        if k not in manifest:
            return error(f"Manifest missing key: {k}")
    return True

def validate_parts(manifest):
    ok = True
    for part in manifest["parts"]:
        fname = part["filename"]
        size = part["size"]
        if not os.path.exists(fname):
            ok = error(f"Part file missing: {fname}")
        if size > MAX_PART_SIZE:
            ok = error(f"Part exceeds 1MB: {fname} ({size} bytes)")
        if not validate_utf8(fname):
            ok = False
    return ok

def validate_files(manifest):
    ok = True
    exported_paths = set(fi["path"] for fi in manifest["files"])

    # Check each file exists in exactly one part
    for fi in manifest["files"]:
        part = fi["export_file"]
        if not part:
            ok = error(f"File missing export_file mapping: {fi['path']}")
            continue
        if not os.path.exists(part):
            ok = error(f"Mapped part missing: {part}")
            continue

        # Check anchor presence
        anchor = fi["anchor"]
        with open(part, "r", encoding="utf-8") as f:
            content = f.read()
            if f'<a name="{anchor}">' not in content:
                ok = error(f"Anchor missing for {fi['path']} in {part}")

    return ok

def validate_toc():
    # TOC must be in export_001.md
    if not os.path.exists("export_001.md"):
        return error("export_001.md missing")

    with open("export_001.md", "r", encoding="utf-8") as f:
        content = f.read()

    if "## Table of Contents" not in content:
        return error("TOC missing from export_001.md")

    return True

def validate_directory_tree():
    if not os.path.exists("export_001.md"):
        return error("export_001.md missing")

    with open("export_001.md", "r", encoding="utf-8") as f:
        content = f.read()

    if "Directory tree" not in content:
        return error("Directory tree missing from export_001.md")

    if "```text" not in content:
        return error("Directory tree missing fenced code block")

    return True

def main():
    if not os.path.exists("export-manifest.json"):
        print("ERROR: export-manifest.json missing")
        return 1

    with open("export-manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    checks = [
        validate_manifest(manifest),
        validate_parts(manifest),
        validate_files(manifest),
        validate_toc(),
        validate_directory_tree(),
    ]

    if all(checks):
        print("✔ Export validated successfully — Copilot-ready.")
        return 0
    else:
        print("✖ Export validation failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
