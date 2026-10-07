"""
Scanner Module for Intake and Runtime Layer.
Scans intake/ and .agents/skills/ non-destructively, identifying packages,
classifying runtime symlinks vs physical installations, and inspecting integration metadata.
"""

import os
import re
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set

from .config import (
    DEEP_CATEGORIES,
    DESTRUCTIVE_COMMAND_PATTERNS,
    FLAT_CATEGORIES,
    INTAKE_DIR,
    LIBRARY_DIR,
    PROTECTED_RUNTIME_ENTRIES,
    PROVIDER_COUPLING_PATTERNS,
    REPO_ROOT,
    RUNTIME_DIR,
    TRIGGER_CONTRACT_PATTERN,
    WORKSTATION_PATH_PATTERNS,
)
from .manifest import RuntimeManifest


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


@dataclass
class CandidatePackage:
    name: str
    source_dir: str
    has_skill_md: bool = False
    frontmatter_valid: bool = False
    frontmatter_name: str = ""
    description: str = ""
    trigger_valid: bool = False
    bundled_scripts: List[str] = field(default_factory=list)
    bundled_references: List[str] = field(default_factory=list)
    bundled_assets: List[str] = field(default_factory=list)
    provider_assumptions: List[str] = field(default_factory=list)
    workstation_paths: List[str] = field(default_factory=list)
    destructive_commands: List[str] = field(default_factory=list)
    installer_metadata: Dict[str, str] = field(default_factory=dict)
    suggested_category: str = ""
    suggested_subcategory: str = ""
    suggested_parent_router: str = ""
    issues: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RuntimeEntryClassification:
    name: str
    path: str
    classification: str  # MANAGED_LINK, EXTERNAL_PHYSICAL, BROKEN_LINK, EXTERNAL_LINK, PROTECTED, COLLISION
    target_path: Optional[str] = None
    resolved_canonical_path: Optional[str] = None
    installer_integration_info: Dict[str, str] = field(default_factory=dict)
    action: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScanResult:
    intake_candidates: List[CandidatePackage] = field(default_factory=list)
    runtime_entries: List[RuntimeEntryClassification] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "intake_candidates": [c.to_dict() for c in self.intake_candidates],
            "runtime_entries": [r.to_dict() for r in self.runtime_entries],
        }


def scan_candidate_directory(pkg_dir: str, name: Optional[str] = None) -> CandidatePackage:
    """Non-destructively inspects a candidate skill directory."""
    pkg_name = name or os.path.basename(pkg_dir.rstrip(os.sep))
    pkg = CandidatePackage(name=pkg_name, source_dir=pkg_dir)

    skill_md = os.path.join(pkg_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        pkg.issues.append("Missing SKILL.md")
        return pkg

    pkg.has_skill_md = True

    try:
        with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        pkg.issues.append(f"Cannot read SKILL.md: {e}")
        return pkg

    # Parse frontmatter
    fm = parse_frontmatter(content)
    if fm and "name" in fm and "description" in fm:
        pkg.frontmatter_valid = True
        pkg.frontmatter_name = fm.get("name", "")
        pkg.description = fm.get("description", "")
        if TRIGGER_CONTRACT_PATTERN.search(pkg.description):
            pkg.trigger_valid = True
        else:
            pkg.issues.append("Description fails trigger contract: must start with capital letter and include '. Use when'")
    else:
        pkg.issues.append("Invalid or missing frontmatter in SKILL.md (requires name and description)")

    # Scan for bundled scripts and resources
    for root, _, files in os.walk(pkg_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, pkg_dir).replace(os.sep, "/")
            if rel.startswith("scripts/"):
                pkg.bundled_scripts.append(rel)
            elif rel.startswith("references/"):
                pkg.bundled_references.append(rel)
            elif rel.startswith("assets/"):
                pkg.bundled_assets.append(rel)

            # Check file content for provider couplings, paths, destructive commands
            if fname.endswith((".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt")):
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as cf:
                        fcontent = cf.read()

                    # Provider coupling
                    for pat in PROVIDER_COUPLING_PATTERNS:
                        for m in pat.finditer(fcontent):
                            val = m.group(0)
                            if val not in pkg.provider_assumptions:
                                pkg.provider_assumptions.append(f"{val} in {rel}")

                    # Workstation paths
                    for pat in WORKSTATION_PATH_PATTERNS:
                        for m in pat.finditer(fcontent):
                            val = m.group(0)
                            if val not in pkg.workstation_paths:
                                pkg.workstation_paths.append(f"{val} in {rel}")

                    # Destructive commands
                    for pat in DESTRUCTIVE_COMMAND_PATTERNS:
                        for m in pat.finditer(fcontent):
                            val = m.group(0)
                            if val not in pkg.destructive_commands:
                                pkg.destructive_commands.append(f"{val} in {rel}")
                except Exception:
                    pass

    # Check for installer metadata
    meta_file = os.path.join(pkg_dir, ".installer-metadata.json")
    if os.path.exists(meta_file):
        try:
            import json
            with open(meta_file, "r", encoding="utf-8") as mf:
                pkg.installer_metadata = json.load(mf)
        except Exception:
            pass

    # Heuristic Classification (predict category & subcategory)
    desc_lower = (pkg.description + " " + pkg.name).lower()
    best_cat = "workflow-and-automation"
    best_subcat = "tool-integration"

    if any(k in desc_lower for k in ["data", "etl", "analytics", "sql", "bigquery", "pandas", "ml", "rag", "vector"]):
        best_cat = "data-and-ai"
        best_subcat = "analytics" if "analytic" in desc_lower else ("llm-and-rag" if "rag" in desc_lower or "llm" in desc_lower else "data-engineering")
    elif any(k in desc_lower for k in ["docker", "kubernetes", "k8s", "deploy", "aws", "gcp", "azure", "ci/cd", "pipeline", "infra", "observability", "telemetry", "metric", "monitoring"]):
        best_cat = "infrastructure-and-ops"
        best_subcat = "observability" if ("observab" in desc_lower or "telemetry" in desc_lower or "metric" in desc_lower or "monitor" in desc_lower) else ("ci-cd" if "ci" in desc_lower else "cloud-platforms")

    elif any(k in desc_lower for k in ["react", "nextjs", "vue", "frontend", "backend", "fastapi", "django", "api", "architecture", "code", "typescript"]):
        best_cat = "development"
        best_subcat = "frontend" if "front" in desc_lower else ("backend" if "back" in desc_lower or "api" in desc_lower else "software-architecture")
    elif any(k in desc_lower for k in ["ui", "ux", "design", "figma", "css", "theme", "tailwind", "motion", "critique"]):
        best_cat = "design-and-experience"
        best_subcat = "ui-ux" if "ui" in desc_lower or "ux" in desc_lower else "design-systems"
    elif any(k in desc_lower for k in ["seo", "keyword", "ranking", "serp", "marketing", "campaign", "cro"]):
        best_cat = "marketing-and-seo"
        best_subcat = "technical-seo" if "seo" in desc_lower else "content-and-campaigns"
    elif any(k in desc_lower for k in ["test", "audit", "security", "vulnerability", "debug", "qa", "lint", "compliance"]):
        best_cat = "quality-and-security"
        best_subcat = "security" if "security" in desc_lower or "vuln" in desc_lower else "testing"
    elif any(k in desc_lower for k in ["agent", "skill", "prompt", "subagent", "orchestration"]):
        best_cat = "meta-and-agent-skills"
        best_subcat = "skill-lifecycle"
    elif any(k in desc_lower for k in ["doc", "writing", "guide", "readme", "markdown", "copy"]):
        best_cat = "content-and-documentation"
        best_subcat = "technical-writing"
    elif any(k in desc_lower for k in ["business", "finance", "startup", "legal", "compliance", "pricing"]):
        best_cat = "business-and-operations"
        best_subcat = "strategy"

    pkg.suggested_category = best_cat
    pkg.suggested_subcategory = best_subcat
    if best_cat in DEEP_CATEGORIES:
        pkg.suggested_parent_router = f"library/{best_cat}/{best_subcat}/SKILL.md"
    else:
        pkg.suggested_parent_router = f"library/{best_cat}/SKILL.md"

    return pkg


def scan_intake(intake_dir: str = INTAKE_DIR) -> List[CandidatePackage]:
    """Scans intake directory for candidate packages."""
    candidates = []
    if not os.path.exists(intake_dir):
        return candidates

    for item in sorted(os.listdir(intake_dir)):
        if item.startswith(".") or item in ["README.md", ".gitkeep"]:
            continue
        pkg_dir = os.path.join(intake_dir, item)
        if os.path.isdir(pkg_dir):
            candidates.append(scan_candidate_directory(pkg_dir, name=item))

    return candidates


def inspect_external_installer_environment(entry_path: str) -> Dict[str, str]:
    """
    Inspects surrounding environment to preserve external installer compatibility.
    Checks package.json, manifests, .skills, and installer references.
    """
    info = {}
    parent = os.path.dirname(entry_path)
    info["parent_directory"] = parent

    # Check for skills.sh or npm installer artifacts
    pkg_json = os.path.join(entry_path, "package.json")
    if os.path.exists(pkg_json):
        info["has_package_json"] = "true"
        try:
            import json
            with open(pkg_json, "r", encoding="utf-8") as f:
                pj = json.load(f)
                info["package_name"] = pj.get("name", "")
                info["package_version"] = pj.get("version", "")
        except Exception:
            pass

    # Check agent configuration files in repository root or parent
    for cfg_candidate in [".agent-skills.json", "skills.config.json"]:
        cfg_path = os.path.join(REPO_ROOT, cfg_candidate)
        if os.path.exists(cfg_path):
            info["agent_config_file"] = cfg_candidate

    return info


def scan_runtime(
    runtime_dir: str = RUNTIME_DIR,
    library_dir: str = LIBRARY_DIR,
    manifest: Optional[RuntimeManifest] = None,
) -> List[RuntimeEntryClassification]:
    """
    Inspects .agents/skills/ and classifies each entry.
    """
    results = []
    if not os.path.exists(runtime_dir):
        return results

    m = manifest or RuntimeManifest()
    norm_lib_dir = os.path.normpath(library_dir)

    for item in sorted(os.listdir(runtime_dir)):
        item_path = os.path.join(runtime_dir, item)

        if item in PROTECTED_RUNTIME_ENTRIES:
            results.append(RuntimeEntryClassification(
                name=item,
                path=item_path,
                classification="PROTECTED",
                action="PASS / LEAVE UNCHANGED (Protected System Task)",
            ))
            continue

        if os.path.islink(item_path):
            raw_target = os.readlink(item_path)
            # Resolve relative symlink from runtime_dir
            abs_target = os.path.normpath(os.path.join(runtime_dir, raw_target))
            target_exists = os.path.exists(abs_target)

            if not target_exists:
                results.append(RuntimeEntryClassification(
                    name=item,
                    path=item_path,
                    classification="BROKEN_LINK",
                    target_path=raw_target,
                    action="REPORT / REPAIR (Symlink target missing)",
                ))
            elif abs_target.startswith(norm_lib_dir):
                # Points inside library
                rel_canonical = os.path.relpath(abs_target, REPO_ROOT).replace(os.sep, "/")
                results.append(RuntimeEntryClassification(
                    name=item,
                    path=item_path,
                    classification="MANAGED_LINK",
                    target_path=raw_target,
                    resolved_canonical_path=rel_canonical,
                    action="PASS / LEAVE UNCHANGED",
                ))
            else:
                # Points outside library
                results.append(RuntimeEntryClassification(
                    name=item,
                    path=item_path,
                    classification="EXTERNAL_LINK",
                    target_path=raw_target,
                    action="REPORT / INSPECT (Points outside canonical library)",
                ))
        elif os.path.isdir(item_path):
            # Physical directory created directly under .agents/skills/
            integration_info = inspect_external_installer_environment(item_path)

            # Check if this name collides with an existing managed canonical name
            is_collision = item in m.skills

            if is_collision:
                results.append(RuntimeEntryClassification(
                    name=item,
                    path=item_path,
                    classification="COLLISION",
                    installer_integration_info=integration_info,
                    action="STOP FOR REVIEW (Name collides with canonical skill)",
                ))
            else:
                results.append(RuntimeEntryClassification(
                    name=item,
                    path=item_path,
                    classification="EXTERNAL_PHYSICAL",
                    installer_integration_info=integration_info,
                    action="DISCOVER -> stage to intake -> process through intake pipeline",
                ))
        else:
            # Regular file (unmanaged)
            results.append(RuntimeEntryClassification(
                name=item,
                path=item_path,
                classification="EXTERNAL_PHYSICAL",
                action="DISCOVER / INSPECT (Unmanaged file in runtime directory)",
            ))

    return results


def run_full_scan() -> ScanResult:
    """Executes a non-destructive scan of both intake/ and .agents/skills/."""
    m = RuntimeManifest()
    intake_c = scan_intake()
    runtime_e = scan_runtime(manifest=m)
    return ScanResult(intake_candidates=intake_c, runtime_entries=runtime_e)
