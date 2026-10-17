"""
Universal Catalog Registry, Multi-View Discovery, Alias Resolution,
Transitive Dependency Closure, and Project Materialization Contracts.

Governs the Execution and Discovery Plane established under REV-130 and ADR-004:
  1. Universal Catalog Registry Schema (audit/skills-registry.json v1.0.0)
  2. Multi-View Projections (Functional, Family, Semantic Group, Execution Provider)
  3. Inverted Search Index (audit/search-index.json)
  4. Single-Hop Alias Resolution & Direction-Neutral Duplicate Consolidation (INV-3)
  5. Transitive Dependency Closure, Topological Execution Plans & DAG Invariants (INV-1, INV-8)
  6. Semantic Group Capability Clusters & Group Closure Materialization
  7. Recursive Family Router Generators (Tier 1 Physical Hubs & Tier 2 Logical Routers)
  8. Deterministic Project Materialization with Dependency Completeness (INV-9)
  9. Deterministic Compilation & Zero-Drift Verification (INV-10)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

from skill_library.object_model import (
    AliasObject,
    CanonicalIdentity,
    CanonicalIdentityError,
    CapabilityObject,
    FamilyObject,
    InvariantViolationError,
    ObjectGraph,
    OverlayObject,
    PrimitiveObject,
    Relationship,
    RelationshipType,
    ReviewStatus,
    SkillObject,
    SkillRole,
)


class RegistryError(Exception):
    """Base exception for catalog registry errors."""
    pass


class ProjectionMode(str, Enum):
    """Runtime projection modes defined under ADR-004 Section 9.1."""
    FULL = "full"
    SUBSET = "subset"
    FAMILY = "family"
    SEMANTIC_GROUP = "semantic_group"
    STANDALONE_CLOSURE = "standalone_closure"


@dataclass
class SemanticGroupObject:
    """
    First-class cross-cutting capability cluster defined under ADR-004 Section 7.
    Spans functional domains to combine tools across vendors and domains for cohesive execution.
    """
    group_id: str
    name: str
    description: str = ""
    domain_scope: str = "cross-domain"
    members: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    materialization_policy: str = "transitive_closure"

    GROUP_ID_REGEX = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")

    def __post_init__(self):
        if not self.group_id:
            raise RegistryError("Semantic group_id cannot be empty.")
        if not self.GROUP_ID_REGEX.match(self.group_id):
            raise RegistryError(
                f"Invalid group_id '{self.group_id}'. Must be lowercase alphanumeric with hyphens."
            )
        # Validate member canonical IDs
        for m in self.members:
            CanonicalIdentity.parse(m)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_id": self.group_id,
            "name": self.name,
            "description": self.description,
            "domain_scope": self.domain_scope,
            "members": sorted(self.members),
            "tags": sorted(self.tags),
            "materialization_policy": self.materialization_policy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SemanticGroupObject:
        return cls(
            group_id=data["group_id"],
            name=data["name"],
            description=data.get("description", ""),
            domain_scope=data.get("domain_scope", "cross-domain"),
            members=list(data.get("members", [])),
            tags=list(data.get("tags", [])),
            materialization_policy=data.get("materialization_policy", "transitive_closure"),
        )


@dataclass
class RegistryEntry:
    """
    Compiled registry record for a single skill entity conforming to ADR-004 Section 2.2.
    Decouples the 4 axes:
      1. Identity: canonical_id, urn, name
      2. Semantic Ownership: domain, category, subcategory, owner
      3. Physical Location: physical_path
      4. Family Memberships: families, relationships.belongs_to_family
    """
    canonical_id: str
    urn: str
    name: str
    role: str
    description: str = ""
    domain: str = ""
    category: str = ""
    subcategory: str = ""
    owner: Optional[str] = None
    families: List[str] = field(default_factory=list)
    semantic_groups: List[str] = field(default_factory=list)
    physical_path: Optional[str] = None
    version: str = "1.0.0"
    status: str = "active"
    confidence: str = "high"
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    relationships: Dict[str, Any] = field(default_factory=lambda: {
        "composed_of": [],
        "extends": None,
        "depends_on": [],
        "adapts": None,
        "aliased_to": None,
        "belongs_to_family": None,
    })
    execution_providers: List[Dict[str, Any]] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=lambda: {
        "source_hash": "",
        "content_hash": "",
        "commit_sha": "",
        "last_validated": "",
    })

    def __post_init__(self):
        # Enforce canonical identity parsing
        self._parsed_id = CanonicalIdentity.parse(self.canonical_id)
        if not self.urn:
            self.urn = self._parsed_id.urn

        # Validate Invariant 6: Path-Independent Identity
        for part, name in [(self._parsed_id.scope, "scope"), (self._parsed_id.slug, "slug")]:
            if "/" in part or "\\" in part or any(part.endswith(ext) for ext in [".md", ".json", ".yaml", ".yml"]):
                raise InvariantViolationError(
                    f"Invariant 6 Violation (Path Independence): Canonical identifier '{self.canonical_id}' contains path separators or extensions."
                )

        # Normalize role
        norm_role = SkillRole.normalize_role(self.role)
        self.role = norm_role.value

        # Normalize relationships dict structure
        rels = self.relationships or {}
        self.relationships = {
            "composed_of": sorted(rels.get("composed_of", [])),
            "extends": rels.get("extends"),
            "depends_on": sorted(rels.get("depends_on", [])),
            "adapts": rels.get("adapts"),
            "aliased_to": rels.get("aliased_to"),
            "belongs_to_family": rels.get("belongs_to_family"),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "urn": self.urn,
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "domain": self.domain,
            "category": self.category,
            "subcategory": self.subcategory,
            "owner": self.owner,
            "families": sorted(self.families),
            "semantic_groups": sorted(self.semantic_groups),
            "physical_path": self.physical_path,
            "version": self.version,
            "status": self.status,
            "confidence": self.confidence,
            "tags": sorted(self.tags),
            "keywords": sorted(self.keywords),
            "relationships": self.relationships,
            "execution_providers": self.execution_providers,
            "provenance": self.provenance,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RegistryEntry:
        return cls(
            canonical_id=data["canonical_id"],
            urn=data.get("urn", ""),
            name=data.get("name", ""),
            role=data.get("role", "capability"),
            description=data.get("description", ""),
            domain=data.get("domain", ""),
            category=data.get("category", ""),
            subcategory=data.get("subcategory", ""),
            owner=data.get("owner"),
            families=list(data.get("families", [])),
            semantic_groups=list(data.get("semantic_groups", [])),
            physical_path=data.get("physical_path"),
            version=data.get("version", "1.0.0"),
            status=data.get("status", "active"),
            confidence=data.get("confidence", "high"),
            tags=list(data.get("tags", [])),
            keywords=list(data.get("keywords", [])),
            relationships=dict(data.get("relationships", {})),
            execution_providers=list(data.get("execution_providers", [])),
            provenance=dict(data.get("provenance", {})),
        )

    @classmethod
    def from_skill_object(
        cls,
        obj: SkillObject,
        category: str = "",
        subcategory: str = "",
        semantic_groups: Optional[List[str]] = None,
        execution_providers: Optional[List[Dict[str, Any]]] = None,
        provenance: Optional[Dict[str, Any]] = None,
        keywords: Optional[List[str]] = None,
        confidence: str = "high",
    ) -> RegistryEntry:
        """Construct RegistryEntry from an object_model.SkillObject instance."""
        rels = {
            "composed_of": [],
            "extends": None,
            "depends_on": [],
            "adapts": None,
            "aliased_to": None,
            "belongs_to_family": None,
        }
        for r in obj.relationships:
            if r.rel_type == RelationshipType.COMPOSED_OF:
                rels["composed_of"].append(r.target_id)
            elif r.rel_type == RelationshipType.EXTENDS:
                rels["extends"] = r.target_id
            elif r.rel_type == RelationshipType.DEPENDS_ON:
                rels["depends_on"].append(r.target_id)
            elif r.rel_type == RelationshipType.ADAPTS:
                rels["adapts"] = r.target_id
            elif r.rel_type == RelationshipType.ALIASED_TO:
                rels["aliased_to"] = r.target_id
            elif r.rel_type == RelationshipType.BELONGS_TO_FAMILY:
                rels["belongs_to_family"] = r.target_id

        # Fallback if specific object subclasses set attributes directly
        if isinstance(obj, AliasObject) and obj.target_id:
            rels["aliased_to"] = obj.target_id
        elif isinstance(obj, OverlayObject) and obj.target_id:
            rels["extends"] = obj.target_id

        providers = execution_providers or []
        if not providers and isinstance(obj, CapabilityObject) and obj.execution_provider:
            providers = [{
                "provider_id": f"{obj.name}-{obj.execution_provider}",
                "provider_type": obj.execution_provider,
                "transport": obj.execution_provider,
                "is_default": True,
            }]

        status_val = obj.status.value if isinstance(obj.status, ReviewStatus) else str(obj.status)

        return cls(
            canonical_id=obj.canonical_id,
            urn=obj.id_object.urn,
            name=obj.name,
            role=obj.role.value,
            description=obj.description,
            domain=obj.domain or category,
            category=category or obj.domain,
            subcategory=subcategory,
            owner=obj.owner,
            families=list(obj.families),
            semantic_groups=list(semantic_groups or []),
            physical_path=obj.physical_path,
            version=obj.version,
            status=status_val,
            confidence=confidence,
            tags=list(obj.tags),
            keywords=list(keywords or []),
            relationships=rels,
            execution_providers=providers,
            provenance=provenance or {},
        )


class CatalogRegistry:
    """
    Authoritative Compiled Catalog Registry conforming to ADR-004.
    Encapsulates all registered skills, semantic groups, and deterministic schema serialization.
    """
    SCHEMA_URI = "https://json-schema.revrebel.io/v1/skills-registry.schema.json"
    VERSION = "1.0.0"

    def __init__(self, commit_sha: str = "", generated_at: Optional[str] = None):
        self.commit_sha = commit_sha
        self.generated_at = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.skills: Dict[str, RegistryEntry] = {}
        self.semantic_groups: Dict[str, SemanticGroupObject] = {}

    def add_entry(self, entry: RegistryEntry) -> None:
        """Register a skill entry. Enforces Invariant 2: Single Canonical Owner."""
        cid = entry.canonical_id
        if cid in self.skills:
            raise InvariantViolationError(
                f"Invariant 2 Violation (Single Canonical Owner): Duplicate canonical_id '{cid}' already registered."
            )
        self.skills[cid] = entry

    def get_entry(self, canonical_id: str) -> Optional[RegistryEntry]:
        """Retrieve entry by canonical ID."""
        return self.skills.get(canonical_id)

    def add_semantic_group(self, group: SemanticGroupObject) -> None:
        """Register a semantic group."""
        gid = group.group_id
        if gid in self.semantic_groups:
            raise InvariantViolationError(
                f"Duplicate semantic group_id '{gid}' already registered."
            )
        self.semantic_groups[gid] = group

    def get_semantic_group(self, group_id: str) -> Optional[SemanticGroupObject]:
        """Retrieve semantic group by ID."""
        return self.semantic_groups.get(group_id)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize complete registry matching ADR-004 Section 2.2 schema."""
        return {
            "$schema": self.SCHEMA_URI,
            "version": self.VERSION,
            "generated_at": self.generated_at,
            "commit_sha": self.commit_sha,
            "total_skills": len(self.skills),
            "total_semantic_groups": len(self.semantic_groups),
            "skills": {cid: entry.to_dict() for cid, entry in sorted(self.skills.items())},
            "semantic_groups": {gid: group.to_dict() for gid, group in sorted(self.semantic_groups.items())},
        }

    def to_json(self, indent: int = 2) -> str:
        """Deterministic JSON string serialization (sorted keys)."""
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CatalogRegistry:
        reg = cls(
            commit_sha=data.get("commit_sha", ""),
            generated_at=data.get("generated_at"),
        )
        for cid, edata in data.get("skills", {}).items():
            reg.add_entry(RegistryEntry.from_dict(edata))
        for gid, gdata in data.get("semantic_groups", {}).items():
            reg.add_semantic_group(SemanticGroupObject.from_dict(gdata))
        return reg

    @classmethod
    def from_json(cls, json_str: str) -> CatalogRegistry:
        return cls.from_dict(json.loads(json_str))


class DependencyResolver:
    """
    Evaluates directed dependency closures, enforces strict DAG acyclicity (INV-1),
    detects dead references (INV-8), and computes topological execution plans.
    """

    def __init__(self, registry: CatalogRegistry):
        self.registry = registry

    def _get_outbound_edges(self, entry: RegistryEntry) -> List[Tuple[str, str]]:
        """Return list of (target_id, relationship_type) for all directed structural edges."""
        edges = []
        rels = entry.relationships
        for target in rels.get("depends_on", []):
            edges.append((target, "depends_on"))
        for target in rels.get("composed_of", []):
            edges.append((target, "composed_of"))
        if rels.get("extends"):
            edges.append((rels["extends"], "extends"))
        if rels.get("adapts"):
            edges.append((rels["adapts"], "adapts"))
        return edges

    def validate_invariants(self) -> List[str]:
        """
        Validate all dependency and relationship invariants across the registry:
          - INV-1: Strict DAG Acyclicity across depends_on, composed_of, extends, adapts
          - INV-8: Dead Reference Prevention (every target ID exists)
          - INV-4: Shallow Overlay Specialization (overlay cannot extend overlay, must target cap/wf)
          - INV-5: Leaf Primitives (primitives cannot compose workflows)
        Raises InvariantViolationError if any violation is discovered.
        """
        errors = []

        # 1. Invariant 8: Dead Reference Prevention
        for cid, entry in sorted(self.registry.skills.items()):
            # Check all relationship fields
            rels = entry.relationships
            all_targets = (
                list(rels.get("depends_on", []))
                + list(rels.get("composed_of", []))
                + ([rels["extends"]] if rels.get("extends") else [])
                + ([rels["adapts"]] if rels.get("adapts") else [])
                + ([rels["aliased_to"]] if rels.get("aliased_to") else [])
            )
            for target_id in all_targets:
                if target_id not in self.registry.skills:
                    errors.append(
                        f"Invariant 8 Violation (Dead Reference): Skill '{cid}' references non-existent canonical target '{target_id}'."
                    )

        # 2. Invariant 4: Shallow Overlays
        for cid, entry in sorted(self.registry.skills.items()):
            if entry.role == SkillRole.OVERLAY.value:
                target_id = entry.relationships.get("extends")
                if target_id and target_id in self.registry.skills:
                    target = self.registry.skills[target_id]
                    if target.role == SkillRole.OVERLAY.value:
                        errors.append(
                            f"Invariant 4 Violation (Shallow Overlay): Overlay '{cid}' extends another overlay '{target_id}'. Overlays cannot extend overlays."
                        )
                    elif target.role not in (SkillRole.CAPABILITY.value, SkillRole.WORKFLOW.value):
                        errors.append(
                            f"Invariant 4 Violation (Shallow Overlay): Overlay '{cid}' targets role '{target.role}', must target capability or workflow."
                        )

        # 3. Invariant 5: Leaf Primitives
        for cid, entry in sorted(self.registry.skills.items()):
            if entry.role == SkillRole.PRIMITIVE.value:
                if entry.relationships.get("composed_of"):
                    errors.append(
                        f"Invariant 5 Violation (Leaf Primitives): Primitive '{cid}' declares composed_of targets. Primitives cannot compose workflows."
                    )

        # 4. Invariant 1: Strict DAG Acyclicity
        cycle = self.detect_cycle()
        if cycle:
            errors.append(
                f"Invariant 1 Violation (DAG Acyclicity): Circular relationship detected: {' -> '.join(cycle)}"
            )

        if errors:
            raise InvariantViolationError(
                f"Catalog invariant violations detected ({len(errors)}):\n"
                + "\n".join(f"  • {e}" for e in errors)
            )
        return []

    def detect_cycle(self) -> Optional[List[str]]:
        """
        Detect cycles in the directed dependency graph using depth-first search 3-color marking.
        Returns the cycle path [A, B, ..., A] if found, or None.
        """
        adj: Dict[str, List[str]] = {cid: [] for cid in self.registry.skills}
        for cid, entry in self.registry.skills.items():
            for target_id, _ in self._get_outbound_edges(entry):
                if target_id in self.registry.skills:
                    adj[cid].append(target_id)

        color: Dict[str, int] = {cid: 0 for cid in adj}  # 0: white, 1: gray, 2: black
        parent_path: List[str] = []

        def dfs(node: str) -> Optional[List[str]]:
            color[node] = 1
            parent_path.append(node)

            for neighbor in adj.get(node, []):
                if color[neighbor] == 1:
                    cycle_start = parent_path.index(neighbor)
                    return parent_path[cycle_start:] + [neighbor]
                elif color[neighbor] == 0:
                    result = dfs(neighbor)
                    if result:
                        return result

            parent_path.pop()
            color[node] = 2
            return None

        for node in sorted(adj.keys()):
            if color[node] == 0:
                cycle = dfs(node)
                if cycle:
                    return cycle

        return None

    def compute_transitive_closure(self, targets: Union[str, Iterable[str]]) -> Set[str]:
        """
        Computes the complete transitive dependency closure for one or more target skill IDs.
        Closure(S) = S ∪ ⋃ (DependsOn ∪ ComposedOf ∪ Extends ∪ Adapts)
        """
        if isinstance(targets, str):
            initial = [targets]
        else:
            initial = list(targets)

        closure: Set[str] = set()
        queue: List[str] = list(initial)

        while queue:
            current_id = queue.pop(0)
            if current_id in closure:
                continue
            closure.add(current_id)

            entry = self.registry.get_entry(current_id)
            if not entry:
                # Target does not exist in registry; raise Invariant 8 violation
                raise InvariantViolationError(
                    f"Invariant 8 Violation (Dead Reference): Cannot compute closure for non-existent target '{current_id}'."
                )

            for target_id, _ in self._get_outbound_edges(entry):
                if target_id not in closure and target_id not in queue:
                    queue.append(target_id)

        return closure

    def compute_execution_plan(self, targets: Union[str, Iterable[str]]) -> List[str]:
        """
        Computes deterministic topological execution/load order for the transitive closure.
        If skill A depends on / extends / adapts / is composed of B, then B MUST appear
        BEFORE A in the returned execution order.
        """
        closure = self.compute_transitive_closure(targets)

        # Build subgraph on closure
        subgraph_adj: Dict[str, Set[str]] = {cid: set() for cid in closure}
        in_degree: Dict[str, int] = {cid: 0 for cid in closure}

        # Outbound edge: entry -> dependency.
        # Dependency precedes entry: dependency -> entry in execution order!
        for cid in closure:
            entry = self.registry.skills[cid]
            for dep_id, _ in self._get_outbound_edges(entry):
                if dep_id in closure:
                    # dep_id must be loaded before cid
                    if cid not in subgraph_adj[dep_id]:
                        subgraph_adj[dep_id].add(cid)
                        in_degree[cid] += 1

        # Kahn's algorithm with deterministic tie-breaking (sorted canonical_id)
        ready_queue = sorted([cid for cid, deg in in_degree.items() if deg == 0])
        ordered: List[str] = []

        while ready_queue:
            # Deterministic: pick lowest canonical_id
            ready_queue.sort()
            node = ready_queue.pop(0)
            ordered.append(node)

            for dependent in sorted(subgraph_adj[node]):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    ready_queue.append(dependent)

        if len(ordered) != len(closure):
            raise InvariantViolationError(
                "Invariant 1 Violation (DAG Acyclicity): Cycle encountered during topological execution plan calculation."
            )

        return ordered

    def find_orphaned_primitives_and_adapters(self) -> Dict[str, List[str]]:
        """
        Detects primitives and adapters with in-degree 0 (no capability or workflow referencing them).
        Useful for dead code analysis and catalog hygiene.
        """
        referenced_primitives: Set[str] = set()
        referenced_adapters: Set[str] = set()

        for cid, entry in self.registry.skills.items():
            for target_id, rel_type in self._get_outbound_edges(entry):
                target = self.registry.get_entry(target_id)
                if target:
                    if target.role == SkillRole.PRIMITIVE.value:
                        referenced_primitives.add(target_id)
                    elif target.role == SkillRole.ADAPTER.value:
                        referenced_adapters.add(target_id)

        orphaned_primitives = [
            cid for cid, e in sorted(self.registry.skills.items())
            if e.role == SkillRole.PRIMITIVE.value and cid not in referenced_primitives
        ]
        orphaned_adapters = [
            cid for cid, e in sorted(self.registry.skills.items())
            if e.role == SkillRole.ADAPTER.value and cid not in referenced_adapters
        ]

        return {
            "orphaned_primitives": orphaned_primitives,
            "orphaned_adapters": orphaned_adapters,
        }


class AliasResolver:
    """
    Enforces Single-Hop Alias Resolution (INV-3), manages backward-compatible deprecation telemetry,
    and implements direction-neutral candidate duplicate resolution.
    """

    def __init__(self, registry: CatalogRegistry):
        self.registry = registry

    def resolve(self, identifier: str) -> Tuple[RegistryEntry, List[str]]:
        """
        Resolve an identifier to its canonical target entry.
        Enforces Invariant 3 (Single-Hop Alias).
        Returns (target_entry, hop_list).
        """
        entry = self.registry.get_entry(identifier)
        if not entry:
            raise KeyError(f"Identifier '{identifier}' not found in catalog registry.")

        if entry.role != SkillRole.ALIAS.value:
            return entry, [identifier]

        # Entry is an alias
        target_id = entry.relationships.get("aliased_to")
        if not target_id:
            raise InvariantViolationError(f"Alias '{identifier}' has no aliased_to target defined.")

        target_entry = self.registry.get_entry(target_id)
        if not target_entry:
            raise InvariantViolationError(
                f"Invariant 8 Violation (Dead Reference): Alias '{identifier}' points to non-existent target '{target_id}'."
            )

        if target_entry.role == SkillRole.ALIAS.value:
            raise InvariantViolationError(
                f"Invariant 3 Violation (Single-Hop Alias): Alias '{identifier}' points to another alias '{target_id}' (chaining forbidden)."
            )

        return target_entry, [identifier, target_id]

    def get_deprecation_telemetry(self, identifier: str) -> Dict[str, Any]:
        """
        Returns deprecation status and telemetry for an identifier.
        """
        entry = self.registry.get_entry(identifier)
        if not entry:
            raise KeyError(f"Identifier '{identifier}' not found in catalog registry.")

        is_alias = entry.role == SkillRole.ALIAS.value
        is_deprecated = entry.status in ("deprecated", "sunset") or is_alias
        target_id = entry.relationships.get("aliased_to") if is_alias else None

        notice = ""
        if is_alias and target_id:
            notice = f"Skill identifier '{identifier}' is an alias redirected to canonical capability '{target_id}'. Please update references."
        elif is_deprecated:
            notice = f"Skill '{identifier}' is deprecated."

        return {
            "identifier": identifier,
            "is_alias": is_alias,
            "is_deprecated": is_deprecated,
            "status": entry.status,
            "canonical_target": target_id or identifier,
            "deprecation_notice": notice,
        }

    @staticmethod
    def build_direction_neutral_duplicate_pair(
        canonical_hub_entry: RegistryEntry,
        legacy_path_entry_data: Dict[str, Any],
    ) -> Tuple[RegistryEntry, RegistryEntry]:
        """
        Implements ADR-004 Section 5.2: Direction-neutral duplicate pair resolution.
        Designates the Tier 1 platform hub capability as the canonical target,
        and constructs a backward-compatible AliasObject with status 'deprecated'.
        """
        alias_id = legacy_path_entry_data["canonical_id"]
        alias_name = legacy_path_entry_data.get("name", canonical_hub_entry.name)

        alias_entry = RegistryEntry(
            canonical_id=alias_id,
            urn=f"urn:skill:{alias_id}",
            name=alias_name,
            role=SkillRole.ALIAS.value,
            description=f"Backward-compatible redirect to canonical capability '{canonical_hub_entry.canonical_id}'.",
            domain=legacy_path_entry_data.get("domain", ""),
            category=legacy_path_entry_data.get("category", ""),
            subcategory=legacy_path_entry_data.get("subcategory", ""),
            physical_path=legacy_path_entry_data.get("physical_path"),
            status="deprecated",
            confidence="high",
            relationships={
                "composed_of": [],
                "extends": None,
                "depends_on": [],
                "adapts": None,
                "aliased_to": canonical_hub_entry.canonical_id,
                "belongs_to_family": canonical_hub_entry.relationships.get("belongs_to_family"),
            },
        )
        return canonical_hub_entry, alias_entry


class MultiViewProjector:
    """
    Compiles the 4 canonical discovery projection views and inverted search index
    defined under ADR-004 Section 3.
    """

    def __init__(self, registry: CatalogRegistry):
        self.registry = registry

    def project_functional_view(self) -> Dict[str, Any]:
        """
        Functional / Domain View: domain -> category -> subcategory -> skill summaries.
        """
        tree: Dict[str, Dict[str, Dict[str, List[Dict[str, Any]]]]] = {}

        for cid, entry in sorted(self.registry.skills.items()):
            domain = entry.domain or "general"
            cat = entry.category or "uncategorized"
            subcat = entry.subcategory or "general"

            if domain not in tree:
                tree[domain] = {}
            if cat not in tree[domain]:
                tree[domain][cat] = {}
            if subcat not in tree[domain][cat]:
                tree[domain][cat][subcat] = []

            tree[domain][cat][subcat].append({
                "canonical_id": entry.canonical_id,
                "name": entry.name,
                "role": entry.role,
                "description": entry.description,
                "status": entry.status,
            })

        return {
            "view_type": "functional_domain",
            "version": "1.0.0",
            "total_domains": len(tree),
            "domains": tree,
        }

    def project_family_view(self, family_metadata: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Platform / Family View: platform -> tier, hub_path, tier_1_members, tier_2_members.
        """
        meta = family_metadata or {}
        families: Dict[str, Dict[str, Any]] = {}

        for cid, entry in sorted(self.registry.skills.items()):
            all_families = list(entry.families)
            if entry.relationships.get("belongs_to_family") and entry.relationships["belongs_to_family"] not in all_families:
                all_families.append(entry.relationships["belongs_to_family"])

            for fam in all_families:
                if fam not in families:
                    fam_meta = meta.get(fam, {})
                    families[fam] = {
                        "family_id": fam,
                        "title": fam_meta.get("title", fam.replace("-", " ").title()),
                        "vendor": fam_meta.get("vendor", ""),
                        "tier": fam_meta.get("tier", "tier_2_logical_family"),
                        "hub_path": f"library/tools-and-platforms/{fam}",
                        "tier_1_members": [],
                        "tier_2_members": [],
                        "total_members": 0,
                    }

                # Determine if member is physically in hub or logical
                is_hub_member = entry.physical_path and f"tools-and-platforms/{fam}" in entry.physical_path
                summary = {
                    "canonical_id": entry.canonical_id,
                    "name": entry.name,
                    "role": entry.role,
                    "physical_path": entry.physical_path,
                }
                if is_hub_member:
                    families[fam]["tier_1_members"].append(summary)
                else:
                    families[fam]["tier_2_members"].append(summary)
                families[fam]["total_members"] += 1

        return {
            "view_type": "platform_family",
            "version": "1.0.0",
            "total_families": len(families),
            "families": dict(sorted(families.items())),
        }

    def project_semantic_group_view(self) -> Dict[str, Any]:
        """
        Semantic Group View: group_id -> members, cross-domain task cluster information.
        """
        groups: Dict[str, Dict[str, Any]] = {}

        # 1. Registered semantic groups
        for gid, grp in sorted(self.registry.semantic_groups.items()):
            groups[gid] = grp.to_dict()

        # 2. Reconcile entries that declare semantic_groups
        for cid, entry in sorted(self.registry.skills.items()):
            for gid in entry.semantic_groups:
                if gid not in groups:
                    groups[gid] = {
                        "group_id": gid,
                        "name": gid.replace("-", " ").title(),
                        "description": f"Cross-cutting group for {gid}",
                        "domain_scope": "cross-domain",
                        "members": [],
                        "tags": [],
                        "materialization_policy": "transitive_closure",
                    }
                if cid not in groups[gid]["members"]:
                    groups[gid]["members"].append(cid)
                    groups[gid]["members"].sort()

        return {
            "view_type": "semantic_group",
            "version": "1.0.0",
            "total_groups": len(groups),
            "groups": dict(sorted(groups.items())),
        }

    def project_provider_view(self) -> Dict[str, Any]:
        """
        Execution / Provider View: transport -> capabilities supporting execution.
        """
        providers: Dict[str, List[Dict[str, Any]]] = {}

        for cid, entry in sorted(self.registry.skills.items()):
            for prov in entry.execution_providers:
                transport = prov.get("transport") or prov.get("provider_type") or "unspecified"
                if transport not in providers:
                    providers[transport] = []
                providers[transport].append({
                    "canonical_id": entry.canonical_id,
                    "name": entry.name,
                    "provider_id": prov.get("provider_id", ""),
                    "provider_type": prov.get("provider_type", ""),
                    "is_default": prov.get("is_default", False),
                })

        return {
            "view_type": "execution_provider",
            "version": "1.0.0",
            "total_transports": len(providers),
            "transports": {k: sorted(v, key=lambda x: x["canonical_id"]) for k, v in sorted(providers.items())},
        }

    def build_search_index(self) -> Dict[str, List[str]]:
        """
        Constructs the inverted search index (audit/search-index.json).
        Tokenizes names, tags, keywords, and description terms into canonical ID postings.
        """
        stopwords = {
            "a", "an", "the", "in", "on", "of", "and", "or", "for", "with",
            "to", "at", "by", "from", "is", "it", "this", "that", "as", "be",
        }
        index: Dict[str, Set[str]] = {}

        def add_token(tok: str, cid: str):
            clean = tok.lower().strip(" \t\n\r.,;:!?()[]{}\"'`")
            if len(clean) >= 2 and clean not in stopwords:
                if clean not in index:
                    index[clean] = set()
                index[clean].add(cid)

        for cid, entry in self.registry.skills.items():
            # Index canonical ID components
            add_token(entry.canonical_id, cid)
            for part in entry.canonical_id.split(":"):
                add_token(part, cid)

            # Index name
            for part in entry.name.replace("-", " ").replace("_", " ").split():
                add_token(part, cid)

            # Index tags and keywords
            for tag in entry.tags:
                add_token(tag, cid)
            for kw in entry.keywords:
                for kw_part in kw.split():
                    add_token(kw_part, cid)

            # Index description words
            for word in entry.description.split():
                add_token(word, cid)

        # Emit deterministically sorted dictionary
        return {tok: sorted(list(cids)) for tok, cids in sorted(index.items())}


class ProjectMaterializer:
    """
    Computes complete, self-contained project materialization bundles with
    transitive dependency completeness (INV-9) and collision-free flat runtime naming.
    """

    def __init__(self, registry: CatalogRegistry):
        self.registry = registry
        self.resolver = DependencyResolver(registry)

    def materialize_bundle(
        self,
        mode: ProjectionMode,
        target_ids: Optional[List[str]] = None,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Materializes a self-contained skill bundle.
        Guarantees that all transitive dependencies are satisfied (INV-9).
        """
        initial_set: Set[str] = set()

        if mode == ProjectionMode.FULL:
            initial_set = set(self.registry.skills.keys())
        elif mode == ProjectionMode.STANDALONE_CLOSURE:
            if not target_ids:
                raise RegistryError("STANDALONE_CLOSURE projection mode requires target_ids.")
            initial_set = set(target_ids)
        elif mode == ProjectionMode.SEMANTIC_GROUP:
            if not target_ids:
                raise RegistryError("SEMANTIC_GROUP projection mode requires group_ids in target_ids.")
            for gid in target_ids:
                group = self.registry.get_semantic_group(gid)
                if not group:
                    raise RegistryError(f"Semantic group '{gid}' not found in registry.")
                initial_set.update(group.members)
        elif mode == ProjectionMode.FAMILY:
            if not target_ids:
                raise RegistryError("FAMILY projection mode requires family_ids in target_ids.")
            for fam in target_ids:
                for cid, entry in self.registry.skills.items():
                    if fam in entry.families or entry.relationships.get("belongs_to_family") == fam:
                        initial_set.add(cid)
        elif mode == ProjectionMode.SUBSET:
            criteria = filter_criteria or {}
            target_cat = criteria.get("category")
            target_domain = criteria.get("domain")
            for cid, entry in self.registry.skills.items():
                if target_cat and entry.category == target_cat:
                    initial_set.add(cid)
                elif target_domain and entry.domain == target_domain:
                    initial_set.add(cid)

        # Enforce Invariant 9: Transitive Dependency Completeness
        full_closure = self.resolver.compute_transitive_closure(initial_set)
        execution_order = self.resolver.compute_execution_plan(initial_set)

        # Compute collision-free flat runtime naming
        runtime_names = self._generate_flat_runtime_names(full_closure)

        return {
            "mode": mode.value,
            "target_count": len(initial_set),
            "total_materialized": len(full_closure),
            "targets": sorted(initial_set),
            "closure": sorted(full_closure),
            "execution_order": execution_order,
            "runtime_names": runtime_names,
            "skills": {cid: self.registry.skills[cid].to_dict() for cid in sorted(full_closure)},
        }

    def _generate_flat_runtime_names(self, cids: Iterable[str]) -> Dict[str, str]:
        """
        Generate collision-free runtime names according to ADR-004 Section 9.2:
        Unique leaf slugs remain un-prefixed; colliding leaf slugs are scoped.
        """
        entries = [self.registry.skills[cid] for cid in cids]
        slug_counts: Dict[str, int] = {}
        for e in entries:
            slug = e.name
            slug_counts[slug] = slug_counts.get(slug, 0) + 1

        names: Dict[str, str] = {}
        for e in entries:
            cid = e.canonical_id
            slug = e.name
            if slug_counts[slug] > 1:
                # Collision: prefix with category or scope
                prefix = e.category or e.domain or e._parsed_id.scope
                names[cid] = f"{prefix}-{slug}"
            else:
                names[cid] = slug

        return dict(sorted(names.items()))


class FamilyRouterGenerator:
    """
    Generates recursive markdown navigation routers conforming to ADR-004 Section 8.
    Enforces relative link integrity, trigger contracts, provider badges, and zero absolute paths.
    """

    @staticmethod
    def generate_tier_1_hub_router(
        family_slug: str,
        family_title: str,
        vendor: str,
        member_entries: List[RegistryEntry],
        description: str = "",
    ) -> str:
        """
        Generates root markdown router for a Tier 1 Platform Hub (library/tools-and-platforms/<family-slug>/SKILL.md).
        """
        lines = [
            "---",
            f"name: {family_slug}-router",
            f"description: Hierarchical navigation router for the {family_title} ecosystem.",
            "---",
            "",
            f"# {family_title} Platform Router",
            "",
            f"**Vendor / Ecosystem**: {vendor or 'Independent'}",
            f"**Classification**: Tier 1 Platform Hub",
            f"**Total Managed Skills**: {len(member_entries)}",
            "",
            description or f"Navigation router for capabilities, primitives, and workflows in the `{family_slug}` platform hub.",
            "",
        ]

        # Group by role
        primitives = [e for e in member_entries if e.role == SkillRole.PRIMITIVE.value]
        capabilities = [e for e in member_entries if e.role == SkillRole.CAPABILITY.value]
        workflows = [e for e in member_entries if e.role == SkillRole.WORKFLOW.value]
        others = [e for e in member_entries if e not in primitives and e not in capabilities and e not in workflows]

        def format_section(title: str, entries: List[RegistryEntry]):
            if not entries:
                return
            lines.append(f"## {title}")
            lines.append("")
            for e in sorted(entries, key=lambda x: x.name):
                badges = []
                for prov in e.execution_providers:
                    t = prov.get("transport", "").upper()
                    if t:
                        badges.append(f"[{t}]")
                badge_str = " " + " ".join(badges) if badges else ""
                lines.append(f"- [{e.name}]({e.name}/SKILL.md){badge_str}: {e.description or 'No description provided.'}")
            lines.append("")

        format_section("Platform Primitives & Shared Authentication", primitives)
        format_section("Core Capabilities", capabilities)
        format_section("Platform Workflows", workflows)
        format_section("Supporting Entities", others)

        return "\n".join(lines)

    @staticmethod
    def generate_tier_2_virtual_router(
        family_slug: str,
        family_title: str,
        vendor: str,
        member_entries: List[RegistryEntry],
    ) -> str:
        """
        Generates virtual projected markdown router for a Tier 2 Logical Family (views/routers/family-<family-slug>.md).
        """
        lines = [
            f"# {family_title} Logical Family Router",
            "",
            f"- **Classification**: Tier 2 Logical Family (Domain-Anchored)",
            f"- **Vendor**: {vendor or 'Independent'}",
            f"- **Total Discovered Capabilities**: {len(member_entries)}",
            "",
            f"The `{family_slug}` family is anchored across multiple functional domains throughout the catalog.",
            "",
            "## Discovered Members by Category",
            "",
        ]

        # Group by category
        by_cat: Dict[str, List[RegistryEntry]] = {}
        for e in member_entries:
            cat = e.category or "uncategorized"
            by_cat.setdefault(cat, []).append(e)

        for cat, entries in sorted(by_cat.items()):
            lines.append(f"### {cat.title()}")
            lines.append("")
            for e in sorted(entries, key=lambda x: x.name):
                rel_path = e.physical_path or f"library/{cat}/{e.subcategory}/{e.name}"
                lines.append(f"- **{e.name}** (`{e.canonical_id}`): {e.description or 'No description'}")
                lines.append(f"  - Physical Path: `{rel_path}`")
            lines.append("")

        return "\n".join(lines)


class CatalogCompiler:
    """
    Deterministic, idempotent catalog compilation pipeline conforming to ADR-004 Section 4.
    Compiles raw skill entities, census records, and ledgers into authoritative registry artifacts.
    """

    def __init__(self, commit_sha: str = "HEAD"):
        self.commit_sha = commit_sha

    def compile(
        self,
        skill_objects: List[SkillObject],
        semantic_groups: Optional[List[SemanticGroupObject]] = None,
        category_map: Optional[Dict[str, Tuple[str, str]]] = None,
        family_metadata: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> Tuple[CatalogRegistry, Dict[str, Any], Dict[str, List[str]]]:
        """
        Executes the deterministic compilation pipeline:
          Stage 1: Ingestion & Parsing into RegistryEntry
          Stage 2: Invariant Verification (DAG, Dead Reference, Single-Hop)
          Stage 3: View Projections (Functional, Family, Group, Provider)
          Stage 4: Inverted Search Index Generation
        Returns (registry, projections, search_index).
        """
        registry = CatalogRegistry(commit_sha=self.commit_sha)
        cat_map = category_map or {}

        # Stage 1: Ingest skill objects
        for obj in skill_objects:
            cat, subcat = cat_map.get(obj.canonical_id, (obj.domain, ""))
            entry = RegistryEntry.from_skill_object(
                obj=obj,
                category=cat,
                subcategory=subcat,
            )
            registry.add_entry(entry)

        # Ingest semantic groups
        for grp in (semantic_groups or []):
            registry.add_semantic_group(grp)

        # Stage 2: Invariant Verification
        resolver = DependencyResolver(registry)
        resolver.validate_invariants()

        alias_resolver = AliasResolver(registry)
        for cid, entry in registry.skills.items():
            if entry.role == SkillRole.ALIAS.value:
                alias_resolver.resolve(cid)

        # Stage 3: View Projections
        projector = MultiViewProjector(registry)
        projections = {
            "functional_view": projector.project_functional_view(),
            "family_view": projector.project_family_view(family_metadata),
            "semantic_group_view": projector.project_semantic_group_view(),
            "provider_view": projector.project_provider_view(),
        }

        # Stage 4: Inverted Search Index
        search_index = projector.build_search_index()

        return registry, projections, search_index
