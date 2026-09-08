name: Export repository snapshot

on:
  workflow_dispatch:

jobs:
  export:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      - name: Checkout
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: '3.11'

      - name: Run export script
        run: |
          python3 tools/export_repo.py --root . --output export.md --manifest-file export-manifest.json --max-size 2000000

      - name: Run gitleaks secret scan
        uses: gitleaks/gitleaks-action@v3
        env:
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}

      - name: Run markdown text sanitizer
        run: |
          chmod +x tools/markdown_text_sanitizer.py
          python3 tools/markdown_text_sanitizer.py

      - name: Sanitize manifest (remove blob_sha/commit metadata)
        run: |
          python3 - <<'PY'
          import json, sys
          try:
              m = json.load(open('export-manifest.json'))
          except FileNotFoundError:
              print('export-manifest.json not found', file=sys.stderr)
              sys.exit(0)
          for f in m.get('files', []):
              f.pop('blob_sha', None)
              f.pop('last_commit', None)
              f.pop('last_commit_date', None)
          json.dump(m, open('export-manifest-sanitized.json','w'), indent=2)
          PY

      - name: Upload sanitized export artifact (sanitized parts + sanitized manifest + gitleaks SARIF)
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: repo-export-sanitized
          path: |
            export_*_sanitized.md
            export-manifest-sanitized.json
            results.sarif
