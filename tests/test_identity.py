"""
Unit and regression tests for deterministic canonical identity derivation.

Covers the ZI-07 scope rule:
  * scope = ownership root (via SCOPE_MAP), slug = leaf directory
  * functional categories are depth 3, operational roots are depth 2
  * nested sub-skills and routers are not minted
  * collisions are surfaced for ADR-004 5.2 adjudication, never resolved here
"""

import json
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

from skill_library.config import LIBRARY_DIR
from skill_library.identity import (
    SCOPE_MAP,
    canonical_package_paths,
    derive_scope,
    derive_slug,
    find_collisions,
    mint_canonical_id,
)

LIBRARY = str(REPO_ROOT / "library")


def census_population() -> int:
    """Authoritative canonical package count.

    Derived rather than hardcoded: the library changes whenever skills are
    added, merged or pruned, and a fixed denominator broke these tests every
    time it did.
    """
    path = REPO_ROOT / "audit" / "taxonomy-census" / "semantic-role-census.json"
    with open(path, encoding="utf-8") as handle:
        return len(json.load(handle))




def make_package(root: str, relative: str) -> str:
    path = os.path.join(root, *relative.split("/"))
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "SKILL.md"), "w", encoding="utf-8") as handle:
        handle.write("---\nname: demo\n---\n")
    return path


class TestDeriveScope(unittest.TestCase):
    def test_functional_category_scope(self):
        path = os.path.join(LIBRARY, "development", "backend", "wordpress")
        self.assertEqual(derive_scope(path, library_dir=LIBRARY), "development")

    def test_operational_root_scope(self):
        path = os.path.join(LIBRARY, "github-operations", "pr-review")
        self.assertEqual(derive_scope(path, library_dir=LIBRARY), "github-operations")

    def test_scope_map_renames_curated_root(self):
        path = os.path.join(LIBRARY, "skills-create-manage-update", "skill-writer")
        self.assertEqual(derive_scope(path, library_dir=LIBRARY), "skills-lifecycle")
        self.assertEqual(SCOPE_MAP["skills-create-manage-update"], "skills-lifecycle")

    def test_scope_map_is_overridable(self):
        path = os.path.join(LIBRARY, "skills-create-manage-update", "skill-writer")
        self.assertEqual(
            derive_scope(path, scope_map={}, library_dir=LIBRARY),
            "skills-create-manage-update",
        )

    def test_router_has_no_scope(self):
        self.assertIsNone(derive_scope(os.path.join(LIBRARY, "development"), library_dir=LIBRARY))
        self.assertIsNone(
            derive_scope(os.path.join(LIBRARY, "development", "backend"), library_dir=LIBRARY)
        )

    def test_nested_subskill_has_no_scope(self):
        path = os.path.join(
            LIBRARY, "marketing-and-seo", "technical-seo", "seo-skills-main", "skills", "brief"
        )
        self.assertIsNone(derive_scope(path, library_dir=LIBRARY))

    def test_path_outside_library_has_no_scope(self):
        self.assertIsNone(derive_scope("/tmp/elsewhere/skill", library_dir=LIBRARY))


class TestMintCanonicalId(unittest.TestCase):
    def test_functional_id(self):
        path = os.path.join(LIBRARY, "quality-and-security", "testing", "unit-testing")
        self.assertEqual(
            mint_canonical_id(path, library_dir=LIBRARY),
            "quality-and-security:unit-testing",
        )

    def test_operational_id(self):
        path = os.path.join(LIBRARY, "github-operations", "security-review")
        self.assertEqual(
            mint_canonical_id(path, library_dir=LIBRARY),
            "github-operations:security-review",
        )

    def test_slug_is_leaf_not_full_path(self):
        path = os.path.join(LIBRARY, "marketing-and-seo", "cro", "competitor-analysis")
        self.assertEqual(derive_slug(path, library_dir=LIBRARY), "competitor-analysis")

    def test_non_canonical_returns_none(self):
        self.assertIsNone(
            mint_canonical_id(os.path.join(LIBRARY, "development"), library_dir=LIBRARY)
        )


class TestCollisions(unittest.TestCase):
    def test_collision_is_reported_for_duplicate_leaf(self):
        with tempfile.TemporaryDirectory() as root:
            library = os.path.join(root, "library")
            make_package(library, "development/backend/shared-name")
            make_package(library, "development/frontend/shared-name")
            make_package(library, "development/backend/unique-name")

            collisions = find_collisions(library_dir=library)
            self.assertEqual(list(collisions), ["development:shared-name"])
            self.assertEqual(len(collisions["development:shared-name"]), 2)

    def test_no_collision_for_distinct_leaves(self):
        with tempfile.TemporaryDirectory() as root:
            library = os.path.join(root, "library")
            make_package(library, "development/backend/alpha")
            make_package(library, "development/backend/beta")
            self.assertEqual(find_collisions(library_dir=library), {})

    def test_operational_and_functional_roots_do_not_collide(self):
        with tempfile.TemporaryDirectory() as root:
            library = os.path.join(root, "library")
            make_package(library, "github-operations/shared")
            make_package(library, "development/backend/shared")
            self.assertEqual(find_collisions(library_dir=library), {})


class TestRealLibraryInvariants(unittest.TestCase):
    """Guards the published population. A change here is a deliberate event."""

    @classmethod
    def setUpClass(cls):
        cls.paths = canonical_package_paths(library_dir=LIBRARY)
        cls.ids = [mint_canonical_id(p, library_dir=LIBRARY) for p in cls.paths]

    def test_population_size(self):
        self.assertEqual(len(self.paths), census_population())

    def test_collisions_are_structural(self):
        # A collision is a duplicate pair awaiting adjudication. Which pairs exist
        # depends on the population, so assert the shape rather than the members.
        collisions = find_collisions(library_dir=LIBRARY)
        self.assertIsInstance(collisions, dict)
        for canonical_id, paths in collisions.items():
            self.assertIn(":", canonical_id, canonical_id)
            self.assertGreater(len(paths), 1, f"{canonical_id} should claim at least two paths")

    def test_matches_census_exactly(self):
        census_path = REPO_ROOT / "audit" / "taxonomy-census" / "semantic-role-census.json"
        with open(census_path, encoding="utf-8") as handle:
            census = {row["current_path"] for row in json.load(handle)}

        derived = {
            os.path.relpath(path, str(REPO_ROOT)).replace(os.sep, "/") for path in self.paths
        }
        self.assertEqual(derived, census)


if __name__ == "__main__":
    unittest.main()