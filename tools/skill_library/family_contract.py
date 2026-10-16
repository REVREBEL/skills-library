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
class FamilyQualificationRecord:
    """Census-backed qualification evidence ledger record for a candidate ecosystem."""
    family_slug: str
    candidate_name: str
    census_member_count: int
    categories_spanned: List[str]
    subcategories_spanned: List[str]
    tool_surface_evidence: str
    shared_primitives_evidence: str
    coordinated_lifecycle_evidence: str
    gate_1_tool_surface_cohesion: bool
    gate_2_shared_primitives: bool
    gate_3_critical_mass: bool
    gate_4_coordinated_lifecycle: bool
    expected_tier: FamilyTier
    uncertain_cases_or_boundary_notes: Optional[str] = None
    is_internal_meta: bool = False


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
        if self.provider_type != ProviderType.PROMPT:
            if not (self.command or self.tool_name or self.endpoint or self.adapter_ref):
                raise FamilyEligibilityError(
                    f"Provider binding '{self.name}' ({self.provider_type.value}) must specify at least one binding target "
                    "(command, tool_name, endpoint, or adapter_ref)."
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
        "notebooklm": {
            "title": "NotebookLM Synthesis & Research",
            "vendor": "Google",
            "min_members": 4,
            "min_categories": 2,
            "surface": "NotebookLM Web Client, notebooklm-py, Playwright harness, Private RPCs",
            "primitives": ["session-cookies", "notebook-context", "source-grounding-documents"],
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

    # Authoritative Census-Backed Qualification Evidence Ledger
    # Derived from REV-126/REV-150 census, family-candidate-register.md, and skill package audits
    CENSUS_FAMILY_QUALIFICATION_LEDGER: Dict[str, FamilyQualificationRecord] = {
        "github": FamilyQualificationRecord(
            family_slug="github",
            candidate_name="GitHub Operations",
            census_member_count=22,
            categories_spanned=["development", "github-operations", "quality-and-security"],
            subcategories_spanned=["workflow-automation", "security-audit"],
            tool_surface_evidence="gh CLI, GitHub MCP server, GitHub GraphQL/REST APIs",
            shared_primitives_evidence="GH_TOKEN, GITHUB_TOKEN, repo context, Git credentials",
            coordinated_lifecycle_evidence="Actions, issues, PRs, and security scans track GitHub API/CLI changes together in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="27 generic keyword mentions pruned during census. 15 duplicate candidate pairs retained direction-neutral under REV-128.",
        ),
        "webflow": FamilyQualificationRecord(
            family_slug="webflow",
            candidate_name="Webflow Platform",
            census_member_count=22,
            categories_spanned=["design-and-experience", "development", "marketing-and-seo", "quality-and-security"],
            subcategories_spanned=["cms", "designer-extensions", "devlink", "ui-components"],
            tool_surface_evidence="webflow-cli, Webflow Designer API, Webflow REST CMS API",
            shared_primitives_evidence="Site API tokens, Designer extension tokens, DevLink React components",
            coordinated_lifecycle_evidence="Designer API versions, CMS v2 schema updates, DevLink sync track in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="6 generic audit mentions pruned during census. 16 prefix packages + 6 dedicated tools.",
        ),
        "figma": FamilyQualificationRecord(
            family_slug="figma",
            candidate_name="Figma Design Platform",
            census_member_count=14,
            categories_spanned=["design-and-experience", "development"],
            subcategories_spanned=["design-systems", "motion-and-graphics", "fullstack"],
            tool_surface_evidence="Figma Plugin API, Code Connect CLI, REST API",
            shared_primitives_evidence="Figma access tokens, design tokens, FigJam/Slides context",
            coordinated_lifecycle_evidence="Plugin manifest schema updates, REST OAuth tokens, Code Connect releases in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="2 broad design methodology skills (design-system-architect, product-design) pruned.",
        ),
        "n8n": FamilyQualificationRecord(
            family_slug="n8n",
            candidate_name="n8n Workflow Automation",
            census_member_count=14,
            categories_spanned=["business-and-operations", "data-and-ai", "marketing-and-seo", "quality-and-security", "workflow-and-automation"],
            subcategories_spanned=["integrations", "ai-workflows", "campaigns", "error-handling", "automation"],
            tool_surface_evidence="n8n Node SDK, Public REST API, Community Node interfaces",
            shared_primitives_evidence="Instance credentials, node expression syntax, webhook triggers",
            coordinated_lifecycle_evidence="Node versioning contracts, n8n core runtime upgrades in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="Member skills scattered across 5 functional categories, requiring dedicated hub consolidation.",
        ),
        "hugging-face": FamilyQualificationRecord(
            family_slug="hugging-face",
            candidate_name="Hugging Face Machine Learning",
            census_member_count=19,
            categories_spanned=["data-and-ai", "quality-and-security"],
            subcategories_spanned=["models", "datasets", "spaces", "evaluations"],
            tool_surface_evidence="huggingface_hub CLI, Python SDK, Inference API, ZeroGPU",
            shared_primitives_evidence="HF_TOKEN, dataset viewer protocols, model repository schemas",
            coordinated_lifecycle_evidence="Hub client releases, token permissions, model card schemas in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="13 hugging-face-* packages + 6 huggingface-* packages unified under single family hub.",
        ),
        "wordpress": FamilyQualificationRecord(
            family_slug="wordpress",
            candidate_name="WordPress / WooCommerce CMS",
            census_member_count=7,
            categories_spanned=["development", "marketing-and-seo"],
            subcategories_spanned=["cms", "ecommerce"],
            tool_surface_evidence="WP-CLI binary, WordPress Core REST API, WooCommerce REST API",
            shared_primitives_evidence="Application passwords, site connection configs, DB credentials",
            coordinated_lifecycle_evidence="WordPress REST API schema, PHP/plugin compatibility, WooCommerce API versions in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="7 validated members across CMS and eCommerce domains.",
        ),
        "1password": FamilyQualificationRecord(
            family_slug="1password",
            candidate_name="1Password Secret Management",
            census_member_count=5,
            categories_spanned=["infrastructure-and-ops"],
            subcategories_spanned=["secrets-management"],
            tool_surface_evidence="op CLI binary, 1Password Connect API, Kubernetes operator",
            shared_primitives_evidence="Service account tokens, vault profile paths, secret references (op://)",
            coordinated_lifecycle_evidence="op CLI v2 commands, connect server tokens, k8s operator CRDs in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes="Satisfies single-domain high-density threshold (>=5 ops) requiring dedicated primitive/adapter harness.",
        ),
        "skill-lifecycle": FamilyQualificationRecord(
            family_slug="skill-lifecycle",
            candidate_name="Skills Lifecycle & Governance",
            census_member_count=13,
            categories_spanned=["skills-create-manage-update"],
            subcategories_spanned=["lifecycle-management"],
            tool_surface_evidence="skill-library CLI, validate/lint tooling, CI workflows",
            shared_primitives_evidence="skill.json schemas, census ledger formats, ADR contracts",
            coordinated_lifecycle_evidence="Catalog architecture versions (REV-126 -> REV-130) upgrade in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_META_FAMILY,
            uncertain_cases_or_boundary_notes="Internal meta-capability family residing in meta-and-agent-skills/, not a third-party vendor platform.",
            is_internal_meta=True,
        ),
        "notebooklm": FamilyQualificationRecord(
            family_slug="notebooklm",
            candidate_name="NotebookLM Synthesis & Research",
            census_member_count=4,
            categories_spanned=["content-and-documentation", "marketing-and-seo"],
            subcategories_spanned=["presentations", "on-page-seo", "technical-writing"],
            tool_surface_evidence="NotebookLM Web Client, unofficial CLI (notebooklm-py), Playwright automation harness, private Google RPC endpoints",
            shared_primitives_evidence="Google session authentication cookies, notebook ID context, source grounding documents",
            coordinated_lifecycle_evidence="Unofficial APIs, session token extraction, and Playwright harnesses break and upgrade in lockstep whenever Google alters NotebookLM web endpoints",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            uncertain_cases_or_boundary_notes=(
                "Census contains 4 packages spanning 2 categories. Includes 1 byte-for-byte duplicate pair "
                "(library/marketing-and-seo/on-page-seo/notebooklm identical to library/content-and-documentation/presentations/notebooklm) "
                "and 2 skills in manual_review disposition. Even if de-duplicated to 3 distinct skills, it satisfies Gate 3 (>=3 skills "
                "spanning 2 categories). Classified as Tier 1 Platform Hub adhering strictly to qualification rules."
            ),
        ),
        "stripe": FamilyQualificationRecord(
            family_slug="stripe",
            candidate_name="Stripe Payments",
            census_member_count=2,
            categories_spanned=["business-and-operations"],
            subcategories_spanned=["finance-and-accounting"],
            tool_surface_evidence="Stripe CLI (stripe), Stripe Python/Node SDK, Stripe REST API",
            shared_primitives_evidence="STRIPE_SECRET_KEY, webhook signing secrets, customer/charge ID tokens",
            coordinated_lifecycle_evidence="Tracks Stripe API version dates (e.g. 2024-04-10) in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_2_LOGICAL_FAMILY,
            uncertain_cases_or_boundary_notes="Fails Gate 3 critical mass (2 members < 3 cross-domain, < 5 single-domain). Retained in business-and-operations.",
        ),
        "supabase": FamilyQualificationRecord(
            family_slug="supabase",
            candidate_name="Supabase BaaS",
            census_member_count=2,
            categories_spanned=["development"],
            subcategories_spanned=["databases"],
            tool_surface_evidence="supabase CLI, PostgREST HTTP, Supabase GoTrue Auth SDK",
            shared_primitives_evidence="SUPABASE_URL, anon key, service_role key, project ref",
            coordinated_lifecycle_evidence="Tracks Supabase platform migrations and PostgREST schema versions in lockstep",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=True,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=True,
            expected_tier=FamilyTier.TIER_2_LOGICAL_FAMILY,
            uncertain_cases_or_boundary_notes="Fails Gate 3 critical mass (2 members < 3 cross-domain, < 5 single-domain). Retained in development/databases.",
        ),
        "curl": FamilyQualificationRecord(
            family_slug="curl",
            candidate_name="cURL HTTP Utility",
            census_member_count=1,
            categories_spanned=["development"],
            subcategories_spanned=["http-tools"],
            tool_surface_evidence="Generic POSIX curl binary commands",
            shared_primitives_evidence="None (ad-hoc URLs and headers)",
            coordinated_lifecycle_evidence="None (standard POSIX utility)",
            gate_1_tool_surface_cohesion=False,
            gate_2_shared_primitives=False,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=False,
            expected_tier=FamilyTier.DISQUALIFIED_SPRAWL,
            uncertain_cases_or_boundary_notes="Generic utility failing Gates 1, 2, 3, 4. Strictly forbidden from creating family tags or platform folders.",
        ),
        "docker-basics": FamilyQualificationRecord(
            family_slug="docker-basics",
            candidate_name="Docker Basics",
            census_member_count=1,
            categories_spanned=["infrastructure-and-ops"],
            subcategories_spanned=["containerization"],
            tool_surface_evidence="Local docker CLI commands",
            shared_primitives_evidence="None (ad-hoc container names and flags)",
            coordinated_lifecycle_evidence="None (isolated utility script)",
            gate_1_tool_surface_cohesion=True,
            gate_2_shared_primitives=False,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=False,
            expected_tier=FamilyTier.DISQUALIFIED_SPRAWL,
            uncertain_cases_or_boundary_notes="Isolated single capability failing Gates 2, 3, 4. Retained as independent domain capability.",
        ),
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

    @classmethod
    def evaluate_from_ledger(
        cls,
        family_slug: str,
    ) -> Tuple[FamilyTier, FamilyQualificationGate, FamilyQualificationRecord]:
        """
        Evaluate a candidate platform family directly from the census-backed evidence ledger.
        Ensures qualification decisions are grounded in documented census evidence and inspected skill packages.
        """
        slug = family_slug.lower().strip()
        if slug not in cls.CENSUS_FAMILY_QUALIFICATION_LEDGER:
            raise FamilyEligibilityError(
                f"Candidate family '{family_slug}' is not registered in the census qualification ledger."
            )

        record = cls.CENSUS_FAMILY_QUALIFICATION_LEDGER[slug]
        tier, gate = cls.evaluate(
            family_slug=record.family_slug,
            member_count=record.census_member_count,
            categories_spanned=len(record.categories_spanned),
            has_tool_surface=record.gate_1_tool_surface_cohesion,
            has_shared_primitives=record.gate_2_shared_primitives,
            has_coordinated_lifecycle=record.gate_4_coordinated_lifecycle,
            is_internal_meta=record.is_internal_meta,
        )
        return tier, gate, record


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
        1. Providers have unique binding identities (name).
        2. Multiple providers of the same transport type (e.g. 2 MCP servers, 2 CLI tools) are permitted.
        3. Adapter references point to valid canonical IDs, not physical paths.
        4. No canonical ID fragmentation (e.g. creating foo-via-cli and foo-via-mcp).
        """
        if not providers:
            return

        seen_names: Set[str] = set()
        for prov in providers:
            prov.validate()
            if prov.name in seen_names:
                raise FamilyEligibilityError(
                    f"Capability '{capability.canonical_id}' has duplicate execution provider binding name '{prov.name}'."
                )
            seen_names.add(prov.name)

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
