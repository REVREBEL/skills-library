"""
Physical Storage Plane Specification, Validation, and Duplicate Resolution Engine.
Governs the physical layout contracts established under REV-128 and ADR-002:
  1. Platform Hubs (library/tools-and-platforms/<family-slug>/)
  2. Domain-Centric Trees (library/<category-slug>/<subcategory-slug>/)
  3. Meta Infrastructure (library/meta-and-agent-skills/)
  4. Physical Overlay and Adapter Placement Contracts
  5. Resolution and Migration Architecture for Duplicate Pairs
"""

import os
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from skill_library.object_model import (
    CanonicalIdentity,
    CanonicalIdentityError,
    InvariantViolationError,
    SkillObject,
    SkillRole,
)


class PhysicalPlane(str, Enum):
    """The standardized physical storage planes under library/."""
    PLATFORM_HUB = "platform_hub"              # library/tools-and-platforms/<family>/...
    DOMAIN_TREE = "domain_tree"                # library/<category>/<subcategory>/...
    META_INFRASTRUCTURE = "meta_infrastructure"# library/meta-and-agent-skills/...
    LEGACY_ROOT = "legacy_root"                # library/github-operations, skills-create-manage-update


class LayoutValidationError(Exception):
    """Raised when a physical path or directory layout violates architectural invariants."""
    pass


@dataclass(frozen=True)
class ParsedPhysicalPath:
    """Structured breakdown of a canonical library physical path."""
    raw_path: str
    normalized_path: str
    plane: PhysicalPlane
    top_level: str
    sub_level: Optional[str] = None
    component_type: Optional[str] = None  # "overlays", "adapters", "primitives", or None
    leaf_name: str = ""
    is_legacy: bool = False


class PhysicalPathContract:
    """
    Validates, normalizes, and inspects filesystem paths for the skills library.
    Enforces ADR-002 directory depth, naming standards, and placement constraints.
    """

    ALLOWED_SEGMENT_REGEX = re.compile(r"^[a-z0-9-]+$")
    PLATFORM_HUB_ROOT = "tools-and-platforms"
    META_ROOT = "meta-and-agent-skills"

    LEGACY_ROOTS = {
        "github-operations",
        "skills-create-manage-update",
    }

    CANONICAL_CATEGORIES = {
        "business-and-operations",
        "content-and-documentation",
        "data-and-ai",
        "design-and-experience",
        "development",
        "infrastructure-and-ops",
        "marketing-and-seo",
        "meta-and-agent-skills",
        "quality-and-security",
        "workflow-and-automation",
    }

    @classmethod
    def normalize(cls, path_str: str) -> str:
        """Normalize a path to a relative POSIX path under library/."""
        if not path_str or not isinstance(path_str, str):
            raise LayoutValidationError("Physical path must be a non-empty string.")

        # Rejects Windows drive letters, backslashes, or path traversals
        if "\\" in path_str:
            raise LayoutValidationError(f"Invalid physical path '{path_str}'. Backslashes are forbidden.")
        if ".." in path_str.split("/"):
            raise LayoutValidationError(f"Invalid physical path '{path_str}'. Path traversal '..' is forbidden.")

        clean = path_str.strip("/")
        if clean.startswith("library/"):
            clean = clean[len("library/"):]

        return clean

    @classmethod
    def parse(cls, path_str: str) -> ParsedPhysicalPath:
        """Parse and validate a library relative path."""
        norm = cls.normalize(path_str)
        segments = norm.split("/")

        # Check for empty segments or invalid characters
        for seg in segments:
            if not seg:
                raise LayoutValidationError(f"Invalid physical path '{path_str}'. Contains empty segment.")
            if not cls.ALLOWED_SEGMENT_REGEX.match(seg):
                raise LayoutValidationError(
                    f"Invalid path segment '{seg}' in '{path_str}'. Must be lowercase alphanumeric with hyphens."
                )

        # Enforce overlay nesting limit: at most one 'overlays' segment
        overlay_count = segments.count("overlays")
        if overlay_count > 1:
            raise LayoutValidationError(
                f"Invariant Violation (Overlay Nesting): Path '{path_str}' contains {overlay_count} 'overlays' segments. Nested overlays are forbidden."
            )

        top = segments[0]

        # 1. Legacy roots
        if top in cls.LEGACY_ROOTS:
            leaf = segments[-1]
            return ParsedPhysicalPath(
                raw_path=path_str,
                normalized_path=norm,
                plane=PhysicalPlane.LEGACY_ROOT,
                top_level=top,
                sub_level=None,
                component_type=None,
                leaf_name=leaf,
                is_legacy=True,
            )

        # 2. Platform Hubs
        if top == cls.PLATFORM_HUB_ROOT:
            if len(segments) < 3:
                raise LayoutValidationError(
                    f"Platform hub path '{path_str}' too shallow. Expected 'tools-and-platforms/<family>/<slug>' or 'tools-and-platforms/<family>/<component>/<slug>'."
                )
            family = segments[1]
            if len(segments) == 3:
                # tools-and-platforms/<family>/<skill>
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.PLATFORM_HUB,
                    top_level=family,
                    sub_level=None,
                    component_type=None,
                    leaf_name=segments[2],
                    is_legacy=False,
                )
            elif len(segments) == 4:
                # tools-and-platforms/<family>/<component>/<skill>
                comp = segments[2]
                if comp not in ("primitives", "adapters", "overlays"):
                    raise LayoutValidationError(
                        f"Invalid platform component '{comp}' in '{path_str}'. Allowed components: 'primitives', 'adapters', 'overlays'."
                    )
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.PLATFORM_HUB,
                    top_level=family,
                    sub_level=None,
                    component_type=comp,
                    leaf_name=segments[3],
                    is_legacy=False,
                )
            else:
                raise LayoutValidationError(
                    f"Platform hub path '{path_str}' exceeds maximum allowed directory depth (4)."
                )

        # 3. Meta Infrastructure
        if top == cls.META_ROOT:
            if len(segments) < 2:
                raise LayoutValidationError(f"Meta infrastructure path '{path_str}' too shallow.")
            sub = segments[1]
            if len(segments) == 2:
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.META_INFRASTRUCTURE,
                    top_level=top,
                    sub_level=sub,
                    component_type=None,
                    leaf_name=sub,
                    is_legacy=False,
                )
            elif len(segments) == 3:
                comp = "adapters" if sub == "adapters" else None
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.META_INFRASTRUCTURE,
                    top_level=top,
                    sub_level=sub,
                    component_type=comp,
                    leaf_name=segments[2],
                    is_legacy=False,
                )
            elif len(segments) == 4 and segments[2] in ("overlays", "adapters", "primitives"):
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.META_INFRASTRUCTURE,
                    top_level=top,
                    sub_level=sub,
                    component_type=segments[2],
                    leaf_name=segments[3],
                    is_legacy=False,
                )
            else:
                raise LayoutValidationError(
                    f"Meta infrastructure path '{path_str}' exceeds maximum allowed directory depth."
                )

        # 4. Domain-Centric Functional Trees
        if top in cls.CANONICAL_CATEGORIES:
            if len(segments) < 3:
                raise LayoutValidationError(
                    f"Domain path '{path_str}' too shallow. Expected '<category>/<subcategory>/<skill>'."
                )
            subcat = segments[1]
            if len(segments) == 3:
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.DOMAIN_TREE,
                    top_level=top,
                    sub_level=subcat,
                    component_type=None,
                    leaf_name=segments[2],
                    is_legacy=False,
                )
            elif len(segments) == 4 and segments[2] == "overlays":
                return ParsedPhysicalPath(
                    raw_path=path_str,
                    normalized_path=norm,
                    plane=PhysicalPlane.DOMAIN_TREE,
                    top_level=top,
                    sub_level=subcat,
                    component_type="overlays",
                    leaf_name=segments[3],
                    is_legacy=False,
                )
            else:
                raise LayoutValidationError(
                    f"Domain path '{path_str}' exceeds maximum allowed directory depth or contains invalid nesting."
                )

        raise LayoutValidationError(
            f"Unrecognized top-level category '{top}' in path '{path_str}'. Must be one of canonical categories, 'tools-and-platforms', or recognized legacy root."
        )


@dataclass(frozen=True)
class DuplicateCandidateHypothesis:
    """
    Defines a direction-neutral evaluation hypothesis for a candidate duplicate leaf name.
    
    In accordance with REV-128 and REV-126/150 census principles, candidate pairs remain
    unresolved until source-backed semantic reviews are adjudicated in downstream work orders.
    No executable migration instructions or irreversible canonical-identity changes are made.
    """
    leaf_name: str
    legacy_main_path: str
    candidate_platform_path: str
    candidate_canonical_id: str
    hypothesis_type: str  # e.g., "platform_consolidation_hypothesis", "dual_retention_hypothesis", "rename_collision_hypothesis"
    evaluation_notes: str

    @property
    def target_physical_home(self) -> str:
        """Backward-compatible alias for candidate_platform_path."""
        return self.candidate_platform_path

    @property
    def canonical_id(self) -> str:
        """Backward-compatible alias for candidate_canonical_id."""
        return self.candidate_canonical_id

    @property
    def resolution_type(self) -> str:
        """Backward-compatible alias for hypothesis_type."""
        return self.hypothesis_type

    @property
    def description(self) -> str:
        """Backward-compatible alias for evaluation_notes."""
        return self.evaluation_notes


# Backward-compatible type alias
DuplicatePairResolution = DuplicateCandidateHypothesis


class DuplicateCandidateRegistry:
    """
    Registry defining direction-neutral evaluation hypotheses for the 15 GitHub duplicate
    pairs identified during the REV-126/150 census.

    Architectural Boundary (REV-128 vs REV-129/130):
      - REV-128 models candidate filesystem paths and hypothesis types without executing migrations.
      - Final asset-level adjudications are deferred to downstream work orders upon source-backed reviews.
    """

    CANDIDATE_HYPOTHESES: Dict[str, DuplicateCandidateHypothesis] = {
        "actions-debugger": DuplicateCandidateHypothesis(
            leaf_name="actions-debugger",
            legacy_main_path="infrastructure-and-ops/ci-cd/actions-debugger",
            candidate_platform_path="tools-and-platforms/github/actions-debugger",
            candidate_canonical_id="github:actions-debugger",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: GitHub Actions diagnostics workflow consolidated to platform hub. Hypothesis B: Retain in CI/CD if generalized across runners.",
        ),
        "advanced-workflows": DuplicateCandidateHypothesis(
            leaf_name="advanced-workflows",
            legacy_main_path="workflow-and-automation/git-and-vcs/advanced-workflows",
            candidate_platform_path="tools-and-platforms/github/advanced-workflows",
            candidate_canonical_id="github:advanced-workflows",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Advanced Git workflow consolidated to platform hub. Hypothesis B: Retain in git-and-vcs with platform overlay.",
        ),
        "commit": DuplicateCandidateHypothesis(
            leaf_name="commit",
            legacy_main_path="development/systems/commit",
            candidate_platform_path="tools-and-platforms/github/commit",
            candidate_canonical_id="github:commit",
            hypothesis_type="dual_retention_hypothesis",
            evaluation_notes="Candidate Hypothesis A (Dual-Retention): Distinct functional semantics between github:commit (PR/review commit flow) and development:commit (generic Git staging). Hypothesis B: Merge with adapter.",
        ),
        "create-branch": DuplicateCandidateHypothesis(
            leaf_name="create-branch",
            legacy_main_path="development/systems/create-branch",
            candidate_platform_path="tools-and-platforms/github/create-branch",
            candidate_canonical_id="github:create-branch",
            hypothesis_type="dual_retention_hypothesis",
            evaluation_notes="Candidate Hypothesis A (Dual-Retention): Distinct functional semantics between github:create-branch (repo policy/issue linking) and development:create-branch (generic VCS branching). Hypothesis B: Single branch workflow.",
        ),
        "create-issue-gate": DuplicateCandidateHypothesis(
            leaf_name="create-issue-gate",
            legacy_main_path="business-and-operations/product-management/create-issue-gate",
            candidate_platform_path="tools-and-platforms/github/create-issue-gate",
            candidate_canonical_id="github:create-issue-gate",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Issue-first gate consolidated to platform hub. Hypothesis B: Retain in product-management with adapter.",
        ),
        "feature-tracking": DuplicateCandidateHypothesis(
            leaf_name="feature-tracking",
            legacy_main_path="business-and-operations/product-management/feature-tracking",
            candidate_platform_path="tools-and-platforms/github/feature-tracking",
            candidate_canonical_id="github:feature-tracking",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Repo-native issue tracking workflow consolidated to platform hub. Hypothesis B: Retain in product-management as generic feature memory.",
        ),
        "github": DuplicateCandidateHypothesis(
            leaf_name="github",
            legacy_main_path="development/fullstack/github",
            candidate_platform_path="tools-and-platforms/github/general-operations",
            candidate_canonical_id="github:general-operations",
            hypothesis_type="rename_collision_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Rename leaf to general-operations to prevent package root collision. Hypothesis B: Decompose across platform hub components.",
        ),
        "hooks-automation": DuplicateCandidateHypothesis(
            leaf_name="hooks-automation",
            legacy_main_path="infrastructure-and-ops/ci-cd/hooks-automation",
            candidate_platform_path="tools-and-platforms/github/hooks-automation",
            candidate_canonical_id="github:hooks-automation",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Git hooks automation consolidated to platform hub. Hypothesis B: Retain in CI/CD as generic hooks orchestrator.",
        ),
        "issue-creator": DuplicateCandidateHypothesis(
            leaf_name="issue-creator",
            legacy_main_path="business-and-operations/product-management/issue-creator",
            candidate_platform_path="tools-and-platforms/github/issue-creator",
            candidate_canonical_id="github:issue-creator",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Issue creator consolidated to platform hub. Hypothesis B: Retain in product-management with issue tracker adapter.",
        ),
        "pr-merge-champion": DuplicateCandidateHypothesis(
            leaf_name="pr-merge-champion",
            legacy_main_path="development/fullstack/pr-merge-champion",
            candidate_platform_path="tools-and-platforms/github/pr-merge-champion",
            candidate_canonical_id="github:pr-merge-champion",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Merge gate workflow consolidated to platform hub. Hypothesis B: Retain in development/fullstack as generic code review champion.",
        ),
        "pr-review": DuplicateCandidateHypothesis(
            leaf_name="pr-review",
            legacy_main_path="quality-and-security/code-review/pr-review",
            candidate_platform_path="tools-and-platforms/github/pr-review",
            candidate_canonical_id="github:pr-review",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Code review workflow consolidated to platform hub. Hypothesis B: Retain in quality-and-security as core review capability.",
        ),
        "pr-writer": DuplicateCandidateHypothesis(
            leaf_name="pr-writer",
            legacy_main_path="development/fullstack/pr-writer",
            candidate_platform_path="tools-and-platforms/github/pr-writer",
            candidate_canonical_id="github:pr-writer",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: PR writer workflow consolidated to platform hub. Hypothesis B: Retain in development as generic changeset documentation generator.",
        ),
        "presence": DuplicateCandidateHypothesis(
            leaf_name="presence",
            legacy_main_path="marketing-and-seo/cro/presence",
            candidate_platform_path="tools-and-platforms/github/presence",
            candidate_canonical_id="github:presence",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Discoverability/README workflow consolidated to platform hub. Hypothesis B: Retain in marketing-and-seo as digital footprint optimization.",
        ),
        "review-requests": DuplicateCandidateHypothesis(
            leaf_name="review-requests",
            legacy_main_path="development/fullstack/review-requests",
            candidate_platform_path="tools-and-platforms/github/review-requests",
            candidate_canonical_id="github:review-requests",
            hypothesis_type="platform_consolidation_hypothesis",
            evaluation_notes="Candidate Hypothesis A: Review request ranking consolidated to platform hub. Hypothesis B: Retain in development as peer review routing workflow.",
        ),
        "security-review": DuplicateCandidateHypothesis(
            leaf_name="security-review",
            legacy_main_path="quality-and-security/security/security-review",
            candidate_platform_path="tools-and-platforms/github/security-review",
            candidate_canonical_id="github:security-review",
            hypothesis_type="dual_retention_hypothesis",
            evaluation_notes="Candidate Hypothesis A (Dual-Retention): Distinct functional semantics between github:security-review (Actions workflow security audit) and quality-and-security:security-review (general static code security). Hypothesis B: Unified security audit.",
        ),
    }

    # Backward-compatible dictionary reference
    RESOLUTIONS = CANDIDATE_HYPOTHESES

    @classmethod
    def is_candidate_leaf(cls, leaf_name: str) -> bool:
        """Check if leaf name is one of the 15 GitHub duplicate collision candidate pairs."""
        return leaf_name in cls.CANDIDATE_HYPOTHESES

    @classmethod
    def get_candidate_hypothesis(cls, leaf_name: str) -> Optional[DuplicateCandidateHypothesis]:
        """Fetch the evaluation hypothesis record for a candidate duplicate leaf name."""
        return cls.CANDIDATE_HYPOTHESES.get(leaf_name)

    @classmethod
    def get_all_candidates(cls) -> List[DuplicateCandidateHypothesis]:
        """Return all 15 candidate duplicate evaluation records."""
        return list(cls.CANDIDATE_HYPOTHESES.values())

    # Backward-compatible helper methods
    @classmethod
    def is_duplicate_leaf(cls, leaf_name: str) -> bool:
        return cls.is_candidate_leaf(leaf_name)

    @classmethod
    def get_resolution(cls, leaf_name: str) -> Optional[DuplicateCandidateHypothesis]:
        return cls.get_candidate_hypothesis(leaf_name)

    @classmethod
    def get_all_pairs(cls) -> List[DuplicateCandidateHypothesis]:
        return cls.get_all_candidates()


# Backward-compatible class alias
DuplicateResolutionRegistry = DuplicateCandidateRegistry


class PhysicalLayoutValidator:
    """
    Validates physical storage locations of SkillObjects against the provisional layout rules
    of ADR-002 and the Semantic Object Model.

    Architectural Boundary Warning:
      - Physical path structure, overlay directory conventions, and adapter placement rules are governed by REV-128.
      - Platform family qualification thresholds and provider interfaces are governed by REV-129.
      - Registry manifest schemas and dynamic alias resolution are governed by REV-130.
      This validator enforces provisional structural layout conformance without preempting downstream work orders.
    """

    @classmethod
    def validate_object_placement(cls, obj: SkillObject) -> None:
        """
        Validate that a SkillObject's physical_path conforms to its role and family affiliations.
        """
        if not obj.physical_path:
            # Physical path is optional in conceptual models, but if set, must conform.
            return

        parsed = PhysicalPathContract.parse(obj.physical_path)

        # 1. Overlay Placement Contract
        if obj.role == SkillRole.OVERLAY:
            if parsed.component_type != "overlays":
                raise LayoutValidationError(
                    f"Invariant Violation (Overlay Placement): Overlay '{obj.canonical_id}' at '{obj.physical_path}' must reside in an 'overlays/' directory (e.g. 'tools-and-platforms/<family>/overlays/<slug>' or '<category>/<subcategory>/overlays/<slug>')."
                )

        # 2. Adapter Placement Contract
        if obj.role == SkillRole.ADAPTER:
            if parsed.component_type != "adapters" and not parsed.is_legacy:
                raise LayoutValidationError(
                    f"Invariant Violation (Adapter Placement): Adapter '{obj.canonical_id}' at '{obj.physical_path}' must reside in an 'adapters/' directory."
                )

        # 3. Platform Hub Membership Contract
        if parsed.plane == PhysicalPlane.PLATFORM_HUB:
            family_slug = parsed.top_level
            # The object must either have matching scope, belong to the family, or have family in metadata
            has_family_affinity = (
                obj.id_object.scope == family_slug
                or family_slug in obj.families
                or obj.metadata.get("family") == family_slug
            )
            if not has_family_affinity:
                raise LayoutValidationError(
                    f"Invariant Violation (Platform Hub Ownership): Object '{obj.canonical_id}' placed in platform hub '{family_slug}' ('{obj.physical_path}') does not declare affiliation with family '{family_slug}'."
                )

    @classmethod
    def verify_path_independent_relocation(
        cls,
        obj: SkillObject,
        new_physical_path: str,
    ) -> None:
        """
        Simulate a physical relocation and assert that canonical identity is strictly preserved.
        Enforces ADR-001 / ADR-002 path-independent identity stability across file moves.
        """
        original_id = obj.canonical_id
        original_urn = obj.id_object.urn

        # Validate new path syntax
        parsed_new = PhysicalPathContract.parse(new_physical_path)

        # Mutate physical path (mutable metadata)
        obj.physical_path = new_physical_path

        # Assert identity stability
        if obj.canonical_id != original_id:
            raise InvariantViolationError(
                f"Path Independence Violation: Moving object to '{new_physical_path}' altered canonical_id from '{original_id}' to '{obj.canonical_id}'."
            )
        if obj.id_object.urn != original_urn:
            raise InvariantViolationError(
                f"Path Independence Violation: Moving object to '{new_physical_path}' altered URN from '{original_urn}' to '{obj.id_object.urn}'."
            )
