root = Path(args.root).resolve()
output_base = Path(args.output).resolve()
manifest_path = Path(args.manifest_file).resolve()
excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)
part_size = args.part_size
max_size = args.max_size

head = git_head_sha(root)
branch = git_branch(root)
remote = git_remote_url(root)
head_tag = git_describe_tag(root)
blob_map = git_ls_tree_blob_map(root)

files = build_file_list(root, excludes, max_size)
tree_lines = build_tree_lines(files, root)

file_infos = []
for pth, size in files:
    rel = pth.relative_to(root)
    rel_str = str(rel)
    anchor = slugify_anchor(rel_str)
    ext = pth.suffix.lower()
    lang = EXT_LANG.get(ext, '')
    meta = git_last_commit_for_file(root, rel)
    blob_sha = blob_map.get(rel_str)
    file_infos.append({
        "path": rel_str,
        "size": size,
        "language": lang or None,
        "anchor": anchor,
        "last_commit": meta['sha'] if meta else None,
        "last_commit_date": meta['date'] if meta else None,
        "last_commit_author": meta['author'] if meta else None,
        "blob_sha": blob_sha,
        "export_file": None,
        "sanitized": False
    })

toc_lines = [f"- [{fi['path']}](#{fi['anchor']})" for fi in file_infos]

def write_and_count(fhandle, s, counter):
    b = s.encode('utf-8')
    fhandle.write(s)
    return counter + len(b)

base_stem = output_base.stem
base_suffix = output_base.suffix or '.md'

def part_filename_for(index):
    return f"{base_stem}_{index:03}{base_suffix}"

part_index = 1
part_path = root / part_filename_for(part_index)
out = part_path.open('w', encoding='utf-8')
current_bytes = 0
parts_meta = []

def write_part_header(f, idx, counter):
    header = f"# Repository export: {root.name} (part {idx})\n\n"
    if head:
        header += f"- commit: `{head}`\n\n"
    if branch:
        header += f"- branch: `{branch}`\n\n"
    if head_tag:
        header += f"- tag: `{head_tag}`\n\n"
    if remote:
        header += f"- remote: `{remote}`\n\n"
    header += f"- generated_by: tools/export_repo.py\n"
    header += f"- generated_at: {datetime.utcnow().isoformat()}Z\n\n"
    header += "---\n\n"
    counter = write_and_count(f, header, counter)
    if idx == 1:
        tree_block = "## Directory tree\n\n```\n"
        for l in tree_lines:
            tree_block += l + "\n"
        tree_block += "```\n\n"
        counter = write_and_count(f, tree_block, counter)

        toc_block = "## Table of contents\n\n"
        if toc_lines:
            toc_block += "\n".join(toc_lines) + "\n\n"
        else:
            toc_block += "_No exported files_\n\n"
        counter = write_and_count(f, toc_block, counter)
        counter = write_and_count(f, "---\n\n", counter)
        counter = write_and_count(f, "## Files\n\n", counter)
    return counter

current_bytes = write_part_header(out, part_index, current_bytes)

for fi in file_infos:
    rel = fi['path']
    anchor = fi['anchor']
    fpath = root / rel

    meta_lines = []
    meta_lines.append(f"<a name=\"{anchor}\"></a>\n\n")
    meta_lines.append(f"### {rel}\n\n")
    meta_lines.append(f"- size: {fi['size']} bytes\n")
    if fi['last_commit']:
        meta_lines.append(f"- last_commit: `{fi['last_commit']}` ({fi['last_commit_date']}) by {fi['last_commit_author']}\n")
    if fi['blob_sha']:
        meta_lines.append(f"- blob_sha: `{fi['blob_sha']}`\n")
    if fi['language']:
        meta_lines.append(f"- language: {fi['language']}\n")
    meta_lines.append("\n")

    text = safe_read_text(fpath)
    if args.sanitize:
        sanitized_text = sanitize_content(text, rel)
        text_to_write = sanitized_text
        fi['sanitized'] = True
    else:
        text_to_write = text
        fi['sanitized'] = False

    text_bytes_len = len(text_to_write.encode('utf-8'))
    ext = fpath.suffix.lower()
    lang = fi['language'] or ''

    if lang:
        fence_start = f"```{lang}\n"
        fence_end = "```\n\n"
    else:
        fence_start = "```\n"
        fence_end = "```\n\n"

    meta_bytes = sum(len(s.encode('utf-8')) for s in meta_lines)
    fence_start_bytes = len(fence_start.encode('utf-8'))
    fence_end_bytes = len(fence_end.encode('utf-8'))
    section_bytes = meta_bytes + fence_start_bytes + text_bytes_len + fence_end_bytes

    if current_bytes + section_bytes > part_size and current_bytes > 0:
        out.close()
        parts_meta.append({
            "filename": str(part_path.relative_to(root)),
            "size": current_bytes
        })
        part_index += 1
        part_path = root / part_filename_for(part_index)
        out = part_path.open('w', encoding='utf-8')
        current_bytes = 0
        current_bytes = write_part_header(out, part_index, current_bytes)

    for s in meta_lines:
        current_bytes = write_and_count(out, s, current_bytes)
    current_bytes = write_and_count(out, fence_start, current_bytes)
    current_bytes = write_and_count(out, text_to_write.rstrip() + "\n", current_bytes)
    current_bytes = write_and_count(out, fence_end, current_bytes)

    fi['export_file'] = str(part_path.relative_to(root))

out.close()
parts_meta.append({
    "filename": str(part_path.relative_to(root)),
    "size": current_bytes
})

manifest = {
    "repo": root.name,
    "head": head,
    "branch": branch,
    "head_tag": head_tag,
    "remote": remote,
    "generated_at": datetime.utcnow().isoformat() + 'Z',
    "generated_by": 'tools/export_repo.py',
    "part_size": part_size,
    "parts": parts_meta,
    "files": []
}

for fi in file_infos:
    entry = {
        "path": fi['path'],
        "size": fi['size'],
        "language": fi['language'],
        "anchor": fi['anchor'],
        "last_commit": fi['last_commit'],
        "last_commit_date": fi['last_commit_date'],
        "last_commit_author": fi['last_commit_author'],
        "blob_sha": fi['blob_sha'],
        "export_file": fi['export_file'],
        "sanitized": fi.get('sanitized', False)
    }
    manifest["files"].append(entry)

try:
    with manifest_path.open('w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2)
except Exception:
    pass

print("Export parts written:")
for pm in parts_meta:
    print(f" - {pm['filename']} ({pm['size']} bytes)")
print(f"Manifest written to {manifest_path}")
