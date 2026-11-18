"""
Execution contract: risk, side effects, permissions, environment and load plans.

ZI-08 asks for three things:

  1. typed risk / side-effect / permission / environment declarations
  2. a minimal runtime load plan, distinct from the availability closure
  3. health probes only where a concrete execution consumer exists

This module implements 1 and 2. It deliberately does not implement 3: no
consumer exists yet, and probing without one would invent a dependency on
services the library cannot vouch for.

Declarations are *derived* from evidence rather than hand-written, because
``risk`` is ``unknown`` on 2,102 of 2,133 canonical packages and manual backfill
does not scale. Evidence sources, strongest first:

  * the code-presence tier (bundled scripts, executable blocks, prose)
  * the Phase 09 resource registry, where a resource exists for the skill
  * frontmatter declarations, when they carry a real value
"""

from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .code_presence import PackageSurvey, classify_package
from .frontmatter import parse_frontmatter
from .identity import mint_canonical_id

PHASE09_REGISTRY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "audit",
    "rebuild-phase-1-12",
    "phase09-resource-registry.csv",
)


class SideEffect(str, Enum):
    """What a skill does to the world when it runs."""

    NONE = "none"
    READS_FILES = "reads_files"
    WRITES_FILES = "writes_files"
    EXECUTES_COMMANDS = "executes_commands"
    NETWORK = "network"
    EXTERNAL_STATE = "external_state"
    DESTRUCTIVE = "destructive"


class Permission(str, Enum):
    """What a skill needs from the runtime to run."""

    NONE = "none"
    FILESYSTEM_READ = "filesystem_read"
    FILESYSTEM_WRITE = "filesystem_write"
    SHELL = "shell"
    NETWORK = "network"
    CREDENTIALS = "credentials"


@dataclass(frozen=True)
class EnvironmentRequirement:
    """What must exist outside the skill for it to run."""

    runtimes: Tuple[str, ...] = ()
    tools: Tuple[str, ...] = ()
    needs_network: bool = False
    env_vars: Tuple[str, ...] = ()


@dataclass
class ExecutionProfile:
    """A derived execution contract for one canonical package."""

    canonical_id: str
    risk: str = "unknown"
    side_effects: Set[SideEffect] = field(default_factory=set)
    permissions: Set[Permission] = field(default_factory=set)
    environment: EnvironmentRequirement = field(default_factory=EnvironmentRequirement)
    evidence: List[str] = field(default_factory=list)
    tier: int = 4

    @property
    def requires_shell(self) -> bool:
        return Permission.SHELL in self.permissions

    def to_dict(self) -> Dict[str, object]:
        return {
            "canonical_id": self.canonical_id,
            "risk": self.risk,
            "tier": self.tier,
            "side_effects": sorted(e.value for e in self.side_effects),
            "permissions": sorted(p.value for p in self.permissions),
            "runtimes": list(self.environment.runtimes),
            "tools": list(self.environment.tools),
            "needs_network": self.environment.needs_network,
            "env_vars": list(self.environment.env_vars),
            "evidence": list(self.evidence),
        }


@dataclass
class LoadPlan:
    """The minimal set of things needed to execute one skill.

    This is deliberately *not* the availability closure. The availability
    closure answers "is this skill present and indexed"; the load plan answers
    "what must be read or executed to run it".
    """

    canonical_id: str
    entrypoint: str
    resources: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    runtimes: Set[str] = field(default_factory=set)
    needs_network: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "canonical_id": self.canonical_id,
            "entrypoint": self.entrypoint,
            "resources": sorted(self.resources),
            "scripts": sorted(self.scripts),
            "runtimes": sorted(self.runtimes),
            "needs_network": self.needs_network,
        }


# --------------------------------------------------------------------------
# Phase 09 evidence
# --------------------------------------------------------------------------

def load_phase09_index(path: Optional[str] = None) -> Dict[str, Dict[str, object]]:
    """Index the Phase 09 resource registry by owner slug.

    Phase 09 records one row per *resource*; a skill may own several. The index
    keeps the strongest (most permissive) status per owner.
    """
    registry_path = path or PHASE09_REGISTRY
    if not os.path.exists(registry_path):
        return {}

    strongest: Dict[str, Dict[str, object]] = {}
    with open(registry_path, "r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            owner = (row.get("owner_skill") or "").strip()
            if not owner:
                continue
            current = strongest.get(owner)
            if current is None or _phase09_rank(row) > _phase09_rank(current):
                strongest[owner] = dict(row)
    return strongest


def _phase09_rank(row: Dict[str, object]) -> int:
    """Rank a Phase 09 row by how much execution surface it exposes."""
    rank = 0
    if (row.get("shell_execution_status") or "") != "no_shell_calls":
        rank += 4
    if (row.get("remote_execution_status") or "") != "no_remote_calls":
        rank += 4
    if (row.get("destructive_operation_status") or "") != "read_only_or_additive":
        rank += 8
    if (row.get("input_validation_status") or "") != "static_resource_non_executable":
        rank += 1
    return rank


# --------------------------------------------------------------------------
# Derivation
# --------------------------------------------------------------------------

_SCRIPT_SUFFIX_TO_RUNTIME = {
    ".py": "python",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".js": "node",
    ".mjs": "node",
    ".cjs": "node",
    ".ts": "node",
    ".tsx": "node",
    ".jsx": "node",
    ".rb": "ruby",
    ".pl": "perl",
    ".php": "php",
}

_EXEC_BLOCK_LANGUAGES = {"shell", "python", "javascript", "typescript", "sql"}

# Commands that indicate destructive intent when they appear in code, not prose.
_DESTRUCTIVE_PATTERN = re.compile(
    r"\brm\s+-[a-zA-Z]*[rf]\b"
    r"|\bmkfs(\.[a-z0-9]+)?\b"
    r"|\bdd\s+[^\n]*\bif="
    r"|\bshutdown\s+(-[hrp]|--poweroff)\b"
    r"|\b(drop|truncate)\s+table\b"
    r"|\bterraform\s+destroy\b"
    r"|\bgit\s+push\s+(--force|-f)\b"
    r"|>\s*/dev/(sd|nvme|disk)",
    re.IGNORECASE,
)

# Fenced blocks and inline code spans. Destructive commands are only meaningful
# as instructions; the same words in prose ("auto-start on reboot") are not.
_FENCED_BLOCK = re.compile(r"(?ms)^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n(.*?)^[ \t]{0,3}\1[ \t]*$")
_INLINE_CODE = re.compile(r"`([^`\n]+)`")

_CREDENTIAL_PATTERN = re.compile(
    r"\b(?:api[_-]?key|secret|token|password|credential|service[_-]?account)\b",
    re.IGNORECASE,
)


def _tier(survey: PackageSurvey) -> int:
    if survey.has_scripts:
        return 1
    languages = {lang for lang in survey.block_languages if lang}
    if languages & _EXEC_BLOCK_LANGUAGES:
        return 2
    if languages:
        return 3
    return 4


_DEFAULT_RISK = {1: "elevated", 2: "low", 3: "safe", 4: "safe"}


def derive_execution_profile(
    skill_dir: str,
    survey: Optional[PackageSurvey] = None,
    phase09_index: Optional[Dict[str, Dict[str, object]]] = None,
    library_dir: Optional[str] = None,
) -> Optional[ExecutionProfile]:
    """Derive an execution profile for a canonical package.

    Returns ``None`` when the package is not canonical.
    """
    canonical_id = mint_canonical_id(skill_dir, library_dir=library_dir)
    if canonical_id is None:
        return None

    survey = survey or classify_package(skill_dir, library_dir=library_dir)
    if survey is None:
        return None

    tier = _tier(survey)
    profile = ExecutionProfile(canonical_id=canonical_id, tier=tier, risk=_DEFAULT_RISK[tier])
    slug = canonical_id.split(":", 1)[1]

    # --- tier 1: bundled executables -------------------------------------
    if survey.has_scripts:
        profile.side_effects.add(SideEffect.EXECUTES_COMMANDS)
        profile.permissions.add(Permission.SHELL)
        profile.permissions.add(Permission.FILESYSTEM_READ)
        profile.evidence.append(f"bundled_scripts:{survey.script_count}")
        for language in survey.script_languages:
            runtime = _SCRIPT_SUFFIX_TO_RUNTIME.get(f".{language.lower()}")
            if runtime:
                profile.environment = EnvironmentRequirement(
                    runtimes=tuple(sorted(set(profile.environment.runtimes) | {runtime})),
                    tools=profile.environment.tools,
                    needs_network=profile.environment.needs_network,
                    env_vars=profile.environment.env_vars,
                )

    # --- tier 2: executable fenced blocks --------------------------------
    if survey.has_code_blocks:
        languages = {lang for lang in survey.block_languages if lang}
        if languages & _EXEC_BLOCK_LANGUAGES:
            profile.side_effects.add(SideEffect.EXECUTES_COMMANDS)
            profile.permissions.add(Permission.SHELL)
            profile.evidence.append("executable_code_blocks")
        else:
            profile.side_effects.add(SideEffect.READS_FILES)
            profile.evidence.append("illustrative_blocks_only")

    if tier >= 3:
        profile.side_effects.add(SideEffect.READS_FILES)
        profile.permissions.add(Permission.FILESYSTEM_READ)

    # --- destructive intent in prose or blocks ---------------------------
    if _contains_destructive_command(skill_dir):
        profile.side_effects.add(SideEffect.DESTRUCTIVE)
        profile.risk = "critical"
        profile.evidence.append("destructive_command_pattern")

    # --- credential references -------------------------------------------
    if _contains_credential_reference(skill_dir):
        profile.permissions.add(Permission.CREDENTIALS)
        profile.evidence.append("credential_reference")

    # --- Phase 09 refinement ---------------------------------------------
    if phase09_index is None:
        phase09_index = load_phase09_index()
    record = phase09_index.get(slug)
    if record:
        profile.evidence.append("phase09_resource_registry")
        shell_status = record.get("shell_execution_status") or ""
        if shell_status not in ("", "no_shell_calls"):
            profile.side_effects.add(SideEffect.EXECUTES_COMMANDS)
            profile.permissions.add(Permission.SHELL)
        remote_status = record.get("remote_execution_status") or ""
        if remote_status not in ("", "no_remote_calls"):
            profile.side_effects.add(SideEffect.NETWORK)
            profile.permissions.add(Permission.NETWORK)
            profile.environment = EnvironmentRequirement(
                runtimes=profile.environment.runtimes,
                tools=profile.environment.tools,
                needs_network=True,
                env_vars=profile.environment.env_vars,
            )
        if (record.get("destructive_operation_status") or "").startswith("temp_artifact"):
            # Scoped cleanup of temporary artifacts still writes to disk.
            profile.side_effects.add(SideEffect.WRITES_FILES)
        dependency = record.get("dependency_status") or ""
        if dependency not in ("", "none_static"):
            profile.evidence.append(f"phase09_dependency:{dependency}")

    return profile


def _read_text(skill_dir: str) -> str:
    path = os.path.join(skill_dir, "SKILL.md")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _code_text(text: str) -> str:
    """Return only fenced-block bodies and inline code spans."""
    parts = [match.group(2) for match in _FENCED_BLOCK.finditer(text)]
    without_blocks = _FENCED_BLOCK.sub("\n", text)
    parts.extend(match.group(1) for match in _INLINE_CODE.finditer(without_blocks))
    return "\n".join(parts)


def _contains_destructive_command(skill_dir: str) -> bool:
    return bool(_DESTRUCTIVE_PATTERN.search(_code_text(_read_text(skill_dir))))


def _contains_credential_reference(skill_dir: str) -> bool:
    return bool(_CREDENTIAL_PATTERN.search(_read_text(skill_dir)))


# --------------------------------------------------------------------------
# Load plans
# --------------------------------------------------------------------------

def build_load_plan(
    skill_dir: str,
    profile: Optional[ExecutionProfile] = None,
    library_dir: Optional[str] = None,
) -> Optional[LoadPlan]:
    """Build the minimal load plan for a canonical package."""
    canonical_id = mint_canonical_id(skill_dir, library_dir=library_dir)
    if canonical_id is None:
        return None

    profile = profile or derive_execution_profile(skill_dir, library_dir=library_dir)
    if profile is None:
        return None

    entrypoint = os.path.join(skill_dir, "SKILL.md").replace(os.sep, "/")
    resources: List[str] = []
    scripts: List[str] = []

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", "node_modules"})
        for name in sorted(files):
            relative = os.path.relpath(os.path.join(root, name), skill_dir).replace(os.sep, "/")
            if relative == "SKILL.md":
                continue
            if os.path.splitext(name)[1].lower() in _SCRIPT_SUFFIX_TO_RUNTIME:
                scripts.append(relative)
            else:
                resources.append(relative)

    runtimes = set(profile.environment.runtimes)
    for script in scripts:
        runtime = _SCRIPT_SUFFIX_TO_RUNTIME.get(os.path.splitext(script)[1].lower())
        if runtime:
            runtimes.add(runtime)
    if profile.permissions and Permission.SHELL in profile.permissions:
        runtimes.add("shell")

    return LoadPlan(
        canonical_id=canonical_id,
        entrypoint=entrypoint,
        resources=resources,
        scripts=scripts,
        runtimes=runtimes,
        needs_network=profile.environment.needs_network,
    )


def summarise_profiles(profiles: Iterable[ExecutionProfile]) -> Dict[str, object]:
    """Aggregate profiles for reporting."""
    profiles = list(profiles)
    total = len(profiles)
    by_tier: Dict[int, int] = {}
    by_risk: Dict[str, int] = {}
    by_permission: Dict[str, int] = {}
    by_side_effect: Dict[str, int] = {}

    for profile in profiles:
        by_tier[profile.tier] = by_tier.get(profile.tier, 0) + 1
        by_risk[profile.risk] = by_risk.get(profile.risk, 0) + 1
        for permission in profile.permissions:
            by_permission[permission.value] = by_permission.get(permission.value, 0) + 1
        for side_effect in profile.side_effects:
            by_side_effect[side_effect.value] = by_side_effect.get(side_effect.value, 0) + 1

    return {
        "total": total,
        "by_tier": dict(sorted(by_tier.items())),
        "by_risk": dict(sorted(by_risk.items())),
        "by_permission": dict(sorted(by_permission.items())),
        "by_side_effect": dict(sorted(by_side_effect.items())),
        "with_phase09_evidence": sum(1 for p in profiles if any("phase09" in e for e in p.evidence)),
    }