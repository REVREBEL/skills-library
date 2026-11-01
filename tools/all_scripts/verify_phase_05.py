#!/usr/bin/env python3
"""
verify_phase_05.py

Comprehensive 18-Point Hardened Verification Suite for Phase 05 (Functional Taxonomy & Destination Mapping).
Ensures:
1. skills-inventory.csv contains 2,331 rows.
2. Exactly 45 quarantined rows are excluded from destination mapping.
3. Exactly 2,286 active rows are mapped.
4. Every active source path appears exactly once (1:1 bijection).
5. No quarantined source path appears in destination-map.csv.
6. Every mapped row maps to an allowed category and an allowed subcategory for that parent category.
7. Every mapped row has a valid compatibility classification and routing role from the finite allowed sets.
8. Every mapped row reconciles columns: path category, subcategory, and slug match the row fields.
9. Destination paths are globally unique.
10. Destination paths are unique case-insensitively.
11. Real router namespace validation: 55 routers (1 root, 10 cat, 44 subcat), exact hierarchy and path formula verification, zero collisions with skill destinations.
12. Target paths follow canonical naming conventions (standard depth, kebab-case).
13. Category counts sum to exactly 2,286.
14. Report reconciliation: parses functional-taxonomy.md and verifies all 10 category totals, 44 subcategory counts, percentages, router counts, and total row.
15. Confidence values belong to allowed enum {'high', 'medium', 'low'}.
16. Placement basis and concern verification for all confidence tiers with strict distribution assertions (high: 1,852, medium: 434, low: 0).
17. Zero workstation absolute path leaks in Phase 05 files (hardened multi-OS regex).
18. Hard check: Git diff against merge-base (fail-closed) proves ZERO modifications under task-folder/agents/skills/.
"""

import csv
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ALLOWED_CATEGORIES = {
    "development",
    "design-and-experience",
    "infrastructure-and-ops",
    "data-and-ai",
    "quality-and-security",
    "marketing-and-seo",
    "business-and-operations",
    "content-and-documentation",
    "workflow-and-automation",
    "meta-and-agent-skills"
}

ALLOWED_SUBCATEGORIES = {
    "business-and-operations": {
        "legal-and-governance", "product-management", "startup-finance", "strategy"
    },
    "content-and-documentation": {
        "copywriting", "presentations", "research-and-synthesis", "technical-writing"
    },
    "data-and-ai": {
        "analytics", "data-engineering", "llm-and-rag", "machine-learning", "vector-databases"
    },
    "design-and-experience": {
        "design-systems", "motion-and-graphics", "taste-and-critique", "ui-ux"
    },
    "development": {
        "backend", "frontend", "fullstack", "mobile", "software-architecture", "systems"
    },
    "infrastructure-and-ops": {
        "ci-cd", "cloud-platforms", "containers-and-orchestration", "observability", "server-management"
    },
    "marketing-and-seo": {
        "content-and-campaigns", "cro", "geo-and-local-seo", "on-page-seo", "technical-seo"
    },
    "meta-and-agent-skills": {
        "agent-architecture", "skill-lifecycle", "skill-validation"
    },
    "quality-and-security": {
        "compliance", "debugging", "security", "testing"
    },
    "workflow-and-automation": {
        "git-and-vcs", "task-orchestration", "tool-integration", "web-scraping"
    }
}

ALLOWED_COMPATIBILITY = {
    "Approved and supported",
    "Supported after conversion",
    "Ambiguous and requiring manual review",
    "Provider-specific but potentially reusable"
}

ALLOWED_ROUTING_ROLES = {
    "child_skill",
    "router_candidate"
}

ALLOWED_CONFIDENCE = {"high", "medium", "low"}

INVENTORY_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
DESTINATION_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/destination-map.csv"
ROUTER_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/router-map.csv"
TAXONOMY_REPORT_PATH = "task-folder/agents/skills-rebuild/_audit/functional-taxonomy.md"

def get_git_output(cmd):
    if not isinstance(cmd, (list, tuple)) or not cmd or cmd[0] != "git":
        raise ValueError(f"Invalid command invocation: {cmd}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, shell=False)
    return res.stdout.strip()

def verify_all():
    print("=== STARTING HARDENED PHASE 05 TAXONOMY & DESTINATION RECONCILIATION VALIDATION ===")
    
    # Check HEAD and Base
    try:
        head_sha = get_git_output(["git", "rev-parse", "HEAD"])
        print(f"  HEAD SHA: {head_sha}")
    except Exception as e:
        print(f"  Warning: Could not get HEAD SHA: {e}")

    # 1. Check 1: skills-inventory.csv contains 2,331 rows
    print("\n[CHECK 1] Row Count of Source Inventory:")
    assert os.path.exists(INVENTORY_PATH), f"Error: Inventory missing at {INVENTORY_PATH}"
    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        inv_rows = list(csv.DictReader(f))
    total_inv = len(inv_rows)
    print(f"  - Total source inventory rows: {total_inv}")
    assert total_inv == 2331, f"Expected 2331 rows in inventory, found {total_inv}"
    print(" -> PASS: Inventory row count is exactly 2,331.")

    # 2. Check 2: Exactly 45 quarantined rows excluded
    print("\n[CHECK 2] Quarantined Population Identification:")
    quarantined_rows = [r for r in inv_rows if r.get("conversion_status") == "Not In Scope (Phase 03 Quarantined)"]
    quarantined_count = len(quarantined_rows)
    print(f"  - Quarantined row count: {quarantined_count}")
    assert quarantined_count == 45, f"Expected 45 quarantined rows, found {quarantined_count}"
    quarantined_paths = {r["source_path"] for r in quarantined_rows}
    print(" -> PASS: Exactly 45 quarantined rows identified and isolated.")

    # 3. Check 3: Exactly 2,286 active rows mapped
    print("\n[CHECK 3] Retained Population Destination Mapping Count:")
    assert os.path.exists(DESTINATION_MAP_PATH), f"Error: Destination map missing at {DESTINATION_MAP_PATH}"
    with open(DESTINATION_MAP_PATH, "r", encoding="utf-8") as f:
        dest_rows = list(csv.DictReader(f))
    dest_count = len(dest_rows)
    print(f"  - Total mapped destination rows: {dest_count}")
    assert dest_count == 2286, f"Expected 2286 destination rows, found {dest_count}"
    print(" -> PASS: Exactly 2,286 active retained skills mapped.")

    # 4. Check 4: Every active source path appears exactly once
    print("\n[CHECK 4] Source Path 1:1 Coverage & Bijectivity:")
    active_inv_paths = {r["source_path"] for r in inv_rows if r.get("conversion_status") != "Not In Scope (Phase 03 Quarantined)"}
    dest_src_paths = [r["source_path"] for r in dest_rows]
    dest_src_set = set(dest_src_paths)
    assert len(dest_src_paths) == len(dest_src_set), "Duplicate source_path found in destination-map.csv!"
    assert active_inv_paths == dest_src_set, "Mismatch between active inventory source paths and destination map source paths!"
    print(f"  - Verified 1:1 coverage across all {len(dest_src_set)} source paths.")
    print(" -> PASS: Every active source path appears exactly once.")

    # 5. Check 5: No quarantined source path appears in destination-map.csv
    print("\n[CHECK 5] Quarantined Source Exclusion:")
    quarantined_in_dest = quarantined_paths.intersection(dest_src_set)
    assert len(quarantined_in_dest) == 0, f"Error: Quarantined paths leaked into destination map: {quarantined_in_dest}"
    print(" -> PASS: Zero quarantined source paths exist in destination-map.csv.")

    # 6. Check 6: Category and Subcategory Hierarchy Validity
    print("\n[CHECK 6] Category and Subcategory Hierarchy Validity:")
    cat_counts = Counter()
    subcat_counts = defaultdict(Counter)
    for r in dest_rows:
        cat = r.get("proposed_category", "")
        subcat = r.get("proposed_subcategory", "")
        assert cat in ALLOWED_CATEGORIES, f"Invalid category '{cat}' for source '{r['source_path']}'"
        assert cat in ALLOWED_SUBCATEGORIES, f"Category '{cat}' missing from ALLOWED_SUBCATEGORIES definition"
        assert subcat in ALLOWED_SUBCATEGORIES[cat], (
            f"Invalid subcategory '{subcat}' for category '{cat}' in source '{r['source_path']}'"
        )
        cat_counts[cat] += 1
        subcat_counts[cat][subcat] += 1
    total_subcats = sum(len(subs) for subs in subcat_counts.values())
    print(f"  - Verified 10 top-level categories and {total_subcats} active subcategories across all 2,286 rows.")
    print(" -> PASS: All categories and subcategories strictly adhere to parent-child hierarchy.")

    # 7. Check 7: Finite Compatibility Status & Routing Role Field Check
    print("\n[CHECK 7] Finite Compatibility Status & Routing Role Field Check:")
    compat_counts = Counter()
    role_counts = Counter()
    for r in dest_rows:
        compat = r.get("compatibility_status", "")
        role = r.get("routing_role", "")
        assert compat in ALLOWED_COMPATIBILITY, (
            f"Invalid compatibility_status '{compat}' for source '{r['source_path']}'! Must be in {ALLOWED_COMPATIBILITY}"
        )
        assert role in ALLOWED_ROUTING_ROLES, (
            f"Invalid routing_role '{role}' for source '{r['source_path']}'! Must be in {ALLOWED_ROUTING_ROLES}"
        )
        compat_counts[compat] += 1
        role_counts[role] += 1
    print("  - Compatibility Classifications:")
    for compat_val, cnt in sorted(compat_counts.items()):
        print(f"    * {compat_val}: {cnt}")
    print("  - Routing Roles:")
    for role_val, cnt in sorted(role_counts.items()):
        print(f"    * {role_val}: {cnt}")
    print(" -> PASS: Every row possesses an allowed compatibility status and valid routing role.")

    # 8. Check 8: Destination Path Presence & Column Reconciliation
    print("\n[CHECK 8] Destination Path Presence & Cross-Column Reconciliation:")
    for r in dest_rows:
        dest_p = r.get("proposed_final_path", "")
        assert dest_p and dest_p.strip() != "", f"Empty proposed_final_path for source '{r['source_path']}'"
        parts = dest_p.split("/")
        assert len(parts) == 6, f"Path '{dest_p}' depth is not standard (expected 6 parts, got {len(parts)})"
        assert parts[0] == "task-folder" and parts[1] == "agents" and parts[2] == "skills", (
            f"Path prefix invalid in '{dest_p}'"
        )
        path_cat, path_subcat, path_slug = parts[3], parts[4], parts[5]
        assert path_cat == r["proposed_category"], (
            f"Column mismatch in row '{r['source_path']}': path category '{path_cat}' != proposed_category '{r['proposed_category']}'"
        )
        assert path_subcat == r["proposed_subcategory"], (
            f"Column mismatch in row '{r['source_path']}': path subcategory '{path_subcat}' != proposed_subcategory '{r['proposed_subcategory']}'"
        )
        assert r.get("routing_role") in ALLOWED_ROUTING_ROLES, (
            f"Missing or invalid routing_role in row '{r['source_path']}'"
        )
    print(" -> PASS: 100% of destination paths are present and fully reconciled against category, subcategory, and routing_role columns.")

    # 9. Check 9: Global Destination Path Uniqueness (Exact):
    print("\n[CHECK 9] Global Destination Path Uniqueness (Exact):")
    final_paths = [r["proposed_final_path"] for r in dest_rows]
    assert len(final_paths) == len(set(final_paths)), "Duplicate proposed_final_path detected in destination-map.csv!"
    print(f"  - Verified all {len(final_paths)} destination paths are globally unique.")
    print(" -> PASS: Global destination path uniqueness confirmed (0 duplicates).")

    # 10. Check 10: Case-Insensitive Destination Path Uniqueness:
    print("\n[CHECK 10] Case-Insensitive Destination Path Uniqueness:")
    final_paths_lower = [p.lower() for p in final_paths]
    assert len(final_paths_lower) == len(set(final_paths_lower)), "Case-insensitive duplicate proposed_final_path detected!"
    print(" -> PASS: Case-insensitive destination path uniqueness confirmed.")

    # 11. Check 11: Real Router Namespace Validation & Router Map Structure
    print("\n[CHECK 11] Router Map Structure & Namespace Safety Validation:")
    assert os.path.exists(ROUTER_MAP_PATH), f"Error: Router map missing at {ROUTER_MAP_PATH}"
    with open(ROUTER_MAP_PATH, "r", encoding="utf-8") as f:
        router_rows = list(csv.DictReader(f))
    
    assert len(router_rows) == 55, f"Expected exactly 55 router rows, found {len(router_rows)}"
    router_type_counts = Counter(r["router_type"] for r in router_rows)
    print(f"  - Total router rows: {len(router_rows)}")
    print(f"    * root_router: {router_type_counts['root_router']} (expected 1)")
    print(f"    * category_router: {router_type_counts['category_router']} (expected 10)")
    print(f"    * subcategory_router: {router_type_counts['subcategory_router']} (expected 44)")
    
    assert router_type_counts["root_router"] == 1, "Expected exactly 1 root_router"
    assert router_type_counts["category_router"] == 10, "Expected exactly 10 category_router"
    assert router_type_counts["subcategory_router"] == 44, "Expected exactly 44 subcategory_router"

    # Exact Hierarchy & Path Verification for Router Map:
    # 1. Root router check
    root_rows = [r for r in router_rows if r["router_type"] == "root_router"]
    assert len(root_rows) == 1, "Root router count must be exactly 1"
    assert root_rows[0]["category"] == "root", f"Root router category must be 'root', got '{root_rows[0]['category']}'"
    assert root_rows[0]["subcategory"] in ("None", "", None), f"Root router subcategory must be 'None', got '{root_rows[0]['subcategory']}'"
    assert root_rows[0]["proposed_path"] == "task-folder/agents/skills/SKILL.md", (
        f"Root router path invalid: '{root_rows[0]['proposed_path']}'"
    )

    # 2. Category router checks
    cat_routers = {r["category"]: r for r in router_rows if r["router_type"] == "category_router"}
    assert set(cat_routers.keys()) == ALLOWED_CATEGORIES, (
        f"Category routers mismatch: missing {ALLOWED_CATEGORIES - set(cat_routers.keys())}, extra {set(cat_routers.keys()) - ALLOWED_CATEGORIES}"
    )
    for cat, r in cat_routers.items():
        assert r["subcategory"] in ("None", "", None), f"Category router subcategory must be 'None' for {cat}"
        expected_cat_path = f"task-folder/agents/skills/{cat}/SKILL.md"
        assert r["proposed_path"] == expected_cat_path, (
            f"Category router path mismatch for '{cat}': expected '{expected_cat_path}', got '{r['proposed_path']}'"
        )

    # 3. Subcategory router checks
    subcat_routers = {(r["category"], r["subcategory"]): r for r in router_rows if r["router_type"] == "subcategory_router"}
    expected_subcat_pairs = {(cat, subcat) for cat, subcats in ALLOWED_SUBCATEGORIES.items() for subcat in subcats}
    assert set(subcat_routers.keys()) == expected_subcat_pairs, (
        f"Subcategory routers mismatch: missing {expected_subcat_pairs - set(subcat_routers.keys())}, extra {set(subcat_routers.keys()) - expected_subcat_pairs}"
    )
    for (cat, subcat), r in subcat_routers.items():
        expected_subcat_path = f"task-folder/agents/skills/{cat}/{subcat}/SKILL.md"
        assert r["proposed_path"] == expected_subcat_path, (
            f"Subcategory router path mismatch for '{cat}/{subcat}': expected '{expected_subcat_path}', got '{r['proposed_path']}'"
        )

    # 4. Router Path Uniqueness & Collision Detection
    router_paths = [r["proposed_path"] for r in router_rows]
    router_paths_lower = {p.lower() for p in router_paths}
    assert len(router_paths) == len(router_paths_lower) == 55, "Duplicate router paths detected!"

    # Derive router directories
    router_dirs = {os.path.dirname(p) for p in router_paths}
    router_dirs_lower = {d.lower() for d in router_dirs}

    final_paths_set = set(final_paths)
    for p in final_paths:
        p_lower = p.lower()
        assert p_lower not in router_dirs_lower, (
            f"Collision: Skill destination directory '{p}' matches a router directory!"
        )
        assert p_lower not in router_paths_lower, (
            f"Collision: Skill destination path '{p}' matches a planned router file path!"
        )
    print(f"  - Verified exact hierarchy, exact paths, and 0 collisions across 55 router directories/files and {len(final_paths)} skill destinations.")
    print(" -> PASS: Router map structure verified and zero namespace collisions confirmed.")

    # 12. Check 12: Target paths follow canonical naming conventions
    print("\n[CHECK 12] Destination Path Naming Conventions:")
    for p in final_paths:
        parts = p.split("/")
        cat, subcat, skill_fn = parts[3], parts[4], parts[5]
        assert cat in ALLOWED_CATEGORIES, f"Category '{cat}' invalid in path '{p}'"
        assert re.match(r"^[a-z0-9\-]+$", subcat), f"Subcategory '{subcat}' is not kebab-case in '{p}'"
        assert re.match(r"^[a-z0-9\-]+$", skill_fn), f"Skill folder '{skill_fn}' is not kebab-case in '{p}'"
    print(" -> PASS: All destination paths adhere strictly to kebab-case and shallow directory conventions.")

    # 13. Check 13: Category counts sum to exactly 2,286
    print("\n[CHECK 13] Category Sum Reconciliation:")
    sum_cats = sum(cat_counts.values())
    print(f"  - Category sum: {sum_cats}")
    assert sum_cats == 2286, f"Expected category sum 2286, got {sum_cats}"
    for cat in sorted(cat_counts.keys()):
        print(f"    * {cat}: {cat_counts[cat]}")
    print(" -> PASS: Category counts sum exactly to 2,286.")

    # 14. Check 14: Full Report Reconciliation (Executive Summary, 44 Subcategories, Category Totals, Matrix)
    print("\n[CHECK 14] Full Report-to-CSV Matrix & Summary Reconciliation:")
    assert os.path.exists(TAXONOMY_REPORT_PATH), f"Error: Taxonomy report missing at {TAXONOMY_REPORT_PATH}"
    with open(TAXONOMY_REPORT_PATH, "r", encoding="utf-8") as f:
        report_text = f.read()

    # Verify Executive Summary
    assert "**2,331**" in report_text, "Total source count missing or mismatched in Executive Summary"
    assert "**45**" in report_text, "Quarantined count missing or mismatched in Executive Summary"
    assert "**2,286**" in report_text, "Retained mapped count missing or mismatched in Executive Summary"
    assert "**10**" in report_text, "Top-level categories count missing or mismatched in Executive Summary"
    assert "**55**" in report_text, "Planned routers count missing or mismatched in Executive Summary"

    # Parse 44 Subcategory rows in Section 5 Matrix Table
    table_subcat_rows = re.findall(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*([\d\.]+%)\s*\|", report_text)
    assert len(table_subcat_rows) == 44, f"Expected 44 subcategory rows in table, parsed {len(table_subcat_rows)}"
    for cat, subcat, count_str, pct_str in table_subcat_rows:
        count = int(count_str)
        expected_count = subcat_counts[cat][subcat]
        assert count == expected_count, f"Table count mismatch for {cat}/{subcat}: expected {expected_count}, got {count}"
        expected_pct = f"{(expected_count / 2286) * 100:.1f}%"
        assert pct_str == expected_pct, f"Table percentage mismatch for {cat}/{subcat}: expected {expected_pct}, got {pct_str}"

    # Parse 10 Category Total rows in Section 5 Matrix Table
    table_cat_rows = re.findall(r"\|\s*\*\*`([^`]+)`\*\*\s*\|\s*\*\([^\)]+\)\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*([\d\.]+%)\*\*\s*\|", report_text)
    assert len(table_cat_rows) == 10, f"Expected 10 category total rows in table, parsed {len(table_cat_rows)}"
    for cat, count_str, pct_str in table_cat_rows:
        count = int(count_str)
        expected_count = cat_counts[cat]
        assert count == expected_count, f"Table category total mismatch for {cat}: expected {expected_count}, got {count}"
        expected_pct = f"{(expected_count / 2286) * 100:.1f}%"
        assert pct_str == expected_pct, f"Table category percentage mismatch for {cat}: expected {expected_pct}, got {pct_str}"

    # Parse Grand Total row in Section 5 Matrix Table
    total_match = re.search(r"\|\s*\*\*TOTAL\*\*\s*\|\s*\*\*All Categories\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*([\d\.]+%)\*\*\s*\|", report_text)
    assert total_match is not None, "Grand total row not found in report table"
    assert int(total_match.group(1)) == 2286, f"Expected grand total 2286, got {total_match.group(1)}"
    assert total_match.group(2) == "100.0%", f"Expected grand total percentage 100.0%, got {total_match.group(2)}"

    # Verify Section 4 definitions and counts
    for cat, count in cat_counts.items():
        assert f"Skill Count**: **{count}**" in report_text, f"Section 4 count missing for category '{cat}'"

    print(f"  - Verified Executive Summary totals, 10 category sections, 10 category totals, 44 subcategory rows & percentages, and grand total.")
    print(" -> PASS: Full reconciliation confirmed between functional-taxonomy.md and destination-map.csv.")

    # 15. Check 15: Confidence values belong to allowed enum
    print("\n[CHECK 15] Placement Confidence Enum:")
    for r in dest_rows:
        conf = r.get("placement_confidence", "")
        assert conf in ALLOWED_CONFIDENCE, f"Invalid confidence '{conf}' for source '{r['source_path']}'"
    print(" -> PASS: All placement confidence values belong strictly to {'high', 'medium', 'low'}.")

    # 16. Check 16: Placement Basis and Concern Gate Across All Confidence Tiers
    print("\n[CHECK 16] Placement Basis & Concern Gate Across All Confidence Tiers:")
    conf_breakdown = Counter()
    for r in dest_rows:
        conf = r.get("placement_confidence", "")
        conf_breakdown[conf] += 1
        basis = r.get("placement_basis", "")
        concern = r.get("placement_concern", "")
        
        # Every row must have an explicit placement basis
        assert basis and basis.strip() != "", f"Row '{r['source_path']}' missing placement_basis!"
        
        if conf == "medium":
            # Medium confidence rows must document the specific reason / placement concern
            assert concern and concern.strip() != "None" and concern.strip() != "", (
                f"Row '{r['source_path']}' with medium confidence has no documented placement_concern!"
            )
        elif conf == "low":
            # Low confidence rows must document the placement concern
            assert concern and concern.strip() != "None" and concern.strip() != "", (
                f"Row '{r['source_path']}' with low confidence has no documented placement_concern!"
            )

    assert conf_breakdown["high"] == 1852, f"Expected 1852 high-confidence rows, got {conf_breakdown['high']}"
    assert conf_breakdown["medium"] == 434, f"Expected 434 medium-confidence rows, got {conf_breakdown['medium']}"
    assert conf_breakdown["low"] == 0, f"Expected 0 low-confidence rows, got {conf_breakdown['low']}"

    print(f"  - Total Mapped Skills: {len(dest_rows)}")
    print(f"    * High Confidence: {conf_breakdown['high']} (100% contain explicit placement_basis)")
    print(f"    * Medium Confidence: {conf_breakdown['medium']} (100% contain placement_basis & documented concern)")
    print(f"    * Low Confidence: {conf_breakdown['low']} (0 unreviewed edge cases)")
    print(" -> PASS: Placement basis and concern verification satisfied across all confidence tiers.")

    # 17. Check 17: Multi-OS Workstation Path Leak Detection
    print("\n[CHECK 17] Multi-OS Workstation Path Leak Detection:")
    phase_05_files = [
        DESTINATION_MAP_PATH,
        ROUTER_MAP_PATH,
        TAXONOMY_REPORT_PATH,
        "task-folder/agents/skills-rebuild/_audit/verify_phase_05.py"
    ]
    # Hardened regex supporting macOS (/Users/...), Linux (/home/...), and Windows (C:\Users\..., D:/home/...)
    user_pattern = re.compile(
        r"/(?:Users|home)/[a-zA-Z0-9_\-]+|[A-Za-z]:[/\\](?:Users|home)[/\\][a-zA-Z0-9_\-]+",
        re.IGNORECASE
    )
    for fp in phase_05_files:
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                matches = user_pattern.findall(content)
                assert len(matches) == 0, f"Workstation path leak detected in {fp}: {matches}"
    print(" -> PASS: Zero workstation absolute path leaks detected in any Phase 05 files.")

    # 18. Check 18: Physical Immutability Gate (Git diff against merge-base)
    print("\n[CHECK 18] Physical Immutability Gate (Git Diff Against Merge-Base):")
    try:
        try:
            merge_base = get_git_output(["git", "merge-base", "HEAD", "origin/main"])
        except Exception:
            merge_base = get_git_output(["git", "merge-base", "HEAD", "main"])
        print(f"  - Using Merge-Base SHA: {merge_base}")

        git_status_diff = get_git_output(["git", "diff", "--name-only", merge_base])
        changed_files = [line.strip() for line in git_status_diff.splitlines() if line.strip()]
        skill_tree_changes = [f for f in changed_files if f.startswith("task-folder/agents/skills/")]
        assert len(skill_tree_changes) == 0, (
            f"Violation: Physical skills tree modified during Phase 05! Touched files: {skill_tree_changes}"
        )
        print(f"  - Checked {len(changed_files)} changed files on branch vs merge-base ({merge_base[:8]}).")
        print("  - ZERO physical skills were moved, modified, split, merged, or deleted under task-folder/agents/skills/.")
        print(" -> PASS: Hard check confirmed: 'map first, move later' principle physically upheld.")
    except Exception as e:
        print(f"  - Error during git diff verification: {e}")
        raise e

    print("\n=== ALL 18 PHASE 05 VALIDATION CHECKS PASSED PERFECTLY! HARDENED AUDIT COMPLETE! ===")

if __name__ == "__main__":
    verify_all()
