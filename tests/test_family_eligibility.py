"""
Comprehensive Unit and Negative Regression Test Suite for REV-129 Platform Family Eligibility
and Provider-Adapter Implementation Rules.

Validates the architecture contracts defined in ADR-003 and tools/skill_library/family_contract.py:
  1. The 4-Gate Family Qualification Framework (Gates 1 through 4)
  2. Qualification of verified Tier 1 Platform Hubs (GitHub, Webflow, Figma, n8n, Hugging Face, WordPress, 1Password)
  3. Qualification of verified Tier 1 Meta-Families (Skills Lifecycle)
  4. Proper classification of Tier 2 Logical Families (NotebookLM, Stripe, Supabase)
  5. Strict disqualification and rejection of vendor sprawl (curl, jq, docker-basics, slack-notifier)
  6. Execution provider binding validation (preventing duplicate canonical IDs across mechanisms)
  7. Pure AdapterObject invariants (zero business workflow logic, protocol declaration required)
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
    RelationshipType,
    SkillObject,
    SkillRole,
    WorkflowObject,
)
from skill_library.family_contract import (
    ExecutionProviderBinding,
    ExecutionProviderContract,
    FamilyCandidateEvaluator,
    FamilyEligibilityError,
    FamilyQualificationGate,
    FamilyQualificationRecord,
    FamilyTier,
    ProviderType,
)


class TestFamilyEligibilityGates(unittest.TestCase):
    """Unit tests for the 4-Gate Family Qualification Framework."""

    def test_tier_1_platform_qualification_github(self):
        """GitHub Operations satisfies all 4 gates -> Tier 1 Platform Hub."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="github",
            member_count=22,
            categories_spanned=3,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_1_PLATFORM_HUB)
        self.assertTrue(gate.is_tier_1_eligible)
        self.assertEqual(
            FamilyCandidateEvaluator.get_physical_storage_plane("github", tier),
            "tools-and-platforms/github",
        )

    def test_tier_1_platform_qualification_webflow(self):
        """Webflow satisfies all 4 gates across 4 categories -> Tier 1 Platform Hub."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="webflow",
            member_count=22,
            categories_spanned=4,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_1_PLATFORM_HUB)
        self.assertTrue(gate.is_tier_1_eligible)
        self.assertEqual(
            FamilyCandidateEvaluator.get_physical_storage_plane("webflow", tier),
            "tools-and-platforms/webflow",
        )

    def test_tier_1_platform_qualification_single_domain_high_density_1password(self):
        """1Password satisfies high-density single-domain threshold (>=5 ops) -> Tier 1 Platform Hub."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="1password",
            member_count=5,
            categories_spanned=1,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_1_PLATFORM_HUB)
        self.assertTrue(gate.is_tier_1_eligible)
        self.assertEqual(
            FamilyCandidateEvaluator.get_physical_storage_plane("1password", tier),
            "tools-and-platforms/1password",
        )

    def test_tier_1_meta_family_skills_lifecycle(self):
        """Skills Lifecycle qualifies as Tier 1 Meta-Family -> meta-and-agent-skills/."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="skill-lifecycle",
            member_count=13,
            categories_spanned=1,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
            is_internal_meta=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_1_META_FAMILY)
        self.assertTrue(gate.is_tier_1_eligible)
        self.assertEqual(
            FamilyCandidateEvaluator.get_physical_storage_plane("skill-lifecycle", tier),
            "meta-and-agent-skills/skill-lifecycle",
        )

    def test_tier_1_platform_qualification_notebooklm_from_census(self):
        """NotebookLM satisfies all 4 gates on actual census figures (4 members across 2 domains) -> Tier 1 Platform Hub."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="notebooklm",
            member_count=4,
            categories_spanned=2,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_1_PLATFORM_HUB)
        self.assertTrue(gate.is_tier_1_eligible)
        self.assertEqual(
            FamilyCandidateEvaluator.get_physical_storage_plane("notebooklm", tier),
            "tools-and-platforms/notebooklm",
        )

    def test_tier_1_platform_qualification_notebooklm_deduplicated_scenario(self):
        """Even under a de-duplicated scenario (3 distinct skills across 2 domains), NotebookLM satisfies Gate 3."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="notebooklm",
            member_count=3,
            categories_spanned=2,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_1_PLATFORM_HUB)
        self.assertTrue(gate.is_tier_1_eligible)

    def test_tier_2_logical_family_sub_critical_mass_stripe(self):
        """Stripe has dedicated tools & primitives but sub-critical mass (2 skills, 1 domain) -> Tier 2 Logical Family."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="stripe",
            member_count=2,
            categories_spanned=1,
            has_tool_surface=True,
            has_shared_primitives=True,
            has_coordinated_lifecycle=True,
        )
        self.assertEqual(tier, FamilyTier.TIER_2_LOGICAL_FAMILY)
        self.assertFalse(gate.is_tier_1_eligible)
        self.assertTrue(gate.is_tier_2_eligible)
        self.assertEqual(
            FamilyCandidateEvaluator.get_physical_storage_plane("stripe", tier),
            "<primary_domain>/<subcategory>",
        )

    def test_census_qualification_ledger_all_candidates_match_expected_tiers(self):
        """Reconcile all candidates in the census-backed evidence ledger against their expected qualification tiers."""
        ledger = FamilyCandidateEvaluator.CENSUS_FAMILY_QUALIFICATION_LEDGER
        self.assertGreaterEqual(len(ledger), 10)

        for slug, record in ledger.items():
            with self.subTest(candidate=slug):
                tier, gate, rec = FamilyCandidateEvaluator.evaluate_from_ledger(slug)
                self.assertEqual(
                    tier,
                    record.expected_tier,
                    f"Candidate '{slug}' evaluated to {tier} but expected {record.expected_tier}",
                )
                self.assertIsNotNone(record.tool_surface_evidence)
                self.assertIsNotNone(record.shared_primitives_evidence)
                self.assertIsNotNone(record.coordinated_lifecycle_evidence)

    def test_disqualified_vendor_sprawl_generic_curl(self):
        """Generic POSIX utilities (curl, jq) fail tool surface & primitives -> Disqualified."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="curl",
            member_count=1,
            categories_spanned=1,
            has_tool_surface=False,
            has_shared_primitives=False,
            has_coordinated_lifecycle=False,
        )
        self.assertEqual(tier, FamilyTier.DISQUALIFIED_SPRAWL)
        self.assertFalse(gate.is_tier_1_eligible)
        self.assertFalse(gate.is_tier_2_eligible)

        # Attempting to assign physical platform storage raises FamilyEligibilityError
        with self.assertRaises(FamilyEligibilityError):
            FamilyCandidateEvaluator.get_physical_storage_plane("curl", tier)

    def test_disqualified_single_tool_sprawl_docker_basics(self):
        """Isolated single capability referencing an external technology cannot claim family hub."""
        tier, gate = FamilyCandidateEvaluator.evaluate(
            family_slug="docker-basics",
            member_count=1,
            categories_spanned=1,
            has_tool_surface=True,
            has_shared_primitives=False,
            has_coordinated_lifecycle=False,
        )
        self.assertEqual(tier, FamilyTier.DISQUALIFIED_SPRAWL)
        with self.assertRaises(FamilyEligibilityError):
            FamilyCandidateEvaluator.get_physical_storage_plane("docker-basics", tier)


class TestProviderAdapterRules(unittest.TestCase):
    """Unit tests for Execution Provider Binding and Adapter purity contracts."""

    def test_valid_multi_provider_binding_on_single_capability(self):
        """A single canonical capability can attach CLI, MCP, and REST execution providers."""
        cap = CapabilityObject(
            canonical_id="github:create-pr",
            name="create-pr",
            domain="development",
            description="Create a pull request with structured checklist.",
        )
        providers = [
            ExecutionProviderBinding(
                name="gh_cli",
                provider_type=ProviderType.CLI,
                command="gh pr create",
                adapter_ref="github:gh-cli-adapter",
            ),
            ExecutionProviderBinding(
                name="github_mcp",
                provider_type=ProviderType.MCP,
                tool_name="create_pull_request",
                adapter_ref="github:mcp-adapter",
            ),
            ExecutionProviderBinding(
                name="github_rest",
                provider_type=ProviderType.REST,
                endpoint="POST /repos/{owner}/{repo}/pulls",
            ),
        ]
        # Should validate without raising an error
        ExecutionProviderContract.validate_capability_providers(cap, providers)

    def test_valid_multiple_providers_of_same_type(self):
        """
        Positive regression test: A capability can attach multiple execution providers of the same
        transport type (e.g. two distinct MCP servers, or two distinct CLI binaries for different environments).
        """
        cap = CapabilityObject(
            canonical_id="github:create-pr",
            name="create-pr",
            domain="development",
            description="Create a pull request with structured checklist.",
        )
        providers = [
            # Two MCP providers for different environments/servers
            ExecutionProviderBinding(
                name="github_mcp_official",
                provider_type=ProviderType.MCP,
                tool_name="create_pull_request",
                adapter_ref="github:mcp-official-adapter",
            ),
            ExecutionProviderBinding(
                name="github_mcp_enterprise",
                provider_type=ProviderType.MCP,
                tool_name="create_pull_request",
                endpoint="https://github.enterprise.internal/api/mcp",
            ),
            # Two CLI providers for different packaging/environments
            ExecutionProviderBinding(
                name="gh_cli_brew",
                provider_type=ProviderType.CLI,
                command="gh pr create",
            ),
            ExecutionProviderBinding(
                name="gh_cli_nix",
                provider_type=ProviderType.CLI,
                command="/nix/var/nix/profiles/default/bin/gh pr create",
            ),
        ]
        # Must validate successfully without error
        ExecutionProviderContract.validate_capability_providers(cap, providers)

    def test_negative_duplicate_provider_name_rejected(self):
        """Attaching multiple providers with the same binding name is rejected."""
        cap = CapabilityObject(
            canonical_id="github:create-pr",
            name="create-pr",
            domain="development",
        )
        providers = [
            ExecutionProviderBinding(
                name="gh_cli",
                provider_type=ProviderType.CLI,
                command="gh pr create",
            ),
            ExecutionProviderBinding(
                name="gh_cli",
                provider_type=ProviderType.MCP,
                tool_name="gh_pr_create",
            ),
        ]
        with self.assertRaises(FamilyEligibilityError) as ctx:
            ExecutionProviderContract.validate_capability_providers(cap, providers)
        self.assertIn("duplicate execution provider binding name 'gh_cli'", str(ctx.exception))

    def test_negative_provider_missing_binding_target(self):
        """A non-PROMPT provider missing all binding targets (command, tool_name, endpoint, adapter_ref) is rejected."""
        with self.assertRaises(FamilyEligibilityError) as ctx:
            binding = ExecutionProviderBinding(
                name="empty_cli",
                provider_type=ProviderType.CLI,
            )
            binding.validate()
        self.assertIn("must specify at least one binding target", str(ctx.exception))

    def test_negative_canonical_slug_encoding_mechanism_rejected(self):
        """Creating duplicate skills with mechanism suffixes (e.g. create-pr-via-cli) violates Invariant."""
        cap_bad = CapabilityObject(
            canonical_id="github:create-pr-via-cli",
            name="create-pr-via-cli",
            domain="development",
        )
        providers = [
            ExecutionProviderBinding(name="gh_cli", provider_type=ProviderType.CLI, command="gh pr create")
        ]
        with self.assertRaises(InvariantViolationError) as ctx:
            ExecutionProviderContract.validate_capability_providers(cap_bad, providers)
        self.assertIn("Invariant Violation (Provider Decoupling)", str(ctx.exception))

    def test_negative_adapter_ref_cannot_be_physical_path(self):
        """An adapter reference must be a canonical ID, not a physical filesystem path."""
        cap = CapabilityObject(
            canonical_id="github:create-pr",
            name="create-pr",
            domain="development",
        )
        bad_binding = [
            ExecutionProviderBinding(
                name="gh_cli",
                provider_type=ProviderType.CLI,
                adapter_ref="library/tools-and-platforms/github/adapters/gh-cli/SKILL.md",
            )
        ]
        with self.assertRaises(FamilyEligibilityError) as ctx:
            ExecutionProviderContract.validate_capability_providers(cap, bad_binding)
        self.assertIn("Must be a canonical ID, not a physical path", str(ctx.exception))

    def test_adapter_purity_invariant(self):
        """A pure adapter specifies a protocol and interface schema with zero business workflow steps."""
        pure_adapter = AdapterObject(
            canonical_id="github:gh-cli-adapter",
            name="gh-cli-adapter",
            protocol="cli",
            interface_spec="gh pr create --title {title} --body {body}",
        )
        ExecutionProviderContract.validate_adapter_purity(pure_adapter)
        self.assertEqual(pure_adapter.protocol, "cli")

    def test_negative_adapter_containing_workflow_steps_rejected(self):
        """An adapter that embeds business workflow logic violates Adapter Purity Invariant."""
        impure_adapter = AdapterObject(
            canonical_id="github:impure-adapter",
            name="impure-adapter",
            protocol="cli",
        )
        # Inject workflow steps onto adapter
        impure_adapter.steps = ["review_code", "gate_approval", "execute_push"]
        with self.assertRaises(InvariantViolationError) as ctx:
            ExecutionProviderContract.validate_adapter_purity(impure_adapter)
        self.assertIn("Invariant Violation (Adapter Purity)", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
