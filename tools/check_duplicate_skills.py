#!/usr/bin/env python3
"""
tools/check_duplicate_skills.py

Permanent repository maintenance tool for detecting, auditing, and safely
cleaning up duplicate and nested child skill packages in the canonical library.

Background & Invariants:
-------------------------
In the canonical Agent Skills library:
1. Every skill package must be a single, standalone leaf package:
   library/<category>/<subcategory>/<skill-name>/
2. Skill packages must NOT contain nested child skills (directories containing
   their own SKILL.md) inside them.
3. When child skills are promoted or extracted as canonical members (e.g., Phase 08
   Batch 30 where design-it styles were extracted to taste-and-critique/), the
   original parent package must not retain copies of those child skills inside its
   own folder.

Usage:
------
# 1. Audit / check mode (non-mutating, returns 0 if clean, 1 if duplicates found):
python3 tools/check_duplicate_skills.py
python3 tools/check_duplicate_skills.py --json

# 2. Preview cleanup (dry-run):
python3 tools/check_duplicate_skills.py --fix --dry-run

# 3. Perform safe cleanup of confirmed duplicates:
python3 tools/check_duplicate_skills.py --fix --yes

# 4. Via npm task alias:
npm run audit:duplicates
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class NestedSkillViolation:
    parent_package: str
    parent_path: str
    child_name: str
    child_path: str
    canonical_counterparts: List[str]
    is_confirmed_duplicate: bool
    child_file_count: int


@dataclass
class ContentDuplicateViolation:
    content_hash: str
    skill_paths: List[str]
    skill_names: List[str]


@dataclass
class NameCollisionViolation:
    skill_name: str
    subcategory: str
    skill_paths: List[str]


@dataclass
class DuplicateAuditReport:
    library_dir: str
    total_canonical_skills: int = 0
    total_routers: int = 0
    nested_violations: List[NestedSkillViolation] = field(default_factory=list)
    content_duplicates: List[ContentDuplicateViolation] = field(default_factory=list)
    name_collisions: List[NameCollisionViolation] = field(default_factory=list)
    unconfirmed_nested_skills: List[NestedSkillViolation] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        """
        True if there are zero structural duplicate violations
        (no nested child skills, no unconfirmed nested skills, and no same-subcategory name collisions).
        """
        return (
            len(self.nested_violations) == 0
            and len(self.name_collisions) == 0
            and len(self.unconfirmed_nested_skills) == 0
        )

    @property
    def total_nested_count(self) -> int:
        return len(self.nested_violations) + len(self.unconfirmed_nested_skills)

    def summary_dict(self) -> dict:
        return {
            "library_dir": self.library_dir,
            "is_clean": self.is_clean,
            "total_canonical_skills": self.total_canonical_skills,
            "total_routers": self.total_routers,
            "nested_child_duplicates": len(self.nested_violations),
            "unconfirmed_nested_skills": len(self.unconfirmed_nested_skills),
            "content_duplicates": len(self.content_duplicates),
            "name_collisions": len(self.name_collisions),
        }


def get_router_paths(library_path: Path) -> Set[Path]:
    """
    Identifies all router SKILL.md paths in the library:
    - Root router: library/SKILL.md
    - Category routers: library/<category>/SKILL.md
    - Subcategory routers: library/<category>/<subcategory>/SKILL.md (for deep categories)
    """
    routers = set()
    root_router = library_path / "SKILL.md"
    if root_router.exists():
        routers.add(root_router.resolve())

    for cat_dir in library_path.iterdir():
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        cat_router = cat_dir / "SKILL.md"
        if cat_router.exists():
            routers.add(cat_router.resolve())

        for subcat_dir in cat_dir.iterdir():
            if not subcat_dir.is_dir() or subcat_dir.name.startswith("."):
                continue
            subcat_router = subcat_dir / "SKILL.md"
            if subcat_router.exists():
                routers.add(subcat_router.resolve())

    return routers


def audit_duplicate_skills(library_dir: str = "library") -> DuplicateAuditReport:
    """
    Performs a thorough audit of the library directory for:
    1. Nested child skill packages within canonical packages
    2. Same-subcategory package name collisions
    3. Exact content duplicates (SHA-256 matching SKILL.md)
    """
    lib = Path(library_dir).resolve()
    if not lib.exists() or not lib.is_dir():
        raise FileNotFoundError(f"Library directory not found at: {library_dir}")

    report = DuplicateAuditReport(library_dir=str(lib))
    router_paths = get_router_paths(lib)
    report.total_routers = len(router_paths)

    # 1. Discover all canonical packages (depth 3 relative to library: <cat>/<subcat>/<pkg>)
    canonical_packages: Dict[str, List[Path]] = {}
    canonical_dirs: Set[Path] = set()
    all_skill_mds = list(lib.glob("**/SKILL.md"))

    for smd in all_skill_mds:
        smd_res = smd.resolve()
        if smd_res in router_paths:
            continue
        try:
            rel = smd_res.parent.relative_to(lib)
        except ValueError:
            continue

        # Canonical skills are at category/subcategory/skill-name (parts == 3)
        if len(rel.parts) == 3:
            pkg_name = rel.parts[2]
            canonical_packages.setdefault(pkg_name, []).append(smd_res.parent)
            canonical_dirs.add(smd_res.parent)

    report.total_canonical_skills = len(canonical_dirs)

    # 2. Check for nested child skills (depth > 3)
    for smd in all_skill_mds:
        smd_res = smd.resolve()
        if smd_res in router_paths:
            continue
        try:
            rel = smd_res.parent.relative_to(lib)
        except ValueError:
            continue

        if len(rel.parts) > 3:
            # Child skill nested inside another skill package
            parent_pkg_dir = lib / rel.parts[0] / rel.parts[1] / rel.parts[2]
            parent_name = rel.parts[2]
            child_name = smd_res.parent.name
            child_path = str(smd_res.parent)

            # Check if this child exists as a canonical standalone skill anywhere
            canonical_peers = [str(p) for p in canonical_packages.get(child_name, [])]
            is_confirmed = len(canonical_peers) > 0

            # Count files in the child directory
            file_count = sum(len(files) for _, _, files in os.walk(str(smd_res.parent)))

            violation = NestedSkillViolation(
                parent_package=parent_name,
                parent_path=str(parent_pkg_dir),
                child_name=child_name,
                child_path=child_path,
                canonical_counterparts=canonical_peers,
                is_confirmed_duplicate=is_confirmed,
                child_file_count=file_count,
            )

            if is_confirmed:
                report.nested_violations.append(violation)
            else:
                report.unconfirmed_nested_skills.append(violation)

    # 3. Check for name collisions within the same subcategory
    subcat_skills: Dict[Tuple[str, str], List[Path]] = {}
    for pkg_dir in canonical_dirs:
        rel = pkg_dir.relative_to(lib)
        subcat_key = (rel.parts[0], rel.parts[1])
        subcat_skills.setdefault(subcat_key, []).append(pkg_dir)

    for (cat, subcat), pkgs in subcat_skills.items():
        names: Dict[str, List[Path]] = {}
        for p in pkgs:
            names.setdefault(p.name, []).append(p)
        for name, p_list in names.items():
            if len(p_list) > 1:
                report.name_collisions.append(
                    NameCollisionViolation(
                        skill_name=name,
                        subcategory=f"{cat}/{subcat}",
                        skill_paths=[str(p) for p in p_list],
                    )
                )

    # 4. Check for identical SKILL.md content hashes among canonical packages
    content_hashes: Dict[str, List[Path]] = {}
    for pkg_dir in canonical_dirs:
        smd = pkg_dir / "SKILL.md"
        try:
            content = smd.read_bytes()
            h = hashlib.sha256(content).hexdigest()
            content_hashes.setdefault(h, []).append(pkg_dir)
        except Exception:
            pass

    for h, p_list in content_hashes.items():
        if len(p_list) > 1:
            report.content_duplicates.append(
                ContentDuplicateViolation(
                    content_hash=h,
                    skill_paths=[str(p) for p in p_list],
                    skill_names=[p.name for p in p_list],
                )
            )

    return report


@dataclass
class CleanupResult:
    cleaned_directories: List[str] = field(default_factory=list)
    skipped_directories: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    dry_run: bool = False


def cleanup_duplicate_skills(
    report: DuplicateAuditReport,
    dry_run: bool = False,
    clean_unconfirmed: bool = False,
) -> CleanupResult:
    """
    Safely removes confirmed nested duplicate skill directories.
    - Only deletes directories inside parent packages that contain SKILL.md
      and have verified canonical counterparts.
    - Parent package root files (SKILL.md, references/, assets/, etc.) are never deleted.
    - If clean_unconfirmed is False, unconfirmed nested skills are skipped for safety.
    """
    result = CleanupResult(dry_run=dry_run)
    targets_to_clean: List[NestedSkillViolation] = list(report.nested_violations)

    if clean_unconfirmed:
        targets_to_clean.extend(report.unconfirmed_nested_skills)

    # Sort by path depth descending so nested children inside nested children
    # are removed from leaf upward
    targets_to_clean.sort(key=lambda v: len(Path(v.child_path).parts), reverse=True)

    for violation in targets_to_clean:
        target_path = Path(violation.child_path)
        if not target_path.exists():
            continue

        # Extra safety check: ensure the target is strictly inside the parent path
        try:
            target_path.relative_to(Path(violation.parent_path))
        except ValueError:
            result.errors.append(
                f"Safety check failed: {target_path} is not inside parent {violation.parent_path}"
            )
            continue

        # Extra safety check: never delete the parent package itself
        if target_path.resolve() == Path(violation.parent_path).resolve():
            result.errors.append(
                f"Safety check failed: refused to delete parent package {target_path}"
            )
            continue

        if dry_run:
            result.cleaned_directories.append(str(target_path))
        else:
            try:
                shutil.rmtree(target_path)
                result.cleaned_directories.append(str(target_path))
                # Safely prune empty intermediate parent directories up to (not including) parent_root
                parent_root = Path(violation.parent_path).resolve()
                p = target_path.parent.resolve()
                while p != parent_root and p.exists():
                    try:
                        if not any(p.iterdir()):
                            p.rmdir()
                            p = p.parent.resolve()
                        else:
                            break
                    except Exception:
                        break
            except Exception as e:
                result.errors.append(f"Failed to remove {target_path}: {e}")

    return result


def print_report(report: DuplicateAuditReport, verbose: bool = False):
    print("=" * 72)
    print("Agent Skills Library: Duplicate & Nested Package Audit")
    print("=" * 72)
    print(f"Library Path:             {report.library_dir}")
    print(f"Canonical Active Skills:  {report.total_canonical_skills}")
    print(f"Verified Routers:         {report.total_routers}")
    print(f"Nested Child Duplicates:  {len(report.nested_violations)}")
    print(f"Unconfirmed Nested Skills:{len(report.unconfirmed_nested_skills)}")
    print(f"Content Duplicates:       {len(report.content_duplicates)}")
    print(f"Subcategory Collisions:   {len(report.name_collisions)}")
    print("-" * 72)

    if report.is_clean:
        print("STATUS: PASS (0 structural duplicate or nested skill violations)")
        if report.content_duplicates:
            print("\n[INFO / WARNING] Cross-Category Content-Identical Skills:")
            for cd in report.content_duplicates:
                print(f"  * Hash {cd.content_hash[:12]}: {', '.join(cd.skill_names)}")
                for p in cd.skill_paths:
                    print(f"      - {p}")
        print("=" * 72)
        return

    print("STATUS: VIOLATIONS DETECTED")
    print("-" * 72)

    if report.nested_violations:
        # Group by parent package
        parents: Dict[str, List[NestedSkillViolation]] = {}
        for v in report.nested_violations:
            parents.setdefault(v.parent_package, []).append(v)

        print(f"\n[!] Nested Child Skill Duplicates ({len(report.nested_violations)} in {len(parents)} packages):")
        for p_name, children in sorted(parents.items()):
            print(f"  * {p_name} ({len(children)} nested duplicate skills):")
            for c in children[:5 if not verbose else len(children)]:
                canonical_str = ", ".join(c.canonical_counterparts) if c.canonical_counterparts else "none"
                print(f"      - {c.child_name} -> canonical: {canonical_str}")
            if len(children) > 5 and not verbose:
                print(f"      ... and {len(children) - 5} more (use --verbose to view all)")

    if report.unconfirmed_nested_skills:
        print(f"\n[?] Unconfirmed Nested Skills (no canonical counterpart found):")
        for v in report.unconfirmed_nested_skills:
            print(f"  * {v.child_name} in {v.parent_package} ({v.child_path})")

    if report.content_duplicates:
        print(f"\n[!] Content-Identical Skills (matching SHA-256 of SKILL.md):")
        for cd in report.content_duplicates:
            print(f"  * Hash {cd.content_hash[:12]}: {', '.join(cd.skill_names)}")
            for p in cd.skill_paths:
                print(f"      - {p}")

    if report.name_collisions:
        print(f"\n[!] Subcategory Name Collisions:")
        for nc in report.name_collisions:
            print(f"  * '{nc.skill_name}' duplicated in {nc.subcategory}:")
            for p in nc.skill_paths:
                print(f"      - {p}")

    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(
        description="Audit and clean duplicate/nested skill packages in the Agent Skills library."
    )
    parser.add_argument(
        "library_dir",
        nargs="?",
        default="library",
        help="Path to the library directory (default: library)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Safely remove confirmed nested duplicate skill directories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cleanup actions without modifying disk.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompt when running with --fix.",
    )
    parser.add_argument(
        "--strict-content",
        action="store_true",
        help="Treat cross-category identical content as an audit failure (exit 1).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output audit report as JSON.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print full list of violated paths.",
    )

    args = parser.parse_args()

    try:
        report = audit_duplicate_skills(args.library_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    is_clean = report.is_clean
    if args.strict_content and len(report.content_duplicates) > 0:
        is_clean = False

    if args.json:
        data = {
            "summary": report.summary_dict(),
            "nested_violations": [asdict(v) for v in report.nested_violations],
            "unconfirmed_nested_skills": [asdict(v) for v in report.unconfirmed_nested_skills],
            "content_duplicates": [asdict(v) for v in report.content_duplicates],
            "name_collisions": [asdict(v) for v in report.name_collisions],
        }
        print(json.dumps(data, indent=2))
        sys.exit(0 if is_clean else 1)

    print_report(report, verbose=args.verbose)

    if args.fix:
        if report.is_clean or (len(report.nested_violations) == 0):
            print("\nNo nested duplicate skills to clean up.")
            sys.exit(0)

        total_targets = len(report.nested_violations)
        print(f"\nTargeted for cleanup: {total_targets} confirmed nested child skill directories.")

        if not args.dry_run and not args.yes:
            try:
                confirm = input("Are you sure you want to proceed with cleanup? [y/N]: ").strip().lower()
                if confirm not in ("y", "yes"):
                    print("Cleanup aborted by user.")
                    sys.exit(1)
            except EOFError:
                print("Non-interactive session detected. Use --yes to confirm cleanup.", file=sys.stderr)
                sys.exit(1)

        result = cleanup_duplicate_skills(report, dry_run=args.dry_run)
        if args.dry_run:
            print(f"\n[DRY RUN] Would remove {len(result.cleaned_directories)} directories:")
            for d in result.cleaned_directories[:10]:
                print(f"  - {d}")
            if len(result.cleaned_directories) > 10:
                print(f"  ... and {len(result.cleaned_directories) - 10} more.")
        else:
            print(f"\nSuccessfully removed {len(result.cleaned_directories)} duplicate directories.")
            if result.errors:
                print(f"Encountered {len(result.errors)} errors during cleanup:")
                for err in result.errors:
                    print(f"  ! {err}")

        # Post-cleanup audit verification
        if not args.dry_run:
            post_report = audit_duplicate_skills(args.library_dir)
            print("\nPost-cleanup verification:")
            if post_report.total_nested_count == 0:
                print("✓ All nested child skill duplicates successfully cleaned up.")
                sys.exit(0)
            else:
                print(f"Remaining nested duplicates: {post_report.total_nested_count}")
                sys.exit(1)

        sys.exit(0)

    # Default audit mode exit code
    sys.exit(0 if report.is_clean else 1)


if __name__ == "__main__":
    main()
