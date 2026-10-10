"""
Comprehensive Regression Test Suite for Runtime Git-Clone Publication Architecture.
Tests all 14 requirements specified in docs/bugs/runtime-git-clone-publication.md.

All tests operate in completely isolated temporary Git repositories and never touch
the production environment or the user's ~/.agents or ~/.gemini directories.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

TEST_DIR = Path(__file__).resolve().parent
REPO_ROOT_DIR = TEST_DIR.parent
TOOLS_DIR = REPO_ROOT_DIR / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.config import (
    CATEGORIES,
    DEEP_CATEGORIES,
    RUNTIME_BRANCH,
    RuntimeTarget,
    load_runtime_targets,
)
from skill_library.intake import evaluate_candidate
from skill_library.intake_capture import (
    capture_dirty_target,
    convert_incoming_to_intake,
    scan_target_dirty_state,
)
from skill_library.manifest import RuntimeManifest
from skill_library.publisher import (
    get_commit_tree_sha,
    get_library_tree_sha,
    publish_runtime_branch,
)
from skill_library.sync import (
    detect_target_state,
    sync_all_targets,
    sync_target,
)
from skill_library.validator import validate_library_integrity


def run_git(cmd, cwd, check=True):
    return subprocess.run(
        ["git"] + cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
    )


class TestRuntimeGitClonePublication(unittest.TestCase):
    """Isolated unit and integration test suite covering 14 core requirements."""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.sandbox = Path(self.tmp_dir.name)

        # Initialize mock main repository
        self.repo_dir = self.sandbox / "origin-repo"
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        run_git(["init", "-b", "main"], cwd=self.repo_dir)
        run_git(["config", "user.name", "Test Runner"], cwd=self.repo_dir)
        run_git(["config", "user.email", "test@example.com"], cwd=self.repo_dir)

        # Setup standard library structure inside repo
        self.lib_dir = self.repo_dir / "library"
        self.cat1_dir = self.lib_dir / "quality-and-security" / "debugging"
        self.cat1_dir.mkdir(parents=True, exist_ok=True)
        self.cat2_dir = self.lib_dir / "workflow-and-automation" / "tool-integration"
        self.cat2_dir.mkdir(parents=True, exist_ok=True)

        # Create routers for all categories and deep subcategories
        root_links = []
        for cat in CATEGORIES:
            cat_r = self.lib_dir / cat / "SKILL.md"
            cat_r.parent.mkdir(parents=True, exist_ok=True)
            root_links.append(f"- [{cat}]({cat}/SKILL.md)")
            if not cat_r.exists():
                cat_r.write_text(f"# {cat} Router\n\n")

        for cat, subcats in DEEP_CATEGORIES.items():
            for sub in subcats:
                sub_r = self.lib_dir / cat / sub / "SKILL.md"
                sub_r.parent.mkdir(parents=True, exist_ok=True)
                if not sub_r.exists():
                    sub_r.write_text(f"# {sub} Router\n\n")

        (self.lib_dir / "SKILL.md").write_text("# Root Router\n\n" + "\n".join(root_links) + "\n")
        (self.lib_dir / "quality-and-security" / "SKILL.md").write_text(
            "# Quality Router\n\n- [`bug-hunter`](debugging/bug-hunter/SKILL.md)\n"
        )
        (self.lib_dir / "workflow-and-automation" / "SKILL.md").write_text(
            "# Workflow Router\n\n- [`task-runner`](tool-integration/task-runner/SKILL.md)\n"
        )

        # Skills
        bug_hunter = self.cat1_dir / "bug-hunter"
        bug_hunter.mkdir(parents=True, exist_ok=True)
        (bug_hunter / "SKILL.md").write_text(
            "---\nname: bug-hunter\ndescription: Hunt bugs. Use when hunting application defects.\n---\n# Bug Hunter\n"
        )

        task_runner = self.cat2_dir / "task-runner"
        task_runner.mkdir(parents=True, exist_ok=True)
        (task_runner / "SKILL.md").write_text(
            "---\nname: task-runner\ndescription: Run tasks. Use when running workflow tasks.\n---\n# Task Runner\n"
        )

        # Non-canonical repo folders
        (self.repo_dir / "docs").mkdir(parents=True, exist_ok=True)
        (self.repo_dir / "docs" / "README.md").write_text("# Docs\n")
        (self.repo_dir / "tools").mkdir(parents=True, exist_ok=True)
        (self.repo_dir / "tools" / "script.py").write_text("# Tools\n")
        (self.repo_dir / "config").mkdir(parents=True, exist_ok=True)
        (self.repo_dir / "config" / "settings.json").write_text("{}\n")
        (self.repo_dir / "intake").mkdir(parents=True, exist_ok=True)

        # Manifest
        self.audit_dir = self.repo_dir / "audit"
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.audit_dir / "runtime-manifest.json"
        self.manifest = RuntimeManifest(manifest_path=str(self.manifest_path))
        self.manifest.add_skill(
            runtime_name="bug-hunter",
            canonical_name="bug-hunter",
            canonical_path="library/quality-and-security/debugging/bug-hunter",
            functional_parent="library/quality-and-security/SKILL.md",
            source="test",
            managed=True,
        )
        self.manifest.add_skill(
            runtime_name="task-runner",
            canonical_name="task-runner",
            canonical_path="library/workflow-and-automation/tool-integration/task-runner",
            functional_parent="library/workflow-and-automation/SKILL.md",
            source="test",
            managed=True,
        )
        self.manifest.save()

        # Commit initial state on main
        run_git(["add", "."], cwd=self.repo_dir)
        run_git(["commit", "-m", "Initial commit on main"], cwd=self.repo_dir)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_01_publish_runtime_generates_root_tree_matching_library(self):
        """Requirement 1: publish-runtime generates a root tree exactly matching main:library/."""
        res = publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        self.assertEqual(res["status"], "created")

        lib_tree = get_library_tree_sha(str(self.repo_dir), ref="HEAD")
        runtime_commit = res["commit_sha"]
        runtime_tree = get_commit_tree_sha(str(self.repo_dir), runtime_commit)

        self.assertEqual(lib_tree, runtime_tree)
        self.assertEqual(res["tree_sha"], lib_tree)

    def test_02_non_canonical_paths_absent_from_runtime_branch(self):
        """Requirement 2: non-canonical paths (docs/, tools/, intake/, config/) are absent from runtime branch."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        ls_proc = run_git(["ls-tree", "--name-only", "runtime"], cwd=self.repo_dir)
        runtime_root_items = set(ls_proc.stdout.splitlines())

        self.assertIn("quality-and-security", runtime_root_items)
        self.assertIn("workflow-and-automation", runtime_root_items)
        self.assertIn("SKILL.md", runtime_root_items)

        # Strictly absent from runtime root
        self.assertNotIn("docs", runtime_root_items)
        self.assertNotIn("tools", runtime_root_items)
        self.assertNotIn("intake", runtime_root_items)
        self.assertNotIn("config", runtime_root_items)
        self.assertNotIn("audit", runtime_root_items)
        self.assertNotIn("library", runtime_root_items)

    def test_03_unchanged_library_makes_publish_runtime_noop(self):
        """Requirement 3: an unchanged library/ makes publish-runtime a no-op."""
        res1 = publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        self.assertEqual(res1["status"], "created")

        # Second call without changes
        res2 = publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        self.assertEqual(res2["status"], "unchanged")
        self.assertEqual(res1["commit_sha"], res2["commit_sha"])

    def test_04_modified_skill_updates_runtime_commit_and_tree(self):
        """Requirement 4: a modified skill updates the runtime branch commit and tree correctly."""
        res1 = publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        initial_commit = res1["commit_sha"]

        # Modify skill on main
        skill_file = self.cat1_dir / "bug-hunter" / "SKILL.md"
        skill_file.write_text(skill_file.read_text() + "\n## Added Section\n")
        run_git(["add", "."], cwd=self.repo_dir)
        run_git(["commit", "-m", "Update bug-hunter skill"], cwd=self.repo_dir)

        # Publish updated runtime branch
        res2 = publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        self.assertEqual(res2["status"], "updated")
        self.assertNotEqual(initial_commit, res2["commit_sha"])

        # Check commit history parentage
        parent_proc = run_git(["rev-parse", "runtime^"], cwd=self.repo_dir)
        self.assertEqual(parent_proc.stdout.strip(), initial_commit)

    def test_05_target_configuration_loading_and_schema_validation(self):
        """Requirement 5: target configuration loading and schema validation."""
        cfg_file = self.sandbox / "runtime-targets.json"
        cfg_data = {
            "targets": [
                {
                    "name": "custom-global",
                    "path": "~/test-agents/skills",
                    "mode": "full",
                    "accept_external_intake": True,
                    "enabled": True,
                },
                {
                    "name": "custom-subset",
                    "path": "~/test-gemini/skills",
                    "mode": "subset",
                    "include": ["quality-and-security"],
                    "accept_external_intake": False,
                    "enabled": False,
                },
            ]
        }
        cfg_file.write_text(json.dumps(cfg_data, indent=2))

        targets = load_runtime_targets(str(cfg_file))
        self.assertEqual(len(targets), 2)
        self.assertEqual(targets[0].name, "custom-global")
        self.assertEqual(targets[0].mode, "full")
        self.assertTrue(targets[0].accept_external_intake)
        self.assertEqual(targets[1].name, "custom-subset")
        self.assertEqual(targets[1].mode, "subset")
        self.assertEqual(targets[1].include, ["quality-and-security"])
        self.assertFalse(targets[1].enabled)

    def test_06_full_target_synchronization_produces_physical_git_clone_on_runtime(self):
        """Requirement 6: full target synchronization produces a physical Git clone on runtime."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)

        target_path = self.sandbox / "target-full"
        target = RuntimeTarget(name="test-full", path=str(target_path), mode="full", enabled=True)

        report = sync_target(target, source_repo=str(self.repo_dir))
        self.assertEqual(report.status, "created")
        self.assertTrue(target_path.exists())
        self.assertTrue((target_path / ".git").exists())

        # Physical file presence and zero symlinks
        skill_file = target_path / "quality-and-security" / "debugging" / "bug-hunter" / "SKILL.md"
        self.assertTrue(skill_file.exists())
        self.assertFalse(skill_file.is_symlink())

        state = detect_target_state(target_path)
        self.assertEqual(state["branch"], "runtime")
        self.assertFalse(state["is_dirty"])

    def test_07_subset_target_synchronization_configures_sparse_checkout(self):
        """Requirement 7: subset target synchronization configures sparse-checkout and materializes only selected scopes."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)

        target_path = self.sandbox / "target-subset"
        target = RuntimeTarget(
            name="test-subset",
            path=str(target_path),
            mode="subset",
            include=["quality-and-security"],
            enabled=True,
        )

        report = sync_target(target, source_repo=str(self.repo_dir))
        self.assertEqual(report.status, "created")

        # Included scope is materialized
        self.assertTrue((target_path / "quality-and-security" / "debugging" / "bug-hunter" / "SKILL.md").exists())
        # Excluded scope is NOT materialized
        self.assertFalse((target_path / "workflow-and-automation").exists())

        state = detect_target_state(target_path)
        self.assertTrue(state["sparse_enabled"])
        self.assertIn("quality-and-security", state["sparse_rules"])

    def test_08_clean_target_fast_forwards_when_runtime_branch_updates(self):
        """Requirement 8: a clean target fast-forwards when the runtime branch updates."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-ff"
        target = RuntimeTarget(name="test-ff", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Add commit to main and update runtime branch
        new_skill = self.cat1_dir / "new-feature"
        new_skill.mkdir(parents=True, exist_ok=True)
        (new_skill / "SKILL.md").write_text("---\nname: new-feature\ndescription: New.\n---\n")
        run_git(["add", "."], cwd=self.repo_dir)
        run_git(["commit", "-m", "Add new-feature skill"], cwd=self.repo_dir)
        res = publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        new_runtime_sha = res["commit_sha"]

        # Sync target
        rep = sync_target(target, source_repo=str(self.repo_dir))
        self.assertEqual(rep.status, "updated")
        self.assertEqual(rep.commit_sha, new_runtime_sha)
        self.assertTrue((target_path / "quality-and-security" / "debugging" / "new-feature" / "SKILL.md").exists())

    def test_09_dirty_target_is_never_overwritten_or_reset_during_sync(self):
        """Requirement 9: a dirty target is never overwritten or reset during sync."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-dirty"
        target = RuntimeTarget(name="test-dirty", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Simulate external modification (e.g. skills.sh installing an untracked skill)
        untracked_skill = target_path / "quality-and-security" / "debugging" / "skills-sh-installed"
        untracked_skill.mkdir(parents=True, exist_ok=True)
        untracked_file = untracked_skill / "SKILL.md"
        untracked_file.write_text("---\nname: skills-sh-installed\ndescription: External.\n---\n")

        # Sync target should detect dirty state and REFUSE destructive operation
        rep = sync_target(target, source_repo=str(self.repo_dir))
        self.assertEqual(rep.status, "dirty")
        self.assertTrue(len(rep.dirty_files) > 0)
        self.assertTrue(untracked_file.exists())
        self.assertIn("Refusing destructive update", rep.message)

    def test_10_local_intake_collector_groups_dirty_runtime_files_into_incoming_snapshot(self):
        """Requirement 10: local intake collector groups dirty runtime files into incoming/* snapshot."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-collector"
        target = RuntimeTarget(name="test-collector", path=str(target_path), mode="full", accept_external_intake=True, enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Add dirty files
        pkg1 = target_path / "custom-pkg-one"
        pkg1.mkdir(parents=True, exist_ok=True)
        (pkg1 / "SKILL.md").write_text("---\nname: custom-pkg-one\ndescription: Test.\n---\n")

        dirty_state = scan_target_dirty_state(target_path)
        self.assertTrue(dirty_state["is_dirty"])
        self.assertIn("custom-pkg-one", dirty_state["packages"])

        # Capture dirty state without remote push
        cap = capture_dirty_target(target, push=False)
        self.assertTrue(cap["captured"])
        self.assertTrue(cap["branch"].startswith("incoming/"))
        self.assertIn("custom-pkg-one", cap["packages"])

    def test_11_local_intake_collector_does_not_clear_dirty_working_state_if_push_fails(self):
        """Requirement 11: local intake collector does not clear dirty working state if snapshot push fails."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-push-fail"
        target = RuntimeTarget(name="test-push-fail", path=str(target_path), mode="full", accept_external_intake=True, enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Add dirty file
        dirty_file = target_path / "unpushed-skill" / "SKILL.md"
        dirty_file.parent.mkdir(parents=True, exist_ok=True)
        dirty_file.write_text("---\nname: unpushed-skill\ndescription: Retained.\n---\n")

        # Attempt capture with invalid remote to trigger push failure
        cap = capture_dirty_target(target, remote="nonexistent-remote", push=True)
        self.assertFalse(cap["captured"])
        self.assertTrue(cap["retained"])
        self.assertIn("Failed to push", cap["error"])

        # The dirty files MUST be preserved and not wiped
        self.assertTrue(dirty_file.exists())

    def test_12_github_intake_workflow_conversion_produces_reviewed_intake_branch_from_main(self):
        """Requirement 12: GitHub intake workflow conversion produces a reviewed intake/* branch from main."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-workflow"
        target = RuntimeTarget(name="test-workflow", path=str(target_path), mode="full", accept_external_intake=True, enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Add dirty skill and capture with push
        incoming_skill = target_path / "external-tool"
        incoming_skill.mkdir(parents=True, exist_ok=True)
        (incoming_skill / "SKILL.md").write_text("---\nname: external-tool\ndescription: From skills.sh.\n---\n")

        cap = capture_dirty_target(target, remote="origin", push=True)
        self.assertTrue(cap["captured"])
        incoming_branch = cap["branch"]

        # Run conversion
        res = convert_incoming_to_intake(
            repo_path=str(self.repo_dir),
            incoming_branch=incoming_branch,
            base_branch="main",
            remote="origin",
        )
        self.assertTrue(res["intake_branch"].startswith("intake/"))
        self.assertIn("external-tool", res["packages_staged"])

        # Verify staged package in intake/
        staged_pkg = self.repo_dir / "intake" / "external-tool"
        self.assertTrue((staged_pkg / "SKILL.md").exists())
        self.assertTrue((staged_pkg / ".installer-metadata.json").exists())

    def test_13_duplicate_candidates_with_synthetic_suffixes_rejected_or_routed_to_merge(self):
        """Requirement 13: duplicate candidates with synthetic suffixes (_1, _v1) are rejected or routed to merge."""
        # Candidate 1: synthetic version suffix `bug-hunter_v1`
        c1_dir = self.repo_dir / "intake" / "bug-hunter_v1"
        c1_dir.mkdir(parents=True, exist_ok=True)
        (c1_dir / "SKILL.md").write_text(
            "---\nname: bug-hunter_v1\ndescription: Autonomous system to identify and capture code bugs. Use when hunting application defects.\n---\n# Bug Hunter V1\n"
        )

        ev1 = evaluate_candidate(
            candidate_name="bug-hunter_v1",
            intake_dir=str(self.repo_dir / "intake"),
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
        )
        self.assertTrue(ev1.approval_required)
        self.assertTrue(ev1.name_collision)
        self.assertIn(ev1.recommended_decision, ["REJECT", "MERGE"])

        # Candidate 2: synthetic counter suffix `bug-hunter_1`
        c2_dir = self.repo_dir / "intake" / "bug-hunter_1"
        c2_dir.mkdir(parents=True, exist_ok=True)
        (c2_dir / "SKILL.md").write_text(
            "---\nname: bug-hunter_1\ndescription: Bug hunter variant. Use when hunting application defects.\n---\n# Bug Hunter 1\n"
        )

        ev2 = evaluate_candidate(
            candidate_name="bug-hunter_1",
            intake_dir=str(self.repo_dir / "intake"),
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
        )
        self.assertTrue(ev2.approval_required)
        self.assertTrue(ev2.name_collision)
        self.assertIn(ev2.recommended_decision, ["REJECT", "MERGE"])

    def test_14_living_library_validation_passes_without_symlinks(self):
        """Requirement 14: living library validation passes against published runtime trees and targets without symlinks."""
        # Publish runtime branch
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)

        # Create target config
        target_path = self.sandbox / "target-val"
        target = RuntimeTarget(name="test-val", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        cfg_file = self.repo_dir / "config" / "runtime-targets.json"
        cfg_file.write_text(json.dumps({
            "targets": [
                {
                    "name": "test-val",
                    "path": str(target_path),
                    "mode": "full",
                    "accept_external_intake": True,
                    "enabled": True,
                }
            ]
        }, indent=2))

        # Validate library integrity
        res = validate_library_integrity(
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
            config_path=str(cfg_file),
            verify_publication=True,
            verify_targets=True,
        )

        self.assertTrue(res.is_valid, msg=res.summary())
        self.assertTrue(res.canonical_reconciliation_passed)
        self.assertTrue(res.runtime_publication_passed)
        self.assertTrue(res.target_reconciliation_passed)
        self.assertEqual(len(res.broken_router_links), 0)
        self.assertEqual(len(res.publication_errors), 0)
        self.assertEqual(len(res.target_errors), 0)

    def test_15_target_validation_fails_on_wrong_remote(self):
        """Target validation fails when checkout origin URL does not match source repository."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-bad-remote"
        target = RuntimeTarget(name="bad-remote", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Point origin to a completely different, unauthorized remote
        run_git(["remote", "set-url", "origin", "https://unauthorized-remote.example.com/fake.git"], cwd=target_path)

        cfg_file = self.repo_dir / "config" / "runtime-targets.json"
        cfg_file.write_text(json.dumps({
            "targets": [{"name": "bad-remote", "path": str(target_path), "mode": "full", "enabled": True}]
        }))

        res = validate_library_integrity(
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
            config_path=str(cfg_file),
            verify_publication=True,
            verify_targets=True,
        )
        self.assertFalse(res.is_valid)
        self.assertFalse(res.target_reconciliation_passed)
        self.assertTrue(any("remote URL" in err and "does not match" in err for err in res.target_errors))

    def test_16_target_validation_fails_on_wrong_branch(self):
        """Target validation fails when target checkout is not on runtime branch."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-bad-branch"
        target = RuntimeTarget(name="bad-branch", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Switch to main or other branch in target
        run_git(["checkout", "-b", "feature-wrong"], cwd=target_path)

        cfg_file = self.repo_dir / "config" / "runtime-targets.json"
        cfg_file.write_text(json.dumps({
            "targets": [{"name": "bad-branch", "path": str(target_path), "mode": "full", "enabled": True}]
        }))

        res = validate_library_integrity(
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
            config_path=str(cfg_file),
            verify_publication=True,
            verify_targets=True,
        )
        self.assertFalse(res.is_valid)
        self.assertFalse(res.target_reconciliation_passed)
        self.assertTrue(any("on branch 'feature-wrong'" in err for err in res.target_errors))

    def test_17_target_validation_fails_on_commit_mismatch(self):
        """Target validation fails when target HEAD commit does not match published runtime commit."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-commit-mismatch"
        target = RuntimeTarget(name="commit-mismatch", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Commit an extra commit directly in the target on branch runtime
        test_file = target_path / "extra.txt"
        test_file.write_text("drift")
        run_git(["add", "extra.txt"], cwd=target_path)
        run_git(["commit", "-m", "Drift commit"], cwd=target_path)

        cfg_file = self.repo_dir / "config" / "runtime-targets.json"
        cfg_file.write_text(json.dumps({
            "targets": [{"name": "commit-mismatch", "path": str(target_path), "mode": "full", "enabled": True}]
        }))

        res = validate_library_integrity(
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
            config_path=str(cfg_file),
            verify_publication=True,
            verify_targets=True,
        )
        self.assertFalse(res.is_valid)
        self.assertFalse(res.target_reconciliation_passed)
        self.assertTrue(any("HEAD commit" in err and "does not match" in err for err in res.target_errors))

    def test_18_target_validation_fails_on_sparse_scope_mismatch(self):
        """Target validation fails when subset target sparse rules do not match include list."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-bad-sparse"
        target = RuntimeTarget(
            name="bad-sparse",
            path=str(target_path),
            mode="subset",
            include=["design-and-experience/design-systems"],
            enabled=True,
        )
        sync_target(target, source_repo=str(self.repo_dir))

        # Reconfigure sparse checkout to a different scope
        run_git(["sparse-checkout", "set", "quality-and-security/debugging"], cwd=target_path)

        cfg_file = self.repo_dir / "config" / "runtime-targets.json"
        cfg_file.write_text(json.dumps({
            "targets": [{
                "name": "bad-sparse",
                "path": str(target_path),
                "mode": "subset",
                "include": ["design-and-experience/design-systems"],
                "enabled": True,
            }]
        }))

        res = validate_library_integrity(
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
            config_path=str(cfg_file),
            verify_publication=True,
            verify_targets=True,
        )
        self.assertFalse(res.is_valid)
        self.assertFalse(res.target_reconciliation_passed)
        self.assertTrue(any("sparse scopes" in err and "do not match configured include" in err for err in res.target_errors))

    def test_19_target_validation_fails_when_full_target_has_sparse_active(self):
        """Target validation fails when a target configured as full has sparse-checkout filtering active."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-bad-full"
        target = RuntimeTarget(name="bad-full", path=str(target_path), mode="full", enabled=True)
        sync_target(target, source_repo=str(self.repo_dir))

        # Enable sparse-checkout on a full target
        run_git(["sparse-checkout", "init", "--cone"], cwd=target_path)
        run_git(["sparse-checkout", "set", "workflow-and-automation"], cwd=target_path)

        cfg_file = self.repo_dir / "config" / "runtime-targets.json"
        cfg_file.write_text(json.dumps({
            "targets": [{"name": "bad-full", "path": str(target_path), "mode": "full", "enabled": True}]
        }))

        res = validate_library_integrity(
            library_dir=str(self.lib_dir),
            manifest=self.manifest,
            config_path=str(cfg_file),
            verify_publication=True,
            verify_targets=True,
        )
        self.assertFalse(res.is_valid)
        self.assertFalse(res.target_reconciliation_passed)
    def test_20_end_to_end_remote_clone_dirty_capture_fresh_conversion(self):
        """Requirement 20: bare upstream remote end-to-end test.
        Clones target from bare remote, dirties target with new skill and update,
        captures and pushes snapshot to bare remote, resets cleanly,
        and converts from a completely separate fresh runner clone.
        """
        # 1. Publish runtime branch
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)

        # 2. Set up bare remote standing in for GitHub
        remote_bare = self.sandbox / "upstream-github.git"
        run_git(["init", "--bare", str(remote_bare)], cwd=self.sandbox)
        run_git(["push", str(remote_bare), "main:main", "runtime:runtime"], cwd=self.repo_dir)
        run_git(["symbolic-ref", "HEAD", "refs/heads/main"], cwd=remote_bare)

        # 3. Clone runtime target against bare upstream remote URL
        target_path = self.sandbox / "target-e2e-workstation"
        target = RuntimeTarget(
            name="e2e-workstation",
            path=str(target_path),
            mode="full",
            remote_url=str(remote_bare),
            accept_external_intake=True,
            enabled=True,
        )
        sync_res = sync_target(target, remote_url=str(remote_bare))
        self.assertEqual(sync_res.status, "created")

        # Verify origin URL points to the bare upstream
        t_url = run_git(["config", "--get", "remote.origin.url"], cwd=target_path).stdout.strip()
        self.assertEqual(t_url, str(remote_bare))

        # 4. Dirty the target: one new external skill, one updated hierarchical skill
        new_skill = target_path / "community-new-tool"
        new_skill.mkdir(parents=True, exist_ok=True)
        (new_skill / "SKILL.md").write_text("---\nname: community-new-tool\ndescription: Brand new tool from external intake.\n---\n# Community Tool\n")

        # Real hierarchical skill in runtime: quality-and-security/debugging/bug-hunter
        update_skill = target_path / "quality-and-security" / "debugging" / "bug-hunter"
        self.assertTrue(update_skill.exists(), "bug-hunter must physically exist in published runtime clone")
        (update_skill / "SKILL.md").write_text("---\nname: bug-hunter\ndescription: Updated description for bug-hunter.\n---\n# Bug Hunter Updated\n")

        # Verify dirty scanner groups changed files by nearest package root
        dirty_before_cap = scan_target_dirty_state(target_path)
        self.assertTrue(dirty_before_cap["is_dirty"])
        self.assertIn("bug-hunter", dirty_before_cap["packages"])
        self.assertIn("quality-and-security/debugging/bug-hunter", dirty_before_cap["packages"])
        self.assertIn("community-new-tool", dirty_before_cap["packages"])

        # 5. Capture dirty state, pushing incoming branch to bare upstream
        cap = capture_dirty_target(target, remote="origin", push=True, trigger_workflow=False)
        self.assertTrue(cap["captured"])
        self.assertTrue(cap["pushed"])
        self.assertTrue(cap["reset"])
        self.assertIn("bug-hunter", cap["packages"])
        self.assertIn("community-new-tool", cap["packages"])
        incoming_branch = cap["branch"]

        # Target should now be reset and clean on branch runtime
        d_state = scan_target_dirty_state(target_path)
        self.assertFalse(d_state["is_dirty"])

        # 6. Fresh runner clone from bare remote (no access to workstation filesystem)
        fresh_runner = self.sandbox / "github-runner-fresh"
        run_git(["clone", str(remote_bare), str(fresh_runner)], cwd=self.sandbox)

        # 7. Convert incoming branch to intake on the fresh runner
        conv_res = convert_incoming_to_intake(
            repo_path=str(fresh_runner),
            incoming_branch=incoming_branch,
            base_branch="main",
            remote="origin",
        )
        self.assertTrue(conv_res["intake_branch"].startswith("intake/"))
        self.assertIn("community-new-tool", conv_res["packages_staged"])
        self.assertIn("bug-hunter", conv_res["packages_staged"])

        # 8. Verify metadata classifications: new vs external_update
        intake_dir = fresh_runner / "intake"
        self.assertTrue((intake_dir / "bug-hunter").exists())
        self.assertTrue((intake_dir / "community-new-tool").exists())
        # CRITICAL: Parent category and subcategory must NOT be copied wholesale into intake/!
        self.assertFalse((intake_dir / "quality-and-security").exists(), "Category directory must not be copied into intake")
        self.assertFalse((intake_dir / "debugging").exists(), "Subcategory directory must not be copied into intake")

        new_meta = json.loads((intake_dir / "community-new-tool" / ".installer-metadata.json").read_text())
        self.assertEqual(new_meta["classification"], "EXTERNAL_PHYSICAL")
        self.assertEqual(new_meta["type"], "external_install")

        upd_meta = json.loads((intake_dir / "bug-hunter" / ".installer-metadata.json").read_text())
        self.assertEqual(upd_meta["classification"], "EXTERNAL_UPDATE")
        self.assertEqual(upd_meta["type"], "external_update")
        self.assertEqual(upd_meta["target_canonical_path"], "library/quality-and-security/debugging/bug-hunter")
        self.assertEqual(upd_meta["runtime_path"], "quality-and-security/debugging/bug-hunter")
        self.assertEqual(upd_meta["package_name"], "bug-hunter")

        # 9. Verify invalid ref is rejected
        with self.assertRaises(ValueError):
            convert_incoming_to_intake(str(fresh_runner), "main")
        with self.assertRaises(ValueError):
            convert_incoming_to_intake(str(fresh_runner), "incoming/bad;injection")

    def test_21_accept_external_intake_enforcement_and_dispatch_failure(self):
        """Requirement 21: accept_external_intake enforcement and workflow dispatch error tracking."""
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)
        target_path = self.sandbox / "target-intake-policy"
        target = RuntimeTarget(
            name="test-policy",
            path=str(target_path),
            mode="full",
            accept_external_intake=False,
            enabled=True,
        )
        sync_target(target, source_repo=str(self.repo_dir))

        # Add dirty file
        dirty_file = target_path / "community-tool" / "SKILL.md"
        dirty_file.parent.mkdir(parents=True, exist_ok=True)
        dirty_file.write_text("---\nname: community-tool\n---\n")

        # 1. When accept_external_intake is False, capture is skipped
        cap_skip = capture_dirty_target(target, push=False, force=False)
        self.assertFalse(cap_skip["captured"])
        self.assertIn("accept_external_intake is False", cap_skip["reason"])

        # 2. When force is True, capture proceeds
        cap_force = capture_dirty_target(target, push=False, force=True)
        self.assertTrue(cap_force["captured"])
        self.assertIn("community-tool", cap_force["packages"])

        # 3. Test push failure retains dirty state locally
        # Add new dirty change to target
        extra_file = target_path / "community-tool" / "extra.py"
        extra_file.parent.mkdir(parents=True, exist_ok=True)
        extra_file.write_text("print('dirty extra')\n")

        cap_push_fail = capture_dirty_target(
            target,
            remote="nonexistent-remote",
            push=True,
            trigger_workflow=False,
            force=True,
        )
        self.assertFalse(cap_push_fail["captured"])
        self.assertTrue(cap_push_fail.get("retained", False))
        self.assertTrue(extra_file.exists())

        # 4. Test dispatch failure after successful push:
        # Reset target back to clean runtime state first
        run_git(["checkout", "runtime"], cwd=target_path)
        run_git(["reset", "--hard", "origin/runtime"], cwd=target_path)
        run_git(["clean", "-fd"], cwd=target_path)

        # Dirty a new file for dispatch test
        dispatch_file = target_path / "community-tool" / "dispatch_test.py"
        dispatch_file.parent.mkdir(parents=True, exist_ok=True)
        dispatch_file.write_text("print('test dispatch')\n")

        # remote snapshot branch is preserved, local runtime is restored,
        # but workflow_error is recorded and workflow_triggered is False.
        # Push to the valid test repo as remote
        cap_dispatch = capture_dirty_target(
            target,
            remote="origin",
            push=True,
            trigger_workflow=True,
            force=True,
        )
        self.assertTrue(cap_dispatch["captured"])
        self.assertTrue(cap_dispatch["pushed"])
        self.assertTrue(cap_dispatch["reset"])
        self.assertFalse(cap_dispatch["workflow_triggered"])
        self.assertIn("workflow_error", cap_dispatch)

    def test_22_duplicate_leaf_name_intake_collision_resolution(self):
        """Requirement 22: duplicate leaf skill names in different taxonomy paths
        resolve deterministically to distinct, collision-safe intake directories
        without overwriting one another.
        """
        # 1. Setup duplicate leaf skills in mock library and manifest
        dev_ad = self.lib_dir / "development" / "backend" / "ad-creative"
        dev_ad.mkdir(parents=True, exist_ok=True)
        (dev_ad / "SKILL.md").write_text("---\nname: ad-creative\ndescription: Backend ad creative generation.\n---\n# Ad Creative Backend\n")

        mkt_ad = self.lib_dir / "marketing-and-seo" / "content-and-campaigns" / "ad-creative"
        mkt_ad.mkdir(parents=True, exist_ok=True)
        (mkt_ad / "SKILL.md").write_text("---\nname: ad-creative\ndescription: Marketing campaign ad creative.\n---\n# Ad Creative Marketing\n")

        manifest_file = self.repo_dir / "audit" / "runtime-manifest.json"
        manifest_file.parent.mkdir(parents=True, exist_ok=True)
        m = RuntimeManifest(str(manifest_file))
        m.add_skill(
            runtime_name="development-ad-creative",
            canonical_name="ad-creative",
            canonical_path="library/development/backend/ad-creative",
            functional_parent="library/development/backend/SKILL.md",
        )
        m.add_skill(
            runtime_name="marketing-and-seo-ad-creative",
            canonical_name="ad-creative",
            canonical_path="library/marketing-and-seo/content-and-campaigns/ad-creative",
            functional_parent="library/marketing-and-seo/content-and-campaigns/SKILL.md",
        )
        m.save()

        run_git(["add", "library", "audit"], cwd=self.repo_dir)
        run_git(["commit", "-m", "Add duplicate leaf skills for collision testing"], cwd=self.repo_dir)

        # 2. Publish runtime branch
        publish_runtime_branch(str(self.repo_dir), branch_name="runtime", push=False)

        # 3. Set up bare remote standing in for GitHub
        remote_bare = self.sandbox / "upstream-github-22.git"
        run_git(["init", "--bare", str(remote_bare)], cwd=self.sandbox)
        run_git(["push", str(remote_bare), "main:main", "runtime:runtime"], cwd=self.repo_dir)
        run_git(["symbolic-ref", "HEAD", "refs/heads/main"], cwd=remote_bare)

        # 4. Clone runtime target against bare upstream
        target_path = self.sandbox / "target-collision-workstation"
        target = RuntimeTarget(
            name="collision-workstation",
            path=str(target_path),
            mode="full",
            remote_url=str(remote_bare),
            accept_external_intake=True,
            enabled=True,
        )
        sync_res = sync_target(target, remote_url=str(remote_bare))
        self.assertEqual(sync_res.status, "created")

        # 5. Verify both duplicate skills exist in published runtime
        skill1 = target_path / "development" / "backend" / "ad-creative" / "SKILL.md"
        skill2 = target_path / "marketing-and-seo" / "content-and-campaigns" / "ad-creative" / "SKILL.md"
        self.assertTrue(skill1.exists(), "development/backend/ad-creative must exist in runtime")
        self.assertTrue(skill2.exists(), "marketing-and-seo/.../ad-creative must exist in runtime")

        # 6. Dirty BOTH skills with distinct content
        skill1.write_text("---\nname: ad-creative\ndescription: Updated dev backend ad-creative.\n---\n# Backend Ad Creative Updated\n")
        skill2.write_text("---\nname: ad-creative\ndescription: Updated marketing ad-creative.\n---\n# Marketing Ad Creative Updated\n")

        # 7. Capture dirty state into incoming snapshot branch
        cap = capture_dirty_target(target, remote="origin", push=True, trigger_workflow=False)
        self.assertTrue(cap["captured"])
        self.assertTrue(cap["pushed"])
        self.assertTrue(cap["reset"])
        self.assertEqual(len(cap["package_details"]), 2)
        incoming_branch = cap["branch"]

        # Target should now be reset and clean on branch runtime
        d_state = scan_target_dirty_state(target_path)
        self.assertFalse(d_state["is_dirty"])

        # 8. Fresh runner clone from bare remote
        fresh_runner = self.sandbox / "github-runner-fresh-22"
        run_git(["clone", str(remote_bare), str(fresh_runner)], cwd=self.sandbox)

        # 9. Convert incoming branch to intake on the fresh runner
        conv_res = convert_incoming_to_intake(
            repo_path=str(fresh_runner),
            incoming_branch=incoming_branch,
            base_branch="main",
            remote="origin",
        )
        self.assertTrue(conv_res["intake_branch"].startswith("intake/"))
        self.assertEqual(len(conv_res["packages_staged"]), 2)
        self.assertIn("development-ad-creative", conv_res["packages_staged"])
        self.assertIn("marketing-and-seo-ad-creative", conv_res["packages_staged"])

        # 10. Verify 2 separate intake directories exist and no files overwrite one another
        intake_dir = fresh_runner / "intake"
        dir1 = intake_dir / "development-ad-creative"
        dir2 = intake_dir / "marketing-and-seo-ad-creative"
        self.assertTrue(dir1.exists(), "development-ad-creative must exist in intake")
        self.assertTrue(dir2.exists(), "marketing-and-seo-ad-creative must exist in intake")
        self.assertFalse((intake_dir / "ad-creative").exists(), "Colliding un-prefixed leaf name must not be used")

        content1 = (dir1 / "SKILL.md").read_text()
        content2 = (dir2 / "SKILL.md").read_text()
        self.assertIn("Backend Ad Creative Updated", content1)
        self.assertIn("Marketing Ad Creative Updated", content2)
        self.assertNotEqual(content1, content2, "Skills must not overwrite one another")

        # 11. Check metadata: both EXTERNAL_UPDATE with exact canonical paths
        meta1 = json.loads((dir1 / ".installer-metadata.json").read_text())
        self.assertEqual(meta1["classification"], "EXTERNAL_UPDATE")
        self.assertEqual(meta1["type"], "external_update")
        self.assertEqual(meta1["package_name"], "ad-creative")
        self.assertEqual(meta1["runtime_name"], "development-ad-creative")
        self.assertEqual(meta1["runtime_path"], "development/backend/ad-creative")
        self.assertEqual(meta1["target_canonical_path"], "library/development/backend/ad-creative")

        meta2 = json.loads((dir2 / ".installer-metadata.json").read_text())
        self.assertEqual(meta2["classification"], "EXTERNAL_UPDATE")
        self.assertEqual(meta2["type"], "external_update")
        self.assertEqual(meta2["package_name"], "ad-creative")
        self.assertEqual(meta2["runtime_name"], "marketing-and-seo-ad-creative")
        self.assertEqual(meta2["runtime_path"], "marketing-and-seo/content-and-campaigns/ad-creative")
        self.assertEqual(meta2["target_canonical_path"], "library/marketing-and-seo/content-and-campaigns/ad-creative")


if __name__ == "__main__":
    unittest.main()

