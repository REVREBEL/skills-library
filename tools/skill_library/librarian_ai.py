"""
Cloudflare Workers AI bindings for the Librarian.

Provides the concrete implementations of the rerank and claim extraction
steps using @cf/baai/bge-reranker-base and a general chat model.

These are called from the execute harness where the Cloudflare AI API
is available. In production, they'd be HTTP calls to the Workers AI API.
"""

import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

# --- Configuration ---

# Model for claim extraction (reading comprehension over skill bodies).
CLAIM_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"

# Model for merge decisions (bounded classification with confidence).
DECISION_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"


# --- OpenCode CLI bridge ---

def opencode_run(prompt: str, model: str = CLAIM_MODEL, timeout: int = 120) -> str:
    """Run a prompt through the OpenCode CLI and return the response text.

    Uses `opencode run --model <model> <prompt>`. The CLI handles session
    management, model routing, and API calls. The response is the last
    assistant message.

    This is the concrete implementation of the AI steps. It shells out to
    the `opencode` CLI, which must be installed and on PATH.
    """
    try:
        result = subprocess.run(
            ["opencode", "run", "--model", model, prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"opencode run failed (exit {result.returncode}): {result.stderr[:200]}"
            )
        # The CLI prints the session header followed by the response.
        # Strip the header line (starts with ">") and return the rest.
        lines = result.stdout.strip().split("\n")
        response_lines = [l for l in lines if not l.startswith(">") and not l.startswith("[0m")]
        return "\n".join(response_lines).strip()
    except FileNotFoundError:
        raise RuntimeError(
            "opencode CLI not found. Install OpenCode or add it to PATH."
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"opencode run timed out after {timeout}s")

# --- Rerank ---

def rerank_with_bge(
    query: str,
    passages: List[str],
) -> List[Tuple[int, float]]:
    """Rerank passages using @cf/baai/bge-reranker-base.

    Returns [(index, score)] sorted by score descending.

    This function is called from the execute harness where the
    Cloudflare AI API is available. In production, it would be an
    HTTP call to the Workers AI API.
    """
    # This is a placeholder — the actual call is made from the execute
    # harness where tools.cloudflare.ai_run is available.
    # In production, this would be:
    #   POST /accounts/{account_id}/ai/run/@cf/baai/bge-reranker-base
    #   body: { input: { query, contexts: [{text: p} for p in passages] } }
    raise NotImplementedError(
        "rerank_with_bge must be called from the execute harness "
        "where the Cloudflare AI API is available."
    )


# --- Claim extraction ---

CLAIM_EXTRACTION_PROMPT = """You are extracting atomic claims from a skill's SKILL.md body.

A claim is a discrete, verifiable instruction — one config change, one command,
one verification step. Not sentences, not words.

Rules:
1. Extract claims at the level of discrete verifiable actions.
   - GOOD: "Install via apt on Debian/Ubuntu" (one action)
   - GOOD: "Configure postgresql.conf for remote access" (one config)
   - BAD: "Install and configure PostgreSQL" (two actions merged)
   - BAD: "PostgreSQL is a powerful database" (explanation, not action)

2. Classify each claim:
   - "operational": changes what the skill DOES (a flag, a config, a step)
   - "explanatory": explains WHY or provides context (background, rationale)

3. Default to operational over explanatory. If a claim is borderline,
   classify it as operational.

4. Return a JSON array. No prose, no markdown.

Skill: {skill_name}

Body:
{body}

Return JSON:
[
  {{"id": "C1", "text": "...", "type": "operational"}},
  {{"id": "C2", "text": "...", "type": "explanatory"}}
]"""


def build_claim_extraction_prompt(skill_name: str, body: str) -> str:
    """Build the prompt for claim extraction."""
    return CLAIM_EXTRACTION_PROMPT.format(
        skill_name=skill_name,
        body=body[:4000],  # Cap at 4000 chars to stay within context
    )


def parse_claim_extraction_response(response: str) -> List[Dict[str, Any]]:
    """Parse the model's response into a list of claims."""
    # Strip markdown code fences if present
    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        claims = json.loads(response)
        if not isinstance(claims, list):
            return []

        result = []
        for i, c in enumerate(claims):
            if not isinstance(c, dict):
                continue
            result.append({
                "id": c.get("id", f"C{i+1}"),
                "text": c.get("text", ""),
                "type": c.get("type", "operational"),
            })
        return result
    except json.JSONDecodeError:
        return []


# --- Merge decision ---

MERGE_DECISION_PROMPT = """You are deciding how to merge a candidate skill into an existing skill.

Existing skill: {skill1_name}
Candidate skill: {skill2_name}

Claim diff:
  Added (in candidate but not existing): {added_claims}
  Restatement (same as existing): {restatement_claims}
  Conflict (contradicts existing): {conflict_claims}

For each "added" claim, decide:
- INCLUDE: operational claim that adds real capability
- SKIP: explanatory claim or restatement in different words
- ESCALATE: contradicts existing skill or you're unsure

Return JSON:
{{
  "verdict": "SUPPLEMENT" | "EXTEND" | "CONFLICT" | "ALIAS" | "REJECT",
  "confidence": "high" | "medium" | "low",
  "include_claims": ["C5", "C6"],
  "skip_claims": ["C1'"],
  "escalate_claims": [],
  "reasoning": "Brief explanation of the decision."
}}"""


def build_merge_decision_prompt(
    skill1_name: str,
    skill2_name: str,
    added_claims: List[Dict],
    restatement_claims: List[Dict],
    conflict_claims: List[Dict],
) -> str:
    """Build the prompt for the merge decision."""
    added_str = "\n".join(f"  [{c['id']}] {c['text']} ({c['type']})" for c in added_claims) or "  (none)"
    restatement_str = "\n".join(f"  [{c['id']}] {c['text']}" for c in restatement_claims) or "  (none)"
    conflict_str = "\n".join(f"  [{c['id']}] {c['text']}" for c in conflict_claims) or "  (none)"

    return MERGE_DECISION_PROMPT.format(
        skill1_name=skill1_name,
        skill2_name=skill2_name,
        added_claims=added_str,
        restatement_claims=restatement_str,
        conflict_claims=conflict_str,
    )


def parse_merge_decision_response(response: str) -> Dict[str, Any]:
    """Parse the model's merge decision response."""
    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        result = json.loads(response)
        if not isinstance(result, dict):
            return {"verdict": "REVIEW", "confidence": "low", "reasoning": "Invalid response format"}

        return {
            "verdict": result.get("verdict", "REVIEW"),
            "confidence": result.get("confidence", "low"),
            "include_claims": result.get("include_claims", []),
            "skip_claims": result.get("skip_claims", []),
            "escalate_claims": result.get("escalate_claims", []),
            "reasoning": result.get("reasoning", ""),
        }
    except json.JSONDecodeError:
        return {"verdict": "REVIEW", "confidence": "low", "reasoning": "Failed to parse response"}

# --- Concrete AI step implementations (OpenCode CLI) ---

def extract_claims_opencode(skill_name: str, skill_body: str) -> List[Dict[str, Any]]:
    """Extract claims using OpenCode CLI.

    This is the concrete implementation of the extract_fn interface
    expected by librarian.extract_claims.
    """
    prompt = build_claim_extraction_prompt(skill_name, skill_body)
    response = opencode_run(prompt, model=CLAIM_MODEL)
    return parse_claim_extraction_response(response)


def decide_merge_opencode(
    skill1_name: str,
    skill2_name: str,
    claim_diff: Any,
) -> Dict[str, Any]:
    """Decide merge using OpenCode CLI.

    This is the concrete implementation of the decide_fn interface
    expected by librarian.decide_merge.
    """
    added = [{"id": c.id, "text": c.text, "type": c.claim_type} for c in claim_diff.added]
    restatement = [{"id": c.id, "text": c.text} for c in claim_diff.restatement]
    conflict = [{"id": c.id, "text": c.text} for c in claim_diff.conflict]

    prompt = build_merge_decision_prompt(
        skill1_name, skill2_name, added, restatement, conflict
    )
    response = opencode_run(prompt, model=DECISION_MODEL)
    return parse_merge_decision_response(response)
