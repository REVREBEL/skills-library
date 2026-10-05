#!/usr/bin/env python3
"""
Phase 12 Pilot & Publication Verification Suite
Validates all Task 12 release invariants:
- Gate 01: Preconditions & non-blocking unresolved items check (UNRES-01, UNRES-02)
- Gate 02: Active Universe & Router Traversability (26 routers, 2,177 links, 2,103 leaves 1:1)
- Gate 03: Representative Pilot Scenarios Routing Integrity (expected == actual route, link resolution)
- Gate 04: Pilot Defect Remediation & Provider Decoupling (travel-planner, deliverability-checker)
- Gate 05: Portability & Workstation Absolute Path Sanitization (0 leaks across 7 approved files)
- Gate 06: Phase 12 Artifacts Completeness & Reconciliation Invariant (dynamic HEAD readback)
- Gate 07: Git Hygiene, Branch, Merge Base & Diff Scope Invariant (exact 7-file diff scope enforced)
"""

import os
import re
import sys
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
TASK_FOLDER = os.path.join(REPO_ROOT, "task-folder/agents/skills-rebuild")
AUDIT_DIR = os.path.join(TASK_FOLDER, "_audit")
STARTING_MAIN_SHA = "8a106d4f7b3bd82e897b11c054c2584d3aeb6260"
EXPECTED_BRANCH = "skills-rebuild/phase-12-pilot-publish"
EXPECTED_COMMIT_SUBJECT = "skills-rebuild: complete phase 12 pilot and publication"

APPROVED_DIFF_SCOPE = {
    "task-folder/agents/skills-rebuild/_audit/gen_phase12_artifacts.py",
    "task-folder/agents/skills-rebuild/_audit/pilot-report.md",
    "task-folder/agents/skills-rebuild/_audit/pr_12_body.md",
    "task-folder/agents/skills-rebuild/_audit/publication-record.md",
    "task-folder/agents/skills-rebuild/_audit/verify_phase_12.py",
    "task-folder/agents/skills-rebuild/design-and-experience/ui-ux/travel-planner/SKILL.md",
    "task-folder/agents/skills-rebuild/quality-and-security/debugging/deliverability-checker/SKILL.md",
}

def run_git(args):
    res = subprocess.run(["git"] + args, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\n{res.stderr}")
    return res.stdout.strip()

def parse_simple_frontmatter(file_path):
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
    for line in fm_raw.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        if ":" in line_clean and not line_clean.startswith("-"):
            k, v = line_clean.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'").strip()
    return data

# ==============================================================================
# GATE 01: Preconditions & Non-Blocking Unresolved Items
# ==============================================================================
def verify_gate_01():
    precondition_files = [
        os.path.join(AUDIT_DIR, "validation-report.md"),
        os.path.join(AUDIT_DIR, "unresolved-items.md"),
        os.path.join(AUDIT_DIR, "router-validation.md"),
        os.path.join(REPO_ROOT, ".agents/skills/SKILL.md")
    ]
    for fp in precondition_files:
        assert os.path.exists(fp), f"Missing precondition file: {fp}"

    unres_path = os.path.join(AUDIT_DIR, "unresolved-items.md")
    with open(unres_path, "r", encoding="utf-8") as f:
        unres_text = f.read()

    assert "UNRES-01" in unres_text, "UNRES-01 missing from unresolved-items.md"
    assert "UNRES-02" in unres_text, "UNRES-02 missing from unresolved-items.md"
    assert "NON-BLOCKING" in unres_text, "Non-blocking status not confirmed in unresolved-items.md"

    evidence = "All 4 required precondition files present; UNRES-01 and UNRES-02 verified non-blocking for hierarchical routing."
    return {"gate": "Gate 01", "name": "Preconditions & Unresolved Items Invariant", "status": "PASSED", "evidence": evidence}

# ==============================================================================
# GATE 02: Active Universe & Router Traversability
# ==============================================================================
def verify_gate_02():
    canonical_csv = os.path.join(AUDIT_DIR, "phase08-canonical-registry.csv")
    with open(canonical_csv, "r", encoding="utf-8") as f:
        lines = [line.strip().split(",") for line in f if line.strip()][1:]

    active_paths = [row[1] for row in lines]
    assert len(active_paths) == 2103, f"Expected 2103 active skills, found {len(active_paths)}"

    for rel_path in active_paths:
        full_path = os.path.join(REPO_ROOT, rel_path, "SKILL.md")
        assert os.path.exists(full_path), f"Missing active skill: {rel_path}"

    deep_categories = {
        "development": ["backend", "frontend", "fullstack", "mobile", "software-architecture", "systems"],
        "marketing-and-seo": ["content-and-campaigns", "cro", "geo-and-local-seo", "on-page-seo", "technical-seo"],
        "design-and-experience": ["design-systems", "motion-and-graphics", "taste-and-critique", "ui-ux"]
    }
    flat_categories = [
        "business-and-operations", "content-and-documentation", "data-and-ai",
        "infrastructure-and-ops", "meta-and-agent-skills", "quality-and-security",
        "workflow-and-automation"
    ]

    root_router = os.path.join(TASK_FOLDER, "SKILL.md")
    assert os.path.exists(root_router), "Root SKILL.md missing"

    category_routers = []
    subcategory_routers = []

    for cat, subcats in deep_categories.items():
        cat_file = os.path.join(TASK_FOLDER, cat, "SKILL.md")
        assert os.path.exists(cat_file), f"Category router missing: {cat_file}"
        category_routers.append(cat_file)
        for subcat in subcats:
            subcat_file = os.path.join(TASK_FOLDER, cat, subcat, "SKILL.md")
            assert os.path.exists(subcat_file), f"Subcategory router missing: {subcat_file}"
            subcategory_routers.append(subcat_file)

    for cat in flat_categories:
        cat_file = os.path.join(TASK_FOLDER, cat, "SKILL.md")
        assert os.path.exists(cat_file), f"Flat category router missing: {cat_file}"
        category_routers.append(cat_file)

    assert len(category_routers) == 10, f"Expected 10 category routers, found {len(category_routers)}"
    assert len(subcategory_routers) == 15, f"Expected 15 subcategory routers, found {len(subcategory_routers)}"
    all_routers = [root_router] + category_routers + subcategory_routers
    assert len(all_routers) == 26, f"Expected 26 total routers, found {len(all_routers)}"

    # Full router traversability scan (Phase 11 parity)
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    total_router_links = 0
    leaf_links = []

    for r_path in all_routers:
        with open(r_path, "r", encoding="utf-8") as f:
            content = f.read()
        r_dir = os.path.dirname(r_path)
        for m in link_pattern.finditer(content):
            target = m.group(2).split("#")[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            total_router_links += 1
            abs_target = os.path.normpath(os.path.join(r_dir, target))
            assert os.path.exists(abs_target), f"Broken router link in {r_path}: {target} -> {abs_target}"
            if os.path.basename(abs_target) == "SKILL.md":
                fm = parse_simple_frontmatter(abs_target)
                if fm and fm.get("type") not in ["master-router", "category-router", "subcategory-router"]:
                    leaf_links.append(abs_target)

    assert total_router_links == 2177, f"Total router links {total_router_links} != 2177"
    assert len(leaf_links) == 2103, f"Leaf links count {len(leaf_links)} != 2103"
    assert len(set(leaf_links)) == 2103, f"Duplicate leaf links found in router hierarchy"

    evidence = (
        f"26 routers (1 Master Root + 10 Category + 15 Subcategory) contain exactly 2,177 total links and "
        f"index all 2,103 canonical active leaf skills with 1:1 bijective coverage (0 orphan skills, 0 duplicates)."
    )
    return {"gate": "Gate 02", "name": "Active Universe & Router Traversability Invariant", "status": "PASSED", "evidence": evidence}

# ==============================================================================
# GATE 03: Representative Pilot Scenarios Routing Integrity
# ==============================================================================
def verify_gate_03():
    from gen_phase12_artifacts import PILOT_SCENARIOS
    assert len(PILOT_SCENARIOS) == 8, f"Expected 8 pilot scenarios, found {len(PILOT_SCENARIOS)}"

    trigger_regex = re.compile(r"^[A-Z].*\.\s+Use when\b")
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for s in PILOT_SCENARIOS:
        # 1. Assert expected functional route matches actual functional route
        assert s["expected_route"] == s["actual_route"], f"Scenario {s['id']}: expected route '{s['expected_route']}' != actual '{s['actual_route']}'"

        # 2. Verify router file exists on disk
        router_full = os.path.join(REPO_ROOT, s["router_path"])
        assert os.path.exists(router_full), f"Scenario {s['id']}: router file missing: {s['router_path']}"

        # 3. Read router content and extract all markdown links
        with open(router_full, "r", encoding="utf-8") as f:
            router_content = f.read()

        router_links = [m.group(2).split("#")[0] for m in link_pattern.finditer(router_content)]
        assert s["link_target_in_router"] in router_links, \
            f"Scenario {s['id']}: link target '{s['link_target_in_router']}' not found in router '{s['router_path']}'"

        # 4. Resolve link target from router location to child skill
        router_dir = os.path.dirname(router_full)
        resolved_child = os.path.normpath(os.path.join(router_dir, s["link_target_in_router"]))
        expected_child = os.path.normpath(os.path.join(REPO_ROOT, s["child_skill"]))
        assert resolved_child == expected_child, \
            f"Scenario {s['id']}: resolved child '{resolved_child}' != expected child '{expected_child}'"

        # 5. Verify child skill file exists on disk
        assert os.path.exists(resolved_child), f"Scenario {s['id']}: child skill file does not exist: {resolved_child}"

        # 6. Verify frontmatter name and description trigger contract
        with open(resolved_child, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        assert match, f"Scenario {s['id']}: missing frontmatter in {s['child_skill']}"
        fm_block = match.group(1)
        name_match = re.search(r"^name:\s*[\"']?([^\"'\n]+)[\"']?", fm_block, re.MULTILINE)
        desc_match = re.search(r"^description:\s*[\"']?([^\"\n]+|(?:\n\s+.*)+)", fm_block, re.MULTILINE)
        assert name_match and desc_match, f"Scenario {s['id']}: invalid frontmatter keys in {s['child_skill']}"
        desc = desc_match.group(1).replace("\n", " ").strip()
        assert trigger_regex.search(desc), f"Scenario {s['id']}: trigger contract failed in {s['child_skill']}: {desc[:50]}"

    evidence = "All 8 pilot scenarios verified: expected_route == actual_route, direct router markdown link resolution, child existence, and valid trigger contracts."
    return {"gate": "Gate 03", "name": "Representative Pilot Scenarios Routing Integrity", "status": "PASSED", "evidence": evidence}

# ==============================================================================
# GATE 04: Pilot Defect Remediation & Provider Decoupling
# ==============================================================================
def verify_gate_04():
    tp_path = os.path.join(TASK_FOLDER, "design-and-experience/ui-ux/travel-planner/SKILL.md")
    with open(tp_path, "r", encoding="utf-8") as f:
        tp_text = f.read()

    assert "Claude" not in tp_text, "Defect DEF-01 unresolved: 'Claude' found in travel-planner/SKILL.md"

    dc_path = os.path.join(TASK_FOLDER, "quality-and-security/debugging/deliverability-checker/SKILL.md")
    with open(dc_path, "r", encoding="utf-8") as f:
        dc_text = f.read()

    assert "Claude" not in dc_text, "Defect DEF-02 unresolved: 'Claude' found in deliverability-checker/SKILL.md"

    # Test travel_db.py execution
    res = subprocess.run([sys.executable, "scripts/travel_db.py", "is_initialized"],
                         cwd=os.path.join(TASK_FOLDER, "design-and-experience/ui-ux/travel-planner"),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"travel_db.py execution failed: {res.stderr}"
    assert res.stdout.strip() in ["true", "false"], f"Unexpected travel_db.py output: {res.stdout}"

    evidence = "Defects DEF-01 and DEF-02 fully remediated; 0 occurrences of 'Claude'; travel_db.py script operational."
    return {"gate": "Gate 04", "name": "Pilot Defect Remediation & Provider Decoupling Invariant", "status": "PASSED", "evidence": evidence}

# ==============================================================================
# GATE 05: Portability & Workstation Absolute Path Sanitization
# ==============================================================================
def verify_gate_05():
    banned_patterns = [
        re.compile(r"/Users/[a-zA-Z0-9_-]+"),
        re.compile(r"/home/[a-zA-Z0-9_-]+"),
        re.compile(r"[A-Za-z]:\\[Uu]sers\\[a-zA-Z0-9_-]+"),
        re.compile(r"\\\\[a-zA-Z0-9_.-]+\\[a-zA-Z0-9_.-]+"),
        re.compile(r"/mnt/[a-zA-Z0-9_.-]+"),
        re.compile(r"/media/[a-zA-Z0-9_.-]+"),
        re.compile(r"/Volumes/[a-zA-Z0-9_.-]+")
    ]

    for rel_f in APPROVED_DIFF_SCOPE:
        full_f = os.path.join(REPO_ROOT, rel_f)
        if not os.path.exists(full_f):
            continue
        with open(full_f, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for pat in banned_patterns:
            matches = pat.findall(content)
            assert not matches, f"Path leak in {rel_f}: {matches}"

    evidence = f"0 workstation-specific absolute path leaks found across all {len(APPROVED_DIFF_SCOPE)} approved files."
    return {"gate": "Gate 05", "name": "Portability & Workstation Path Sanitization Invariant", "status": "PASSED", "evidence": evidence}

# ==============================================================================
# GATE 06: Phase 12 Artifacts Completeness & Reconciliation
# ==============================================================================
def verify_gate_06():
    pilot_rep = os.path.join(AUDIT_DIR, "pilot-report.md")
    pub_rec = os.path.join(AUDIT_DIR, "publication-record.md")

    assert os.path.exists(pilot_rep), "pilot-report.md missing"
    assert os.path.exists(pub_rec), "publication-record.md missing"

    with open(pilot_rep, "r", encoding="utf-8") as f:
        pilot_text = f.read()
    with open(pub_rec, "r", encoding="utf-8") as f:
        pub_text = f.read()

    assert "PILOT-01" in pilot_text and "PILOT-08" in pilot_text, "pilot-report.md missing scenario coverage"
    assert "DEF-01" in pilot_text and "DEF-02" in pilot_text, "pilot-report.md missing defect ledger"
    assert "05972f2e" in pilot_text and "05972f2e" in pub_text, "Focused repair commit 05972f2e not linked in artifacts"

    # Dynamic HEAD query
    head_sha = run_git(["rev-parse", "HEAD"])
    head_subject = run_git(["log", "-1", "--format=%s"])
    assert head_subject == EXPECTED_COMMIT_SUBJECT, f"HEAD subject '{head_subject}' != '{EXPECTED_COMMIT_SUBJECT}'"

    evidence = f"Artifacts complete, reconciled to repair commit 05972f2e and dynamic HEAD {head_sha[:8]} ('{head_subject}')."
    return {"gate": "Gate 06", "name": "Phase 12 Artifacts Completeness & Reconciliation Invariant", "status": "PASSED", "evidence": evidence}

# ==============================================================================
# GATE 07: Git Hygiene, Branch, Merge Base & Diff Scope Invariant
# ==============================================================================
def verify_gate_07():
    current_branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    assert current_branch == EXPECTED_BRANCH, f"Current branch '{current_branch}' != '{EXPECTED_BRANCH}'"

    merge_base = run_git(["merge-base", "HEAD", "origin/main"])
    assert merge_base == STARTING_MAIN_SHA, f"Merge base '{merge_base}' != '{STARTING_MAIN_SHA}'"

    commits = run_git(["log", "--oneline", f"{STARTING_MAIN_SHA}..HEAD"]).splitlines()
    assert len(commits) >= 2, f"Expected at least 2 commits on branch, found {len(commits)}"
    assert any("05972f2e" in c or "fix(skills): remove provider-specific coupling" in c for c in commits), \
        "Repair commit 05972f2e missing from branch history"

    diff_files = set(run_git(["diff", "--name-only", f"{STARTING_MAIN_SHA}..HEAD"]).splitlines())
    assert diff_files == APPROVED_DIFF_SCOPE, f"Cumulative diff does not match approved scope. Difference: {diff_files ^ APPROVED_DIFF_SCOPE}"

    evidence = f"Branch '{EXPECTED_BRANCH}' based on main '{STARTING_MAIN_SHA[:8]}', repair commit present, exact 7-file diff scope verified."
    return {"gate": "Gate 07", "name": "Git Hygiene, Branch, Merge Base & Diff Scope Invariant", "status": "PASSED", "evidence": evidence}

def run_all_gates():
    gates = [
        verify_gate_01,
        verify_gate_02,
        verify_gate_03,
        verify_gate_04,
        verify_gate_05,
        verify_gate_06,
        verify_gate_07
    ]
    print("=" * 80)
    print("RUNNING PHASE 12 PILOT & PUBLICATION VERIFICATION SUITE")
    print("=" * 80)
    passed = 0
    for g in gates:
        try:
            res = g()
            print(f"[{res['status']:<17}] {res['gate']}: {res['name']}")
            passed += 1
        except Exception as e:
            print(f"[FAILED           ] {g.__name__}: {e}")
            sys.exit(1)

    print("-" * 80)
    print(f"Validation Summary: {passed} PASSED | 0 FAILED")
    print("=" * 80)

if __name__ == "__main__":
    run_all_gates()
