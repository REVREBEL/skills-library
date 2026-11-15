"""
Deterministic canonical identity derivation.

Implements the ZI-07 scope rule:

  1. Scope  = the top-level ownership root under ``library/``, mapped through
              ``SCOPE_MAP`` for roots whose curated name differs from the
              physical folder name.
  2. Slug   = the leaf directory name.
  3. Uniqueness is ``Count(owner(<scope>:<slug>)) == 1`` (ADR-001 2.2 rule 5).
  4. A collision is a duplicate pair for ADR-004 5.2 adjudication. It is never
     resolved with a naming ladder.

Canonical packages sit at two depths:

  * functional categories   ``library/<category>/<subcategory>/<skill>``
  * operational roots       ``library/<root>/<skill>``

Anything deeper is a sub-skill nested inside a vendored pack and is not minted.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from .config import LIBRARY_DIR, OPERATIONAL_SYSTEM_PACKAGES

# Curated scope names that differ from the physical ownership root. This mirrors
# the convention already used by audit/taxonomy-census/semantic-role-census.json.
SCOPE_MAP: Dict[str, str] = {
    "skills-create-manage-update": "skills-lifecycle",
}

FUNCTIONAL_DEPTH = 3
OPERATIONAL_DEPTH = 2


def _relative_to_library(repo_path: str, library_dir: Optional[str] = None) -> Optional[str]:
    """Return ``repo_path`` relative to ``library/`` in posix form, else ``None``."""
    if not repo_path:
        return None

    root = os.path.abspath(library_dir or LIBRARY_DIR)
    absolute = os.path.abspath(repo_path)

    try:
        relative = os.path.relpath(absolute, root)
    except ValueError:
        return None

    if relative == os.pardir or relative.startswith(os.pardir + os.sep):
        return None
    if relative == os.curdir:
        return None

    return relative.replace(os.sep, "/")


def canonical_depth(root: str) -> Optional[int]:
    """Return the canonical package depth for an ownership root, else ``None``."""
    if root in OPERATIONAL_SYSTEM_PACKAGES:
        return OPERATIONAL_DEPTH
    return FUNCTIONAL_DEPTH


def _parts(repo_path: str, library_dir: Optional[str] = None) -> Optional[List[str]]:
    relative = _relative_to_library(repo_path, library_dir)
    if relative is None:
        return None
    return relative.split("/")


def derive_scope(
    repo_path: str,
    scope_map: Optional[Dict[str, str]] = None,
    library_dir: Optional[str] = None,
) -> Optional[str]:
    """Return the immutable provenance scope for a canonical package."""
    parts = _parts(repo_path, library_dir)
    if not parts:
        return None

    root = parts[0]
    if canonical_depth(root) is None or len(parts) != canonical_depth(root):
        return None

    return (SCOPE_MAP if scope_map is None else scope_map).get(root, root)


def derive_slug(
    repo_path: str,
    library_dir: Optional[str] = None,
) -> Optional[str]:
    """Return the capability slug (leaf directory name) for a canonical package."""
    parts = _parts(repo_path, library_dir)
    if not parts:
        return None

    root = parts[0]
    if canonical_depth(root) is None or len(parts) != canonical_depth(root):
        return None

    return parts[-1]


def mint_canonical_id(
    repo_path: str,
    scope_map: Optional[Dict[str, str]] = None,
    library_dir: Optional[str] = None,
) -> Optional[str]:
    """Return ``<scope>:<slug>`` for a canonical package, else ``None``.

    Returns ``None`` rather than raising for routers, category nodes and nested
    sub-skills, because those are legitimately outside the canonical set.
    """
    scope = derive_scope(repo_path, scope_map, library_dir)
    slug = derive_slug(repo_path, library_dir)
    if not scope or not slug:
        return None
    return f"{scope}:{slug}"


def canonical_package_paths(library_dir: Optional[str] = None) -> List[str]:
    """Return every canonical package directory, sorted for determinism."""
    root = library_dir or LIBRARY_DIR
    found: List[str] = []

    for current, _dirs, files in os.walk(root):
        if "SKILL.md" not in files:
            continue
        path = current.replace(os.sep, "/")
        if mint_canonical_id(path, library_dir=root) is not None:
            found.append(path)

    return sorted(found)


def find_collisions(
    library_dir: Optional[str] = None,
    scope_map: Optional[Dict[str, str]] = None,
) -> Dict[str, List[str]]:
    """Map each duplicated canonical id to the packages claiming it.

    A non-empty result is a list of duplicate pairs awaiting ADR-004 5.2
    adjudication.
    """
    claims: Dict[str, List[str]] = {}

    for path in canonical_package_paths(library_dir):
        canonical_id = mint_canonical_id(path, scope_map, library_dir)
        if canonical_id is None:
            continue
        claims.setdefault(canonical_id, []).append(path)

    return {cid: paths for cid, paths in claims.items() if len(paths) > 1}


__all__ = [
    "FUNCTIONAL_DEPTH",
    "OPERATIONAL_DEPTH",
    "SCOPE_MAP",
    "canonical_depth",
    "canonical_package_paths",
    "derive_scope",
    "derive_slug",
    "find_collisions",
    "mint_canonical_id",
]