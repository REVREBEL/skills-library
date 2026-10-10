"""
Runtime Git Clone and Sparse-Checkout Synchronization Module.
Synchronizes configured runtime targets with the published 'runtime' branch
using physical Git clones and native sparse-checkouts, preserving dirty workstation
state, capturing external installs, and providing non-destructive migrations.
"""

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from .config import (
    INTAKE_DIR,
    LIBRARY_DIR,
    REPO_ROOT,
    RUNTIME_BRANCH,
    RuntimeTarget,
    load_runtime_targets,
)


def run_git(cmd: List[str], cwd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in cwd and return CompletedProcess."""
    return subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


@dataclass
class TargetSyncReport:
    name: str
    path: str
    status: str  # "created", "up_to_date", "updated", "dirty", "unmanaged", "migrated", "error"
    mode: str = "full"
    commit_sha: Optional[str] = None
    dirty_files: List[str] = field(default_factory=list)
    message: str = ""
    errors: List[str] = field(default_factory=list)


@dataclass
class MultiTargetSyncReport:
    targets: List[TargetSyncReport] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(bool(t.errors or t.status == "error") for t in self.targets)

    @property
    def has_dirty(self) -> bool:
        return any(t.status == "dirty" for t in self.targets)

    def summary(self) -> str:
        lines = ["=== Runtime Targets Synchronization Summary ==="]
        for t in self.targets:
            lines.append(f"Target '{t.name}' ({t.path}) [{t.mode}]: {t.status.upper()}")
            if t.commit_sha:
                lines.append(f"  Commit: {t.commit_sha[:10]}")
            if t.message:
                lines.append(f"  Info: {t.message}")
            if t.dirty_files:
                lines.append(f"  Dirty Files ({len(t.dirty_files)}):")
                for df in t.dirty_files[:5]:
                    lines.append(f"    {df}")
                if len(t.dirty_files) > 5:
                    lines.append(f"    ... and {len(t.dirty_files) - 5} more")
            if t.errors:
                lines.append("  Errors:")
                for err in t.errors:
                    lines.append(f"    - {err}")
        return "\n".join(lines)


def detect_target_state(
    target_path: Path,
    expected_branch: str = RUNTIME_BRANCH,
    expected_remote: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects target directory to assess if absent, git checkout, dirty, or unmanaged."""
    state: Dict[str, Any] = {
        "exists": target_path.exists(),
        "is_dir": target_path.is_dir(),
        "is_git": False,
        "branch": None,
        "is_dirty": False,
        "dirty_files": [],
        "commit_sha": None,
        "sparse_enabled": False,
        "sparse_rules": [],
        "has_legacy_symlinks": False,
        "unmanaged_physical_files": [],
    }

    if not state["exists"]:
        return state

    git_dir = target_path / ".git"
    if git_dir.exists() and (git_dir.is_dir() or git_dir.is_file()):
        state["is_git"] = True
        try:
            branch_proc = run_git(["branch", "--show-current"], cwd=str(target_path), check=False)
            state["branch"] = branch_proc.stdout.strip()

            commit_proc = run_git(["rev-parse", "HEAD"], cwd=str(target_path), check=False)
            if commit_proc.returncode == 0:
                state["commit_sha"] = commit_proc.stdout.strip()

            status_proc = run_git(["status", "--porcelain"], cwd=str(target_path), check=False)
            dirty = [line.strip() for line in status_proc.stdout.splitlines() if line.strip()]
            state["is_dirty"] = bool(dirty)
            state["dirty_files"] = dirty

            sparse_cfg = run_git(["config", "core.sparseCheckout"], cwd=str(target_path), check=False)
            state["sparse_enabled"] = sparse_cfg.stdout.strip().lower() == "true"
            if state["sparse_enabled"]:
                sparse_list = run_git(["sparse-checkout", "list"], cwd=str(target_path), check=False)
                state["sparse_rules"] = [r.strip() for r in sparse_list.stdout.splitlines() if r.strip()]
        except Exception as e:
            state["error"] = str(e)
    else:
        # Non-git directory: check for legacy symlinks and unmanaged physical files
        try:
            for item in target_path.iterdir():
                if item.name in (".DS_Store", ".git"):
                    continue
                if item.is_symlink():
                    state["has_legacy_symlinks"] = True
                else:
                    state["unmanaged_physical_files"].append(item.name)
        except Exception as e:
            state["error"] = str(e)

    return state


def migrate_legacy_symlink_target(
    target_path: Path,
    library_dir: str = LIBRARY_DIR,
) -> Dict[str, Any]:
    """
    Non-destructively removes managed legacy symlinks from a target directory,
    ensuring unmanaged physical files are preserved.
    """
    removed_symlinks = 0
    preserved_unmanaged = []

    if not target_path.exists():
        return {"migrated": False, "reason": "does_not_exist"}

    for item in list(target_path.iterdir()):
        if item.name in (".DS_Store",):
            try:
                item.unlink()
            except Exception:
                pass
            continue
        if item.is_symlink():
            try:
                item.unlink()
                removed_symlinks += 1
            except Exception:
                pass
        else:
            preserved_unmanaged.append(str(item))

    return {
        "migrated": True,
        "removed_symlinks": removed_symlinks,
        "preserved_unmanaged": preserved_unmanaged,
    }


def sync_target(
    target: RuntimeTarget,
    source_repo: Optional[str] = None,
    runtime_branch: str = RUNTIME_BRANCH,
    allow_intake_capture: bool = True,
    remote_url: Optional[str] = None,
    dry_run: bool = False,
) -> TargetSyncReport:
    """
    Reconciles an individual runtime target to the published runtime branch.
    Never overwrites a dirty target. Applies sparse-checkout rules for subset mode.
    Clones/fetches from configured canonical remote URL unless an explicit test source is provided.
    """
    dest = target.resolved_path
    effective_remote = remote_url or source_repo or target.remote_url or "https://github.com/REVREBEL/skills-library.git"
    report = TargetSyncReport(name=target.name, path=str(dest), status="up_to_date", mode=target.mode)

    if dry_run:
        state = detect_target_state(dest, expected_branch=runtime_branch)
        if not state["exists"] or (dest.is_dir() and not list(dest.iterdir())):
            report.status = "created"
            report.message = f"[DRY RUN] Would clone {runtime_branch} branch from {effective_remote} ({target.mode} mode)."
            return report
        if state["exists"] and not state["is_git"]:
            if state["has_legacy_symlinks"] and not state["unmanaged_physical_files"]:
                report.status = "migrated"
                report.message = f"[DRY RUN] Would remove legacy symlinks and clone {runtime_branch} from {effective_remote}."
                return report
            elif state["unmanaged_physical_files"]:
                report.status = "unmanaged"
                report.message = "[DRY RUN] Directory contains unmanaged non-symlink items. Would refuse initialization."
                return report
        if state["is_git"]:
            if state["is_dirty"]:
                report.status = "dirty"
                report.message = "[DRY RUN] Target is dirty. Would capture changes or refuse destructive overwrite."
                return report
            report.status = "up_to_date"
            report.commit_sha = state["commit_sha"]
            report.message = f"[DRY RUN] Target is Git clone of {runtime_branch} at {state['commit_sha'][:8] if state['commit_sha'] else 'unknown'}."
            return report
        report.status = "dry_run"
        report.message = f"[DRY RUN] Simulated check for {target.name}."
        return report

    try:
        state = detect_target_state(dest, expected_branch=runtime_branch)

        # Step 1: Check for legacy symlink migration if not a git repo
        if state["exists"] and not state["is_git"]:
            if state["has_legacy_symlinks"] and not state["unmanaged_physical_files"]:
                # Pure legacy symlink farm: clean it up so we can clone cleanly
                migrate_res = migrate_legacy_symlink_target(dest)
                report.message = f"Cleaned {migrate_res['removed_symlinks']} legacy symlinks."
                # Refresh state
                state = detect_target_state(dest, expected_branch=runtime_branch)
            elif state["unmanaged_physical_files"]:
                report.status = "unmanaged"
                report.message = (
                    f"Directory contains {len(state['unmanaged_physical_files'])} unmanaged non-symlink items. "
                    "Refusing destructive initialization."
                )
                report.errors.append("Unmanaged files present in non-git destination.")
                return report

        # Step 2: Handle absent or empty destination -> Git Clone
        if not state["exists"] or (dest.is_dir() and not list(dest.iterdir())):
            dest.parent.mkdir(parents=True, exist_ok=True)
            if target.mode == "subset":
                # Clone with --no-checkout then set sparse-checkout
                run_git(
                    ["clone", "--branch", runtime_branch, "--no-checkout", effective_remote, str(dest)],
                    cwd=str(dest.parent),
                )
                if target.include:
                    run_git(
                        ["sparse-checkout", "set"] + target.include,
                        cwd=str(dest),
                    )
                run_git(["checkout", runtime_branch], cwd=str(dest))
            else:
                # Full clone
                run_git(
                    ["clone", "--branch", runtime_branch, effective_remote, str(dest)],
                    cwd=str(dest.parent),
                )

            commit_proc = run_git(["rev-parse", "HEAD"], cwd=str(dest))
            report.status = "created"
            report.commit_sha = commit_proc.stdout.strip()
            report.message = f"Cloned {runtime_branch} branch ({target.mode} mode)."
            return report

        # Step 3: Destination is an existing Git clone
        if state["is_git"]:
            # Check dirty state first: NEVER overwrite dirty target
            if state["is_dirty"]:
                report.status = "dirty"
                report.commit_sha = state["commit_sha"]
                report.dirty_files = state["dirty_files"]
                report.message = (
                    f"Target has {len(state['dirty_files'])} uncommitted changes. "
                    "Refusing destructive update; capture incoming changes first."
                )
                return report

            # Align remote origin URL with effective_remote
            cur_rem = run_git(["config", "--get", "remote.origin.url"], cwd=str(dest), check=False)
            if cur_rem.returncode != 0:
                run_git(["remote", "add", "origin", effective_remote], cwd=str(dest), check=False)
            elif cur_rem.stdout.strip() != effective_remote:
                run_git(["remote", "set-url", "origin", effective_remote], cwd=str(dest), check=False)

            # Check branch
            if state["branch"] != runtime_branch:
                # Attempt to checkout runtime branch
                run_git(["checkout", runtime_branch], cwd=str(dest))

            # Reconcile sparse-checkout rules
            if target.mode == "subset":
                run_git(["sparse-checkout", "set"] + (target.include or []), cwd=str(dest))
            else:
                if state["sparse_enabled"]:
                    run_git(["sparse-checkout", "disable"], cwd=str(dest))

            # Fetch and fast-forward
            old_sha = state["commit_sha"]
            fetch_res = run_git(["fetch", "origin", runtime_branch], cwd=str(dest), check=False)
            if fetch_res.returncode == 0:
                ff_res = run_git(["merge", "--ff-only", "FETCH_HEAD"], cwd=str(dest), check=False)
                if ff_res.returncode != 0:
                    report.status = "error"
                    report.errors.append(f"Fast-forward merge failed on {target.name}: {ff_res.stderr.strip() or ff_res.stdout.strip()}")
                    return report
                new_sha = run_git(["rev-parse", "HEAD"], cwd=str(dest)).stdout.strip()
                report.commit_sha = new_sha
                if old_sha != new_sha:
                    report.status = "updated"
                    report.message = f"Fast-forwarded from {old_sha[:8] if old_sha else 'unknown'} to {new_sha[:8]}."
                else:
                    report.status = "up_to_date"
                    report.message = "Already up to date."
            else:
                report.status = "error"
                report.errors.append(f"Failed to fetch {runtime_branch} from origin ({effective_remote}): {fetch_res.stderr.strip()}")

            return report

        report.status = "error"
        report.errors.append("Target directory is neither an empty directory nor a valid git checkout.")
        return report

    except Exception as e:
        report.status = "error"
        report.errors.append(str(e))
        return report


def sync_all_targets(
    config_path: Optional[str] = None,
    source_repo: Optional[str] = None,
    remote_url: Optional[str] = None,
    dry_run: bool = False,
) -> MultiTargetSyncReport:
    """Loads all runtime targets from configuration and synchronizes all enabled targets."""
    targets = load_runtime_targets(config_path)
    report = MultiTargetSyncReport()

    for target in targets:
        if not target.enabled:
            continue
        target_report = sync_target(
            target=target,
            source_repo=source_repo,
            remote_url=remote_url,
            dry_run=dry_run,
        )
        report.targets.append(target_report)

    return report
