"""Project-level skill materialization.

Resolves human-authored groups and project profiles against a canonical test
library, then emits a self-contained runtime bundle using the existing
CatalogCompiler / ProjectMaterializer contracts.
"""

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .object_model import Relationship, RelationshipType, SkillObject, SkillRole
from .registry_contract import (
    CatalogCompiler,
    ProjectMaterializer,
    ProjectionMode,
    SemanticGroupObject,
)


class MaterializationError(ValueError):
    pass


def _split_frontmatter(content: str) -> Tuple[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", content, re.DOTALL)
    if not match:
        return "", content
    return match.group(1), match.group(2)


def _scalar(frontmatter: str, key: str, default: str = "") -> str:
    match = re.search(rf'^{re.escape(key)}:[ \t]*"?([^"\n]+)"?', frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else default


def _metadata_scalar(frontmatter: str, key: str, default: str = "") -> str:
    match = re.search(rf'^[ ]{{2}}{re.escape(key)}:[ \t]*"?([^"\n]+)"?', frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else default


def _metadata_list(frontmatter: str, key: str) -> List[str]:
    match = re.search(rf'^[ ]{{2}}{re.escape(key)}:[ \t]*(.*?)(?=^[ ]{{2}}[a-zA-Z_]+:|\Z)', frontmatter, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    return [v.strip().strip('"') for v in re.findall(r"^[ ]+-[ ]+(.+)$", match.group(1), re.MULTILINE)]


def _relationships(frontmatter: str) -> Dict[str, Any]:
    block = re.search(r"^[ ]{2}relationships:[ \t]*\n(.*?)(?=^[ ]{2}[a-zA-Z_]+:|\Z)", frontmatter, re.MULTILINE | re.DOTALL)
    if not block:
        return {}
    text = block.group(1)
    result: Dict[str, Any] = {}
    for key in ("depends_on", "composed_of"):
        match = re.search(rf"^[ ]{{4}}{key}:[ \t]*(.*?)(?=^[ ]{{4}}[a-zA-Z_]+:|\Z)", text, re.MULTILINE | re.DOTALL)
        result[key] = [v.strip().strip('"') for v in re.findall(r"^[ ]+-[ ]+(.+)$", match.group(1), re.MULTILINE)] if match else []
    for key in ("extends", "adapts", "aliased_to"):
        match = re.search(rf"^[ ]{{4}}{key}:[ \t]*([^\n]+)", text, re.MULTILINE)
        value = match.group(1).strip().strip('"') if match else ""
        result[key] = None if value in {"", "null", "None", "~"} else value
    return result


def parse_skill_file(path: Path, library: Path) -> SkillObject:
    content = path.read_text(encoding="utf-8")
    frontmatter, _ = _split_frontmatter(content)
    name = _scalar(frontmatter, "name", path.parent.name)
    canonical_id = _metadata_scalar(frontmatter, "canonical_id")
    if not canonical_id:
        canonical_id = f"{path.relative_to(library).parts[0]}:{name}"
    role = SkillRole.normalize_role(_metadata_scalar(frontmatter, "role", "capability"))
    rel_parts = path.parent.relative_to(library).parts
    category = rel_parts[0] if rel_parts else ""
    subcategory = rel_parts[1] if len(rel_parts) > 2 else ""
    rels = _relationships(frontmatter)
    relationships = []
    for key, rel_type in (
        ("depends_on", RelationshipType.DEPENDS_ON),
        ("composed_of", RelationshipType.COMPOSED_OF),
    ):
        for target in rels.get(key, []):
            relationships.append(Relationship(canonical_id, target, rel_type))
    for key, rel_type in (
        ("extends", RelationshipType.EXTENDS),
        ("adapts", RelationshipType.ADAPTS),
        ("aliased_to", RelationshipType.ALIASED_TO),
    ):
        if rels.get(key):
            relationships.append(Relationship(canonical_id, rels[key], rel_type))
    return SkillObject(
        canonical_id=canonical_id,
        name=name,
        role=role,
        description=_scalar(frontmatter, "description"),
        domain=category,
        physical_path=path.parent.relative_to(library).as_posix(),
        tags=_metadata_list(frontmatter, "tags"),
        relationships=relationships,
        metadata={
            "applications": _metadata_list(frontmatter, "applications"),
            "keywords": _metadata_list(frontmatter, "keywords"),
            "subcategory": subcategory,
        },
    )


def load_skills(library: Path) -> Tuple[List[SkillObject], Dict[str, SkillObject], Dict[str, SkillObject]]:
    skills: List[SkillObject] = []
    by_id: Dict[str, SkillObject] = {}
    by_name: Dict[str, SkillObject] = {}
    ambiguous_names: Set[str] = set()
    for path in sorted(library.glob("**/SKILL.md")):
        frontmatter, _ = _split_frontmatter(path.read_text(encoding="utf-8"))
        if not _scalar(frontmatter, "name"):
            continue  # router, not a skill
        skill = parse_skill_file(path, library)
        if skill.canonical_id in by_id:
            raise MaterializationError(f"Duplicate canonical ID: {skill.canonical_id}")
        if skill.name in by_name:
            # Duplicate leaf names are expected in a canonical library. The
            # materializer disambiguates them; bare-name references cannot.
            by_name.pop(skill.name)
            ambiguous_names.add(skill.name)
        elif skill.name not in ambiguous_names:
            by_name[skill.name] = skill
        skills.append(skill)
        by_id[skill.canonical_id] = skill
    if not skills:
        raise MaterializationError(f"No skills found in {library}")
    return skills, by_id, by_name


def _resolve_ref(ref: str, by_id: Dict[str, SkillObject], by_name: Dict[str, SkillObject]) -> str:
    if ref in by_id:
        return ref
    if ref in by_name:
        return by_name[ref].canonical_id
    raise MaterializationError(f"Unknown skill or canonical ID: {ref}")


def _safe_include_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise MaterializationError(f"Unsafe include_path: {value}")
    return path.as_posix().strip("/")


def resolve_groups(config: Dict[str, Any], skills: List[SkillObject]) -> Tuple[Dict[str, SemanticGroupObject], Dict[str, Any]]:
    by_id = {s.canonical_id: s for s in skills}
    by_name = {s.name: s for s in skills}
    raw_groups = config.get("groups", {})
    if not isinstance(raw_groups, dict):
        raise MaterializationError("skill-groups config must contain a groups object")

    resolved: Dict[str, SemanticGroupObject] = {}
    resolved_payloads: Dict[str, Any] = {}
    visiting: Set[str] = set()

    def resolve(group_id: str) -> Set[str]:
        if group_id in resolved:
            return set(resolved[group_id].members)
        if group_id in visiting:
            raise MaterializationError(f"Cyclic skill group reference: {group_id}")
        if group_id not in raw_groups:
            raise MaterializationError(f"Unknown skill group: {group_id}")
        visiting.add(group_id)
        raw = raw_groups[group_id]
        members: Set[str] = set()
        for ref in raw.get("skills", []):
            members.add(_resolve_ref(ref, by_id, by_name))
        for child in raw.get("groups", []):
            members.update(resolve(child))
        for app in raw.get("match", {}).get("applications", []):
            members.update(s.canonical_id for s in skills if app in s.metadata.get("applications", []))
        for include in raw.get("include_paths", []):
            prefix = _safe_include_path(include)
            members.update(
                s.canonical_id for s in skills
                if s.physical_path == prefix or s.physical_path.startswith(prefix + "/")
            )
        for ref in raw.get("exclude", []):
            members.discard(_resolve_ref(ref, by_id, by_name))
        visiting.remove(group_id)
        group = SemanticGroupObject(
            group_id=group_id,
            name=raw.get("name", group_id),
            description=raw.get("description", ""),
            members=sorted(members),
            tags=list(raw.get("tags", [])),
        )
        resolved[group_id] = group
        resolved_payloads[group_id] = {
            **group.to_dict(),
            "total_skills": len(members),
            "skills": [
                {
                    "runtime_name": by_id[cid].name,
                    "canonical_id": cid,
                    "canonical_path": by_id[cid].physical_path,
                    "role": by_id[cid].role.value,
                }
                for cid in sorted(members)
            ],
        }
        return members

    for group_id in raw_groups:
        resolve(group_id)
    return resolved, resolved_payloads


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_hash(skill_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        if path.is_symlink():
            raise MaterializationError(f"Symlinks are not allowed in skill packages: {path}")
        digest.update(path.relative_to(skill_dir).as_posix().encode("utf-8"))
        digest.update(_hash_file(path).encode("ascii"))
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def materialize_project(
    library: Path,
    profile: Dict[str, Any],
    groups_config: Dict[str, Any],
    target: Path,
    source_commit: str = "HEAD",
    replace: bool = False,
) -> Dict[str, Any]:
    library = library.resolve()
    target = target.resolve()
    real_library = (Path(__file__).resolve().parents[2] / "library").resolve()
    if target == real_library or real_library in target.parents:
        raise MaterializationError("Refusing to materialize a project into the real library/")
    if target == target.parent:
        raise MaterializationError("Refusing to materialize into a filesystem root")

    skills, by_id, by_name = load_skills(library)
    groups, resolved_groups = resolve_groups(groups_config, skills)
    category_map = {
        s.canonical_id: (s.domain, s.metadata.get("subcategory", ""))
        for s in skills
    }
    try:
        registry, projections, search_index = CatalogCompiler(commit_sha=source_commit).compile(
            skills,
            semantic_groups=list(groups.values()),
            category_map=category_map,
        )
    except Exception as e:
        raise MaterializationError(f"Catalog compilation failed: {e}") from e

    selected: Set[str] = set()
    for ref in profile.get("skills", []):
        selected.add(_resolve_ref(ref, by_id, by_name))
    for group_id in profile.get("groups", []):
        if group_id not in groups:
            raise MaterializationError(f"Unknown project group: {group_id}")
        selected.update(groups[group_id].members)
    for ref in profile.get("exclude", []):
        selected.discard(_resolve_ref(ref, by_id, by_name))
    if not selected:
        raise MaterializationError("Project profile selected no skills")

    bundle = ProjectMaterializer(registry).materialize_bundle(
        mode=ProjectionMode.STANDALONE_CLOSURE,
        target_ids=sorted(selected),
    )
    runtime_names = bundle["runtime_names"]

    stage = target.parent / f".{target.name}.materialize-staging"
    backup = target.parent / f".{target.name}.materialize-backup"
    if stage.exists():
        shutil.rmtree(stage)
    if backup.exists():
        shutil.rmtree(backup)
    stage.mkdir(parents=True)

    lock_skills: Dict[str, Any] = {}
    for cid in bundle["closure"]:
        skill = by_id[cid]
        runtime_name = runtime_names[cid]
        source_dir = library / skill.physical_path
        if any(path.is_symlink() for path in source_dir.rglob("*")):
            raise MaterializationError(f"Symlinks are not allowed in skill packages: {source_dir}")
        destination = stage / runtime_name
        shutil.copytree(source_dir, destination)
        lock_skills[runtime_name] = {
            "canonical_id": cid,
            "urn": registry.skills[cid].urn,
            "name": skill.name,
            "version": skill.version,
            "source_commit": source_commit,
            "content_hash": _package_hash(source_dir),
            "role": skill.role.value,
            "dependencies": sorted(
                rel.target_id for rel in skill.relationships
                if rel.rel_type in {RelationshipType.DEPENDS_ON, RelationshipType.EXTENDS, RelationshipType.COMPOSED_OF}
            ),
            "source_path": skill.physical_path,
        }

    router_lines = ["# Project Skills", ""]
    for runtime_name in sorted(lock_skills):
        entry = lock_skills[runtime_name]
        router_lines.append(f"- [`{runtime_name}`]({runtime_name}/SKILL.md) — {entry['role']}")
    (stage / "SKILL.md").write_text("\n".join(router_lines) + "\n", encoding="utf-8")

    _write_json(stage / "skills-catalog.json", {
        "version": "1.0",
        "project_name": profile.get("name", target.name),
        "skills": lock_skills,
    })
    _write_json(stage / "skill-groups-catalog.json", resolved_groups)
    _write_json(stage / "load-plan.json", {
        "version": "1.0",
        "entrypoint": "SKILL.md",
        "selected": sorted(selected),
        "execution_order": bundle["execution_order"],
        "policy": "progressive",
    })
    _write_json(stage / "skills.lock.json", {
        "lockfile_version": "1.0",
        "project_name": profile.get("name", target.name),
        "source_commit": source_commit,
        "skills": lock_skills,
    })

    if target.exists():
        if not replace:
            shutil.rmtree(stage)
            raise MaterializationError(f"Target already exists: {target}; use --replace to snapshot and replace it")
        shutil.move(str(target), str(backup))
    try:
        shutil.move(str(stage), str(target))
    except Exception:
        if backup.exists():
            shutil.move(str(backup), str(target))
        raise
    if backup.exists():
        shutil.rmtree(backup)

    return {
        "project_name": profile.get("name", target.name),
        "target": str(target),
        "selected": sorted(selected),
        "closure": bundle["closure"],
        "runtime_names": runtime_names,
        "execution_order": bundle["execution_order"],
        "total_materialized": len(lock_skills),
        "lockfile": str(target / "skills.lock.json"),
    }
