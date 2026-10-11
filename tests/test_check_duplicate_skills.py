#!/usr/bin/env python3
"""
Unit and regression tests for tools/check_duplicate_skills.py.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add tools to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
TOOLS_DIR = os.path.join(REPO_ROOT, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from check_duplicate_skills import (
    audit_duplicate_skills,
    cleanup_duplicate_skills,
    DuplicateAuditReport,
)


class TestCheckDuplicateSkills(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.tmp_dir.name).resolve()
        self.lib_dir = self.test_root / "library"
        self.lib_dir.mkdir(parents=True, exist_ok=True)

        # Setup standard routers
        (self.lib_dir / "SKILL.md").write_text("---\nname: root\n---\n# Root\n")
        
        # Category: design-and-experience
        cat_dir = self.lib_dir / "design-and-experience"
        cat_dir.mkdir(parents=True, exist_ok=True)
        (cat_dir / "SKILL.md").write_text("---\nname: design\n---\n# Design\n")

        # Subcategory: taste-and-critique
        self.subcat_dir = cat_dir / "taste-and-critique"
        self.subcat_dir.mkdir(parents=True, exist_ok=True)
        (self.subcat_dir / "SKILL.md").write_text("---\nname: taste\n---\n# Taste\n")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def _create_skill(self, parent_dir: Path, name: str, desc: str = "A skill") -> Path:
        skill_dir = parent_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\n# {name}\n")
        return skill_dir

    def test_01_clean_library_passes_audit(self):
        """Clean library with proper depth-3 packages passes audit."""
        self._create_skill(self.subcat_dir, "skill-a")
        self._create_skill(self.subcat_dir, "skill-b")

        report = audit_duplicate_skills(str(self.lib_dir))
        self.assertTrue(report.is_clean)
        self.assertEqual(report.total_canonical_skills, 2)
        self.assertEqual(len(report.nested_violations), 0)
        self.assertEqual(len(report.name_collisions), 0)

    def test_02_detects_nested_child_skill_from_extracted_container(self):
        """Reproduces Phase 08 Batch 30 container pattern (design-it):
        design-it contains 3d-ui, while 3d-ui is also a canonical peer.
        Audit must detect 3d-ui as a confirmed duplicate nested violation.
        """
        # Canonical 3d-ui
        canonical_3d = self._create_skill(self.subcat_dir, "3d-ui")
        # Container design-it
        design_it = self._create_skill(self.subcat_dir, "design-it")
        # Nested duplicate 3d-ui inside design-it
        nested_3d = self._create_skill(design_it, "3d-ui")
        # Also add a resource folder to design-it that should NOT be detected as a skill
        (design_it / "references").mkdir(parents=True, exist_ok=True)
        (design_it / "references" / "guide.md").write_text("# Reference Guide\n")

        report = audit_duplicate_skills(str(self.lib_dir))
        self.assertFalse(report.is_clean)
        self.assertEqual(len(report.nested_violations), 1)

        violation = report.nested_violations[0]
        self.assertEqual(violation.parent_package, "design-it")
        self.assertEqual(violation.child_name, "3d-ui")
        self.assertEqual(violation.child_path, str(nested_3d))
        self.assertTrue(violation.is_confirmed_duplicate)
        self.assertEqual(violation.canonical_counterparts, [str(canonical_3d)])

    def test_03_cleanup_dry_run_does_not_mutate_disk(self):
        """Cleanup with dry_run=True must report target paths without deleting them."""
        self._create_skill(self.subcat_dir, "3d-ui")
        design_it = self._create_skill(self.subcat_dir, "design-it")
        nested_3d = self._create_skill(design_it, "3d-ui")

        report = audit_duplicate_skills(str(self.lib_dir))
        self.assertEqual(len(report.nested_violations), 1)

        result = cleanup_duplicate_skills(report, dry_run=True)
        self.assertEqual(len(result.cleaned_directories), 1)
        self.assertEqual(result.cleaned_directories[0], str(nested_3d))
        # Verify nested directory still exists on disk
        self.assertTrue(nested_3d.exists())

    def test_04_cleanup_execution_safely_removes_nested_duplicates_only(self):
        """Cleanup with dry_run=False removes nested duplicate directories,
        strictly preserving parent package files, parent resource folders,
        and canonical peer packages.
        """
        canonical_3d = self._create_skill(self.subcat_dir, "3d-ui")
        design_it = self._create_skill(self.subcat_dir, "design-it")
        nested_3d = self._create_skill(design_it, "3d-ui")
        nested_bento = self._create_skill(design_it, "bento-ui")
        canonical_bento = self._create_skill(self.subcat_dir, "bento-ui")

        # Non-skill resource folder in parent
        refs = design_it / "references"
        refs.mkdir(parents=True, exist_ok=True)
        (refs / "styles.md").write_text("Palette info\n")

        report = audit_duplicate_skills(str(self.lib_dir))
        self.assertEqual(len(report.nested_violations), 2)

        result = cleanup_duplicate_skills(report, dry_run=False)
        self.assertEqual(len(result.cleaned_directories), 2)
        self.assertEqual(len(result.errors), 0)

        # 1. Nested child skill folders must be gone
        self.assertFalse(nested_3d.exists())
        self.assertFalse(nested_bento.exists())

        # 2. Parent package root files and resources must remain intact
        self.assertTrue(design_it.exists())
        self.assertTrue((design_it / "SKILL.md").exists())
        self.assertTrue((refs / "styles.md").exists())

        # 3. Canonical peer skills must remain completely intact
        self.assertTrue(canonical_3d.exists())
        self.assertTrue((canonical_3d / "SKILL.md").exists())
        self.assertTrue(canonical_bento.exists())
        self.assertTrue((canonical_bento / "SKILL.md").exists())

        # 4. Post-cleanup audit must pass cleanly
        post_report = audit_duplicate_skills(str(self.lib_dir))
        self.assertTrue(post_report.is_clean)
        self.assertEqual(post_report.total_nested_count, 0)

    def test_05_unconfirmed_nested_skill_not_removed_by_default(self):
        """If a nested child skill does NOT have a canonical peer elsewhere,
        it is marked unconfirmed and NOT deleted by default, protecting unique data.
        """
        design_it = self._create_skill(self.subcat_dir, "design-it")
        unique_nested = self._create_skill(design_it, "experimental-unique-style")

        report = audit_duplicate_skills(str(self.lib_dir))
        self.assertFalse(report.is_clean)
        self.assertEqual(len(report.nested_violations), 0)
        self.assertEqual(len(report.unconfirmed_nested_skills), 1)

        # Default cleanup should skip unconfirmed
        result = cleanup_duplicate_skills(report, dry_run=False, clean_unconfirmed=False)
        self.assertEqual(len(result.cleaned_directories), 0)
        self.assertTrue(unique_nested.exists())

    def test_06_cli_exit_codes_and_json(self):
        """CLI returns exit code 1 when duplicates exist, code 0 when clean, and outputs JSON."""
        self._create_skill(self.subcat_dir, "3d-ui")
        design_it = self._create_skill(self.subcat_dir, "design-it")
        self._create_skill(design_it, "3d-ui")

        tool_path = os.path.join(TOOLS_DIR, "check_duplicate_skills.py")

        # 1. Audit fails with code 1
        proc_audit = subprocess.run(
            [sys.executable, tool_path, str(self.lib_dir)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc_audit.returncode, 1)
        self.assertIn("VIOLATIONS DETECTED", proc_audit.stdout)

        # 2. JSON mode outputs valid JSON
        proc_json = subprocess.run(
            [sys.executable, tool_path, str(self.lib_dir), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc_json.returncode, 1)
        data = json.loads(proc_json.stdout)
        self.assertFalse(data["summary"]["is_clean"])
        self.assertEqual(data["summary"]["nested_child_duplicates"], 1)

        # 3. Fix removes duplicate
        proc_fix = subprocess.run(
            [sys.executable, tool_path, str(self.lib_dir), "--fix", "--yes"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc_fix.returncode, 0)
        self.assertIn("Successfully removed 1 duplicate directories", proc_fix.stdout)

        # 4. Audit passes with code 0 after fix
        proc_clean = subprocess.run(
            [sys.executable, tool_path, str(self.lib_dir)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc_clean.returncode, 0)
        self.assertIn("STATUS: PASS", proc_clean.stdout)


if __name__ == "__main__":
    unittest.main()
