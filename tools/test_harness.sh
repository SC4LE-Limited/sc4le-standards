#!/usr/bin/env bash
set -e

echo "=== SC4LE Export Test Harness ==="

# 1. Clean old exports
rm -f export_*.md export-manifest.json

# 2. Run exporter
echo "Running exporter..."
python tools/export_repo.py --branch main --max-size-bytes 1000000

# 3. Validate export
echo "Validating export..."
python tools/validate_export.py

# 4. Compare expected vs exported markdown files
echo "Checking completeness..."
find . -type f -name "*.md" | sort > expected.txt
jq -r '.files[].path' export-manifest.json | sort > exported.txt

echo "Diff (expected vs exported):"
diff expected.txt exported.txt || true

# 5. Check part sizes
echo "Part sizes:"
ls -lh export_*.md

echo "=== Test harness complete ==="
