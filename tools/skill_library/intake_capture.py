"""
Runtime Intake Capture Module.
Detects dirty workstation state in configured runtime targets (e.g. from skills.sh),
groups incoming changes, preserves provenance, pushes incoming/* snapshot branches to remote,
and guarantees dirty state is never reset until remote transport succeeds.
"""

import json
import os
import re
import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import (
    CATEGORIES,
    DEEP_CATEGORIES,
    INTAKE_DIR,
    LIBRARY_DIR,
    REPO_ROOT,
    RUNTIME_BRANCH,
    RuntimeTarget,
    load_runtime_targets,
)
from .manifest import RuntimeManifest

INCOMING_REF_PATTERN = re.compile(r"^incoming/[A-Za-z0-9._/-]+$")


def validate_incoming_ref(ref_name: str) -> None:
    """Validate that incoming ref is a well-formed incoming/* ref with no command injection or traversal."""
    if not isinstance(ref_name, str) or not ref_name.startswith("incoming/"):
        raise ValueError(f"Invalid incoming branch ref '{ref_name}': must start with 'incoming/'")
    if not INCOMING_REF_PATTERN.match(ref_name) or ".." in ref_name or ref_name.endswith(("/", ".lock")):
        raise ValueError(f"Invalid incoming branch ref '{ref_name}': contains unsafe or illegal characters")


def run_git(cmd: List[str], cwd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in cwd and return CompletedProcess."""
    return subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def is_router_directory(target_path: Path, rel_dir: Path) -> bool:
    """
    Returns True if rel_dir represents a category or subcategory router directory
    rather than an individual skill package root.
    """
    posix_str = rel_dir.as_posix()
    if posix_str in ("", "."):
        return True
    # Depth 1 category router (e.g. quality-and-security)
    if posix_str in CATEGORIES:
        return True
    # Depth 2 subcategory router in deep categories (e.g. development/backend)
    parts = rel_dir.parts
    if len(parts) == 2 and parts[0] in DEEP_CATEGORIES and parts[1] in DEEP_CATEGORIES[parts[0]]:
        return True
    # Check if SKILL.md in this directory contains router markers
    skill_file = target_path / rel_dir / "SKILL.md"
    if skill_file.is_file():
        try:
            head = skill_file.read_text(encoding="utf-8", errors="replace")[:400]
            if "type: master-router" in head or "type: category-router" in head or "type: subcategory-router" in head:
                return True
        except Exception:
            pass
    return False


def find_skill_package_root(target_path: Path, rel_file: str) -> tuple[str, str]:
    """
    Resolves the nearest actual skill package root for a dirty file path.
    Returns (package_name, runtime_path).
    For example:
      'quality-and-security/debugging/bug-hunter/scripts/test.py'
      -> ('bug-hunter', 'quality-and-security/debugging/bug-hunter')
      'custom-pkg-one/SKILL.md'
      -> ('custom-pkg-one', 'custom-pkg-one')
    """
    file_path = Path(rel_file)
    curr = file_path.parent

    # 1. Walk upward looking for nearest non-router ancestor containing SKILL.md
    while curr.as_posix() not in ("", "."):
        candidate_skill_md = target_path / curr / "SKILL.md"
        if candidate_skill_md.is_file() and not is_router_directory(target_path, curr):
            return (curr.name, curr.as_posix())
        # Check git HEAD if file was deleted in working tree
        if (target_path / ".git").exists():
            check_head = run_git(["cat-file", "-e", f"HEAD:{curr.as_posix()}/SKILL.md"], cwd=str(target_path), check=False)
            if check_head.returncode == 0 and not is_router_directory(target_path, curr):
                return (curr.name, curr.as_posix())
        curr = curr.parent

    # 2. Taxonomy fallback if no SKILL.md found on disk (e.g. newly untracked files or deleted packages)
    parts = file_path.parts
    if not parts:
        return ("root", ".")

    if parts[0] not in CATEGORIES:
        # Standalone / external package at target root (e.g. "community-new-tool")
        return (parts[0], parts[0])

    # In canonical taxonomy, skill leaves reside at category/subcategory/skill-name
    if len(parts) >= 3:
        return (parts[2], "/".join(parts[:3]))

    # Fallback for changes directly at category or subcategory level
    runtime_path = "/".join(parts[:-1]) if len(parts) > 1 else parts[0]
    return (parts[-1], runtime_path)


def scan_target_dirty_state(target_path: Path) -> Dict[str, Any]:
    """
    Inspects target Git checkout with git status --porcelain.
    Groups changes by nearest skill package root.
    """
    res: Dict[str, Any] = {
        "is_dirty": False,
        "raw_entries": [],
        "packages": {},
        "untracked": [],
        "modified": [],
        "deleted": [],
        "renamed": [],
    }

    if not target_path.exists() or not (target_path / ".git").exists():
        return res

    proc = run_git(["status", "--porcelain"], cwd=str(target_path), check=False)
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if not lines:
        return res

    res["is_dirty"] = True

    for line in lines:
        status = line[:2]
        rel_file = line[3:].strip()
        res["raw_entries"].append((status, rel_file))

        if "??" in status:
            res["untracked"].append(rel_file)
        elif "M" in status:
            res["modified"].append(rel_file)
        elif "D" in status:
            res["deleted"].append(rel_file)
        elif "R" in status:
            res["renamed"].append(rel_file)

        # Resolve nearest skill package root
        pkg_name, runtime_path = find_skill_package_root(target_path, rel_file)
        if runtime_path not in res["packages"]:
            res["packages"][runtime_path] = {
                "package_name": pkg_name,
                "runtime_path": runtime_path,
                "files": [],
            }
        res["packages"][runtime_path]["files"].append(rel_file)

        # Support lookup by leaf package name as well
        if pkg_name != runtime_path and pkg_name not in res["packages"]:
            res["packages"][pkg_name] = res["packages"][runtime_path]

    return res


def get_external_provenance(target_path: Path) -> Dict[str, Any]:
    """
    Searches for external installer provenance metadata in ~/.agents/.skill-lock.json
    or inside the target directory.
    """
    provenance: Dict[str, Any] = {}
    candidate_paths = [
        target_path / ".skill-lock.json",
        target_path / "skills-lock.json",
        Path.home() / ".agents" / ".skill-lock.json",
        Path.home() / ".agents" / "skills-lock.json",
    ]

    for p in candidate_paths:
        if p.exists() and p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        provenance[str(p)] = data
            except Exception:
                pass

    return provenance


def capture_dirty_target(
    target: RuntimeTarget,
    remote: str = "origin",
    push: bool = True,
    base_repo_path: str = REPO_ROOT,
    trigger_workflow: bool = True,
    force: bool = False,
) -> Dict[str, Any]:
    """
    Captures uncommitted changes from a dirty runtime target.
    Commits changes to an incoming/<timestamp-id> snapshot branch, pushes to remote,
    dispatches GitHub Action workflow on main, and ONLY resets the local working copy if the push succeeds.
    """
    dest = target.resolved_path

    if not target.accept_external_intake and not force:
        return {
            "captured": False,
            "target": target.name,
            "reason": "Target does not accept external intake (accept_external_intake is False)",
        }

    dirty_state = scan_target_dirty_state(dest)

    if not dirty_state["is_dirty"]:
        return {
            "captured": False,
            "target": target.name,
            "reason": "Target checkout is clean",
        }

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    snapshot_id = f"{timestamp}-{rand_suffix}"
    branch_name = f"incoming/{snapshot_id}"

    provenance = get_external_provenance(dest)

    # Dedup packages by unique runtime_path
    unique_packages = {}
    for pkg_info in dirty_state["packages"].values():
        unique_packages[pkg_info["runtime_path"]] = pkg_info

    # 1. Create incoming branch in the target checkout
    run_git(["checkout", "-b", branch_name], cwd=str(dest))

    # 2. Write intake snapshot metadata
    meta_path = dest / ".incoming-metadata.json"
    metadata = {
        "snapshot_id": snapshot_id,
        "target_name": target.name,
        "target_path": str(target.path),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "packages": [
            {
                "package_name": info["package_name"],
                "runtime_path": info["runtime_path"],
            }
            for info in unique_packages.values()
        ],
        "dirty_summary": {
            "untracked": dirty_state["untracked"],
            "modified": dirty_state["modified"],
            "deleted": dirty_state["deleted"],
            "renamed": dirty_state["renamed"],
        },
        "provenance": provenance,
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # 3. Stage and commit incoming files
    run_git(["add", "-A"], cwd=str(dest))
    commit_msg = f"Capture incoming runtime changes from {target.name} [{snapshot_id}]"
    run_git(["commit", "-m", commit_msg], cwd=str(dest))

    # 4. Push to remote
    push_success = False
    push_error = ""

    if push:
        push_proc = run_git(["push", remote, f"{branch_name}:{branch_name}"], cwd=str(dest), check=False)
        if push_proc.returncode == 0:
            push_success = True
        else:
            push_error = push_proc.stderr or push_proc.stdout
    else:
        # In dry/offline mode without push requirement, consider committed
        push_success = True

    # 5. Confirm push succeeded BEFORE resetting local checkout
    if push_success:
        workflow_triggered = False
        workflow_message = ""
        if push and trigger_workflow:
            try:
                wf_proc = subprocess.run(
                    ["gh", "workflow", "run", "runtime-intake.yml", "--ref", "main", "-f", f"incoming_branch={branch_name}"],
                    cwd=base_repo_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if wf_proc.returncode == 0:
                    workflow_triggered = True
                    workflow_message = "GitHub Action runtime-intake.yml successfully dispatched on main."
                else:
                    workflow_message = wf_proc.stderr.strip() or wf_proc.stdout.strip()
            except Exception as e:
                workflow_message = str(e)

        # Switch back to runtime branch
        run_git(["checkout", RUNTIME_BRANCH], cwd=str(dest))
        # Reset cleanly to remote runtime baseline
        run_git(["reset", "--hard", f"{remote}/{RUNTIME_BRANCH}"], cwd=str(dest), check=False)
        run_git(["clean", "-fd"], cwd=str(dest), check=False)

        res = {
            "captured": True,
            "target": target.name,
            "snapshot_id": snapshot_id,
            "branch": branch_name,
            "packages": [info["package_name"] for info in unique_packages.values()],
            "package_details": list(unique_packages.values()),
            "pushed": push,
            "reset": True,
            "workflow_triggered": workflow_triggered,
            "workflow_message": workflow_message,
        }
        if push and trigger_workflow and not workflow_triggered:
            res["workflow_error"] = workflow_message or "GitHub Action workflow dispatch failed."
        return res
    else:
        # Push failed: RETAIN dirty content! Do NOT reset!
        return {
            "captured": False,
            "target": target.name,
            "snapshot_id": snapshot_id,
            "branch": branch_name,
            "packages": [info["package_name"] for info in unique_packages.values()],
            "package_details": list(unique_packages.values()),
            "pushed": False,
            "reset": False,
            "error": f"Failed to push snapshot branch to {remote}: {push_error}",
            "retained": True,
        }


def convert_incoming_to_intake(
    repo_path: str,
    incoming_branch: str,
    base_branch: str = "main",
    remote: str = "origin",
) -> Dict[str, Any]:
    """
    Converts an incoming snapshot branch into a reviewed intake branch based on main.
    Copies incoming skill packages into intake/ and creates a commit ready for PR.
    """
    validate_incoming_ref(incoming_branch)
    clean_id = incoming_branch.replace("incoming/", "")
    intake_branch = f"intake/{clean_id}"

    # Fetch explicit refspec to ensure remote ref is populated
    refspec = f"refs/heads/{incoming_branch}:refs/remotes/{remote}/{incoming_branch}"
    run_git(["fetch", remote, refspec], cwd=repo_path, check=False)
    run_git(["fetch", remote, base_branch], cwd=repo_path, check=False)

    # Resolve immutable commit SHA for incoming branch
    sha_proc = run_git(["rev-parse", f"refs/remotes/{remote}/{incoming_branch}"], cwd=repo_path, check=False)
    if sha_proc.returncode != 0 or not sha_proc.stdout.strip():
        sha_proc = run_git(["rev-parse", incoming_branch], cwd=repo_path, check=False)
    if sha_proc.returncode != 0 or not sha_proc.stdout.strip():
        sha_proc = run_git(["rev-parse", "FETCH_HEAD"], cwd=repo_path, check=False)
    if sha_proc.returncode != 0 or not sha_proc.stdout.strip():
        raise ValueError(f"Could not resolve incoming branch ref '{incoming_branch}' to an immutable commit SHA.")
    incoming_commit = sha_proc.stdout.strip()

    # Resolve base branch ref
    base_sha_proc = run_git(["rev-parse", f"refs/remotes/{remote}/{base_branch}"], cwd=repo_path, check=False)
    if base_sha_proc.returncode != 0 or not base_sha_proc.stdout.strip():
        base_sha_proc = run_git(["rev-parse", base_branch], cwd=repo_path, check=False)
    base_ref = base_sha_proc.stdout.strip() if base_sha_proc.returncode == 0 and base_sha_proc.stdout.strip() else base_branch

    # Checkout new intake branch starting from base_ref
    run_git(["checkout", "-B", intake_branch, base_ref], cwd=repo_path, check=True)

    # Extract metadata using immutable incoming commit SHA
    meta_proc = run_git(["show", f"{incoming_commit}:.incoming-metadata.json"], cwd=repo_path, check=False)
    metadata = {}
    if meta_proc.returncode == 0:
        try:
            metadata = json.loads(meta_proc.stdout)
        except Exception:
            pass

    # Load canonical manifest to determine whether incoming skills are external updates or new
    try:
        manifest_file = os.path.join(repo_path, "audit", "runtime-manifest.json")
        manifest = RuntimeManifest(manifest_path=manifest_file)
    except Exception:
        manifest = None

    packages_staged = []
    intake_dir = (Path(repo_path) / "intake").resolve()
    intake_dir.mkdir(parents=True, exist_ok=True)

    # Check out incoming tree into intake directory with containment validation
    for item in metadata.get("packages", []):
        if isinstance(item, dict):
            pkg = item.get("package_name", "").strip()
            runtime_path = item.get("runtime_path", pkg).strip()
        elif isinstance(item, str):
            pkg = item.strip()
            runtime_path = item.strip()
        else:
            continue

        if not pkg or not runtime_path:
            continue
        if any(c in pkg for c in ("\0", "/", "\\", "..")) or pkg in (".git", ".DS_Store", "SKILL.md", ".incoming-metadata.json"):
            continue
        if any(c in runtime_path for c in ("\0", "\\", "..")):
            continue

        # Resolve runtime_name and canonical target from manifest
        canonical_path_candidate = f"library/{runtime_path}"
        manifest_entry = None
        if manifest:
            manifest_entry = manifest.find_by_canonical_path(canonical_path_candidate)
            if not manifest_entry and pkg in manifest.skills:
                manifest_entry = manifest.skills[pkg]

        if manifest_entry:
            runtime_name = manifest_entry.get("runtime_name", pkg)
            target_can_path = manifest_entry.get("canonical_path", canonical_path_candidate)
            classification = "EXTERNAL_UPDATE"
            installer_type = "external_update"
        else:
            # Check if runtime_path is within library category taxonomy
            if any(runtime_path.startswith(f"{c}/") for c in CATEGORIES):
                target_can_path = canonical_path_candidate
                classification = "EXTERNAL_UPDATE"
                installer_type = "external_update"
                # Check for collision with already staged packages
                parts = Path(runtime_path).parts
                if len(parts) > 1 and (pkg in packages_staged or (intake_dir / pkg).exists()):
                    runtime_name = f"{parts[0]}-{pkg}"
                else:
                    runtime_name = pkg
            else:
                target_can_path = ""
                classification = "EXTERNAL_PHYSICAL"
                installer_type = "external_install"
                runtime_name = pkg

        # Disambiguate runtime_name if still colliding with already staged candidates
        if runtime_name in packages_staged or (intake_dir / runtime_name).exists():
            parts = Path(runtime_path).parts
            if len(parts) > 2:
                candidate = f"{parts[0]}-{parts[1]}-{pkg}"
                if candidate not in packages_staged and not (intake_dir / candidate).exists():
                    runtime_name = candidate
            elif len(parts) > 1:
                candidate = f"{parts[0]}-{pkg}"
                if candidate not in packages_staged and not (intake_dir / candidate).exists():
                    runtime_name = candidate

        if any(c in runtime_name for c in ("\0", "/", "\\", "..")) or runtime_name in (".git", ".DS_Store", "SKILL.md", ".incoming-metadata.json"):
            continue

        dest_pkg_dir = (intake_dir / runtime_name).resolve()
        try:
            dest_pkg_dir.relative_to(intake_dir)
        except ValueError:
            raise ValueError(f"Path traversal detected: package '{runtime_name}' escapes intake directory.")

        dest_pkg_dir.mkdir(parents=True, exist_ok=True)

        # Checkout files from incoming branch into intake/<runtime_name> using git archive scoped to runtime_path
        archive_target = f"{incoming_commit}:{runtime_path}" if runtime_path not in ("", ".") else incoming_commit
        tree_check = run_git(["rev-parse", "--verify", archive_target], cwd=repo_path, check=False)
        if tree_check.returncode != 0:
            continue

        archive_proc = subprocess.Popen(
            ["git", "archive", f"--prefix={runtime_name}/", archive_target],
            cwd=repo_path,
            stdout=subprocess.PIPE,
        )
        tar_proc = subprocess.Popen(
            ["tar", "-x", "-C", str(intake_dir)],
            stdin=archive_proc.stdout,
            cwd=repo_path,
        )
        archive_proc.stdout.close()
        tar_proc.communicate()
        archive_proc.wait()

        # Write provenance info, canonical path, and classification
        pkg_meta_path = dest_pkg_dir / ".installer-metadata.json"
        with open(pkg_meta_path, "w", encoding="utf-8") as pf:
            json.dump({
                "source_snapshot": incoming_branch,
                "type": installer_type,
                "classification": classification,
                "package_name": pkg,
                "runtime_name": runtime_name,
                "runtime_path": runtime_path,
                "target_canonical_path": target_can_path,
                "captured_at": metadata.get("captured_at"),
                "target_name": metadata.get("target_name"),
                "provenance": metadata.get("provenance", {}),
            }, pf, indent=2)

        packages_staged.append(runtime_name)

    # Stage intake changes
    run_git(["add", "intake"], cwd=repo_path)
    run_git(["commit", "-m", f"Stage incoming runtime intake from {incoming_branch}"], cwd=repo_path)

    return {
        "intake_branch": intake_branch,
        "incoming_branch": incoming_branch,
        "packages_staged": packages_staged,
    }
