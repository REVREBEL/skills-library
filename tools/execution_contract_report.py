#!/usr/bin/env python3
"""
Execution Contract Report CLI.

Derives a risk / side-effect / permission / environment profile for every
canonical skill package, and summarises coverage. This is the ZI-08 evidence
surface: it shows how much of the catalog can be executed safely today.

Usage:
    python3 tools/execution_contract_report.py
    python3 tools/execution_contract_report.py --output audit/zero-index/ZI-08/execution-profiles.csv
"""

import argparse
import csv
import json
import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from skill_library.config import LIBRARY_DIR, REPO_ROOT
from skill_library.execution import (
    derive_execution_profile,
    load_phase09_index,
    summarise_profiles,
)
from skill_library.identity import canonical_package_paths

DEFAULT_OUTPUT = os.path.join(REPO_ROOT, "audit", "zero-index", "ZI-08", "execution-profiles.csv")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Derive execution contracts for canonical skills")
    parser.add_argument("--library", default=LIBRARY_DIR, help="Library root (default: library/)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="CSV output path")
    parser.add_argument("--json", action="store_true", help="Print the summary as JSON")
    args = parser.parse_args(argv)

    phase09 = load_phase09_index()
    profiles = []
    for path in canonical_package_paths(args.library):
        profile = derive_execution_profile(
            path, phase09_index=phase09, library_dir=args.library
        )
        if profile is not None:
            profiles.append(profile)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "canonical_id",
            "risk",
            "tier",
            "side_effects",
            "permissions",
            "runtimes",
            "tools",
            "needs_network",
            "env_vars",
            "evidence",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for profile in profiles:
            row = profile.to_dict()
            row["side_effects"] = ";".join(row["side_effects"])
            row["permissions"] = ";".join(row["permissions"])
            row["runtimes"] = ";".join(row["runtimes"])
            row["tools"] = ";".join(row["tools"])
            row["env_vars"] = ";".join(row["env_vars"])
            row["evidence"] = ";".join(row["evidence"])
            writer.writerow(row)

    summary = summarise_profiles(profiles)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Canonical packages profiled: {summary['total']}")
        print(f"  by tier          : {summary['by_tier']}")
        print(f"  by risk          : {summary['by_risk']}")
        print(f"  by permission    : {summary['by_permission']}")
        print(f"  by side effect   : {summary['by_side_effect']}")
        print(f"  phase09 evidence : {summary['with_phase09_evidence']}")
        print(f"Wrote: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())