"""
Automated Test Suite for Task 13 Scenarios A through H.
Tests manual intake, external installer simulation, sync idempotency,
broken link repair, name collision halts, semantic overlap detection,
and dedicated regression tests for skills.sh new installs and updates.

ALL tests execute in fully isolated temporary fixtures and NEVER mutate
the production library, runtime links, manifest, routers, or ledger.
"""

import copy
import json
import os
import shutil
import sys
import tempfile
import unittest

# Ensure tools directory is in sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TEST_DIR)
TOOLS_DIR = os.path.join(REPO_ROOT, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from unittest.mock import patch

from skill_library.intake import (
    add_link_to_router,
    apply_candidate,
    evaluate_candidate,
    normalize_package_content,
)
from skill_library.ledger import ChangeLedger
from skill_library.manifest import RuntimeManifest
from skill_library.pilot import PilotResult, run_targeted_pilot
from skill_library.scanner import scan_candidate_directory, scan_runtime
from skill_library.sync import reconcile_runtime_symlinks
from skill_library.validator import validate_single_skill


class TestSkillLibraryIsolatedScenarios(unittest.TestCase):
    """
    Completely isolated test suite operating in a temporary sandbox.
    Guarantees zero pollution of production library, runtime, manifest, or ledger.
    """

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.sandbox = self.tmp_dir.name

        # Create isolated directory structure
        self.library_dir = os.path.join(self.sandbox, "library")
        self.runtime_dir = os.path.join(self.sandbox, ".agents", "skills")
        self.intake_dir = os.path.join(self.sandbox, "intake")
        self.audit_dir = os.path.join(self.sandbox, "audit")

        os.makedirs(self.library_dir, exist_ok=True)
        os.makedirs(self.runtime_dir, exist_ok=True)
        os.makedirs(self.intake_dir, exist_ok=True)
        os.makedirs(self.audit_dir, exist_ok=True)

        self.manifest_file = os.path.join(self.audit_dir, "runtime-manifest.json")
        self.ledger_file = os.path.join(self.audit_dir, "change-ledger.jsonl")

        self.manifest = RuntimeManifest(manifest_path=self.manifest_file)
        self.ledger = ChangeLedger(ledger_path=self.ledger_file)

        # Create sample routers
        self.root_router = os.path.join(self.library_dir, "SKILL.md")
        with open(self.root_router, "w", encoding="utf-8") as f:
            f.write("# Root Router\n\n| Category | Link |\n|---|---|\n| Quality | quality-and-security/SKILL.md |\n")

        self.qs_router = os.path.join(self.library_dir, "quality-and-security", "SKILL.md")
        os.makedirs(os.path.dirname(self.qs_router), exist_ok=True)
        with open(self.qs_router, "w", encoding="utf-8") as f:
            f.write("# Quality and Security Router\n\n### debugging\n\n| Skill | Description |\n|---|---|\n")

        self.wa_router = os.path.join(self.library_dir, "workflow-and-automation", "SKILL.md")
        os.makedirs(os.path.dirname(self.wa_router), exist_ok=True)
        with open(self.wa_router, "w", encoding="utf-8") as f:
            f.write("# Workflow and Automation Router\n\n### tool-integration\n\n| Skill | Description |\n|---|---|\n")

        # Seed an existing canonical skill: bug-hunter
        self.seed_existing_skill(
            category="quality-and-security",
            subcategory="debugging",
            name="bug-hunter",
            description="Autonomous system to identify and capture code bugs. Use when hunting application defects.",
            router_path=self.qs_router,
        )

        # Seed an existing canonical skill: existing-tool
        self.seed_existing_skill(
            category="workflow-and-automation",
            subcategory="tool-integration",
            name="existing-tool",
            description="Standard automation helper v1. Use when running automation scripts.",
            router_path=self.wa_router,
        )

        # Establish runtime symlinks
        reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def seed_existing_skill(self, category: str, subcategory: str, name: str, description: str, router_path: str):
        pkg_dir = os.path.join(self.library_dir, category, subcategory, name)
        os.makedirs(pkg_dir, exist_ok=True)
        skill_md = os.path.join(pkg_dir, "SKILL.md")
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(f"""---
name: {name}
description: {description}
---
# {name.title()}
Instructions for {name}.
""")
        # Update router
        add_link_to_router(
            router_path=router_path,
            skill_name=name,
            skill_dir_path=pkg_dir,
            subcategory=subcategory,
            description=description,
        )
        # Register in manifest
        canonical_rel = os.path.relpath(pkg_dir, self.sandbox).replace(os.sep, "/")
        router_rel = os.path.relpath(router_path, self.sandbox).replace(os.sep, "/")
        self.manifest.add_skill(
            runtime_name=name,
            canonical_name=name,
            canonical_path=canonical_rel,
            functional_parent=router_rel,
            source="seed",
            managed=True,
        )
        self.manifest.save()

    def test_scenario_c_idempotent_sync(self):
        """Scenario C: sync against already-synchronized library produces zero changes."""
        report = reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
        )
        self.assertEqual(len(report.created), 0)
        self.assertEqual(len(report.repaired), 0)
        self.assertEqual(len(report.staged_to_intake), 0)
        self.assertEqual(len(report.collisions), 0)
        self.assertEqual(len(report.errors), 0)
        self.assertFalse(report.has_changes)

    def test_scenario_d_broken_link_repair(self):
        """Scenario D: broken managed link is identified and repaired."""
        test_symlink_name = "bug-hunter"
        sym_path = os.path.join(self.runtime_dir, test_symlink_name)
        self.assertTrue(os.path.islink(sym_path))

        # Deliberately point symlink to non-existent target
        os.unlink(sym_path)
        os.symlink("../../library/non_existent_path", sym_path)
        self.assertFalse(os.path.exists(sym_path))

        # Run sync
        report = reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
        )
        self.assertIn(f"{test_symlink_name} -> library/quality-and-security/debugging/bug-hunter", report.repaired)
        self.assertTrue(os.path.exists(sym_path))

    def test_scenario_e_name_collision(self):
        """Scenario E: new skill using existing canonical name triggers collision halt."""
        collision_name = "bug-hunter"
        cand_dir = os.path.join(self.intake_dir, collision_name)
        os.makedirs(cand_dir, exist_ok=True)

        skill_md_content = """---
name: bug-hunter
description: Brand new alternative debugger. Use when hunting application defects.
---
# Bug Hunter
Alternative tool.
"""
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(skill_md_content)

        ev = evaluate_candidate(
            candidate_name=collision_name,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            manifest=self.manifest,
        )
        self.assertTrue(ev.name_collision)
        self.assertTrue(ev.approval_required)
        self.assertTrue(any("collision" in r.lower() or "duplicate" in r.lower() for r in ev.approval_reasons))

    def test_scenario_f_semantic_overlap(self):
        """Scenario F: skill with high semantic overlap recommends MERGE and halts for review."""
        cand_name = "smart-bug-finder"
        cand_dir = os.path.join(self.intake_dir, cand_name)
        os.makedirs(cand_dir, exist_ok=True)

        skill_md_content = """---
name: smart-bug-finder
description: Autonomous system to identify, capture, and hunt code bugs and defects. Use when hunting application defects or debugging bugs.
---
# Smart Bug Finder
Tool for debugging issues.
"""
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(skill_md_content)

        ev = evaluate_candidate(
            candidate_name=cand_name,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            manifest=self.manifest,
        )
        self.assertTrue(ev.approval_required)
        self.assertIn(ev.recommended_decision, ["MERGE", "KEEP_SEPARATE"])
        self.assertTrue(len(ev.semantic_competitors) > 0)
        top_match = ev.semantic_competitors[0]
        self.assertEqual(top_match["name"], "bug-hunter")
        self.assertGreater(top_match["similarity"], 0.25)

    def test_scenario_a_manual_intake_end_to_end(self):
        """Scenario A: manual intake candidate evaluated, approved, applied to library, symlinked, and piloted."""
        cand_name = "scenario-a-collector"
        cand_dir = os.path.join(self.intake_dir, cand_name)
        os.makedirs(os.path.join(cand_dir, "scripts"), exist_ok=True)

        # 1. Author new skill in intake/
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: scenario-a-collector
description: High-throughput telemetry and metric collection daemon. Use when collecting custom performance metrics or configuring agent telemetry.
---
# Scenario A Collector
Detailed instructions.
""")
        with open(os.path.join(cand_dir, "scripts", "run.py"), "w", encoding="utf-8") as f:
            f.write("import sys\nprint('Collecting metrics from args:', sys.argv[1:])\n")

        # 2. Evaluate candidate
        ev = evaluate_candidate(
            candidate_name=cand_name,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            manifest=self.manifest,
        )
        self.assertTrue(ev.is_valid_package)
        self.assertEqual(ev.recommended_decision, "NEW")

        # 3. Apply candidate with approval
        res = apply_candidate(
            candidate_name=cand_name,
            category="workflow-and-automation",
            subcategory="tool-integration",
            approved=True,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            runtime_dir=self.runtime_dir,
            manifest=self.manifest,
            ledger=self.ledger,
        )
        target_canonical_path = res["target_directory"]
        self.assertTrue(os.path.exists(target_canonical_path))
        self.assertFalse(os.path.exists(cand_dir))

        # 4. Verify runtime symlink was created automatically
        runtime_symlink = os.path.join(self.runtime_dir, cand_name)
        self.assertTrue(os.path.islink(runtime_symlink))
        self.assertTrue(os.path.exists(runtime_symlink))

        # 5. Targeted Pilot Verification
        pilot_rep = run_targeted_pilot(target_canonical_path, self.wa_router)
        self.assertTrue(pilot_rep.passed)
        self.assertTrue(pilot_rep.router_link_verified)
        self.assertTrue(pilot_rep.contract_verified)
        self.assertEqual(pilot_rep.scripts_executed_or_parsed, 1)

    def test_scenario_b_external_installer_simulation(self):
        """Scenario B: external installer places physical directory into .agents/skills; sync stages, normalizes provider coupling, and restores symlink."""
        external_name = "scenario-b-external-tool"
        runtime_pkg_dir = os.path.join(self.runtime_dir, external_name)
        os.makedirs(runtime_pkg_dir, exist_ok=True)

        with open(os.path.join(runtime_pkg_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: scenario-b-external-tool
description: Integrates third-party automation tools with Claude workflows. Use when integrating webhook hooks or automating external triggers.
---
# External Tool
Workflow automation content.
""")
        with open(os.path.join(runtime_pkg_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "scenario-b-external-tool", "version": "1.0.0"}, f)

        # 1. Scanner detects EXTERNAL_PHYSICAL
        scan_res = scan_runtime(runtime_dir=self.runtime_dir, library_dir=self.library_dir, manifest=self.manifest)
        ext_entries = [r for r in scan_res if r.name == external_name]
        self.assertEqual(len(ext_entries), 1)
        self.assertEqual(ext_entries[0].classification, "EXTERNAL_PHYSICAL")
        self.assertEqual(ext_entries[0].installer_integration_info.get("has_package_json"), "true")

        # 2. Sync stages physical install to intake/
        sync_rep = reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
            stage_external=True,
        )
        self.assertIn(external_name, sync_rep.staged_to_intake)
        staged_intake_dir = os.path.join(self.intake_dir, external_name)
        self.assertTrue(os.path.exists(staged_intake_dir))

        # 3. Evaluate and detect provider coupling ("Claude")
        ev = evaluate_candidate(
            candidate_name=external_name,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            manifest=self.manifest,
        )
        self.assertTrue(ev.provider_coupling_found)
        self.assertTrue(ev.approval_required)

        # 4. Enforce Approval Gate: applying without approved=True raises PermissionError
        with self.assertRaises(PermissionError):
            apply_candidate(
                candidate_name=external_name,
                category="workflow-and-automation",
                subcategory="tool-integration",
                approved=False,
                intake_dir=self.intake_dir,
                library_dir=self.library_dir,
                runtime_dir=self.runtime_dir,
                manifest=self.manifest,
                ledger=self.ledger,
            )

        # 5. Apply with approved=True normalizes provider coupling and restores symlink
        res = apply_candidate(
            candidate_name=external_name,
            category="workflow-and-automation",
            subcategory="tool-integration",
            approved=True,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            runtime_dir=self.runtime_dir,
            manifest=self.manifest,
            ledger=self.ledger,
        )
        target_dir = res["target_directory"]
        with open(os.path.join(target_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            clean_content = f.read()
        self.assertNotIn("Claude", clean_content)
        self.assertIn("Agent", clean_content)

        # Verify physical runtime folder replaced with canonical symlink
        runtime_item = os.path.join(self.runtime_dir, external_name)
        self.assertTrue(os.path.islink(runtime_item))
        self.assertTrue(os.path.exists(runtime_item))

    def test_scenario_g_skills_sh_brand_new_install(self):
        """
        Scenario G (Regression Test): skills.sh install of a brand-new skill.
        External tool writes physical package directly into .agents/skills/<name>.
        Pipeline automatically detects, stages, evaluates, approves, applies to canonical
        library, updates routers and manifest, runs real pilot/validation, and replaces
        physical runtime folder with canonical symlink.
        """
        tool_name = "skills-sh-brand-new"
        runtime_pkg_dir = os.path.join(self.runtime_dir, tool_name)
        os.makedirs(os.path.join(runtime_pkg_dir, "scripts"), exist_ok=True)

        with open(os.path.join(runtime_pkg_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: skills-sh-brand-new
description: Fresh external skill installed via skills.sh tool. Use when testing automated external intake workflows.
---
# Brand New Skills.sh Tool
Functional documentation.
""")
        with open(os.path.join(runtime_pkg_dir, "scripts", "main.py"), "w", encoding="utf-8") as f:
            f.write("print('Executed brand-new skills.sh tool')\n")
        with open(os.path.join(runtime_pkg_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": tool_name, "version": "1.0.0", "installer": "skills.sh"}, f)

        # 1. Detection via scanner
        classifications = scan_runtime(runtime_dir=self.runtime_dir, library_dir=self.library_dir, manifest=self.manifest)
        matching = [c for c in classifications if c.name == tool_name]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0].classification, "EXTERNAL_PHYSICAL")

        # 2. Stage to intake
        sync_rep = reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
            stage_external=True,
        )
        self.assertIn(tool_name, sync_rep.staged_to_intake)
        staged_path = os.path.join(self.intake_dir, tool_name)
        self.assertTrue(os.path.exists(staged_path))

        # 3. Evaluation
        ev = evaluate_candidate(
            candidate_name=tool_name,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            manifest=self.manifest,
        )
        self.assertTrue(ev.is_valid_package)
        self.assertEqual(ev.recommended_decision, "NEW")

        # 4. Apply with approval
        res = apply_candidate(
            candidate_name=tool_name,
            category="workflow-and-automation",
            subcategory="tool-integration",
            approved=True,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            runtime_dir=self.runtime_dir,
            manifest=self.manifest,
            ledger=self.ledger,
        )
        self.assertEqual(res["operation"], "ADD")
        canonical_dest = res["target_directory"]
        self.assertTrue(os.path.exists(canonical_dest))

        # 5. Verify runtime directory is now a valid relative symbolic link
        runtime_item = os.path.join(self.runtime_dir, tool_name)
        self.assertTrue(os.path.islink(runtime_item))
        self.assertTrue(os.path.exists(runtime_item))
        self.assertFalse(os.path.isdir(runtime_item) and not os.path.islink(runtime_item))

        # 6. Verify ledger record has real PASS statuses
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["canonical_name"], tool_name)
        self.assertEqual(latest_change["validation_status"], "PASS")
        self.assertEqual(latest_change["pilot_status"], "PASS")

    def test_scenario_h_skills_sh_update_to_managed_skill(self):
        """
        Scenario H (Regression Test): skills.sh install of an UPDATE to an already-managed skill.
        External tool places updated physical package into .agents/skills/existing-tool.
        Pipeline:
        1. Classifies as EXTERNAL_UPDATE (not a collision!).
        2. Diffs against canonical library copy and stages to intake with update metadata.
        3. Intake evaluation recommends UPDATE and requires human approval.
        4. Apply without approval is rejected.
        5. Apply with approval updates canonical package, executes real validation/pilot,
           logs operation='UPDATE' in change ledger, and safely restores canonical symlink.
        """
        managed_name = "existing-tool"
        runtime_pkg_dir = os.path.join(self.runtime_dir, managed_name)

        # 1. Simulate skills.sh overwriting runtime symlink with a physical updated directory
        self.assertTrue(os.path.islink(runtime_pkg_dir))
        os.unlink(runtime_pkg_dir)
        os.makedirs(os.path.join(runtime_pkg_dir, "scripts"), exist_ok=True)

        v2_skill_md = """---
name: existing-tool
description: Standard automation helper v2 with enhanced capabilities. Use when running automation scripts.
---
# Existing Tool V2
Upgraded instructions for existing tool v2.
"""
        with open(os.path.join(runtime_pkg_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(v2_skill_md)
        with open(os.path.join(runtime_pkg_dir, "scripts", "v2_action.py"), "w", encoding="utf-8") as f:
            f.write("print('V2 action execution')\n")
        with open(os.path.join(runtime_pkg_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": managed_name, "version": "2.0.0", "updated_by": "skills.sh"}, f)

        # 2. Scanner detects EXTERNAL_UPDATE
        scan_res = scan_runtime(runtime_dir=self.runtime_dir, library_dir=self.library_dir, manifest=self.manifest)
        matching = [c for c in scan_res if c.name == managed_name]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0].classification, "EXTERNAL_UPDATE")
        diff_info = matching[0].installer_integration_info.get("diff_summary", "")
        self.assertIn("SKILL.md", diff_info)

        # 3. Sync stages update to intake
        sync_rep = reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
            stage_external=True,
        )
        self.assertTrue(any(managed_name in s and "EXTERNAL_UPDATE" in s for s in sync_rep.staged_to_intake))
        staged_path = os.path.join(self.intake_dir, managed_name)
        self.assertTrue(os.path.exists(staged_path))

        # 4. Evaluate update candidate
        ev = evaluate_candidate(
            candidate_name=managed_name,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            manifest=self.manifest,
        )
        self.assertTrue(ev.is_update)
        self.assertEqual(ev.recommended_decision, "UPDATE")
        self.assertTrue(ev.approval_required)
        self.assertFalse(ev.name_collision)  # Should NOT be flagged as unwanted collision

        # 5. Gate blocks unapproved apply
        with self.assertRaises(PermissionError):
            apply_candidate(
                candidate_name=managed_name,
                approved=False,
                intake_dir=self.intake_dir,
                library_dir=self.library_dir,
                runtime_dir=self.runtime_dir,
                manifest=self.manifest,
                ledger=self.ledger,
            )

        # 6. Apply with approval succeeds
        res = apply_candidate(
            candidate_name=managed_name,
            approved=True,
            intake_dir=self.intake_dir,
            library_dir=self.library_dir,
            runtime_dir=self.runtime_dir,
            manifest=self.manifest,
            ledger=self.ledger,
        )
        self.assertEqual(res["operation"], "UPDATE")
        self.assertTrue(res["is_update"])

        # 7. Canonical library package has updated files
        target_canonical = res["target_directory"]
        with open(os.path.join(target_canonical, "SKILL.md"), "r", encoding="utf-8") as f:
            saved_content = f.read()
        self.assertIn("Standard automation helper v2", saved_content)
        self.assertTrue(os.path.exists(os.path.join(target_canonical, "scripts", "v2_action.py")))

        # 8. Runtime symlink is safely restored
        runtime_item = os.path.join(self.runtime_dir, managed_name)
        self.assertTrue(os.path.islink(runtime_item))
        self.assertTrue(os.path.exists(runtime_item))

        # 9. Ledger recorded UPDATE with genuine PASS
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["operation"], "UPDATE")
        self.assertEqual(latest_change["decision"], "UPDATE")
        self.assertEqual(latest_change["validation_status"], "PASS")
        self.assertEqual(latest_change["pilot_status"], "PASS")

    def test_scenario_i_new_candidate_fails_pre_validation(self):
        """Scenario I (Regression Test): NEW candidate fails package validation prior to install; produces zero canonical changes."""
        cand_name = "scenario-i-invalid-candidate"
        cand_dir = os.path.join(self.intake_dir, cand_name)
        os.makedirs(cand_dir, exist_ok=True)

        # 1. Author candidate with invalid frontmatter (missing name and invalid syntax)
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("Invalid SKILL file with no frontmatter\n")

        with open(self.wa_router, "r", encoding="utf-8") as f:
            router_before = f.read()
        manifest_skills_before = set(self.manifest.skills.keys())

        # 2. Attempt apply_candidate with approval; must abort before canonical modifications
        with self.assertRaises(ValueError) as ctx:
            apply_candidate(
                candidate_name=cand_name,
                category="workflow-and-automation",
                subcategory="tool-integration",
                approved=True,
                intake_dir=self.intake_dir,
                library_dir=self.library_dir,
                runtime_dir=self.runtime_dir,
                manifest=self.manifest,
                ledger=self.ledger,
            )
        self.assertIn("failed prior to installation", str(ctx.exception))

        # 3. Assert ZERO canonical changes occurred
        expected_canonical = os.path.join(self.library_dir, "workflow-and-automation", "tool-integration", cand_name)
        self.assertFalse(os.path.exists(expected_canonical))

        # 4. Assert router was not modified
        with open(self.wa_router, "r", encoding="utf-8") as f:
            router_after = f.read()
        self.assertEqual(router_before, router_after)

        # 5. Assert manifest was not modified
        self.assertEqual(set(self.manifest.skills.keys()), manifest_skills_before)

        # 6. Assert runtime symlink was not created
        runtime_item = os.path.join(self.runtime_dir, cand_name)
        self.assertFalse(os.path.lexists(runtime_item))

        # 7. Assert candidate remains in intake for correction
        self.assertTrue(os.path.exists(cand_dir))

        # 8. Assert ledger recorded the failed attempt truthfully
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["original_name"], cand_name)
        self.assertEqual(latest_change["decision"], "REJECT")
        self.assertEqual(latest_change["validation_status"], "FAIL")
        self.assertEqual(latest_change["pilot_status"], "NOT_RUN")

    def test_scenario_j_new_candidate_fails_pilot_rolls_back(self):
        """Scenario J (Regression Test): NEW candidate passes pre-validation but fails targeted pilot; rolls back all canonical/runtime changes."""
        cand_name = "scenario-j-bad-pilot"
        cand_dir = os.path.join(self.intake_dir, cand_name)
        os.makedirs(os.path.join(cand_dir, "scripts"), exist_ok=True)

        # 1. Author candidate with valid SKILL.md and scripts
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: scenario-j-bad-pilot
description: System to test transaction rollback. Use when testing pipeline failure handling.
---
# Scenario J Bad Pilot
""")
        with open(os.path.join(cand_dir, "scripts", "run.py"), "w", encoding="utf-8") as f:
            f.write("print('valid python')\n")

        with open(self.wa_router, "r", encoding="utf-8") as f:
            router_before = f.read()
        manifest_skills_before = set(self.manifest.skills.keys())

        # 2. Attempt apply_candidate with simulated pilot failure; must roll back completely
        simulated_pilot_fail = PilotResult(
            skill_name=cand_name,
            parent_router=self.wa_router,
            passed=False,
            errors=["Simulated pilot failure: trigger contract ambiguity"],
        )
        with patch("skill_library.intake.run_targeted_pilot", return_value=simulated_pilot_fail):
            with self.assertRaises(RuntimeError) as ctx:
                apply_candidate(
                    candidate_name=cand_name,
                    category="workflow-and-automation",
                    subcategory="tool-integration",
                    approved=True,
                    intake_dir=self.intake_dir,
                    library_dir=self.library_dir,
                    runtime_dir=self.runtime_dir,
                    manifest=self.manifest,
                    ledger=self.ledger,
                )
        self.assertIn("failed post-install checks", str(ctx.exception))
        self.assertIn("rolled back", str(ctx.exception))

        # 3. Assert canonical package was removed
        expected_canonical = os.path.join(self.library_dir, "workflow-and-automation", "tool-integration", cand_name)
        self.assertFalse(os.path.exists(expected_canonical))

        # 4. Assert router was restored to its exact previous content
        with open(self.wa_router, "r", encoding="utf-8") as f:
            router_after = f.read()
        self.assertEqual(router_before, router_after)

        # 5. Assert manifest entry was removed
        self.assertEqual(set(self.manifest.skills.keys()), manifest_skills_before)

        # 6. Assert runtime symlink was removed
        runtime_item = os.path.join(self.runtime_dir, cand_name)
        self.assertFalse(os.path.lexists(runtime_item))

        # 7. Assert candidate was restored to intake
        self.assertTrue(os.path.exists(cand_dir))
        self.assertTrue(os.path.exists(os.path.join(cand_dir, "scripts", "run.py")))

        # 8. Assert ledger recorded the failure truthfully
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["original_name"], cand_name)
        self.assertEqual(latest_change["decision"], "ROLLBACK")
        self.assertEqual(latest_change["validation_status"], "PASS")
        self.assertEqual(latest_change["pilot_status"], "FAIL")

    def test_scenario_k_update_fails_pre_validation(self):
        """Scenario K (Regression Test): UPDATE candidate fails pre-validation; leaves prior canonical skill completely untouched."""
        managed_name = "bug-hunter"
        canonical_dir = os.path.join(self.library_dir, "quality-and-security", "debugging", managed_name)

        with open(os.path.join(canonical_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            orig_skill_md_content = f.read()

        # Stage invalid update into intake
        cand_dir = os.path.join(self.intake_dir, managed_name)
        os.makedirs(cand_dir, exist_ok=True)
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("Broken update with no frontmatter\n")

        with open(os.path.join(cand_dir, ".installer-metadata.json"), "w", encoding="utf-8") as mf:
            json.dump({
                "type": "external_update",
                "target_canonical_path": "library/quality-and-security/debugging/bug-hunter",
                "timestamp": "2026-10-08T00:00:00Z"
            }, mf)

        # Must abort prior to installation
        with self.assertRaises(ValueError) as ctx:
            apply_candidate(
                candidate_name=managed_name,
                approved=True,
                intake_dir=self.intake_dir,
                library_dir=self.library_dir,
                runtime_dir=self.runtime_dir,
                manifest=self.manifest,
                ledger=self.ledger,
            )
        self.assertIn("failed prior to installation", str(ctx.exception))

        # Assert prior canonical version is completely untouched
        with open(os.path.join(canonical_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            current_content = f.read()
        self.assertEqual(current_content, orig_skill_md_content)

        # Assert ledger recorded failure
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["original_name"], managed_name)
        self.assertEqual(latest_change["decision"], "REJECT")
        self.assertEqual(latest_change["validation_status"], "FAIL")

    def test_scenario_l_update_fails_pilot_restores_prior_canonical(self):
        """Scenario L (Regression Test): UPDATE candidate fails pilot; completely restores prior canonical version and leaves update in intake."""
        managed_name = "bug-hunter"
        canonical_dir = os.path.join(self.library_dir, "quality-and-security", "debugging", managed_name)

        # Record original canonical state
        with open(os.path.join(canonical_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            orig_skill_md_content = f.read()
        router_path = self.qs_router
        with open(router_path, "r", encoding="utf-8") as f:
            router_before = f.read()
        manifest_entry_before = copy.deepcopy(self.manifest.skills[managed_name])

        # Stage proposed update into intake with valid frontmatter but will fail pilot
        cand_dir = os.path.join(self.intake_dir, managed_name)
        os.makedirs(os.path.join(cand_dir, "scripts"), exist_ok=True)
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: bug-hunter
description: Autonomous system to identify and capture code bugs. Use when hunting application defects.
---
# Bug Hunter v2.0 - Proposed Update
""")
        with open(os.path.join(cand_dir, "scripts", "new_feature.py"), "w", encoding="utf-8") as f:
            f.write("print('new feature')\n")

        with open(os.path.join(cand_dir, ".installer-metadata.json"), "w", encoding="utf-8") as mf:
            json.dump({
                "type": "external_update",
                "target_canonical_path": "library/quality-and-security/debugging/bug-hunter",
                "timestamp": "2026-10-08T00:00:00Z"
            }, mf)

        # Attempt apply; must fail pilot and restore prior canonical version
        simulated_pilot_fail = PilotResult(
            skill_name=managed_name,
            parent_router=self.qs_router,
            passed=False,
            errors=["Simulated pilot failure: trigger contract conflict"],
        )
        with patch("skill_library.intake.run_targeted_pilot", return_value=simulated_pilot_fail):
            with self.assertRaises(RuntimeError) as ctx:
                apply_candidate(
                    candidate_name=managed_name,
                    approved=True,
                    intake_dir=self.intake_dir,
                    library_dir=self.library_dir,
                    runtime_dir=self.runtime_dir,
                    manifest=self.manifest,
                    ledger=self.ledger,
                )
        self.assertIn("failed post-install checks", str(ctx.exception))

        # Assert prior canonical version is completely restored
        with open(os.path.join(canonical_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            restored_skill_md = f.read()
        self.assertEqual(restored_skill_md, orig_skill_md_content)
        self.assertFalse(os.path.exists(os.path.join(canonical_dir, "scripts", "new_feature.py")))

        # Assert router is preserved
        with open(router_path, "r", encoding="utf-8") as f:
            router_after = f.read()
        self.assertEqual(router_before, router_after)

        # Assert manifest entry is preserved
        self.assertEqual(self.manifest.skills[managed_name], manifest_entry_before)

        # Assert runtime symlink still points to canonical bug-hunter
        runtime_item = os.path.join(self.runtime_dir, managed_name)
        self.assertTrue(os.path.islink(runtime_item))
        self.assertEqual(os.path.realpath(runtime_item), os.path.realpath(canonical_dir))

        # Assert proposed update is preserved in intake for review
        self.assertTrue(os.path.exists(cand_dir))
        self.assertTrue(os.path.exists(os.path.join(cand_dir, "scripts", "new_feature.py")))

        # Assert ledger recorded the rollback truthfully
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["operation"], "UPDATE")
        self.assertEqual(latest_change["decision"], "ROLLBACK")
        self.assertEqual(latest_change["validation_status"], "PASS")
        self.assertEqual(latest_change["pilot_status"], "FAIL")

    def test_scenario_m_external_update_fails_pilot_restores_symlink(self):
        """Scenario M (Regression Test): skills.sh external update fails pilot; restores prior canonical version, restores runtime symlink, and leaves update in intake."""
        managed_name = "bug-hunter"
        canonical_dir = os.path.join(self.library_dir, "quality-and-security", "debugging", managed_name)
        runtime_item = os.path.join(self.runtime_dir, managed_name)

        # 1. Start with managed symlink
        self.assertTrue(os.path.islink(runtime_item))
        with open(os.path.join(canonical_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            orig_skill_md_content = f.read()
        router_path = self.qs_router
        with open(router_path, "r", encoding="utf-8") as f:
            router_before = f.read()
        manifest_entry_before = copy.deepcopy(self.manifest.skills[managed_name])

        # 2. skills.sh replaces symlink with physical updated directory
        os.unlink(runtime_item)
        os.makedirs(runtime_item, exist_ok=True)
        with open(os.path.join(runtime_item, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: bug-hunter
description: Autonomous system to identify and capture code bugs. Use when hunting application defects.
---
# Bug Hunter v3 - External Update by skills.sh
""")
        os.makedirs(os.path.join(runtime_item, "scripts"), exist_ok=True)
        with open(os.path.join(runtime_item, "scripts", "feature.py"), "w", encoding="utf-8") as f:
            f.write("print('feature')\n")
        with open(os.path.join(runtime_item, ".skills-installer-env.json"), "w", encoding="utf-8") as f:
            json.dump({"installer": "skills.sh", "version": "1.0"}, f)

        self.assertTrue(os.path.isdir(runtime_item))
        self.assertFalse(os.path.islink(runtime_item))

        # 3. Sync stages EXTERNAL_UPDATE to intake
        sync_rep = reconcile_runtime_symlinks(
            runtime_dir=self.runtime_dir,
            library_dir=self.library_dir,
            intake_dir=self.intake_dir,
            manifest=self.manifest,
            dry_run=False,
            stage_external=True,
        )
        self.assertTrue(any(managed_name in s and "EXTERNAL_UPDATE" in s for s in sync_rep.staged_to_intake))
        cand_dir = os.path.join(self.intake_dir, managed_name)
        self.assertTrue(os.path.exists(cand_dir))

        # 4. Attempt apply update with simulated pilot failure
        simulated_pilot_fail = PilotResult(
            skill_name=managed_name,
            parent_router=self.qs_router,
            passed=False,
            errors=["Simulated pilot failure in external update"],
        )
        with patch("skill_library.intake.run_targeted_pilot", return_value=simulated_pilot_fail):
            with self.assertRaises(RuntimeError) as ctx:
                apply_candidate(
                    candidate_name=managed_name,
                    approved=True,
                    intake_dir=self.intake_dir,
                    library_dir=self.library_dir,
                    runtime_dir=self.runtime_dir,
                    manifest=self.manifest,
                    ledger=self.ledger,
                )
        self.assertIn("failed post-install checks", str(ctx.exception))
        self.assertIn("rolled back", str(ctx.exception))

        # 5. Assert previous canonical package is restored
        with open(os.path.join(canonical_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            restored_skill_md = f.read()
        self.assertEqual(restored_skill_md, orig_skill_md_content)
        self.assertFalse(os.path.exists(os.path.join(canonical_dir, "scripts", "feature.py")))

        # 6. Assert failed update remains in intake for review
        self.assertTrue(os.path.exists(cand_dir))
        self.assertTrue(os.path.exists(os.path.join(cand_dir, "scripts", "feature.py")))

        # 7. Assert .agents/skills/<name> is restored as a symlink to previous canonical package
        self.assertTrue(os.path.islink(runtime_item))
        self.assertTrue(os.path.exists(runtime_item))
        self.assertEqual(os.path.realpath(runtime_item), os.path.realpath(canonical_dir))

        # 8. Assert manifest/router unchanged
        with open(router_path, "r", encoding="utf-8") as f:
            router_after = f.read()
        self.assertEqual(router_before, router_after)
        self.assertEqual(self.manifest.skills[managed_name], manifest_entry_before)

        # 9. Assert ledger records ROLLBACK
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["operation"], "UPDATE")
        self.assertEqual(latest_change["decision"], "ROLLBACK")
        self.assertEqual(latest_change["validation_status"], "PASS")
        self.assertEqual(latest_change["pilot_status"], "FAIL")

    def test_scenario_n_unexpected_exception_triggers_transactional_rollback(self):
        """Scenario N (Regression Test): Unexpected exception during deployment triggers transactional rollback and re-raises."""
        cand_name = "scenario-n-crash"
        cand_dir = os.path.join(self.intake_dir, cand_name)
        os.makedirs(cand_dir, exist_ok=True)
        with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: scenario-n-crash
description: System to test crash rollback. Use when testing pipeline crash handling.
---
# Scenario N Crash
""")

        # Simulate unexpected crash during router update (Step D, after canonical copy in Step C)
        with patch("skill_library.intake.add_link_to_router", side_effect=IOError("Simulated disk error during router update")):
            with self.assertRaises(IOError):
                apply_candidate(
                    candidate_name=cand_name,
                    category="workflow-and-automation",
                    subcategory="tool-integration",
                    approved=True,
                    intake_dir=self.intake_dir,
                    library_dir=self.library_dir,
                    runtime_dir=self.runtime_dir,
                    manifest=self.manifest,
                    ledger=self.ledger,
                )

        # Assert canonical package was removed
        expected_canonical = os.path.join(self.library_dir, "workflow-and-automation", "tool-integration", cand_name)
        self.assertFalse(os.path.exists(expected_canonical))

        # Assert candidate was restored to intake
        self.assertTrue(os.path.exists(cand_dir))

        # Assert ledger recorded rollback
        latest_change = self.ledger.get_history(limit=1)[0]
        self.assertEqual(latest_change["decision"], "ROLLBACK")


if __name__ == "__main__":
    unittest.main()
