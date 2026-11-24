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
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --- Configuration ---

# Model for claim extraction (reading comprehension over skill bodies).
CLAIM_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"

# Model for merge decisions (bounded classification with confidence).
DECISION_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"


# --- OpenCode CLI bridge ---

def _find_opencode() -> str:
    """Locate the opencode binary.

    Checks PATH first, then known install locations (nvm, Homebrew, the
    OpenChamber app bundle). The CLI is not a Python package — it's a
    standalone binary, so we search common install roots rather than
    relying on the parent process PATH being set up.
    """
    found = shutil.which("opencode")
    if found:
        return found

    candidates = [
        Path.home() / ".nvm" / "current" / "bin" / "opencode",
        Path("/usr/local/bin/opencode"),
        Path("/opt/homebrew/bin/opencode"),
        Path("/Applications/OpenChamber.app/Contents/Resources/opencode-cli/opencode"),
    ]
    # nvm keeps versioned installs; check the newest.
    nvm_bin = Path.home() / ".nvm" / "versions" / "node"
    if nvm_bin.exists():
        for version_dir in sorted(nvm_bin.iterdir(), reverse=True):
            candidates.append(version_dir / "bin" / "opencode")

    for candidate in candidates:
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)

    raise RuntimeError(
        "opencode CLI not found. Install it or add it to PATH. "
        "Checked: PATH, ~/.nvm, /usr/local/bin, /opt/homebrew/bin, OpenChamber.app"
    )


def opencode_run(prompt: str, model: str = CLAIM_MODEL, timeout: int = 120) -> str:
    """Run a prompt through the OpenCode CLI and return the response text.

    Uses `opencode run --model <model> <prompt>`. The CLI handles session
    management, model routing, and API calls. The response is the last
    assistant message.

    This is the concrete implementation of the AI steps. It shells out to
    the `opencode` CLI, which must be installed.
    """
    try:
        opencode_bin = _find_opencode()
        result = subprocess.run(
            [opencode_bin, "run", "--model", model, prompt],
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
    """Parse the model's response into a list of claims.

    Filters out template boilerplate — meta-instructions that appear in
    template-format skills but aren't real operational claims.
    """
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
            text = c.get("text", "")
            if _is_boilerplate(text):
                continue
            result.append({
                "id": c.get("id", f"C{i+1}"),
                "text": text,
                "type": c.get("type", "operational"),
            })
        return result
    except json.JSONDecodeError:
        return []


# Template boilerplate phrases — meta-instructions from template-format
# skills that aren't real operational claims.
_BOILERPLATE_PATTERNS = [
    r"clarify goals?,? constraints?,? and required inputs",
    r"provide actionable steps and verification",
    r"apply relevant best practices and validate outcomes",
    r"do not treat the output as a substitute",
    r"use this skill only when the task clearly matches",
    r"stop and ask for clarification if required inputs",
    r"if detailed examples are required, open",
    r"provide actionable steps and verification",
    r"apply relevant best practices",
    r"validate outcomes",
]


def _is_boilerplate(text: str) -> bool:
    """Return True if the claim is template boilerplate, not a real instruction."""
    lower = text.lower().strip()
    for pattern in _BOILERPLATE_PATTERNS:
        if re.search(pattern, lower):
            return True
    return False


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

def rerank_with_opencode(
    query: str,
    passages: List[str],
) -> List[Tuple[int, float]]:
    """Rerank passages using a chat model via OpenCode CLI.

    Frames reranking as a scoring task: the model scores each passage
    for relevance to the query. Returns [(index, score)] sorted by
    score descending.

    This is more effective than a dedicated rerank model for the
    Librarian's use case because it evaluates *semantic relatedness*,
    not just lexical similarity. A dedicated rerank model (bge-reranker-base)
    scored mcp-builder-ms at 0.011 against the mcp-builder query; a chat
    model scored it at 0.95 because it understood both are about building
    MCP servers.
    """
    if not passages:
        return []

    # Build the scoring prompt
    passage_texts = "\n\n".join(
        f"Passage {chr(65+i)}: {p[:200]}" for i, p in enumerate(passages)
    )
    prompt = (
        f"Score these passages for relevance to the query. "
        f"Query: '{query[:200]}'\n\n"
        f"{passage_texts}\n\n"
        f"Return JSON array: ["
        + ", ".join(
            f"{{\"passage\":\"{chr(65+i)}\",\"score\":0.0-1.0}}"
            for i in range(len(passages))
        )
        + "]"
    )

    response = opencode_run(prompt, model=CLAIM_MODEL)

    # Parse the JSON response
    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        scores = json.loads(response)
        if not isinstance(scores, list):
            return [(i, 0.0) for i in range(len(passages))]

        result = []
        for item in scores:
            if not isinstance(item, dict):
                continue
            passage_label = item.get("passage", "")
            score = item.get("score", 0.0)
            # Convert label (A, B, C...) to index (0, 1, 2...)
            idx = ord(passage_label) - ord("A") if passage_label else -1
            if 0 <= idx < len(passages):
                result.append((idx, float(score)))

        # Sort by score descending
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    except (json.JSONDecodeError, ValueError):
        return [(i, 0.0) for i in range(len(passages))]


def rerank_with_openrouter(
    query: str,
    passages: List[str],
) -> List[Tuple[int, float]]:
    """Rerank passages using the OpenRouter rerank endpoint.

    Uses nvidia/nemotron-3.5-rerank-8b:free via the /api/v1/rerank
    endpoint. This is a dedicated rerank model with well-calibrated
    relevance scores — unlike a chat model, it's trained specifically
    for passage ranking.

    The OpenRouter API key is read from OpenCode's credential store
    (~/.local/share/opencode/opencode.db), so no separate key management
    is needed.
    """
    if not passages:
        return []

    import sqlite3

    # Read the OpenRouter API key from OpenCode's credential store
    db_path = os.path.expanduser("~/.local/share/opencode/opencode.db")
    try:
        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT value FROM credential WHERE integration_id='openrouter' AND active=1"
        ).fetchone()
        conn.close()
        if not row:
            raise RuntimeError("No OpenRouter credential found in OpenCode's credential store")
        cred = json.loads(row[0])
        api_key = cred.get("key", "")
        if not api_key:
            raise RuntimeError("OpenRouter credential has no key")
    except sqlite3.Error as e:
        raise RuntimeError(f"Could not read OpenCode credential store: {e}")

    # Call the rerank endpoint
    import urllib.request
    import urllib.error

    payload = json.dumps({
        "model": "nvidia/nemotron-3.5-rerank-8b:free",
        "query": query[:500],
        "documents": [p[:500] for p in passages],
        "top_n": len(passages),
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/rerank",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            results = data.get("results", [])
            # results are sorted by relevance_score descending
            return [(r["index"], r["relevance_score"]) for r in results]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"OpenRouter rerank failed (HTTP {e.code}): {body[:200]}")
    except Exception as e:
        raise RuntimeError(f"OpenRouter rerank failed: {e}")


def rerank_with_openrouter(
    query: str,
    passages: List[str],
) -> List[Tuple[int, float]]:
    """Rerank passages using the dedicated OpenRouter rerank endpoint.

    Uses nvidia/nemotron-3.5-rerank-8b:free via the /api/v1/rerank
    endpoint. This is a purpose-built rerank model — it scores query-passage
    relevance directly, not through chat completion.

    The OpenRouter API key is read from OpenCode's credential store.
    """
    if not passages:
        return []

    import sqlite3
    from pathlib import Path

    # Read the OpenRouter API key from OpenCode's credential store
    db_path = Path.home() / ".local" / "share" / "opencode" / "opencode.db"
    if not db_path.exists():
        raise RuntimeError(f"OpenCode credential store not found: {db_path}")

    conn = sqlite3.connect(str(db_path))
    row = conn.execute(
        "SELECT value FROM credential WHERE integration_id='openrouter' AND active=1"
    ).fetchone()
    conn.close()

    if not row:
        raise RuntimeError("No active OpenRouter credential found in OpenCode's credential store")

    cred = json.loads(row[0])
    api_key = cred.get("key", "")
    if not api_key:
        raise RuntimeError("OpenRouter credential has no key")

    # Call the rerank endpoint
    import urllib.request
    import urllib.error

    payload = json.dumps({
        "model": "nvidia/nemotron-3.5-rerank-8b:free",
        "query": query,
        "documents": passages,
        "top_n": len(passages),
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/rerank",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            results = data.get("results", [])
            # results are sorted by relevance_score descending
            return [(r["index"], r["relevance_score"]) for r in results]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"OpenRouter rerank failed (HTTP {e.code}): {body[:200]}")
    except Exception as e:
        raise RuntimeError(f"OpenRouter rerank failed: {e}")


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


# --- Metadata generation ---

METADATA_PROMPT = """You are generating the discovery metadata for a skill.

Skill: {skill_name}
Description: {description}
Assigned category: {category}/{subcategory}

Body (first 1500 chars):
{body}

Produce the metadata block for this skill. Determine:
- role: one of capability, workflow, primitive, overlay, adapter, reference, alias
- applications: every platform/tool/framework the skill operates (e.g. figma, react, swiftui, flutter, postgres). List ALL that apply, not just the primary one.
- keywords: atomic discovery phrases (lowercase, hyphenated)
- tags: broad classifiers (e.g. design, frontend, testing)
- depends_on: canonical ids of skills this requires (use "scope:slug", empty if none)
- extends: canonical id of the base capability this specializes, or null
- risk: low, medium, high, or critical
- side_effects: read-only, write, destructive, or privileged

Return ONLY a JSON object, no prose:
{{
  "role": "...",
  "applications": ["..."],
  "keywords": ["..."],
  "tags": ["..."],
  "depends_on": [],
  "extends": null,
  "risk": "...",
  "side_effects": "..."
}}"""


def generate_metadata_opencode(
    skill_name: str,
    description: str,
    category: str,
    subcategory: str,
    body: str,
) -> Dict[str, Any]:
    """Generate the discovery metadata block for a skill.

    Uses the OpenCode CLI. Returns a dict with role, applications,
    keywords, tags, depends_on, extends, risk, side_effects.
    Falls back to safe defaults on failure.
    """
    import json as _json

    defaults = {
        "role": "capability",
        "applications": [],
        "keywords": [],
        "tags": [],
        "depends_on": [],
        "extends": None,
        "risk": "low",
        "side_effects": "read-only",
    }

    prompt = METADATA_PROMPT.format(
        skill_name=skill_name,
        description=description[:300],
        category=category,
        subcategory=subcategory or "(root)",
        body=body[:1500],
    )

    try:
        response = opencode_run(prompt, model=CLAIM_MODEL)
    except Exception:
        return defaults

    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        result = _json.loads(response)
        if not isinstance(result, dict):
            return defaults
        # Merge with defaults so missing keys don't crash the writer
        merged = dict(defaults)
        merged.update({k: v for k, v in result.items() if v is not None})
        return merged
    except _json.JSONDecodeError:
        return defaults


def render_frontmatter(
    skill_name: str,
    description: str,
    metadata: Dict[str, Any],
    canonical_id: str,
) -> str:
    """Render the two-tier YAML frontmatter from generated metadata.

    Outer shell: name, description (portable).
    Inner metadata: role, applications, keywords, tags, relationships, security.
    """
    lines = [
        "---",
        f'name: "{skill_name}"',
        f'description: "{description}"',
    ]

    def _fmt_list(key, items, indent="  "):
        if not items:
            lines.append(f"{indent}{key}: []")
        else:
            lines.append(f"{indent}{key}:")
            for item in items:
                lines.append(f"{indent}  - {item}")

    lines.append("metadata:")
    lines.append(f'  canonical_id: "{canonical_id}"')
    lines.append(f'  urn: "urn:skill:{canonical_id}"')
    lines.append(f'  role: "{metadata.get("role", "capability")}"')
    _fmt_list("applications", metadata.get("applications", []))
    _fmt_list("keywords", metadata.get("keywords", []))
    _fmt_list("tags", metadata.get("tags", []))
    lines.append(f'  applications_compatibility: "universal"')

    # Relationships
    depends_on = metadata.get("depends_on", [])
    extends = metadata.get("extends")
    lines.append("  relationships:")
    _fmt_list("depends_on", depends_on, indent="    ")
    lines.append(f'    extends: {json.dumps(extends) if extends else "null"}')
    lines.append('    composed_of: []')
    lines.append('    adapts: null')
    lines.append('    aliased_to: null')

    # Security
    lines.append("  security:")
    lines.append(f'    risk: "{metadata.get("risk", "low")}"')
    lines.append(f'    side_effects: "{metadata.get("side_effects", "read-only")}"')
    lines.append(f'    requires_approval: {"true" if metadata.get("risk") in ("high", "critical") else "false"}')

    lines.append("---")
    return "\n".join(lines)


# --- Placement proposal ---

PLACEMENT_PROMPT = """You are placing a new skill into a library taxonomy.

Skill: {skill_name}
Description: {description}

Available categories and subcategories:
{categories}

Choose the best destination for this skill. Consider:
- What the skill actually does (from the description)
- Which category's scope best matches
- If no category fits, say "uncategorized"

Return JSON:
{{"category": "...", "subcategory": "...", "reasoning": "..."}}"""


def propose_placement_opencode(
    skill_name: str,
    description: str,
    categories: Dict[str, List[str]],
) -> Dict[str, Any]:
    """Propose a destination category/subcategory for a skill.

    Uses the OpenCode CLI to classify the skill into the taxonomy.
    Returns {"category": ..., "subcategory": ..., "reasoning": ...}.
    """
    import json as _json

    # Format the categories for the prompt
    cat_lines = []
    for cat, subs in sorted(categories.items()):
        if subs:
            cat_lines.append(f"- {cat}/{{{', '.join(subs)}}}")
        else:
            cat_lines.append(f"- {cat}/")
    categories_str = "\n".join(cat_lines)

    prompt = PLACEMENT_PROMPT.format(
        skill_name=skill_name,
        description=description[:300],
        categories=categories_str,
    )

    response = opencode_run(prompt, model=CLAIM_MODEL)

    # Parse the response
    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        result = _json.loads(response)
        if not isinstance(result, dict):
            return {"category": "uncategorized", "subcategory": "", "reasoning": "Invalid response"}
        return {
            "category": result.get("category", "uncategorized"),
            "subcategory": result.get("subcategory", ""),
            "reasoning": result.get("reasoning", ""),
        }
    except _json.JSONDecodeError:
        return {"category": "uncategorized", "subcategory": "", "reasoning": "Failed to parse response"}
