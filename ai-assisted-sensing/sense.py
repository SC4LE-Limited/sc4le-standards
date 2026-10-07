"""
SC4LE Sensing Engine
--------------------
This script validates YAML metadata across the SC4LE Standards repository.

Inline notes explain:
- non-obvious logic
- constraints and assumptions
- warnings for future maintainers

Long-form documentation (architecture, design decisions, roadmap)
is stored in:
    /ai-assisted-sensing/sensing-engine-notes.md
"""

import os
import yaml
import json
from datetime import datetime

# ---------------------------------------------------------
# 1. Load governed schema index dynamically
# ---------------------------------------------------------
# IMPORTANT:
# - This replaces hard-coded schema definitions.
# - Any new schema added to /schemas/schema-index.json is
#   automatically recognised by the sensing engine.
# - This prevents drift between governance and code.
# - If the schema index fails to load, metadata validation
#   will fail safely with helpful errors.
# ---------------------------------------------------------

SCHEMA_INDEX_FILE = "schemas/schema-index.json"

def load_schema_index():
    """Load schema definitions from the governed schema index."""
    try:
        with open(SCHEMA_INDEX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("schemas", {})
    except Exception as e:
        # WARNING:
        # If this fails, metadata validation cannot proceed correctly.
        # Future maintainers: do NOT silence this error.
        print(f"ERROR: Could not load schema index: {e}")
        return {}

SCHEMA_REQUIREMENTS = load_schema_index()


# ---------------------------------------------------------
# 2. Files and directories that should NOT be validated
# ---------------------------------------------------------
# RATIONALE:
# - ai-assisted-sensing contains sensing output, not governed content.
# - Documentation files do not require YAML metadata.
# - Only Markdown files with YAML headers should be validated.
# ---------------------------------------------------------

SKIP_FILENAMES = {
    "readme.md",
    "license.md",
    "contributing.md",
    "trademarks.md",
    "index.md",
}

SKIP_DIRECTORY_KEYWORDS = {
    "ai-assisted-sensing",
}

def should_validate_file(file_path: str) -> bool:
    """Determine whether a file should undergo metadata validation."""
    filename = os.path.basename(file_path).lower()
    directory_path = os.path.dirname(file_path).lower()

    # Skip documentation files
    if filename in SKIP_FILENAMES:
        return False

    # Skip sensing output directories
    for keyword in SKIP_DIRECTORY_KEYWORDS:
        if keyword in directory_path:
            return False

    # Only validate Markdown files
    if not filename.endswith(".md"):
        return False

    return True


# ---------------------------------------------------------
# 3. Load YAML header safely
# ---------------------------------------------------------
# NOTE:
# - Only the YAML front matter is parsed.
# - If the file has no YAML header, metadata_missing_header is recorded.
# - This function must remain stable; many SC4LE tools rely on this format.
# ---------------------------------------------------------

def load_yaml_header(file_path: str):
    """Extract YAML front matter from a Markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # No YAML header present
        if not lines or not lines[0].strip() == "---":
            return None

        yaml_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            yaml_lines.append(line)

        return yaml.safe_load("".join(yaml_lines))

    except Exception:
        # WARNING:
        # Do not raise — sensing must continue even if a file is malformed.
        return None


# ---------------------------------------------------------
# 4. Validate metadata using dynamic schema index
# ---------------------------------------------------------
# NOTE:
# - This is the core of the sensing engine.
# - Required fields come from schema-index.json.
# - If a schema is missing, we produce a helpful error message
#   telling editors exactly how to fix it.
# ---------------------------------------------------------

def validate_metadata(file_path: str):
    """Validate YAML metadata against governed schema definitions."""
    issues = []
    header = load_yaml_header(file_path)

    if header is None:
        issues.append("metadata_missing_header")
        return issues

    schema = header.get("schema")

    if schema not in SCHEMA_REQUIREMENTS:
        issues.append(
            f"metadata_unknown_schema — Schema '{schema}' is not registered. "
            f"Add it to {SCHEMA_INDEX_FILE}."
        )
        return issues

    required_fields = SCHEMA_REQUIREMENTS[schema].get("required", [])

    for field in required_fields:
        if field not in header:
            issues.append(f"metadata_missing_{field}")

    return issues


# ---------------------------------------------------------
# 5. Record signals
# ---------------------------------------------------------
# NOTE:
# - High severity issues are logged here.
# - This file is used by CDA and LDAs to track metadata drift.
# - Do not change formatting; dashboards depend on this structure.
# ---------------------------------------------------------

ADAPTATION_LOG = "ai-assisted-sensing/adaptation-log.md"

def record_signal(file_path: str, issues: list):
    """Append issues to the adaptation log."""
    with open(ADAPTATION_LOG, "a", encoding="utf-8") as f:
        f.write(f"- **{file_path}**\n")
        for issue in issues:
            f.write(f"  - {issue}\n")


# ---------------------------------------------------------
# 6. Generate dashboard
# ---------------------------------------------------------
# NOTE:
# - Only high severity issues exist today.
# - Medium/low severity categories are reserved for future expansion.
# - Dashboard must remain human-readable for LDAs.
# ---------------------------------------------------------

OUTCOME_DASHBOARD = "ai-assisted-sensing/outcome-dashboard.md"

def generate_dashboard(high, medium, low):
    """Generate a human-readable dashboard summarising sensing results."""
    with open(OUTCOME_DASHBOARD, "w", encoding="utf-8") as f:
        f.write("# SC4LE Adaptation Log\n")
        f.write(f"_Last updated: {datetime.utcnow().isoformat()}Z_\n\n")
        f.write("---\n\n")
        f.write("## 🔍 Summary of Signals\n")
        f.write(f"- **High severity files:** {len(high)}\n")
        f.write(f"- **Medium severity files:** {len(medium)}\n")
        f.write(f"- **Low severity files:** {len(low)}\n\n")
        f.write("---\n\n")

        if high:
            f.write("## 🚨 High Severity Issues\n")
            for file, issues in high.items():
                f.write(f"### {file}\n")
                for issue in issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
        else:
            f.write("## 🚨 High Severity Issues\n_No high severity issues detected._\n\n")

        f.write("---\n\n")


# ---------------------------------------------------------
# 7. Main sensing loop
# ---------------------------------------------------------
# NOTE:
# - Walks the entire repo.
# - Applies skip rules.
# - Validates metadata.
# - Records issues.
# - Future maintainers: do NOT parallelise this without ensuring
#   deterministic ordering — the dashboard depends on stable output.
# ---------------------------------------------------------

def run_sensing():
    """Run the full sensing pass across the repository."""
    high = {}
    medium = {}
    low = {}

    # Reset adaptation log header
    with open(ADAPTATION_LOG, "w", encoding="utf-8") as f:
        f.write("# SC4LE Adaptation Log\n")
        f.write(f"_Last updated: {datetime.utcnow().isoformat()}Z_\n\n")
        f.write("---\n\n")

    for root, _, files in os.walk(REPO_ROOT):
        for file in files:
            file_path = os.path.join(root, file)

            if not should_validate_file(file_path):
                continue

            issues = validate_metadata(file_path)

            if issues:
                high[file_path] = issues
                record_signal(file_path, issues)

    generate_dashboard(high, medium, low)


# ---------------------------------------------------------
# 8. Entrypoint
# ---------------------------------------------------------
# NOTE:
# - Running this file triggers a full sensing pass.
# - This is intentionally simple; do not wrap in CLI frameworks.
# ---------------------------------------------------------

if __name__ == "__main__":
    run_sensing()
