"""
Comprehensive Unit and Negative Regression Test Suite for REV-128 Physical Ownership Model.

Validates the physical storage plane contracts defined in ADR-002:
  - Platform Hubs, Domain-Centric Trees, and Meta Infrastructure directory layouts
  - Physical placement contracts for Overlays and Adapters
  - Overlay nesting constraints and directory depth limits
  - Authoritative resolution and mapping of the 15 GitHub duplicate pairs
  - Path-independent canonical identity invariance across physical relocations
"""

import sys
import unittest
from pathlib import Path

# Ensure tools directory is in sys.path
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.object_model import (
    AdapterObject,
    CanonicalIdentity,
    CapabilityObject,
    FamilyObject,
    InvariantViolationError,
    OverlayObject,
    PrimitiveObject,
    SkillObject,
    SkillRole,
    WorkflowObject,
)
from skill_library.physical_layout import (
    DuplicateResolutionRegistry,
    LayoutValidationError,
    ParsedPhysicalPath,
    PhysicalPathContract,
    PhysicalPlane,
    PhysicalLayoutValidator,
)


class TestPhysicalPathContract(unittest.TestCase):
    """Unit tests for physical path normalization, parsing, and directory validation."""

    def test_parse_platform_hub_paths(self):
        """Valid platform hub paths parse into structured planes and components."""
        # Standard platform workflow
        p1 = PhysicalPathContract.parse("tools-and-platforms/github/commit")
        self.assertEqual(p1.plane, PhysicalPlane.PLATFORM_HUB)
        self.assertEqual(p1.top_level, "github")
        self.assertIsNone(p1.component_type)
        self.assertEqual(p1.leaf_name, "commit")

        # Platform primitive
        p2 = PhysicalPathContract.parse("tools-and-platforms/figma/primitives/color-tokens")
        self.assertEqual(p2.plane, PhysicalPlane.PLATFORM_HUB)
        self.assertEqual(p2.top_level, "figma")
        self.assertEqual(p2.component_type, "primitives")
        self.assertEqual(p2.leaf_name, "color-tokens")

        # Platform adapter
        p3 = PhysicalPathContract.parse("tools-and-platforms/github/adapters/gh-cli")
        self.assertEqual(p3.plane, PhysicalPlane.PLATFORM_HUB)
        self.assertEqual(p3.top_level, "github")
        self.assertEqual(p3.component_type, "adapters")
        self.assertEqual(p3.leaf_name, "gh-cli")

        # Platform overlay
        p4 = PhysicalPathContract.parse("tools-and-platforms/figma/overlays/figma-implement-motion")
        self.assertEqual(p4.plane, PhysicalPlane.PLATFORM_HUB)
        self.assertEqual(p4.top_level, "figma")
        self.assertEqual(p4.component_type, "overlays")
        self.assertEqual(p4.leaf_name, "figma-implement-motion")

    def test_parse_domain_tree_paths(self):
        """Valid canonical category and domain subcategory paths parse correctly."""
        p1 = PhysicalPathContract.parse("development/systems/commit")
        self.assertEqual(p1.plane, PhysicalPlane.DOMAIN_TREE)
        self.assertEqual(p1.top_level, "development")
        self.assertEqual(p1.sub_level, "systems")
        self.assertIsNone(p1.component_type)
        self.assertEqual(p1.leaf_name, "commit")

        # Domain-hosted overlay
        p2 = PhysicalPathContract.parse("design-and-experience/motion-and-graphics/overlays/lottie-export")
        self.assertEqual(p2.plane, PhysicalPlane.DOMAIN_TREE)
        self.assertEqual(p2.top_level, "design-and-experience")
        self.assertEqual(p2.sub_level, "motion-and-graphics")
        self.assertEqual(p2.component_type, "overlays")
        self.assertEqual(p2.leaf_name, "lottie-export")

    def test_parse_meta_infrastructure_paths(self):
        """Meta-and-agent-skills paths parse with proper plane and components."""
        p1 = PhysicalPathContract.parse("meta-and-agent-skills/skill-lifecycle/eval-skill")
        self.assertEqual(p1.plane, PhysicalPlane.META_INFRASTRUCTURE)
        self.assertEqual(p1.top_level, "meta-and-agent-skills")
        self.assertEqual(p1.sub_level, "skill-lifecycle")
        self.assertEqual(p1.leaf_name, "eval-skill")

        p2 = PhysicalPathContract.parse("meta-and-agent-skills/adapters/http-tool")
        self.assertEqual(p2.plane, PhysicalPlane.META_INFRASTRUCTURE)
        self.assertEqual(p2.component_type, "adapters")
        self.assertEqual(p2.leaf_name, "http-tool")

    def test_parse_legacy_root_paths(self):
        """Legacy roots (github-operations and skills-create-manage-update) are identified."""
        p1 = PhysicalPathContract.parse("github-operations/pr-writer")
        self.assertEqual(p1.plane, PhysicalPlane.LEGACY_ROOT)
        self.assertTrue(p1.is_legacy)
        self.assertEqual(p1.leaf_name, "pr-writer")

        p2 = PhysicalPathContract.parse("skills-create-manage-update/audit-skill")
        self.assertEqual(p2.plane, PhysicalPlane.LEGACY_ROOT)
        self.assertTrue(p2.is_legacy)
        self.assertEqual(p2.leaf_name, "audit-skill")

    def test_normalize_strips_leading_library_prefix(self):
        """Physical paths with or without leading 'library/' or slashes normalize consistently."""
        norm1 = PhysicalPathContract.normalize("library/development/backend/launch")
        norm2 = PhysicalPathContract.normalize("/library/development/backend/launch/")
        norm3 = PhysicalPathContract.normalize("development/backend/launch")
        self.assertEqual(norm1, "development/backend/launch")
        self.assertEqual(norm2, "development/backend/launch")
        self.assertEqual(norm3, "development/backend/launch")

    def test_negative_rejection_of_backslashes_and_traversal(self):
        """Backslashes and directory traversal '..' are strictly rejected."""
        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("development\\backend\\launch")

        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("development/../backend/launch")

        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("../outside/skill")

    def test_negative_rejection_of_unrecognized_categories(self):
        """Paths starting with unknown or unmapped categories fail validation."""
        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("random-category/subcat/my-skill")

    def test_negative_rejection_of_uppercase_and_special_characters(self):
        """Directory paths with uppercase or invalid symbols fail validation."""
        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("development/BackEnd/launch")

        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("development/backend/launch_skill!")

    def test_negative_rejection_of_nested_overlays(self):
        """Invariant: An overlay directory cannot be nested within another overlay."""
        nested_overlay_path = "design-and-experience/motion-and-graphics/overlays/sub-domain/overlays/bad-skill"
        with self.assertRaises(LayoutValidationError) as ctx:
            PhysicalPathContract.parse(nested_overlay_path)
        self.assertIn("Nested overlays are forbidden", str(ctx.exception))

    def test_negative_rejection_of_excessive_platform_hub_depth(self):
        """Platform hubs cannot exceed depth 4 (tools-and-platforms/<fam>/<comp>/<slug>)."""
        with self.assertRaises(LayoutValidationError):
            PhysicalPathContract.parse("tools-and-platforms/github/primitives/nested/too-deep")


class TestPhysicalLayoutValidator(unittest.TestCase):
    """Unit tests validating SkillObject roles against physical placement contracts."""

    def test_overlay_placement_enforcement(self):
        """Overlays MUST reside in an 'overlays/' directory."""
        # Valid platform-hosted overlay
        valid_overlay = OverlayObject(
            canonical_id="figma:implement-motion",
            name="Figma Motion Implementation",
            target_id="motion:implement-motion",
            platform="figma",
            families=["figma"],
            physical_path="tools-and-platforms/figma/overlays/figma-implement-motion",
        )
        # Should pass without exception
        PhysicalLayoutValidator.validate_object_placement(valid_overlay)

        # Invalid overlay: placed in regular development directory
        invalid_overlay = OverlayObject(
            canonical_id="webflow:component-overlay",
            name="Webflow Component Overlay",
            target_id="dev:component-scaffold",
            platform="webflow",
            families=["webflow"],
            physical_path="development/frontend/webflow-component-overlay",
        )
        with self.assertRaises(LayoutValidationError) as ctx:
            PhysicalLayoutValidator.validate_object_placement(invalid_overlay)
        self.assertIn("must reside in an 'overlays/' directory", str(ctx.exception))

    def test_adapter_placement_enforcement(self):
        """Adapters MUST reside in an 'adapters/' directory."""
        valid_adapter = AdapterObject(
            canonical_id="mcp:not-human-search",
            name="Not Human Search MCP Adapter",
            protocol="mcp",
            physical_path="meta-and-agent-skills/adapters/not-human-search-mcp",
        )
        PhysicalLayoutValidator.validate_object_placement(valid_adapter)

        invalid_adapter = AdapterObject(
            canonical_id="mcp:invalid-placement",
            name="Misplaced Adapter",
            protocol="mcp",
            physical_path="development/backend/not-human-search-mcp",
        )
        with self.assertRaises(LayoutValidationError) as ctx:
            PhysicalLayoutValidator.validate_object_placement(invalid_adapter)
        self.assertIn("must reside in an 'adapters/' directory", str(ctx.exception))

    def test_platform_hub_affinity_enforcement(self):
        """Objects in platform hubs must declare family affinity via scope, families, or metadata."""
        # Valid: matching scope
        obj1 = CapabilityObject(
            canonical_id="github:actions-advanced",
            name="Advanced GitHub Actions",
            physical_path="tools-and-platforms/github/actions-advanced",
        )
        PhysicalLayoutValidator.validate_object_placement(obj1)

        # Valid: declared in families list
        obj2 = CapabilityObject(
            canonical_id="ci:actions-runner",
            name="Actions Runner",
            families=["github"],
            physical_path="tools-and-platforms/github/actions-runner",
        )
        PhysicalLayoutValidator.validate_object_placement(obj2)

        # Invalid: placed in github hub without any github affiliation
        unaffiliated_obj = CapabilityObject(
            canonical_id="marketing:seo-audit",
            name="Unrelated SEO Audit",
            families=["marketing"],
            physical_path="tools-and-platforms/github/seo-audit",
        )
        with self.assertRaises(LayoutValidationError) as ctx:
            PhysicalLayoutValidator.validate_object_placement(unaffiliated_obj)
        self.assertIn("does not declare affiliation with family 'github'", str(ctx.exception))

    def test_path_independent_relocation_invariance(self):
        """Physical relocation updates physical_path while strictly preserving canonical_id and URN."""
        obj = WorkflowObject(
            canonical_id="development:create-pr",
            name="Create Pull Request Workflow",
            domain="development",
            physical_path="development/fullstack/create-pr",
        )
        original_id = obj.canonical_id
        original_urn = obj.id_object.urn

        # Move to platform hub
        new_path = "tools-and-platforms/github/create-pr"
        obj.families.append("github")
        PhysicalLayoutValidator.verify_path_independent_relocation(obj, new_path)

        self.assertEqual(obj.physical_path, new_path)
        self.assertEqual(obj.canonical_id, original_id)
        self.assertEqual(obj.id_object.urn, original_urn)


class TestDuplicateResolutionRegistry(unittest.TestCase):
    """Unit tests verifying the 15 GitHub duplicate pairs resolution architecture."""

    def test_all_15_duplicate_pairs_registered(self):
        """Registry must contain exactly the 15 verified duplicate pairs from REV-126/150."""
        pairs = DuplicateResolutionRegistry.get_all_pairs()
        self.assertEqual(len(pairs), 15)

        expected_leaves = {
            "actions-debugger",
            "advanced-workflows",
            "commit",
            "create-branch",
            "create-issue-gate",
            "feature-tracking",
            "github",
            "hooks-automation",
            "issue-creator",
            "pr-merge-champion",
            "pr-review",
            "pr-writer",
            "presence",
            "review-requests",
            "security-review",
        }
        registered_leaves = {p.leaf_name for p in pairs}
        self.assertEqual(registered_leaves, expected_leaves)

    def test_dual_retention_pairs(self):
        """Dual retention pairs (commit, create-branch, security-review) have distinct scopes."""
        for leaf in ("commit", "create-branch", "security-review"):
            res = DuplicateResolutionRegistry.get_resolution(leaf)
            self.assertIsNotNone(res)
            self.assertEqual(res.resolution_type, "dual_retention")
            self.assertTrue(res.canonical_id.startswith("github:"))

    def test_alias_to_platform_pairs(self):
        """Operational workflows migrating to platform hubs are registered with valid canonical IDs."""
        for leaf in ("actions-debugger", "create-issue-gate", "pr-writer", "pr-review"):
            res = DuplicateResolutionRegistry.get_resolution(leaf)
            self.assertIsNotNone(res)
            self.assertEqual(res.resolution_type, "alias_to_platform")
            self.assertEqual(res.canonical_id, f"github:{leaf}")
            self.assertEqual(res.target_physical_home, f"tools-and-platforms/github/{leaf}")

    def test_rename_resolution_for_root_github_leaf(self):
        """The 'github' leaf is renamed to 'general-operations' to prevent root package collisions."""
        res = DuplicateResolutionRegistry.get_resolution("github")
        self.assertIsNotNone(res)
        self.assertEqual(res.resolution_type, "rename")
        self.assertEqual(res.canonical_id, "github:general-operations")
        self.assertEqual(res.target_physical_home, "tools-and-platforms/github/general-operations")


if __name__ == "__main__":
    unittest.main()
