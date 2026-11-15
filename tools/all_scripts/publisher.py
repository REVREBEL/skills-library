"""
Runtime Branch Publisher.
Generates and maintains the standalone 'runtime' publication branch whose root
mirrors main:library/ exactly, containing only deployable physical skill packages.
"""

import os
import subprocess
from typing import Optional, Dict, Any

from skill_library.config import REPO_ROOT, RUNTIME_BRANCH


def run_git(cmd: list, cwd: str = REPO_ROOT, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in cwd and return CompletedProcess."""
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Antigravity Agent")
    env.setdefault("GIT_AUTHOR_EMAIL", "agent@antigravity.local")
    env.setdefault("GIT_COMMITTER_NAME", "Antigravity Agent")
    env.setdefault("GIT_COMMITTER_EMAIL", "agent@antigravity.local")
    return subprocess.run(
        ["git"] + cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=check,
    )


def get_library_tree_sha(repo_path: str = REPO_ROOT, ref: str = "HEAD", library_rel: str = "library") -> str:
    """Return the git tree SHA for the library directory at ref."""
    target_spec = f"{ref}:{library_rel}".replace("\\", "/")
    proc = run_git(["rev-parse", target_spec], cwd=repo_path)
    return proc.stdout.strip()


def get_commit_tree_sha(repo_path: str, commit_or_ref: str) -> Optional[str]:
    """Return the root tree SHA for a given commit or ref."""
    try:
        proc = run_git(["rev-parse", f"{commit_or_ref}^{{tree}}"], cwd=repo_path)
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_ref_commit_sha(repo_path: str, ref_name: str) -> Optional[str]:
    """Return the commit SHA for a ref name if it exists, else None."""
    try:
        proc = run_git(["rev-parse", "--verify", ref_name], cwd=repo_path)
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def _push_runtime(repo_path: str, remote: str, branch_name: str) -> None:
    res = run_git(["push", remote, f"{branch_name}:{branch_name}"], cwd=repo_path, check=False)
    if res.returncode != 0:
        raise RuntimeError(
            f"Failed to push runtime branch '{branch_name}' to remote '{remote}' (returncode {res.returncode}):\n"
            f"{res.stderr.strip() or res.stdout.strip()}"
        )


def publish_runtime_branch(
    repo_path: str = REPO_ROOT,
    branch_name: str = RUNTIME_BRANCH,
    library_rel: str = "library",
    push: bool = False,
    remote: str = "origin",
) -> Dict[str, Any]:
    """
    Publish or regenerate the runtime publication branch so its root tree matches library_rel.
    Deterministic, failure-safe, and independent of working-tree index.
    """
    library_tree = get_library_tree_sha(repo_path, ref="HEAD", library_rel=library_rel)
    head_sha = run_git(["rev-parse", "HEAD"], cwd=repo_path).stdout.strip()[:10]

    local_ref = f"refs/heads/{branch_name}"
    current_commit = get_ref_commit_sha(repo_path, local_ref)
    
    # If not local, check remote ref
    if not current_commit:
        remote_ref = f"refs/remotes/{remote}/{branch_name}"
        current_commit = get_ref_commit_sha(repo_path, remote_ref)

    if current_commit:
        current_tree = get_commit_tree_sha(repo_path, current_commit)
        if current_tree == library_tree:
            # Tree matches exactly; ensure local ref is set to this commit
            run_git(["update-ref", local_ref, current_commit], cwd=repo_path)
            if push:
                _push_runtime(repo_path, remote, branch_name)
            return {
                "status": "unchanged",
                "branch": branch_name,
                "tree_sha": library_tree,
                "commit_sha": current_commit,
            }
        
        # Tree has changed; create commit with previous commit as parent
        msg = f"Generated runtime publication from {library_rel}/ at {head_sha}"
        commit_cmd = ["commit-tree", library_tree, "-p", current_commit, "-m", msg]
        new_commit = run_git(commit_cmd, cwd=repo_path).stdout.strip()
        run_git(["update-ref", local_ref, new_commit], cwd=repo_path)
        
        if push:
            _push_runtime(repo_path, remote, branch_name)
            
        return {
            "status": "updated",
            "branch": branch_name,
            "tree_sha": library_tree,
            "commit_sha": new_commit,
            "parent_sha": current_commit,
        }
    else:
        # First publication: create root commit
        msg = f"Initial runtime publication from {library_rel}/ at {head_sha}"
        commit_cmd = ["commit-tree", library_tree, "-m", msg]
        new_commit = run_git(commit_cmd, cwd=repo_path).stdout.strip()
        run_git(["update-ref", local_ref, new_commit], cwd=repo_path)

        if push:
            _push_runtime(repo_path, remote, branch_name)

        return {
            "status": "created",
            "branch": branch_name,
            "tree_sha": library_tree,
            "commit_sha": new_commit,
        }
