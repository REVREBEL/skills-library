#!/usr/bin/env python3
"""
CLI Tool: skill-library
The unified management interface for the Agent Skills Intake, Canonical Library,
Published Runtime Branch, and Configured Runtime Targets.

Commands:
  scan             Non-destructively inspect intake/ candidates
  intake           Evaluate candidates, check overlap, and enforce human approval gates
  apply            Install an approved candidate into library/ and update router/manifest
  publish-runtime  Generate or update the standalone 'runtime' branch from main:library/
  sync             Reconcile configured runtime targets (clones/sparse checkouts) with runtime branch
  capture-intake   Capture dirty workstation runtime state and transport via incoming/* snapshot
  convert-incoming Convert an incoming snapshot branch into a reviewed intake/ PR branch
  validate         Run full living library, publication, and target validation
  status           Print concise library status and target checkout metrics
  test             Run automated regression test suite
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
    RUNTIME_BRANCH,
    RUNTIME_DIR,
    TARGETS_CONFIG_PATH,
    VALIDATION_REPORT_FILE,
    load_runtime_targets,
)
from skill_library.intake import apply_candidate, evaluate_candidate
from skill_library.intake_capture import capture_dirty_target, convert_incoming_to_intake, scan_target_dirty_state
from skill_library.ledger import ChangeLedger
from skill_library.manifest import RuntimeManifest
from skill_library.publisher import get_commit_tree_sha, get_library_tree_sha, get_ref_commit_sha, publish_runtime_branch
from skill_library.scanner import scan_intake
from skill_library.sync import detect_target_state, sync_all_targets, sync_target
from skill_library.validator import validate_library_integrity


def cmd_scan(args):
    print("Scanning intake/ candidates ...")
    candidates = scan_intake()

    if args.json:
        print(json.dumps([c.to_dict() for c in candidates], indent=2))
        return 0

    print(f"\n--- Intake Candidates ({len(candidates)}) ---")
    if not candidates:
        print("  (None found in intake/)")
    for c in candidates:
        valid_mark = "VALID" if c.has_skill_md and c.frontmatter_valid else "INVALID"
        print(f"  • {c.name:25} [{valid_mark}] -> Suggested: {c.suggested_category}/{c.suggested_subcategory}")
        if c.issues:
            for issue in c.issues:
                print(f"      Issue: {issue}")

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
        print("\nNext step: Run 'publish-runtime' and 'sync' to propagate changes to runtime targets.")
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


def cmd_publish_runtime(args):
    print(f"Publishing runtime branch '{args.branch}' from canonical library/ ...")
    res = publish_runtime_branch(
        repo_path=REPO_ROOT,
        branch_name=args.branch,
        push=args.push,
        remote=args.remote,
    )
    status_label = res["status"].upper()
    print(f"Status:     {status_label}")
    print(f"Branch:     {res['branch']}")
    print(f"Tree SHA:   {res['tree_sha']}")
    print(f"Commit SHA: {res['commit_sha']}")
    if args.push:
        print(f"Pushed to:  {args.remote}/{res['branch']}")
    return 0


def cmd_sync(args):
    print("Synchronizing configured runtime targets ...")
    report = sync_all_targets(source_repo=REPO_ROOT)
    print(report.summary())
    return 1 if report.has_errors else 0


def cmd_capture_intake(args):
    targets = load_runtime_targets()
    captured_any = False
    has_errors = False

    for t in targets:
        if not t.enabled:
            continue
        if args.target and t.name != args.target:
            continue

        print(f"Checking target '{t.name}' ({t.path}) for dirty runtime changes ...")
        res = capture_dirty_target(
            target=t,
            push=not args.no_push,
            remote=args.remote,
            trigger_workflow=args.dispatch_workflow,
        )
        if res.get("captured"):
            captured_any = True
            print(f"  SUCCESS: Captured {len(res['packages'])} packages into snapshot branch '{res['branch']}'.")
            if res.get("pushed"):
                print(f"  Pushed to {args.remote} and reset local checkout cleanly.")
            if res.get("workflow_triggered"):
                print(f"  DISPATCHED: {res.get('workflow_message')}")
            elif args.dispatch_workflow:
                print(f"  WORKFLOW DISPATCH NOTE: {res.get('workflow_message')}")
        elif res.get("retained"):
            has_errors = True
            print(f"  FAILED: {res.get('error')}. Dirty state retained locally.")
        else:
            print(f"  Target is clean ({res.get('reason', 'no changes')}).")

    return 1 if has_errors else 0


def cmd_convert_incoming(args):
    print(f"Converting incoming branch '{args.incoming_branch}' to intake PR branch ...")
    res = convert_incoming_to_intake(
        repo_path=REPO_ROOT,
        incoming_branch=args.incoming_branch,
        base_branch=args.base_branch,
        remote=args.remote,
    )
    print(f"Created intake branch: {res['intake_branch']}")
    print(f"Staged packages:       {', '.join(res['packages_staged']) or 'None'}")
    return 0


def cmd_validate(args):
    print("Running living library validation (canonical, routers, publication, targets)...")
    manifest = RuntimeManifest()
    res = validate_library_integrity(
        manifest=manifest,
        verify_publication=not args.skip_publication,
        verify_targets=not args.skip_targets,
    )
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

    lib_tree = get_library_tree_sha(REPO_ROOT, ref="HEAD")
    runtime_commit = get_ref_commit_sha(REPO_ROOT, f"refs/heads/{RUNTIME_BRANCH}")
    runtime_tree = get_commit_tree_sha(REPO_ROOT, runtime_commit) if runtime_commit else None

    print(f"Canonical library skills: {len(manifest.skills)}")
    print(f"Pending intake candidates: {len(intake_candidates)}")
    print(f"HEAD:library Tree SHA:    {lib_tree[:10]}")
    if runtime_commit:
        status_match = "MATCH" if runtime_tree == lib_tree else "OUT_OF_SYNC"
        print(f"Published runtime branch: {runtime_commit[:10]} (Tree: {runtime_tree[:10]} [{status_match}])")
    else:
        print("Published runtime branch: NOT FOUND (run 'publish-runtime')")

    print("\n--- Configured Runtime Targets ---")
    targets = load_runtime_targets()
    for t in targets:
        state = detect_target_state(t.resolved_path)
        status_text = "ABSENT"
        if state["exists"]:
            if state["is_git"]:
                status_text = "DIRTY" if state["is_dirty"] else "CLEAN"
            else:
                status_text = "NON-GIT"
        print(f"  • {t.name:20} [{t.mode:6}] -> {t.path} ({status_text}, enabled={t.enabled})")

    return 0


def cmd_test(args):
    import unittest
    loader = unittest.TestLoader()
    tests_dir = os.path.join(REPO_ROOT, "tests")
    suite = loader.discover(tests_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    return 0 if res.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(
        prog="skill-library",
        description="Agent Skills Intake, Canonical Library, and Runtime Sync Tool",
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # scan
    p_scan = subparsers.add_parser("scan", help="Non-destructively inspect intake candidates")
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
    p_apply.add_argument("--approve", action="store_true", help="Authorize application through Human Approval Gate")
    p_apply.add_argument("--dry-run", action="store_true", help="Simulate without modifying files")

    # publish-runtime
    p_pub = subparsers.add_parser("publish-runtime", help="Publish runtime branch from main:library/")
    p_pub.add_argument("--branch", default=RUNTIME_BRANCH, help=f"Branch name (default: {RUNTIME_BRANCH})")
    p_pub.add_argument("--push", action="store_true", help="Push branch to remote after generation")
    p_pub.add_argument("--remote", default="origin", help="Remote name (default: origin)")

    # sync
    p_sync = subparsers.add_parser("sync", help="Synchronize configured runtime targets")
    p_sync.add_argument("--dry-run", action="store_true", help="Simulate changes without modifying checkouts")

    # capture-intake
    p_cap = subparsers.add_parser("capture-intake", help="Capture dirty target state into incoming/* snapshot branch")
    p_cap.add_argument("--target", help="Specific target name to capture (default: all)")
    p_cap.add_argument("--remote", default="origin", help="Remote to push snapshot branch")
    p_cap.add_argument("--no-push", action="store_true", help="Commit snapshot locally without pushing to remote")
    p_cap.add_argument("--dispatch-workflow", action="store_true", help="Trigger runtime-intake.yml GitHub Action via gh workflow run")

    # convert-incoming
    p_conv = subparsers.add_parser("convert-incoming", help="Convert incoming snapshot branch to intake/ PR branch")
    p_conv.add_argument("--incoming-branch", required=True, help="Name of incoming branch (e.g. incoming/20261008-xyz)")
    p_conv.add_argument("--base-branch", default="main", help="Base branch (default: main)")
    p_conv.add_argument("--remote", default="origin", help="Remote name (default: origin)")

    # validate
    p_val = subparsers.add_parser("validate", help="Run living library and runtime validation")
    p_val.add_argument("--output-report", action="store_true", help="Write audit/validation-report.md")
    p_val.add_argument("--skip-publication", action="store_true", help="Skip runtime branch publication check")
    p_val.add_argument("--skip-targets", action="store_true", help="Skip target checkout validation")

    # status
    subparsers.add_parser("status", help="Print concise status overview")

    # test
    subparsers.add_parser("test", help="Run automated test suite")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    dispatch = {
        "scan": cmd_scan,
        "intake": cmd_intake,
        "apply": cmd_apply,
        "publish-runtime": cmd_publish_runtime,
        "sync": cmd_sync,
        "capture-intake": cmd_capture_intake,
        "convert-incoming": cmd_convert_incoming,
        "validate": cmd_validate,
        "status": cmd_status,
        "test": cmd_test,
    }

    exit_code = dispatch[args.command](args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
