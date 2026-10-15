"""
Comprehensive Unit and Negative Regression Test Suite for REV-127 Semantic Object Model.

Validates the first-class object types, path-independent canonical identities,
directed relationship graphs, and architectural invariant validation.
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
    AliasObject,
    CanonicalIdentity,
    CanonicalIdentityError,
    CapabilityObject,
    FamilyObject,
    GeneratedArtifactObject,
    InvariantViolationError,
    ObjectGraph,
    OverlayObject,
    PrimitiveObject,
    ReferenceObject,
    RelationshipType,
    ReviewStatus,
    RouterObject,
    SkillObject,
    SkillRole,
    WorkflowObject,
)


class TestCanonicalIdentity(unittest.TestCase):
    """Path-independent canonical identity specification tests."""

    def test_valid_compact_identity_parsing(self):
        """Compact '<scope>:<slug>' parses correctly."""
        cid = CanonicalIdentity.parse("github:create-pull-request")
        self.assertEqual(cid.scope, "github")
        self.assertEqual(cid.slug, "create-pull-request")
        self.assertEqual(cid.compact, "github:create-pull-request")
        self.assertEqual(cid.urn, "urn:skill:github:create-pull-request")

    def test_valid_urn_parsing(self):
        """Formal URN 'urn:skill:<scope>:<slug>' parses correctly."""
        cid = CanonicalIdentity.parse("urn:skill:architecture:code-refactoring-tech-debt")
        self.assertEqual(cid.scope, "architecture")
        self.assertEqual(cid.slug, "code-refactoring-tech-debt")
        self.assertEqual(cid.compact, "architecture:code-refactoring-tech-debt")
        self.assertEqual(cid.urn, "urn:skill:architecture:code-refactoring-tech-debt")

    def test_negative_rejection_of_path_separators(self):
        """Negative test: canonical ID with slashes must be rejected (path independence)."""
        with self.assertRaises(CanonicalIdentityError) as ctx:
            CanonicalIdentity.parse("library/development/backend:launch")
        self.assertIn("path separators", str(ctx.exception))

        with self.assertRaises(CanonicalIdentityError) as ctx:
            CanonicalIdentity.parse("development:backend/launch")
        self.assertIn("path separators", str(ctx.exception))

        with self.assertRaises(CanonicalIdentityError) as ctx:
            CanonicalIdentity.parse("dev\\backend:launch")
        self.assertIn("path separators", str(ctx.exception))

    def test_negative_rejection_of_file_extensions(self):
        """Negative test: canonical ID with file extensions must be rejected."""
        with self.assertRaises(CanonicalIdentityError) as ctx:
            CanonicalIdentity.parse("seo:audit.md")
        self.assertIn("file extensions", str(ctx.exception))

        with self.assertRaises(CanonicalIdentityError) as ctx:
            CanonicalIdentity.parse("seo:audit.json")
        self.assertIn("file extensions", str(ctx.exception))

    def test_negative_rejection_of_invalid_characters(self):
        """Negative test: uppercase, spaces, or illegal punctuation must be rejected."""
        invalid_ids = [
            "GitHub:create-pr",
            "github:Create-PR",
            "github:create_pr",  # underscores forbidden in kebab-case slugs
            "github:create pr",
            "create-pr",         # missing scope colon
            "github:",           # missing slug
            ":create-pr",        # missing scope
            "a:b:c",             # multiple colons
            "",                  # empty string
        ]
        for inv in invalid_ids:
            with self.subTest(identifier=inv):
                with self.assertRaises(CanonicalIdentityError):
                    CanonicalIdentity.parse(inv)


class TestFirstClassObjectTypes(unittest.TestCase):
    """Validation of all 10 first-class semantic object types."""

    def test_all_ten_first_class_roles_exist_and_normalize(self):
        """Verify role enum includes exactly 10 roles and census aliases normalize correctly."""
        expected_roles = {
            "capability",
            "workflow",
            "family",
            "primitive",
            "overlay",
            "adapter",
            "alias",
            "reference",
            "router",
            "generated_artifact",
        }
        actual_roles = {role.value for role in SkillRole}
        self.assertEqual(actual_roles, expected_roles)
        self.assertEqual(len(SkillRole), 10)

        # Census string normalization
        self.assertEqual(SkillRole.normalize_role("independent_capability"), SkillRole.CAPABILITY)
        self.assertEqual(SkillRole.normalize_role("family_primitive"), SkillRole.PRIMITIVE)
        self.assertEqual(SkillRole.normalize_role("reference_or_support_candidate"), SkillRole.REFERENCE)
        self.assertEqual(SkillRole.normalize_role("alias_candidate"), SkillRole.ALIAS)

    def test_manual_review_is_review_status_not_object_type(self):
        """Verify manual_review is an analytical lifecycle ReviewStatus, not a SkillRole."""
        self.assertNotIn("manual_review", [r.value for r in SkillRole])
        self.assertEqual(ReviewStatus.MANUAL_REVIEW.value, "manual_review")
        self.assertEqual(ReviewStatus.ACTIVE.value, "active")

        # An ambiguous skill object has a concrete object role (e.g. capability) with status=manual_review
        disputed_cap = CapabilityObject(
            canonical_id="dev:unsettled-boundary-tool",
            name="unsettled-boundary-tool",
            description="Tool under boundary review.",
            domain="development",
            status=ReviewStatus.MANUAL_REVIEW,
        )
        self.assertEqual(disputed_cap.role, SkillRole.CAPABILITY)
        self.assertEqual(disputed_cap.status, ReviewStatus.MANUAL_REVIEW)
        self.assertEqual(disputed_cap.to_dict()["status"], "manual_review")

    def test_capability_instantiation(self):
        """Capability attributes and serialization."""
        cap = CapabilityObject(
            canonical_id="seo:audit",
            name="seo-audit",
            description="Comprehensive SEO audit engine. Use when evaluating on-page technical health.",
            domain="marketing-and-seo",
            physical_path="library/marketing-and-seo/on-page-seo/seo-audit",
            execution_provider="python",
        )
        self.assertEqual(cap.role, SkillRole.CAPABILITY)
        self.assertEqual(cap.execution_provider, "python")
        d = cap.to_dict()
        self.assertEqual(d["canonical_id"], "seo:audit")
        self.assertEqual(d["role"], "capability")
        self.assertEqual(d["urn"], "urn:skill:seo:audit")

    def test_workflow_instantiation_and_composition_sync(self):
        """Workflow automatically synchronizes composed_of relationships from steps."""
        wf = WorkflowObject(
            canonical_id="workflow:launch",
            name="launch",
            description="Multi-phase launch pipeline. Use when deploying production release.",
            domain="development",
            steps=["infra:pre-flight-check", "deploy:execute", "monitor:smoke-test"],
            approval_gates=["deploy:execute"],
        )
        self.assertEqual(wf.role, SkillRole.WORKFLOW)
        self.assertEqual(len(wf.steps), 3)
        self.assertEqual(len(wf.relationships), 3)
        self.assertEqual(wf.relationships[0].rel_type, RelationshipType.COMPOSED_OF)
        self.assertEqual(wf.relationships[0].target_id, "infra:pre-flight-check")
        self.assertEqual(wf.relationships[0].metadata["order"], 1)

    def test_family_instantiation(self):
        """Family logical container attributes."""
        fam = FamilyObject(
            canonical_id="platform:github",
            name="github",
            description="GitHub platform integrations and VCS operations.",
            domain="workflow-and-automation",
            vendor="GitHub",
        )
        self.assertEqual(fam.role, SkillRole.FAMILY)
        self.assertEqual(fam.vendor, "GitHub")
        self.assertEqual(fam.family_id, "github")

    def test_primitive_instantiation(self):
        """Primitive reusable building block attributes."""
        prim = PrimitiveObject(
            canonical_id="design:design-token",
            name="design-token",
            description="Base design tokens for spacing, typography, and color palettes.",
            domain="design-and-experience",
            primitive_type="token",
        )
        self.assertEqual(prim.role, SkillRole.PRIMITIVE)
        self.assertEqual(prim.primitive_type, "token")

    def test_overlay_instantiation(self):
        """Overlay platform specialization automatically synchronizes extends relationship."""
        ov = OverlayObject(
            canonical_id="figma:implement-motion",
            name="figma-implement-motion",
            description="Figma motion prototype implementation overlay.",
            domain="design-and-experience",
            target_id="motion:implement-animation",
            platform="figma",
        )
        self.assertEqual(ov.role, SkillRole.OVERLAY)
        self.assertEqual(ov.platform, "figma")
        self.assertEqual(len(ov.relationships), 1)
        self.assertEqual(ov.relationships[0].rel_type, RelationshipType.EXTENDS)
        self.assertEqual(ov.relationships[0].target_id, "motion:implement-animation")

    def test_adapter_instantiation(self):
        """Adapter protocol translation shim attributes."""
        adp = AdapterObject(
            canonical_id="mcp:not-human-search",
            name="not-human-search-mcp",
            description="Pure MCP protocol adapter bridging external search API.",
            domain="development",
            protocol="mcp",
        )
        self.assertEqual(adp.role, SkillRole.ADAPTER)
        self.assertEqual(adp.protocol, "mcp")

    def test_alias_instantiation(self):
        """Alias redirect pointer automatically registers aliased_to relationship."""
        alias = AliasObject(
            canonical_id="alias:create-pr",
            name="create-pr",
            description="Legacy alias pointing to canonical GitHub PR creator.",
            domain="development",
            target_id="github:create-pull-request",
        )
        self.assertEqual(alias.role, SkillRole.ALIAS)
        self.assertEqual(alias.target_id, "github:create-pull-request")
        self.assertEqual(len(alias.relationships), 1)
        self.assertEqual(alias.relationships[0].rel_type, RelationshipType.ALIASED_TO)

    def test_reference_instantiation(self):
        """Reference non-executable documentation attributes."""
        ref = ReferenceObject(
            canonical_id="docs:react-cheatsheet",
            name="react-cheatsheet",
            description="Quick reference cheat sheet for React hooks and lifecycle.",
            domain="development",
            reference_format="cheatsheet",
        )
        self.assertEqual(ref.role, SkillRole.REFERENCE)
        self.assertEqual(ref.reference_format, "cheatsheet")

    def test_router_instantiation(self):
        """Router navigational node attributes."""
        router = RouterObject(
            canonical_id="router:development",
            name="development-router",
            description="Navigational router for development engineering skills.",
            domain="development",
            route_level="category",
            managed_skills=["dev:backend-api", "dev:frontend-ui"],
        )
        self.assertEqual(router.role, SkillRole.ROUTER)
        self.assertEqual(router.route_level, "category")

    def test_generated_artifact_instantiation(self):
        """Generated runtime artifact attributes."""
        art = GeneratedArtifactObject(
            canonical_id="runtime:manifest",
            name="runtime-manifest",
            description="Authoritative compiled runtime discovery manifest.",
            domain="meta-and-agent-skills",
            artifact_type="manifest",
            source_commit="b4eabf9e",
        )
        self.assertEqual(art.role, SkillRole.GENERATED_ARTIFACT)
        self.assertEqual(art.artifact_type, "manifest")


class TestObjectGraphInvariants(unittest.TestCase):
    """Validation of graph invariants, cycle detection, and integrity rules."""

    def test_single_canonical_owner_invariant(self):
        """Invariant 2: duplicate canonical_id registration must raise InvariantViolationError."""
        graph = ObjectGraph()
        cap1 = CapabilityObject(
            canonical_id="dev:unit-test",
            name="unit-test",
            description="Unit testing capability.",
            domain="development",
        )
        cap2 = CapabilityObject(
            canonical_id="dev:unit-test",
            name="unit-test",
            description="Duplicate testing capability.",
            domain="development",
        )
        graph.add_object(cap1)
        with self.assertRaises(InvariantViolationError) as ctx:
            graph.add_object(cap2)
        self.assertIn("Single Canonical Owner", str(ctx.exception))

    def test_dag_acyclicity_valid_graph_passes(self):
        """Invariant 1: Acyclic dependency and composition graph passes validation."""
        graph = ObjectGraph()
        prim = PrimitiveObject(
            canonical_id="auth:tokens",
            name="tokens",
            description="Auth token primitives.",
            domain="development",
        )
        cap1 = CapabilityObject(
            canonical_id="auth:login",
            name="login",
            description="Login capability.",
            domain="development",
        )
        cap1.add_relationship(RelationshipType.DEPENDS_ON, "auth:tokens")

        wf = WorkflowObject(
            canonical_id="auth:user-onboarding",
            name="user-onboarding",
            description="User onboarding multi-phase workflow.",
            domain="development",
            steps=["auth:login"],
        )

        graph.add_object(prim)
        graph.add_object(cap1)
        graph.add_object(wf)
        self.assertEqual(graph.validate_invariants(), [])

    def test_negative_direct_cycle_triggers_violation(self):
        """Negative test Invariant 1: Direct circular dependency (A -> B -> A) triggers violation."""
        graph = ObjectGraph()
        cap1 = CapabilityObject(
            canonical_id="pkg:service-a",
            name="service-a",
            description="Service A.",
            domain="development",
        )
        cap2 = CapabilityObject(
            canonical_id="pkg:service-b",
            name="service-b",
            description="Service B.",
            domain="development",
        )
        cap1.add_relationship(RelationshipType.DEPENDS_ON, "pkg:service-b")
        cap2.add_relationship(RelationshipType.DEPENDS_ON, "pkg:service-a")

        graph.add_object(cap1)
        graph.add_object(cap2)

        with self.assertRaises(InvariantViolationError) as ctx:
            graph.validate_invariants()
        self.assertIn("Circular relationship detected", str(ctx.exception))

    def test_negative_multi_node_workflow_cycle_triggers_violation(self):
        """Negative test Invariant 1: Multi-node workflow composition cycle triggers violation."""
        graph = ObjectGraph()
        wf1 = WorkflowObject(
            canonical_id="flow:phase-1",
            name="phase-1",
            description="Phase 1 workflow.",
            domain="development",
            steps=["flow:phase-2"],
        )
        wf2 = WorkflowObject(
            canonical_id="flow:phase-2",
            name="phase-2",
            description="Phase 2 workflow.",
            domain="development",
            steps=["flow:phase-3"],
        )
        wf3 = WorkflowObject(
            canonical_id="flow:phase-3",
            name="phase-3",
            description="Phase 3 workflow.",
            domain="development",
            steps=["flow:phase-1"],  # Loop back to phase 1
        )
        graph.add_object(wf1)
        graph.add_object(wf2)
        graph.add_object(wf3)

        with self.assertRaises(InvariantViolationError) as ctx:
            graph.validate_invariants()
        self.assertIn("Circular relationship detected", str(ctx.exception))

    def test_single_hop_alias_resolution(self):
        """Invariant 3: Single-hop alias resolves directly to target canonical object."""
        graph = ObjectGraph()
        cap = CapabilityObject(
            canonical_id="github:create-pull-request",
            name="create-pull-request",
            description="Create PR on GitHub.",
            domain="workflow-and-automation",
        )
        alias = AliasObject(
            canonical_id="alias:create-pr",
            name="create-pr",
            description="Legacy shortcut.",
            domain="development",
            target_id="github:create-pull-request",
        )
        graph.add_object(cap)
        graph.add_object(alias)

        resolved_obj, hops = graph.resolve_alias("alias:create-pr")
        self.assertEqual(resolved_obj.canonical_id, "github:create-pull-request")
        self.assertEqual(hops, ["alias:create-pr", "github:create-pull-request"])
        self.assertEqual(graph.validate_invariants(), [])

    def test_negative_chained_alias_triggers_violation(self):
        """Negative test Invariant 3: Chained alias (Alias 1 -> Alias 2 -> Target) triggers violation."""
        graph = ObjectGraph()
        cap = CapabilityObject(
            canonical_id="target:endpoint",
            name="endpoint",
            description="Target endpoint.",
            domain="development",
        )
        alias2 = AliasObject(
            canonical_id="alias:second-hop",
            name="second-hop",
            description="Second hop alias.",
            domain="development",
            target_id="target:endpoint",
        )
        alias1 = AliasObject(
            canonical_id="alias:first-hop",
            name="first-hop",
            description="First hop alias.",
            domain="development",
            target_id="alias:second-hop",
        )
        graph.add_object(cap)
        graph.add_object(alias2)
        graph.add_object(alias1)

        with self.assertRaises(InvariantViolationError) as ctx:
            graph.validate_invariants()
        self.assertIn("Invariant 3 Violation", str(ctx.exception))
        self.assertIn("chains to another alias", str(ctx.exception))

    def test_negative_overlay_extending_overlay_triggers_violation(self):
        """Negative test Invariant 4: Overlay extending another overlay triggers violation."""
        graph = ObjectGraph()
        cap = CapabilityObject(
            canonical_id="motion:animate",
            name="animate",
            description="Generic animation capability.",
            domain="design-and-experience",
        )
        ov1 = OverlayObject(
            canonical_id="figma:animate",
            name="figma-animate",
            description="Figma animation overlay.",
            domain="design-and-experience",
            target_id="motion:animate",
            platform="figma",
        )
        ov2 = OverlayObject(
            canonical_id="figma:deep-motion",
            name="figma-deep-motion",
            description="Overlay on overlay.",
            domain="design-and-experience",
            target_id="figma:animate",  # Extending an overlay!
            platform="figma",
        )
        graph.add_object(cap)
        graph.add_object(ov1)
        graph.add_object(ov2)

        with self.assertRaises(InvariantViolationError) as ctx:
            graph.validate_invariants()
        self.assertIn("Invariant 4 Violation", str(ctx.exception))
        self.assertIn("Overlays cannot extend overlays", str(ctx.exception))

    def test_negative_primitive_composing_workflow_triggers_violation(self):
        """Negative test Invariant 5: Primitive declaring composed_of triggers violation."""
        graph = ObjectGraph()
        cap = CapabilityObject(
            canonical_id="task:step",
            name="step",
            description="Step.",
            domain="development",
        )
        prim = PrimitiveObject(
            canonical_id="prim:token",
            name="token",
            description="Token primitive.",
            domain="development",
        )
        prim.add_relationship(RelationshipType.COMPOSED_OF, "task:step")

        graph.add_object(cap)
        graph.add_object(prim)

        with self.assertRaises(InvariantViolationError) as ctx:
            graph.validate_invariants()
        self.assertIn("Invariant 5 Violation", str(ctx.exception))
        self.assertIn("Primitives cannot compose workflows", str(ctx.exception))

    def test_path_independence_preserves_canonical_id_across_relocation(self):
        """Invariant 6: Physical disk relocation mutates physical_path without altering canonical identity."""
        cap = CapabilityObject(
            canonical_id="arch:refactor",
            name="refactor",
            description="Refactoring capability.",
            domain="development",
            physical_path="library/development/software-architecture/refactor",
        )
        self.assertEqual(cap.physical_path, "library/development/software-architecture/refactor")
        self.assertEqual(cap.canonical_id, "arch:refactor")

        # Simulate physical relocation in storage plane
        cap.physical_path = "library/tools-and-platforms/refactor"
        self.assertEqual(cap.physical_path, "library/tools-and-platforms/refactor")
        # Canonical identity remains unchanged
        self.assertEqual(cap.canonical_id, "arch:refactor")
        self.assertEqual(cap.id_object.urn, "urn:skill:arch:refactor")


class TestCatalogBoundaryCaseStudies(unittest.TestCase):
    """Validates the canonical modeling of controversial census sample skills."""

    def test_launch_is_workflow(self):
        """Launch is a multi-phase cross-domain workflow."""
        launch = WorkflowObject(
            canonical_id="backend:launch",
            name="launch",
            description="Multi-phase release orchestrator. Use when performing production deployment.",
            domain="development",
            steps=["infra:pre-flight", "git:tag-release", "deploy:ship"],
        )
        self.assertEqual(launch.role, SkillRole.WORKFLOW)
        self.assertEqual(len(launch.steps), 3)

    def test_agent_memory_mcp_is_capability_with_provider(self):
        """Agent-memory-mcp is a domain capability using an MCP execution provider."""
        mem = CapabilityObject(
            canonical_id="architecture:agent-memory-mcp",
            name="agent-memory-mcp",
            description="Persistent agent memory architecture. Use when storing conversational state.",
            domain="development",
            execution_provider="mcp",
        )
        self.assertEqual(mem.role, SkillRole.CAPABILITY)
        self.assertEqual(mem.execution_provider, "mcp")

    def test_not_human_search_mcp_is_adapter(self):
        """Not-human-search-mcp is a pure protocol adapter."""
        adp = AdapterObject(
            canonical_id="adapter:not-human-search-mcp",
            name="not-human-search-mcp",
            description="Protocol bridge for autonomous search provider.",
            domain="development",
            protocol="mcp",
        )
        self.assertEqual(adp.role, SkillRole.ADAPTER)
        self.assertEqual(adp.protocol, "mcp")

    def test_figma_implement_motion_is_overlay(self):
        """Figma-implement-motion is an overlay extending base motion capability."""
        ov = OverlayObject(
            canonical_id="figma:implement-motion",
            name="figma-implement-motion",
            description="Figma motion prototype implementation.",
            domain="design-and-experience",
            target_id="motion:implement-motion",
            platform="figma",
        )
        self.assertEqual(ov.role, SkillRole.OVERLAY)
        self.assertEqual(ov.relationships[0].rel_type, RelationshipType.EXTENDS)
        self.assertEqual(ov.relationships[0].target_id, "motion:implement-motion")

    def test_duplicate_name_scope_separation_prevents_collision(self):
        """
        Verify that duplicate leaf names across domains (e.g. create-pr) survive
        without collision due to scoped path-independent identity.
        """
        graph = ObjectGraph()
        gh_pr = CapabilityObject(
            canonical_id="github:create-pr",
            name="create-pr",
            description="GitHub CLI create PR capability.",
            domain="workflow-and-automation",
        )
        dev_pr = CapabilityObject(
            canonical_id="development:create-pr",
            name="create-pr",
            description="Legacy development PR capability.",
            domain="development",
        )
        graph.add_object(gh_pr)
        graph.add_object(dev_pr)
        self.assertEqual(len(graph.objects), 2)
        self.assertIsNotNone(graph.get_object("github:create-pr"))
        self.assertIsNotNone(graph.get_object("development:create-pr"))
        self.assertEqual(graph.validate_invariants(), [])

    def test_rfc8141_urn_syntax_structure(self):
        """Verify URN syntax follows RFC 8141 structure urn:<NID>:<NSS>."""
        cid = CanonicalIdentity.parse("urn:skill:software-architecture:tech-debt")
        self.assertEqual(cid.urn, "urn:skill:software-architecture:tech-debt")
        self.assertEqual(cid.compact, "software-architecture:tech-debt")
        # Ensure NID is 'skill' and NSS is 'software-architecture:tech-debt'
        urn_parts = cid.urn.split(":", 2)
        self.assertEqual(urn_parts[0], "urn")
        self.assertEqual(urn_parts[1], "skill")
    def test_semantic_reownership_preserves_canonical_identity(self):
        """
        Verify that semantic reownership (moving from general domain to platform family)
        preserves the permanent identity namespace (canonical_id) while updating
        current domain, owner, family memberships, and physical path.
        """
        # Initially minted in development namespace
        skill = CapabilityObject(
            canonical_id="development:create-pr",
            name="create-pr",
            description="Automated pull request creation tool.",
            domain="development",
            owner="apps-team",
            families=["development"],
            physical_path="library/development/fullstack/create-pr",
        )
        self.assertEqual(skill.canonical_id, "development:create-pr")
        self.assertEqual(skill.id_object.scope, "development")
        self.assertEqual(skill.domain, "development")

        # Semantic reownership: asset moves to universal platform family
        skill.domain = "platform"
        skill.owner = "core-infra"
        skill.families = ["github", "developer-tools"]
        skill.physical_path = "library/tools-and-platforms/github/create-pr"

        # Canonical identity remains permanently untouched
        self.assertEqual(skill.canonical_id, "development:create-pr")
        self.assertEqual(skill.id_object.scope, "development")
        self.assertEqual(skill.id_object.compact, "development:create-pr")
        self.assertEqual(skill.id_object.urn, "urn:skill:development:create-pr")

        # Mutable metadata reflects current state
        self.assertEqual(skill.domain, "platform")
        self.assertEqual(skill.owner, "core-infra")
        self.assertEqual(skill.families, ["github", "developer-tools"])
        self.assertEqual(skill.physical_path, "library/tools-and-platforms/github/create-pr")

        # Verify serialization contains all four decoupled axes
        d = skill.to_dict()
        self.assertEqual(d["canonical_id"], "development:create-pr")
        self.assertEqual(d["urn"], "urn:skill:development:create-pr")
        self.assertEqual(d["domain"], "platform")
        self.assertEqual(d["owner"], "core-infra")
        self.assertEqual(d["families"], ["github", "developer-tools"])
        self.assertEqual(d["physical_path"], "library/tools-and-platforms/github/create-pr")

    def test_immutable_scope_decoupled_from_mutable_metadata(self):
        """
        Verify that scope is strictly an immutable provenance namespace,
        independent of arbitrary mutations to domain or family memberships.
        """
        skill = CapabilityObject(
            canonical_id="seo:audit-core-web-vitals",
            name="audit-core-web-vitals",
            description="Core Web Vitals diagnostic audit.",
            domain="marketing-and-seo",
        )
        self.assertEqual(skill.id_object.scope, "seo")

        # Reassign to quality domain and web-performance family
        skill.domain = "quality-and-security"
        skill.families.append("web-performance")
        skill.physical_path = "library/quality-and-security/performance/audit-core-web-vitals"

        self.assertEqual(skill.canonical_id, "seo:audit-core-web-vitals")
        self.assertEqual(skill.id_object.scope, "seo")
        self.assertEqual(skill.domain, "quality-and-security")
        self.assertIn("web-performance", skill.families)


if __name__ == "__main__":
    unittest.main()
