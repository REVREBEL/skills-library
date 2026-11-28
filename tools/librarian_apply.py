#!/usr/bin/env python3
"""Controlled apply and rollback for approved Librarian proposals.

Usage:
    python3 tools/librarian_apply.py plan --all
    python3 tools/librarian_apply.py apply --all
    python3 tools/librarian_apply.py apply <proposal-id>
    python3 tools/librarian_apply.py rollback <snapshot-id>
    python3 tools/librarian_apply.py snapshots

Only test-library/ is allowed. The real library/ is never modified.
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.proposal_apply import (
    apply_proposal,
    format_plan,
    preflight_proposal,
    rollback,
    validate_test_library,
)
from skill_library.proposal_review import load_proposals


def _selected(store, args):
    proposals = load_proposals(store)
    if args.proposal_id:
        proposals = [p for p in proposals if p["id"] == args.proposal_id]
        if not proposals:
            raise ValueError(f"Unknown proposal: {args.proposal_id}")
    elif not args.all:
        raise ValueError("Specify a proposal ID or --all")
    return proposals


def cmd_plan(args):
    library = validate_test_library(args.library, REPO_ROOT / "library")
    for envelope in _selected(args.store, args):
        if envelope["status"] != "APPROVED":
            print(f"SKIP {envelope['id']}: status is {envelope['status']}")
            continue
        try:
            plan = preflight_proposal(library, envelope)
        except ValueError as e:
            print(f"BLOCKED {envelope['id']}: {e}")
            continue
        print(f"READY {envelope['id']}")
        print(format_plan(plan, library))
    return 0


def cmd_apply(args):
    library = validate_test_library(args.library, REPO_ROOT / "library")
    failures = 0
    for envelope in _selected(args.store, args):
        if envelope["status"] != "APPROVED":
            print(f"SKIP {envelope['id']}: status is {envelope['status']}")
            continue
        try:
            snapshot = apply_proposal(library, args.store, args.snapshots, envelope)
            print(f"APPLIED {envelope['id']} (snapshot {snapshot.name})")
        except Exception as e:
            failures += 1
            print(f"FAILED {envelope['id']}: {e}", file=sys.stderr)
    return 1 if failures else 0


def cmd_rollback(args):
    library = validate_test_library(args.library, REPO_ROOT / "library")
    proposal = rollback(library, args.store, args.snapshots, args.snapshot_id)
    print(f"ROLLED BACK {proposal['id']} to {args.snapshot_id}")
    return 0


def cmd_snapshots(args):
    if not args.snapshots.exists():
        print("No snapshots found.")
        return 0
    for snapshot in sorted(args.snapshots.iterdir()):
        if snapshot.is_dir() and (snapshot / "metadata.json").exists():
            print(snapshot.name)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Apply approved Librarian proposals to a test library")
    parser.add_argument("--store", type=Path, default=REPO_ROOT / "test-library" / "proposals.json")
    parser.add_argument("--library", type=Path, default=REPO_ROOT / "test-library")
    parser.add_argument("--snapshots", type=Path, default=REPO_ROOT / "test-library-snapshots")
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="Preflight approved proposals")
    p_plan.add_argument("proposal_id", nargs="?")
    p_plan.add_argument("--all", action="store_true")
    p_plan.set_defaults(func=cmd_plan)

    p_apply = sub.add_parser("apply", help="Apply approved proposals with snapshots")
    p_apply.add_argument("proposal_id", nargs="?")
    p_apply.add_argument("--all", action="store_true")
    p_apply.set_defaults(func=cmd_apply)

    p_rollback = sub.add_parser("rollback", help="Restore a snapshot")
    p_rollback.add_argument("snapshot_id")
    p_rollback.set_defaults(func=cmd_rollback)

    p_snapshots = sub.add_parser("snapshots", help="List snapshots")
    p_snapshots.set_defaults(func=cmd_snapshots)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, KeyError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
