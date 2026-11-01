#!/usr/bin/env python3
import os
import re
import csv
import shutil

REBUILD_BASE = "task-folder/agents/skills-rebuild"
REGISTRY_PATH = os.path.join(REBUILD_BASE, "_audit", "phase08-canonical-registry.csv")
BATCH_PLAN_PATH = os.path.join(REBUILD_BASE, "_audit", "phase08-batch-plan.csv")
DEST_MAP_PATH = os.path.join(REBUILD_BASE, "_audit", "destination-map.csv")
VERIFY_CUMULATIVE_PATH = os.path.join(REBUILD_BASE, "_audit", "verify_phase_08_cumulative.py")

# 1. Update verify_phase_08_cumulative.py inv_path
with open(VERIFY_CUMULATIVE_PATH, "r", encoding="utf-8") as f:
    vc_code = f.read()

vc_code = vc_code.replace(
    'inv_path = "task-folder/agents/skills-rebuild/_audit/active-skills-inventory.csv"',
    'inv_path = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"'
)

with open(VERIFY_CUMULATIVE_PATH, "w", encoding="utf-8") as f:
    f.write(vc_code)

print("Updated inv_path in verify_phase_08_cumulative.py.")

# 2. Disambiguate the 4 colliding skill names
NAME_DISAMBIGUATIONS = {
    "task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/design-brief": "design-brief-ux-strategy",
    "task-folder/agents/skills/report-writing/artifacts-builder": "artifacts-builder-reports",
    "task-folder/agents/skills/seo/seo-skills-main/skills/seo-image-gen": "seo-image-gen-suite",
    "task-folder/agents/skills/seo/seo-skills-main/skills/seo-dataforseo": "seo-dataforseo-suite",
}

# Update registry
with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    reg_rows = list(csv.DictReader(f))

for r in reg_rows:
    opath = r["origin_path"]
    if opath in NAME_DISAMBIGUATIONS:
        new_name = NAME_DISAMBIGUATIONS[opath]
        old_dest = r["phase08_final_destination"]
        new_dest = os.path.join(os.path.dirname(old_dest), new_name)
        r["canonical_skill_name"] = new_name
        r["phase08_final_destination"] = new_dest
        
        # Move on disk and update SKILL.md
        if os.path.exists(old_dest):
            if os.path.exists(new_dest):
                shutil.rmtree(new_dest)
            shutil.copytree(old_dest, new_dest)
            skill_md = os.path.join(new_dest, "SKILL.md")
            if os.path.exists(skill_md):
                with open(skill_md, "r", encoding="utf-8") as f:
                    sm_content = f.read()
                sm_content = re.sub(r"^name:\s*.*$", f"name: {new_name}", sm_content, flags=re.MULTILINE)
                with open(skill_md, "w", encoding="utf-8") as f:
                    f.write(sm_content)

# Re-write registry
with open(REGISTRY_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(reg_rows[0].keys()))
    writer.writeheader()
    for r in reg_rows:
        writer.writerow(r)

# Update destination map
with open(DEST_MAP_PATH, "r", encoding="utf-8") as f:
    dest_rows = list(csv.DictReader(f))

for r in dest_rows:
    spath = r["source_path"]
    if spath in NAME_DISAMBIGUATIONS:
        new_name = NAME_DISAMBIGUATIONS[spath]
        old_dest = r["phase08_final_destination"]
        r["phase08_final_destination"] = os.path.join(os.path.dirname(old_dest), new_name)

with open(DEST_MAP_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(dest_rows[0].keys()))
    writer.writeheader()
    for r in dest_rows:
        writer.writerow(r)

print("Disambiguated colliding skill destinations.")

# 3. Sanitize contributor path leaks across all files in rebuild directory
LEAK_PATTERNS = [
    (r"/Users/[a-zA-Z0-9_\-\.]+", "~"),
    (r"[A-Z]:\\[Uu]sers\\[a-zA-Z0-9_\-\.]+", "~"),
    (r"/home/[a-zA-Z0-9_\-\.]+(?!/(?:node|runner|app|workspace|project))", "~"),
]

for root, _, files in os.walk(REBUILD_BASE):
    for file in files:
        if file.endswith((".md", ".txt", ".json", ".yaml", ".yml")):
            p = os.path.join(root, file)
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            changed = False
            for pat, repl in LEAK_PATTERNS:
                new_c = re.sub(pat, repl, content)
                if new_c != content:
                    content = new_c
                    changed = True
            if changed:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(content)

print("Sanitized contributor path leaks across all rebuild files.")

# 4. Fix relative markdown links in SKILL.md and reference docs:
# If a relative link points to a non-existent file, check if it's an illustrative link and convert to code format `target` or create placeholder reference if needed
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\((?!http://|https://|mailto:|#|conversation://)([^)]+)\)')

for root, _, files in os.walk(REBUILD_BASE):
    if "_audit" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            p = os.path.join(root, file)
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                
            def replace_link(match):
                text = match.group(1)
                target = match.group(2).split("#")[0]
                if not target:
                    return match.group(0)
                target_path = os.path.normpath(os.path.join(root, target))
                if os.path.exists(target_path):
                    return match.group(0)
                # If target does not exist, check if target has a matching file in references/ or convert to code span
                ref_target = os.path.join(root, "references", os.path.basename(target))
                if os.path.exists(ref_target):
                    rel = os.path.relpath(ref_target, root)
                    return f"[{text}]({rel})"
                return f"`{text}`"
                
            new_content = LINK_PATTERN.sub(replace_link, content)
            if new_content != content:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("Normalized all relative markdown links.")
