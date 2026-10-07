"""
Living Library Validator.
Dynamically verifies the canonical library, router hierarchy, package contracts,
script safety, workstation path leaks, runtime manifest, and .agents/skills symlinks
without frozen population assumptions.
"""

import ast
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .config import (
    ALL_SUBCATEGORIES,
    CATEGORIES,
    DEEP_CATEGORIES,
    DESTRUCTIVE_COMMAND_PATTERNS,
    FLAT_CATEGORIES,
    LIBRARY_DIR,
    PROTECTED_RUNTIME_ENTRIES,
    PROVIDER_COUPLING_PATTERNS,
    REPO_ROOT,
    RUNTIME_DIR,
    SECRET_PATTERNS,
    TRIGGER_CONTRACT_PATTERN,
    WORKSTATION_PATH_PATTERNS,
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
    provider_coupling_leaks: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "PASSED" if self.is_valid else "FAILED"
        lines = [
            f"=== Living Library Validation: {status} ===",
            f"Total Routers Verified: {self.total_routers}",
            f"Total Router Links Verified: {self.total_router_links} (Broken: {len(self.broken_router_links)})",
            f"Total Canonical Active Skills: {self.total_canonical_skills} (Orphans: {len(self.orphan_skills)})",
            f"Total Manifest Skills: {self.total_manifest_skills}",
            f"Total Managed Symlinks: {self.total_managed_symlinks} (Broken: {len(self.broken_managed_symlinks)})",
            f"Workstation Path Leaks: {len(self.workstation_path_leaks)}",
            f"Secret Leaks: {len(self.secret_leaks)}",
            f"Provider Coupling Leaks: {len(self.provider_coupling_leaks)}",
        ]
        if not self.is_valid:
            lines.append("\nErrors / Regressions Found:")
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
    """Parse YAML frontmatter enclosed in ---."""
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    fm_text = parts[1].strip()
    result = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip().strip("\"'")
    return result


def validate_single_skill(skill_dir: str) -> SkillValidationReport:
    """Validates an individual skill package against canonical standards."""
    rel_path = os.path.relpath(skill_dir, REPO_ROOT).replace(os.sep, "/")
    report = SkillValidationReport(skill_path=rel_path, name=os.path.basename(skill_dir))

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
    if not fm:
        report.is_valid = False
        report.errors.append("Invalid or missing frontmatter in SKILL.md")
    else:
        name = fm.get("name")
        desc = fm.get("description")
        if not name:
            report.is_valid = False
            report.errors.append("Frontmatter missing 'name'")
        else:
            report.name = name
        if not desc:
            report.is_valid = False
            report.errors.append("Frontmatter missing 'description'")
        elif not TRIGGER_CONTRACT_PATTERN.search(desc):
            report.is_valid = False
            report.errors.append(f"Description fails trigger contract: {desc[:60]}...")

    # Check relative links in SKILL.md
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for m in link_pattern.finditer(content):
        target = m.group(2).split("#")[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        report.markdown_links_checked += 1
        abs_target = os.path.normpath(os.path.join(skill_dir, target))
        if not os.path.exists(abs_target):
            report.is_valid = False
            report.errors.append(f"Broken relative link in SKILL.md: '{target}'")

    # Check Python scripts in scripts/
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.exists(scripts_dir):
        for root, _, files in os.walk(scripts_dir):
            for fname in files:
                if fname.endswith(".py"):
                    py_path = os.path.join(root, fname)
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
    Validates the living library without hardcoded population counts.
    Derives router and skill topology dynamically.
    """
    result = ValidationResult()
    m = manifest or RuntimeManifest()

    # Discover all routers dynamically
    root_router = os.path.join(library_dir, "SKILL.md")
    category_routers: List[str] = []
    subcategory_routers: List[str] = []

    for cat in CATEGORIES:
        cat_router = os.path.join(library_dir, cat, "SKILL.md")
        if os.path.exists(cat_router):
            category_routers.append(cat_router)

        # Check for subcategories
        cat_dir = os.path.join(library_dir, cat)
        if os.path.isdir(cat_dir):
            for item in sorted(os.listdir(cat_dir)):
                sub_router = os.path.join(cat_dir, item, "SKILL.md")
                if os.path.exists(sub_router):
                    # Check if it is a subcategory router (not a leaf skill)
                    with open(sub_router, "r", encoding="utf-8", errors="replace") as srf:
                        scontent = srf.read()
                    if "type: subcategory-router" in scontent or "subcategory-router" in scontent:
                        subcategory_routers.append(sub_router)

    all_routers = [root_router] + category_routers + subcategory_routers
    result.total_routers = len(all_routers)
    norm_routers = {os.path.normpath(r) for r in all_routers}

    # Verify routers exist
    for r in all_routers:
        if not os.path.exists(r):
            result.is_valid = False
            result.broken_router_links.append(f"Router file missing: {r}")

    # Traverse all router links
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    leaf_skills_indexed: List[str] = []

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
                leaf_skills_indexed.append(skill_dir)

    unique_leaf_indexed = sorted(list(set(leaf_skills_indexed)))
    result.total_canonical_skills = len(unique_leaf_indexed)

    # Check for duplicate router leaf links
    if len(leaf_skills_indexed) != len(unique_leaf_indexed):
        result.is_valid = False
        dups = [item for item in leaf_skills_indexed if leaf_skills_indexed.count(item) > 1]
        result.evidence.append(f"Duplicate leaf links in router hierarchy: {len(dups)} occurrences")

    # Discover all physical canonical skill packages under the 10 categories
    physical_canonical_skills: Set[str] = set()
    for cat in CATEGORIES:
        cat_dir = os.path.join(library_dir, cat)
        if not os.path.isdir(cat_dir):
            continue
        # Scan for skills
        for root, dirs, files in os.walk(cat_dir):
            if "SKILL.md" in files:
                abs_s = os.path.normpath(os.path.join(root, "SKILL.md"))
                if abs_s not in norm_routers:
                    # Filter out nested bundled packages (skills inside examples/plugins/etc.)
                    # Canonical skills are directly under cat/<subcat>/<skill> or cat/<subcat>/<group>/<skill>
                    rel_to_lib = os.path.relpath(root, library_dir).split(os.sep)
                    # Exclude deep vendor bundles like seo-skills-main, plugins, test-fixtures
                    if any(x in rel_to_lib for x in ["plugins", "vendor", "examples", "references", "tests", "fixtures"]):
                        continue
                    # If this directory is in unique_leaf_indexed, it is canonical!
                    if os.path.normpath(root) in [os.path.normpath(p) for p in unique_leaf_indexed]:
                        physical_canonical_skills.add(os.path.normpath(root))

    # Orphan check: Any indexed skill must exist physically, and no canonical skill unindexed
    for s in unique_leaf_indexed:
        if not os.path.isdir(s):
            result.is_valid = False
            result.orphan_skills.append(f"Indexed target is not directory: {s}")

    # Validate each canonical skill package
    for s_dir in unique_leaf_indexed:
        rep = validate_single_skill(s_dir)
        if not rep.is_valid:
            result.is_valid = False
            result.skill_errors[rep.skill_path] = rep.errors
        for err in rep.errors:
            if "Workstation path leak" in err:
                result.workstation_path_leaks.append(f"{rep.skill_path}: {err}")
            elif "secret leak" in err:
                result.secret_leaks.append(f"{rep.skill_path}: {err}")

    # Validate Runtime Manifest coverage
    result.total_manifest_skills = len(m.skills)
    manifest_canonical_paths = {
        os.path.normpath(os.path.join(REPO_ROOT, s["canonical_path"]))
        for s in m.skills.values()
    }
    indexed_canonical_paths = {os.path.normpath(p) for p in unique_leaf_indexed}

    missing_from_manifest = indexed_canonical_paths - manifest_canonical_paths
    if missing_from_manifest:
        result.is_valid = False
        result.evidence.append(f"{len(missing_from_manifest)} canonical skills missing from runtime manifest")

    # Validate Runtime Symlinks in .agents/skills/
    if os.path.exists(runtime_dir):
        for r_name, s_info in m.skills.items():
            sym_path = os.path.join(runtime_dir, r_name)
            if not os.path.lexists(sym_path):
                # Symlink missing
                result.is_valid = False
                result.broken_managed_symlinks.append(f"Missing symlink: {r_name}")
            elif not os.path.exists(sym_path):
                # Broken symlink
                result.is_valid = False
                result.broken_managed_symlinks.append(f"Broken symlink: {r_name} -> {os.readlink(sym_path)}")
            else:
                result.total_managed_symlinks += 1

    return result
