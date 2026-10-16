"""
Platform Family Eligibility Specification, Verification Engine, and Provider-Adapter Rules.
Governs the contracts established under REV-129 and ADR-003:
  1. The 4-Gate Family Qualification Framework (Tool Surface, Shared Primitives, Critical Mass, Lifecycle)
  2. The 3-Tier Family Classification (Tier 1 Hubs, Tier 2 Logical Families, Disqualified Sprawl)
  3. Execution Provider Contracts (CLI, MCP, REST, SDK, Prompt) decoupling from Canonical Identity
  4. Pluggable Adapter shims (pure protocol/transport translation without domain logic)
  5. Anti-Sprawl Validation ensuring living catalog integrity
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from skill_library.object_model import (
    AdapterObject,
    CanonicalIdentity,
    CanonicalIdentityError,
    CapabilityObject,
    FamilyObject,
    InvariantViolationError,
    OverlayObject,
    SkillObject,
    SkillRole,
)


class FamilyTier(str, Enum):
    """Classification tiers for platform and tool families."""
    TIER_1_PLATFORM_HUB = "tier_1_platform_hub"         # Dedicated physical hub under tools-and-platforms/<family>/
    TIER_1_META_FAMILY = "tier_1_meta_family"           # Dedicated meta hub under meta-and-agent-skills/<family>/
    TIER_2_LOGICAL_FAMILY = "tier_2_logical_family"     # Domain-anchored logical family (metadata tag only)
    DISQUALIFIED_SPRAWL = "disqualified_sprawl"         # Vendor sprawl / isolated tool (no family designation)


class ProviderType(str, Enum):
    """Permitted execution provider mechanism types."""
    CLI = "cli"       # Local CLI binary invocation (e.g., gh, op, wp)
    MCP = "mcp"       # Model Context Protocol tool invocation
    REST = "rest"     # HTTP/REST or GraphQL API endpoint dispatch
    SDK = "sdk"       # Programmatic client SDK in Python/TS/Go
    PROMPT = "prompt" # Native reasoning / generative transformation without external tool transport


class FamilyEligibilityError(Exception):
    """Raised when family qualification or provider-adapter contracts are violated."""
    pass


@dataclass
class FamilyQualificationGate:
    """Evaluation result for the 4 qualification gates."""
    gate_1_tool_surface_cohesion: bool
    gate_2_shared_primitives: bool
    gate_3_critical_mass: bool
    gate_4_coordinated_lifecycle: bool
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_tier_1_eligible(self) -> bool:
        """Satisfies all 4 gates for a dedicated Tier 1 physical platform hub."""
        return (
            self.gate_1_tool_surface_cohesion
            and self.gate_2_shared_primitives
            and self.gate_3_critical_mass
            and self.gate_4_coordinated_lifecycle
        )

    @property
    def is_tier_2_eligible(self) -> bool:
        """Satisfies cohesion & primitives (Gates 1 & 2), but lacks critical mass or multi-domain footprint."""
        return (
            self.gate_1_tool_surface_cohesion
            and self.gate_2_shared_primitives
            and not self.is_tier_1_eligible
        )


@dataclass
class ExecutionProviderBinding:
    """Execution provider binding for a capability."""
    name: str
    provider_type: ProviderType
    adapter_ref: Optional[str] = None
    command: Optional[str] = None
    tool_name: Optional[str] = None
    endpoint: Optional[str] = None

    def validate(self) -> None:
        """Validate provider configuration invariants."""
        if not self.name or not re.match(r"^[a-z0-9_-]+$", self.name):
            raise FamilyEligibilityError(f"Invalid provider binding name '{self.name}'. Must be alphanumeric.")
        if self.adapter_ref:
            # Must reference a valid canonical ID format, not a physical path
            if "/" in self.adapter_ref or "\\" in self.adapter_ref:
                raise FamilyEligibilityError(
                    f"Invalid adapter_ref '{self.adapter_ref}'. Must be a canonical ID, not a physical path."
                )


class FamilyCandidateEvaluator:
    """
    Evaluates candidate platform ecosystems against REV-129 / ADR-003 qualification rules.
    Prevents vendor-bucket sprawl and enforces catalog structural hygiene.
    """

    # Baseline empirical catalog families recognized during REV-126/150 census
    AUTHORITATIVE_TIER_1_PLATFORMS: Dict[str, Dict[str, Any]] = {
        "github": {
            "title": "GitHub Operations",
            "vendor": "GitHub / Microsoft",
            "min_members": 22,
            "min_categories": 3,
            "surface": "gh CLI, GitHub MCP, REST API",
            "primitives": ["auth-token", "repo-context"],
        },
        "webflow": {
            "title": "Webflow Platform",
            "vendor": "Webflow",
            "min_members": 22,
            "min_categories": 4,
            "surface": "webflow-cli, Designer API, REST CMS",
            "primitives": ["site-credentials", "cms-schema-tokens"],
        },
        "figma": {
            "title": "Figma Design Platform",
            "vendor": "Figma",
            "min_members": 14,
            "min_categories": 2,
            "surface": "Figma Plugin API, Code Connect, REST",
            "primitives": ["access-token", "design-tokens"],
        },
        "n8n": {
            "title": "n8n Workflow Automation",
            "vendor": "n8n",
            "min_members": 14,
            "min_categories": 5,
            "surface": "n8n Node SDK, Public API, Community Nodes",
            "primitives": ["node-expression-syntax", "instance-credentials"],
        },
        "hugging-face": {
            "title": "Hugging Face Machine Learning",
            "vendor": "Hugging Face",
            "min_members": 19,
            "min_categories": 2,
            "surface": "huggingface_hub CLI, Python SDK, Inference API",
            "primitives": ["user-access-token", "model-repo-schema"],
        },
        "wordpress": {
            "title": "WordPress / WooCommerce CMS",
            "vendor": "Automattic / WordPress Foundation",
            "min_members": 7,
            "min_categories": 2,
            "surface": "WP-CLI, WordPress REST API",
            "primitives": ["app-passwords", "site-connection-config"],
        },
        "1password": {
            "title": "1Password Secret Management",
            "vendor": "1Password",
            "min_members": 5,
            "min_categories": 1,
            "surface": "op CLI, Connect API, K8s Operator",
            "primitives": ["service-account-token", "vault-profile"],
        },
    }

    AUTHORITATIVE_TIER_1_META_FAMILIES: Dict[str, Dict[str, Any]] = {
        "skill-lifecycle": {
            "title": "Skills Lifecycle & Governance",
            "vendor": "Internal Meta Engineering",
            "min_members": 13,
            "surface": "skill-library CLI, CI Workflows",
            "primitives": ["manifest-schema", "audit-ledger"],
        }
    }

    AUTHORITATIVE_TIER_2_LOGICAL_FAMILIES: Dict[str, Dict[str, Any]] = {
        "notebooklm": {
            "title": "NotebookLM Synthesis",
            "vendor": "Google",
            "members": 4,
            "primary_domain": "content-and-documentation",
            "surface": "NotebookLM Web / Private API",
        },
        "stripe": {
            "title": "Stripe Payments",
            "vendor": "Stripe",
            "members": 2,
            "primary_domain": "business-and-operations",
            "surface": "Stripe CLI, Stripe SDK, REST",
        },
        "supabase": {
            "title": "Supabase BaaS",
            "vendor": "Supabase",
            "members": 2,
            "primary_domain": "development",
            "surface": "supabase CLI, PostgREST, Auth SDK",
        },
    }

    # Examples of rejected vendor sprawl candidates
    DISQUALIFIED_SPRAWL_CANDIDATES: Set[str] = {
        "curl",
        "jq",
        "grep",
        "docker-basics",
        "slack-notifier",
        "json-formatter",
        "generic-webhook",
    }

    @classmethod
    def evaluate(
        cls,
        family_slug: str,
        member_count: int,
        categories_spanned: int,
        has_tool_surface: bool,
        has_shared_primitives: bool,
        has_coordinated_lifecycle: bool,
        is_internal_meta: bool = False,
    ) -> Tuple[FamilyTier, FamilyQualificationGate]:
        """
        Evaluate a candidate family against the 4 qualification gates.
        Returns the determined FamilyTier and detailed evaluation gate metrics.
        """
        slug = family_slug.lower().strip()

        # Gate 1: Tool Surface & Protocol Cohesion
        gate_1 = bool(has_tool_surface)

        # Gate 2: Shared Reusable Primitives
        gate_2 = bool(has_shared_primitives)

        # Gate 3: Critical Mass & Cross-Domain Footprint
        # - Standard cross-domain: member_count >= 3 and categories_spanned >= 2
        # - High-density single-domain: member_count >= 5 and categories_spanned >= 1
        # - Internal meta family: member_count >= 5 and is_internal_meta
        gate_3 = (
            (member_count >= 3 and categories_spanned >= 2)
            or (member_count >= 5 and categories_spanned >= 1)
            or (is_internal_meta and member_count >= 5)
        )

        # Gate 4: Coordinated Lifecycle Maintenance
        gate_4 = bool(has_coordinated_lifecycle)

        eval_gate = FamilyQualificationGate(
            gate_1_tool_surface_cohesion=gate_1,
            gate_2_shared_primitives=gate_2,
            gate_3_critical_mass=gate_3,
            gate_4_coordinated_lifecycle=gate_4,
            details={
                "slug": slug,
                "member_count": member_count,
                "categories_spanned": categories_spanned,
                "is_internal_meta": is_internal_meta,
            },
        )

        # Determine Tier
        if is_internal_meta and eval_gate.is_tier_1_eligible:
            return FamilyTier.TIER_1_META_FAMILY, eval_gate

        if eval_gate.is_tier_1_eligible:
            return FamilyTier.TIER_1_PLATFORM_HUB, eval_gate

        if eval_gate.is_tier_2_eligible:
            return FamilyTier.TIER_2_LOGICAL_FAMILY, eval_gate

        return FamilyTier.DISQUALIFIED_SPRAWL, eval_gate

    @classmethod
    def get_physical_storage_plane(cls, family_slug: str, tier: FamilyTier) -> str:
        """Determine required physical directory plane based on family qualification tier."""
        slug = family_slug.lower().strip()
        if tier == FamilyTier.TIER_1_PLATFORM_HUB:
            return f"tools-and-platforms/{slug}"
        elif tier == FamilyTier.TIER_1_META_FAMILY:
            return f"meta-and-agent-skills/{slug}"
        elif tier == FamilyTier.TIER_2_LOGICAL_FAMILY:
            # Anchored in domain tree, forbidden from claiming dedicated tools-and-platforms root
            return "<primary_domain>/<subcategory>"
        else:
            raise FamilyEligibilityError(
                f"Candidate '{family_slug}' is classified as {tier.value} and is strictly forbidden "
                "from establishing a platform directory."
            )


class ExecutionProviderContract:
    """
    Enforces Provider-Adapter architecture rules on skills.
    Ensures that different execution mechanisms (CLI, MCP, REST, SDK) do not
    proliferate duplicate canonical identities.
    """

    @classmethod
    def validate_capability_providers(
        cls,
        capability: CapabilityObject,
        providers: List[ExecutionProviderBinding],
    ) -> None:
        """
        Validate that execution providers attached to a capability adhere to:
        1. Providers are valid mechanisms.
        2. Adapter references point to valid canonical IDs, not physical paths.
        3. No canonical ID fragmentation (e.g. creating foo-via-cli and foo-via-mcp).
        """
        if not providers:
            return

        seen_types: Set[ProviderType] = set()
        for prov in providers:
            prov.validate()
            if prov.provider_type in seen_types:
                raise FamilyEligibilityError(
                    f"Capability '{capability.canonical_id}' has duplicate execution provider for type '{prov.provider_type.value}'."
                )
            seen_types.add(prov.provider_type)

        # Invariant: Canonical ID must NOT encode provider mechanisms
        forbidden_suffixes = ["-via-cli", "-via-mcp", "-via-rest", "-via-sdk", "-cli-wrapper", "-mcp-wrapper"]
        slug = capability.id_object.slug
        for suff in forbidden_suffixes:
            if slug.endswith(suff):
                raise InvariantViolationError(
                    f"Invariant Violation (Provider Decoupling): Canonical slug '{slug}' encodes execution mechanism '{suff}'. "
                    "Use a single canonical identity with pluggable ExecutionProviderBindings instead of mechanism-specific skills."
                )

    @classmethod
    def validate_adapter_purity(cls, adapter: AdapterObject) -> None:
        """
        Validate that an AdapterObject satisfies the Pure Transport Shim invariant:
        1. Must declare an external protocol or tool interface.
        2. Zero business workflow logic.
        """
        if not adapter.protocol:
            raise FamilyEligibilityError(
                f"Adapter '{adapter.canonical_id}' must specify a target protocol (e.g., mcp, cli, rest, graphql)."
            )
        # Invariant: Adapters cannot declare workflow steps
        if hasattr(adapter, "steps") and getattr(adapter, "steps"):
            raise InvariantViolationError(
                f"Invariant Violation (Adapter Purity): Adapter '{adapter.canonical_id}' contains workflow steps. "
                "Adapters must be pure transport translation shims with zero business workflow logic."
            )
