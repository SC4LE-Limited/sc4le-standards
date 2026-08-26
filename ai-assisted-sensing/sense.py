import os
import yaml
from datetime import datetime

REPO_ROOT = "."
ADAPTATION_LOG = "ai-assisted-sensing/adaptation-log.md"
OUTCOME_DASHBOARD = "ai-assisted-sensing/outcome-dashboard.md"

# ---------------------------------------------------------
# 1. Files and directories that should NOT be validated
# ---------------------------------------------------------
SKIP_FILENAMES = {
    "readme.md",
    "license.md",
    "contributing.md",
    "trademarks.md",
}

SKIP_DIRECTORY_KEYWORDS = {
    "ai-assisted-sensing",
}


def should_validate_file(file_path: str) -> bool:
    """
    Determines whether a file should undergo metadata validation.
    Documentation and sensing output files must be ignored.
    """
    filename = os.path.basename(file_path).lower()
    directory_path = os.path.dirname(file_path).lower()

    # Skip documentation files
    if filename in SKIP_FILENAMES:
        return False

    # Skip any file inside ai-assisted-sensing (in any path form)
    for keyword in SKIP_DIRECTORY_KEYWORDS:
        if keyword in directory_path:
            return False

    # Skip non-Markdown files
    if not filename.endswith(".md"):
        return False

    return True


# ---------------------------------------------------------
# 2. Load YAML header safely
# ---------------------------------------------------------
def load_yaml_header(file_path: str):
    """
    Loads the YAML header from a Markdown file.
    Returns None if no YAML header exists.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines or not lines[0].strip() == "---":
            return None

        yaml_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            yaml_lines.append(line)

        return yaml.safe_load("".join(yaml_lines))

    except Exception:
        return None


# ---------------------------------------------------------
# 3. Schema requirements
# ---------------------------------------------------------
SCHEMA_REQUIREMENTS = {
    "sc4le-standard-v1": ["title", "tags", "owner", "status", "version", "updated"],
    "sc4le-service-v1": ["title", "service_category", "target_customer", "pricing_model", "tags"],
    "sc4le-brand-v1": ["title", "brand_asset_type", "usage_rules", "tags"],
    "sc4le-diagram-v1": ["title", "diagram_type", "source_file", "tags"],
    "sc4le-template-v1": ["title", "template_type", "use_cases", "tags"],
    "sc4le-web-v1": ["title", "slug", "layout", "tags"],
    "sc4le-value-v1": ["title", "value_type", "target_customer", "tags"],
    "sc4le-programme-v1": ["title", "programme_type", "target_group", "tags"],
    "sc4le-maturity-v1": ["title", "maturity_dimension", "tags"],
}


# ---------------------------------------------------------
# 4. Validate metadata
# ---------------------------------------------------------
def validate_metadata(file_path: str):
    issues = []
    header = load_yaml_header(file_path)

    if header is None:
        issues.append("metadata_missing_header")
        return issues

    schema = header.get("schema")
    if schema not in SCHEMA_REQUIREMENTS:
        issues.append("metadata_unknown_schema")
        return issues

    required_fields = SCHEMA_REQUIREMENTS[schema]

    for field in required_fields:
        if field not in header:
            issues.append(f"metadata_missing_{field}")

    return issues


# ---------------------------------------------------------
# 5. Record signals
# ---------------------------------------------------------
def record_signal(file_path: str, issues: list):
    with open(ADAPTATION_LOG, "a", encoding="utf-8") as f:
        f.write(f"- **{file_path}**\n")
        for issue in issues:
            f.write(f"  - {issue}\n")


# ---------------------------------------------------------
# 6. Generate dashboard
# ---------------------------------------------------------
def generate_dashboard(high, medium, low):
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
def run_sensing():
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

            # Skip documentation + sensing output
            if not should_validate_file(file_path):
                continue

            issues = validate_metadata(file_path)

            if issues:
                high[file_path] = issues
                record_signal(file_path, issues)

    generate_dashboard(high, medium, low)


# ---------------------------------------------------------
# 8. Run sensing engine
# ---------------------------------------------------------
if __name__ == "__main__":
    run_sensing()
