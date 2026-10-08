"""
Living Library and Skill Validation Module.
Independently verifies router integrity, four-way set equality (physical == router == manifest == runtime),
and per-skill structural health without hardcoded population counts.
"""

import ast
import glob
import os
import re
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .config import (
    CATEGORIES,
    DEEP_CATEGORIES,
    FLAT_CATEGORIES,
    LIBRARY_DIR,
    OPERATIONAL_SYSTEM_PACKAGES,
    PROTECTED_RUNTIME_ENTRIES,
    REPO_ROOT,
    RUNTIME_DIR,
    SECRET_PATTERNS,
    TRIGGER_CONTRACT_PATTERN,
    WORKSTATION_PATH_PATTERNS,
    get_all_routers,
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
    set_reconciliation_passed: bool = True
    total_routers: int = 0
    total_router_links: int = 0
    total_canonical_skills: int = 0
    total_manifest_skills: int = 0
    total_managed_symlinks: int = 0
    broken_router_links: List[str] = field(default_factory=list)
    orphan_skills: List[str] = field(default_factory=list)
    broken_managed_symlinks: List[str] = field(default_factory=list)
    skill_errors: Dict[str, List[str]] = field(default_factory=dict)
    workstation_path_leaks: List[str] = field(default_factory=list)
    secret_leaks: List[str] = field(default_factory=list)
    reconciliation_discrepancies: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "PASSED" if self.is_valid else "FAILED"
        lines = [
            f"=== Living Library Validation: {status} ===",
            f"4-Way Set Reconciliation (Physical == Router == Manifest == Runtime): {'PASSED' if self.set_reconciliation_passed else 'FAILED'}",
            f"Total Routers Verified: {self.total_routers}",
            f"Total Router Links Verified: {self.total_router_links} (Broken: {len(self.broken_router_links)})",
            f"Total Canonical Active Skills: {self.total_canonical_skills} (Orphans: {len(self.orphan_skills)})",
            f"Total Manifest Skills: {self.total_manifest_skills}",
            f"Total Managed Symlinks: {self.total_managed_symlinks} (Broken: {len(self.broken_managed_symlinks)})",
            f"Workstation Path Leaks: {len(self.workstation_path_leaks)}",
            f"Potential Secret Leaks: {len(self.secret_leaks)}",
        ]
        if not self.is_valid:
            lines.append("\nErrors / Regressions Found:")
            for r in self.reconciliation_discrepancies[:10]:
                lines.append(f"  - Reconciliation Discrepancy: {r}")
            for b in self.broken_router_links[:5]:
                lines.append(f"  - Broken Router Link: {b}")
            for o in self.orphan_skills[:5]:
                lines.append(f"  - Orphan Skill: {o}")
            for b in self.broken_managed_symlinks[:5]:
                lines.append(f"  - Broken Symlink: {b}")
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
        report.errors.append(f"Cannot read SKILL.md: {e}")
        return report

    fm = parse_frontmatter(content)
    if not fm or "name" not in fm or "description" not in fm:
        report.is_valid = False
        report.errors.append("Invalid or missing frontmatter in SKILL.md")
    else:
        desc = fm.get("description", "")
        if not TRIGGER_CONTRACT_PATTERN.search(desc):
            report.is_valid = False
            report.errors.append("Frontmatter description fails trigger contract")

    # Check internal markdown links
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for m in link_pattern.finditer(content):
        target = m.group(2).split("#")[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        report.markdown_links_checked += 1
        abs_target = os.path.normpath(os.path.join(skill_dir, target))
        if not os.path.exists(abs_target):
            report.is_valid = False
            report.errors.append(f"Broken markdown link in SKILL.md: {target}")

    # Check python syntax in scripts/
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        for fname in os.listdir(scripts_dir):
            if fname.endswith(".py"):
                py_path = os.path.join(scripts_dir, fname)
                report.scripts_checked += 1
                try:
                    with open(py_path, "r", encoding="utf-8", errors="replace") as pf:
                        py_code = pf.read()
                    ast.parse(py_code, filename=py_path)
                except SyntaxError as se:
                    report.is_valid = False
                    report.errors.append(f"Python syntax error in {fname}: {se}")

    # Check for workstation path leaks and secrets
    for root, _, files in os.walk(skill_dir):
        for fname in files:
            if fname.endswith((".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt")):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as cf:
                        fc = cf.read()
                    for pat in WORKSTATION_PATH_PATTERNS:
                        m = pat.search(fc)
                        if m:
                            report.is_valid = False
                            report.errors.append(f"Workstation path leak in {fname}: {m.group(0)}")
                    if fname.endswith((".py", ".js", ".ts", ".sh", ".json", ".yaml", ".yml", ".env")):
                        for pat in SECRET_PATTERNS:
                            m = pat.search(fc)
                            if m:
                                report.is_valid = False
                                report.errors.append(f"Potential secret leak in {fname}: {m.group(0)[:20]}...")
                except Exception:
                    pass

    return report


def validate_library(
    library_dir: str = LIBRARY_DIR,
    runtime_dir: str = RUNTIME_DIR,
    manifest: Optional[RuntimeManifest] = None,
) -> ValidationResult:
    """
    Validates the living library with exact four-way set reconciliation:
    Physical canonical packages == Router-indexed packages == Manifest entries == Runtime symlinks.
    """
    result = ValidationResult()
    m = manifest or RuntimeManifest()

    # Step 1: Discover all 26 routers dynamically
    all_routers = get_all_routers(library_dir=library_dir)
    result.total_routers = len(all_routers)
    norm_routers = {os.path.normpath(r) for r in all_routers}
    rel_routers = {os.path.relpath(r, REPO_ROOT).replace(os.sep, "/") for r in all_routers}

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
                result.broken_router_links.append(f"{os.path.relpath(r_path, REPO_ROOT)} -> {target}")
            elif os.path.basename(abs_target) == "SKILL.md" and abs_target not in norm_routers:
                skill_dir = os.path.dirname(abs_target)
                rel_target_dir = os.path.relpath(skill_dir, REPO_ROOT).replace(os.sep, "/")
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
                rel_s_dir = os.path.relpath(s_dir, REPO_ROOT).replace(os.sep, "/")
                physical_packages_set.add(rel_s_dir)

    # Step 4: Extract manifest packages
    manifest_packages_set: Set[str] = {
        s["canonical_path"].replace(os.sep, "/").strip("/")
        for s in m.skills.values()
    }
    result.total_manifest_skills = len(manifest_packages_set)

    # Step 5: Extract runtime symlink targets
    runtime_targets_set: Set[str] = set()
    if os.path.exists(runtime_dir):
        for item in os.listdir(runtime_dir):
            if item in PROTECTED_RUNTIME_ENTRIES:
                continue
            item_path = os.path.join(runtime_dir, item)
            if os.path.islink(item_path):
                raw_target = os.readlink(item_path)
                abs_t = os.path.normpath(os.path.join(runtime_dir, raw_target))
                if not os.path.exists(abs_t):
                    result.is_valid = False
                    result.broken_managed_symlinks.append(f"{item} -> {raw_target}")
                else:
                    rel_t = os.path.relpath(abs_t, REPO_ROOT).replace(os.sep, "/")
                    if rel_t.startswith("library/"):
                        runtime_targets_set.add(rel_t)
            elif os.path.isdir(item_path):
                result.is_valid = False
                result.reconciliation_discrepancies.append(
                    f"Physical directory found in runtime: {item} (must be managed symlink)"
                )
    result.total_managed_symlinks = len(runtime_targets_set)

    # Step 6: 4-Way Exact Set Equality Reconciliation (Finding 5)
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

    if manifest_packages_set != runtime_targets_set:
        unlinked = manifest_packages_set - runtime_targets_set
        extra_linked = runtime_targets_set - manifest_packages_set
        if unlinked:
            discrepancies.append(f"Manifest skills missing runtime symlinks ({len(unlinked)}): {sorted(list(unlinked))[:3]}")
        if extra_linked:
            discrepancies.append(f"Runtime symlinks pointing outside manifest ({len(extra_linked)}): {sorted(list(extra_linked))[:3]}")

    if discrepancies:
        result.is_valid = False
        result.set_reconciliation_passed = False
        result.reconciliation_discrepancies.extend(discrepancies)

    # Step 7: Validate each canonical skill package
    for s_rel in sorted(list(router_indexed_set)):
        s_abs = os.path.join(REPO_ROOT, s_rel)
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
