#!/usr/bin/env python3
"""
CLI Tool: skill-library
The unified management interface for the Agent Skills Intake, Canonical Library,
and Runtime Synchronization Pipeline.

Commands:
  scan      Non-destructively inspect intake/ and global runtime (~/.agents/skills/)
  intake    Evaluate candidates, check overlap, and enforce human approval gates
  apply     Install an approved candidate into library/ and update router/manifest
  sync      Reconcile global runtime symlinks with manifest, stage external installs
  validate  Run full living library and runtime validation
  status    Print concise library status and health metrics
  test      Run automated end-to-end test scenarios
"""

import argparse
import json
import os
import sys

# Ensure tools directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from skill_library.config import (
    CATEGORIES,
    DEEP_CATEGORIES,
    FLAT_CATEGORIES,
    INTAKE_DIR,
    LIBRARY_DIR,
    MANIFEST_FILE,
    REPO_ROOT,
    RUNTIME_DIR,
    VALIDATION_REPORT_FILE,
)
from skill_library.intake import apply_candidate, evaluate_candidate
from skill_library.ledger import ChangeLedger
from skill_library.manifest import RuntimeManifest
from skill_library.pilot import run_targeted_pilot
from skill_library.scanner import run_full_scan, scan_intake, scan_runtime
from skill_library.sync import reconcile_runtime_symlinks
from skill_library.validator import validate_library


def cmd_scan(args):
    print(f"Scanning intake/ and {RUNTIME_DIR} ...")
    res = run_full_scan()

    if args.json:
        print(json.dumps(res.to_dict(), indent=2))
        return 0

    print(f"\n--- Intake Candidates ({len(res.intake_candidates)}) ---")
    if not res.intake_candidates:
        print("  (None found in intake/)")
    for c in res.intake_candidates:
        valid_mark = "VALID" if c.has_skill_md and c.frontmatter_valid else "INVALID"
        print(f"  • {c.name:25} [{valid_mark}] -> Suggested: {c.suggested_category}/{c.suggested_subcategory}")
        if c.issues:
            for issue in c.issues:
                print(f"      Issue: {issue}")

    print(f"\n--- Runtime Entries ({len(res.runtime_entries)}) ---")
    for r in res.runtime_entries:
        target_str = f"-> {r.target_path}" if r.target_path else ""
        print(f"  • {r.name:25} [{r.classification:18}] {target_str}")
        if r.action:
            print(f"      Action: {r.action}")

    return 0


def cmd_intake(args):
    intake_candidates = scan_intake()
    if not intake_candidates:
        print("No candidates found in intake/.")
        return 0

    manifest = RuntimeManifest()
    targets = [args.candidate] if args.candidate else [c.name for c in intake_candidates]

    evaluations = []
    has_approval_blocker = False

    for cname in targets:
        print(f"\nEvaluating candidate '{cname}' ...")
        ev = evaluate_candidate(candidate_name=cname, manifest=manifest)
        evaluations.append(ev)
        print(ev.summary())
        if ev.approval_required:
            has_approval_blocker = True

    if args.json:
        print(json.dumps([e.to_dict() for e in evaluations], indent=2))

    if has_approval_blocker and not args.force:
        print("\n[HUMAN APPROVAL GATE] One or more candidates require human approval.")
        print("Review the decisions above before running 'apply'.")

    return 0


def cmd_apply(args):
    print(f"Applying candidate '{args.candidate}'...")
    try:
        manifest = RuntimeManifest()
        ledger = ChangeLedger()
        res = apply_candidate(
            candidate_name=args.candidate,
            category=args.category,
            subcategory=args.subcategory,
            canonical_name=args.canonical_name,
            approved=args.approve,
            manifest=manifest,
            ledger=ledger,
            dry_run=args.dry_run,
        )
        op_label = "Updated existing canonical skill" if res.get("is_update") else "Installed new skill"
        print(f"SUCCESS: {op_label} '{args.candidate}' -> {res['target_directory']}")
        print(f"Router updated: {res['router_updated']}")
        print("Manifest and change ledger updated.")
        symlink_out = res.get("runtime_symlink", os.path.join(RUNTIME_DIR, res["runtime_name"]))
        print(f"Runtime symlink established: {symlink_out}")
        return 0
    except PermissionError as pe:
        print(f"\n[HUMAN APPROVAL GATE BLOCKED]\n{pe}", file=sys.stderr)
        return 1
    except ValueError as ve:
        print(f"\n[PRE-INSTALL VALIDATION FAILED - ZERO CHANGES]\n{ve}", file=sys.stderr)
        return 1
    except RuntimeError as re:
        print(f"\n[POST-INSTALL CHECKS FAILED - TRANSACTION ROLLED BACK]\n{re}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[ERROR] Failed to apply candidate: {e}", file=sys.stderr)
        return 1


def cmd_sync(args):
    print(f"Reconciling {RUNTIME_DIR} runtime symlinks with canonical manifest...")
    manifest = RuntimeManifest()
    report = reconcile_runtime_symlinks(
        manifest=manifest,
        dry_run=args.dry_run,
        stage_external=not args.no_stage,
    )
    print(report.summary())
    return 1 if report.errors else 0


def cmd_validate(args):
    print("Running living library validation (dynamic population and router analysis)...")
    manifest = RuntimeManifest()
    res = validate_library(manifest=manifest)
    print(res.summary())

    if args.output_report:
        os.makedirs(os.path.dirname(VALIDATION_REPORT_FILE), exist_ok=True)
        with open(VALIDATION_REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Living Library Validation Report\n\n```text\n{res.summary()}\n```\n")
        print(f"Saved validation report to: {VALIDATION_REPORT_FILE}")

    return 0 if res.is_valid else 1


def cmd_status(args):
    manifest = RuntimeManifest()
    intake_candidates = scan_intake()
    runtime_entries = scan_runtime(manifest=manifest)

    managed_links = sum(1 for r in runtime_entries if r.classification == "MANAGED_LINK")
    broken_links = sum(1 for r in runtime_entries if r.classification == "BROKEN_LINK")
    external_installs = sum(1 for r in runtime_entries if r.classification == "EXTERNAL_PHYSICAL")
    collisions = sum(1 for r in runtime_entries if r.classification == "COLLISION")

    print(f"Canonical skills:      {len(manifest.skills)}")
    print(f"Managed runtime links: {managed_links}")
    print(f"New external installs: {external_installs}")
    print(f"Broken links:          {broken_links}")
    print(f"Pending intake:        {len(intake_candidates)}")
    print(f"Conflicts/Collisions:  {collisions}")

    # Health check
    is_healthy = (broken_links == 0 and collisions == 0)
    print(f"Validation Status:     {'PASS' if is_healthy else 'ATTENTION_NEEDED'}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="skill-library",
        description="Agent Skills Intake, Canonical Library, and Runtime Sync Tool",
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # scan
    p_scan = subparsers.add_parser("scan", help="Non-destructively inspect intake and runtime")
    p_scan.add_argument("--json", action="store_true", help="Output JSON format")

    # intake
    p_intake = subparsers.add_parser("intake", help="Evaluate candidates in intake/")
    p_intake.add_argument("--candidate", help="Specific candidate to evaluate")
    p_intake.add_argument("--force", action="store_true", help="Bypass approval warning display")
    p_intake.add_argument("--json", action="store_true", help="Output JSON format")

    # apply
    p_apply = subparsers.add_parser("apply", help="Install approved candidate into library/")
    p_apply.add_argument("--candidate", required=True, help="Candidate name in intake/")
    p_apply.add_argument("--category", choices=CATEGORIES, help="Target category (required for new skills)")
    p_apply.add_argument("--subcategory", help="Target subcategory (required for new skills)")
    p_apply.add_argument("--canonical-name", help="Optional override for canonical package name")
    p_apply.add_argument("--approve", action="store_true", help="Authorize application through the Human Approval Gate")
    p_apply.add_argument("--dry-run", action="store_true", help="Simulate without modifying files")

    # sync
    p_sync = subparsers.add_parser("sync", help="Reconcile runtime symlinks with manifest")
    p_sync.add_argument("--dry-run", action="store_true", help="Simulate changes")
    p_sync.add_argument("--no-stage", action="store_true", help="Do not stage physical installs to intake")

    # validate
    p_val = subparsers.add_parser("validate", help="Run living library validation")
    p_val.add_argument("--output-report", action="store_true", help="Write audit/validation-report.md")

    # status
    subparsers.add_parser("status", help="Print concise status overview")

    # test
    subparsers.add_parser("test", help="Run automated test suite for Scenarios A-F")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    def cmd_test(args):
        import unittest
        loader = unittest.TestLoader()
        tests_dir = os.path.join(REPO_ROOT, "tests")
        suite = loader.discover(tests_dir, pattern="test_*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(suite)
        return 0 if res.wasSuccessful() else 1

    dispatch = {
        "scan": cmd_scan,
        "intake": cmd_intake,
        "apply": cmd_apply,
        "sync": cmd_sync,
        "validate": cmd_validate,
        "status": cmd_status,
        "test": cmd_test,
    }

    exit_code = dispatch[args.command](args)
    sys.exit(exit_code)



if __name__ == "__main__":
    main()
