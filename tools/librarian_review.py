#!/usr/bin/env python3
"""Review Librarian proposals without applying them.

Usage:
    python3 tools/librarian_review.py list
    python3 tools/librarian_review.py show <proposal-id>
    python3 tools/librarian_review.py approve <proposal-id> --note "..."
    python3 tools/librarian_review.py reject <proposal-id> --note "..."
    python3 tools/librarian_review.py edit <proposal-id> --file proposal.json

The default store is test-library/proposals.json. Nothing in this command
modifies skills, routers, manifests, or ledgers.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.proposal_review import (
    edit_proposal,
    format_proposal,
    get_proposal,
    load_proposals,
    set_status,
)


def _subject(envelope):
    payload = envelope["proposal"]
    if envelope["kind"] == "merge":
        return f"{payload['candidate']} -> {payload['target']} ({payload['verdict']})"
    return f"{payload['candidate']} -> {payload['parent']} ({payload['action']})"


def cmd_list(args):
    proposals = load_proposals(args.store)
    if args.status:
        proposals = [p for p in proposals if p["status"] == args.status.upper()]
    if args.kind:
        proposals = [p for p in proposals if p["kind"] == args.kind]
    if args.candidate:
        proposals = [
            p for p in proposals
            if args.candidate in (p["proposal"].get("candidate"), p["proposal"].get("target"), p["proposal"].get("parent"))
        ]
    if args.json:
        print(json.dumps(proposals, indent=2))
        return 0
    if not proposals:
        print("No proposals found.")
        return 0
    print(f"{'ID':<22} {'KIND':<12} {'STATUS':<10} SUBJECT")
    for p in proposals:
        print(f"{p['id']:<22} {p['kind']:<12} {p['status']:<10} {_subject(p)}")
    return 0


def cmd_show(args):
    proposal = get_proposal(args.store, args.proposal_id)
    if args.json:
        print(json.dumps(proposal, indent=2))
    else:
        print(format_proposal(proposal))
    return 0


def cmd_decision(args):
    status = {"approve": "APPROVED", "reject": "REJECTED"}[args.action]
    proposal = set_status(args.store, args.proposal_id, status, args.note or "")
    print(f"{proposal['id']}: {proposal['status']}")
    return 0


def cmd_edit(args):
    try:
        payload = json.loads(Path(args.file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Could not read proposal JSON: {e}", file=sys.stderr)
        return 1
    try:
        proposal = edit_proposal(args.store, args.proposal_id, payload, args.note or "")
    except (ValueError, KeyError) as e:
        print(f"Edit rejected: {e}", file=sys.stderr)
        return 1
    print(f"{proposal['id']}: {proposal['status']} (revision {proposal['revision']})")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Review Librarian proposals; never apply them")
    parser.add_argument("--store", type=Path, default=REPO_ROOT / "test-library" / "proposals.json")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List proposals")
    p_list.add_argument("--status", choices=["PROPOSED", "APPROVED", "REJECTED", "APPLIED", "ROLLED_BACK"])
    p_list.add_argument("--kind", choices=["merge", "granularity"])
    p_list.add_argument("--candidate", help="Filter by candidate, target, or parent name")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show one proposal")
    p_show.add_argument("proposal_id")
    p_show.add_argument("--json", action="store_true")
    p_show.set_defaults(func=cmd_show)

    for action in ("approve", "reject"):
        p = sub.add_parser(action, help=f"Mark a proposal {action}d")
        p.add_argument("proposal_id")
        p.add_argument("--note", default="")
        p.set_defaults(func=cmd_decision, action=action)

    p_edit = sub.add_parser("edit", help="Replace a proposal payload from a JSON file")
    p_edit.add_argument("proposal_id")
    p_edit.add_argument("--file", required=True)
    p_edit.add_argument("--note", default="")
    p_edit.set_defaults(func=cmd_edit)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
