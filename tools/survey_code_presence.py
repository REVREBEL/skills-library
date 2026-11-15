#!/usr/bin/env python3
"""
Code-Presence Survey CLI.

Classifies every canonical skill package as ``code`` or ``prose`` so the risk
model can be sized before ZI-08 design begins.

Usage:
    python3 tools/survey_code_presence.py
    python3 tools/survey_code_presence.py --output audit/zero-index/ZI-07/code-presence.csv
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from skill_library.code_presence import survey_library, summarise
from skill_library.config import LIBRARY_DIR, REPO_ROOT

DEFAULT_OUTPUT = os.path.join(REPO_ROOT, "audit", "zero-index", "ZI-07", "code-presence.csv")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Survey code presence across canonical skills")
    parser.add_argument("--library", default=LIBRARY_DIR, help="Library root (default: library/)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="CSV output path")
    parser.add_argument("--json", action="store_true", help="Print the summary as JSON")
    args = parser.parse_args(argv)

    surveys = survey_library(args.library)
    summary = summarise(surveys)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(surveys[0].to_row()))
        writer.writeheader()
        for survey in surveys:
            writer.writerow(survey.to_row())

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Canonical packages surveyed: {summary['total']}")
        print(f"  code : {summary['code']['total']} ({summary['code_share_pct']}%)")
        print(f"         with scripts          : {summary['code']['with_scripts']}")
        print(f"         with code blocks      : {summary['code']['with_code_blocks']}")
        print(f"         with command metadata : {summary['code']['with_command_metadata']}")
        print(f"  prose: {summary['prose']['total']}")
        print(f"         risk unknown          : {summary['prose']['risk_unknown']}")
        print(f"         risk missing          : {summary['prose']['risk_missing']}")
        print(f"Wrote: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())