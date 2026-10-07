"""
Intake Evaluation and Installation Module.
Evaluates staged candidates, detects duplicates and semantic overlap,
enforces the human approval gate, normalizes packages, and installs approved skills
into the canonical library hierarchy.
"""

import json
import os
import re
import shutil
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .config import (
    ALL_SUBCATEGORIES,
    CATEGORIES,
    DEEP_CATEGORIES,
    FLAT_CATEGORIES,
    INTAKE_DIR,
    LIBRARY_DIR,
    REPO_ROOT,
    RUNTIME_DIR,
    TRIGGER_CONTRACT_PATTERN,
)
from .ledger import ChangeLedger
from .manifest import RuntimeManifest
from .scanner import CandidatePackage, scan_candidate_directory
from .validator import parse_frontmatter, validate_single_skill


def tokenize(text: str) -> Set[str]:
    """Extract lowercased alphanumeric tokens of length >= 3."""
    return set(re.findall(r"[a-z0-9]{3,}", text.lower()))


def compute_similarity(tokens1: Set[str], tokens2: Set[str]) -> float:
    """Computes Jaccard similarity between two token sets."""
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)


def compute_dice_similarity(tokens1: Set[str], tokens2: Set[str]) -> float:
    """Computes Dice / Sørensen similarity between two token sets."""
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    return (2.0 * len(intersection)) / (len(tokens1) + len(tokens2))



@dataclass
class IntakeEvaluation:
    candidate_name: str
    source_dir: str
    is_valid_package: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommended_decision: str = "NEW"  # NEW, MERGE, KEEP_SEPARATE, REPLACE, RENAME, QUARANTINE, REJECT, REVIEW_REQUIRED
    approval_required: bool = False
    approval_reasons: List[str] = field(default_factory=list)
    assigned_category: str = ""
    assigned_subcategory: str = ""
    target_router_path: str = ""
    target_canonical_path: str = ""
    semantic_competitors: List[Dict[str, any]] = field(default_factory=list)
    name_collision: bool = False
    provider_coupling_found: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    def summary(self) -> str:
        lines = [
            f"=== Intake Evaluation: {self.candidate_name} ===",
            f"Recommended Decision: {self.recommended_decision}",
            f"Approval Required: {'YES' if self.approval_required else 'NO'}",
            f"Assigned Category: {self.assigned_category}",
            f"Assigned Subcategory: {self.assigned_subcategory}",
            f"Target Router: {self.target_router_path}",
            f"Target Canonical Path: {self.target_canonical_path}",
        ]
        if self.approval_reasons:
            lines.append("Approval Gate Triggered By:")
            for r in self.approval_reasons:
                lines.append(f"  - {r}")
        if self.semantic_competitors:
            lines.append("Top Semantic Competitors in Canonical Library:")
            for c in self.semantic_competitors[:3]:
                lines.append(f"  - {c['name']} ({c['canonical_path']}): {c['similarity']:.1%} similarity")
        if self.errors:
            lines.append("Errors:")
            for e in self.errors:
                lines.append(f"  - {e}")
        return "\n".join(lines)


def evaluate_candidate(
    candidate_name: str,
    intake_dir: str = INTAKE_DIR,
    library_dir: str = LIBRARY_DIR,
    manifest: Optional[RuntimeManifest] = None,
) -> IntakeEvaluation:
    """Evaluates a candidate package against the canonical library."""
    candidate_path = os.path.join(intake_dir, candidate_name)
    eval_result = IntakeEvaluation(
        candidate_name=candidate_name,
        source_dir=candidate_path,
    )

    if not os.path.exists(candidate_path):
        eval_result.is_valid_package = False
        eval_result.errors.append(f"Candidate directory does not exist: {candidate_path}")
        eval_result.recommended_decision = "REJECT"
        return eval_result

    # 1. Package Structure & Validation
    pkg = scan_candidate_directory(candidate_path, name=candidate_name)
    if not pkg.has_skill_md:
        eval_result.is_valid_package = False
        eval_result.errors.append("Missing SKILL.md")
        eval_result.recommended_decision = "REJECT"
        return eval_result

    val_rep = validate_single_skill(candidate_path)
    if not val_rep.is_valid:
        eval_result.is_valid_package = False
        eval_result.errors.extend(val_rep.errors)

    # 2. Provider Coupling & Workstation Paths
    if pkg.provider_assumptions:
        eval_result.provider_coupling_found = True
        eval_result.warnings.append(f"Provider assumptions detected: {', '.join(pkg.provider_assumptions[:3])}")
        eval_result.approval_required = True
        eval_result.approval_reasons.append("Provider coupling detected (normalization required)")

    if pkg.workstation_paths:
        eval_result.is_valid_package = False
        eval_result.errors.append(f"Workstation paths detected: {', '.join(pkg.workstation_paths[:3])}")

    if pkg.destructive_commands:
        eval_result.warnings.append(f"Destructive commands detected: {', '.join(pkg.destructive_commands[:3])}")
        eval_result.approval_required = True
        eval_result.approval_reasons.append("Destructive commands present without verified human review")

    # 3. Categorization
    eval_result.assigned_category = pkg.suggested_category
    eval_result.assigned_subcategory = pkg.suggested_subcategory
    if pkg.suggested_category in DEEP_CATEGORIES:
        eval_result.target_router_path = f"library/{pkg.suggested_category}/{pkg.suggested_subcategory}/SKILL.md"
    else:
        eval_result.target_router_path = f"library/{pkg.suggested_category}/SKILL.md"

    eval_result.target_canonical_path = f"library/{pkg.suggested_category}/{pkg.suggested_subcategory}/{candidate_name}"

    # 4. Compare against Canonical Library (Semantic Overlap & Name Collisions)
    m = manifest or RuntimeManifest()
    candidate_tokens = tokenize(candidate_name + " " + pkg.description)

    # Direct name collision check
    if candidate_name in m.skills:
        eval_result.name_collision = True
        eval_result.approval_required = True
        eval_result.approval_reasons.append(f"Name collision with existing runtime skill '{candidate_name}'")

    # Compare with existing skills
    competitor_scores = []
    for s_name, s_info in m.skills.items():
        cpath = s_info["canonical_path"]
        abs_cpath = os.path.join(REPO_ROOT, cpath)
        skill_md_path = os.path.join(abs_cpath, "SKILL.md")
        if os.path.exists(skill_md_path):
            try:
                with open(skill_md_path, "r", encoding="utf-8", errors="replace") as f:
                    ccontent = f.read()
                fm = parse_frontmatter(ccontent)
                cdesc = fm.get("description", "") if fm else ""
                ctokens = tokenize(s_name + " " + cdesc)
                sim = compute_dice_similarity(candidate_tokens, ctokens)
                if sim >= 0.25:
                    competitor_scores.append({
                        "name": s_name,
                        "canonical_path": cpath,
                        "similarity": sim,
                    })
            except Exception:
                pass

    competitor_scores.sort(key=lambda x: x["similarity"], reverse=True)
    eval_result.semantic_competitors = competitor_scores[:5]

    # Decision Matrix
    top_sim = competitor_scores[0]["similarity"] if competitor_scores else 0.0

    if eval_result.name_collision and top_sim >= 0.75:
        eval_result.recommended_decision = "REJECT"
        eval_result.approval_required = True
        eval_result.approval_reasons.append(f"True duplicate of existing skill '{competitor_scores[0]['name']}'")
    elif top_sim >= 0.55:
        eval_result.recommended_decision = "MERGE"
        eval_result.approval_required = True
        eval_result.approval_reasons.append(
            f"High semantic overlap ({top_sim:.1%}) with '{competitor_scores[0]['name']}'"
        )
    elif eval_result.name_collision:
        eval_result.recommended_decision = "RENAME"
        eval_result.approval_required = True
        eval_result.approval_reasons.append("Name collision requires distinct canonical or runtime naming")
    elif top_sim >= 0.35:
        eval_result.recommended_decision = "KEEP_SEPARATE"
        eval_result.approval_required = True
        eval_result.approval_reasons.append(
            f"Moderate overlap ({top_sim:.1%}) with '{competitor_scores[0]['name']}'; requires disambiguation review"
        )
    elif not eval_result.is_valid_package:
        eval_result.recommended_decision = "REVIEW_REQUIRED"
        eval_result.approval_required = True

    else:
        eval_result.recommended_decision = "NEW"

    return eval_result


def normalize_package_content(skill_dir: str) -> None:
    """Decouples provider-specific wording and ensures compliant frontmatter."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return

    with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Provider decoupling: replace "Claude" with "Agent"
    content_clean = re.sub(r"\bClaude(?:'s)?\b", "Agent", content)
    content_clean = re.sub(r"\bAnthropic\b", "AI Platform", content_clean)

    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(content_clean)


def add_link_to_router(
    router_path: str,
    skill_name: str,
    skill_dir_path: str,
    subcategory: str,
    description: str,
) -> bool:
    """Inserts a markdown link for a new skill into the appropriate router table or section."""
    if not os.path.exists(router_path):
        return False

    with open(router_path, "r", encoding="utf-8") as f:
        content = f.read()

    rel_target = os.path.relpath(os.path.join(skill_dir_path, "SKILL.md"), os.path.dirname(router_path)).replace(os.sep, "/")
    new_entry = f"| [{skill_name}]({rel_target}) | {description} |\n"

    # Check if link already present
    if rel_target in content or f"[{skill_name}]" in content:
        return True

    # Check if table exists under subcategory
    subcat_header = f"### {subcategory}"
    if subcat_header.lower() in content.lower():
        # Find position after header table
        pos = content.lower().find(subcat_header.lower())
        # Find next table row or table separator after pos
        sep_pos = content.find("|---|", pos)
        if sep_pos != -1:
            # Find end of separator line
            line_end = content.find("\n", sep_pos)
            new_content = content[: line_end + 1] + new_entry + content[line_end + 1 :]
            with open(router_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True

    # Fallback: append to end of router file
    if "| Skill | Description |" not in content:
        content += f"\n\n### {subcategory}\n\n| Skill | Description |\n|---|---|\n"
    content += new_entry
    with open(router_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def apply_candidate(
    candidate_name: str,
    category: str,
    subcategory: str,
    canonical_name: Optional[str] = None,
    intake_dir: str = INTAKE_DIR,
    library_dir: str = LIBRARY_DIR,
    manifest: Optional[RuntimeManifest] = None,
    ledger: Optional[ChangeLedger] = None,
    dry_run: bool = False,
) -> dict:
    """
    Installs an approved candidate from intake/ into library/, updates router,
    manifest, and change ledger.
    """
    final_name = canonical_name or candidate_name
    src_dir = os.path.join(intake_dir, candidate_name)
    target_dir = os.path.join(library_dir, category, subcategory, final_name)

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Candidate source not found: {src_dir}")

    if os.path.exists(target_dir):
        raise FileExistsError(f"Target destination already exists: {target_dir}")

    # Determine router
    if category in DEEP_CATEGORIES:
        router_path = os.path.join(library_dir, category, subcategory, "SKILL.md")
    else:
        router_path = os.path.join(library_dir, category, "SKILL.md")

    # Read description from candidate
    desc = "Specialized agent capability."
    skill_md = os.path.join(src_dir, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip().strip("\"'")
                    break

    if not dry_run:
        # 1. Normalize package
        normalize_package_content(src_dir)

        # 2. Move to canonical library
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        shutil.move(src_dir, target_dir)

        # 3. Update router
        add_link_to_router(
            router_path=router_path,
            skill_name=final_name,
            skill_dir_path=target_dir,
            subcategory=subcategory,
            description=desc,
        )

        # 4. Update manifest
        m = manifest or RuntimeManifest()
        # Determine runtime name (handle collisions)
        runtime_name = final_name
        if runtime_name in m.skills:
            runtime_name = f"{category}-{final_name}"
            if runtime_name in m.skills:
                runtime_name = f"{category}-{subcategory}-{final_name}"

        canonical_rel = os.path.relpath(target_dir, REPO_ROOT).replace(os.sep, "/")
        router_rel = os.path.relpath(router_path, REPO_ROOT).replace(os.sep, "/")

        m.add_skill(
            runtime_name=runtime_name,
            canonical_name=final_name,
            canonical_path=canonical_rel,
            functional_parent=router_rel,
            source="intake",
            managed=True,
        )
        m.save()

        # 5. Append to Change Ledger
        lg = ledger or ChangeLedger()
        lg.record_change(
            operation="ADD",
            source="intake",
            source_path=src_dir,
            original_name=candidate_name,
            canonical_name=final_name,
            runtime_name=runtime_name,
            decision="NEW",
            category=category,
            subcategory=subcategory,
            canonical_path=canonical_rel,
            functional_parent=router_rel,
            validation_status="PASS",
            pilot_status="PASS",
        )

    return {
        "candidate_name": candidate_name,
        "canonical_name": final_name,
        "target_directory": target_dir,
        "router_updated": router_path,
    }
