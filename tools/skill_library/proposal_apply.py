"""Controlled application of approved Librarian proposals.

This module is deliberately test-library-only. It snapshots the full target
library before each proposal, applies approved changes, records a ledger entry,
and restores the snapshot on any failure. It never targets the real library/.
"""

import copy
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .librarian_ai import render_frontmatter
from .proposal_review import get_proposal, set_status, validate_proposal


def validate_test_library(library: Path, real_library: Path) -> Path:
    library = library.resolve()
    real_library = real_library.resolve()
    if library == real_library or real_library in library.parents:
        raise ValueError("Refusing to apply Librarian proposals to the real library/")
    if library == library.parent:
        raise ValueError("Refusing to use a filesystem root as the test library")
    return library


def _split_frontmatter(content: str) -> Tuple[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", content, re.DOTALL)
    if not match:
        return "", content
    return match.group(1), match.group(2)


def _scalar(frontmatter: str, key: str, default: str = "") -> str:
    match = re.search(rf'^{re.escape(key)}:\s*"?([^"\n]+)"?', frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else default


def _normalize_claim(text: str) -> str:
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", text)
    text = text.strip().strip("`*_ ")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _claim_line_indices(body: str, claims: List[Dict[str, Any]]) -> List[int]:
    lines = body.splitlines()
    remove = set()
    for claim in claims:
        target = _normalize_claim(claim.get("text", ""))
        if not target:
            raise ValueError("Cannot remove an empty claim from the parent")
        matches = [i for i, line in enumerate(lines) if _normalize_claim(line) == target]
        if not matches:
            raise ValueError(
                f"Cannot safely remove parent claim {claim.get('id')}: "
                f"no exact body line matches {claim.get('text')!r}"
            )
        remove.update(matches)
    return sorted(remove)


def _metadata_list(lines: List[str], key: str) -> List[str]:
    """Read a simple metadata list such as relationships.composed_of."""
    try:
        metadata_index = next(i for i, line in enumerate(lines) if line.strip() == "metadata:")
    except StopIteration:
        return []
    key_index = None
    for i in range(metadata_index + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped and len(lines[i]) - len(lines[i].lstrip()) == 0 and not stripped.startswith("-"):
            break
        if lines[i] == f"    {key}:" or lines[i] == f"    {key}: []":
            key_index = i
            break
    if key_index is None:
        return []
    values = []
    for line in lines[key_index + 1:]:
        stripped = line.strip()
        if stripped and len(line) - len(line.lstrip()) <= 4 and not stripped.startswith("-"):
            break
        match = re.match(r"^\s+-\s+(.+)$", line)
        if match:
            values.append(match.group(1).strip().strip('"'))
    return values


def _set_metadata_list(lines: List[str], key: str, values: List[str]) -> None:
    values = list(dict.fromkeys(values))
    try:
        metadata_index = next(i for i, line in enumerate(lines) if line.strip() == "metadata:")
    except StopIteration as e:
        raise ValueError("Parent skill has no metadata block") from e

    key_index = None
    block_end = None
    for i in range(metadata_index + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped and len(lines[i]) - len(lines[i].lstrip()) == 0 and not stripped.startswith("-"):
            block_end = i
            break
        if lines[i] == f"    {key}:" or lines[i] == f"    {key}: []":
            key_index = i
            for j in range(i + 1, len(lines)):
                s = lines[j].strip()
                if s and len(lines[j]) - len(lines[j].lstrip()) <= 4 and not s.startswith("-"):
                    block_end = j
                    break
            else:
                block_end = len(lines)
            break
    if block_end is None:
        block_end = len(lines)

    replacement = [f"    {key}: []"] if not values else [f"    {key}:"] + [f"      - {v}" for v in values]
    if key_index is None:
        lines[block_end:block_end] = replacement
    else:
        lines[key_index:block_end] = replacement


def _find_skill(library: Path, name: str) -> Path:
    matches = sorted(library.glob(f"**/{name}/SKILL.md"))
    if not matches:
        raise ValueError(f"Skill {name!r} is not present in the test library")
    if len(matches) > 1:
        raise ValueError(f"Skill {name!r} is ambiguous in the test library: {matches}")
    return matches[0]


def _preflight_merge(library: Path, payload: Dict[str, Any]) -> Dict[str, Any]:
    validate_proposal("merge", payload)
    target = _find_skill(library, payload["target"])
    claims = payload.get("include_claims", [])
    if any(not c.get("text") for c in claims):
        raise ValueError("Merge proposal contains an empty claim")
    return {"kind": "merge", "target": target, "claims": claims}


def _preflight_granularity(library: Path, payload: Dict[str, Any]) -> Dict[str, Any]:
    validate_proposal("granularity", payload)
    if payload["action"] != "EXTRACT_FACET":
        raise ValueError(f"Granularity action {payload['action']} has no structural change to apply")

    parent = _find_skill(library, payload["parent"])
    source_path = payload.get("source_path")
    placement = payload.get("placement")
    metadata = payload.get("metadata")
    if not source_path:
        raise ValueError("Split proposal is missing its candidate source_path; re-run the test pipe")
    source_dir = Path(source_path)
    source_file = source_dir / "SKILL.md" if source_dir.is_dir() else source_dir
    if not source_file.exists():
        raise ValueError("Split proposal source SKILL.md does not exist; re-run the test pipe")
    if not isinstance(placement, dict) or not placement.get("category"):
        raise ValueError("Split proposal is missing placement; re-run the test pipe")
    if not isinstance(metadata, dict):
        raise ValueError("Split proposal is missing generated metadata; re-run the test pipe")

    name = payload["new_skill_name"]
    if not re.fullmatch(r"[a-z0-9_-]+", name):
        raise ValueError("new_skill_name must be a single kebab-case directory name")
    category = placement["category"]
    subcategory = placement.get("subcategory") or ""
    for part in (category, subcategory):
        if part and (not re.fullmatch(r"[a-z0-9_-]+", part) or part in {".", ".."}):
            raise ValueError(f"Unsafe placement component: {part!r}")
    destination = library / category / subcategory / name if subcategory else library / category / name
    if destination.exists():
        raise ValueError(f"Split destination already exists: {destination}")

    parent_content = parent.read_text(encoding="utf-8")
    parent_lines = parent_content.splitlines()
    removals = _claim_line_indices(parent_content, payload.get("parent_remove_claims", []))
    additions = payload.get("parent_composed_of_add", [])
    if payload["new_skill_id"] not in additions:
        additions = additions + [payload["new_skill_id"]]
    existing_composed = _metadata_list(parent_lines, "composed_of")

    return {
        "kind": "granularity",
        "parent": parent,
        "parent_lines": parent_lines,
        "removals": removals,
        "parent_composed_of": list(dict.fromkeys(existing_composed + additions)),
        "source_path": source_file,
        "destination": destination,
        "category": category,
        "subcategory": subcategory,
        "metadata": metadata,
        "payload": payload,
    }


def preflight_proposal(library: Path, envelope: Dict[str, Any]) -> Dict[str, Any]:
    if envelope.get("status") != "APPROVED":
        raise ValueError(f"Proposal {envelope['id']} is not APPROVED")
    payload = envelope["proposal"]
    if envelope["kind"] == "merge":
        return _preflight_merge(library, payload)
    return _preflight_granularity(library, payload)


def create_snapshot(library: Path, snapshots: Path, proposal_id: str) -> Path:
    snapshots.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    snapshot = snapshots / f"snap-{proposal_id}-{stamp}"
    shutil.copytree(library, snapshot / "library")
    (snapshot / "metadata.json").write_text(json.dumps({
        "snapshot": snapshot.name,
        "proposal_id": proposal_id,
        "library_path": str(library),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")
    return snapshot


def restore_snapshot(library: Path, snapshot: Path) -> None:
    source = snapshot / "library"
    if not source.exists():
        raise ValueError(f"Snapshot has no library payload: {snapshot}")
    if library.exists():
        shutil.rmtree(library)
    shutil.copytree(source, library)


def _append_ledger(library: Path, entry: Dict[str, Any]) -> None:
    ledger = library / "change-ledger.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def _update_manifest(library: Path, name: str, path: Path, category: str, subcategory: str, role: str, source: Path) -> None:
    manifest_path = library / "runtime-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"version": "1.0", "skills": {}}
    manifest.setdefault("skills", {})[name] = {
        "canonical_path": path.relative_to(library).as_posix(),
        "category": category,
        "subcategory": subcategory,
        "role": role,
        "source": str(source),
    }
    manifest["total_managed_skills"] = len(manifest["skills"])
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _apply_plan(library: Path, plan: Dict[str, Any], proposal_id: str, snapshot: Path) -> None:
    if plan["kind"] == "merge":
        target = plan["target"]
        content = target.read_text(encoding="utf-8")
        # Avoid duplicating a previously applied claim.
        body_norm = {_normalize_claim(line) for line in content.splitlines()}
        new_claims = [c for c in plan["claims"] if _normalize_claim(c.get("text", "")) not in body_norm]
        if new_claims:
            section = "\n\n## Merged Capabilities\n\n" + "\n".join(f"- {c['text']}" for c in new_claims) + "\n"
            target.write_text(content.rstrip() + section, encoding="utf-8")
        _append_ledger(library, {
            "action": "LIBRARIAN_APPLY", "proposal_id": proposal_id,
            "kind": "merge", "target": plan["target"].relative_to(library).as_posix(),
            "snapshot": snapshot.name, "claims_added": len(new_claims),
        })
        return

    payload = plan["payload"]
    parent = plan["parent"]
    parent_lines = plan["parent_lines"]
    for index in reversed(plan["removals"]):
        del parent_lines[index]
    _set_metadata_list(parent_lines, "composed_of", plan["parent_composed_of"])
    parent.write_text("\n".join(parent_lines) + "\n", encoding="utf-8")

    source_content = plan["source_path"].read_text(encoding="utf-8")
    source_fm, source_body = _split_frontmatter(source_content)
    description = _scalar(source_fm, "description", payload.get("scope", ""))
    license_id = _scalar(source_fm, "license", "MIT")
    metadata = copy.deepcopy(plan["metadata"])
    metadata["role"] = payload["role"]
    metadata["extends"] = payload.get("candidate_extends")
    metadata["depends_on"] = payload.get("candidate_depends_on", [])
    metadata["composed_of"] = []
    frontmatter = render_frontmatter(
        payload["new_skill_name"], description, metadata,
        payload["new_skill_id"], license_id=license_id,
    )
    plan["destination"].mkdir(parents=True, exist_ok=True)
    child_file = plan["destination"] / "SKILL.md"
    child_file.write_text(frontmatter + "\n" + source_body.strip() + "\n", encoding="utf-8")
    _update_manifest(
        library, payload["new_skill_name"], plan["destination"],
        plan["category"], plan["subcategory"], payload["role"], plan["source_path"],
    )
    _append_ledger(library, {
        "action": "LIBRARIAN_APPLY", "proposal_id": proposal_id,
        "kind": "granularity", "parent": parent.relative_to(library).as_posix(),
        "child": plan["destination"].relative_to(library).as_posix(),
        "snapshot": snapshot.name,
    })


def apply_proposal(library: Path, store: Path, snapshots: Path, envelope: Dict[str, Any]) -> Path:
    plan = preflight_proposal(library, envelope)
    snapshot = create_snapshot(library, snapshots, envelope["id"])
    try:
        _apply_plan(library, plan, envelope["id"], snapshot)
        from librarian_testpipe import generate_routers
        generate_routers(library)
        set_status(store, envelope["id"], "APPLIED", envelope.get("note", ""))
    except Exception:
        restore_snapshot(library, snapshot)
        raise
    return snapshot


def rollback(library: Path, store: Path, snapshots: Path, snapshot_id: str) -> Dict[str, Any]:
    if Path(snapshot_id).name != snapshot_id or snapshot_id in {".", ".."}:
        raise ValueError("Snapshot ID must be a single directory name")
    snapshot = snapshots / snapshot_id
    metadata_path = snapshot / "metadata.json"
    if not metadata_path.exists():
        raise ValueError(f"Unknown snapshot: {snapshot_id}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if Path(metadata["library_path"]).resolve() != library.resolve():
        raise ValueError("Snapshot belongs to a different test library")
    restore_snapshot(library, snapshot)
    proposal_id = metadata["proposal_id"]
    proposal = get_proposal(store, proposal_id)
    set_status(store, proposal_id, "ROLLED_BACK", f"Rolled back to {snapshot_id}")
    _append_ledger(library, {
        "action": "LIBRARIAN_ROLLBACK", "proposal_id": proposal_id,
        "snapshot": snapshot_id,
    })
    return proposal


def format_plan(plan: Dict[str, Any], library: Optional[Path] = None) -> str:
    if plan["kind"] == "merge":
        target = plan["target"].relative_to(library).as_posix() if library else str(plan["target"])
        return f"Merge {len(plan['claims'])} approved claims into {target}"
    parent = plan["parent"].relative_to(library).as_posix() if library else str(plan["parent"])
    child = plan["destination"].relative_to(library).as_posix() if library else str(plan["destination"])
    return (
        f"Extract {plan['payload']['new_skill_id']} from {parent}\n"
        f"  child: {child}\n"
        f"  parent claim lines removed: {len(plan['removals'])}\n"
        f"  parent composed_of: {', '.join(plan['parent_composed_of'])}"
    )
