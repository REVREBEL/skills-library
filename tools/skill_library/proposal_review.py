"""Review store for Librarian merge and granularity proposals.

Proposals are non-destructive. This module only records them and manages
human decisions; it never changes a skill, router, manifest, or ledger.
"""

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

VALID_STATUSES = {"PROPOSED", "APPROVED", "REJECTED", "APPLIED", "ROLLED_BACK"}
VALID_KINDS = {"merge", "granularity"}


def _canonical_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def proposal_id(kind: str, payload: Dict[str, Any]) -> str:
    """Return a stable ID for an exact proposal payload."""
    digest = hashlib.sha256(f"{kind}:{_canonical_json(payload)}".encode("utf-8")).hexdigest()[:12]
    return f"{kind}-{digest}"


def load_proposals(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid proposal store {path}: {e}") from e
    if not isinstance(data, list):
        raise ValueError(f"Proposal store {path} must contain a JSON array")
    return data


def save_proposals(path: Path, proposals: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proposals, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_proposal(kind: str, payload: Dict[str, Any]) -> None:
    if kind not in VALID_KINDS:
        raise ValueError(f"Unknown proposal kind: {kind}")
    if not isinstance(payload, dict):
        raise ValueError("Proposal payload must be a JSON object")

    if kind == "merge":
        required = {"target", "candidate", "verdict", "confidence", "claim_diff"}
        missing = sorted(required - set(payload))
        if missing:
            raise ValueError(f"Merge proposal missing fields: {', '.join(missing)}")
        if payload["verdict"] not in {"SUPPLEMENT", "EXTEND", "CONFLICT", "ALIAS", "REJECT"}:
            raise ValueError(f"Invalid merge verdict: {payload['verdict']}")
        if payload["confidence"] not in {"high", "medium", "low"}:
            raise ValueError(f"Invalid merge confidence: {payload['confidence']}")
        if not isinstance(payload["claim_diff"], dict):
            raise ValueError("Merge claim_diff must be an object")
        conflicts = payload["claim_diff"].get("conflict", [])
        conflict_ids = {
            c.get("candidate", {}).get("id") for c in conflicts if isinstance(c, dict)
        }
        include_ids = {c.get("id") for c in payload.get("include_claims", []) if isinstance(c, dict)}
        escalate_ids = {c.get("id") for c in payload.get("escalate_claims", []) if isinstance(c, dict)}
        if conflict_ids & include_ids:
            raise ValueError("Conflicting claims cannot be included in a merge")
        if not conflict_ids <= escalate_ids:
            raise ValueError("Every semantic conflict must be escalated")
        return

    required = {"parent", "candidate", "action", "confidence", "reasoning"}
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"Granularity proposal missing fields: {', '.join(missing)}")
    if payload["action"] not in {"EXTRACT_FACET", "KEEP_SEPARATE", "MERGE", "NO_SPLIT"}:
        raise ValueError(f"Invalid granularity action: {payload['action']}")
    if payload["confidence"] not in {"high", "medium", "low"}:
        raise ValueError(f"Invalid granularity confidence: {payload['confidence']}")
    if payload["action"] == "EXTRACT_FACET":
        for field in ("new_skill_name", "new_skill_id", "role", "scope"):
            if not payload.get(field):
                raise ValueError(f"EXTRACT_FACET requires {field}")
        if not re.fullmatch(r"[a-z0-9_-]+:[a-z0-9_-]+", payload["new_skill_id"]):
            raise ValueError("new_skill_id must use scope:slug format")
        if not payload.get("extracted_claim_ids"):
            raise ValueError("EXTRACT_FACET requires extracted_claim_ids")


def upsert_proposal(path: Path, kind: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a proposal or return the existing identical proposal.

    Re-running the test pipe does not duplicate proposals or erase a human
    decision already made about the exact same payload.
    """
    validate_proposal(kind, payload)
    proposals = load_proposals(path)
    pid = proposal_id(kind, payload)
    for existing in proposals:
        if existing["id"] == pid:
            return existing

    envelope = {
        "id": pid,
        "kind": kind,
        "status": "PROPOSED",
        "revision": 1,
        "note": "",
        "proposal": copy.deepcopy(payload),
    }
    proposals.append(envelope)
    save_proposals(path, proposals)
    return envelope


def get_proposal(path: Path, proposal_id_: str) -> Dict[str, Any]:
    for proposal in load_proposals(path):
        if proposal["id"] == proposal_id_:
            return proposal
    raise KeyError(proposal_id_)


def set_status(path: Path, proposal_id_: str, status: str, note: str = "") -> Dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    proposals = load_proposals(path)
    for proposal in proposals:
        if proposal["id"] == proposal_id_:
            proposal["status"] = status
            proposal["note"] = note
            save_proposals(path, proposals)
            return proposal
    raise KeyError(proposal_id_)


def edit_proposal(path: Path, proposal_id_: str, payload: Dict[str, Any], note: str = "") -> Dict[str, Any]:
    proposals = load_proposals(path)
    for index, proposal in enumerate(proposals):
        if proposal["id"] != proposal_id_:
            continue
        if proposal["status"] not in {"PROPOSED", "APPROVED"}:
            raise ValueError(f"Cannot edit a {proposal['status']} proposal")
        validate_proposal(proposal["kind"], payload)
        new_id = proposal_id(proposal["kind"], payload)
        if any(p["id"] == new_id for i, p in enumerate(proposals) if i != index):
            raise ValueError(f"Edited proposal duplicates existing proposal {new_id}")
        edited = {
            "id": new_id,
            "kind": proposal["kind"],
            "status": "PROPOSED",
            "revision": proposal["revision"] + 1,
            "note": note,
            "proposal": copy.deepcopy(payload),
        }
        proposals[index] = edited
        save_proposals(path, proposals)
        return edited
    raise KeyError(proposal_id_)


def format_proposal(envelope: Dict[str, Any]) -> str:
    payload = envelope["proposal"]
    lines = [
        f"ID: {envelope['id']}",
        f"Kind: {envelope['kind']}",
        f"Status: {envelope['status']}",
        f"Revision: {envelope['revision']}",
    ]
    if envelope.get("note"):
        lines.append(f"Note: {envelope['note']}")

    if envelope["kind"] == "merge":
        lines.extend([
            "",
            f"MERGE {payload['candidate']} -> {payload['target']}",
            f"Verdict: {payload['verdict']} (confidence: {payload['confidence']})",
        ])
        for label, key, marker in (
            ("INCLUDE", "include_claims", "+"),
            ("SKIP", "skip_claims", "~"),
            ("ESCALATE", "escalate_claims", "!"),
        ):
            claims = payload.get(key, [])
            if claims:
                lines.append(f"{label}:")
                for claim in claims:
                    lines.append(f"  {marker} [{claim.get('id')}] {claim.get('text', '')}")
        conflicts = payload.get("claim_diff", {}).get("conflict", [])
        if conflicts:
            lines.append("CONFLICTS:")
            for conflict in conflicts:
                lines.append(
                    f"  ! {conflict['candidate'].get('id')} <-> {conflict['existing'].get('id')}: "
                    f"{conflict.get('reason', '')}"
                )
        if payload.get("reasoning"):
            lines.append(f"Reasoning: {payload['reasoning']}")
    else:
        lines.extend([
            "",
            f"GRANULARITY: {payload['candidate']} relative to {payload['parent']}",
            f"Action: {payload['action']} (confidence: {payload['confidence']})",
        ])
        if payload["action"] == "EXTRACT_FACET":
            lines.extend([
                f"New skill: {payload.get('new_skill_name')} ({payload.get('new_skill_id')})",
                f"Role: {payload.get('role')}",
                f"Scope: {payload.get('scope')}",
                f"Extract claims: {', '.join(payload.get('extracted_claim_ids', []))}",
                f"Remove from parent: {', '.join(payload.get('parent_remove_claim_ids', []))}",
                f"Parent composed_of += {', '.join(payload.get('parent_composed_of_add', []))}",
            ])
        lines.append(f"Reasoning: {payload.get('reasoning', '')}")
        lines.append("Status: PROPOSED — human approval required")
    return "\n".join(lines)
