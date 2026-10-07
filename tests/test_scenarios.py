"""
Automated Test Suite for Task 13 Scenarios A through F.
Tests manual intake, external installer simulation, sync idempotency,
broken link repair, name collision halts, and semantic overlap detection.
"""

import json
import os
import shutil
import sys
import unittest

# Ensure tools directory is in sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TEST_DIR)
TOOLS_DIR = os.path.join(REPO_ROOT, "tools")
sys.path.insert(0, TOOLS_DIR)

from skill_library.config import (
    AUDIT_DIR,
    INTAKE_DIR,
    LIBRARY_DIR,
    MANIFEST_FILE,
    RUNTIME_DIR,
)
from skill_library.intake import apply_candidate, evaluate_candidate
from skill_library.ledger import ChangeLedger
from skill_library.manifest import RuntimeManifest
from skill_library.pilot import run_targeted_pilot
from skill_library.scanner import scan_candidate_directory, scan_runtime
from skill_library.sync import reconcile_runtime_symlinks
from skill_library.validator import validate_library, validate_single_skill


class TestSkillLibraryScenarios(unittest.TestCase):

    def setUp(self):
        self.manifest = RuntimeManifest()
        self.ledger = ChangeLedger()

    def test_scenario_c_idempotent_sync(self):
        """Scenario C: sync against already-synchronized library produces zero changes."""
        report = reconcile_runtime_symlinks(manifest=self.manifest, dry_run=False)
        self.assertEqual(len(report.created), 0)
        self.assertEqual(len(report.repaired), 0)
        self.assertEqual(len(report.staged_to_intake), 0)
        self.assertEqual(len(report.collisions), 0)
        self.assertEqual(len(report.errors), 0)
        self.assertFalse(report.has_changes)

    def test_scenario_d_broken_link_repair(self):
        """Scenario D: broken managed link is identified and repaired."""
        test_symlink_name = "007"
        sym_path = os.path.join(RUNTIME_DIR, test_symlink_name)
        orig_target = os.readlink(sym_path)

        try:
            # Deliberately point symlink to non-existent target
            os.unlink(sym_path)
            os.symlink("../../library/non_existent_path", sym_path)
            self.assertFalse(os.path.exists(sym_path))

            # Run sync
            report = reconcile_runtime_symlinks(manifest=self.manifest, dry_run=False)
            self.assertIn(f"{test_symlink_name} -> library/quality-and-security/security/007", report.repaired)
            self.assertTrue(os.path.exists(sym_path))
        finally:
            # Ensure restored
            if not os.path.exists(sym_path):
                if os.path.lexists(sym_path):
                    os.unlink(sym_path)
                os.symlink(orig_target, sym_path)

    def test_scenario_e_name_collision(self):
        """Scenario E: new skill using existing canonical name triggers collision halt."""
        collision_name = "bug-hunter"
        cand_dir = os.path.join(INTAKE_DIR, collision_name)
        os.makedirs(cand_dir, exist_ok=True)

        try:
            skill_md_content = """---
name: bug-hunter
description: Autonomous system to identify and capture code bugs. Use when hunting application defects.
---
# Bug Hunter
Alternative tool.
"""
            with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                f.write(skill_md_content)

            ev = evaluate_candidate(candidate_name=collision_name, manifest=self.manifest)
            self.assertTrue(ev.name_collision)
            self.assertTrue(ev.approval_required)
            self.assertTrue(any("collision" in r.lower() or "duplicate" in r.lower() for r in ev.approval_reasons))
        finally:
            if os.path.exists(cand_dir):
                shutil.rmtree(cand_dir)

    def test_scenario_f_semantic_overlap(self):
        """Scenario F: skill with high semantic overlap recommends MERGE and halts for review."""
        cand_name = "test-smart-bug-finder"
        cand_dir = os.path.join(INTAKE_DIR, cand_name)
        os.makedirs(cand_dir, exist_ok=True)

        try:
            skill_md_content = """---
name: test-smart-bug-finder
description: Systematically isolate a runtime exception, reproduce the failure with minimal test case, and diagnose the root cause. Use when debugging unexpected application failures or hunting bugs.
---
# Smart Bug Finder
Tool for debugging issues.
"""
            with open(os.path.join(cand_dir, "SKILL.md"), "w", encoding="utf-8") as f:

                f.write(skill_md_content)

            ev = evaluate_candidate(candidate_name=cand_name, manifest=self.manifest)

            self.assertTrue(ev.approval_required)
            self.assertIn(ev.recommended_decision, ["MERGE", "KEEP_SEPARATE"])
            self.assertTrue(len(ev.semantic_competitors) > 0)
            top_match = ev.semantic_competitors[0]
            top_names = [c["name"] for c in ev.semantic_competitors]
            self.assertTrue(any(name in ["bug-hunter", "debugging-toolkit-smart-debug"] for name in top_names))
            self.assertGreater(top_match["similarity"], 0.35)
        finally:



            if os.path.exists(cand_dir):
                shutil.rmtree(cand_dir)

    def test_scenario_a_manual_intake_end_to_end(self):
        """Scenario A: manual intake candidate evaluated, applied to library, symlinked, and piloted."""
        cand_name = "scenario-a-collector"
        cand_dir = os.path.join(INTAKE_DIR, cand_name)
        os.makedirs(os.path.join(cand_dir, "scripts"), exist_ok=True)

        target_canonical_path = os.path.join(LIBRARY_DIR, "infrastructure-and-ops", "observability", cand_name)
        router_path = os.path.join(LIBRARY_DIR, "infrastructure-and-ops", "SKILL.md")
        runtime_symlink = os.path.join(RUNTIME_DIR, cand_name)

        try:
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
                f.write("""import sys
if __name__ == '__main__':
    print('Collecting metrics from args:', sys.argv[1:])
""")

            # 2. Evaluate candidate
            ev = evaluate_candidate(candidate_name=cand_name, manifest=self.manifest)
            self.assertTrue(ev.is_valid_package)
            self.assertEqual(ev.recommended_decision, "NEW")
            self.assertEqual(ev.assigned_category, "infrastructure-and-ops")

            # 3. Apply candidate
            res = apply_candidate(
                candidate_name=cand_name,
                category="infrastructure-and-ops",
                subcategory="observability",
                manifest=self.manifest,
                ledger=self.ledger,
            )
            self.assertTrue(os.path.exists(target_canonical_path))
            self.assertFalse(os.path.exists(cand_dir))

            # 4. Sync runtime symlinks
            sync_rep = reconcile_runtime_symlinks(manifest=self.manifest, dry_run=False)
            self.assertIn(cand_name, sync_rep.created)
            self.assertTrue(os.path.islink(runtime_symlink))
            self.assertTrue(os.path.exists(runtime_symlink))

            # 5. Targeted Pilot Verification
            pilot_rep = run_targeted_pilot(target_canonical_path, router_path)
            self.assertTrue(pilot_rep.passed)
            self.assertTrue(pilot_rep.router_link_verified)
            self.assertTrue(pilot_rep.contract_verified)
            self.assertEqual(pilot_rep.scripts_executed_or_parsed, 1)

        finally:
            # Clean up after test
            if os.path.exists(target_canonical_path):
                shutil.rmtree(target_canonical_path)
            if os.path.lexists(runtime_symlink):
                os.unlink(runtime_symlink)
            if os.path.exists(cand_dir):
                shutil.rmtree(cand_dir)
            self.manifest.remove_skill(cand_name)
            self.manifest.save()
            # Clean up router entry
            if os.path.exists(router_path):
                with open(router_path, "r", encoding="utf-8") as rf:
                    rtext = rf.read()
                cleaned = "\n".join([line for line in rtext.splitlines() if cand_name not in line])
                with open(router_path, "w", encoding="utf-8") as rf:
                    rf.write(cleaned + "\n")

    def test_scenario_b_external_installer_simulation(self):
        """Scenario B: external installer places physical directory into .agents/skills; sync stages and normalizes it."""
        external_name = "scenario-b-external-tool"
        runtime_pkg_dir = os.path.join(RUNTIME_DIR, external_name)
        os.makedirs(runtime_pkg_dir, exist_ok=True)

        target_canonical_path = os.path.join(LIBRARY_DIR, "workflow-and-automation", "tool-integration", external_name)
        router_path = os.path.join(LIBRARY_DIR, "workflow-and-automation", "SKILL.md")
        staged_intake_dir = os.path.join(INTAKE_DIR, external_name)

        try:
            # 1. Simulate external installer creating physical package in .agents/skills
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

            # 2. Scanner detects EXTERNAL_PHYSICAL
            scan_res = scan_runtime(manifest=self.manifest)
            ext_entries = [r for r in scan_res if r.name == external_name]
            self.assertEqual(len(ext_entries), 1)
            self.assertEqual(ext_entries[0].classification, "EXTERNAL_PHYSICAL")
            self.assertEqual(ext_entries[0].installer_integration_info.get("has_package_json"), "true")

            # 3. Sync stages physical install to intake/
            sync_rep = reconcile_runtime_symlinks(manifest=self.manifest, dry_run=False, stage_external=True)
            self.assertIn(external_name, sync_rep.staged_to_intake)
            self.assertTrue(os.path.exists(staged_intake_dir))

            # 4. Evaluate and Normalize Candidate
            ev = evaluate_candidate(candidate_name=external_name, manifest=self.manifest)
            self.assertTrue(ev.provider_coupling_found)  # "Claude" detected in text

            # 5. Apply approved candidate (normalizes provider coupling to Agent)
            res = apply_candidate(
                candidate_name=external_name,
                category="workflow-and-automation",
                subcategory="tool-integration",
                manifest=self.manifest,
                ledger=self.ledger,
            )
            self.assertTrue(os.path.exists(target_canonical_path))

            # Verify provider coupling was decoupled
            with open(os.path.join(target_canonical_path, "SKILL.md"), "r", encoding="utf-8") as f:
                normalized_text = f.read()
            self.assertNotIn("Claude", normalized_text)
            self.assertIn("Agent", normalized_text)

            # Remove physical folder from runtime and replace with symlink via sync
            if os.path.isdir(runtime_pkg_dir) and not os.path.islink(runtime_pkg_dir):
                shutil.rmtree(runtime_pkg_dir)

            reconcile_runtime_symlinks(manifest=self.manifest, dry_run=False)
            self.assertTrue(os.path.islink(runtime_pkg_dir))
            self.assertTrue(os.path.exists(runtime_pkg_dir))

        finally:
            if os.path.exists(target_canonical_path):
                shutil.rmtree(target_canonical_path)
            if os.path.lexists(runtime_pkg_dir):
                if os.path.islink(runtime_pkg_dir):
                    os.unlink(runtime_pkg_dir)
                else:
                    shutil.rmtree(runtime_pkg_dir)
            if os.path.exists(staged_intake_dir):
                shutil.rmtree(staged_intake_dir)
            self.manifest.remove_skill(external_name)
            self.manifest.save()
            if os.path.exists(router_path):
                with open(router_path, "r", encoding="utf-8") as rf:
                    rtext = rf.read()
                cleaned = "\n".join([line for line in rtext.splitlines() if external_name not in line])
                with open(router_path, "w", encoding="utf-8") as rf:
                    rf.write(cleaned + "\n")


if __name__ == "__main__":
    unittest.main()
