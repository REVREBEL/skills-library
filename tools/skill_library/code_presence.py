"""
Code-presence survey for the canonical skills library.

ZI-07 needs a risk signal for ~2,133 canonical packages, but most are prose. This
module answers one question cheaply: does a package contain executable code, or is
it plain text?

Signals, strongest first:
  1. bundled executable files (.py, .sh, .js, .ts, ...)
  2. fenced code blocks in SKILL.md
  3. command metadata in frontmatter (allowed-tools, argument-hint)

A package is ``code`` if any signal fires, otherwise ``prose``.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .frontmatter import parse_frontmatter
from .identity import mint_canonical_id

EXECUTABLE_SUFFIXES = frozenset(
    {
        ".py",
        ".sh",
        ".bash",
        ".zsh",
        ".js",
        ".mjs",
        ".cjs",
        ".ts",
        ".tsx",
        ".jsx",
        ".rb",
        ".pl",
        ".php",
        ".ps1",
        ".bat",
        ".cmd",
    }
)

SKIP_DIRS = frozenset({"node_modules", ".git", "__pycache__", ".venv", "venv", ".mypy_cache"})

COMMAND_METADATA_FIELDS = ("allowed-tools", "argument-hint")

# Language tags on opening fences, normalised to a coarse bucket.
LANGUAGE_ALIASES = {
    "sh": "shell",
    "bash": "shell",
    "shell": "shell",
    "zsh": "shell",
    "console": "shell",
    "shell-session": "shell",
    "py": "python",
    "python": "python",
    "js": "javascript",
    "javascript": "javascript",
    "node": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "json": "data",
    "yaml": "data",
    "yml": "data",
    "toml": "data",
    "sql": "sql",
    "diff": "diff",
    "text": "text",
    "": "text",
}


@dataclass
class PackageSurvey:
    canonical_id: str
    path: str
    risk: str = ""
    license: str = ""
    has_scripts: bool = False
    script_count: int = 0
    script_languages: List[str] = field(default_factory=list)
    has_code_blocks: bool = False
    block_count: int = 0
    block_languages: List[str] = field(default_factory=list)
    has_command_metadata: bool = False
    classification: str = "prose"

    def to_row(self) -> Dict[str, str]:
        return {
            "canonical_id": self.canonical_id,
            "path": self.path,
            "risk": self.risk,
            "license": self.license,
            "classification": self.classification,
            "has_scripts": str(self.has_scripts).lower(),
            "script_count": str(self.script_count),
            "script_languages": ";".join(sorted(set(self.script_languages))),
            "has_code_blocks": str(self.has_code_blocks).lower(),
            "block_count": str(self.block_count),
            "block_languages": ";".join(sorted(set(self.block_languages))),
            "has_command_metadata": str(self.has_command_metadata).lower(),
        }


def _normalise_language(tag: str) -> str:
    tag = tag.strip().lower().strip("`").strip()
    tag = re.sub(r"^\{.*?\}$", "", tag).strip()
    return LANGUAGE_ALIASES.get(tag, tag or "text")


def scan_scripts(skill_dir: str) -> List[str]:
    """Return executable files bundled anywhere in the package."""
    found: List[str] = []
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if os.path.splitext(name)[1].lower() in EXECUTABLE_SUFFIXES:
                found.append(os.path.relpath(os.path.join(root, name), skill_dir))
    return sorted(found)


def scan_code_blocks(skill_md_path: str) -> List[str]:
    """Return the language tag of every fenced code block in a SKILL.md."""
    if not os.path.exists(skill_md_path):
        return []

    with open(skill_md_path, "r", encoding="utf-8", errors="replace") as handle:
        lines = handle.read().splitlines()

    languages: List[str] = []
    opening: Optional[str] = None

    for line in lines:
        stripped = line.strip()
        if not (stripped.startswith("```") or stripped.startswith("~~~")):
            continue

        fence = stripped[:3]
        remainder = stripped[3:].strip()

        if opening is None:
            opening = fence
            languages.append(_normalise_language(remainder))
        elif fence == opening and not remainder:
            opening = None

    return languages


def classify_package(skill_dir: str, library_dir: Optional[str] = None) -> Optional[PackageSurvey]:
    """Survey one package. Returns ``None`` when it is not a canonical package."""
    canonical_id = mint_canonical_id(skill_dir, library_dir=library_dir)
    if canonical_id is None:
        return None

    skill_md = os.path.join(skill_dir, "SKILL.md")
    frontmatter = parse_frontmatter(_read(skill_md)) or {}

    scripts = scan_scripts(skill_dir)
    blocks = scan_code_blocks(skill_md)
    command_metadata = any(frontmatter.get(field_name) for field_name in COMMAND_METADATA_FIELDS)

    if scripts or blocks or command_metadata:
        classification = "code"
    else:
        classification = "prose"

    return PackageSurvey(
        canonical_id=canonical_id,
        path=os.path.relpath(skill_dir).replace(os.sep, "/"),
        risk=frontmatter.get("risk", ""),
        license=frontmatter.get("license", ""),
        has_scripts=bool(scripts),
        script_count=len(scripts),
        script_languages=[os.path.splitext(s)[1].lower().lstrip(".") for s in scripts],
        has_code_blocks=bool(blocks),
        block_count=len(blocks),
        block_languages=blocks,
        has_command_metadata=command_metadata,
        classification=classification,
    )


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def survey_library(library_dir: str) -> List[PackageSurvey]:
    """Survey every canonical package under ``library_dir``."""
    from .identity import canonical_package_paths

    surveys: List[PackageSurvey] = []
    for path in canonical_package_paths(library_dir):
        survey = classify_package(path, library_dir=library_dir)
        if survey is not None:
            surveys.append(survey)
    return surveys


def summarise(surveys: List[PackageSurvey]) -> Dict[str, object]:
    """Aggregate a survey into counts used by the report."""
    total = len(surveys)
    code = [s for s in surveys if s.classification == "code"]
    prose = [s for s in surveys if s.classification == "prose"]

    def bucket(items: List[PackageSurvey]) -> Dict[str, int]:
        return {
            "total": len(items),
            "with_scripts": sum(1 for s in items if s.has_scripts),
            "with_code_blocks": sum(1 for s in items if s.has_code_blocks),
            "with_command_metadata": sum(1 for s in items if s.has_command_metadata),
            "risk_unknown": sum(1 for s in items if s.risk == "unknown"),
            "risk_missing": sum(1 for s in items if not s.risk),
        }

    return {
        "total": total,
        "code": bucket(code),
        "prose": bucket(prose),
        "code_share_pct": round(100.0 * len(code) / total, 1) if total else 0.0,
    }