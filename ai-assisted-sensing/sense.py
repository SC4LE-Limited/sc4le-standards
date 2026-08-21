import os
import re
import datetime
import yaml

MONITORED_FOLDERS = ["meta", "foundations", "operating-model"]
LOG_PATH = os.path.join("ai-assisted-sensing", "adaptation-log.md")
DASHBOARD_PATH = os.path.join("ai-assisted-sensing", "outcome-dashboard.md")

# ---------- Helpers ----------

def iso_now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def is_semver(version):
    return bool(re.match(r"^\d+\.\d+\.\d+$", str(version)))

def is_iso_date(value):
    try:
        datetime.datetime.fromisoformat(str(value).replace("Z", ""))
        return True
    except Exception:
        return False

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_append(path, text):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def load_dashboard():
    if not os.path.exists(DASHBOARD_PATH):
        return {}
    content = read_file(DASHBOARD_PATH)
    metrics = {}
    for line in content.splitlines():
        if "<count>" in line:
            continue
        m = re.search(r"^- (.+?): (\d+)$", line.strip())
        if m:
            key, val = m.group(1), int(m.group(2))
            metrics[key] = val
    return metrics

def save_dashboard(metrics):
    # Very simple: we only rewrite the counts section, not the whole file structure.
    # Assumes the dashboard uses lines like: "- metadata_missing_header: <count>"
    content = read_file(DASHBOARD_PATH)
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        m = re.search(r"^- (.+?): <count>$", line.strip())
        if m:
            key = m.group(1)
            val = metrics.get(key, 0)
            new_lines.append(f"- {key}: {val}")
        else:
            new_lines.append(line)
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

def parse_yaml_header(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    yaml_lines = []
    body_lines = []
    in_yaml = True
    for line in lines[1:]:
        if in_yaml and line.strip() == "---":
            in_yaml = False
            continue
        if in_yaml:
            yaml_lines.append(line)
        else:
            body_lines.append(line)
    try:
        meta = yaml.safe_load("\n".join(yaml_lines)) or {}
    except Exception:
        meta = {}
    body = "\n".join(body_lines)
    return meta, body

def detect_sections(body):
    # Very simple: look for markdown headings as section markers
    sections = []
    for line in body.splitlines():
        if line.startswith("#"):
            sections.append(line.strip("# ").strip())
    return sections

def emit_signal(folder, file_path, issue, signal_type, routed_to):
    timestamp = iso_now()
    line = f"{timestamp} | {folder}/ | {file_path} | {issue} | {signal_type} | {routed_to}"
    write_append(LOG_PATH, line)
    return line

# ---------- Rule Checks ----------

def check_metadata(folder, file_path, meta):
    signals = []
    routed_to = "Governance Workspace"

    if meta is None:
        signals.append(("metadata_missing_header", "metadata_non_compliant"))
        return signals

    schema = meta.get("schema")
    version = meta.get("version")
    updated = meta.get("updated")
    owner = meta.get("owner")
    tags = meta.get("tags")

    if schema != "sc4le-meta-v1":
        signals.append(("metadata_invalid_schema", "metadata_non_compliant"))
    if not is_semver(version):
        signals.append(("metadata_invalid_version", "metadata_non_compliant"))
    if not is_iso_date(updated):
        signals.append(("metadata_invalid_date", "metadata_non_compliant"))
    if owner != "SC4LE Limited":
        signals.append(("metadata_invalid_owner", "metadata_non_compliant"))
    if not tags or not isinstance(tags, list) or len(tags) == 0:
        signals.append(("metadata_missing_tags", "metadata_non_compliant"))

    return signals

def check_structure(folder, file_path, body):
    signals = []
    routed_to = "Governance Workspace"
    sections = detect_sections(body)

    required = []
    if folder == "meta":
        required = ["Purpose", "Scope", "Governance", "Roles", "Workflow", "Versioning"]
    elif folder == "foundations":
        required = ["Principle", "Description", "Behaviour", "Anti‑patterns"]
    elif folder == "operating-model":
        required = ["Domains", "Cadences", "Decision pathways", "Roles"]

    for req in required:
        if not any(req.lower() in s.lower() for s in sections):
            signals.append((f"structure_missing_section:{req}", "structure_non_compliant"))

    return signals

def check_naming(folder, file_path):
    signals = []
    routed_to = "Brand Workspace"

    filename = os.path.basename(file_path)

    # Very simple naming checks as a starting point
    if " " in filename:
        signals.append(("naming_invalid_filename", "naming_taxonomy_violation"))

    # Example taxonomy rule: roles should be lowercase with hyphens
    if folder == "operating-model/roles":
        if not re.match(r"^[a-z0-9\-]+\.md$", filename):
            signals.append(("naming_taxonomy_violation", "naming_taxonomy_violation"))

    return signals

# ---------- Main Scanner ----------

def scan_file(root_folder, rel_path):
    full_path = os.path.join(root_folder, rel_path)
    text = read_file(full_path)
    meta, body = parse_yaml_header(text)

    # Metadata
    metadata_signals = check_metadata(root_folder, rel_path, meta)
    for issue, signal_type in metadata_signals:
        emit_signal(root_folder, rel_path, issue, signal_type, "Governance Workspace")

    # Structural
    structural_signals = check_structure(root_folder, rel_path, body)
    for issue, signal_type in structural_signals:
        emit_signal(root_folder, rel_path, issue, signal_type, "Governance Workspace")

    # Naming
    naming_signals = check_naming(root_folder, rel_path)
    for issue, signal_type in naming_signals:
        emit_signal(root_folder, rel_path, issue, signal_type, "Brand Workspace")

def main():
    # Ensure log file exists
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("# AI‑Assisted Sensing — Adaptation Log\n")

    # Scan monitored folders
    for folder in MONITORED_FOLDERS:
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            for name in files:
                if not name.endswith(".md"):
                    continue
                rel_path = os.path.relpath(os.path.join(root, name), folder)
                scan_file(folder, rel_path)

    # Dashboard update (simple count aggregation)
    metrics = {}
    if os.path.exists(LOG_PATH):
        content = read_file(LOG_PATH)
        for line in content.splitlines():
            if "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 6:
                continue
            issue = parts[3]
            metrics[issue] = metrics.get(issue, 0) + 1

    # Map issues to dashboard keys
    dashboard_metrics = {
        "metadata_missing_header": metrics.get("metadata_missing_header", 0),
        "metadata_invalid_schema": metrics.get("metadata_invalid_schema", 0),
        "metadata_invalid_version": metrics.get("metadata_invalid_version", 0),
        "metadata_invalid_date": metrics.get("metadata_invalid_date", 0),
        "metadata_missing_tags": metrics.get("metadata_missing_tags", 0),
        "structure_missing_section": sum(
            v for k, v in metrics.items() if k.startswith("structure_missing_section")
        ),
        "structure_invalid_order": metrics.get("structure_invalid_order", 0),
        "structure_schema_violation": metrics.get("structure_schema_violation", 0),
        "naming_invalid_filename": metrics.get("naming_invalid_filename", 0),
        "naming_taxonomy_violation": metrics.get("naming_taxonomy_violation", 0),
    }

    if os.path.exists(DASHBOARD_PATH):
        save_dashboard(dashboard_metrics)

if __name__ == "__main__":
    main()
