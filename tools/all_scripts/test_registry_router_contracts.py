"""
Unit and Negative Regression Test Suite for REV-130 / ADR-004:
Universal Catalog Registry, Multi-View Discovery, Alias Resolution,
Transitive Dependency Closure, and Project Materialization Contracts.

Verifies:
  - INV-1: Strict DAG Acyclicity across dependencies, composition, extensions, adapters
  - INV-2: Single Canonical Owner (unique canonical IDs)
  - INV-3: Single-Hop Alias Resolution (no chaining, no loops)
  - INV-4: Shallow Overlay Specialization (no overlay chains, targets cap/wf)
  - INV-5: Leaf Primitive Purity (primitives cannot compose workflows)
  - INV-6: Path Independence (no filesystem path separators or extensions in IDs)
  - INV-8: Dead Reference Prevention (every target ID exists)
  - INV-9: Transitive Completeness in Project Materialization
  - INV-10: Deterministic Compilation & Idempotency
"""

import json
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
    AliasObject,
    CanonicalIdentity,
    CanonicalIdentityError,
    CapabilityObject,
    FamilyObject,
    InvariantViolationError,
    OverlayObject,
    PrimitiveObject,
    RelationshipType,
    ReviewStatus,
    SkillRole,
    WorkflowObject,
)
from skill_library.registry_contract import (
    AliasResolver,
    CatalogCompiler,
    CatalogRegistry,
    DependencyResolver,
    DuplicateAdjudicationOutcome,
    FamilyRouterGenerator,
    MultiViewProjector,
    ProjectMaterializer,
    ProjectionMode,
    RegistryEntry,
    RegistryError,
    SemanticGroupObject,
)


class TestRegistryEntryAndIdentity(unittest.TestCase):
    """Verifies RegistryEntry schema compliance and INV-6 (Path Independence)."""

    def test_valid_entry_creation_and_dict_serialization(self):
        entry = RegistryEntry(
            canonical_id="github:create-pull-request",
            urn="urn:skill:github:create-pull-request",
            name="create-pull-request",
            role="capability",
            description="Creates a GitHub pull request.",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="github",
            owner="core-tooling",
            families=["github"],
            semantic_groups=["git-automation"],
            physical_path="library/tools-and-platforms/github/create-pull-request",
            version="1.2.0",
            status="active",
            confidence="high",
            tags=["git", "github", "pr"],
            keywords=["pull request", "gh pr create"],
            relationships={
                "composed_of": [],
                "extends": None,
                "depends_on": ["github:auth-profile"],
                "adapts": None,
                "aliased_to": None,
                "belongs_to_family": "github",
            },
            execution_providers=[{
                "provider_id": "github-cli",
                "provider_type": "cli",
                "transport": "bash",
                "command": "gh pr create",
                "is_default": True,
            }],
        )

        d = entry.to_dict()
        self.assertEqual(d["canonical_id"], "github:create-pull-request")
        self.assertEqual(d["urn"], "urn:skill:github:create-pull-request")
        self.assertEqual(d["role"], "capability")
        self.assertEqual(d["families"], ["github"])
        self.assertEqual(d["semantic_groups"], ["git-automation"])
        self.assertEqual(d["relationships"]["depends_on"], ["github:auth-profile"])

        # Roundtrip from_dict
        restored = RegistryEntry.from_dict(d)
        self.assertEqual(restored.canonical_id, entry.canonical_id)
        self.assertEqual(restored.role, entry.role)
        self.assertEqual(restored.execution_providers[0]["provider_id"], "github-cli")

    def test_inv_6_path_independence_rejection_of_path_syntax(self):
        """INV-6: Canonical identifiers containing '/', '\\', or extensions must be rejected."""
        with self.assertRaises(CanonicalIdentityError):
            RegistryEntry(
                canonical_id="tools-and-platforms/github:create-pr",
                urn="",
                name="create-pr",
                role="capability",
            )

        with self.assertRaises(CanonicalIdentityError):
            RegistryEntry(
                canonical_id="github:create-pr.md",
                urn="",
                name="create-pr",
                role="capability",
            )

        with self.assertRaises(CanonicalIdentityError):
            RegistryEntry(
                canonical_id="github:subfolder/create-pr",
                urn="",
                name="create-pr",
                role="capability",
            )

    def test_from_skill_object_factory(self):
        cap = CapabilityObject(
            canonical_id="webflow:deploy-site",
            name="deploy-site",
            description="Deploys Webflow site to production.",
            domain="tools-and-platforms",
            owner="frontend-team",
            families=["webflow"],
            physical_path="library/tools-and-platforms/webflow/deploy-site",
            execution_provider="cli",
        )
        cap.add_relationship(RelationshipType.DEPENDS_ON, "webflow:api-credentials")
        cap.add_relationship(RelationshipType.BELONGS_TO_FAMILY, "family:webflow")

        entry = RegistryEntry.from_skill_object(
            obj=cap,
            category="tools-and-platforms",
            subcategory="webflow",
            semantic_groups=["cms-publishing"],
        )
        self.assertEqual(entry.canonical_id, "webflow:deploy-site")
        self.assertEqual(entry.role, "capability")
        self.assertEqual(entry.relationships["depends_on"], ["webflow:api-credentials"])
        self.assertEqual(entry.relationships["belongs_to_family"], "family:webflow")
        self.assertEqual(entry.semantic_groups, ["cms-publishing"])
        self.assertEqual(entry.execution_providers[0]["provider_type"], "cli")


class TestCatalogRegistry(unittest.TestCase):
    """Verifies CatalogRegistry management and INV-2 (Single Canonical Owner)."""

    def setUp(self):
        self.registry = CatalogRegistry(commit_sha="test-commit-sha-123")
        self.entry_a = RegistryEntry(
            canonical_id="seo:audit-content",
            urn="",
            name="audit-content",
            role="capability",
            description="Audit content SEO.",
        )
        self.entry_b = RegistryEntry(
            canonical_id="seo:keyword-research",
            urn="",
            name="keyword-research",
            role="capability",
            description="Research keywords.",
        )

    def test_registration_and_retrieval(self):
        self.registry.add_entry(self.entry_a)
        self.registry.add_entry(self.entry_b)

        self.assertEqual(len(self.registry.skills), 2)
        retrieved = self.registry.get_entry("seo:audit-content")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "audit-content")

    def test_inv_2_duplicate_canonical_id_rejection(self):
        """INV-2: Registering a duplicate canonical_id must raise InvariantViolationError."""
        self.registry.add_entry(self.entry_a)
        duplicate = RegistryEntry(
            canonical_id="seo:audit-content",
            urn="",
            name="audit-content-duplicate",
            role="workflow",
        )
        with self.assertRaises(InvariantViolationError) as ctx:
            self.registry.add_entry(duplicate)
        self.assertIn("Invariant 2 Violation", str(ctx.exception))

    def test_json_roundtrip_idempotency(self):
        self.registry.add_entry(self.entry_a)
        self.registry.add_entry(self.entry_b)
        json_output = self.registry.to_json()

        restored = CatalogRegistry.from_json(json_output)
        self.assertEqual(restored.commit_sha, "test-commit-sha-123")
        self.assertEqual(len(restored.skills), 2)
        self.assertEqual(restored.to_json(), json_output)


class TestSemanticGroups(unittest.TestCase):
    """Verifies SemanticGroup schema, cross-domain grouping, and group validation."""

    def test_semantic_group_creation_and_membership(self):
        grp = SemanticGroupObject(
            group_id="fullstack-auth",
            name="Fullstack Authentication",
            description="Cross-cutting authentication tools.",
            domain_scope="cross-domain",
            members=["supabase:manage-auth", "nextjs:setup-auth-middleware", "security:audit-jwt"],
            tags=["auth", "security", "jwt"],
        )
        self.assertEqual(grp.group_id, "fullstack-auth")
        self.assertEqual(len(grp.members), 3)

        d = grp.to_dict()
        self.assertEqual(d["group_id"], "fullstack-auth")
        self.assertEqual(d["members"], ["nextjs:setup-auth-middleware", "security:audit-jwt", "supabase:manage-auth"])

        restored = SemanticGroupObject.from_dict(d)
        self.assertEqual(restored.group_id, grp.group_id)

    def test_invalid_group_id_rejection(self):
        with self.assertRaises(RegistryError):
            SemanticGroupObject(group_id="Invalid Group Name!", name="Invalid")

        with self.assertRaises(CanonicalIdentityError):
            SemanticGroupObject(
                group_id="bad-members",
                name="Bad Members",
                members=["invalid_id_without_colon"],
            )


class TestDependencyResolverAndDAGInvariants(unittest.TestCase):
    """Verifies transitive closure, topological sort, INV-1 (Acyclicity), and INV-8 (Dead Reference)."""

    def setUp(self):
        self.registry = CatalogRegistry()
        # Build valid DAG:
        # A depends on B and C
        # B depends on D
        # C depends on D
        # D (primitive) depends on nothing
        self.entry_d = RegistryEntry(canonical_id="core:token-primitive", urn="", name="token-primitive", role="primitive")
        self.entry_b = RegistryEntry(
            canonical_id="backend:db-query",
            urn="",
            name="db-query",
            role="capability",
            relationships={"composed_of": [], "extends": None, "depends_on": ["core:token-primitive"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        self.entry_c = RegistryEntry(
            canonical_id="backend:cache-manager",
            urn="",
            name="cache-manager",
            role="capability",
            relationships={"composed_of": [], "extends": None, "depends_on": ["core:token-primitive"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        self.entry_a = RegistryEntry(
            canonical_id="workflow:user-sync",
            urn="",
            name="user-sync",
            role="workflow",
            relationships={"composed_of": ["backend:db-query", "backend:cache-manager"], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )

        for e in [self.entry_a, self.entry_b, self.entry_c, self.entry_d]:
            self.registry.add_entry(e)

        self.resolver = DependencyResolver(self.registry)

    def test_transitive_dependency_closure(self):
        """Transitive closure of workflow:user-sync must include A, B, C, and D."""
        closure = self.resolver.compute_transitive_closure("workflow:user-sync")
        self.assertEqual(closure, {
            "workflow:user-sync",
            "backend:db-query",
            "backend:cache-manager",
            "core:token-primitive",
        })

    def test_topological_execution_plan(self):
        """In execution plan, prerequisites must appear before their dependents."""
        plan = self.resolver.compute_execution_plan("workflow:user-sync")
        self.assertEqual(len(plan), 4)

        idx_d = plan.index("core:token-primitive")
        idx_b = plan.index("backend:db-query")
        idx_c = plan.index("backend:cache-manager")
        idx_a = plan.index("workflow:user-sync")

        # D must precede B and C
        self.assertLess(idx_d, idx_b)
        self.assertLess(idx_d, idx_c)
        # B and C must precede A
        self.assertLess(idx_b, idx_a)
        self.assertLess(idx_c, idx_a)

    def test_inv_1_dag_acyclicity_rejection_direct_cycle(self):
        """INV-1: Direct circular dependency (A -> B -> A) must be detected and rejected."""
        cyc_reg = CatalogRegistry()
        e1 = RegistryEntry(
            canonical_id="test:skill-a",
            urn="",
            name="skill-a",
            role="capability",
            relationships={"composed_of": [], "extends": None, "depends_on": ["test:skill-b"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        e2 = RegistryEntry(
            canonical_id="test:skill-b",
            urn="",
            name="skill-b",
            role="capability",
            relationships={"composed_of": [], "extends": None, "depends_on": ["test:skill-a"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        cyc_reg.add_entry(e1)
        cyc_reg.add_entry(e2)

        res = DependencyResolver(cyc_reg)
        with self.assertRaises(InvariantViolationError) as ctx:
            res.validate_invariants()
        self.assertIn("Invariant 1 Violation", str(ctx.exception))
        self.assertIn("Circular relationship detected", str(ctx.exception))

    def test_inv_1_dag_acyclicity_rejection_multi_hop_cycle(self):
        """INV-1: Multi-hop circular dependency (A -> B -> C -> A) must be detected and rejected."""
        cyc_reg = CatalogRegistry()
        e1 = RegistryEntry(canonical_id="cycle:node-1", urn="", name="node-1", role="capability", relationships={"composed_of": ["cycle:node-2"], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None})
        e2 = RegistryEntry(canonical_id="cycle:node-2", urn="", name="node-2", role="capability", relationships={"composed_of": ["cycle:node-3"], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None})
        e3 = RegistryEntry(canonical_id="cycle:node-3", urn="", name="node-3", role="capability", relationships={"composed_of": ["cycle:node-1"], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None})
        for e in [e1, e2, e3]:
            cyc_reg.add_entry(e)

        res = DependencyResolver(cyc_reg)
        with self.assertRaises(InvariantViolationError) as ctx:
            res.validate_invariants()
        self.assertIn("Invariant 1 Violation", str(ctx.exception))

    def test_inv_8_dead_reference_rejection(self):
        """INV-8: Dangling target pointers in relationships must trigger InvariantViolationError."""
        bad_reg = CatalogRegistry()
        e = RegistryEntry(
            canonical_id="test:caller",
            urn="",
            name="caller",
            role="capability",
            relationships={"composed_of": [], "extends": None, "depends_on": ["nonexistent:target-skill"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        bad_reg.add_entry(e)

        res = DependencyResolver(bad_reg)
        with self.assertRaises(InvariantViolationError) as ctx:
            res.validate_invariants()
        self.assertIn("Invariant 8 Violation", str(ctx.exception))
        self.assertIn("nonexistent:target-skill", str(ctx.exception))

    def test_inv_4_shallow_overlay_violation(self):
        """INV-4: Overlay extending another overlay or non-cap/wf must be rejected."""
        reg = CatalogRegistry()
        base = RegistryEntry(canonical_id="core:base-cap", urn="", name="base-cap", role="capability")
        ov1 = RegistryEntry(
            canonical_id="overlay:layer-1",
            urn="",
            name="layer-1",
            role="overlay",
            relationships={"composed_of": [], "extends": "core:base-cap", "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        ov2 = RegistryEntry(
            canonical_id="overlay:layer-2",
            urn="",
            name="layer-2",
            role="overlay",
            relationships={"composed_of": [], "extends": "overlay:layer-1", "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        for e in [base, ov1, ov2]:
            reg.add_entry(e)

        res = DependencyResolver(reg)
        with self.assertRaises(InvariantViolationError) as ctx:
            res.validate_invariants()
        self.assertIn("Invariant 4 Violation", str(ctx.exception))
        self.assertIn("Overlays cannot extend overlays", str(ctx.exception))

    def test_inv_5_leaf_primitive_violation(self):
        """INV-5: Primitives declaring composed_of must be rejected."""
        reg = CatalogRegistry()
        dep = RegistryEntry(canonical_id="core:sub-leaf", urn="", name="sub-leaf", role="capability")
        prim = RegistryEntry(
            canonical_id="core:bad-primitive",
            urn="",
            name="bad-primitive",
            role="primitive",
            relationships={"composed_of": ["core:sub-leaf"], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        reg.add_entry(dep)
        reg.add_entry(prim)

        res = DependencyResolver(reg)
        with self.assertRaises(InvariantViolationError) as ctx:
            res.validate_invariants()
        self.assertIn("Invariant 5 Violation", str(ctx.exception))

    def test_orphan_detection(self):
        """Prims/adapters not referenced by any capability or workflow are detected."""
        reg = CatalogRegistry()
        orphan_p = RegistryEntry(canonical_id="core:orphan-prim", urn="", name="orphan-prim", role="primitive")
        orphan_a = RegistryEntry(canonical_id="core:orphan-adapt", urn="", name="orphan-adapt", role="adapter")
        reg.add_entry(orphan_p)
        reg.add_entry(orphan_a)

        res = DependencyResolver(reg)
        orphans = res.find_orphaned_primitives_and_adapters()
        self.assertIn("core:orphan-prim", orphans["orphaned_primitives"])
        self.assertIn("core:orphan-adapt", orphans["orphaned_adapters"])


class TestAliasResolverAndInvariants(unittest.TestCase):
    """Verifies Single-Hop Alias Resolution (INV-3) and direction-neutral duplicate pair resolution."""

    def setUp(self):
        self.registry = CatalogRegistry()
        self.cap = RegistryEntry(
            canonical_id="github:create-pull-request",
            urn="",
            name="create-pull-request",
            role="capability",
            description="Canonical create PR capability.",
        )
        self.alias_direct = RegistryEntry(
            canonical_id="dev:create-pr",
            urn="",
            name="create-pr",
            role="alias",
            status="deprecated",
            relationships={"composed_of": [], "extends": None, "depends_on": [], "adapts": None, "aliased_to": "github:create-pull-request", "belongs_to_family": None},
        )
        self.registry.add_entry(self.cap)
        self.registry.add_entry(self.alias_direct)
        self.resolver = AliasResolver(self.registry)

    def test_single_hop_alias_resolution(self):
        """Resolving dev:create-pr yields canonical target github:create-pull-request."""
        target, hops = self.resolver.resolve("dev:create-pr")
        self.assertEqual(target.canonical_id, "github:create-pull-request")
        self.assertEqual(hops, ["dev:create-pr", "github:create-pull-request"])

    def test_non_alias_resolves_directly(self):
        target, hops = self.resolver.resolve("github:create-pull-request")
        self.assertEqual(target.canonical_id, "github:create-pull-request")
        self.assertEqual(hops, ["github:create-pull-request"])

    def test_inv_3_chained_alias_rejection(self):
        """INV-3: Chained alias (A -> B -> C) must raise InvariantViolationError."""
        alias_chained = RegistryEntry(
            canonical_id="legacy:pr-maker",
            urn="",
            name="pr-maker",
            role="alias",
            relationships={"composed_of": [], "extends": None, "depends_on": [], "adapts": None, "aliased_to": "dev:create-pr", "belongs_to_family": None},
        )
        self.registry.add_entry(alias_chained)

        with self.assertRaises(InvariantViolationError) as ctx:
            self.resolver.resolve("legacy:pr-maker")
        self.assertIn("Invariant 3 Violation", str(ctx.exception))
        self.assertIn("chaining forbidden", str(ctx.exception))

    def test_inv_8_dead_reference_alias(self):
        """Alias pointing to non-existent target raises InvariantViolationError."""
        bad_alias = RegistryEntry(
            canonical_id="ghost:alias",
            urn="",
            name="ghost-alias",
            role="alias",
            relationships={"composed_of": [], "extends": None, "depends_on": [], "adapts": None, "aliased_to": "ghost:missing", "belongs_to_family": None},
        )
        self.registry.add_entry(bad_alias)

        with self.assertRaises(InvariantViolationError) as ctx:
            self.resolver.resolve("ghost:alias")
        self.assertIn("Invariant 8 Violation", str(ctx.exception))

    def test_deprecation_telemetry(self):
        telem = self.resolver.get_deprecation_telemetry("dev:create-pr")
        self.assertTrue(telem["is_alias"])
        self.assertTrue(telem["is_deprecated"])
        self.assertEqual(telem["canonical_target"], "github:create-pull-request")
        self.assertIn("Please update references", telem["deprecation_notice"])

    def test_direction_neutral_duplicate_pair_resolution(self):
        """Helper produces governed outcomes for duplicate candidates under ADR-004 Section 5.2."""
        hub_cap = RegistryEntry(
            canonical_id="github:list-repos",
            urn="",
            name="list-repos",
            role="capability",
            domain="tools-and-platforms",
            physical_path="library/tools-and-platforms/github/list-repos",
            relationships={"composed_of": [], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": "github"},
        )
        legacy_data = {
            "canonical_id": "development:github-list-repos",
            "name": "list-repos",
            "domain": "development",
            "category": "development",
            "subcategory": "backend",
            "physical_path": "library/development/backend/list-repos",
        }
        # Outcome 1: PLATFORM_CANONICAL (hub is canonical, domain is deprecated alias)
        canonical, alias = AliasResolver.build_direction_neutral_duplicate_pair(
            hub_cap, legacy_data, outcome=DuplicateAdjudicationOutcome.PLATFORM_CANONICAL
        )
        self.assertEqual(canonical.canonical_id, "github:list-repos")
        self.assertEqual(alias.canonical_id, "development:github-list-repos")
        self.assertEqual(alias.role, "alias")
        self.assertEqual(alias.status, "deprecated")
        self.assertEqual(alias.relationships["aliased_to"], "github:list-repos")

        # Outcome 2: DOMAIN_CANONICAL (domain is canonical, hub is platform alias)
        c_dom, a_hub = AliasResolver.build_direction_neutral_duplicate_pair(
            hub_cap, legacy_data, outcome=DuplicateAdjudicationOutcome.DOMAIN_CANONICAL
        )
        self.assertEqual(c_dom.canonical_id, "development:github-list-repos")
        self.assertEqual(a_hub.canonical_id, "github:list-repos")
        self.assertEqual(a_hub.role, "alias")
        self.assertEqual(a_hub.status, "deprecated")
        self.assertEqual(a_hub.relationships["aliased_to"], "development:github-list-repos")

        # Outcome 3: DUAL_RETENTION (both canonicals, zero aliases)
        e1, e2 = AliasResolver.build_direction_neutral_duplicate_pair(
            hub_cap, legacy_data, outcome=DuplicateAdjudicationOutcome.DUAL_RETENTION
        )
        self.assertEqual(e1.canonical_id, "github:list-repos")
        self.assertEqual(e2.canonical_id, "development:github-list-repos")
        self.assertNotEqual(e1.role, "alias")
        self.assertNotEqual(e2.role, "alias")
        self.assertIsNone(e1.relationships.get("aliased_to"))
        self.assertIsNone(e2.relationships.get("aliased_to"))

        # Outcome 4: PENDING_ADJUDICATION (direction-neutral provisional baseline)
        p1, p2 = AliasResolver.build_direction_neutral_duplicate_pair(
            hub_cap, legacy_data, outcome=DuplicateAdjudicationOutcome.PENDING_ADJUDICATION
        )
        self.assertEqual(p1.status, "provisional")
        self.assertEqual(p2.status, "provisional")
        self.assertIsNone(p1.relationships.get("aliased_to"))
        self.assertIsNone(p2.relationships.get("aliased_to"))

    def test_omitted_outcome_defaults_to_pending_adjudication_safe_by_construction(self):
        """
        Regression test: omitting the outcome parameter in build_direction_neutral_duplicate_pair
        MUST default to PENDING_ADJUDICATION.
        It must NEVER create an alias or mark either skill deprecated without explicit adjudication.
        """
        hub_cap = RegistryEntry(
            canonical_id="github:list-repos",
            urn="",
            name="list-repos",
            role="capability",
            domain="tools-and-platforms",
            physical_path="library/tools-and-platforms/github/list-repos",
            relationships={"composed_of": [], "extends": None, "depends_on": [], "adapts": None, "aliased_to": None, "belongs_to_family": "github"},
        )
        legacy_data = {
            "canonical_id": "development:github-list-repos",
            "name": "list-repos",
            "domain": "development",
            "category": "development",
            "subcategory": "backend",
            "physical_path": "library/development/backend/list-repos",
        }

        # Call with omitted outcome
        e_hub, e_domain = AliasResolver.build_direction_neutral_duplicate_pair(hub_cap, legacy_data)

        # Neither skill may be converted to an alias
        self.assertNotEqual(e_hub.role, "alias", "Hub must not be converted to alias by default")
        self.assertNotEqual(e_domain.role, "alias", "Domain skill must not be converted to alias by default")

        # Neither skill may have an aliased_to pointer
        self.assertIsNone(e_hub.relationships.get("aliased_to"), "Hub must have no aliased_to pointer")
        self.assertIsNone(e_domain.relationships.get("aliased_to"), "Domain skill must have no aliased_to pointer")

        # Neither skill may be marked deprecated
        self.assertNotEqual(e_hub.status, "deprecated", "Hub must not be marked deprecated by default")
        self.assertNotEqual(e_domain.status, "deprecated", "Domain skill must not be marked deprecated by default")

        # Both remain in provisional direction-neutral baseline
        self.assertEqual(e_hub.status, "provisional")
        self.assertEqual(e_domain.status, "provisional")


class TestMultiViewProjector(unittest.TestCase):
    """Verifies all 4 projection views and inverted search index generation."""

    def setUp(self):
        self.registry = CatalogRegistry()
        self.e1 = RegistryEntry(
            canonical_id="github:create-pr",
            urn="",
            name="create-pr",
            role="capability",
            description="Create PR on GitHub repository.",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="github",
            families=["github"],
            semantic_groups=["git-automation"],
            physical_path="library/tools-and-platforms/github/create-pr",
            tags=["git", "pr"],
            keywords=["pull request"],
            execution_providers=[{"provider_id": "gh-cli", "provider_type": "cli", "transport": "bash", "is_default": True}],
        )
        self.e2 = RegistryEntry(
            canonical_id="dev:git-branch",
            urn="",
            name="git-branch",
            role="capability",
            description="Manage git branches.",
            domain="development",
            category="development",
            subcategory="version-control",
            families=["github"],
            semantic_groups=["git-automation"],
            physical_path="library/development/version-control/git-branch",
            tags=["git", "branch"],
            keywords=["checkout"],
            execution_providers=[{"provider_id": "git-mcp", "provider_type": "mcp", "transport": "mcp", "is_default": True}],
        )
        self.registry.add_entry(self.e1)
        self.registry.add_entry(self.e2)
        self.projector = MultiViewProjector(self.registry)

    def test_functional_view_projection(self):
        view = self.projector.project_functional_view()
        self.assertEqual(view["view_type"], "functional_domain")
        self.assertIn("tools-and-platforms", view["domains"])
        self.assertIn("development", view["domains"])
        skills = view["domains"]["development"]["development"]["version-control"]
        self.assertEqual(skills[0]["canonical_id"], "dev:git-branch")

    def test_family_view_projection(self):
        meta = {"github": {"title": "GitHub Platform", "tier": "tier_1_platform_hub"}}
        view = self.projector.project_family_view(meta)
        self.assertEqual(view["view_type"], "platform_family")
        self.assertIn("github", view["families"])
        fam = view["families"]["github"]
        self.assertEqual(fam["total_members"], 2)
        self.assertEqual(len(fam["tier_1_members"]), 1)
        self.assertEqual(fam["tier_1_members"][0]["canonical_id"], "github:create-pr")
        self.assertEqual(len(fam["tier_2_members"]), 1)
        self.assertEqual(fam["tier_2_members"][0]["canonical_id"], "dev:git-branch")

    def test_semantic_group_view_projection(self):
        view = self.projector.project_semantic_group_view()
        self.assertEqual(view["view_type"], "semantic_group")
        self.assertIn("git-automation", view["groups"])
        grp = view["groups"]["git-automation"]
        self.assertEqual(grp["members"], ["dev:git-branch", "github:create-pr"])

    def test_provider_view_projection(self):
        view = self.projector.project_provider_view()
        self.assertEqual(view["view_type"], "execution_provider")
        self.assertIn("bash", view["transports"])
        self.assertIn("mcp", view["transports"])
        self.assertEqual(view["transports"]["mcp"][0]["canonical_id"], "dev:git-branch")

    def test_inverted_search_index(self):
        index = self.projector.build_search_index()
        self.assertIn("pull", index)
        self.assertIn("github:create-pr", index["pull"])
        self.assertIn("branch", index)
        self.assertIn("dev:git-branch", index["branch"])


class TestProjectMaterializerAndTransitiveCompleteness(unittest.TestCase):
    """Verifies INV-9 (Transitive Completeness Guarantee) and flat runtime naming."""

    def setUp(self):
        self.registry = CatalogRegistry()
        # Cap A depends on Prim B
        self.prim = RegistryEntry(canonical_id="shared:auth", urn="", name="auth", role="primitive", category="shared")
        self.cap = RegistryEntry(
            canonical_id="dev:api-caller",
            urn="",
            name="api-caller",
            role="capability",
            category="development",
            relationships={"composed_of": [], "extends": None, "depends_on": ["shared:auth"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )
        # Another skill with leaf name collision
        self.marketing_caller = RegistryEntry(
            canonical_id="marketing:api-caller",
            urn="",
            name="api-caller",
            role="capability",
            category="marketing",
            relationships={"composed_of": [], "extends": None, "depends_on": ["shared:auth"], "adapts": None, "aliased_to": None, "belongs_to_family": None},
        )

        for e in [self.prim, self.cap, self.marketing_caller]:
            self.registry.add_entry(e)

        self.materializer = ProjectMaterializer(self.registry)

    def test_inv_9_transitive_completeness_guarantee(self):
        """Materializing dev:api-caller must automatically bundle its prerequisite shared:auth."""
        bundle = self.materializer.materialize_bundle(
            mode=ProjectionMode.STANDALONE_CLOSURE,
            target_ids=["dev:api-caller"],
        )
        self.assertEqual(bundle["target_count"], 1)
        self.assertEqual(bundle["total_materialized"], 2)
        self.assertIn("shared:auth", bundle["closure"])
        self.assertIn("dev:api-caller", bundle["closure"])

        # Prerequisite auth must precede caller in execution order
        self.assertEqual(bundle["execution_order"], ["shared:auth", "dev:api-caller"])

    def test_flat_runtime_naming_collision_resolution(self):
        """Colliding leaf names receive scoped prefixes; unique names do not."""
        bundle = self.materializer.materialize_bundle(mode=ProjectionMode.FULL)
        names = bundle["runtime_names"]

        # 'auth' is unique, so un-prefixed
        self.assertEqual(names["shared:auth"], "auth")
        # 'api-caller' collided between development and marketing, so prefixed
        self.assertEqual(names["dev:api-caller"], "development-api-caller")
        self.assertEqual(names["marketing:api-caller"], "marketing-api-caller")

    def test_flat_runtime_naming_collision_identical_name_and_category(self):
        """
        When two skills share identical leaf name AND identical category,
        materializer falls back to canonical scope to guarantee collision-free uniqueness.
        """
        e1 = RegistryEntry(
            canonical_id="dev:commit",
            urn="",
            name="commit",
            role="capability",
            category="development",
        )
        e2 = RegistryEntry(
            canonical_id="github:commit",
            urn="",
            name="commit",
            role="capability",
            category="development",
        )
        reg = CatalogRegistry()
        reg.add_entry(e1)
        reg.add_entry(e2)
        mat = ProjectMaterializer(reg)
        bundle = mat.materialize_bundle(mode=ProjectionMode.FULL)
        names = bundle["runtime_names"]

        self.assertEqual(len(set(names.values())), 2, "Runtime names must be globally unique")
        self.assertNotEqual(names["dev:commit"], names["github:commit"])
        self.assertIn("commit", names["dev:commit"])
        self.assertIn("commit", names["github:commit"])

    def test_flat_runtime_naming_collision_with_existing_prefix_name(self):
        """
        When a skill's natural name matches another skill's category prefix candidate,
        materializer prevents prefix collision from stealing the natural name.
        """
        e1 = RegistryEntry(
            canonical_id="tools:development-commit",
            urn="",
            name="development-commit",
            role="capability",
            category="tools",
        )
        e2 = RegistryEntry(
            canonical_id="dev:commit",
            urn="",
            name="commit",
            role="capability",
            category="development",
        )
        e3 = RegistryEntry(
            canonical_id="git:commit",
            urn="",
            name="commit",
            role="capability",
            category="development",
        )
        reg = CatalogRegistry()
        reg.add_entry(e1)
        reg.add_entry(e2)
        reg.add_entry(e3)
        mat = ProjectMaterializer(reg)
        bundle = mat.materialize_bundle(mode=ProjectionMode.FULL)
        names = bundle["runtime_names"]

        # e1 has unique natural name 'development-commit' and must keep it
        self.assertEqual(names["tools:development-commit"], "development-commit")
        # e2 and e3 must receive distinct names without colliding with e1
        self.assertNotEqual(names["dev:commit"], "development-commit")
        self.assertNotEqual(names["git:commit"], "development-commit")
        self.assertEqual(len(set(names.values())), 3)


class TestFamilyRouterGenerator(unittest.TestCase):
    """Verifies Tier 1 and Tier 2 markdown router formatting rules."""

    def test_tier_1_hub_router_generation(self):
        entries = [
            RegistryEntry(
                canonical_id="github:auth-token",
                urn="",
                name="auth-token",
                role="primitive",
                description="GitHub authentication token provider.",
                physical_path="library/tools-and-platforms/github/auth-token",
            ),
            RegistryEntry(
                canonical_id="github:create-issue",
                urn="",
                name="create-issue",
                role="capability",
                description="Creates a GitHub issue.",
                physical_path="library/tools-and-platforms/github/create-issue",
                execution_providers=[{"transport": "cli"}],
            ),
        ]
        router_md = FamilyRouterGenerator.generate_tier_1_hub_router(
            family_slug="github",
            family_title="GitHub Platform",
            vendor="GitHub / Microsoft",
            member_entries=entries,
        )
        self.assertIn("# GitHub Platform Platform Router", router_md)
        self.assertIn("Tier 1 Platform Hub", router_md)
        self.assertIn("- [auth-token](auth-token/SKILL.md):", router_md)
        self.assertIn("- [create-issue](create-issue/SKILL.md) [CLI]:", router_md)
        # Must not contain absolute filesystem paths
        self.assertNotIn("/Users/", router_md)
        self.assertNotIn("/home/", router_md)

    def test_tier_1_hub_router_nested_and_domain_anchored_paths(self):
        """Derived router links correctly handle nested child directories and domain-anchored paths."""
        entries = [
            RegistryEntry(
                canonical_id="github:deploy-action",
                urn="",
                name="deploy-action",
                role="capability",
                description="Deploy action workflow.",
                physical_path="library/tools-and-platforms/github/actions/deploy-action",
            ),
            RegistryEntry(
                canonical_id="dev:gh-sync",
                urn="",
                name="gh-sync",
                role="capability",
                description="Sync helper anchored in functional domain.",
                physical_path="library/development/backend/gh-sync",
            ),
        ]
        router_md = FamilyRouterGenerator.generate_tier_1_hub_router(
            family_slug="github",
            family_title="GitHub Platform",
            vendor="GitHub / Microsoft",
            member_entries=entries,
        )
        self.assertIn("- [deploy-action](actions/deploy-action/SKILL.md):", router_md)
        self.assertIn("- [gh-sync](../../development/backend/gh-sync/SKILL.md):", router_md)

    def test_tier_2_virtual_router_generation(self):
        entries = [
            RegistryEntry(
                canonical_id="db:supabase-query",
                urn="",
                name="supabase-query",
                role="capability",
                category="databases",
                subcategory="sql",
                description="Executes Supabase SQL queries.",
                physical_path="library/databases/sql/supabase-query",
            ),
        ]
        router_md = FamilyRouterGenerator.generate_tier_2_virtual_router(
            family_slug="supabase",
            family_title="Supabase Backend Platform",
            vendor="Supabase Inc.",
            member_entries=entries,
        )
        self.assertIn("# Supabase Backend Platform Logical Family Router", router_md)
        self.assertIn("Tier 2 Logical Family", router_md)
        self.assertIn("Databases", router_md)
        self.assertIn("- [supabase-query](../../library/databases/sql/supabase-query/SKILL.md)", router_md)
        self.assertNotIn("/Users/", router_md)

    def test_router_generation_missing_physical_path_raises_registry_error(self):
        entries = [
            RegistryEntry(
                canonical_id="github:missing-path",
                urn="",
                name="missing-path",
                role="capability",
                physical_path="",
            )
        ]
        with self.assertRaises(RegistryError) as ctx:
            FamilyRouterGenerator.generate_tier_1_hub_router(
                family_slug="github",
                family_title="GitHub",
                vendor="GitHub",
                member_entries=entries,
            )
        self.assertIn("has no physical_path", str(ctx.exception))

    def test_router_generation_prohibited_absolute_path_raises_registry_error(self):
        entries = [
            RegistryEntry(
                canonical_id="github:abs-path",
                urn="",
                name="abs-path",
                role="capability",
                physical_path="/Users/user/skills-library/library/tools-and-platforms/github/abs-path",
            )
        ]
        with self.assertRaises(RegistryError) as ctx:
            FamilyRouterGenerator.generate_tier_1_hub_router(
                family_slug="github",
                family_title="GitHub",
                vendor="GitHub",
                member_entries=entries,
            )
        self.assertIn("Prohibited absolute path", str(ctx.exception))


class TestCatalogCompilerAndIdempotency(unittest.TestCase):
    """Verifies end-to-end compilation pipeline and INV-10 (Deterministic Output)."""

    def test_deterministic_compilation_and_zero_drift(self):
        # Create a set of SkillObjects
        cap1 = CapabilityObject(canonical_id="tools:curl-fetch", name="curl-fetch", description="HTTP fetch")
        cap2 = CapabilityObject(canonical_id="tools:json-parse", name="json-parse", description="JSON parser")
        wf = WorkflowObject(canonical_id="wf:api-workflow", name="api-workflow", description="Fetch and parse")
        wf.add_relationship(RelationshipType.COMPOSED_OF, "tools:curl-fetch")
        wf.add_relationship(RelationshipType.COMPOSED_OF, "tools:json-parse")

        compiler = CatalogCompiler(commit_sha="commit-abc-456")
        reg1, proj1, idx1 = compiler.compile(skill_objects=[wf, cap2, cap1])
        reg2, proj2, idx2 = compiler.compile(skill_objects=[cap1, wf, cap2])

        # Regardless of input list order, compiled JSON must be byte-for-byte identical (INV-10)
        json1 = reg1.to_json()
        json2 = reg2.to_json()
        self.assertEqual(json1, json2)

        # Projections and search index must also be identical
        self.assertEqual(json.dumps(proj1, sort_keys=True), json.dumps(proj2, sort_keys=True))
        self.assertEqual(json.dumps(idx1, sort_keys=True), json.dumps(idx2, sort_keys=True))

    def test_deterministic_compilation_two_independent_instances_byte_identical(self):
        """
        Two separate CatalogCompiler instances with identical inputs and no explicit timestamp
        must produce byte-for-byte identical output without wall-clock drift.
        """
        cap1 = CapabilityObject(canonical_id="tools:curl-fetch", name="curl-fetch", description="HTTP fetch")
        cap2 = CapabilityObject(canonical_id="tools:json-parse", name="json-parse", description="JSON parser")

        compiler1 = CatalogCompiler()
        compiler2 = CatalogCompiler()

        reg1, proj1, idx1 = compiler1.compile(skill_objects=[cap1, cap2])
        reg2, proj2, idx2 = compiler2.compile(skill_objects=[cap1, cap2])

        # Verify byte-for-byte identical serialization across independent instances
        self.assertEqual(reg1.to_json(), reg2.to_json())
        self.assertEqual(json.dumps(proj1, sort_keys=True), json.dumps(proj2, sort_keys=True))
        self.assertEqual(json.dumps(idx1, sort_keys=True), json.dumps(idx2, sort_keys=True))

        # Verify deterministic timestamp (no wall-clock timestamp leak)
        data = reg1.to_dict()
        self.assertEqual(data["generated_at"], "1970-01-01T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
