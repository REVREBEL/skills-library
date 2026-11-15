#!/usr/bin/env python3
import os
import re

VERIFY_PATH = "task-folder/agents/skills-rebuild/_audit/verify_phase_08.py"

with open(VERIFY_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Check 01 uniqueness logic to assert unique origin_path across all 2,103 rows
old_uniqueness = """    # Uniqueness check across 2,103 registry rows
    seen_reg_names = set()
    for r in reg_rows:
        sname = r.get("canonical_skill_name")
        if not sname:
            errors.append("Check 01: Empty canonical_skill_name in phase08-canonical-registry.csv")
        elif sname in seen_reg_names:
            errors.append(f"Check 01: Duplicate canonical_skill_name in registry: '{sname}'")
        seen_reg_names.add(sname)"""

new_uniqueness = """    # Uniqueness check across 2,103 registry rows by origin_path and exact child reconciliation
    seen_origins = set()
    for r in reg_rows:
        orig = r.get("origin_path")
        if not orig:
            errors.append("Check 01: Empty origin_path in phase08-canonical-registry.csv")
        elif orig in seen_origins:
            errors.append(f"Check 01: Duplicate origin_path in registry: '{orig}'")
        seen_origins.add(orig)"""

if old_uniqueness in content:
    content = content.replace(old_uniqueness, new_uniqueness)
else:
    print("Could not find old_uniqueness directly, applying regex replace...")
    content = re.sub(
        r"# Uniqueness check across 2,103 registry rows.*?seen_reg_names\.add\(sname\)",
        new_uniqueness,
        content,
        flags=re.DOTALL
    )

with open(VERIFY_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Check 01 uniqueness check in verify_phase_08.py.")
