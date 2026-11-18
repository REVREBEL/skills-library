"""
Canonical YAML frontmatter parsing and schema validation.

This module replaces three divergent implementations that previously lived in
``scanner.py``, ``validator.py`` and ``intake.py``. The scanner variant split on
the first ``---`` anywhere in the file and did not skip comment lines, so it
disagreed with the other two on real input.

Schema decisions (ZI-07):
  * Canonical five fields are ``name, description, risk, source, license``.
  * ``category`` / ``subcategory`` are derived ownership axes and are compiled
    into the registry, never stored in the package.
  * ``source`` is a free-form provenance string.
  * ``risk`` and ``license`` have closed vocabularies.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# The five canonical fields. Order is stable and used in messages.
REQUIRED_FIELDS: Tuple[str, ...] = ("name", "description", "risk", "source", "license")

# Fields whose absence has always been a hard failure.
CORE_FIELDS: Tuple[str, ...] = ("name", "description")

# Fields whose absence is reported as a warning until the library is backfilled.
SCHEMA_FIELDS: Tuple[str, ...] = ("risk", "source", "license")

RISK_LEVELS = frozenset({"safe", "low", "elevated", "critical", "unknown"})

LICENSE_VALUES = frozenset(
    {
        "MIT",
        "Apache-2.0",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "GPL-3.0",
        "LGPL-3.0",
        "MPL-2.0",
        "CC-BY-4.0",
        "CC0-1.0",
        "Unlicense",
        "proprietary",
        "not_declared_upstream",
    }
)

# A license may legitimately point at a bundled license file rather than naming
# an SPDX identifier. This is accepted, but only in this exact form.
_LICENSE_FILE_REFERENCE = re.compile(r"^complete terms in .*licen[cs]e(\.txt|\.md)?$", re.IGNORECASE)

VOCABULARIES: Dict[str, frozenset] = {
    "risk": RISK_LEVELS,
    "license": LICENSE_VALUES,
}

# Case-insensitive lookup tables so that "apache-2.0" and "Apache-2.0" agree.
_RISK_LOOKUP = {v.lower(): v for v in RISK_LEVELS}
_LICENSE_LOOKUP = {v.lower(): v for v in LICENSE_VALUES}


def parse_frontmatter(content: str) -> Optional[dict]:
    """Parse YAML frontmatter delimited by ``---`` lines.

    Returns ``None`` when the document has no frontmatter block. Only the
    simple ``key: value`` form used by SKILL.md files is supported; nested
    mappings are not part of the schema.
    """
    if not content:
        return None

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return None

    result: Dict[str, str] = {}
    for line in lines[1:closing]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            continue
        result[key] = value.strip().strip("\"'")
    return result


def _vocabulary_for(field: str) -> Optional[Dict[str, str]]:
    if field == "risk":
        return _RISK_LOOKUP
    if field == "license":
        return _LICENSE_LOOKUP
    return None


def _check_vocabulary(field: str, value: str) -> Optional[str]:
    """Return an error message when ``value`` is outside the field's vocabulary."""
    if field == "license" and _LICENSE_FILE_REFERENCE.match(value.strip()):
        return None

    lookup = _vocabulary_for(field)
    if lookup is None:
        return None
    if value.strip().lower() in lookup:
        return None

    allowed = ", ".join(sorted(VOCABULARIES[field]))
    return (
        f"Frontmatter '{field}' value '{value}' is not in the allowed vocabulary "
        f"({allowed})"
    )


def validate_frontmatter(
    frontmatter: Optional[dict],
    strict: bool = False,
) -> Tuple[List[str], List[str]]:
    """Validate a parsed frontmatter mapping.

    Returns ``(errors, warnings)``.

    ``name`` and ``description`` are always required. ``risk``, ``source`` and
    ``license`` are required by the schema but reported as warnings unless
    ``strict`` is set, because 543 packages still lack them. Out-of-vocabulary
    values are errors in both modes: a value that is present but wrong is an
    unambiguous defect.
    """
    if frontmatter is None:
        return ["Invalid or missing YAML frontmatter in SKILL.md"], []

    errors: List[str] = []
    warnings: List[str] = []

    for field in CORE_FIELDS:
        if not frontmatter.get(field):
            errors.append(f"Frontmatter missing required '{field}'")

    for field in SCHEMA_FIELDS:
        if not frontmatter.get(field):
            message = f"Frontmatter missing required '{field}'"
            if strict:
                errors.append(message)
            else:
                warnings.append(message)

    for field in VOCABULARIES:
        value = frontmatter.get(field)
        if not value:
            continue
        problem = _check_vocabulary(field, value)
        if problem:
            errors.append(problem)

    return errors, warnings


__all__ = [
    "CORE_FIELDS",
    "LICENSE_VALUES",
    "REQUIRED_FIELDS",
    "RISK_LEVELS",
    "SCHEMA_FIELDS",
    "VOCABULARIES",
    "parse_frontmatter",
    "validate_frontmatter",
]