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


def scan_target_dirty_state(target_path: Path) -> Dict[str, Any]:
    """
    Inspects target Git checkout with git status --porcelain.
    Groups changes by top-level incoming package directory.
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

        # Identify top-level package or root file
        parts = Path(rel_file).parts
        if parts:
            pkg_name = parts[0]
            if pkg_name not in res["packages"]:
                res["packages"][pkg_name] = []
            res["packages"][pkg_name].append(rel_file)

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
) -> Dict[str, Any]:
    """
    Captures uncommitted changes from a dirty runtime target.
    Commits changes to an incoming/<timestamp-id> snapshot branch, pushes to remote,
    dispatches GitHub Action workflow on main, and ONLY resets the local working copy if the push succeeds.
    """
    dest = target.resolved_path
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

    # 1. Create incoming branch in the target checkout
    run_git(["checkout", "-b", branch_name], cwd=str(dest))

    # 2. Write intake snapshot metadata
    meta_path = dest / ".incoming-metadata.json"
    metadata = {
        "snapshot_id": snapshot_id,
        "target_name": target.name,
        "target_path": str(target.path),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "packages": list(dirty_state["packages"].keys()),
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

        return {
            "captured": True,
            "target": target.name,
            "snapshot_id": snapshot_id,
            "branch": branch_name,
            "packages": list(dirty_state["packages"].keys()),
            "pushed": push,
            "reset": True,
            "workflow_triggered": workflow_triggered,
            "workflow_message": workflow_message,
        }
    else:
        # Push failed: RETAIN dirty content! Do NOT reset!
        return {
            "captured": False,
            "target": target.name,
            "snapshot_id": snapshot_id,
            "branch": branch_name,
            "packages": list(dirty_state["packages"].keys()),
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
    for pkg in metadata.get("packages", []):
        if not isinstance(pkg, str) or not pkg.strip():
            continue
        if any(c in pkg for c in ("\0", "/", "\\", "..")) or pkg in (".git", ".DS_Store", "SKILL.md", ".incoming-metadata.json"):
            continue

        dest_pkg_dir = (intake_dir / pkg).resolve()
        try:
            dest_pkg_dir.relative_to(intake_dir)
        except ValueError:
            raise ValueError(f"Path traversal detected: package '{pkg}' escapes intake directory.")

        dest_pkg_dir.mkdir(parents=True, exist_ok=True)

        # Checkout files from incoming branch into intake/<pkg>
        archive_proc = subprocess.Popen(
            ["git", "archive", incoming_commit, pkg],
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

        # Classify as external update if package exists in canonical manifest
        is_existing = bool(manifest and pkg in manifest.skills)
        target_can_path = manifest.skills[pkg].get("canonical_path", "") if is_existing else ""
        classification = "EXTERNAL_UPDATE" if is_existing else "EXTERNAL_PHYSICAL"
        installer_type = "external_update" if is_existing else "external_install"

        # Write provenance info and classification
        pkg_meta_path = dest_pkg_dir / ".installer-metadata.json"
        with open(pkg_meta_path, "w", encoding="utf-8") as pf:
            json.dump({
                "source_snapshot": incoming_branch,
                "type": installer_type,
                "classification": classification,
                "target_canonical_path": target_can_path,
                "captured_at": metadata.get("captured_at"),
                "target_name": metadata.get("target_name"),
                "provenance": metadata.get("provenance", {}),
            }, pf, indent=2)

        packages_staged.append(pkg)

    # Stage intake changes
    run_git(["add", "intake"], cwd=repo_path)
    run_git(["commit", "-m", f"Stage incoming runtime intake from {incoming_branch}"], cwd=repo_path)

    return {
        "intake_branch": intake_branch,
        "incoming_branch": incoming_branch,
        "packages_staged": packages_staged,
    }
