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
class DuplicatePairResolution:
    """Defines the authoritative resolution contract for a duplicate leaf name."""
    leaf_name: str
    legacy_main_path: str
    target_physical_home: str
    canonical_id: str
    resolution_type: str  # "alias_to_platform", "dual_retention", "rename"
    description: str


class DuplicateResolutionRegistry:
    """
    Registry defining the authoritative physical resolution and consolidation
    mapping for the 15 GitHub duplicate pairs discovered in REV-126/150.
    """

    RESOLUTIONS: Dict[str, DuplicatePairResolution] = {
        "actions-debugger": DuplicatePairResolution(
            leaf_name="actions-debugger",
            legacy_main_path="infrastructure-and-ops/ci-cd/actions-debugger",
            target_physical_home="tools-and-platforms/github/actions-debugger",
            canonical_id="github:actions-debugger",
            resolution_type="alias_to_platform",
            description="GitHub Actions diagnostics workflow. Main-tree instance aliased to canonical platform hub.",
        ),
        "advanced-workflows": DuplicatePairResolution(
            leaf_name="advanced-workflows",
            legacy_main_path="workflow-and-automation/git-and-vcs/advanced-workflows",
            target_physical_home="tools-and-platforms/github/advanced-workflows",
            canonical_id="github:advanced-workflows",
            resolution_type="alias_to_platform",
            description="Advanced Git recovery, rebase, and worktrees workflow owned by GitHub platform hub.",
        ),
        "commit": DuplicatePairResolution(
            leaf_name="commit",
            legacy_main_path="development/systems/commit",
            target_physical_home="tools-and-platforms/github/commit",
            canonical_id="github:commit",
            resolution_type="dual_retention",
            description="Dual retention: github:commit owns PR/review commit integration; development:commit owns generic Git staging.",
        ),
        "create-branch": DuplicatePairResolution(
            leaf_name="create-branch",
            legacy_main_path="development/systems/create-branch",
            target_physical_home="tools-and-platforms/github/create-branch",
            canonical_id="github:create-branch",
            resolution_type="dual_retention",
            description="Dual retention: github:create-branch enforces repository issue-branch policy; development:create-branch provides generic VCS branching.",
        ),
        "create-issue-gate": DuplicatePairResolution(
            leaf_name="create-issue-gate",
            legacy_main_path="business-and-operations/product-management/create-issue-gate",
            target_physical_home="tools-and-platforms/github/create-issue-gate",
            canonical_id="github:create-issue-gate",
            resolution_type="alias_to_platform",
            description="Issue-first gate workflow owned by GitHub platform hub. Main-tree instance aliased to canonical.",
        ),
        "feature-tracking": DuplicatePairResolution(
            leaf_name="feature-tracking",
            legacy_main_path="business-and-operations/product-management/feature-tracking",
            target_physical_home="tools-and-platforms/github/feature-tracking",
            canonical_id="github:feature-tracking",
            resolution_type="alias_to_platform",
            description="Repository-native long-lived feature memory workflow owned by GitHub platform hub.",
        ),
        "github": DuplicatePairResolution(
            leaf_name="github",
            legacy_main_path="development/fullstack/github",
            target_physical_home="tools-and-platforms/github/general-operations",
            canonical_id="github:general-operations",
            resolution_type="rename",
            description="Renamed to general-operations to prevent package root collision. Main-tree instance aliased to canonical.",
        ),
        "hooks-automation": DuplicatePairResolution(
            leaf_name="hooks-automation",
            legacy_main_path="infrastructure-and-ops/ci-cd/hooks-automation",
            target_physical_home="tools-and-platforms/github/hooks-automation",
            canonical_id="github:hooks-automation",
            resolution_type="alias_to_platform",
            description="Git hooks automation workflow owned by GitHub platform hub. Main-tree instance aliased to canonical.",
        ),
        "issue-creator": DuplicatePairResolution(
            leaf_name="issue-creator",
            legacy_main_path="business-and-operations/product-management/issue-creator",
            target_physical_home="tools-and-platforms/github/issue-creator",
            canonical_id="github:issue-creator",
            resolution_type="alias_to_platform",
            description="Actionable issue creator workflow owned by GitHub platform hub. Main-tree instance aliased to canonical.",
        ),
        "pr-merge-champion": DuplicatePairResolution(
            leaf_name="pr-merge-champion",
            legacy_main_path="development/fullstack/pr-merge-champion",
            target_physical_home="tools-and-platforms/github/pr-merge-champion",
            canonical_id="github:pr-merge-champion",
            resolution_type="alias_to_platform",
            description="Merge gate verification and queueing workflow owned by GitHub platform hub.",
        ),
        "pr-review": DuplicatePairResolution(
            leaf_name="pr-review",
            legacy_main_path="quality-and-security/code-review/pr-review",
            target_physical_home="tools-and-platforms/github/pr-review",
            canonical_id="github:pr-review",
            resolution_type="alias_to_platform",
            description="Code review and risk assessment workflow owned by GitHub platform hub.",
        ),
        "pr-writer": DuplicatePairResolution(
            leaf_name="pr-writer",
            legacy_main_path="development/fullstack/pr-writer",
            target_physical_home="tools-and-platforms/github/pr-writer",
            canonical_id="github:pr-writer",
            resolution_type="alias_to_platform",
            description="PR title and body generator workflow owned by GitHub platform hub.",
        ),
        "presence": DuplicatePairResolution(
            leaf_name="presence",
            legacy_main_path="marketing-and-seo/cro/presence",
            target_physical_home="tools-and-platforms/github/presence",
            canonical_id="github:presence",
            resolution_type="alias_to_platform",
            description="README and repository discoverability workflow owned by GitHub platform hub.",
        ),
        "review-requests": DuplicatePairResolution(
            leaf_name="review-requests",
            legacy_main_path="development/fullstack/review-requests",
            target_physical_home="tools-and-platforms/github/review-requests",
            canonical_id="github:review-requests",
            resolution_type="alias_to_platform",
            description="PR review request ranking workflow owned by GitHub platform hub.",
        ),
        "security-review": DuplicatePairResolution(
            leaf_name="security-review",
            legacy_main_path="quality-and-security/security/security-review",
            target_physical_home="tools-and-platforms/github/security-review",
            canonical_id="github:security-review",
            resolution_type="dual_retention",
            description="Dual retention: github:security-review owns Actions workflow exploit audit; quality-and-security owns general code security.",
        ),
    }

    @classmethod
    def is_duplicate_leaf(cls, leaf_name: str) -> bool:
        """Check if leaf name is one of the 15 GitHub duplicate pairs."""
        return leaf_name in cls.RESOLUTIONS

    @classmethod
    def get_resolution(cls, leaf_name: str) -> Optional[DuplicatePairResolution]:
        """Fetch the resolution contract for a duplicate leaf name."""
        return cls.RESOLUTIONS.get(leaf_name)

    @classmethod
    def get_all_pairs(cls) -> List[DuplicatePairResolution]:
        """Return all 15 duplicate pair resolution records."""
        return list(cls.RESOLUTIONS.values())


class PhysicalLayoutValidator:
    """
    Validates physical storage locations of SkillObjects against the architectural
    rules of ADR-002 and the Semantic Object Model.
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
