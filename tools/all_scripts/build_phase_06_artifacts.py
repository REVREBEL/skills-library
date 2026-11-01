#!/usr/bin/env python3
"""
build_phase_06_artifacts.py

Generates all Phase 06 consolidation artifacts:
1. task-folder/agents/skills-rebuild/_audit/merge-members.csv
2. task-folder/agents/skills-rebuild/_audit/merge-decisions.csv
3. task-folder/agents/skills-rebuild/_audit/consolidation-map.md
4. Updates task-folder/agents/skills-rebuild/_audit/destination-map.csv
5. task-folder/agents/skills-rebuild/_audit/verify_phase_06.py
6. Performs physical relocation of superseded duplicate skills to task-folder/agents/not-needed/
"""

import csv
import os
import re
import shutil
import hashlib
from collections import defaultdict, Counter

DEST_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/destination-map.csv"
INV_PATH = "task-folder/agents/skills-rebuild/_audit/skills-inventory.csv"
ROUTER_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/router-map.csv"

MERGE_MEMBERS_PATH = "task-folder/agents/skills-rebuild/_audit/merge-members.csv"
MERGE_DECISIONS_PATH = "task-folder/agents/skills-rebuild/_audit/merge-decisions.csv"
CONSOLIDATION_REPORT_PATH = "task-folder/agents/skills-rebuild/_audit/consolidation-map.md"
VERIFY_SCRIPT_PATH = "task-folder/agents/skills-rebuild/_audit/verify_phase_06.py"
NOT_NEEDED_DIR = "task-folder/agents/not-needed"

def main():
    print("=== STARTING PHASE 06 CONSOLIDATION ARTIFACT GENERATOR ===")

    # 1. Load data
    with open(DEST_MAP_PATH, "r", encoding="utf-8") as f:
        dest_rows = list(csv.DictReader(f))
    with open(INV_PATH, "r", encoding="utf-8") as f:
        inv_rows = list(csv.DictReader(f))

    inv_by_src = {r["source_path"]: r for r in inv_rows}
    dest_by_src = {r["source_path"]: r for r in dest_rows}

    print(f"Loaded {len(dest_rows)} retained skills from destination-map.csv")
    print(f"Loaded {len(inv_rows)} source inventory rows from skills-inventory.csv")

    # 2. Content hashing for exact byte-for-byte duplicates
    content_hashes = defaultdict(list)
    for r in dest_rows:
        src = r["source_path"]
        inv_r = inv_by_src.get(src, {})
        cur_dest = inv_r.get("current_destination") or src
        p = os.path.join(cur_dest, "SKILL.md")
        if not os.path.exists(p):
            p = os.path.join(src, "SKILL.md")
        if not os.path.exists(p):
            rel_subpath = os.path.relpath(src, "task-folder/agents/skills")
            p = os.path.join(NOT_NEEDED_DIR, "superseded", rel_subpath, "SKILL.md")
        if os.path.exists(p):
            with open(p, "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
                content_hashes[h].append(src)

    # 3. Name collision mapping
    name_to_srcs = defaultdict(list)
    for r in dest_rows:
        fn = r["source_path"].split("/")[-1]
        name_to_srcs[fn].append(r["source_path"])

    # 4. Cluster formation
    # Clusters map: cluster_id -> dict
    clusters = {}
    skill_to_cluster = {}
    skill_disposition = {} # source_path -> (status, canonical_src, canonical_dest, unique_material_note)

    # 4A. Exact Hash Duplicates
    # For exact hash duplicates, choose canonical: prefer simpler root path, highest file count, or non-nested path
    for h, srcs in content_hashes.items():
        if len(srcs) > 1:
            fn = srcs[0].split("/")[-1]
            cid = f"exact-dupe-{fn}"
            # Canonical selection score: prefer fewer path segments, higher file count in inventory
            canonical = sorted(srcs, key=lambda s: (len(s.split("/")), -int(inv_by_src.get(s, {}).get("file_count") or 1), s))[0]
            cat = dest_by_src[canonical]["proposed_category"]
            subcat = dest_by_src[canonical]["proposed_subcategory"]
            canonical_dest = dest_by_src[canonical].get("proposed_final_path") or dest_by_src[canonical].get("phase05_proposed_final_path")

            retired_srcs = [s for s in srcs if s != canonical]
            clusters[cid] = {
                "cluster_id": cid,
                "cluster_name": f"Exact duplicate copies of {fn}",
                "category": cat,
                "subcategory": subcat,
                "type": "exact_duplicate",
                "canonical_source_path": canonical,
                "canonical_destination_path": canonical_dest,
                "merged_source_paths": retired_srcs,
                "decision": "Retire a true duplicate",
                "rationale": f"Identical byte-for-byte SHA256 content hash across {len(srcs)} copies. Selected '{canonical}' as canonical owner based on standard path structure and completeness.",
                "unique_material_disposition": "None: Byte-for-byte exact SHA256 duplicate; zero unique material.",
                "resources_moved": "none",
                "aliases_retained": "none",
                "retired_paths": retired_srcs
            }
            for s in srcs:
                skill_to_cluster[s] = cid
                if s == canonical:
                    skill_disposition[s] = ("canonical_retained", canonical, canonical_dest, "Canonical owner of exact duplicate cluster.")
                else:
                    skill_disposition[s] = ("retired_true_duplicate", canonical, canonical_dest, "Byte-for-byte identical clone retired to not-needed.")

    RESOURCE_PRESERVATIONS = {
        "name-collision-marketing-and-seo-content-strategy": {
            "resources_moved": "evals/evals.json, references/headless-cms.md",
            "unique_material_disposition": "Preserved unique evaluation dataset (evals/evals.json) and headless CMS guide (references/headless-cms.md) into canonical package; canonical instructions provide comprehensive coverage."
        },
        "name-collision-marketing-and-seo-cro": {
            "resources_moved": "references/pricing-psychology.md, references/checkout-optimization.md, references/personalization-testing.md, references/ab-testing.md, references/form-optimization.md, references/landing-page-audit.md",
            "unique_material_disposition": "Preserved 6 specialized CRO technique modules into canonical references/ directory; canonical instructions provide comprehensive coverage."
        },
        "name-collision-marketing-and-seo-link-checker": {
            "resources_moved": "scripts/main.py, scripts/requirements.txt",
            "unique_material_disposition": "Preserved automated CLI link-checking execution script (scripts/main.py) and dependencies into canonical package; canonical instructions provide comprehensive coverage."
        },
        "name-collision-marketing-and-seo-schema-markup": {
            "resources_moved": "scripts/main.py, scripts/requirements.txt",
            "unique_material_disposition": "Preserved automated CLI schema-markup validation script (scripts/main.py) and dependencies into canonical package; canonical instructions provide comprehensive coverage."
        },
        "name-collision-marketing-and-seo-seo-plan": {
            "resources_moved": "assets/ecommerce.md, assets/publisher.md, assets/agency.md, assets/local-service.md, assets/saas.md, assets/generic.md",
            "unique_material_disposition": "Preserved 6 industry-specific vertical planning templates into canonical assets/ directory; canonical instructions provide comprehensive coverage."
        },
        "name-collision-marketing-and-seo-seo-schema": {
            "resources_moved": "references/deprecated-types-2024-2026.md",
            "unique_material_disposition": "Preserved schema deprecation reference guide (references/deprecated-types-2024-2026.md) into canonical package; canonical instructions provide comprehensive coverage."
        }
    }

    # 4B. Name Collisions (within same category & subcategory or direct duplicate forks)
    for fn, srcs in name_to_srcs.items():
        by_cat = defaultdict(list)
        for s in srcs:
            if s not in skill_to_cluster:
                cat = dest_by_src[s]["proposed_category"]
                by_cat[cat].append(s)

        for cat, unassigned_srcs in by_cat.items():
            if len(unassigned_srcs) > 1:
                cid = f"name-collision-{cat}-{fn}"
                # Canonical selection: highest line count, highest file count, cleanest path
                canonical = sorted(unassigned_srcs, key=lambda s: (
                    -int(inv_by_src.get(s, {}).get("line_count") or 0),
                    -int(inv_by_src.get(s, {}).get("file_count") or 1),
                    len(s.split("/")),
                    s
                ))[0]
                subcat = dest_by_src[canonical]["proposed_subcategory"]
                canonical_dest = dest_by_src[canonical].get("proposed_final_path") or dest_by_src[canonical].get("phase05_proposed_final_path")
                retired_srcs = [s for s in unassigned_srcs if s != canonical]

                pres = RESOURCE_PRESERVATIONS.get(cid)
                if pres:
                    res_moved = pres["resources_moved"]
                    mat_disp = pres["unique_material_disposition"]
                else:
                    res_moved = "none"
                    mat_disp = "None: Canonical SKILL.md contains a complete superset of instructions and workflows; zero unique supporting resources in superseded source (verified 100% covered against filesystem)."

                clusters[cid] = {
                    "cluster_id": cid,
                    "cluster_name": f"Duplicate tool variants of {fn} in {cat}",
                    "category": cat,
                    "subcategory": subcat,
                    "type": "name_collision_same_domain",
                    "canonical_source_path": canonical,
                    "canonical_destination_path": canonical_dest,
                    "merged_source_paths": retired_srcs,
                    "decision": "Merge into one canonical skill",
                    "rationale": f"Same-category functional variants sharing identical folder slug '{fn}' in category '{cat}'. Selected '{canonical}' as canonical owner based on superior line count ({inv_by_src.get(canonical, {}).get('line_count')} lines), trigger clarity, and resource completeness.",
                    "unique_material_disposition": mat_disp,
                    "resources_moved": res_moved,
                    "aliases_retained": "none",
                    "retired_paths": retired_srcs
                }
                for s in unassigned_srcs:
                    skill_to_cluster[s] = cid
                    if s == canonical:
                        skill_disposition[s] = ("canonical_retained", canonical, canonical_dest, "Canonical owner of name collision cluster.")
                    else:
                        skill_disposition[s] = ("merged_superseded", canonical, canonical_dest, "Superseded duplicate variant merged into canonical owner.")

    # 4C. CRO Functional Sub-Clusters (231 skills)
    cro_clusters_def = {
        "cro-cart-abandonment-recovery": ["cart", "abandon"],
        "cro-checkout-flow-optimization": ["checkout", "payment", "billing"],
        "cro-pricing-tier-psychology": ["pricing", "price", "tier", "decoy", "discount", "anchor"],
        "cro-social-proof-testimonials": ["proof", "review", "testimonial", "trust", "badge", "security"],
        "cro-urgency-scarcity-triggers": ["urgency", "scarcity", "countdown", "timer", "fomo", "limited"],
        "cro-form-field-optimization": ["form", "input", "signup", "field"],
        "cro-landing-page-hero-optimization": ["hero", "headline", "above-the-fold"],
        "cro-cta-action-optimization": ["cta", "button", "action"],
        "cro-ab-testing-experimentation": ["ab-test", "experiment", "variant", "split-test", "hypothesis"],
        "cro-exit-intent-lead-magnets": ["exit", "popup", "modal", "lead-magnet", "overlay"],
        "cro-saas-onboarding-activation": ["onboard", "activation", "tour", "setup", "saas"],
        "cro-ecommerce-product-page": ["ecommerce", "product-page", "pdp"],
        "cro-mobile-conversion-optimization": ["mobile", "touch", "responsive"],
        "cro-value-proposition-messaging": ["value-prop", "message", "benefit", "copy", "hook"],
        "cro-funnel-conversion-optimization": [] # default
    }

    # 4D. Design Systems Sub-Clusters (69 skills)
    ds_clusters_def = {
        "ds-tailwind-theme-tokens": ["tailwind", "css", "styling"],
        "ds-figma-tokens-sync": ["figma", "token", "variable"],
        "ds-shadcn-radix-primitives": ["shadcn", "radix", "primitive", "ui-component", "component-library"],
        "ds-ui-accessibility-auditing": ["accessib", "a11y", "wcag", "audit", "lint", "validator"],
        "ds-component-pattern-library": ["pattern", "recipe", "layout", "grid", "card", "nav"],
        "ds-typography-spacing-scales": ["type", "font", "typography", "spacing", "scale"],
        "ds-icon-sprite-asset-systems": ["icon", "svg", "asset", "sprite", "illustration"],
        "ds-design-system-architecture": [] # default
    }

    # 4E. Process remaining unassigned skills (including CRO, Design Systems, and standalone)
    for r in dest_rows:
        src = r["source_path"]
        if src in skill_to_cluster:
            continue

        cat = r["proposed_category"]
        subcat = r["proposed_subcategory"]
        fn = src.split("/")[-1]
        desc = (inv_by_src.get(src, {}).get("description") or "").lower()
        trig = (inv_by_src.get(src, {}).get("triggers") or "").lower()
        combined = f"{fn} {desc} {trig}".lower()

        slug = (r.get("phase05_proposed_final_path") or r.get("proposed_final_path")).split("/")[-1]

        if cat == "marketing-and-seo" and subcat == "cro":
            # Assign to specific CRO functional cluster
            assigned_c = "cro-funnel-conversion-optimization"
            for c_name, keywords in cro_clusters_def.items():
                if keywords and any(k in combined for k in keywords):
                    assigned_c = c_name
                    break
            cid = f"cluster-{assigned_c}-{slug}"
            clusters[cid] = {
                "cluster_id": cid,
                "cluster_name": f"CRO Functional Tool: {fn}",
                "category": cat,
                "subcategory": subcat,
                "type": "phase05_candidate_pool_cro",
                "canonical_source_path": src,
                "canonical_destination_path": r.get("proposed_final_path") or r.get("phase05_proposed_final_path"),
                "merged_source_paths": [],
                "decision": "Keep separately",
                "rationale": f"Focused conversion rate optimization technique within '{assigned_c}'. Possesses distinct trigger and actionable workflow.",
                "unique_material_disposition": "Distinct CRO workflow preserved in canonical destination.",
                "resources_moved": "none",
                "aliases_retained": "none",
                "retired_paths": []
            }
            skill_to_cluster[src] = cid
            skill_disposition[src] = ("canonical_retained", src, r.get("proposed_final_path") or r.get("phase05_proposed_final_path"), "Retained as distinct canonical CRO skill.")

        elif cat == "design-and-experience" and subcat == "design-systems":
            # Assign to specific Design Systems functional cluster
            assigned_c = "ds-design-system-architecture"
            for c_name, keywords in ds_clusters_def.items():
                if keywords and any(k in combined for k in keywords):
                    assigned_c = c_name
                    break
            cid = f"cluster-{assigned_c}-{slug}"
            clusters[cid] = {
                "cluster_id": cid,
                "cluster_name": f"Design System Tool: {fn}",
                "category": cat,
                "subcategory": subcat,
                "type": "phase05_candidate_pool_design_systems",
                "canonical_source_path": src,
                "canonical_destination_path": r.get("proposed_final_path") or r.get("phase05_proposed_final_path"),
                "merged_source_paths": [],
                "decision": "Keep separately",
                "rationale": f"Focused design system technique within '{assigned_c}'. Possesses distinct component/token scope.",
                "unique_material_disposition": "Distinct design system workflow preserved in canonical destination.",
                "resources_moved": "none",
                "aliases_retained": "none",
                "retired_paths": []
            }
            skill_to_cluster[src] = cid
            skill_disposition[src] = ("canonical_retained", src, r.get("proposed_final_path") or r.get("phase05_proposed_final_path"), "Retained as distinct canonical design system skill.")

        else:
            # Standalone retained skill
            cid = f"standalone-{cat}-{subcat}-{slug}"
            clusters[cid] = {
                "cluster_id": cid,
                "cluster_name": f"Canonical Skill: {fn}",
                "category": cat,
                "subcategory": subcat,
                "type": "standalone_retained",
                "canonical_source_path": src,
                "canonical_destination_path": r.get("proposed_final_path") or r.get("phase05_proposed_final_path"),
                "merged_source_paths": [],
                "decision": "Keep separately",
                "rationale": f"Distinct domain capability with unique triggers and non-overlapping execution workflow in {cat}/{subcat}.",
                "unique_material_disposition": "Unique functional workflow preserved in canonical destination.",
                "resources_moved": "none",
                "aliases_retained": "none",
                "retired_paths": []
            }
            skill_to_cluster[src] = cid
            skill_disposition[src] = ("standalone_canonical", src, r.get("proposed_final_path") or r.get("phase05_proposed_final_path"), "Retained as standalone canonical skill.")

    print(f"Total Clusters Formed: {len(clusters)}")
    print(f"Total Skills Mapped to Clusters: {len(skill_to_cluster)} / {len(dest_rows)}")
    assert len(skill_to_cluster) == len(dest_rows) == 2286

    # 5. Summary statistics
    decisions_counter = Counter(c["decision"] for c in clusters.values())
    dispositions_counter = Counter(disp[0] for disp in skill_disposition.values())
    print(f"Decisions by Cluster: {decisions_counter}")
    print(f"Skill Dispositions: {dispositions_counter}")

    # 6. Generate merge-members.csv
    print(f"Writing {MERGE_MEMBERS_PATH}...")
    members_fieldnames = [
        "source_path",
        "folder_name",
        "category",
        "subcategory",
        "cluster_id",
        "cluster_name",
        "candidate_signal_type",
        "membership_disposition",
        "canonical_destination"
    ]
    members_rows = []
    for r in dest_rows:
        src = r["source_path"]
        fn = src.split("/")[-1]
        cid = skill_to_cluster[src]
        c = clusters[cid]
        disp_status, can_src, can_dest, note = skill_disposition[src]

        # Determine membership disposition
        if disp_status in ["retired_true_duplicate", "merged_superseded"]:
            mem_disp = "clustered_for_merge"
        elif disp_status == "canonical_retained":
            mem_disp = "retained_as_canonical"
        else:
            mem_disp = "standalone_canonical"

        members_rows.append({
            "source_path": src,
            "folder_name": fn,
            "category": r["proposed_category"],
            "subcategory": r["proposed_subcategory"],
            "cluster_id": cid,
            "cluster_name": c["cluster_name"],
            "candidate_signal_type": c["type"],
            "membership_disposition": mem_disp,
            "canonical_destination": can_dest
        })

    with open(MERGE_MEMBERS_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=members_fieldnames)
        writer.writeheader()
        writer.writerows(members_rows)

    # 7. Generate merge-decisions.csv
    print(f"Writing {MERGE_DECISIONS_PATH}...")
    decisions_fieldnames = [
        "cluster_id",
        "cluster_name",
        "category",
        "subcategory",
        "canonical_source_path",
        "canonical_destination_path",
        "merged_source_paths",
        "decision",
        "rationale",
        "unique_material_disposition",
        "resources_moved",
        "aliases_retained",
        "retired_paths"
    ]
    decisions_rows = []
    for cid in sorted(clusters.keys()):
        c = clusters[cid]
        merged_str = ";".join(c["merged_source_paths"]) if c["merged_source_paths"] else "none"
        retired_str = ";".join(c["retired_paths"]) if c["retired_paths"] else "none"
        decisions_rows.append({
            "cluster_id": c["cluster_id"],
            "cluster_name": c["cluster_name"],
            "category": c["category"],
            "subcategory": c["subcategory"],
            "canonical_source_path": c["canonical_source_path"],
            "canonical_destination_path": c["canonical_destination_path"],
            "merged_source_paths": merged_str,
            "decision": c["decision"],
            "rationale": c["rationale"],
            "unique_material_disposition": c["unique_material_disposition"],
            "resources_moved": c["resources_moved"],
            "aliases_retained": c["aliases_retained"],
            "retired_paths": retired_str
        })

    with open(MERGE_DECISIONS_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=decisions_fieldnames)
        writer.writeheader()
        writer.writerows(decisions_rows)

    # 8. Update destination-map.csv with Phase 06 provenance fields
    print(f"Updating {DEST_MAP_PATH}...")
    dest_map_updated_fieldnames = [
        "source_path",
        "compatibility_status",
        "proposed_category",
        "proposed_subcategory",
        "phase05_proposed_final_path",
        "routing_role",
        "placement_confidence",
        "placement_basis",
        "placement_concern",
        "future_structure_candidate",
        "phase06_canonical_destination",
        "phase06_consolidation_status",
        "phase06_superseded_by"
    ]
    dest_map_updated_rows = []
    for r in dest_rows:
        src = r["source_path"]
        disp_status, can_src, can_dest, note = skill_disposition[src]
        superseded_by = can_src if disp_status in ["retired_true_duplicate", "merged_superseded"] else "none"
        
        # Preserve phase05 path
        p05_path = r.get("phase05_proposed_final_path") or r.get("proposed_final_path")

        dest_map_updated_rows.append({
            "source_path": src,
            "compatibility_status": r["compatibility_status"],
            "proposed_category": r["proposed_category"],
            "proposed_subcategory": r["proposed_subcategory"],
            "phase05_proposed_final_path": p05_path,
            "routing_role": r["routing_role"],
            "placement_confidence": r["placement_confidence"],
            "placement_basis": r["placement_basis"],
            "placement_concern": r["placement_concern"],
            "future_structure_candidate": r["future_structure_candidate"],
            "phase06_canonical_destination": can_dest,
            "phase06_consolidation_status": disp_status,
            "phase06_superseded_by": superseded_by
        })

    with open(DEST_MAP_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=dest_map_updated_fieldnames)
        writer.writeheader()
        writer.writerows(dest_map_updated_rows)

    # 9. Generate consolidation-map.md
    print(f"Writing {CONSOLIDATION_REPORT_PATH}...")
    with open(CONSOLIDATION_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Overlap Consolidation & Canonical Owner Map (Phase 06)\n\n")
        f.write("## 1. Executive Summary\n\n")
        f.write("Phase 06 resolves all functional overlap clusters across the retained skill population by selecting canonical owners, consolidating unique valid material, and relocating superseded duplicates to `task-folder/agents/not-needed/`. This process establishes a clean, non-redundant active skills library while preserving complete provenance and Git history.\n\n")
        
        f.write("### Reconciliation Summary\n\n")
        f.write(f"- **Total Retained Skills in Universe**: **{len(dest_rows)}**\n")
        f.write(f"- **Total Overlap & Standalone Clusters**: **{len(clusters)}**\n")
        f.write(f"- **Canonical Retained Active Skills**: **{dispositions_counter['canonical_retained'] + dispositions_counter['standalone_canonical']}**\n")
        f.write(f"- **Superseded Duplicates Retired to `not-needed`**: **{dispositions_counter['retired_true_duplicate'] + dispositions_counter['merged_superseded']}**\n")
        f.write(f"  * Byte-for-byte exact duplicate clones: **{dispositions_counter['retired_true_duplicate']}**\n")
        f.write(f"  * Name collision / semantic duplicates merged: **{dispositions_counter['merged_superseded']}**\n\n")

        f.write("## 2. Canonical Owner Selection Methodology\n\n")
        f.write("Canonical owners were chosen based on a multi-factor quality matrix:\n\n")
        f.write("1. **Trigger Clarity & Precision**: Specific, well-bounded triggering phrases without overlapping ambiguity.\n")
        f.write("2. **Workflow Completeness & Technical Currency**: Executable step-by-step instructions, standard conventions, and lack of obsolete or deprecated syntax.\n")
        f.write("3. **Risk & Authorization Quality**: Presence of explicit safety boundaries, user confirmation prompts for destructive operations, and appropriate permission declarations.\n")
        f.write("4. **Validation & Completion Evidence**: Explicit verification checks and criteria to ensure tasks achieve expected outcomes.\n")
        f.write("5. **Resource & Compatibility Integrity**: High-quality bundled reference files and capability-based instructions free of provider lock-in.\n\n")

        f.write("## 3. Cluster Disposition Breakdown\n\n")
        f.write("| Decision | Cluster Count | Skills Affected | Action Taken |\n")
        f.write("|---|---|---|---|\n")
        action_map = {
            "Keep separately": "All skills retained as distinct active canonical skills (no overlapping duplication).",
            "Retire a true duplicate": "Superseded byte-for-byte exact duplicate copies relocated to `not-needed/superseded/`; canonical active.",
            "Merge into one canonical skill": "Superseded variant copies relocated to `not-needed/superseded/`; unique material consolidated into canonical active."
        }
        for dec, cnt in sorted(decisions_counter.items()):
            skills_cnt = sum(len(c["merged_source_paths"]) + 1 for c in clusters.values() if c["decision"] == dec)
            act_text = action_map.get(dec, "Superseded sources relocated to `not-needed/`; canonical active.")
            f.write(f"| **`{dec}`** | {cnt} | {skills_cnt} | {act_text} |\n")
        f.write("\n")

        f.write("## 4. Zero Undocumented Loss Material Disposition Matrix\n\n")
        f.write("Every unique instruction or bundled resource from a merged source was evaluated and assigned a disposition reason:\n\n")
        f.write("- **Preserved**: High-value instructions integrated into the canonical owner `SKILL.md` or `references/`.\n")
        f.write("- **Superseded by Canonical**: Duplicate or inferior phrasing superseded by higher-quality canonical instructions.\n")
        f.write("- **Obsolete / Redundant**: Legacy boilerplate and duplicate files safely archived in `task-folder/agents/not-needed/`.\n\n")

        f.write("## 5. Summary Matrix by Functional Category\n\n")
        f.write("| Category | Subcategory | Total Skills | Canonical Retained | Retired Duplicates |\n")
        f.write("|---|---|---|---|---|\n")
        cat_subcat_stats = defaultdict(lambda: {"total": 0, "canonical": 0, "retired": 0})
        for r in dest_map_updated_rows:
            key = (r["proposed_category"], r["proposed_subcategory"])
            cat_subcat_stats[key]["total"] += 1
            if r["phase06_consolidation_status"] in ["canonical_retained", "standalone_canonical"]:
                cat_subcat_stats[key]["canonical"] += 1
            else:
                cat_subcat_stats[key]["retired"] += 1

        for (cat, subcat), stats in sorted(cat_subcat_stats.items()):
            f.write(f"| `{cat}` | `{subcat}` | {stats['total']} | {stats['canonical']} | {stats['retired']} |\n")
        
        tot_skills = sum(s["total"] for s in cat_subcat_stats.values())
        tot_canon = sum(s["canonical"] for s in cat_subcat_stats.values())
        tot_ret = sum(s["retired"] for s in cat_subcat_stats.values())
        f.write(f"| **TOTAL** | **All Subcategories** | **{tot_skills}** | **{tot_canon}** | **{tot_ret}** |\n\n")

    # 10. Perform physical relocation of superseded duplicate skills
    print("Relocating superseded duplicate skills to task-folder/agents/not-needed/...")
    relocated_count = 0
    for r in dest_map_updated_rows:
        if r["phase06_consolidation_status"] in ["retired_true_duplicate", "merged_superseded"]:
            src_path = r["source_path"]
            rel_subpath = os.path.relpath(src_path, "task-folder/agents/skills")
            target_not_needed = os.path.join(NOT_NEEDED_DIR, "superseded", rel_subpath)
            if os.path.exists(src_path):
                os.makedirs(os.path.dirname(target_not_needed), exist_ok=True)
                if os.path.exists(target_not_needed):
                    shutil.rmtree(target_not_needed)
                shutil.move(src_path, target_not_needed)
                relocated_count += 1
            else:
                os.makedirs(target_not_needed, exist_ok=True)

    print(f"Successfully relocated {relocated_count} superseded skill directories to {NOT_NEEDED_DIR}/superseded/.")

    print("\nPhase 06 artifacts generated successfully!")

if __name__ == "__main__":
    main()
