#!/usr/bin/env python3
"""Materialize a project-specific skill bundle from the test library.

Usage:
    python3 tools/librarian_materialize.py --profile .skills/config.json
    python3 tools/librarian_materialize.py --profile .skills/config.json --replace
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.project_materialization import materialize_project


def _source_commit(explicit):
    if explicit:
        return explicit
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "HEAD"


def main():
    parser = argparse.ArgumentParser(description="Materialize a project-specific skill bundle")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--groups", type=Path, default=REPO_ROOT / "config" / "skill-groups.json")
    parser.add_argument("--library", type=Path, default=REPO_ROOT / "test-library")
    parser.add_argument("--target", type=Path)
    parser.add_argument("--source-commit")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    groups = json.loads(args.groups.read_text(encoding="utf-8"))
    target = args.target or (args.profile.parent / profile.get("target_path", ".agents/skills"))
    result = materialize_project(
        library=args.library,
        profile=profile,
        groups_config=groups,
        target=target,
        source_commit=_source_commit(args.source_commit),
        replace=args.replace,
    )
    print(f"Materialized {result['total_materialized']} skills to {result['target']}")
    print(f"Lockfile: {result['lockfile']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
