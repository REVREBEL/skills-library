"""
Canonical Semantic Object Model for the REVREBEL Agent Skills Library.

Implements the formal first-class object types, path-independent canonical identities,
directed relationship graphs, and architectural invariant validation defined under REV-127.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class CanonicalIdentityError(ValueError):
    """Raised when a canonical identity violates specification rules."""
    pass


class InvariantViolationError(ValueError):
    """Raised when the object model graph violates architectural invariants."""
    pass


@dataclass(frozen=True)
class CanonicalIdentity:
    """
    Path-independent, scoped canonical identifier conforming to ADR-001.
    Syntax: <scope>:<slug> or urn:skill:<scope>:<slug>
    """
    scope: str
    slug: str

    SCOPE_REGEX = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")
    SLUG_REGEX = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")
    URN_PREFIX = "urn:skill:"

    def __post_init__(self):
        if not self.scope or not self.slug:
            raise CanonicalIdentityError("Canonical identity components (scope, slug) cannot be empty.")

        # Invariant: No path separators or file extensions permitted
        for part, name in [(self.scope, "scope"), (self.slug, "slug")]:
            if "/" in part or "\\" in part:
                raise CanonicalIdentityError(
                    f"Canonical identity {name} '{part}' must not contain path separators ('/' or '\\')."
                )
            if any(part.endswith(ext) for ext in [".md", ".json", ".yaml", ".yml", ".txt"]):
                raise CanonicalIdentityError(
                    f"Canonical identity {name} '{part}' must not contain file extensions."
                )

        if not self.SCOPE_REGEX.match(self.scope):
            raise CanonicalIdentityError(
                f"Invalid scope '{self.scope}'. Scope must be lowercase alphanumeric with hyphens."
            )

        if not self.SLUG_REGEX.match(self.slug):
            raise CanonicalIdentityError(
                f"Invalid slug '{self.slug}'. Slug must be lowercase alphanumeric with hyphens."
            )

    @classmethod
    def parse(cls, identifier: str) -> CanonicalIdentity:
        """Parse an identifier string (compact 'scope:slug' or URN 'urn:skill:scope:slug')."""
        if not identifier or not isinstance(identifier, str):
            raise CanonicalIdentityError("Identifier must be a non-empty string.")

        s = identifier.strip()
        if s.startswith(cls.URN_PREFIX):
            s = s[len(cls.URN_PREFIX):]

        if ":" not in s:
            raise CanonicalIdentityError(
                f"Invalid canonical identifier '{identifier}'. Must be formatted as '<scope>:<slug>' or 'urn:skill:<scope>:<slug>'."
            )

        parts = s.split(":")
        if len(parts) != 2:
            raise CanonicalIdentityError(
                f"Invalid canonical identifier '{identifier}'. Expected exactly one colon separator."
            )

        return cls(scope=parts[0], slug=parts[1])

    @property
    def compact(self) -> str:
        """Compact string representation: <scope>:<slug>."""
        return f"{self.scope}:{self.slug}"

    @property
    def urn(self) -> str:
        """Formal URN representation: urn:skill:<scope>:<slug>."""
        return f"{self.URN_PREFIX}{self.scope}:{self.slug}"

    def __str__(self) -> str:
        return self.compact


class ReviewStatus(str, Enum):
    """
    Analytical and governance lifecycle review status.
    Distinguishes review states (such as manual_review) from first-class semantic object types.
    """
    ACTIVE = "active"
    MANUAL_REVIEW = "manual_review"
    DEPRECATED = "deprecated"
    DRAFT = "draft"
    SUNSET = "sunset"


class SkillRole(str, Enum):
    """
    Exactly 10 first-class semantic object types in the object model:
      - 7 Leaf / Functional entities: capability, workflow, primitive, overlay, adapter, alias, reference
      - 3 Structural entities: family, router, generated_artifact

    Note: 'manual_review' is an analytical and governance lifecycle review status
    (represented via ReviewStatus), NOT a runtime object type.
    """
    CAPABILITY = "capability"
    WORKFLOW = "workflow"
    FAMILY = "family"
    PRIMITIVE = "primitive"
    OVERLAY = "overlay"
    ADAPTER = "adapter"
    ALIAS = "alias"
    REFERENCE = "reference"
    ROUTER = "router"
    GENERATED_ARTIFACT = "generated_artifact"

    @classmethod
    def normalize_role(cls, role_str: str) -> SkillRole:
        """Normalize legacy or census role strings to first-class SkillRole."""
        mapping = {
            "capability": cls.CAPABILITY,
            "independent_capability": cls.CAPABILITY,
            "workflow": cls.WORKFLOW,
            "family": cls.FAMILY,
            "primitive": cls.PRIMITIVE,
            "family_primitive": cls.PRIMITIVE,
            "overlay": cls.OVERLAY,
            "adapter": cls.ADAPTER,
            "alias": cls.ALIAS,
            "alias_candidate": cls.ALIAS,
            "reference": cls.REFERENCE,
            "reference_or_support_candidate": cls.REFERENCE,
            "router": cls.ROUTER,
            "generated_artifact": cls.GENERATED_ARTIFACT,
        }
        low = role_str.lower().strip()
        if low not in mapping:
            raise ValueError(f"Unknown or unsupported skill role: '{role_str}'")
        return mapping[low]


class RelationshipType(str, Enum):
    """Directed edge relationship types between objects."""
    COMPOSED_OF = "composed_of"
    EXTENDS = "extends"
    DEPENDS_ON = "depends_on"
    ADAPTS = "adapts"
    ALIASED_TO = "aliased_to"
    BELONGS_TO_FAMILY = "belongs_to_family"
    IMPLEMENTS = "implements"


@dataclass
class Relationship:
    """A directed edge in the semantic object model graph."""
    source_id: str
    target_id: str
    rel_type: RelationshipType
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "rel_type": self.rel_type.value,
            "metadata": self.metadata,
        }


@dataclass
class SkillObject:
    """Base class for all first-class entities in the Semantic Object Model."""
    canonical_id: str
    name: str
    role: SkillRole
    description: str
    domain: str
    physical_path: Optional[str] = None
    version: str = "1.0.0"
    status: Union[ReviewStatus, str] = ReviewStatus.ACTIVE
    tags: List[str] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Validate canonical ID
        self._parsed_id = CanonicalIdentity.parse(self.canonical_id)
        if isinstance(self.status, str):
            try:
                self.status = ReviewStatus(self.status.lower().strip())
            except ValueError:
                pass  # Allow custom status strings if needed

    @property
    def id_object(self) -> CanonicalIdentity:
        return self._parsed_id

    def add_relationship(
        self,
        rel_type: RelationshipType,
        target_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Relationship:
        # Validate target ID format
        CanonicalIdentity.parse(target_id)
        rel = Relationship(
            source_id=self.canonical_id,
            target_id=target_id,
            rel_type=rel_type,
            metadata=metadata or {},
        )
        self.relationships.append(rel)
        return rel

    def to_dict(self) -> Dict[str, Any]:
        status_val = self.status.value if isinstance(self.status, ReviewStatus) else str(self.status)
        d = {
            "canonical_id": self.canonical_id,
            "urn": self.id_object.urn,
            "name": self.name,
            "role": self.role.value,
            "description": self.description,
            "domain": self.domain,
            "physical_path": self.physical_path,
            "version": self.version,
            "status": status_val,
            "tags": self.tags,
            "relationships": [r.to_dict() for r in self.relationships],
            "metadata": self.metadata,
        }
        return d


@dataclass
class CapabilityObject(SkillObject):
    """Atomic, self-contained domain capability."""
    execution_provider: Optional[str] = None  # mcp, bash, python, prompt

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.CAPABILITY
        exec_provider = kwargs.pop("execution_provider", None)
        super().__init__(**kwargs)
        self.execution_provider = exec_provider

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["execution_provider"] = self.execution_provider
        return d


@dataclass
class WorkflowObject(SkillObject):
    """Multi-phase orchestration pipeline."""
    steps: List[str] = field(default_factory=list)
    approval_gates: List[str] = field(default_factory=list)

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.WORKFLOW
        steps = kwargs.pop("steps", [])
        gates = kwargs.pop("approval_gates", [])
        super().__init__(**kwargs)
        self.steps = steps
        self.approval_gates = gates
        # Sync composed_of relationships from steps
        for i, step_id in enumerate(self.steps):
            self.add_relationship(
                rel_type=RelationshipType.COMPOSED_OF,
                target_id=step_id,
                metadata={"order": i + 1},
            )

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["steps"] = self.steps
        d["approval_gates"] = self.approval_gates
        return d


@dataclass
class FamilyObject(SkillObject):
    """Logical platform/vendor domain container and namespace."""
    vendor: str = ""
    family_id: str = ""

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.FAMILY
        vendor = kwargs.pop("vendor", "")
        family_id = kwargs.pop("family_id", "")
        super().__init__(**kwargs)
        self.vendor = vendor
        self.family_id = family_id or self.id_object.slug

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["vendor"] = self.vendor
        d["family_id"] = self.family_id
        return d


@dataclass
class PrimitiveObject(SkillObject):
    """Minimal, atomic, reusable building block or configuration fragment."""
    primitive_type: str = "token"  # token, schema, syntax, config_template

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.PRIMITIVE
        p_type = kwargs.pop("primitive_type", "token")
        super().__init__(**kwargs)
        self.primitive_type = p_type

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["primitive_type"] = self.primitive_type
        return d


@dataclass
class OverlayObject(SkillObject):
    """Platform-specific behavioral specialization extending a capability/workflow."""
    target_id: str = ""
    platform: str = ""

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.OVERLAY
        target_id = kwargs.pop("target_id", "")
        platform = kwargs.pop("platform", "")
        super().__init__(**kwargs)
        self.target_id = target_id
        self.platform = platform
        if self.target_id:
            self.add_relationship(RelationshipType.EXTENDS, self.target_id)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["target_id"] = self.target_id
        d["platform"] = self.platform
        return d


@dataclass
class AdapterObject(SkillObject):
    """Pure protocol/transport translation shim."""
    protocol: str = "mcp"  # mcp, rest, graphql, cli
    interface_spec: Optional[str] = None

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.ADAPTER
        proto = kwargs.pop("protocol", "mcp")
        spec = kwargs.pop("interface_spec", None)
        super().__init__(**kwargs)
        self.protocol = proto
        self.interface_spec = spec

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["protocol"] = self.protocol
        d["interface_spec"] = self.interface_spec
        return d


@dataclass
class AliasObject(SkillObject):
    """Non-canonical redirect pointer preserving backward compatibility."""
    target_id: str = ""
    alias_type: str = "compatibility_redirect"

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.ALIAS
        target_id = kwargs.pop("target_id", "")
        a_type = kwargs.pop("alias_type", "compatibility_redirect")
        super().__init__(**kwargs)
        self.target_id = target_id
        self.alias_type = a_type
        if self.target_id:
            self.add_relationship(RelationshipType.ALIASED_TO, self.target_id)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["target_id"] = self.target_id
        d["alias_type"] = self.alias_type
        return d


@dataclass
class ReferenceObject(SkillObject):
    """Passive informational cheatsheet, style manual, or rubric."""
    reference_format: str = "cheatsheet"  # cheatsheet, styleguide, rubric, syntax_guide

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.REFERENCE
        ref_fmt = kwargs.pop("reference_format", "cheatsheet")
        super().__init__(**kwargs)
        self.reference_format = ref_fmt

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["reference_format"] = self.reference_format
        return d


@dataclass
class RouterObject(SkillObject):
    """Hierarchical navigational routing node."""
    route_level: str = "category"  # category, subcategory
    managed_skills: List[str] = field(default_factory=list)

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.ROUTER
        level = kwargs.pop("route_level", "category")
        managed = kwargs.pop("managed_skills", [])
        super().__init__(**kwargs)
        self.route_level = level
        self.managed_skills = managed

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["route_level"] = self.route_level
        d["managed_skills"] = self.managed_skills
        return d


@dataclass
class GeneratedArtifactObject(SkillObject):
    """Deterministic build or runtime projection derived from canonical skills."""
    artifact_type: str = "manifest"  # manifest, symlink_tree, git_branch, index
    source_commit: str = ""

    def __init__(self, **kwargs):
        kwargs["role"] = SkillRole.GENERATED_ARTIFACT
        art_type = kwargs.pop("artifact_type", "manifest")
        commit = kwargs.pop("source_commit", "")
        super().__init__(**kwargs)
        self.artifact_type = art_type
        self.source_commit = commit

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["artifact_type"] = self.artifact_type
        d["source_commit"] = self.source_commit
        return d


class ObjectGraph:
    """
    In-memory graph of semantic objects, relationships, and invariants.
    """

    def __init__(self):
        self.objects: Dict[str, SkillObject] = {}
        self.relationships: List[Relationship] = []

    def add_object(self, obj: SkillObject) -> None:
        """Register a skill object. Enforces single canonical owner invariant."""
        cid = obj.canonical_id
        if cid in self.objects:
            raise InvariantViolationError(
                f"Invariant 2 Violation (Single Canonical Owner): Duplicate canonical_id '{cid}' already registered."
            )
        self.objects[cid] = obj
        for rel in obj.relationships:
            self.relationships.append(rel)

    def get_object(self, canonical_id: str) -> Optional[SkillObject]:
        return self.objects.get(canonical_id)

    def resolve_alias(self, identifier: str) -> Tuple[SkillObject, List[str]]:
        """
        Resolve an identifier through alias pointers to the canonical object.
        Enforces single-hop invariant. Returns (canonical_object, hops).
        """
        obj = self.get_object(identifier)
        if not obj:
            raise KeyError(f"Object '{identifier}' not found in graph.")

        if obj.role != SkillRole.ALIAS:
            return obj, [identifier]

        alias_obj: AliasObject = obj  # type: ignore
        target_id = alias_obj.target_id
        if not target_id:
            raise InvariantViolationError(f"Alias '{identifier}' has no target_id.")

        target_obj = self.get_object(target_id)
        if not target_obj:
            raise InvariantViolationError(
                f"Alias '{identifier}' points to non-existent target '{target_id}'."
            )

        if target_obj.role == SkillRole.ALIAS:
            raise InvariantViolationError(
                f"Invariant 3 Violation (Single-Hop Alias): Alias '{identifier}' points to another alias '{target_id}' (chaining forbidden)."
            )

        return target_obj, [identifier, target_id]

    def validate_invariants(self) -> List[str]:
        """
        Validate architectural invariants across the registered graph.
        
        Distinguishes between:
          - Foundational Invariants (REV-127 core contracts):
              * Invariant 1: Directed Acyclic Graph (DAG) for composition and dependencies
              * Invariant 2: Single Canonical Owner (unique canonical_id)
              * Invariant 3: Single-Hop Alias Resolution (no multi-hop alias chains)
              * Invariant 6: Path-Independent Identity (zero filesystem path syntax in IDs)
          - Provisional Design Guardrails (baseline defaults subject to refinement in REV-128 - REV-130):
              * Invariant 4: Shallow Overlay Specialization (provisional rule against overlay nesting)
              * Invariant 5: Leaf Primitives (provisional rule restricting primitive composition)
        
        Returns empty list if fully valid, or raises InvariantViolationError.
        """
        errors = []

        # 1. Foundational Invariant 3: Single-Hop Aliases & Target Existence
        for cid, obj in self.objects.items():
            if obj.role == SkillRole.ALIAS:
                alias_obj: AliasObject = obj  # type: ignore
                target = self.objects.get(alias_obj.target_id)
                if not target:
                    errors.append(
                        f"Alias '{cid}' references non-existent target '{alias_obj.target_id}'."
                    )
                elif target.role == SkillRole.ALIAS:
                    errors.append(
                        f"Invariant 3 Violation: Alias '{cid}' chains to another alias '{target.canonical_id}'."
                    )

        # 2. Provisional Guardrail 4: Overlay Target Invariants (Depth Limit = 1, must target Capability or Workflow)
        for cid, obj in self.objects.items():
            if obj.role == SkillRole.OVERLAY:
                overlay_obj: OverlayObject = obj  # type: ignore
                target = self.objects.get(overlay_obj.target_id)
                if not target:
                    errors.append(
                        f"Overlay '{cid}' references non-existent target '{overlay_obj.target_id}'."
                    )
                elif target.role == SkillRole.OVERLAY:
                    errors.append(
                        f"Invariant 4 Violation (Provisional): Overlay '{cid}' extends another overlay '{target.canonical_id}'. Overlays cannot extend overlays."
                    )
                elif target.role not in (SkillRole.CAPABILITY, SkillRole.WORKFLOW):
                    errors.append(
                        f"Invariant 4 Violation (Provisional): Overlay '{cid}' targets role '{target.role.value}', must target capability or workflow."
                    )

        # 3. Provisional Guardrail 5: Primitive Purity Invariants (Primitives cannot compose workflows)
        for cid, obj in self.objects.items():
            if obj.role == SkillRole.PRIMITIVE:
                for rel in obj.relationships:
                    if rel.rel_type == RelationshipType.COMPOSED_OF:
                        errors.append(
                            f"Invariant 5 Violation (Provisional): Primitive '{cid}' declares 'composed_of' relationship. Primitives cannot compose workflows."
                        )

        # 4. Foundational Invariant 1: DAG Acyclicity for Composition and Dependencies
        cycle_error = self._check_composition_and_dependency_cycles()
        if cycle_error:
            errors.append(f"Invariant 1 Violation (DAG Acyclicity): {cycle_error}")

        if errors:
            raise InvariantViolationError(
                f"Semantic Object Model invariant violations detected ({len(errors)}):\n"
                + "\n".join(f"  • {e}" for e in errors)
            )

        return []

    def _check_composition_and_dependency_cycles(self) -> Optional[str]:
        """
        Detect cycles in the directed graph formed by COMPOSED_OF and DEPENDS_ON edges.
        Uses depth-first search with 3-color marking (0=white, 1=gray, 2=black).
        """
        # Build adjacency list for composition and dependency edges
        adj: Dict[str, List[str]] = {cid: [] for cid in self.objects}
        for rel in self.relationships:
            if rel.rel_type in (RelationshipType.COMPOSED_OF, RelationshipType.DEPENDS_ON):
                if rel.source_id in adj and rel.target_id in self.objects:
                    adj[rel.source_id].append(rel.target_id)

        color: Dict[str, int] = {node: 0 for node in adj}
        path: List[str] = []

        def dfs(node: str) -> Optional[List[str]]:
            color[node] = 1  # Gray (currently exploring)
            path.append(node)

            for neighbor in adj.get(node, []):
                if color[neighbor] == 1:
                    # Found cycle
                    cycle_start_idx = path.index(neighbor)
                    return path[cycle_start_idx:] + [neighbor]
                elif color[neighbor] == 0:
                    result = dfs(neighbor)
                    if result:
                        return result

            path.pop()
            color[node] = 2  # Black (fully explored)
            return None

        for node in adj:
            if color[node] == 0:
                cycle = dfs(node)
                if cycle:
                    return f"Circular relationship detected: {' -> '.join(cycle)}"

        return None

    def export_catalog(self) -> Dict[str, Any]:
        """Export entire graph to serialized dictionary."""
        return {
            "version": "1.0.0",
            "total_objects": len(self.objects),
            "objects": {cid: obj.to_dict() for cid, obj in sorted(self.objects.items())},
            "relationships": [r.to_dict() for r in self.relationships],
        }
