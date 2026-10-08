"""
Living Library and Skill Validation Module.
Independently verifies router integrity, canonical-manifest-publication set reconciliation,
runtime target Git checkout scopes, and per-skill structural health without symlink dependencies.
"""

import ast
import glob
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

from .config import (
    CATEGORIES,
    DEEP_CATEGORIES,
    FLAT_CATEGORIES,
    LIBRARY_DIR,
    OPERATIONAL_SYSTEM_PACKAGES,
    REPO_ROOT,
    RUNTIME_BRANCH,
    SECRET_PATTERNS,
    TARGETS_CONFIG_PATH,
    TRIGGER_CONTRACT_PATTERN,
    WORKSTATION_PATH_PATTERNS,
    RuntimeTarget,
    get_all_routers,
    load_runtime_targets,
)
from .manifest import RuntimeManifest


@dataclass
class SkillValidationReport:
    skill_path: str
    name: str
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    markdown_links_checked: int = 0
    scripts_checked: int = 0
    resources_checked: int = 0


@dataclass
class ValidationResult:
    is_valid: bool = True
    canonical_reconciliation_passed: bool = True
    runtime_publication_passed: bool = True
    target_reconciliation_passed: bool = True
    total_routers: int = 0
    total_router_links: int = 0
    total_canonical_skills: int = 0
    total_manifest_skills: int = 0
    total_targets_checked: int = 0
    broken_router_links: List[str] = field(default_factory=list)
    orphan_skills: List[str] = field(default_factory=list)
    target_errors: List[str] = field(default_factory=list)
    publication_errors: List[str] = field(default_factory=list)
    skill_errors: Dict[str, List[str]] = field(default_factory=dict)
    workstation_path_leaks: List[str] = field(default_factory=list)
    secret_leaks: List[str] = field(default_factory=list)
    reconciliation_discrepancies: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    @property
    def set_reconciliation_passed(self) -> bool:
        return self.canonical_reconciliation_passed

    def summary(self) -> str:
        status = "PASSED" if self.is_valid else "FAILED"
        lines = [
            f"=== Living Library Validation: {status} ===",
            f"Set Reconciliation (Physical == Router == Manifest): {'PASSED' if self.canonical_reconciliation_passed else 'FAILED'}",
            f"Runtime Publication Validation: {'PASSED' if self.runtime_publication_passed else 'FAILED'}",
            f"Target Checkout Validation: {'PASSED' if self.target_reconciliation_passed else 'FAILED'} (Checked: {self.total_targets_checked})",
            f"Total Routers Verified: {self.total_routers}",
            f"Total Router Links Verified: {self.total_router_links} (Broken: {len(self.broken_router_links)})",
            f"Total Canonical Active Skills: {self.total_canonical_skills} (Orphans: {len(self.orphan_skills)})",
            f"Total Manifest Skills: {self.total_manifest_skills}",
            f"Workstation Path Leaks: {len(self.workstation_path_leaks)}",
            f"Potential Secret Leaks: {len(self.secret_leaks)}",
        ]
        if not self.is_valid:
            lines.append("\nErrors / Regressions Found:")
            for r in self.reconciliation_discrepancies[:10]:
                lines.append(f"  - Reconciliation Discrepancy: {r}")
            for p in self.publication_errors[:5]:
                lines.append(f"  - Publication Error: {p}")
            for t in self.target_errors[:5]:
                lines.append(f"  - Target Error: {t}")
            for b in self.broken_router_links[:5]:
                lines.append(f"  - Broken Router Link: {b}")
            for o in self.orphan_skills[:5]:
                lines.append(f"  - Orphan Skill: {o}")
            for p in self.workstation_path_leaks[:5]:
                lines.append(f"  - Path Leak: {p}")
            for s, errs in list(self.skill_errors.items())[:5]:
                lines.append(f"  - Skill {s}: {errs[0]}")
        return "\n".join(lines)


def parse_frontmatter(content: str) -> Optional[dict]:
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end == -1:
        return None
    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip().strip("\"'")
    return result


def validate_single_skill(skill_dir: str) -> SkillValidationReport:
    """Validates an individual skill directory."""
    name = os.path.basename(skill_dir.rstrip(os.sep))
    report = SkillValidationReport(skill_path=skill_dir, name=name)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        report.is_valid = False
        report.errors.append("Missing SKILL.md")
        return report

    try:
        with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        report.is_valid = False
        report.errors.append(f"Unreadable SKILL.md: {e}")
        return report

    # 1. Frontmatter check
    fm = parse_frontmatter(content)
    if not fm:
        report.is_valid = False
        report.errors.append("Invalid or missing YAML frontmatter in SKILL.md")
    else:
        if not fm.get("name"):
            report.is_valid = False
            report.errors.append("Frontmatter missing required 'name'")
        desc = fm.get("description", "")
        if not desc:
            report.is_valid = False
            report.errors.append("Frontmatter missing required 'description'")
        elif not TRIGGER_CONTRACT_PATTERN.search(desc):
            report.warnings.append("Description lacks strong trigger contract clause")

    # 2. Markdown link verification
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for match in link_pattern.finditer(content):
        target = match.group(2).split("#")[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        report.markdown_links_checked += 1
        abs_target = os.path.normpath(os.path.join(skill_dir, target))
        if not os.path.exists(abs_target):
            report.is_valid = False
            report.errors.append(f"Broken markdown relative link: {target}")

    # 3. Scripts syntax checks
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        for root, _, files in os.walk(scripts_dir):
            for file in files:
                report.scripts_checked += 1
                fpath = os.path.join(root, file)
                if file.endswith(".py"):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="replace") as pf:
                            ast.parse(pf.read(), filename=fpath)
                    except SyntaxError as se:
                        report.is_valid = False
                        report.errors.append(f"Python script syntax error in {file}: {se.msg} (line {se.lineno})")
                elif file.endswith(".sh"):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="replace") as sf:
                            scontent = sf.read()
                        if not scontent.startswith("#!"):
                            report.warnings.append(f"Shell script {file} lacks shebang line")
                    except Exception:
                        pass

    # 4. Resources check
    for sub in ("references", "assets", "templates"):
        sdir = os.path.join(skill_dir, sub)
        if os.path.isdir(sdir):
            for _, _, files in os.walk(sdir):
                report.resources_checked += len(files)

    # 5. Workstation Path and Secret Leaks
    for pattern in WORKSTATION_PATH_PATTERNS:
        match = pattern.search(content)
        if match:
            report.is_valid = False
            report.errors.append(f"Workstation path leak: {match.group(1)}")
            break

    for pattern in SECRET_PATTERNS:
        match = pattern.search(content)
        if match:
            report.is_valid = False
            report.errors.append("Potential secret leak found matching pattern")
            break

    return report


def validate_library_integrity(
    library_dir: str = LIBRARY_DIR,
    manifest: Optional[RuntimeManifest] = None,
    config_path: Optional[str] = None,
    verify_publication: bool = True,
    verify_targets: bool = True,
) -> ValidationResult:
    """
    Validates canonical library, routers, manifest, runtime publication branch,
    and configured target checkouts without symlink dependencies.
    """
    result = ValidationResult()
    m = manifest or RuntimeManifest()
    repo_root = os.path.dirname(os.path.normpath(library_dir))

    # Step 1: Discover all 26 routers dynamically
    all_routers = get_all_routers(library_dir=library_dir)
    result.total_routers = len(all_routers)
    norm_routers = {os.path.normpath(r) for r in all_routers}

    for r in all_routers:
        if not os.path.exists(r):
            result.is_valid = False
            result.broken_router_links.append(f"Router file missing: {r}")

    # Step 2: Extract router-indexed leaf skills
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    router_indexed_set: Set[str] = set()

    for r_path in all_routers:
        r_dir = os.path.dirname(r_path)
        try:
            with open(r_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            result.is_valid = False
            result.broken_router_links.append(f"Cannot read router {r_path}: {e}")
            continue

        for m_match in link_pattern.finditer(content):
            target = m_match.group(2).split("#")[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            result.total_router_links += 1
            abs_target = os.path.normpath(os.path.join(r_dir, target))
            if not os.path.exists(abs_target):
                result.is_valid = False
                result.broken_router_links.append(f"{os.path.relpath(r_path, repo_root)} -> {target}")
            elif os.path.basename(abs_target) == "SKILL.md" and abs_target not in norm_routers:
                skill_dir = os.path.dirname(abs_target)
                rel_target_dir = os.path.relpath(skill_dir, repo_root).replace(os.sep, "/")
                router_indexed_set.add(rel_target_dir)

    result.total_canonical_skills = len(router_indexed_set)

    # Step 3: Discover physical canonical packages (all library/<cat>/*/* containing SKILL.md)
    physical_packages_set: Set[str] = set()
    for cat in CATEGORIES:
        glob_pattern = os.path.join(library_dir, cat, "*", "*", "SKILL.md")
        for s_file in glob.glob(glob_pattern):
            s_abs = os.path.normpath(s_file)
            if s_abs not in norm_routers:
                s_dir = os.path.dirname(s_abs)
                rel_s_dir = os.path.relpath(s_dir, repo_root).replace(os.sep, "/")
                physical_packages_set.add(rel_s_dir)

    # Step 4: Extract manifest packages
    manifest_packages_set: Set[str] = {
        s["canonical_path"].replace(os.sep, "/").strip("/")
        for s in m.skills.values()
    }
    result.total_manifest_skills = len(manifest_packages_set)

    # Step 5: Canonical Set Reconciliation (Physical == Router == Manifest)
    discrepancies = []
    if physical_packages_set != router_indexed_set:
        unindexed = physical_packages_set - router_indexed_set
        missing_phys = router_indexed_set - physical_packages_set
        if unindexed:
            discrepancies.append(f"Physical unindexed in routers ({len(unindexed)}): {sorted(list(unindexed))[:3]}")
        if missing_phys:
            discrepancies.append(f"Router targets missing physical package ({len(missing_phys)}): {sorted(list(missing_phys))[:3]}")

    if router_indexed_set != manifest_packages_set:
        unmanifested = router_indexed_set - manifest_packages_set
        unrouted = manifest_packages_set - router_indexed_set
        if unmanifested:
            discrepancies.append(f"Router skills missing in manifest ({len(unmanifested)}): {sorted(list(unmanifested))[:3]}")
        if unrouted:
            discrepancies.append(f"Manifest skills missing in routers ({len(unrouted)}): {sorted(list(unrouted))[:3]}")

    if discrepancies:
        result.is_valid = False
        result.canonical_reconciliation_passed = False
        result.reconciliation_discrepancies.extend(discrepancies)

    # Step 6: Verify Runtime Publication Branch (if repository git context available)
    if verify_publication:
        try:
            tree_proc = subprocess.run(
                ["git", "rev-parse", "HEAD:library"],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
            if tree_proc.returncode == 0:
                expected_tree = tree_proc.stdout.strip()
                runtime_proc = subprocess.run(
                    ["git", "rev-parse", f"{RUNTIME_BRANCH}^{{tree}}"],
                    cwd=repo_root,
                    capture_output=True,
                    text=True,
                )
                if runtime_proc.returncode == 0:
                    runtime_tree = runtime_proc.stdout.strip()
                    if expected_tree != runtime_tree:
                        result.is_valid = False
                        result.runtime_publication_passed = False
                        result.publication_errors.append(
                            f"Runtime branch tree ({runtime_tree[:10]}) does not match HEAD:library ({expected_tree[:10]}). "
                            "Run 'python3 tools/skill-library.py publish-runtime' to update."
                        )
                else:
                    # Runtime branch not yet generated
                    result.publication_errors.append(
                        f"Branch '{RUNTIME_BRANCH}' does not exist locally. "
                        "Run 'python3 tools/skill-library.py publish-runtime' to create it."
                    )
        except Exception as e:
            result.publication_errors.append(f"Git inspection failed: {e}")

    # Step 7: Verify Configured Runtime Targets
    if verify_targets:
        targets = load_runtime_targets(config_path)
        for target in targets:
            if not target.enabled:
                continue
            result.total_targets_checked += 1
            t_path = target.resolved_path
            if not t_path.exists():
                continue

            git_dir = t_path / ".git"
            if not git_dir.exists():
                result.is_valid = False
                result.target_reconciliation_passed = False
                result.target_errors.append(f"Target '{target.name}' ({t_path}) is not a Git checkout.")
                continue

            # Verify branch is runtime
            b_proc = subprocess.run(["git", "branch", "--show-current"], cwd=str(t_path), capture_output=True, text=True)
            current_b = b_proc.stdout.strip()
            if current_b != RUNTIME_BRANCH:
                result.is_valid = False
                result.target_reconciliation_passed = False
                result.target_errors.append(f"Target '{target.name}' is on branch '{current_b}', expected '{RUNTIME_BRANCH}'.")

            # Verify sparse scope if subset
            if target.mode == "subset":
                sp_proc = subprocess.run(["git", "config", "core.sparseCheckout"], cwd=str(t_path), capture_output=True, text=True)
                if sp_proc.stdout.strip().lower() != "true":
                    result.is_valid = False
                    result.target_reconciliation_passed = False
                    result.target_errors.append(f"Target '{target.name}' is mode 'subset' but sparse-checkout is not enabled.")

    # Step 8: Validate individual skill structural health
    for s_rel in sorted(list(router_indexed_set)):
        s_abs = os.path.join(repo_root, s_rel)
        rep = validate_single_skill(s_abs)
        if not rep.is_valid:
            result.is_valid = False
            result.skill_errors[s_rel] = rep.errors
        for err in rep.errors:
            if "Workstation path leak" in err:
                result.workstation_path_leaks.append(f"{s_rel}: {err}")
            elif "secret leak" in err:
                result.secret_leaks.append(f"{s_rel}: {err}")

    return result
