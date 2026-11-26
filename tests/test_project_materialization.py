import json
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.librarian_ai import render_frontmatter
from skill_library.project_materialization import (
    MaterializationError,
    load_skills,
    materialize_project,
    resolve_groups,
)


def metadata(role="capability", applications=None, depends_on=None, composed_of=None, extends=None):
    return {
        "role": role,
        "applications": applications or [],
        "keywords": ["test"],
        "tags": ["test"],
        "depends_on": depends_on or [],
        "composed_of": composed_of or [],
        "extends": extends,
        "adapts": None,
        "aliased_to": None,
        "execution_provider": {"default": "prompt_template", "supported": []},
        "risk": "low",
        "side_effects": "read-only",
    }


def add_skill(library, category, subcategory, name, canonical_id, body, meta):
    directory = library / category / subcategory / name
    directory.mkdir(parents=True)
    fm = render_frontmatter(name, f"{name} description", meta, canonical_id)
    (directory / "SKILL.md").write_text(fm + "\n" + body, encoding="utf-8")
    return directory


def make_library(root):
    add_skill(root, "shared", "primitives", "auth", "shared:auth", "# Auth\n", metadata("primitive"))
    add_skill(
        root, "development", "backend", "api-caller", "dev:api-caller",
        "# API Caller\n", metadata("capability", ["react"], ["shared:auth"]),
    )
    add_skill(
        root, "marketing", "cro", "api-caller", "marketing:api-caller",
        "# Marketing Caller\n", metadata("capability", ["react"], ["shared:auth"]),
    )
    add_skill(
        root, "design-and-experience", "design-systems", "design-token", "design:token",
        "# Tokens\n", metadata("primitive", ["figma"]),
    )
    add_skill(
        root, "development", "backend", "app", "dev:app",
        "# App\n", metadata("workflow", ["react"], composed_of=["dev:api-caller"]),
    )


class TestProjectMaterialization(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.library = self.root / "test-library"
        self.target = self.root / "project" / ".agents" / "skills"
        make_library(self.library)

    def tearDown(self):
        self.tmp.cleanup()

    def test_nested_groups_match_include_and_exclude(self):
        skills, _, _ = load_skills(self.library)
        config = {"groups": {
            "figma": {"name": "Figma", "match": {"applications": ["figma"]}},
            "foundations": {"name": "Foundations", "include_paths": ["design-and-experience/design-systems"]},
            "bundle": {"name": "Bundle", "groups": ["figma", "foundations"], "skills": ["dev:app"], "exclude": ["design-token"]},
        }}
        groups, payloads = resolve_groups(config, skills)
        self.assertEqual(groups["bundle"].members, ["dev:app"])
        self.assertEqual(payloads["bundle"]["total_skills"], 1)

    def test_group_cycle_is_rejected(self):
        skills, _, _ = load_skills(self.library)
        with self.assertRaises(MaterializationError):
            resolve_groups({"groups": {"a": {"groups": ["b"]}, "b": {"groups": ["a"]}}}, skills)

    def test_materializes_closure_collision_names_and_lockfile(self):
        profile = {"name": "demo", "groups": [], "skills": ["dev:app", "marketing:api-caller"]}
        result = materialize_project(
            self.library, profile, {"groups": {}}, self.target, source_commit="abc123",
        )
        self.assertEqual(result["total_materialized"], 4)
        self.assertIn("shared:auth", result["closure"])
        self.assertEqual(result["runtime_names"]["dev:api-caller"], "development-api-caller")
        self.assertEqual(result["runtime_names"]["marketing:api-caller"], "marketing-api-caller")
        self.assertTrue((self.target / "development-api-caller" / "SKILL.md").exists())
        self.assertTrue((self.target / "SKILL.md").exists())
        lock = json.loads((self.target / "skills.lock.json").read_text())
        self.assertEqual(lock["source_commit"], "abc123")
        self.assertEqual(len(lock["skills"]["development-api-caller"]["content_hash"]), 64)

    def test_materialization_is_deterministic(self):
        profile = {"name": "demo", "skills": ["dev:app"]}
        materialize_project(self.library, profile, {"groups": {}}, self.target, source_commit="abc123")
        first = (self.target / "skills.lock.json").read_bytes()
        materialize_project(self.library, profile, {"groups": {}}, self.target, source_commit="abc123", replace=True)
        second = (self.target / "skills.lock.json").read_bytes()
        self.assertEqual(first, second)

    def test_missing_dependency_fails_before_target_creation(self):
        add_skill(
            self.library, "development", "backend", "broken", "dev:broken",
            "# Broken\n", metadata("capability", depends_on=["missing:dependency"]),
        )
        with self.assertRaises(MaterializationError):
            materialize_project(self.library, {"name": "broken", "skills": ["dev:broken"]}, {"groups": {}}, self.target)
        self.assertFalse(self.target.exists())

    def test_existing_target_requires_replace(self):
        self.target.mkdir(parents=True)
        (self.target / "keep.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(MaterializationError):
            materialize_project(self.library, {"name": "demo", "skills": ["dev:app"]}, {"groups": {}}, self.target)
        self.assertEqual((self.target / "keep.txt").read_text(), "keep")

    def test_real_library_is_rejected(self):
        with self.assertRaises(MaterializationError):
            materialize_project(
                self.library, {"name": "bad", "skills": ["dev:app"]}, {"groups": {}},
                REPO_ROOT / "library",
            )

    def test_cli_materializes_profile(self):
        import subprocess

        profile = self.root / "profile.json"
        groups = self.root / "groups.json"
        profile.write_text(json.dumps({"name": "cli", "skills": ["dev:app"]}), encoding="utf-8")
        groups.write_text(json.dumps({"groups": {}}), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "librarian_materialize.py"),
             "--profile", str(profile), "--groups", str(groups),
             "--library", str(self.library), "--target", str(self.target),
             "--source-commit", "abc123"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "skills.lock.json").exists())


if __name__ == "__main__":
    unittest.main()
