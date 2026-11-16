"""
Unit tests for the execution contract: risk, side effects, permissions,
environment and load plans.

ZI-08 requires these to be tested as behaviour, not inferred from module
presence.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.execution import (
    EnvironmentRequirement,
    Permission,
    SideEffect,
    build_load_plan,
    derive_execution_profile,
    summarise_profiles,
)
from skill_library.identity import mint_canonical_id

LIBRARY = str(REPO_ROOT / "library")


def write_package(root: str, relative: str, body: str = "---\nname: demo\n---\n") -> str:
    path = os.path.join(root, *relative.split("/"))
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "SKILL.md"), "w", encoding="utf-8") as handle:
        handle.write(body)
    return path


class TestProseProfile(unittest.TestCase):
    def test_prose_is_safe_and_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/prose")
            profile = derive_execution_profile(pkg, library_dir=root)

            self.assertEqual(profile.tier, 4)
            self.assertEqual(profile.risk, "safe")
            self.assertIn(SideEffect.READS_FILES, profile.side_effects)
            self.assertIn(Permission.FILESYSTEM_READ, profile.permissions)
            self.assertNotIn(Permission.SHELL, profile.permissions)


class TestScriptProfile(unittest.TestCase):
    def test_scripts_raise_risk_and_grant_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/scripted")
            with open(os.path.join(pkg, "run.py"), "w", encoding="utf-8") as handle:
                handle.write("print('hi')\n")

            profile = derive_execution_profile(pkg, library_dir=root)

            self.assertEqual(profile.tier, 1)
            self.assertEqual(profile.risk, "elevated")
            self.assertIn(SideEffect.EXECUTES_COMMANDS, profile.side_effects)
            self.assertIn(Permission.SHELL, profile.permissions)
            self.assertIn("python", profile.environment.runtimes)


class TestCodeBlockProfile(unittest.TestCase):
    def test_executable_block_is_low_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/blocky", "---\nname: b\n---\n```bash\nls\n```\n")
            profile = derive_execution_profile(pkg, library_dir=root)

            self.assertEqual(profile.tier, 2)
            self.assertEqual(profile.risk, "low")
            self.assertIn(Permission.SHELL, profile.permissions)

    def test_illustrative_block_is_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/doc", "---\nname: d\n---\n```text\nhello\n```\n")
            profile = derive_execution_profile(pkg, library_dir=root)

            self.assertEqual(profile.tier, 3)
            self.assertEqual(profile.risk, "safe")
            self.assertNotIn(Permission.SHELL, profile.permissions)


class TestDestructiveDetection(unittest.TestCase):
    def test_destructive_command_in_code_raises_to_critical(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(
                root, "development/backend/danger", "---\nname: d\n---\n```bash\nrm -rf /tmp/x\n```\n"
            )
            profile = derive_execution_profile(pkg, library_dir=root)

            self.assertEqual(profile.risk, "critical")
            self.assertIn(SideEffect.DESTRUCTIVE, profile.side_effects)
            self.assertIn("destructive_command_pattern", profile.evidence)

    def test_destructive_word_in_prose_is_not_a_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(
                root,
                "development/backend/prose-danger",
                "---\nname: d\n---\nThey will auto-start on reboot. Do not run shutdown casually.\n",
            )
            profile = derive_execution_profile(pkg, library_dir=root)

            self.assertNotEqual(profile.risk, "critical")
            self.assertNotIn(SideEffect.DESTRUCTIVE, profile.side_effects)


class TestPhase09Refinement(unittest.TestCase):
    def test_phase09_shell_status_grants_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/prose", "---\nname: p\n---\ntext\n")
            index = {
                "prose": {
                    "shell_execution_status": "safe_shell_script",
                    "remote_execution_status": "no_remote_calls",
                    "destructive_operation_status": "read_only_or_additive",
                    "dependency_status": "none_static",
                }
            }
            profile = derive_execution_profile(pkg, phase09_index=index, library_dir=root)

            self.assertIn(Permission.SHELL, profile.permissions)
            self.assertIn("phase09_resource_registry", profile.evidence)

    def test_phase09_remote_status_adds_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/prose", "---\nname: p\n---\ntext\n")
            index = {
                "prose": {
                    "shell_execution_status": "no_shell_calls",
                    "remote_execution_status": "standard_api_client",
                    "destructive_operation_status": "read_only_or_additive",
                    "dependency_status": "none_static",
                }
            }
            profile = derive_execution_profile(pkg, phase09_index=index, library_dir=root)

            self.assertIn(SideEffect.NETWORK, profile.side_effects)
            self.assertIn(Permission.NETWORK, profile.permissions)
            self.assertTrue(profile.environment.needs_network)


class TestLoadPlan(unittest.TestCase):
    def test_plan_contains_entrypoint_and_scripts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/plan")
            with open(os.path.join(pkg, "run.py"), "w", encoding="utf-8") as handle:
                handle.write("pass\n")
            with open(os.path.join(pkg, "README.md"), "w", encoding="utf-8") as handle:
                handle.write("# docs\n")

            plan = build_load_plan(pkg, library_dir=root)

            self.assertEqual(plan.canonical_id, "development:plan")
            self.assertTrue(plan.entrypoint.endswith("SKILL.md"))
            self.assertEqual(plan.scripts, ["run.py"])
            self.assertIn("README.md", plan.resources)
            self.assertIn("python", plan.runtimes)

    def test_plan_is_none_for_non_canonical(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development")
            self.assertIsNone(build_load_plan(pkg))


class TestSummarise(unittest.TestCase):
    def test_aggregates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            write_package(root, "development/backend/a")
            write_package(root, "development/backend/b", "---\nname: b\n---\n```bash\nls\n```\n")

            profiles = [
                derive_execution_profile(p, library_dir=root)
                for p in (
                    os.path.join(root, "development/backend/a"),
                    os.path.join(root, "development/backend/b"),
                )
            ]
            summary = summarise_profiles(profiles)

            self.assertEqual(summary["total"], 2)
            self.assertEqual(summary["by_tier"], {2: 1, 4: 1})
            self.assertEqual(summary["by_risk"]["safe"], 1)
            self.assertEqual(summary["by_risk"]["low"], 1)


class TestRealLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from skill_library.execution import load_phase09_index
        from skill_library.identity import canonical_package_paths

        phase09 = load_phase09_index()
        cls.profiles = []
        for path in canonical_package_paths(LIBRARY):
            profile = derive_execution_profile(
                path, phase09_index=phase09, library_dir=LIBRARY
            )
            if profile:
                cls.profiles.append(profile)
        cls.summary = summarise_profiles(cls.profiles)

    def test_population(self):
        self.assertEqual(self.summary["total"], 2133)

    def test_every_package_has_a_risk(self):
        self.assertEqual(sum(self.summary["by_risk"].values()), 2133)

    def test_no_profile_is_unknown(self):
        self.assertNotIn("unknown", self.summary["by_risk"])

    def test_shell_permission_matches_executable_tiers(self):
        shell = self.summary["by_permission"].get("shell", 0)
        executable = self.summary["by_tier"].get(1, 0) + self.summary["by_tier"].get(2, 0)
        self.assertEqual(shell, executable)


if __name__ == "__main__":
    unittest.main()