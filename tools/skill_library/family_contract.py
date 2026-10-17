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
    PENDING_ADJUDICATION = "pending_adjudication"       # Uncertain or provisional qualification held pending human review
    DISQUALIFIED_SPRAWL = "disqualified_sprawl"         # Vendor sprawl / isolated tool (no family designation)


class EvidenceStatus(str, Enum):
    """Evidence rigor status for qualitative qualification gates."""
    VERIFIED_INSPECTED = "verified_inspected"           # Concrete evidence directly inspected in skill package files/scripts
    DOCUMENTED_ADJUDICATION = "documented_adjudication" # Human architectural consensus documented in census/ADR
    ASSUMPTION_PROVISIONAL = "assumption_provisional"   # Unverified assumption requiring human adjudication
    UNSUPPORTED = "unsupported"                         # Lacks required evidence; gate failed


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
    source_paths: List[str]
    candidate_membership_count: int
    duplicate_adjusted_count: int
    category_coverage: List[str]
    subcategory_coverage: List[str]
    gate_1_tool_surface_cohesion: bool
    gate_1_evidence: str
    gate_1_status: EvidenceStatus
    gate_2_shared_primitives: bool
    gate_2_evidence: str
    gate_2_status: EvidenceStatus
    gate_3_critical_mass: bool
    gate_4_coordinated_lifecycle: bool
    gate_4_evidence: str
    gate_4_status: EvidenceStatus
    expected_tier: FamilyTier
    distinct_category_coverage: Optional[List[str]] = None
    manual_review_paths: List[str] = field(default_factory=list)
    uncertain_cases_or_boundary_notes: Optional[str] = None
    is_internal_meta: bool = False

    @property
    def census_member_count(self) -> int:
        """Backward-compatibility alias for candidate_membership_count."""
        return self.candidate_membership_count

    @property
    def categories_spanned(self) -> List[str]:
        """Backward-compatibility alias for category_coverage."""
        return self.category_coverage

    @property
    def subcategories_spanned(self) -> List[str]:
        """Backward-compatibility alias for subcategory_coverage."""
        return self.subcategory_coverage

    @property
    def tool_surface_evidence(self) -> str:
        """Backward-compatibility alias for gate_1_evidence."""
        return self.gate_1_evidence

    @property
    def shared_primitives_evidence(self) -> str:
        """Backward-compatibility alias for gate_2_evidence."""
        return self.gate_2_evidence

    @property
    def coordinated_lifecycle_evidence(self) -> str:
        """Backward-compatibility alias for gate_4_evidence."""
        return self.gate_4_evidence


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
        "supabase": {
            "title": "Supabase BaaS",
            "vendor": "Supabase",
            "members": 2,
            "primary_domain": "development",
            "surface": "supabase CLI, PostgREST, Auth SDK",
        },
    }

    PENDING_ADJUDICATION_CANDIDATES: Dict[str, Dict[str, Any]] = {
        "notebooklm": {
            "title": "NotebookLM Synthesis & Research",
            "vendor": "Google",
            "candidate_members": 4,
            "duplicate_adjusted_members": 3,
            "status": "pending_adjudication",
            "reason": (
                "4 candidate packages in census, 1 duplicate pair, 3 distinct capabilities all in "
                "content-and-documentation (failing single-domain threshold 3 < 5). 2 packages (50%) under "
                "manual_review. Unofficial browser automation and cookie extraction lack verified public platform surface."
            ),
        }
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
            source_paths=[
                "library/development/fullstack/address-github-comments",
                "library/development/fullstack/openclaw-github-repo-commander",
                "library/development/fullstack/push-skill-to-github",
                "library/github-operations/actions-advanced",
                "library/github-operations/actions-debugger",
                "library/github-operations/advanced-workflows",
                "library/github-operations/commit",
                "library/github-operations/create-branch",
                "library/github-operations/create-issue-gate",
                "library/github-operations/feature-tracking",
                "library/github-operations/github",
                "library/github-operations/hooks-automation",
                "library/github-operations/issue-creator",
                "library/github-operations/llms-maintain",
                "library/github-operations/pr-merge-champion",
                "library/github-operations/pr-review",
                "library/github-operations/pr-writer",
                "library/github-operations/presence",
                "library/github-operations/publish-changes",
                "library/github-operations/review-requests",
                "library/github-operations/security-review",
                "library/quality-and-security/testing/actions-templates",
            ],
            candidate_membership_count=22,
            duplicate_adjusted_count=22,
            category_coverage=["development", "github-operations", "quality-and-security"],
            subcategory_coverage=["fullstack", "testing"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="gh CLI v2.x, official GitHub MCP server, GitHub Octokit REST and GraphQL APIs",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="GH_TOKEN, GITHUB_TOKEN, git config, repository context and credentials",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Actions, issues, PRs, and security scans track GitHub API/CLI changes together in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="27 generic keyword mentions pruned during census. 15 candidate duplicate pairs remain under direction-neutral review in REV-128.",
        ),
        "webflow": FamilyQualificationRecord(
            family_slug="webflow",
            candidate_name="Webflow Platform",
            source_paths=[
                "library/design-and-experience/taste-and-critique/webflow-ui-skills",
                "library/design-and-experience/ui-ux/designer-tools",
                "library/design-and-experience/ui-ux/flowkit-naming",
                "library/design-and-experience/ui-ux/webflow-code-component-component-scaffold",
                "library/design-and-experience/ui-ux/webflow-code-component-pre-deploy-check",
                "library/design-and-experience/ui-ux/webflow-code-components",
                "library/development/backend/safe-publish",
                "library/development/frontend/webflow-cli-code-component",
                "library/development/frontend/webflow-cli-designer-extension",
                "library/development/frontend/webflow-cli-devlink",
                "library/development/frontend/webflow-code-component-component-audit",
                "library/development/frontend/webflow-code-component-convert-component",
                "library/development/fullstack/webflow-automation",
                "library/development/fullstack/webflow-cli-cloud",
                "library/development/fullstack/webflow-code-component-deploy-guide",
                "library/development/fullstack/webflow-code-component-local-dev-setup",
                "library/development/fullstack/webflow-code-component-troubleshoot-deploy",
                "library/development/mobile/cms-collection-setup",
                "library/marketing-and-seo/cro/bulk-cms-update",
                "library/marketing-and-seo/on-page-seo/publish-blog",
                "library/quality-and-security/debugging/webflow-cli-troubleshooter",
                "library/quality-and-security/debugging/webflow-designer-api",
            ],
            candidate_membership_count=22,
            duplicate_adjusted_count=22,
            category_coverage=["design-and-experience", "development", "marketing-and-seo", "quality-and-security"],
            subcategory_coverage=["backend", "cro", "debugging", "frontend", "fullstack", "mobile", "on-page-seo", "taste-and-critique", "ui-ux"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="webflow-cli, Webflow Designer API, Webflow REST CMS v2 API",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="Site API tokens, Designer extension tokens, DevLink React components",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Designer API versions, CMS v2 schema updates, DevLink sync track in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=["library/development/fullstack/webflow-cli-cloud"],
            uncertain_cases_or_boundary_notes="6 generic audit mentions pruned during census. 16 prefix packages + 6 dedicated tools.",
        ),
        "figma": FamilyQualificationRecord(
            family_slug="figma",
            candidate_name="Figma Design Platform",
            source_paths=[
                "library/design-and-experience/design-systems/figma-code-connect",
                "library/design-and-experience/design-systems/figma-create-new-file",
                "library/design-and-experience/design-systems/figma-design-to-code",
                "library/design-and-experience/design-systems/figma-generate-design",
                "library/design-and-experience/design-systems/figma-generate-diagram",
                "library/design-and-experience/design-systems/figma-generate-library",
                "library/design-and-experience/design-systems/figma-swiftui",
                "library/design-and-experience/design-systems/figma-use",
                "library/design-and-experience/design-systems/figma-use-figjam",
                "library/design-and-experience/design-systems/figma-use-slides",
                "library/design-and-experience/design-systems/generate-project-plan",
                "library/design-and-experience/motion-and-graphics/figma-implement-motion",
                "library/design-and-experience/motion-and-graphics/figma-use-motion",
                "library/development/fullstack/figma",
            ],
            candidate_membership_count=14,
            duplicate_adjusted_count=14,
            category_coverage=["design-and-experience", "development"],
            subcategory_coverage=["design-systems", "fullstack", "motion-and-graphics"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="Figma Plugin API, Code Connect CLI, Figma REST API",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="Figma OAuth access tokens, design tokens, FigJam/Slides context",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Plugin manifest schema updates, REST OAuth tokens, Code Connect releases in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=[
                "library/design-and-experience/design-systems/figma-swiftui",
                "library/design-and-experience/motion-and-graphics/figma-implement-motion",
            ],
            uncertain_cases_or_boundary_notes="2 broad design methodology skills (design-system-architect, product-design) pruned.",
        ),
        "n8n": FamilyQualificationRecord(
            family_slug="n8n",
            candidate_name="n8n Workflow Automation",
            source_paths=[
                "library/business-and-operations/legal-and-governance/n8n-error-handling",
                "library/data-and-ai/llm-and-rag/n8n-agents",
                "library/marketing-and-seo/cro/n8n-binary-and-data",
                "library/marketing-and-seo/cro/n8n-multi-instance",
                "library/quality-and-security/debugging/n8n-code-javascript",
                "library/quality-and-security/debugging/n8n-expression-syntax",
                "library/quality-and-security/debugging/using-n8n-mcp-skills",
                "library/workflow-and-automation/tool-integration/n8n-code-python",
                "library/workflow-and-automation/tool-integration/n8n-code-tool",
                "library/workflow-and-automation/tool-integration/n8n-mcp-tools-expert",
                "library/workflow-and-automation/tool-integration/n8n-node-configuration",
                "library/workflow-and-automation/tool-integration/n8n-subworkflows",
                "library/workflow-and-automation/tool-integration/n8n-validation-expert",
                "library/workflow-and-automation/tool-integration/n8n-workflow-patterns",
            ],
            candidate_membership_count=14,
            duplicate_adjusted_count=14,
            category_coverage=["business-and-operations", "data-and-ai", "marketing-and-seo", "quality-and-security", "workflow-and-automation"],
            subcategory_coverage=["cro", "debugging", "legal-and-governance", "llm-and-rag", "tool-integration"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="n8n Node SDK, Public REST API, Community Node interfaces",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="Instance credentials, node expression syntax, webhook triggers",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Node versioning contracts, n8n core runtime upgrades in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=[
                "library/marketing-and-seo/cro/n8n-multi-instance",
                "library/quality-and-security/debugging/n8n-expression-syntax",
            ],
            uncertain_cases_or_boundary_notes="Member skills scattered across 5 functional categories, requiring dedicated hub consolidation.",
        ),
        "hugging-face": FamilyQualificationRecord(
            family_slug="hugging-face",
            candidate_name="Hugging Face Machine Learning",
            source_paths=[
                "library/data-and-ai/analytics/hugging-face-vision-trainer",
                "library/data-and-ai/llm-and-rag/hugging-face-community-evals",
                "library/data-and-ai/llm-and-rag/hugging-face-datasets",
                "library/data-and-ai/llm-and-rag/hugging-face-evaluation",
                "library/data-and-ai/machine-learning/hugging-face-cli",
                "library/data-and-ai/machine-learning/hugging-face-dataset-viewer",
                "library/data-and-ai/machine-learning/hugging-face-gradio",
                "library/data-and-ai/machine-learning/hugging-face-jobs",
                "library/data-and-ai/machine-learning/hugging-face-model-trainer",
                "library/data-and-ai/machine-learning/hugging-face-paper-publisher",
                "library/data-and-ai/machine-learning/hugging-face-papers",
                "library/data-and-ai/machine-learning/hugging-face-tool-builder",
                "library/data-and-ai/machine-learning/hugging-face-trackio",
                "library/data-and-ai/machine-learning/huggingface-best",
                "library/data-and-ai/machine-learning/huggingface-local-models",
                "library/data-and-ai/machine-learning/huggingface-lora-space-builder",
                "library/data-and-ai/machine-learning/huggingface-tool-builder",
                "library/data-and-ai/machine-learning/huggingface-zerogpu",
                "library/quality-and-security/debugging/huggingface-spaces",
            ],
            candidate_membership_count=19,
            duplicate_adjusted_count=19,
            category_coverage=["data-and-ai", "quality-and-security"],
            subcategory_coverage=["analytics", "debugging", "llm-and-rag", "machine-learning"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="huggingface_hub CLI, Python SDK, Inference API, ZeroGPU",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="HF_TOKEN, dataset viewer protocols, model repository schemas",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Hub client releases, token permissions, model card schemas in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="13 hugging-face-* packages + 6 huggingface-* packages unified under single family hub.",
        ),
        "wordpress": FamilyQualificationRecord(
            family_slug="wordpress",
            candidate_name="WordPress / WooCommerce CMS",
            source_paths=[
                "library/development/backend/wordpress",
                "library/development/backend/wordpress-core-admin",
                "library/development/backend/wordpress-performance-optimization",
                "library/development/backend/wordpress-plugin-development",
                "library/development/backend/wordpress-theme-development",
                "library/development/backend/wordpress-woocommerce",
                "library/marketing-and-seo/on-page-seo/codebase-to-wordpress-converter",
            ],
            candidate_membership_count=7,
            duplicate_adjusted_count=7,
            category_coverage=["development", "marketing-and-seo"],
            subcategory_coverage=["backend", "on-page-seo"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="WP-CLI binary, WordPress Core REST API, WooCommerce REST API",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="Application passwords, site connection configs, DB credentials",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="WordPress REST API schema, PHP/plugin compatibility, WooCommerce API versions in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="7 validated members across CMS and eCommerce domains.",
        ),
        "1password": FamilyQualificationRecord(
            family_slug="1password",
            candidate_name="1Password Secret Management",
            source_paths=[
                "library/infrastructure-and-ops/containers-and-orchestration/1password",
                "library/infrastructure-and-ops/containers-and-orchestration/1password-cli",
                "library/infrastructure-and-ops/containers-and-orchestration/1password-developer-environments",
                "library/infrastructure-and-ops/containers-and-orchestration/1password-kubernetes",
                "library/infrastructure-and-ops/containers-and-orchestration/1password-service-accounts",
            ],
            candidate_membership_count=5,
            duplicate_adjusted_count=5,
            category_coverage=["infrastructure-and-ops"],
            subcategory_coverage=["containers-and-orchestration"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="op CLI binary, 1Password Connect API, Kubernetes operator",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="Service account tokens, vault profile paths, secret references (op://)",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="op CLI v2 commands, connect server tokens, k8s operator CRDs in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_1_PLATFORM_HUB,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="Satisfies single-domain high-density threshold (>=5 ops) requiring dedicated primitive/adapter harness.",
        ),
        "skill-lifecycle": FamilyQualificationRecord(
            family_slug="skill-lifecycle",
            candidate_name="Skills Lifecycle & Governance",
            source_paths=[
                "library/skills-create-manage-update/skill-audit",
                "library/skills-create-manage-update/skill-check",
                "library/skills-create-manage-update/skill-creator",
                "library/skills-create-manage-update/skill-improver",
                "library/skills-create-manage-update/skill-inventory",
                "library/skills-create-manage-update/skill-library-restructure",
                "library/skills-create-manage-update/skill-make-template",
                "library/skills-create-manage-update/skill-manage",
                "library/skills-create-manage-update/skill-optimizer",
                "library/skills-create-manage-update/skill-review",
                "library/skills-create-manage-update/skill-writer",
                "library/skills-create-manage-update/skills-writing",
                "library/skills-create-manage-update/template-skill-enhanced",
            ],
            candidate_membership_count=13,
            duplicate_adjusted_count=13,
            category_coverage=["skills-create-manage-update"],
            subcategory_coverage=[],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="skill-library CLI, validate/lint tooling, CI workflows",
            gate_1_status=EvidenceStatus.DOCUMENTED_ADJUDICATION,
            gate_2_shared_primitives=True,
            gate_2_evidence="skill.json schemas, census ledger formats, ADR contracts",
            gate_2_status=EvidenceStatus.DOCUMENTED_ADJUDICATION,
            gate_3_critical_mass=True,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Catalog architecture versions (REV-126 -> REV-130) upgrade in lockstep",
            gate_4_status=EvidenceStatus.DOCUMENTED_ADJUDICATION,
            expected_tier=FamilyTier.TIER_1_META_FAMILY,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="Internal meta-capability family residing in meta-and-agent-skills/, not a third-party vendor platform.",
            is_internal_meta=True,
        ),
        "notebooklm": FamilyQualificationRecord(
            family_slug="notebooklm",
            candidate_name="NotebookLM Synthesis & Research",
            source_paths=[
                "library/content-and-documentation/presentations/notebooklm",
                "library/content-and-documentation/presentations/notebooklm-create",
                "library/content-and-documentation/technical-writing/notebook-lm-api",
                "library/marketing-and-seo/on-page-seo/notebooklm",
            ],
            candidate_membership_count=4,
            duplicate_adjusted_count=3,
            category_coverage=["content-and-documentation", "marketing-and-seo"],
            distinct_category_coverage=["content-and-documentation"],
            subcategory_coverage=["on-page-seo", "presentations", "technical-writing"],
            gate_1_tool_surface_cohesion=False,
            gate_1_evidence="Unofficial web client, unverified notebooklm-py script, Playwright browser scraping harness; no official public API or CLI",
            gate_1_status=EvidenceStatus.ASSUMPTION_PROVISIONAL,
            gate_2_shared_primitives=False,
            gate_2_evidence="Scraped Google web session cookies, ad-hoc notebook ID extraction across scripts; lacks standardized platform primitive package",
            gate_2_status=EvidenceStatus.ASSUMPTION_PROVISIONAL,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=False,
            gate_4_evidence="Scripts break on Google web UI updates; lacks synchronized vendor release lifecycle or formal versioning",
            gate_4_status=EvidenceStatus.ASSUMPTION_PROVISIONAL,
            expected_tier=FamilyTier.PENDING_ADJUDICATION,
            manual_review_paths=[
                "library/content-and-documentation/presentations/notebooklm-create",
                "library/marketing-and-seo/on-page-seo/notebooklm",
            ],
            uncertain_cases_or_boundary_notes=(
                "Census contains 4 packages across 2 categories, but includes 1 byte-for-byte duplicate pair "
                "(library/marketing-and-seo/on-page-seo/notebooklm identical to library/content-and-documentation/presentations/notebooklm). "
                "Distinct capabilities total 3, all residing in content-and-documentation (failing single-domain threshold 3 < 5). "
                "2 of 4 packages (50%) have manual_review dispositions. Tools rely on reverse-engineered web scraping without official APIs. "
                "Held as PENDING_ADJUDICATION in domain trees pending human architectural review."
            ),
        ),
        "supabase": FamilyQualificationRecord(
            family_slug="supabase",
            candidate_name="Supabase BaaS",
            source_paths=[
                "library/development/frontend/nextjs-supabase-auth",
                "library/marketing-and-seo/cro/supabase",
            ],
            candidate_membership_count=2,
            duplicate_adjusted_count=2,
            category_coverage=["development", "marketing-and-seo"],
            distinct_category_coverage=["development", "marketing-and-seo"],
            subcategory_coverage=["cro", "frontend"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="supabase CLI, PostgREST HTTP, Supabase GoTrue Auth SDK",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=True,
            gate_2_evidence="SUPABASE_URL, anon key, service_role key, project ref",
            gate_2_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=True,
            gate_4_evidence="Tracks Supabase platform migrations and PostgREST schema versions in lockstep",
            gate_4_status=EvidenceStatus.VERIFIED_INSPECTED,
            expected_tier=FamilyTier.TIER_2_LOGICAL_FAMILY,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="Fails Gate 3 critical mass (2 members < 3 cross-domain threshold). Retained in domain trees as logical family.",
        ),
        "curl": FamilyQualificationRecord(
            family_slug="curl",
            candidate_name="cURL HTTP Utility",
            source_paths=[],
            candidate_membership_count=0,
            duplicate_adjusted_count=0,
            category_coverage=[],
            subcategory_coverage=[],
            gate_1_tool_surface_cohesion=False,
            gate_1_evidence="Generic POSIX curl binary commands",
            gate_1_status=EvidenceStatus.UNSUPPORTED,
            gate_2_shared_primitives=False,
            gate_2_evidence="None (ad-hoc URLs and headers)",
            gate_2_status=EvidenceStatus.UNSUPPORTED,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=False,
            gate_4_evidence="None (standard POSIX utility)",
            gate_4_status=EvidenceStatus.UNSUPPORTED,
            expected_tier=FamilyTier.DISQUALIFIED_SPRAWL,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="Generic utility failing Gates 1, 2, 3, 4. Strictly forbidden from creating family tags or platform folders.",
        ),
        "docker-basics": FamilyQualificationRecord(
            family_slug="docker-basics",
            candidate_name="Docker Basics",
            source_paths=[
                "library/infrastructure-and-ops/containers-and-orchestration/docker-expert",
            ],
            candidate_membership_count=1,
            duplicate_adjusted_count=1,
            category_coverage=["infrastructure-and-ops"],
            subcategory_coverage=["containers-and-orchestration"],
            gate_1_tool_surface_cohesion=True,
            gate_1_evidence="Local docker CLI commands",
            gate_1_status=EvidenceStatus.VERIFIED_INSPECTED,
            gate_2_shared_primitives=False,
            gate_2_evidence="None (isolated CLI flags, no shared platform state or secrets)",
            gate_2_status=EvidenceStatus.UNSUPPORTED,
            gate_3_critical_mass=False,
            gate_4_coordinated_lifecycle=False,
            gate_4_evidence="None (isolated container utility)",
            gate_4_status=EvidenceStatus.UNSUPPORTED,
            expected_tier=FamilyTier.DISQUALIFIED_SPRAWL,
            manual_review_paths=[],
            uncertain_cases_or_boundary_notes="Isolated single capability failing Gates 2, 3, 4. Retained as independent domain capability.",
        ),
    }

    @classmethod
    def validate_record_integrity(cls, record: FamilyQualificationRecord) -> None:
        """
        Validate that a candidate's qualification record is independently auditable and grounded in source evidence:
        1. Member count matches len(source_paths) (unless 0 for disqualified sprawl without library members).
        2. duplicate_adjusted_count satisfies 0 <= duplicate_adjusted_count <= candidate_membership_count.
        3. Category coverage matches categories extracted from source_paths.
        4. Gate 3 critical mass matches quantitative evaluation derived from source_paths.
        5. Qualitative gates (1, 2, 4) have concrete non-empty evidence strings and valid evidence statuses.
        6. Authoritative tiers (Tier 1 Hub, Tier 1 Meta, Tier 2 Logical) cannot be asserted on ASSUMPTION_PROVISIONAL,
           UNSUPPORTED, or unresolved manual_review_paths.
        7. Evaluated tier from gates matches expected_tier (or PENDING_ADJUDICATION if uncertain).
        """
        # 1. Member count vs source_paths
        if len(record.source_paths) != record.candidate_membership_count:
            raise FamilyEligibilityError(
                f"Member count mismatch for candidate '{record.family_slug}': record claims "
                f"{record.candidate_membership_count} but provided {len(record.source_paths)} source paths."
            )
        if record.candidate_membership_count > 0:
            if not (1 <= record.duplicate_adjusted_count <= record.candidate_membership_count):
                raise FamilyEligibilityError(
                    f"Invalid duplicate_adjusted_count {record.duplicate_adjusted_count} for candidate '{record.family_slug}'. "
                    f"Must be between 1 and {record.candidate_membership_count}."
                )

        # 2. Category coverage vs derived categories from source_paths
        derived_categories = set()
        for p in record.source_paths:
            parts = p.strip("/").split("/")
            if len(parts) >= 2 and parts[0] == "library":
                derived_categories.add(parts[1])
            elif len(parts) >= 1:
                derived_categories.add(parts[0])

        if set(record.category_coverage) != derived_categories:
            raise FamilyEligibilityError(
                f"Category coverage mismatch for candidate '{record.family_slug}': record claims "
                f"{sorted(record.category_coverage)} but source paths span {sorted(derived_categories)}."
            )

        # 3. Gate 3 critical mass validation derived directly from source records
        cats_for_gate3 = (
            record.distinct_category_coverage
            if record.distinct_category_coverage is not None
            else record.category_coverage
        )
        cat_count = len(cats_for_gate3)
        dup_count = record.duplicate_adjusted_count

        if record.is_internal_meta:
            derived_gate_3 = dup_count >= 5
        else:
            derived_gate_3 = (
                (dup_count >= 3 and cat_count >= 2)
                or (dup_count >= 5 and cat_count >= 1)
            )

        if record.gate_3_critical_mass != derived_gate_3:
            raise FamilyEligibilityError(
                f"Contradictory Gate 3 assertion for candidate '{record.family_slug}': record claims "
                f"{record.gate_3_critical_mass} but source paths and duplicate-adjusted count evaluate to "
                f"{derived_gate_3} (count={dup_count}, categories={cat_count})."
            )

        # 4. Qualitative gates non-empty evidence and status validation
        if record.gate_1_tool_surface_cohesion:
            if not record.gate_1_evidence or not record.gate_1_evidence.strip():
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' asserts Gate 1 (Tool Surface) but provides empty evidence."
                )
            if record.gate_1_status == EvidenceStatus.UNSUPPORTED:
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' asserts Gate 1 (Tool Surface) but evidence status is UNSUPPORTED."
                )

        if record.gate_2_shared_primitives:
            if not record.gate_2_evidence or not record.gate_2_evidence.strip():
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' asserts Gate 2 (Shared Primitives) but provides empty evidence."
                )
            if record.gate_2_status == EvidenceStatus.UNSUPPORTED:
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' asserts Gate 2 (Shared Primitives) but evidence status is UNSUPPORTED."
                )

        if record.gate_4_coordinated_lifecycle:
            if not record.gate_4_evidence or not record.gate_4_evidence.strip():
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' asserts Gate 4 (Coordinated Lifecycle) but provides empty evidence."
                )
            if record.gate_4_status == EvidenceStatus.UNSUPPORTED:
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' asserts Gate 4 (Coordinated Lifecycle) but evidence status is UNSUPPORTED."
                )

        # 5. Authoritative tier requirements vs. Provisional assumptions / Manual reviews
        is_authoritative = record.expected_tier in (
            FamilyTier.TIER_1_PLATFORM_HUB,
            FamilyTier.TIER_1_META_FAMILY,
            FamilyTier.TIER_2_LOGICAL_FAMILY,
        )
        if is_authoritative:
            asserted_statuses = []
            if record.gate_1_tool_surface_cohesion:
                asserted_statuses.append(("Gate 1", record.gate_1_status))
            if record.gate_2_shared_primitives:
                asserted_statuses.append(("Gate 2", record.gate_2_status))
            if record.gate_4_coordinated_lifecycle:
                asserted_statuses.append(("Gate 4", record.gate_4_status))

            for gate_name, status in asserted_statuses:
                if status in (EvidenceStatus.ASSUMPTION_PROVISIONAL, EvidenceStatus.UNSUPPORTED):
                    raise FamilyEligibilityError(
                        f"Authoritative tier '{record.expected_tier.value}' for candidate '{record.family_slug}' "
                        f"cannot be asserted on provisional assumptions or unsupported evidence ({gate_name} status: {status.value}). "
                        "Candidate must be designated PENDING_ADJUDICATION until verified."
                    )

            if record.manual_review_paths and len(record.manual_review_paths) / max(len(record.source_paths), 1) >= 0.5:
                raise FamilyEligibilityError(
                    f"Candidate '{record.family_slug}' has {len(record.manual_review_paths)} of "
                    f"{len(record.source_paths)} packages under manual_review and cannot claim an authoritative tier. "
                    "Must be designated PENDING_ADJUDICATION."
                )

        # 6. Evaluated tier consistency check
        if record.expected_tier == FamilyTier.PENDING_ADJUDICATION:
            return

        evaluated_tier, _ = cls.evaluate(
            family_slug=record.family_slug,
            member_count=record.duplicate_adjusted_count,
            categories_spanned=cat_count,
            has_tool_surface=record.gate_1_tool_surface_cohesion,
            has_shared_primitives=record.gate_2_shared_primitives,
            has_coordinated_lifecycle=record.gate_4_coordinated_lifecycle,
            is_internal_meta=record.is_internal_meta,
        )

        if evaluated_tier != record.expected_tier:
            raise FamilyEligibilityError(
                f"Contradictory tier assignment for candidate '{record.family_slug}': evaluator yielded "
                f"'{evaluated_tier.value}' but record expected '{record.expected_tier.value}'."
            )

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
        elif tier in (FamilyTier.TIER_2_LOGICAL_FAMILY, FamilyTier.PENDING_ADJUDICATION):
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
        cls.validate_record_integrity(record)

        if record.expected_tier == FamilyTier.PENDING_ADJUDICATION:
            gate = FamilyQualificationGate(
                gate_1_tool_surface_cohesion=record.gate_1_tool_surface_cohesion,
                gate_2_shared_primitives=record.gate_2_shared_primitives,
                gate_3_critical_mass=record.gate_3_critical_mass,
                gate_4_coordinated_lifecycle=record.gate_4_coordinated_lifecycle,
                details={
                    "slug": slug,
                    "member_count": record.duplicate_adjusted_count,
                    "categories_spanned": len(record.distinct_category_coverage or record.category_coverage),
                    "is_internal_meta": record.is_internal_meta,
                    "pending_adjudication": True,
                    "manual_review_count": len(record.manual_review_paths),
                },
            )
            return FamilyTier.PENDING_ADJUDICATION, gate, record

        cats_spanned = len(record.distinct_category_coverage if record.distinct_category_coverage is not None else record.category_coverage)
        tier, gate = cls.evaluate(
            family_slug=record.family_slug,
            member_count=record.duplicate_adjusted_count,
            categories_spanned=cats_spanned,
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
