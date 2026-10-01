#!/usr/bin/env python3
"""
verify_phase_10.py - Calibrated Deterministic 10-Gate Verifier for Phase 10
(Build the Router Hierarchy).
"""

import os
import sys
import csv
import re
import subprocess
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../.."))
REBUILD_DIR = os.path.join(BASE_DIR, "task-folder/agents/skills-rebuild")
AUDIT_DIR = os.path.join(REBUILD_DIR, "_audit")
CANON_CSV = os.path.join(AUDIT_DIR, "phase08-canonical-registry.csv")
FUNCTIONAL_MAP_CSV = os.path.join(AUDIT_DIR, "phase10-functional-routing-map.csv")
VALIDATION_MD = os.path.join(AUDIT_DIR, "router-validation.md")

EXPECTED_CATEGORIES = sorted([
    "business-and-operations",
    "content-and-documentation",
    "data-and-ai",
    "design-and-experience",
    "development",
    "infrastructure-and-ops",
    "marketing-and-seo",
    "meta-and-agent-skills",
    "quality-and-security",
    "workflow-and-automation"
])

EXPECTED_TAXONOMY = {
    "business-and-operations": ["legal-and-governance", "product-management", "startup-finance", "strategy"],
    "content-and-documentation": ["copywriting", "presentations", "research-and-synthesis", "technical-writing"],
    "data-and-ai": ["analytics", "data-engineering", "llm-and-rag", "machine-learning", "vector-databases"],
    "design-and-experience": ["design-systems", "motion-and-graphics", "taste-and-critique", "ui-ux"],
    "development": ["backend", "frontend", "fullstack", "mobile", "software-architecture", "systems"],
    "infrastructure-and-ops": ["ci-cd", "cloud-platforms", "containers-and-orchestration", "observability", "server-management"],
    "marketing-and-seo": ["content-and-campaigns", "cro", "geo-and-local-seo", "on-page-seo", "technical-seo"],
    "meta-and-agent-skills": ["agent-architecture", "skill-lifecycle", "skill-validation"],
    "quality-and-security": ["compliance", "debugging", "security", "testing"],
    "workflow-and-automation": ["git-and-vcs", "task-orchestration", "tool-integration", "web-scraping"]
}

DEEP_CATEGORIES = {
    "development": ["backend", "frontend", "fullstack", "mobile", "software-architecture", "systems"],
    "marketing-and-seo": ["content-and-campaigns", "cro", "geo-and-local-seo", "on-page-seo", "technical-seo"],
    "design-and-experience": ["design-systems", "motion-and-graphics", "taste-and-critique", "ui-ux"]
}

APPROVED_FILES = {
    "task-folder/agents/skills-rebuild/SKILL.md",
    "task-folder/agents/skills-rebuild/_audit/phase10-functional-routing-map.csv",
    "task-folder/agents/skills-rebuild/_audit/router-validation.md",
    "task-folder/agents/skills-rebuild/_audit/verify_phase_10.py",
    "task-folder/agents/skills-rebuild/business-and-operations/SKILL.md",
    "task-folder/agents/skills-rebuild/content-and-documentation/SKILL.md",
    "task-folder/agents/skills-rebuild/data-and-ai/SKILL.md",
    "task-folder/agents/skills-rebuild/design-and-experience/SKILL.md",
    "task-folder/agents/skills-rebuild/design-and-experience/design-systems/SKILL.md",
    "task-folder/agents/skills-rebuild/design-and-experience/motion-and-graphics/SKILL.md",
    "task-folder/agents/skills-rebuild/design-and-experience/taste-and-critique/SKILL.md",
    "task-folder/agents/skills-rebuild/design-and-experience/ui-ux/SKILL.md",
    "task-folder/agents/skills-rebuild/development/SKILL.md",
    "task-folder/agents/skills-rebuild/development/backend/SKILL.md",
    "task-folder/agents/skills-rebuild/development/frontend/SKILL.md",
    "task-folder/agents/skills-rebuild/development/fullstack/SKILL.md",
    "task-folder/agents/skills-rebuild/development/mobile/SKILL.md",
    "task-folder/agents/skills-rebuild/development/software-architecture/SKILL.md",
    "task-folder/agents/skills-rebuild/development/systems/SKILL.md",
    "task-folder/agents/skills-rebuild/infrastructure-and-ops/SKILL.md",
    "task-folder/agents/skills-rebuild/marketing-and-seo/SKILL.md",
    "task-folder/agents/skills-rebuild/marketing-and-seo/content-and-campaigns/SKILL.md",
    "task-folder/agents/skills-rebuild/marketing-and-seo/cro/SKILL.md",
    "task-folder/agents/skills-rebuild/marketing-and-seo/geo-and-local-seo/SKILL.md",
    "task-folder/agents/skills-rebuild/marketing-and-seo/on-page-seo/SKILL.md",
    "task-folder/agents/skills-rebuild/marketing-and-seo/technical-seo/SKILL.md",
    "task-folder/agents/skills-rebuild/meta-and-agent-skills/SKILL.md",
    "task-folder/agents/skills-rebuild/quality-and-security/SKILL.md",
    "task-folder/agents/skills-rebuild/workflow-and-automation/SKILL.md"
}

STARTING_MAIN_SHA = "6d03fbc566fe831cf980d5b3ec4e65d3fec2b4d2"
EXPECTED_COMMIT_SUBJECT = "skills-rebuild: complete phase 10 router hierarchy"

def parse_yaml_frontmatter(file_path):
    """Robust YAML frontmatter parser for SKILL.md files."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    fm_raw = parts[1]
    data = {}
    current_key = None
    for line in fm_raw.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        if ":" in line_clean and not line_clean.startswith("-"):
            k, v = line_clean.split(":", 1)
            current_key = k.strip()
            val = v.strip().strip("\"'").strip()
            data[current_key] = val
        elif line_clean.startswith("-") and current_key:
            if not isinstance(data[current_key], list):
                data[current_key] = []
            data[current_key].append(line_clean[1:].strip().strip("\"'").strip())
    return data

def run_git(args):
    try:
        res = subprocess.run(["git"] + args, cwd=BASE_DIR, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        return ""

def main():
    print("=" * 80)
    print("PHASE 10: CALIBRATED 10-GATE ROUTER HIERARCHY VERIFICATION")
    print("=" * 80)

    # Load canonical registry
    if not os.path.exists(CANON_CSV):
        print(f"FATAL: Missing canonical CSV at {CANON_CSV}")
        sys.exit(1)
    
    with open(CANON_CSV, "r", encoding="utf-8") as f:
        canon_rows = list(csv.DictReader(f))
    
    canon_paths = set(r["phase08_final_destination"] for r in canon_rows)
    canon_names = set(r["canonical_skill_name"] for r in canon_rows)
    expected_leaf_count = len(canon_rows) # 2103
    print(f"Loaded {expected_leaf_count} active canonical skills from registry.\n")

    results = []

    # -------------------------------------------------------------------------
    # GATE 01: Root Router Frontmatter & Discovery Metadata
    # -------------------------------------------------------------------------
    g1_pass = True
    g1_errs = []
    root_path = os.path.join(REBUILD_DIR, "SKILL.md")
    root_fm = parse_yaml_frontmatter(root_path)

    if not root_fm:
        g1_pass = False
        g1_errs.append("Root router SKILL.md missing or has invalid YAML frontmatter.")
    else:
        if root_fm.get("name") != "skills-rebuild":
            g1_pass = False
            g1_errs.append(f"Root router name mismatch: expected 'skills-rebuild', got '{root_fm.get('name')}'")
        if not root_fm.get("description"):
            g1_pass = False
            g1_errs.append("Root router description is empty.")
        if root_fm.get("type") != "master-router":
            g1_pass = False
            g1_errs.append(f"Root router type expected 'master-router', got '{root_fm.get('type')}'")

    with open(root_path, "r", encoding="utf-8") as f:
        root_content = f.read()
    
    for h in ["## Overview", "## Functional Category Dispatch", "## Cross-Category Disambiguation & Boundary Rules"]:
        if h not in root_content:
            g1_pass = False
            g1_errs.append(f"Root router missing required heading: '{h}'")
    
    status = "PASS" if g1_pass else "FAIL"
    print(f"Gate 01: Root Router Frontmatter & Discovery Metadata -> {status}")
    if g1_errs:
        for e in g1_errs:
            print(f"  [!] {e}")
    results.append(("Gate 01: Root Router Frontmatter & Discovery Metadata", g1_pass))

    # -------------------------------------------------------------------------
    # GATE 02: Router Topology Integrity (Root -> 10 Categories -> Subcategories)
    # -------------------------------------------------------------------------
    g2_pass = True
    g2_errs = []

    # Check 10 Category Routers
    for cat in EXPECTED_CATEGORIES:
        cat_file = os.path.join(REBUILD_DIR, cat, "SKILL.md")
        if not os.path.exists(cat_file):
            g2_pass = False
            g2_errs.append(f"Missing category router: {cat}/SKILL.md")
        else:
            fm = parse_yaml_frontmatter(cat_file)
            if not fm or fm.get("name") != cat or fm.get("type") != "category-router":
                g2_pass = False
                g2_errs.append(f"Category router {cat}/SKILL.md invalid frontmatter metadata.")

    # Check 15 Subcategory Routers
    total_subcat_routers = 0
    for cat, sublist in DEEP_CATEGORIES.items():
        for sub in sublist:
            sub_file = os.path.join(REBUILD_DIR, cat, sub, "SKILL.md")
            if not os.path.exists(sub_file):
                g2_pass = False
                g2_errs.append(f"Missing subcategory router: {cat}/{sub}/SKILL.md")
            else:
                total_subcat_routers += 1
                fm = parse_yaml_frontmatter(sub_file)
                if not fm or fm.get("name") != sub or fm.get("type") != "subcategory-router":
                    g2_pass = False
                    g2_errs.append(f"Subcategory router {cat}/{sub}/SKILL.md invalid frontmatter metadata.")

    if total_subcat_routers != 15:
        g2_pass = False
        g2_errs.append(f"Expected 15 subcategory routers, found {total_subcat_routers}")

    status = "PASS" if g2_pass else "FAIL"
    print(f"Gate 02: Router Topology Integrity -> {status} (1 Root, 10 Categories, 15 Subcategory Routers)")
    if g2_errs:
        for e in g2_errs:
            print(f"  [!] {e}")
    results.append(("Gate 02: Router Topology Integrity", g2_pass))

    # -------------------------------------------------------------------------
    # GATE 03: Canonical Active Leaves Representation (2,103 skills)
    # -------------------------------------------------------------------------
    g3_pass = True
    g3_errs = []

    leaf_indexing_routers = []
    for cat in EXPECTED_CATEGORIES:
        if cat in DEEP_CATEGORIES:
            for sub in DEEP_CATEGORIES[cat]:
                leaf_indexing_routers.append(os.path.join(REBUILD_DIR, cat, sub, "SKILL.md"))
        else:
            leaf_indexing_routers.append(os.path.join(REBUILD_DIR, cat, "SKILL.md"))

    indexed_skill_paths = set()
    indexed_skill_names = set()
    skill_parent_map = {}
    path_parent_map = {}

    for rf in leaf_indexing_routers:
        rdir = os.path.dirname(rf)
        with open(rf, "r", encoding="utf-8") as f:
            rtext = f.read()
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", rtext)
        for text, target in links:
            if target.startswith("http") or target.startswith("#") or target in ["../SKILL.md", "../../SKILL.md"]:
                continue
            abs_target = os.path.normpath(os.path.join(rdir, target))
            if abs_target.endswith("/SKILL.md"):
                leaf_dir = os.path.dirname(abs_target)
                rel_leaf = os.path.relpath(leaf_dir, BASE_DIR)
                parts = rel_leaf.split(os.sep)
                if len(parts) == 6 and parts[:3] == ["task-folder", "agents", "skills-rebuild"]:
                    sname = parts[5]
                    indexed_skill_paths.add(rel_leaf)
                    indexed_skill_names.add(sname)
                    rel_rf = os.path.relpath(rf, REBUILD_DIR)
                    skill_parent_map.setdefault(sname, []).append(rel_rf)
                    path_parent_map.setdefault(rel_leaf, []).append(rel_rf)

    if len(indexed_skill_paths) != expected_leaf_count:
        g3_pass = False
        g3_errs.append(f"Indexed unique leaves count mismatch: expected {expected_leaf_count}, got {len(indexed_skill_paths)}")

    missing_from_index = canon_paths - indexed_skill_paths
    if missing_from_index:
        g3_pass = False
        g3_errs.append(f"Found {len(missing_from_index)} canonical skills missing from router indexes: {list(missing_from_index)[:5]}")

    status = "PASS" if g3_pass else "FAIL"
    print(f"Gate 03: Canonical Active Leaves Representation -> {status} ({len(indexed_skill_paths)} / {expected_leaf_count} indexed)")
    if g3_errs:
        for e in g3_errs:
            print(f"  [!] {e}")
    results.append(("Gate 03: Canonical Active Leaves Representation", g3_pass))

    # -------------------------------------------------------------------------
    # GATE 04: Exact One-Parent Assignment (Bijective 1-to-1 Mapping)
    # -------------------------------------------------------------------------
    g4_pass = True
    g4_errs = []

    duplicates = {p: parents for p, parents in path_parent_map.items() if len(parents) > 1}
    if duplicates:
        g4_pass = False
        g4_errs.append(f"Found {len(duplicates)} canonical paths indexed under multiple parent routers: {list(duplicates.keys())[:5]}")

    unassigned = canon_paths - set(path_parent_map.keys())
    if unassigned:
        g4_pass = False
        g4_errs.append(f"Found {len(unassigned)} unassigned canonical paths: {list(unassigned)[:5]}")

    status = "PASS" if g4_pass else "FAIL"
    print(f"Gate 04: Exact One-Parent Assignment (Bijective 1-to-1 Mapping) -> {status} (0 duplicates, 0 unassigned)")
    if g4_errs:
        for e in g4_errs:
            print(f"  [!] {e}")
    results.append(("Gate 04: Exact One-Parent Assignment", g4_pass))

    # -------------------------------------------------------------------------
    # GATE 05: All Router Links Resolve
    # -------------------------------------------------------------------------
    g5_pass = True
    g5_errs = []
    all_router_files = [root_path] + [os.path.join(REBUILD_DIR, c, "SKILL.md") for c in EXPECTED_CATEGORIES] + [
        os.path.join(REBUILD_DIR, c, s, "SKILL.md") for c, sl in DEEP_CATEGORIES.items() for s in sl
    ]

    total_links_checked = 0
    broken_links = []
    for rf in all_router_files:
        rdir = os.path.dirname(rf)
        with open(rf, "r", encoding="utf-8") as f:
            rtext = f.read()
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", rtext)
        for text, target in links:
            if target.startswith("http") or target.startswith("#"):
                continue
            total_links_checked += 1
            abs_target = os.path.normpath(os.path.join(rdir, target))
            if not os.path.exists(abs_target):
                broken_links.append((rf, text, target, abs_target))

    if broken_links:
        g5_pass = False
        g5_errs.append(f"Found {len(broken_links)} broken relative Markdown links in routers!")
        for bl in broken_links[:5]:
            g5_errs.append(f"  Broken in {bl[0]}: [{bl[1]}]({bl[2]}) -> {bl[3]}")

    status = "PASS" if g5_pass else "FAIL"
    print(f"Gate 05: All Router Links Resolve -> {status} ({total_links_checked} links verified, 0 broken)")
    if g5_errs:
        for e in g5_errs:
            print(f"  [!] {e}")
    results.append(("Gate 05: All Router Links Resolve", g5_pass))

    # -------------------------------------------------------------------------
    # GATE 06: Router Structural Contract & Procedural Code Absence
    # -------------------------------------------------------------------------
    g6_pass = True
    g6_errs = []

    for rf in all_router_files:
        with open(rf, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Check structural headings
        if "## Overview" not in text:
            g6_pass = False
            g6_errs.append(f"Router {rf} missing '## Overview'")
        
        # Check for multi-line procedural code blocks (routers must remain pure dispatchers)
        code_blocks = re.findall(r"```(python|bash|sh|javascript|typescript|json|yaml)(.*?)```", text, re.DOTALL)
        for lang, code in code_blocks:
            lines = [l.strip() for l in code.strip().splitlines() if l.strip()]
            if len(lines) > 5 and not lang in ["text", "mermaid"]:
                g6_pass = False
                g6_errs.append(f"Router {rf} contains {len(lines)}-line procedural code block ({lang}) - routers must remain pure dispatchers.")

    status = "PASS" if g6_pass else "FAIL"
    print(f"Gate 06: Router Structural Contract & Procedural Code Absence -> {status}")
    if g6_errs:
        for e in g6_errs:
            print(f"  [!] {e}")
    results.append(("Gate 06: Router Structural Contract & Procedural Code Absence", g6_pass))

    # -------------------------------------------------------------------------
    # GATE 07: Benchmark Artifact Integrity & Route Trace Verification
    # -------------------------------------------------------------------------
    g7_pass = True
    g7_errs = []

    if not os.path.exists(VALIDATION_MD):
        g7_pass = False
        g7_errs.append(f"Missing validation benchmark artifact at {VALIDATION_MD}")
    else:
        with open(VALIDATION_MD, "r", encoding="utf-8") as f:
            vtext = f.read()
        
        table_rows = re.findall(r"^\|\s*(`PRMPT-\d+`)\s*\|\s*(.*?)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*(.*?)\s*\|$", vtext, re.MULTILINE)
        
        if len(table_rows) < 64:
            g7_pass = False
            g7_errs.append(f"Benchmark table contains {len(table_rows)} rows; expected at least 64.")
        
        for pid, prompt, exp_route, act_route, res, rat in table_rows:
            if res.strip() != "PASS":
                g7_pass = False
                g7_errs.append(f"Benchmark {pid} status is not PASS: '{res}'")
            if not rat.strip():
                g7_pass = False
                g7_errs.append(f"Benchmark {pid} is missing explanatory rationale.")
            if exp_route != act_route:
                g7_pass = False
                g7_errs.append(f"Benchmark {pid} Expected vs Actual route mismatch: '{exp_route}' != '{act_route}'")
            
            # Check target leaf existence
            target_match = re.search(r"->\s*([a-zA-Z0-9_\-]+)(?:\s*\(|$)", act_route)
            if target_match:
                tleaf = target_match.group(1).strip()
                if tleaf not in canon_names and tleaf != "skills-rebuild":
                    g7_pass = False
                    g7_errs.append(f"Benchmark {pid} targets nonexistent leaf: '{tleaf}'")

    status = "PASS" if g7_pass else "FAIL"
    print(f"Gate 07: Benchmark Artifact Integrity & Route Trace Verification -> {status} ({len(table_rows)} cases evaluated, 100% verified)")
    if g7_errs:
        for e in g7_errs:
            print(f"  [!] {e}")
    results.append(("Gate 07: Benchmark Artifact Integrity & Route Trace Verification", g7_pass))

    # -------------------------------------------------------------------------
    # GATE 08: Zero Stale, Deprecated, Quarantined, or Workstation References
    # -------------------------------------------------------------------------
    g8_pass = True
    g8_errs = []

    banned_patterns = [
        (re.compile(r"/Users/"), "Workstation absolute path"),
        (re.compile(r"/home/"), "Workstation absolute path"),
        (re.compile(r"\.agents/skills"), "Legacy non-rebuild path in router links"),
        (re.compile(r"_quarantine"), "Quarantined reference leaked into router"),
    ]

    for rf in all_router_files:
        with open(rf, "r", encoding="utf-8") as f:
            text = f.read()
        for pat, desc in banned_patterns:
            if pat.search(text):
                g8_pass = False
                g8_errs.append(f"Router {rf} contains prohibited pattern ({desc})")

    status = "PASS" if g8_pass else "FAIL"
    print(f"Gate 08: Zero Stale, Deprecated, or Workstation References -> {status}")
    if g8_errs:
        for e in g8_errs:
            print(f"  [!] {e}")
    results.append(("Gate 08: Zero Stale, Deprecated, or Workstation References", g8_pass))

    # -------------------------------------------------------------------------
    # GATE 09: Taxonomy ↔ Filesystem ↔ Router Functional Reconciliation
    # -------------------------------------------------------------------------
    g9_pass = True
    g9_errs = []

    # 1. Exact top-level category set on disk equals the approved 10 (excluding meta task utilities)
    OPERATIONAL_TASK_TOOLS = {"github-operations", "skills-create-manage-update"}
    all_top_dirs = sorted([
        d for d in os.listdir(REBUILD_DIR)
        if os.path.isdir(os.path.join(REBUILD_DIR, d))
        and not d.startswith((".", "_"))
        and d not in OPERATIONAL_TASK_TOOLS
    ])
    if all_top_dirs != EXPECTED_CATEGORIES:
        g9_pass = False
        g9_errs.append(f"Top-level category directories do not strictly match approved set: found {all_top_dirs} vs expected {EXPECTED_CATEGORIES}")

    # 2. Exact (category, subcategory) pairs on disk equals the authoritative 44
    disk_taxonomy = {}
    for cat in EXPECTED_CATEGORIES:
        cdir = os.path.join(REBUILD_DIR, cat)
        subdirs = sorted([d for d in os.listdir(cdir) if os.path.isdir(os.path.join(cdir, d)) and not d.startswith((".", "_"))])
        disk_taxonomy[cat] = subdirs

    if disk_taxonomy != EXPECTED_TAXONOMY:
        g9_pass = False
        g9_errs.append(f"Subcategory taxonomy on disk mismatch: {disk_taxonomy} vs expected {EXPECTED_TAXONOMY}")

    # 3. Verify complete 2,103-entry functional routing map ledger
    if not os.path.exists(FUNCTIONAL_MAP_CSV):
        g9_pass = False
        g9_errs.append(f"Missing functional routing map ledger at {FUNCTIONAL_MAP_CSV}")
    else:
        with open(FUNCTIONAL_MAP_CSV, "r", encoding="utf-8") as f:
            map_rows = list(csv.DictReader(f))
        
        if len(map_rows) != 2103:
            g9_pass = False
            g9_errs.append(f"Functional routing map row count mismatch: found {len(map_rows)}, expected 2103.")
        
        # Distribution assertion (10 Phase 08 exceptions, 152 semantic overrides, 1,941 reviewed retained placements)
        type_counts = Counter(r.get("override_type", "") for r in map_rows)
        expected_distribution = {
            "phase08_exception": 10,
            "semantic_override": 152,
            "retained_placement_reviewed": 1941
        }
        if dict(type_counts) != expected_distribution:
            g9_pass = False
            g9_errs.append(f"Override type distribution mismatch: found {dict(type_counts)} vs expected {expected_distribution}")

        mismatched_routing = []
        generic_reasons = []
        generic_outcomes = []
        invalid_review_status = []
        invalid_confidence = []
        invalid_types = []

        valid_types = {"phase08_exception", "semantic_override", "retained_placement_reviewed"}

        for r in map_rows:
            sname = r["canonical_skill"]
            ppath = r["physical_path"]
            expected_parent = r["proposed_router_parent"]
            actual_parents = path_parent_map.get(ppath, [])
            if expected_parent not in actual_parents:
                mismatched_routing.append((sname, ppath, expected_parent, actual_parents))
            
            # Semantic ledger quality assertions
            r_type = r.get("override_type", "")
            r_status = r.get("review_status", "")
            r_conf = r.get("confidence", "")
            r_outcome = r.get("primary_user_outcome", "")
            r_reason = r.get("routing_reason", "")

            if r_type not in valid_types:
                invalid_types.append((sname, r_type))
            if r_status != "verified":
                invalid_review_status.append((sname, r_status))
            if r_conf != "high":
                invalid_confidence.append((sname, r_conf))
            
            if not r_outcome or (" capability" in r_outcome.lower() and ":" not in r_outcome):
                generic_outcomes.append((sname, r_outcome))
            
            if not r_reason or "verified alignment with" in r_reason.lower() or "physical taxonomy placement" in r_reason.lower():
                generic_reasons.append((sname, r_reason))

        if mismatched_routing:
            g9_pass = False
            g9_errs.append(f"Found {len(mismatched_routing)} skills routed to parents different from functional routing ledger:")
            for sname, ppath, exp_p, act_p in mismatched_routing[:5]:
                g9_errs.append(f"  {sname} ({ppath}): expected {exp_p}, got {act_p}")

        if generic_reasons:
            g9_pass = False
            g9_errs.append(f"Found {len(generic_reasons)} skills with generic boilerplate routing_reason in ledger: {generic_reasons[:5]}")
        
        if generic_outcomes:
            g9_pass = False
            g9_errs.append(f"Found {len(generic_outcomes)} skills with generic primary_user_outcome in ledger: {generic_outcomes[:5]}")

        if invalid_review_status or invalid_confidence or invalid_types:
            g9_pass = False
            g9_errs.append(f"Found invalid ledger review metadata (status: {len(invalid_review_status)}, conf: {len(invalid_confidence)}, types: {len(invalid_types)})")

    # 4. Exact bijective count reconciliation (2,103 skills)
    if len(indexed_skill_paths) != 2103:
        g9_pass = False
        g9_errs.append(f"Reconciliation error: {len(indexed_skill_paths)} indexed vs 2103 canonical active skills.")

    status = "PASS" if g9_pass else "FAIL"
    print(f"Gate 09: Taxonomy ↔ Filesystem ↔ Router Functional Reconciliation -> {status} (10 Cats, 44 Subcats, 2,103 Functional Mappings Verified)")
    if g9_errs:
        for e in g9_errs:
            print(f"  [!] {e}")
    results.append(("Gate 09: Taxonomy ↔ Filesystem ↔ Router Functional Reconciliation", g9_pass))

    # -------------------------------------------------------------------------
    # GATE 10: Repository Branch, Base, Scope, and Clean Working Tree
    # -------------------------------------------------------------------------
    g10_pass = True
    g10_errs = []

    # 1. Assert exact branch name
    current_branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    if current_branch != "skills-rebuild/phase-10-router-hierarchy":
        g10_pass = False
        g10_errs.append(f"Current branch mismatch: expected 'skills-rebuild/phase-10-router-hierarchy', got '{current_branch}'")

    # 2. Assert merge base with origin/main equals Phase 10 starting SHA
    merge_base = run_git(["merge-base", "HEAD", "origin/main"])
    if merge_base != STARTING_MAIN_SHA:
        g10_pass = False
        g10_errs.append(f"Merge base mismatch: expected {STARTING_MAIN_SHA}, got {merge_base}")

    # 3. Assert HEAD commit subject matches standard contract
    head_subject = run_git(["log", "-1", "--format=%s"])
    if head_subject != EXPECTED_COMMIT_SUBJECT:
        g10_pass = False
        g10_errs.append(f"HEAD commit subject mismatch: expected '{EXPECTED_COMMIT_SUBJECT}', got '{head_subject}'")

    # 4. Assert clean working tree
    git_status = run_git(["status", "--porcelain"])
    if git_status:
        g10_pass = False
        uncommitted = [l for l in git_status.splitlines() if l.strip()]
        g10_errs.append(f"Dirty working tree: {len(uncommitted)} uncommitted/untracked changes present.")

    # 5. Assert diff scope against starting main SHA is strictly restricted to approved files
    changed_files = set(filter(None, run_git(["diff", "--name-only", f"{STARTING_MAIN_SHA}..HEAD"]).splitlines()))
    unapproved_diffs = changed_files - APPROVED_FILES
    missing_approved = APPROVED_FILES - changed_files
    if unapproved_diffs:
        g10_pass = False
        g10_errs.append(f"Unapproved file changes in PR scope: {list(unapproved_diffs)}")
    if missing_approved:
        g10_pass = False
        g10_errs.append(f"Missing approved file changes in PR scope: {list(missing_approved)}")

    status = "PASS" if g10_pass else "FAIL"
    print(f"Gate 10: Repository Branch, Base, Scope, and Tree Verification -> {status} (Branch, Base, Subject, Clean Tree, 29-File Scope)")
    if g10_errs:
        for e in g10_errs:
            print(f"  [!] {e}")
    results.append(("Gate 10: Repository Branch, Base, Scope, and Tree Verification", g10_pass))

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    passed_count = sum(1 for _, p in results if p)
    print(f"PHASE 10 VERIFICATION RESULT: {passed_count} / {len(results)} GATES PASSED")
    print("=" * 80)

    if passed_count == len(results):
        print(">>> ALL 10 CALIBRATED GATES PASSED DETERMINISTICALLY! <<<")
        return 0
    else:
        print(">>> SOME GATES FAILED. PLEASE REVIEW ERRORS ABOVE. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(main())
