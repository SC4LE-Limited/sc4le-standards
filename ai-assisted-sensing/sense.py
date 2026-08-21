import os
import yaml
from datetime import datetime

# Folders to scan (full repo, but you can tweak this list)
SCAN_ROOTS = [
    ".",  # whole repo
]

# File extensions to include
INCLUDE_EXTENSIONS = [".md"]

# Simple severity mapping
def classify_severity(issue: str) -> str:
    if "missing" in issue or "invalid" in issue:
        return "high"
    if "non_compliant" in issue:
        return "medium"
    return "low"


def find_markdown_files():
    files = []
    for root in SCAN_ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            # Skip .git and ai-assisted-sensing itself
            if ".git" in dirpath or "ai-assisted-sensing" in dirpath:
                continue
            for name in filenames:
                if any(name.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                    rel_path = os.path.relpath(os.path.join(dirpath, name), ".")
                    files.append(rel_path)
    return files


def analyze_file(path):
    """
    Return a list of signals for a single file.
    Each signal is a dict:
    {
        "folder": "foundations",
        "file": "sc4le-principles.md",
        "issue": "metadata_missing_tags",
        "severity": "high"
    }
    """
    signals = []

    folder = os.path.dirname(path) or "."
    file = os.path.basename(path)

    # Read file
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

    # Detect YAML front matter
    yaml_data = None
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_block = parts[1]
            try:
                yaml_data = yaml.safe_load(yaml_block) or {}
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
        # Example checks: title, tags
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

    # Simple structural checks (example: must contain at least one H1)
    if "# " not in content:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "structure_missing_h1",
            "severity": "medium",
        })

    # Naming checks (spaces, parentheses)
    if " " in file or "(" in file or ")" in file:
        signals.append({
            "folder": folder,
            "file": file,
            "issue": "naming_invalid_filename",
            "severity": "low",
        })

    return signals


def write_grouped_log(signals):
    by_folder = {}
    by_type = {}
    severity_counts = {"high": 0, "medium": 0, "low": 0}

    for s in signals:
        folder = s["folder"]
        file = s["file"]
        issue = s["issue"]
        severity = s.get("severity", classify_severity(issue))

        severity_counts[severity] += 1

        if folder not in by_folder:
            by_folder[folder] = {}
        if file not in by_folder[folder]:
            by_folder[folder][file] = []
        by_folder[folder][file].append(issue)

        if issue not in by_type:
            by_type[issue] = []
        by_type[issue].append(f"{folder}/{file}")

    md = []
    md.append("# SC4LE Adaptation Log")
    md.append(f"_Last updated: {datetime.utcnow().isoformat()}Z_")
    md.append("\n---\n")

    md.append("## 🔍 Summary of Signals")
    md.append(f"- **High severity:** {severity_counts['high']}")
    md.append(f"- **Medium severity:** {severity_counts['medium']}")
    md.append(f"- **Low severity:** {severity_counts['low']}")
    md.append("\n---\n")

    md.append("## 📁 Signals by Folder\n")
    for folder, files in sorted(by_folder.items()):
        md.append(f"### {folder}/")
        for file, issues in sorted(files.items()):
            md.append(f"- **{file}**")
            for issue in issues:
                md.append(f"  - {issue}")
        md.append("")

    md.append("\n---\n")

    md.append("## 🧭 Signals by Type\n")
    for issue, locations in sorted(by_type.items()):
        md.append(f"### {issue}")
        for loc in sorted(locations):
            md.append(f"- {loc}")
        md.append("")

    md.append("\n---\n")

    md.append("## 🚨 High‑Priority Issues (Fix Soon)")
    for folder, files in sorted(by_folder.items()):
        for file, issues in sorted(files.items()):
            for issue in issues:
                if "missing" in issue or "invalid" in issue:
                    md.append(f"- {folder}/{file} — {issue}")
    md.append("\n---\n")

    with open("ai-assisted-sensing/adaptation-log.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))


def write_dashboard(signals):
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    by_folder = {}

    for s in signals:
        folder = s["folder"]
        file = s["file"]
        issue = s["issue"]
        severity = s.get("severity", classify_severity(issue))

        severity_counts[severity] += 1

        if folder not in by_folder:
            by_folder[folder] = {"high": 0, "medium": 0, "low": 0}
        by_folder[folder][severity] += 1

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
    for folder, counts in sorted(by_folder.items()):
        md.append(f"### {folder}/")
        md.append(f"- High: {counts['high']}")
        md.append(f"- Medium: {counts['medium']}")
        md.append(f"- Low: {counts['low']}")
        md.append("")

    with open("ai-assisted-sensing/outcome-dashboard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))


def main():
    files = find_markdown_files()
    all_signals = []

    for path in files:
        signals = analyze_file(path)
        all_signals.extend(signals)

    write_grouped_log(all_signals)
    write_dashboard(all_signals)


if __name__ == "__main__":
    main()
