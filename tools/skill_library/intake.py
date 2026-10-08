"""
Intake Evaluation, Normalization, Router Integration, and Lifecycle Application.
Handles the complete path from external or downloaded skill to approved canonical library skill.
"""

import copy
import json
import os
import re
import shutil
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple

from .config import (
    AUDIT_DIR,
    CATEGORIES,
    DEEP_CATEGORIES,
    FLAT_CATEGORIES,
    INTAKE_DIR,
    LIBRARY_DIR,
    PROVIDER_COUPLING_PATTERNS,
    REPO_ROOT,
    RUNTIME_DIR,
    SECRET_PATTERNS,
    TRIGGER_CONTRACT_PATTERN,
    WORKSTATION_PATH_PATTERNS,
)
from .ledger import ChangeLedger
from .manifest import RuntimeManifest
from .pilot import run_targeted_pilot
from .scanner import CandidatePackage, scan_candidate_directory
from .validator import validate_single_skill


def _safe_relpath(target: str, start: str) -> str:
    """Computes relative path, falling back to absolute if on different drives/roots."""
    try:
        return os.path.relpath(target, start)
    except ValueError:
        return os.path.abspath(target)


def tokenize(text: str) -> Set[str]:
    """Tokenize lowercase words for similarity calculation."""
    words = re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", text.lower())
    stop_words = {
        "and", "the", "for", "with", "that", "this", "from", "when", "use",
        "you", "are", "can", "all", "your", "into", "need", "skill", "agent",
    }
    return {w for w in words if w not in stop_words}


def compute_dice_similarity(tokens1: Set[str], tokens2: Set[str]) -> float:
    """Computes Dice similarity coefficient between two token sets."""
    if not tokens1 or not tokens2:
        return 0.0
    intersection = len(tokens1 & tokens2)
    return (2.0 * intersection) / (len(tokens1) + len(tokens2))


def parse_frontmatter(content: str) -> Optional[dict]:
    """Extract frontmatter as dictionary."""
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


@dataclass
class IntakeEvaluation:
    candidate_name: str
    source_dir: str
    is_valid_package: bool = True
    is_update: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommended_decision: str = "NEW"  # NEW, UPDATE, MERGE, KEEP_SEPARATE, RENAME, QUARANTINE, REJECT, REVIEW_REQUIRED
    approval_required: bool = False
    approval_reasons: List[str] = field(default_factory=list)
    assigned_category: str = ""
    assigned_subcategory: str = ""
    target_router_path: str = ""
    target_canonical_path: str = ""
    diff_summary: Dict[str, list] = field(default_factory=dict)
    semantic_competitors: List[Dict[str, any]] = field(default_factory=list)
    name_collision: bool = False
    provider_coupling_found: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    def summary(self) -> str:
        lines = [
            f"=== Intake Evaluation: {self.candidate_name} ===",
            f"Decision: {self.recommended_decision}",
            f"Is Update: {'YES' if self.is_update else 'NO'}",
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
        if self.diff_summary:
            lines.append(f"Diff Summary: {self.diff_summary}")
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

    m = manifest or RuntimeManifest()

    # Check for installer metadata indicating an EXTERNAL_UPDATE
    meta_file = os.path.join(candidate_path, ".installer-metadata.json")
    is_external_update = False
    existing_canonical_path = ""
    if os.path.exists(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
                if meta.get("type") == "external_update":
                    is_external_update = True
                    existing_canonical_path = meta.get("target_canonical_path", "")
        except Exception:
            pass

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

    repo_root = os.path.dirname(os.path.normpath(library_dir))

    # 3. Categorization or Update Routing
    if is_external_update and existing_canonical_path:
        eval_result.is_update = True
        eval_result.target_canonical_path = existing_canonical_path
        # Parse category/subcategory from existing path
        parts = existing_canonical_path.strip("/").split("/")
        if len(parts) >= 3:
            eval_result.assigned_category = parts[1]
            eval_result.assigned_subcategory = parts[2]
        if eval_result.assigned_category in DEEP_CATEGORIES:
            eval_result.target_router_path = f"library/{eval_result.assigned_category}/{eval_result.assigned_subcategory}/SKILL.md"
        else:
            eval_result.target_router_path = f"library/{eval_result.assigned_category}/SKILL.md"

        # Compare diff against canonical
        abs_canonical = os.path.normpath(os.path.join(repo_root, existing_canonical_path))
        diff_summary = {"modified": [], "added": [], "removed": []}
        if os.path.exists(abs_canonical):
            cand_files = {
                os.path.relpath(os.path.join(r, f), candidate_path): os.path.join(r, f)
                for r, _, fs in os.walk(candidate_path) for f in fs if f != ".installer-metadata.json"
            }
            canon_files = {
                os.path.relpath(os.path.join(r, f), abs_canonical): os.path.join(r, f)
                for r, _, fs in os.walk(abs_canonical) for f in fs
            }
            for cf, cp in cand_files.items():
                if cf not in canon_files:
                    diff_summary["added"].append(cf)
                else:
                    try:
                        with open(cp, "rb") as f1, open(canon_files[cf], "rb") as f2:
                            if f1.read() != f2.read():
                                diff_summary["modified"].append(cf)
                    except Exception:
                        pass
            for cf in canon_files.keys():
                if cf not in cand_files:
                    diff_summary["removed"].append(cf)

        eval_result.diff_summary = diff_summary
        eval_result.recommended_decision = "UPDATE"
        eval_result.approval_required = True
        eval_result.approval_reasons.append(
            f"External update to managed skill '{candidate_name}' ({len(diff_summary['modified'])} modified, "
            f"{len(diff_summary['added'])} added, {len(diff_summary['removed'])} removed)"
        )
        return eval_result

    # Brand new candidate categorization
    eval_result.assigned_category = pkg.suggested_category
    eval_result.assigned_subcategory = pkg.suggested_subcategory
    if pkg.suggested_category in DEEP_CATEGORIES:
        eval_result.target_router_path = f"library/{pkg.suggested_category}/{pkg.suggested_subcategory}/SKILL.md"
    else:
        eval_result.target_router_path = f"library/{pkg.suggested_category}/SKILL.md"

    eval_result.target_canonical_path = f"library/{pkg.suggested_category}/{pkg.suggested_subcategory}/{candidate_name}"

    # 4. Compare against Canonical Library (Semantic Overlap & Name Collisions)
    candidate_tokens = tokenize(candidate_name + " " + pkg.description)
    base_candidate_name = re.sub(r"[_vV\-](\d+|v\d+)$", "", candidate_name)
    has_counter_suffix = (base_candidate_name != candidate_name)

    # Direct name collision check
    if candidate_name in m.skills:
        eval_result.name_collision = True
        eval_result.approval_required = True
        eval_result.approval_reasons.append(f"Name collision with existing runtime skill '{candidate_name}'")

    if has_counter_suffix and base_candidate_name in m.skills:
        eval_result.name_collision = True
        eval_result.approval_required = True
        eval_result.approval_reasons.append(
            f"Candidate '{candidate_name}' uses synthetic counter/version suffix masking existing skill '{base_candidate_name}'"
        )

    # Compare with existing skills
    competitor_scores = []
    for s_name, s_info in m.skills.items():
        cpath = s_info["canonical_path"]
        abs_cpath = os.path.normpath(os.path.join(repo_root, cpath))
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

    if eval_result.name_collision and (top_sim >= 0.50 or (has_counter_suffix and base_candidate_name in m.skills)):
        eval_result.recommended_decision = "REJECT"
        eval_result.approval_required = True
        matched_target = base_candidate_name if (has_counter_suffix and base_candidate_name in m.skills) else (competitor_scores[0]['name'] if competitor_scores else candidate_name)
        eval_result.approval_reasons.append(f"True duplicate of existing skill '{matched_target}'")
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


def normalize_package_content(candidate_dir: str) -> None:
    """Removes provider coupling, normalizes trigger contract, and cleans metadata."""
    skill_md = os.path.join(candidate_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return

    with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    content_clean = content
    for pat in PROVIDER_COUPLING_PATTERNS:
        content_clean = pat.sub("Agent", content_clean)

    # Remove temporary installer metadata if present
    meta_path = os.path.join(candidate_dir, ".installer-metadata.json")
    if os.path.exists(meta_path):
        os.remove(meta_path)

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
        pos = content.lower().find(subcat_header.lower())
        sep_pos = content.find("|---|", pos)
        if sep_pos != -1:
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
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    canonical_name: Optional[str] = None,
    approved: bool = False,
    intake_dir: str = INTAKE_DIR,
    library_dir: str = LIBRARY_DIR,
    runtime_dir: str = RUNTIME_DIR,
    manifest: Optional[RuntimeManifest] = None,
    ledger: Optional[ChangeLedger] = None,
    dry_run: bool = False,
) -> dict:
    """
    Installs an approved candidate from intake/ into library/, updates router,
    manifest, change ledger, and automatically replaces any physical runtime folder
    with a canonical relative symlink.
    """
    src_dir = os.path.join(intake_dir, candidate_name)
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Candidate source not found: {src_dir}")

    m = manifest or RuntimeManifest()
    eval_res = evaluate_candidate(candidate_name, intake_dir=intake_dir, library_dir=library_dir, manifest=m)

    # Enforce Human Approval Gate (Finding 3)
    if eval_res.approval_required and not approved:
        reasons = "\n  - ".join(eval_res.approval_reasons)
        raise PermissionError(
            f"Cannot apply candidate '{candidate_name}': Human Approval Gate required.\n"
            f"Reasons:\n  - {reasons}\n"
            "Pass --approve to confirm human authorization."
        )

    repo_root = os.path.dirname(os.path.normpath(library_dir))

    # Determine operation mode: UPDATE or NEW
    is_update = eval_res.is_update or eval_res.recommended_decision == "UPDATE"

    if is_update:
        target_canonical_rel = eval_res.target_canonical_path
        target_dir = os.path.normpath(os.path.join(repo_root, target_canonical_rel))
        final_name = os.path.basename(target_dir)
        cat = eval_res.assigned_category
        subcat = eval_res.assigned_subcategory
        router_path = os.path.normpath(os.path.join(repo_root, eval_res.target_router_path))
        operation = "UPDATE"
        decision = "UPDATE"
        runtime_name = candidate_name
    else:
        final_name = canonical_name or candidate_name
        cat = category or eval_res.assigned_category or "workflow-and-automation"
        subcat = subcategory or eval_res.assigned_subcategory or "tool-integration"
        target_dir = os.path.join(library_dir, cat, subcat, final_name)
        if os.path.exists(target_dir):
            raise FileExistsError(f"Target destination already exists: {target_dir}")

        if cat in DEEP_CATEGORIES:
            router_path = os.path.join(library_dir, cat, subcat, "SKILL.md")
        else:
            router_path = os.path.join(library_dir, cat, "SKILL.md")
        operation = "ADD"
        decision = "NEW"
        runtime_name = final_name
        if runtime_name in m.skills:
            runtime_name = f"{cat}-{final_name}"
            if runtime_name in m.skills:
                runtime_name = f"{cat}-{subcat}-{final_name}"

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
        # Step A: Normalization & Pre-Install Validation
        normalize_package_content(src_dir)
        pre_val = validate_single_skill(src_dir)
        if not pre_val.is_valid:
            lg = ledger or ChangeLedger()
            lg.record_change(
                operation=operation,
                source="intake",
                source_path=src_dir,
                original_name=candidate_name,
                canonical_name=final_name,
                runtime_name=runtime_name,
                decision="REJECT",
                category=cat,
                subcategory=subcat,
                canonical_path="",
                functional_parent="",
                validation_status="FAIL",
                pilot_status="NOT_RUN",
            )
            err_msg = "; ".join(pre_val.errors)
            raise ValueError(f"Candidate package validation failed prior to installation: {err_msg}")

        # Step B: Preserve State for Transactional Rollback
        backup_candidate_dir = tempfile.mkdtemp(prefix="intake_backup_")
        candidate_backup_path = os.path.join(backup_candidate_dir, candidate_name)
        shutil.copytree(src_dir, candidate_backup_path)

        backup_canonical_dir = None
        canonical_backup_path = None
        orig_manifest_entry = None
        if is_update:
            backup_canonical_dir = tempfile.mkdtemp(prefix="canonical_backup_")
            canonical_backup_path = os.path.join(backup_canonical_dir, final_name)
            if os.path.exists(target_dir):
                shutil.copytree(target_dir, canonical_backup_path)
            orig_manifest_entry = copy.deepcopy(m.skills.get(runtime_name))

        orig_router_content = None
        if os.path.exists(router_path):
            with open(router_path, "r", encoding="utf-8") as rf:
                orig_router_content = rf.read()

        runtime_item_path = os.path.join(runtime_dir, runtime_name)
        candidate_runtime_path = os.path.join(runtime_dir, candidate_name)
        orig_runtime_states = {}
        for p in {runtime_item_path, candidate_runtime_path}:
            if os.path.islink(p):
                orig_runtime_states[p] = ("symlink", os.readlink(p))
            elif os.path.isdir(p):
                orig_runtime_states[p] = ("dir", None)
            else:
                orig_runtime_states[p] = ("missing", None)

        canonical_rel = os.path.relpath(target_dir, repo_root).replace(os.sep, "/")
        router_rel = os.path.relpath(router_path, repo_root).replace(os.sep, "/")

        def _do_rollback(val_st: str = "FAIL", pilot_st: str = "FAIL"):
            if is_update:
                # 1. Restore canonical package
                try:
                    if os.path.exists(target_dir):
                        shutil.rmtree(target_dir)
                    if canonical_backup_path and os.path.exists(canonical_backup_path):
                        shutil.copytree(canonical_backup_path, target_dir)
                except Exception:
                    pass

                # 2. Restore router content
                try:
                    if orig_router_content is not None and os.path.exists(router_path):
                        with open(router_path, "w", encoding="utf-8") as rf:
                            rf.write(orig_router_content)
                except Exception:
                    pass

                # 3. Restore manifest entry
                try:
                    if orig_manifest_entry is not None:
                        m.skills[runtime_name] = orig_manifest_entry
                    elif runtime_name in m.skills:
                        m.remove_skill(runtime_name)
                    m.save()
                except Exception:
                    pass

                # 4. Restore candidate in intake for review
                try:
                    if not os.path.exists(src_dir) and os.path.exists(candidate_backup_path):
                        shutil.copytree(candidate_backup_path, src_dir)
                except Exception:
                    pass
            else:
                # NEW skill rollback
                # 1. Remove canonical package
                try:
                    if os.path.exists(target_dir):
                        shutil.rmtree(target_dir)
                except Exception:
                    pass

                # 2. Restore router
                try:
                    if orig_router_content is not None and os.path.exists(router_path):
                        with open(router_path, "w", encoding="utf-8") as rf:
                            rf.write(orig_router_content)
                except Exception:
                    pass

                # 3. Remove manifest entry
                try:
                    if runtime_name in m.skills:
                        m.remove_skill(runtime_name)
                        m.save()
                except Exception:
                    pass

                # 4. Restore candidate in intake
                try:
                    if not os.path.exists(src_dir) and os.path.exists(candidate_backup_path):
                        shutil.copytree(candidate_backup_path, src_dir)
                except Exception:
                    pass

            # Record failure in Change Ledger
            try:
                lg = ledger or ChangeLedger()
                lg.record_change(
                    operation=operation,
                    source="intake",
                    source_path=src_dir,
                    original_name=candidate_name,
                    canonical_name=final_name,
                    runtime_name=runtime_name,
                    decision="ROLLBACK",
                    category=cat,
                    subcategory=subcat,
                    canonical_path=canonical_rel if is_update else "",
                    functional_parent=router_rel if is_update else "",
                    validation_status=val_st,
                    pilot_status=pilot_st,
                )
            except Exception:
                pass

            # Cleanup temporary backups
            shutil.rmtree(backup_candidate_dir, ignore_errors=True)
            if backup_canonical_dir:
                shutil.rmtree(backup_canonical_dir, ignore_errors=True)

        try:
            # Step C: Deploy to Canonical Library
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
            if is_update and os.path.exists(target_dir):
                for item in os.listdir(target_dir):
                    item_p = os.path.join(target_dir, item)
                    if os.path.isdir(item_p):
                        shutil.rmtree(item_p)
                    else:
                        os.unlink(item_p)
                for item in os.listdir(src_dir):
                    s_item = os.path.join(src_dir, item)
                    d_item = os.path.join(target_dir, item)
                    if os.path.isdir(s_item):
                        shutil.copytree(s_item, d_item)
                    else:
                        shutil.copy2(s_item, d_item)
            else:
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                shutil.copytree(src_dir, target_dir)

            # Step D: Update Router if new skill
            if not is_update:
                add_link_to_router(
                    router_path=router_path,
                    skill_name=final_name,
                    skill_dir_path=target_dir,
                    subcategory=subcat,
                    description=desc,
                )

            # Step E: Update Manifest
            m.add_skill(
                runtime_name=runtime_name,
                canonical_name=final_name,
                canonical_path=canonical_rel,
                functional_parent=router_rel,
                source="intake",
                managed=True,
            )
            m.save()

            # Step F: Execute Post-Install Validation & Targeted Pilot Checks
            val_res = validate_single_skill(target_dir)
            val_status = "PASS" if val_res.is_valid else "FAIL"

            pilot_res = run_targeted_pilot(target_dir, router_path)
            pilot_status = "PASS" if pilot_res.passed else "FAIL"

            if val_status != "PASS" or pilot_status != "PASS":
                reasons = []
                if val_status != "PASS":
                    reasons.append(f"Validation failed ({'; '.join(val_res.errors)})")
                if pilot_status != "PASS":
                    reasons.append(f"Pilot failed ({'; '.join(pilot_res.errors)})")
                err_msg = (
                    f"Candidate '{candidate_name}' failed post-install checks: {', '.join(reasons)}. "
                    f"All canonical and runtime changes rolled back successfully."
                )
                _do_rollback(val_st=val_status, pilot_st=pilot_status)
                raise RuntimeError(err_msg)

        except Exception as e:
            if os.path.exists(backup_candidate_dir):
                _do_rollback(val_st="FAIL", pilot_st="NOT_RUN")
            raise

        # Step I: Success! Clean candidate from intake and record in ledger
        if os.path.exists(src_dir):
            shutil.rmtree(src_dir)

        lg = ledger or ChangeLedger()
        lg.record_change(
            operation=operation,
            source="intake",
            source_path=src_dir,
            original_name=candidate_name,
            canonical_name=final_name,
            runtime_name=runtime_name,
            decision=decision,
            category=cat,
            subcategory=subcat,
            canonical_path=canonical_rel,
            functional_parent=router_rel,
            validation_status=val_status,
            pilot_status=pilot_status,
        )

        shutil.rmtree(backup_candidate_dir, ignore_errors=True)
        if backup_canonical_dir:
            shutil.rmtree(backup_canonical_dir, ignore_errors=True)

    return {
        "candidate_name": candidate_name,
        "canonical_name": final_name,
        "runtime_name": runtime_name,
        "runtime_symlink": runtime_item_path,
        "operation": operation,
        "target_directory": target_dir,
        "router_updated": router_path,
        "is_update": is_update,
    }
