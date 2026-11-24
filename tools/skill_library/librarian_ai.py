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
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --- Configuration ---

# Model for claim extraction (reading comprehension over skill bodies).
CLAIM_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"

# Model for merge decisions (bounded classification with confidence).
DECISION_MODEL = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"

# Fallback chain: the OpenRouter free tier has a shared daily quota. When
# it's exhausted (HTTP 429), try OpenCode's free providers, then NVIDIA
# direct. Rerank remains OpenRouter-only and falls back to Dice order in
# the test pipe when rate-limited.
MODEL_FALLBACKS = [
    CLAIM_MODEL,
    "opencode/nemotron-3.5-lightning-free",
    "opencode/nemotron-3.5-super-vl-free",
    "nvidia/nvidia/nemotron-3.5-lightning-30b-a3b",
    "nvidia/nvidia/nemotron-3.5-super-vl-120b-a12b",
    "nvidia/nvidia/nemotron-3-ultra-550b-a55b",
]

# Session-level cooldown: once a model fails (rate limit/provider error),
# don't retry it on every subsequent call. Reset when the process restarts.
_MODEL_COOLDOWNS = set()

# Claim extraction cache: the same skill is often compared against multiple
# candidates. Cache by content hash so each body is extracted only once.
_CLAIM_CACHE: Dict[str, List[Dict[str, Any]]] = {}


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


def opencode_run(
    prompt: str,
    model: str = CLAIM_MODEL,
    timeout: int = 120,
    models: Optional[List[str]] = None,
) -> str:
    """Run a prompt through the OpenCode CLI, trying models in order.

    Uses `opencode run --model <model> <prompt>`. The CLI handles session
    management, model routing, and API calls. If a model fails (rate
    limit, provider error, timeout), the next model in the fallback chain
    is tried. Returns the first non-empty successful response.

    The fallback chain is used automatically when ``models`` is omitted:
      OpenRouter free -> OpenCode free -> NVIDIA direct.
    """
    opencode_bin = _find_opencode()

    if models is None:
        models = [model] + [m for m in MODEL_FALLBACKS if m != model]

    # Skip models that already failed this session.
    models = [m for m in models if m not in _MODEL_COOLDOWNS]

    errors = []
    for candidate_model in models:
        try:
            result = subprocess.run(
                [opencode_bin, "run", "--model", candidate_model, prompt],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode != 0:
                errors.append(
                    f"{candidate_model}: exit {result.returncode} {result.stderr[:120]}"
                )
                _MODEL_COOLDOWNS.add(candidate_model)
                continue

            # The CLI prints the session header followed by the response.
            # Strip the header line (starts with ">") and return the rest.
            lines = result.stdout.strip().split("\n")
            response_lines = [
                l for l in lines
                if not l.startswith(">") and not l.startswith("[0m") and l.strip()
            ]
            response = "\n".join(response_lines).strip()
            if not response:
                errors.append(f"{candidate_model}: empty response")
                _MODEL_COOLDOWNS.add(candidate_model)
                continue

            if candidate_model != MODEL_FALLBACKS[0]:
                print(
                    f"  [librarian] using {candidate_model}",
                    file=sys.stderr,
                )
            return response
        except FileNotFoundError:
            raise RuntimeError(
                "opencode CLI not found. Install OpenCode or add it to PATH."
            )
        except subprocess.TimeoutExpired:
            errors.append(f"{candidate_model}: timeout after {timeout}s")
            _MODEL_COOLDOWNS.add(candidate_model)
            continue

    raise RuntimeError(
        "All OpenCode models failed or are cooling down: " + " | ".join(errors)
    )

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
    """Extract claims using OpenCode CLI, with content-hash caching.

    This is the concrete implementation of the extract_fn interface
    expected by librarian.extract_claims.
    """
    import hashlib

    cache_key = hashlib.sha256(
        (skill_name + "\n" + skill_body).encode("utf-8")
    ).hexdigest()
    if cache_key in _CLAIM_CACHE:
        return _CLAIM_CACHE[cache_key]

    prompt = build_claim_extraction_prompt(skill_name, skill_body)
    response = opencode_run(prompt, model=CLAIM_MODEL)
    claims = parse_claim_extraction_response(response)
    _CLAIM_CACHE[cache_key] = claims
    return claims


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
- composed_of: canonical ids of skills this workflow orchestrates (empty for primitives)
- extends: canonical id of the base capability this specializes, or null
- adapts: canonical id of the capability this protocol adapter binds, or null
- aliased_to: canonical id if this is an alias, or null
- execution_provider: an object with "default" and "supported". Each supported provider has name, provider_type (cli|mcp|rest_api|sdk|prompt_template), transport (node|python|mcp|http|prompt), and optional server_name/tool_name. Infer from the body; use prompt_template when no external tool is required.
- risk: low, medium, high, or critical
- side_effects: read-only, write, destructive, or privileged

Return ONLY a JSON object, no prose:
{{
  "role": "...",
  "applications": ["..."],
  "keywords": ["..."],
  "tags": ["..."],
  "depends_on": [],
  "composed_of": [],
  "extends": null,
  "adapts": null,
  "aliased_to": null,
  "execution_provider": {{
    "default": "...",
    "supported": [
      {{"name": "...", "provider_type": "...", "transport": "..."}}
    ]
  }},
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
        "composed_of": [],
        "extends": None,
        "adapts": None,
        "aliased_to": None,
        "execution_provider": {"default": "prompt_template", "supported": []},
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
    license_id: str = "MIT",
) -> str:
    """Render the two-tier YAML frontmatter from generated metadata.

    Outer shell: name, description, license (portable).
    Inner metadata: role, applications, keywords, tags, execution_provider,
    relationships, security.
    """
    lines = [
        "---",
        f'name: "{skill_name}"',
        f'description: "{description}"',
        f'license: "{license_id}"',
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

    # Execution provider(s)
    provider = metadata.get("execution_provider") or {}
    if not isinstance(provider, dict):
        provider = {"default": "prompt_template", "supported": []}
    default_provider = provider.get("default") or "prompt_template"
    supported = provider.get("supported") or []
    lines.append("  execution_provider:")
    lines.append(f'    default: "{default_provider}"')
    if supported:
        lines.append("    supported:")
        for item in supported:
            if not isinstance(item, dict):
                continue
            lines.append(f'      - name: "{item.get("name", default_provider)}"')
            lines.append(f'        provider_type: "{item.get("provider_type", "prompt_template")}"')
            lines.append(f'        transport: "{item.get("transport", "prompt")}"')
            if item.get("server_name"):
                lines.append(f'        server_name: "{item["server_name"]}"')
            if item.get("tool_name"):
                lines.append(f'        tool_name: "{item["tool_name"]}"')
    else:
        lines.append("    supported: []")

    # Relationships
    lines.append("  relationships:")
    _fmt_list("depends_on", metadata.get("depends_on", []), indent="    ")
    _fmt_list("composed_of", metadata.get("composed_of", []), indent="    ")
    lines.append(f'    extends: {json.dumps(metadata.get("extends")) if metadata.get("extends") else "null"}')
    lines.append(f'    adapts: {json.dumps(metadata.get("adapts")) if metadata.get("adapts") else "null"}')
    lines.append(f'    aliased_to: {json.dumps(metadata.get("aliased_to")) if metadata.get("aliased_to") else "null"}')

    # Security
    lines.append("  security:")
    lines.append(f'    risk: "{metadata.get("risk", "low")}"')
    lines.append(f'    side_effects: "{metadata.get("side_effects", "read-only")}"')
    needs_approval = (
        metadata.get("risk") in ("high", "critical")
        or metadata.get("side_effects") in ("write", "destructive", "privileged")
    )
    lines.append(f'    requires_approval: {"true" if needs_approval else "false"}')

    lines.append("---")
    return "\n".join(lines)


# --- Relationship gate ---

RELATIONSHIP_PROMPT = """You are checking whether a new skill is actually related to existing skills.

Candidate:
  name: {candidate_name}
  description: {candidate_description}
  body sample: {candidate_body}

Top catalog matches:
{matches}

Classify the relationship. This is NOT a "which is better" decision.
- self: the candidate is the same skill already in the catalog (same purpose and scope)
- duplicate: a different skill covers the same capability and could be merged
- overlap: a different skill shares some scope but also has distinct value
- unrelated: none of the matches are the same capability or a meaningful overlap

Return ONLY JSON:
{{"relationship": "self|duplicate|overlap|unrelated", "match": "exact catalog name or null", "reasoning": "one sentence"}}"""


def classify_relationship_opencode(
    candidate_name: str,
    candidate_description: str,
    candidate_body: str,
    matches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Classify candidate vs catalog before doing expensive claim extraction.

    Returns {"relationship": ..., "match": ..., "reasoning": ...}.
    Falls back to "unrelated" on failure (fail closed to NEW, not MERGE).
    """
    import json as _json

    if not matches:
        return {"relationship": "unrelated", "match": None, "reasoning": "No catalog matches"}

    match_lines = []
    for m in matches[:5]:
        match_lines.append(
            f"  - {m['name']}: {m.get('description', '')[:200]} "
            f"(dice={m.get('dice_similarity', 0):.3f}, rerank={m.get('rerank_score', 0):.3f})"
        )

    prompt = RELATIONSHIP_PROMPT.format(
        candidate_name=candidate_name,
        candidate_description=candidate_description[:300],
        candidate_body=candidate_body[:800],
        matches="\n".join(match_lines),
    )

    try:
        response = opencode_run(prompt, model=DECISION_MODEL)
    except Exception:
        return {"relationship": "unrelated", "match": None, "reasoning": "Relationship model unavailable"}

    response = response.strip()
    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        result = _json.loads(response)
        rel = result.get("relationship", "unrelated")
        if rel not in ("self", "duplicate", "overlap", "unrelated"):
            rel = "unrelated"
        return {
            "relationship": rel,
            "match": result.get("match"),
            "reasoning": result.get("reasoning", ""),
        }
    except _json.JSONDecodeError:
        return {"relationship": "unrelated", "match": None, "reasoning": "Failed to parse relationship response"}


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
