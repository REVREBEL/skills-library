"""
Librarian: AI-powered skill intake and merge evaluation.

The Librarian is the single gate through which every skill passes before
entering the library. It replaces the keyword-matching heuristic in
scanner.py with a pipeline of specialized steps:

1. DETERMINISTIC GATE (scanner.py) — structure, secrets, AST, hashes
2. SIMILARITY RETRIEVAL (this module) — Dice on name+desc+body → top 50
3. RERANK (this module) — rerank-class model → top 5
4. RELATIONSHIP GATE (this module) — self / duplicate / overlap / unrelated
5. CLAIM EXTRACTION (this module) — atomic operational claims
6. CLAIM DIFF + CONFLICT DETECTION (this module) — lexical diff, semantic conflicts
7. GRANULARITY PROPOSAL (this module) — one incremental, non-destructive split
8. MERGE DECISION (this module) — include / skip / escalate
9. HUMAN GATE (intake.py) — approve / edit / reject

The design principle: scripts produce candidates and enforce invariants;
AI produces meaning and proposes structure. Scripts never guess at
semantics. AI never moves files or computes hashes.

Steps 2, 4, 5, 6 are in this module. Steps 1, 7 are in scanner.py and
intake.py respectively.
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .intake import (
    _extract_body_for_similarity,
    compute_dice_similarity,
    tokenize,
)
from .scanner import CandidatePackage

# --- Configuration ---

# Number of candidates to retrieve before reranking.
DICE_RETRIEVAL_LIMIT = 50

# Minimum Dice similarity to include a candidate in the retrieval pool.
DICE_THRESHOLD = 0.25

# Number of candidates to keep after reranking.
RERANK_TOP_N = 5

# Minimum similarity for a self-match (same name, different path) to count
# as a duplicate hit.
SELF_MATCH_THRESHOLD = 0.5

# Maximum lines of body to use for claim extraction.
CLAIM_BODY_LINES = 120


# --- Data structures ---

@dataclass
class RetrievedCandidate:
    """A candidate skill retrieved from the catalog by Dice similarity."""
    name: str
    canonical_path: str
    similarity: float
    description: str
    body_sample: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "canonical_path": self.canonical_path,
            "similarity": self.similarity,
            "description": self.description,
        }


@dataclass
class RerankedCandidate:
    """A candidate skill scored by the rerank model."""
    name: str
    canonical_path: str
    rerank_score: float
    dice_similarity: float
    description: str
    body_sample: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "canonical_path": self.canonical_path,
            "rerank_score": self.rerank_score,
            "dice_similarity": self.dice_similarity,
        }


@dataclass
class Claim:
    """An atomic, verifiable instruction extracted from a skill body."""
    id: str
    text: str
    claim_type: str  # "operational" | "explanatory"
    source: str  # skill name this claim came from

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "type": self.claim_type,
            "source": self.source,
        }


@dataclass
class ClaimConflict:
    """A true semantic contradiction between a candidate and existing claim."""
    candidate: Claim
    existing: Claim
    reason: str
    severity: str = "warning"  # "warning" | "critical"

    def to_dict(self) -> dict:
        return {
            "candidate": self.candidate.to_dict(),
            "existing": self.existing.to_dict(),
            "reason": self.reason,
            "severity": self.severity,
        }


@dataclass
class ClaimDiff:
    """The set difference between two skills' claims."""
    added: List[Claim] = field(default_factory=list)  # claims in skill 2 but not skill 1
    restatement: List[Claim] = field(default_factory=list)  # claims in skill 2 that restate skill 1
    conflict: List[ClaimConflict] = field(default_factory=list)  # true semantic contradictions
    unchanged: int = 0  # claims in both

    @property
    def conflict_candidates(self) -> List[Claim]:
        """Candidate claims that must be escalated rather than merged."""
        return [c.candidate for c in self.conflict]

    def to_dict(self) -> dict:
        return {
            "added": [c.to_dict() for c in self.added],
            "restatement": [c.to_dict() for c in self.restatement],
            "conflict": [c.to_dict() for c in self.conflict],
            "unchanged": self.unchanged,
        }


@dataclass
class GranularityProposal:
    """A non-destructive proposal to extract one independently shippable facet.

    The Librarian never applies this automatically. A human approves the
    proposal before the parent body, relationships, or catalog are changed.
    """
    parent: str
    candidate: str
    action: str  # EXTRACT_FACET | KEEP_SEPARATE | MERGE | NO_SPLIT
    new_skill_name: Optional[str] = None
    new_skill_id: Optional[str] = None
    role: Optional[str] = None
    scope: str = ""
    extracted_claim_ids: List[str] = field(default_factory=list)
    parent_remove_claim_ids: List[str] = field(default_factory=list)
    extracted_claims: List[Claim] = field(default_factory=list)
    parent_remove_claims: List[Claim] = field(default_factory=list)
    parent_composed_of_add: List[str] = field(default_factory=list)
    candidate_extends: Optional[str] = None
    candidate_depends_on: List[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: str = "low"

    def to_dict(self) -> dict:
        return {
            "parent": self.parent,
            "candidate": self.candidate,
            "action": self.action,
            "new_skill_name": self.new_skill_name,
            "new_skill_id": self.new_skill_id,
            "role": self.role,
            "scope": self.scope,
            "extracted_claim_ids": self.extracted_claim_ids,
            "parent_remove_claim_ids": self.parent_remove_claim_ids,
            "extracted_claims": [c.to_dict() for c in self.extracted_claims],
            "parent_remove_claims": [c.to_dict() for c in self.parent_remove_claims],
            "parent_composed_of_add": self.parent_composed_of_add,
            "candidate_extends": self.candidate_extends,
            "candidate_depends_on": self.candidate_depends_on,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "status": "PROPOSED",
        }

    def summary(self) -> str:
        lines = [
            f"GRANULARITY PROPOSAL: {self.candidate} relative to {self.parent}",
            f"Action: {self.action} (confidence: {self.confidence})",
        ]
        if self.action == "EXTRACT_FACET":
            lines.extend([
                f"New skill: {self.new_skill_name} ({self.new_skill_id})",
                f"Role: {self.role}",
                f"Scope: {self.scope}",
                f"Extract candidate claims: {', '.join(self.extracted_claim_ids) or '(none)'}",
                f"Remove from parent: {', '.join(self.parent_remove_claim_ids) or '(none)'}",
                f"Parent composed_of += {', '.join(self.parent_composed_of_add) or '(none)'}",
                f"Candidate extends: {self.candidate_extends or '(none)'}",
                f"Candidate depends_on: {', '.join(self.candidate_depends_on) or '(none)'}",
            ])
        lines.extend([
            f"Reasoning: {self.reasoning}",
            "Status: PROPOSED — human approval required",
        ])
        return "\n".join(lines)


def build_granularity_proposal(
    data: Dict[str, Any],
    parent: str,
    candidate: str,
    existing_claims: List[Claim],
    candidate_claims: List[Claim],
) -> GranularityProposal:
    """Validate AI output into a safe, non-destructive granularity proposal."""
    allowed_actions = {"EXTRACT_FACET", "KEEP_SEPARATE", "MERGE", "NO_SPLIT"}
    action = data.get("action", "NO_SPLIT")
    if action not in allowed_actions:
        action = "NO_SPLIT"

    confidence = data.get("confidence", "low")
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"

    existing_ids = {c.id for c in existing_claims}
    candidate_ids = {c.id for c in candidate_claims}

    def _ids(key: str, valid: Set[str]) -> List[str]:
        values = data.get(key, [])
        if not isinstance(values, list):
            return []
        return [v for v in values if isinstance(v, str) and v in valid]

    new_name = data.get("new_skill_name")
    new_id = data.get("new_skill_id")
    role = data.get("role")
    scope = data.get("scope", "")
    extracted = _ids("extracted_claim_ids", candidate_ids)
    parent_remove = _ids("parent_remove_claim_ids", existing_ids)
    candidate_by_id = {c.id: c for c in candidate_claims}
    existing_by_id = {c.id: c for c in existing_claims}
    extracted_claims = [candidate_by_id[i] for i in extracted]
    parent_remove_claims = [existing_by_id[i] for i in parent_remove]
    composed_add = data.get("parent_composed_of_add", [])
    if not isinstance(composed_add, list):
        composed_add = []
    composed_add = [v for v in composed_add if isinstance(v, str)]

    candidate_depends_on = data.get("candidate_depends_on", [])
    if not isinstance(candidate_depends_on, list):
        candidate_depends_on = []
    candidate_depends_on = [v for v in candidate_depends_on if isinstance(v, str)]

    reasoning = data.get("reasoning", "")
    if not isinstance(reasoning, str):
        reasoning = ""

    # An extraction without a concrete, independently shippable child is not
    # actionable. Fail safe to NO_SPLIT rather than inventing structure.
    if action == "EXTRACT_FACET":
        valid_id = isinstance(new_id, str) and re.fullmatch(r"[a-z0-9_-]+:[a-z0-9_-]+", new_id)
        if not (isinstance(new_name, str) and new_name.strip() and valid_id
                and role in {"capability", "workflow", "primitive", "overlay", "adapter", "reference", "alias"}
                and isinstance(scope, str) and scope.strip() and extracted):
            action = "NO_SPLIT"
            confidence = "low"
            reasoning = "Incomplete extraction proposal; no structural change proposed."

    return GranularityProposal(
        parent=parent,
        candidate=candidate,
        action=action,
        new_skill_name=new_name if isinstance(new_name, str) else None,
        new_skill_id=new_id if isinstance(new_id, str) else None,
        role=role if isinstance(role, str) else None,
        scope=scope if isinstance(scope, str) else "",
        extracted_claim_ids=extracted,
        parent_remove_claim_ids=parent_remove,
        extracted_claims=extracted_claims,
        parent_remove_claims=parent_remove_claims,
        parent_composed_of_add=composed_add,
        candidate_extends=data.get("candidate_extends") if isinstance(data.get("candidate_extends"), str) else None,
        candidate_depends_on=candidate_depends_on,
        reasoning=reasoning,
        confidence=confidence,
    )


@dataclass
class MergeProposal:
    """The Librarian's proposal for merging skill 2 into skill 1."""
    target: str  # skill 1 name
    candidate: str  # skill 2 name
    verdict: str  # "SUPPLEMENT" | "EXTEND" | "CONFLICT" | "ALIAS" | "REJECT"
    confidence: str  # "high" | "medium" | "low"
    claim_diff: ClaimDiff = field(default_factory=ClaimDiff)
    include_claims: List[Claim] = field(default_factory=list)
    skip_claims: List[Claim] = field(default_factory=list)
    escalate_claims: List[Claim] = field(default_factory=list)
    reasoning: str = ""

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "candidate": self.candidate,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "claim_diff": self.claim_diff.to_dict(),
            "include_claims": [c.to_dict() for c in self.include_claims],
            "skip_claims": [c.to_dict() for c in self.skip_claims],
            "escalate_claims": [c.to_dict() for c in self.escalate_claims],
            "reasoning": self.reasoning,
        }

    def summary(self) -> str:
        """Human-readable summary for the review card."""
        lines = [
            f"MERGE {self.candidate} → {self.target}",
            "",
            f"Verdict: {self.verdict} (confidence: {self.confidence})",
            "",
        ]

        if self.include_claims:
            lines.append("  INCLUDE:")
            for c in self.include_claims:
                lines.append(f"    + [{c.id}] {c.text}")

        if self.skip_claims:
            lines.append("  SKIP:")
            for c in self.skip_claims:
                lines.append(f"    ~ [{c.id}] {c.text}")

        if self.escalate_claims:
            lines.append("  ESCALATE:")
            conflict_reasons = {
                c.candidate.id: c.reason for c in self.claim_diff.conflict
            }
            for c in self.escalate_claims:
                reason = conflict_reasons.get(c.id)
                suffix = f" — {reason}" if reason else ""
                lines.append(f"    ! [{c.id}] {c.text}{suffix}")

        lines.append("")
        lines.append(f"  Net: {len(self.include_claims)} to add, "
                      f"{len(self.skip_claims)} to skip, "
                      f"{len(self.escalate_claims)} to escalate")
        lines.append(f"  Confidence: {self.confidence.upper()}")

        return "\n".join(lines)


# --- Step 2: Dice retrieval ---

def retrieve_candidates(
    candidate_name: str,
    candidate_description: str,
    candidate_body: str,
    catalog: List[Dict[str, Any]],
    limit: int = DICE_RETRIEVAL_LIMIT,
    threshold: float = DICE_THRESHOLD,
) -> List[RetrievedCandidate]:
    """Stage 1: Retrieve candidates from the catalog using Dice similarity.

    Tokenizes name + description + body sample and compares against every
    catalog entry. Returns the top ``limit`` candidates above ``threshold``.
    """
    candidate_tokens = tokenize(
        candidate_name + " " + candidate_description + " " + candidate_body
    )

    scored: List[RetrievedCandidate] = []
    for entry in catalog:
        entry_tokens = entry.get("tokens", set())
        if not entry_tokens:
            continue
        sim = compute_dice_similarity(candidate_tokens, entry_tokens)
        if sim >= threshold:
            scored.append(RetrievedCandidate(
                name=entry["name"],
                canonical_path=entry["canonical_path"],
                similarity=round(sim, 4),
                description=entry.get("description", ""),
                body_sample=entry.get("body_sample", ""),
            ))

    scored.sort(key=lambda c: c.similarity, reverse=True)
    return scored[:limit]


# --- Step 4: Rerank (interface for external rerank model) ---

def rerank_candidates(
    query: str,
    candidates: List[RetrievedCandidate],
    rerank_fn: Optional[callable] = None,
) -> List[RerankedCandidate]:
    """Stage 2: Rerank candidates using a rerank-class model.

    ``rerank_fn`` is a callable that takes (query, [passage_texts]) and
    returns [(index, score)]. If not provided, returns candidates in Dice
    order (no reranking).

    The rerank step refines duplicate ranking — it pushes the true match
    to the top when Dice returns a large pool. It does NOT catch
    related-but-different skills; that's the claim diff's job.
    """
    if rerank_fn is None or not candidates:
        return [
            RerankedCandidate(
                name=c.name,
                canonical_path=c.canonical_path,
                rerank_score=c.similarity,
                dice_similarity=c.similarity,
                description=c.description,
                body_sample=c.body_sample,
            )
            for c in candidates
        ]

    # Build passage texts for the reranker
    passages = [
        f"{c.name}: {c.description}"
        for c in candidates
    ]

    # Call the rerank function
    scores = rerank_fn(query, passages)

    # Sort by rerank score
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)

    return [
        RerankedCandidate(
            name=candidates[idx].name,
            canonical_path=candidates[idx].canonical_path,
            rerank_score=round(score, 4),
            dice_similarity=candidates[idx].similarity,
            description=candidates[idx].description,
            body_sample=candidates[idx].body_sample,
        )
        for idx, score in ranked
    ]


# --- Step 5: Claim extraction (interface for AI model) ---

def extract_claims(
    skill_name: str,
    skill_body: str,
    extract_fn: Optional[callable] = None,
) -> List[Claim]:
    """Stage 3: Extract atomic claims from a skill body.

    ``extract_fn`` is a callable that takes (skill_name, body_text) and
    returns [{"id": "C1", "text": "...", "type": "operational"|"explanatory"}].

    If not provided, returns an empty list (no extraction).

    Claims are atomic, verifiable instructions — one config change, one
    command, one verification step. Not sentences, not words.
    """
    if extract_fn is None:
        return []

    raw_claims = extract_fn(skill_name, skill_body)

    claims = []
    for c in raw_claims:
        claims.append(Claim(
            id=c.get("id", ""),
            text=c.get("text", ""),
            claim_type=c.get("type", "operational"),
            source=skill_name,
        ))
    return claims


# --- Step 5: Claim diff (deterministic) ---

def diff_claims(
    skill1_claims: List[Claim],
    skill2_claims: List[Claim],
) -> ClaimDiff:
    """Stage 3: Compute the set difference between two skills' claims.

    This is pure set arithmetic — no model call. Returns:
    - added: claims in skill 2 but not skill 1
    - restatement: claims in skill 2 that restate skill 1 (same meaning, different words)
    - conflict: claims in skill 2 that contradict skill 1
    - unchanged: claims in both

    For now, restatement and conflict detection require semantic comparison,
    which is the decision model's job. This function does lexical matching
    only: exact text match = unchanged, high token overlap = restatement.
    """
    # Build a set of normalized skill 1 claims for fast lookup
    skill1_texts = {}
    for c in skill1_claims:
        normalized = _normalize_claim(c.text)
        skill1_texts[normalized] = c

    skill1_tokens = {c.id: tokenize(c.text) for c in skill1_claims}

    added = []
    restatement = []
    unchanged = 0

    for c2 in skill2_claims:
        norm2 = _normalize_claim(c2.text)

        # Exact match → unchanged
        if norm2 in skill1_texts:
            unchanged += 1
            continue

        # High token overlap → restatement
        tokens2 = tokenize(c2.text)
        best_overlap = 0.0
        for c1_id, c1_tokens in skill1_tokens.items():
            if not tokens2 or not c1_tokens:
                continue
            overlap = len(tokens2 & c1_tokens) / max(len(tokens2), len(c1_tokens))
            if overlap > best_overlap:
                best_overlap = overlap

        if best_overlap >= 0.7:
            restatement.append(c2)
        else:
            added.append(c2)

    return ClaimDiff(
        added=added,
        restatement=restatement,
        conflict=[],  # Conflict detection requires semantic comparison (decision model)
        unchanged=unchanged,
    )


def apply_semantic_conflicts(
    claim_diff: ClaimDiff,
    existing_claims: List[Claim],
    conflict_records: List[Dict[str, Any]],
) -> ClaimDiff:
    """Enrich a lexical ClaimDiff with AI-detected semantic conflicts.

    ``conflict_records`` contains dicts with candidate_id, existing_id,
    reason, and optional severity. Conflicted candidate claims are removed
    from ``added`` so they cannot be silently included by the merge step.
    """
    if not conflict_records:
        return claim_diff

    existing_by_id = {c.id: c for c in existing_claims}
    added_by_id = {c.id: c for c in claim_diff.added}
    conflicted_ids = set()

    for record in conflict_records:
        candidate_id = record.get("candidate_id")
        existing_id = record.get("existing_id")
        candidate = added_by_id.get(candidate_id)
        existing = existing_by_id.get(existing_id)
        if candidate is None or existing is None:
            continue
        severity = record.get("severity", "warning")
        if severity not in ("warning", "critical"):
            severity = "warning"
        claim_diff.conflict.append(ClaimConflict(
            candidate=candidate,
            existing=existing,
            reason=record.get("reason", "Semantic contradiction detected"),
            severity=severity,
        ))
        conflicted_ids.add(candidate_id)

    if conflicted_ids:
        claim_diff.added = [c for c in claim_diff.added if c.id not in conflicted_ids]

    return claim_diff


def _normalize_claim(text: str) -> str:
    """Normalize a claim for comparison: lowercase, strip punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


# --- Step 6: Merge decision (interface for decision model) ---

def decide_merge(
    skill1_name: str,
    skill2_name: str,
    claim_diff: ClaimDiff,
    decide_fn: Optional[callable] = None,
) -> MergeProposal:
    """Stage 4: Decide how to merge skill 2 into skill 1.

    ``decide_fn`` is a callable that takes (skill1_name, skill2_name, claim_diff)
    and returns a dict with:
    - verdict: "SUPPLEMENT" | "EXTEND" | "CONFLICT" | "ALIAS" | "REJECT"
    - confidence: "high" | "medium" | "low"
    - include_claims: list of claim IDs to include
    - skip_claims: list of claim IDs to skip
    - escalate_claims: list of claim IDs to escalate
    - reasoning: string explanation

    If not provided, returns a default proposal (all added claims included,
    high confidence).
    """
    if decide_fn is None:
        return MergeProposal(
            target=skill1_name,
            candidate=skill2_name,
            verdict="SUPPLEMENT",
            confidence="high",
            claim_diff=claim_diff,
            include_claims=claim_diff.added,
            skip_claims=claim_diff.restatement,
            escalate_claims=claim_diff.conflict_candidates,
            reasoning="Default: all non-restatement claims included.",
        )

    result = decide_fn(skill1_name, skill2_name, claim_diff)

    # Map claim IDs back to Claim objects
    include = _claims_by_id(claim_diff.added, result.get("include_claims", []))
    skip = _claims_by_id(claim_diff.restatement + claim_diff.added, result.get("skip_claims", []))
    escalate = _claims_by_id(claim_diff.conflict_candidates + claim_diff.added, result.get("escalate_claims", []))

    # Hard safety rule: a detected semantic conflict can never be included
    # or skipped, even if the decision model omits it from escalate_claims.
    for conflicted in claim_diff.conflict_candidates:
        if conflicted not in escalate:
            escalate.append(conflicted)
        include = [c for c in include if c.id != conflicted.id]
        skip = [c for c in skip if c.id != conflicted.id]

    return MergeProposal(
        target=skill1_name,
        candidate=skill2_name,
        verdict=result.get("verdict", "SUPPLEMENT"),
        confidence=result.get("confidence", "medium"),
        claim_diff=claim_diff,
        include_claims=include,
        skip_claims=skip,
        escalate_claims=escalate,
        reasoning=result.get("reasoning", ""),
    )


def _claims_by_id(claims: List[Claim], ids: List[str]) -> List[Claim]:
    """Filter claims to those whose IDs are in the given list."""
    id_set = set(ids)
    return [c for c in claims if c.id in id_set]


# --- Pipeline orchestration ---

def run_librarian_pipeline(
    candidate: CandidatePackage,
    catalog: List[Dict[str, Any]],
    extract_fn: Optional[callable] = None,
    rerank_fn: Optional[callable] = None,
    decide_fn: Optional[callable] = None,
) -> Dict[str, Any]:
    """Run the full Librarian pipeline on a candidate.

    Returns a dict with:
    - retrieved: top candidates from Dice
    - reranked: top candidates after reranking
    - merge_proposals: list of MergeProposal objects (one per reranked candidate)
    - recommended_action: "NEW" | "MERGE" | "SUPPLEMENT" | "CONFLICT" | "REVIEW"

    This is the main entry point for the Librarian. Steps 1 (scan) and
    7 (human gate) are handled by the caller.
    """
    # Step 2: Retrieve candidates
    retrieved = retrieve_candidates(
        candidate_name=candidate.name,
        candidate_description=candidate.description,
        candidate_body=candidate.body_sample,
        catalog=catalog,
    )

    # Step 4: Rerank
    reranked = rerank_candidates(
        query=candidate.description,
        candidates=retrieved,
        rerank_fn=rerank_fn,
    )

    # Step 5: Extract claims from candidate
    candidate_claims = extract_claims(
        skill_name=candidate.name,
        skill_body=candidate.body_sample,
        extract_fn=extract_fn,
    )

    # Steps 5-6: For each reranked candidate, diff claims and decide merge
    merge_proposals = []
    for rc in reranked:
        # Extract claims from the existing skill
        existing_claims = extract_claims(
            skill_name=rc.name,
            skill_body=rc.body_sample if hasattr(rc, 'body_sample') else "",
            extract_fn=extract_fn,
        )

        # Diff claims
        claim_diff = diff_claims(existing_claims, candidate_claims)

        # Decide merge
        proposal = decide_merge(
            skill1_name=rc.name,
            skill2_name=candidate.name,
            claim_diff=claim_diff,
            decide_fn=decide_fn,
        )
        merge_proposals.append(proposal)

    # Determine recommended action
    if not retrieved:
        recommended = "NEW"
    else:
        top_proposal = merge_proposals[0] if merge_proposals else None
        if top_proposal:
            if top_proposal.escalate_claims:
                recommended = "CONFLICT"
            elif top_proposal.verdict == "SUPPLEMENT" and top_proposal.include_claims:
                recommended = "SUPPLEMENT"
            elif top_proposal.verdict in ("ALIAS", "REJECT"):
                recommended = top_proposal.verdict
            else:
                recommended = "REVIEW"
        else:
            recommended = "REVIEW"

    return {
        "retrieved": [c.to_dict() for c in retrieved],
        "reranked": [c.to_dict() for c in reranked],
        "merge_proposals": [p.to_dict() for p in merge_proposals],
        "recommended_action": recommended,
    }