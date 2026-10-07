"""
Runtime Symlink Reconciliation Module.
Synchronizes .agents/skills/ with the canonical library and runtime manifest,
creates portable relative symlinks, repairs broken links, discovers external physical installs,
and guarantees idempotency and safety.
"""

import json
import os
import shutil
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .config import (
    INTAKE_DIR,
    LIBRARY_DIR,
    PROTECTED_RUNTIME_ENTRIES,
    REPO_ROOT,
    RUNTIME_DIR,
)
from .manifest import RuntimeManifest
from .scanner import inspect_external_installer_environment


@dataclass
class SyncReport:
    created: List[str] = field(default_factory=list)
    verified: List[str] = field(default_factory=list)
    repaired: List[str] = field(default_factory=list)
    staged_to_intake: List[str] = field(default_factory=list)
    external_links: List[str] = field(default_factory=list)
    collisions: List[str] = field(default_factory=list)
    protected_skipped: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.created or self.repaired or self.staged_to_intake)

    def summary(self) -> str:
        lines = [
            "=== Runtime Symlink Synchronization Summary ===",
            f"Verified Unchanged: {len(self.verified)}",
            f"Created Symlinks: {len(self.created)}",
            f"Repaired Symlinks: {len(self.repaired)}",
            f"Staged to Intake: {len(self.staged_to_intake)}",
            f"Protected System Skills Preserved: {len(self.protected_skipped)}",
            f"External Unknown Symlinks: {len(self.external_links)}",
            f"Collisions / Blockers: {len(self.collisions)}",
        ]
        if self.errors:
            lines.append("Errors:")
            for e in self.errors:
                lines.append(f"  - {e}")
        return "\n".join(lines)


def reconcile_runtime_symlinks(
    runtime_dir: str = RUNTIME_DIR,
    library_dir: str = LIBRARY_DIR,
    intake_dir: str = INTAKE_DIR,
    manifest: Optional[RuntimeManifest] = None,
    dry_run: bool = False,
    stage_external: bool = True,
) -> SyncReport:
    """
    Reconciles .agents/skills/ symlinks against the runtime manifest.
    Ensures every canonical managed skill has a valid relative symlink.
    """
    report = SyncReport()
    m = manifest or RuntimeManifest()
    os.makedirs(runtime_dir, exist_ok=True)
    os.makedirs(intake_dir, exist_ok=True)

    norm_lib = os.path.normpath(library_dir)

    # Step 1: Scan existing entries in .agents/skills/
    existing_entries = os.listdir(runtime_dir)

    for entry in existing_entries:
        if entry in PROTECTED_RUNTIME_ENTRIES:
            report.protected_skipped.append(entry)
            continue

        entry_path = os.path.join(runtime_dir, entry)

        if os.path.islink(entry_path):
            raw_target = os.readlink(entry_path)
            abs_target = os.path.normpath(os.path.join(runtime_dir, raw_target))
            target_exists = os.path.exists(abs_target)

            if not target_exists:
                # Broken symlink
                if entry in m.skills:
                    # Target is a managed skill whose link is broken or stale -> repair it
                    canonical_rel = m.skills[entry]["canonical_path"]
                    canonical_abs = os.path.normpath(os.path.join(REPO_ROOT, canonical_rel))
                    if os.path.exists(canonical_abs):
                        if not dry_run:
                            os.unlink(entry_path)
                            rel_link = os.path.relpath(canonical_abs, runtime_dir)
                            os.symlink(rel_link, entry_path)
                        report.repaired.append(f"{entry} -> {canonical_rel}")
                    else:
                        report.errors.append(f"Cannot repair {entry}: canonical target {canonical_rel} missing on disk")
                else:
                    report.errors.append(f"Broken unmanaged symlink: {entry} -> {raw_target}")
            elif abs_target.startswith(norm_lib):
                # Valid managed symlink
                if entry in m.skills:
                    report.verified.append(entry)
                else:
                    # Symlink points into library but not in manifest (orphan symlink)
                    report.external_links.append(entry)
            else:
                # Symlink points outside library
                report.external_links.append(entry)

        elif os.path.isdir(entry_path):
            # Physical directory in runtime folder (external install e.g. from skills.sh)
            if entry in m.skills:
                # Collision: a physical directory with the same name as a managed skill
                report.collisions.append(f"Physical directory collides with managed skill: {entry}")
            else:
                if stage_external:
                    # Stage into intake safely
                    dest_intake = os.path.join(intake_dir, entry)
                    if os.path.exists(dest_intake):
                        report.collisions.append(f"Cannot stage {entry}: intake/{entry} already exists")
                    else:
                        integration_info = inspect_external_installer_environment(entry_path)
                        if not dry_run:
                            shutil.copytree(entry_path, dest_intake)
                            # Save installer metadata
                            meta_path = os.path.join(dest_intake, ".installer-metadata.json")
                            with open(meta_path, "w", encoding="utf-8") as mf:
                                json.dump(integration_info, mf, indent=2)
                        report.staged_to_intake.append(entry)
                else:
                    report.errors.append(f"External physical directory found (unstaged): {entry}")

        else:
            # Regular unmanaged file
            report.collisions.append(f"Unmanaged regular file in runtime directory: {entry}")

    # Step 2: Ensure all managed skills in manifest have symlinks in runtime_dir
    for runtime_name, s_info in m.skills.items():
        symlink_path = os.path.join(runtime_dir, runtime_name)
        canonical_rel = s_info["canonical_path"]
        canonical_abs = os.path.normpath(os.path.join(REPO_ROOT, canonical_rel))

        if not os.path.exists(canonical_abs):
            report.errors.append(f"Canonical skill path missing on disk: {canonical_rel}")
            continue

        rel_target = os.path.relpath(canonical_abs, runtime_dir)

        if not os.path.lexists(symlink_path):
            # Missing symlink -> create it
            if not dry_run:
                os.symlink(rel_target, symlink_path)
            report.created.append(runtime_name)
        elif os.path.islink(symlink_path):
            current_target = os.readlink(symlink_path)
            norm_current = os.path.normpath(os.path.join(runtime_dir, current_target))
            if norm_current != canonical_abs:
                # Misdirected symlink -> repair it
                if not dry_run:
                    os.unlink(symlink_path)
                    os.symlink(rel_target, symlink_path)
                report.repaired.append(f"{runtime_name} (redirected to {canonical_rel})")

    return report
