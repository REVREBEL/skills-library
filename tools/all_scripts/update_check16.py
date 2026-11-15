#!/usr/bin/env python3
import os
import re

VERIFY_PATH = "task-folder/agents/skills-rebuild/_audit/verify_phase_08.py"

with open(VERIFY_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Make Check 16 strictly fail on any git status --porcelain output
old_check16 = """        # Verify clean tree via git status --porcelain
        status_proc = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        uncommitted = [line for line in status_proc.stdout.splitlines() if not line.endswith(".py")]
        # Staged or unstaged tracked changes cause Check 16 failure if running at checkpoint verification
        if status_proc.stdout.strip():
            # Check if only python scratch scripts in library-rebuild-tasks/artifacts/ exist
            meaningful_changes = [
                line for line in status_proc.stdout.splitlines()
                if not "library-rebuild-tasks/artifacts/" in line
            ]
            if meaningful_changes:
                errors.append(f"Check 16: Working tree is not clean (git status --porcelain returned {len(meaningful_changes)} uncommitted modifications): {meaningful_changes[:5]}")"""

new_check16 = """        # Verify clean tree via git status --porcelain
        status_proc = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if status_proc.stdout.strip():
            lines = status_proc.stdout.splitlines()
            errors.append(f"Check 16: Working tree is not clean (git status --porcelain returned {len(lines)} uncommitted file(s)): {lines[:5]}")"""

if old_check16 in content:
    content = content.replace(old_check16, new_check16)
else:
    content = re.sub(
        r"# Verify clean tree via git status --porcelain.*?if meaningful_changes:.*?errors\.append\([^\)]+\)",
        new_check16,
        content,
        flags=re.DOTALL
    )

with open(VERIFY_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Check 16 to strictly fail on non-empty git status --porcelain.")
