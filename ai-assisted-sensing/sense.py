import os
import yaml
from datetime import datetime

# ------------------------------------------------------------
# SCHEMA MAP
# ------------------------------------------------------------

SCHEMA_MAP = {
    "foundations": {
        "schema": "sc4le-standard-v1",
        "required": ["title", "tags", "owner", "status", "version", "updated"]
    },
    "operating-model": {
        "schema": "sc4le-standard-v1",
        "required": ["title", "tags", "owner", "status", "version", "updated"]
    },
    "meta": {
        "schema": "sc4le-standard-v1",
        "required": ["title", "tags", "owner", "status", "version", "updated"]
    },

    # NEW — split services into standard + commercial
    "services/standard": {
        "schema": "sc4le-standard-v1",
        "required": ["title", "tags", "owner", "status", "version", "updated"]
    },
    "services/commercial": {
        "schema": "sc4le-service-v1",
        "required": ["title", "service_category", "target_customer", "pricing_model", "tags"]
    },

    # NEW — split value props into framework + commercial
    "value-propositions/framework": {
        "schema": "sc4le-standard-v1",
        "required": ["title", "tags", "owner", "status", "version", "updated"]
    },
    "value-propositions/commercial": {
        "schema": "sc4le-value-v1",
        "required": ["title", "value_type", "target_customer", "tags"]
    },

    "brand": {
        "schema": "sc4le-brand-v1",
        "required": ["title", "brand_asset_type", "usage_rules", "tags"]
    },
    "diagrams": {
        "schema": "sc4le-diagram-v1",
        "required": ["title", "diagram_type", "source_file", "tags"]
    },
    "Templates": {
        "schema": "sc4le-template-v1",
        "required": ["title", "template_type", "use_cases", "tags"]
    },
    "web": {
        "schema": "sc4le-web-v1",
        "required": ["title", "slug", "layout", "tags"]
    },
    "programmes": {
        "schema": "sc4le-programme-v1",
        "required": ["title", "programme_type", "target_group", "tags"]
    },
    "maturity-model": {
        "schema": "sc4le-maturity-v1",
        "required": ["title", "maturity_dimension", "tags"]
    }
}

IGNORE_ROOT_FILES = [
    "README.md", "LICENSE.md", "CONTRIBUTING.md", "TRADEMARKS.md"
]

# ------------------------------------------------------------
# SEVERITY CLASSIFICATION
# ------------------------------------------------------------

def classify_severity(issue: str) -> str:
    if "missing" in issue or "invalid" in issue:
        return "high"
    if "non_compliant" in issue:
        return "medium"
    return "low"

# ------------------------------------------------------------
# FILE DISCOVERY
# ------------------------------------------------------------

def find_markdown_files():
    files = []
    for dirpath, dirnames, filenames in os.walk("."):
        if ".git" in dirpath or "ai-assisted-sensing" in dirpath:
            continue
        for name in filenames:
            if name.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, name), ".")
                files.append(rel)
    return files

# ------------------------------------------------------------
# FILE ANALYSIS
# ------------------------------------------------------------

def analyze_file(path):
    folder = os.path.dirname(path).split("/")[0] or "."
    file = os.path.basename(path)

    # Ignore root-level docs
    if folder == "." and file in IGNORE_ROOT_FILES:
        return []

    signals = []

    # Determine schema
    schema_info = SCHEMA_MAP.get(folder)
    if not schema_info:
        return []  # ignore folders without schemas

    required_fields = schema_info["required"]

    # Read file
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "file_unreadable",
            "severity": "high"
        })
        return signals

    # YAML detection
    yaml_data = None
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                yaml_data = yaml.safe_load(parts[1]) or {}
            except Exception:
                signals.append({
                    "folder": folder,
                    "file": file,
                    "issue": "metadata_invalid_yaml",
                    "severity": "high"
                })

    if yaml_data is None:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "metadata_missing_header",
            "severity": "high"
        })
        return signals

    # Schema validation
    for field in required_fields:
        if field not in yaml_data or yaml_data.get(field) in ["", None]:
            signals.append({
                "folder": folder,
                "file": file,
                "issue": f"metadata_missing_{field}",
                "severity": "high"
            })

    # Structural check
    if "# " not in content:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "structure_missing_h1",
            "severity": "medium"
        })

    # Naming check
    if " " in file or "(" in file or ")" in file:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "naming_invalid_filename",
            "severity": "low"
        })

    return signals

# ------------------------------------------------------------
# LOG WRITER (Severity → File → Issues)
# ------------------------------------------------------------

def write_grouped_log(signals):
    severity_groups = {"high": {}, "medium": {}, "low": {}}

    for s in signals:
        severity = s["severity"]
        file_key = f"{s['folder']}/{s['file']}"
        issue = s["issue"]

        severity_groups[severity].setdefault(file_key, []).append(issue)

    md = []
    md.append("# SC4LE Adaptation Log")
    md.append(f"_Last updated: {datetime.utcnow().isoformat()}Z_")
    md.append("\n---\n")

    md.append("## 🔍 Summary of Signals")
    md.append(f"- **High severity files:** {len(severity_groups['high'])}")
    md.append(f"- **Medium severity files:** {len(severity_groups['medium'])}")
    md.append(f"- **Low severity files:** {len(severity_groups['low'])}")
    md.append("\n---\n")

    for level, title in [
        ("high", "🚨 High Severity Issues"),
        ("medium", "🟡 Medium Severity Issues"),
        ("low", "🟢 Low Severity Issues")
    ]:
        md.append(f"## {title}")
        if severity_groups[level]:
            for file_key, issues in sorted(severity_groups[level].items()):
                md.append(f"### {file_key}")
                for issue in issues:
                    md.append(f"- {issue}")
                md.append("")
        else:
            md.append(f"_No {level} severity issues detected._")
        md.append("\n---\n")

    with open("ai-assisted-sensing/adaptation-log.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

# ------------------------------------------------------------
# DASHBOARD WRITER
# ------------------------------------------------------------

def write_dashboard(signals):
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    folder_health = {}

    for s in signals:
        severity = s["severity"]
        folder = s["folder"]

        severity_counts[severity] += 1
        folder_health.setdefault(folder, {"high": 0, "medium": 0, "low": 0})
        folder_health[folder][severity] += 1

    md = []
    md.append("# SC4LE Sensing Dashboard")
    md.append(f"_Last updated: {datetime.utcnow().isoformat()}Z_")
    md.append("\n---\n")

    md.append("## 🔍 Overall Severity Counts")
    md.append(f"- **High:** {severity_counts['high']}")
    md.append(f"- **Medium:** {severity_counts['medium']}")
    md.append(f"- **Low:** {severity_counts['low']}")
    md.append("\n---\n")

    md.append("## 📁 Folder Health")
    for folder, counts in sorted(folder_health.items()):
        md.append(f"### {folder}/")
        md.append(f"- High: {counts['high']}")
        md.append(f"- Medium: {counts['medium']}")
        md.append(f"- Low: {counts['low']}")
        md.append("")
    md.append("\n---\n")

    with open("ai-assisted-sensing/outcome-dashboard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    files = find_markdown_files()
    all_signals = []
    for path in files:
        all_signals.extend(analyze_file(path))

    write_grouped_log(all_signals)
    write_dashboard(all_signals)

if __name__ == "__main__":
    main()
