import os
import yaml
from datetime import datetime

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

# Scan the entire repo (except .git and sensing folder)
SCAN_ROOTS = ["."]
INCLUDE_EXTENSIONS = [".md"]

# ------------------------------------------------------------
# SEVERITY CLASSIFICATION
# ------------------------------------------------------------

def classify_severity(issue: str) -> str:
    """
    Simple severity rules:
    - High: missing or invalid metadata/structure
    - Medium: structural non-compliance
    - Low: naming issues
    """
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
    for root in SCAN_ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            if ".git" in dirpath or "ai-assisted-sensing" in dirpath:
                continue
            for name in filenames:
                if any(name.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                    rel_path = os.path.relpath(os.path.join(dirpath, name), ".")
                    files.append(rel_path)
    return files

# ------------------------------------------------------------
# FILE ANALYSIS
# ------------------------------------------------------------

def analyze_file(path):
    signals = []
    folder = os.path.dirname(path) or "."
    file = os.path.basename(path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "file_unreadable",
            "severity": "high",
        })
        return signals

    # YAML front matter detection
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
                    "severity": "high",
                })

    # Metadata checks
    if yaml_data is None:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "metadata_missing_header",
            "severity": "high",
        })
    else:
        if "title" not in yaml_data:
            signals.append({
                "folder": folder,
                "file": file,
                "issue": "metadata_missing_title",
                "severity": "high",
            })
        if "tags" not in yaml_data or not yaml_data.get("tags"):
            signals.append({
                "folder": folder,
                "file": file,
                "issue": "metadata_missing_tags",
                "severity": "high",
            })

    # Structural checks
    if "# " not in content:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "structure_missing_h1",
            "severity": "medium",
        })

    # Naming checks
    if " " in file or "(" in file or ")" in file:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "naming_invalid_filename",
            "severity": "low",
        })

    return signals

# ------------------------------------------------------------
# LOG WRITER (Severity → File → Issues)
# ------------------------------------------------------------

def write_grouped_log(signals):
    severity_groups = {"high": {}, "medium": {}, "low": {}}

    for s in signals:
        severity = s.get("severity", classify_severity(s["issue"]))
        file_key = f"{s['folder']}/{s['file']}"
        issue = s["issue"]

        if file_key not in severity_groups[severity]:
            severity_groups[severity][file_key] = []
        severity_groups[severity][file_key].append(issue)

    md = []
    md.append("# SC4LE Adaptation Log")
    md.append(f"_Last updated: {datetime.utcnow().isoformat()}Z_")
    md.append("\n---\n")

    # Summary
    md.append("## 🔍 Summary of Signals")
    md.append(f"- **High severity files:** {len(severity_groups['high'])}")
    md.append(f"- **Medium severity files:** {len(severity_groups['medium'])}")
    md.append(f"- **Low severity files:** {len(severity_groups['low'])}")
    md.append("\n---\n")

    # High severity
    md.append("## 🚨 High Severity Issues")
    if severity_groups["high"]:
        for file_key, issues in sorted(severity_groups["high"].items()):
            md.append(f"### {file_key}")
            for issue in issues:
                md.append(f"- {issue}")
            md.append("")
    else:
        md.append("_No high severity issues detected._")
    md.append("\n---\n")

    # Medium severity
    md.append("## 🟡 Medium Severity Issues")
    if severity_groups["medium"]:
        for file_key, issues in sorted(severity_groups["medium"].items()):
            md.append(f"### {file_key}")
            for issue in issues:
                md.append(f"- {issue}")
            md.append("")
    else:
        md.append("_No medium severity issues detected._")
    md.append("\n---\n")

    # Low severity
    md.append("## 🟢 Low Severity Issues")
    if severity_groups["low"]:
        for file_key, issues in sorted(severity_groups["low"].items()):
            md.append(f"### {file_key}")
            for issue in issues:
                md.append(f"- {issue}")
            md.append("")
    else:
        md.append("_No low severity issues detected._")
    md.append("\n---\n")

    with open("ai-assisted-sensing/adaptation-log.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

# ------------------------------------------------------------
# DASHBOARD WRITER (Severity-first folder health)
# ------------------------------------------------------------

def write_dashboard(signals):
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    folder_health = {}

    for s in signals:
        severity = s.get("severity", classify_severity(s["issue"]))
        folder = s["folder"]

        severity_counts[severity] += 1

        if folder not in folder_health:
            folder_health[folder] = {"high": 0, "medium": 0, "low": 0}
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

    md.append("## 📁 Folder Health (Severity-first)")
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
