#!/usr/bin/env python3
import csv
import os
import math

REGISTRY_PATH = "task-folder/agents/skills-rebuild/_audit/phase08-canonical-registry.csv"
BATCH_PLAN_PATH = "task-folder/agents/skills-rebuild/_audit/phase08-batch-plan.csv"
DEST_MAP_PATH = "task-folder/agents/skills-rebuild/_audit/destination-map.csv"

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    reg_rows = list(csv.DictReader(f))

# Group by category and subcategory
groups = {}
for r in reg_rows:
    cat = r["proposed_category"]
    sc = r["proposed_subcategory"]
    key = (cat, sc)
    if key not in groups:
        groups[key] = []
    groups[key].append(r)

batches = []
batch_counter = 1

# Process each subcategory group
for (cat, sc), members in sorted(groups.items()):
    members.sort(key=lambda x: x["canonical_skill_name"])
    total_m = len(members)
    
    if total_m <= 20:
        # Single batch
        slug = f"{cat}-{sc}"
        if slug == "workflow-and-automation-tool-integration":
            batch_id = "batch-01-workflow-and-automation-tool-integration"
            status = "completed"
            branch = "skills-rebuild/phase-08-canonical-rewrites"
            pr = "https://github.com/REVREBEL/skills-rebuild/pull/78"
            chk_commit = "303b0e81"
            merge_commit = "303b0e81"
            val_status = "verified"
        else:
            batch_counter += 1
            batch_id = f"batch-{batch_counter:02d}-{slug}"
            status = "pending"
            branch = f"phase-08/{batch_id}"
            pr = "pending"
            chk_commit = "pending"
            merge_commit = "pending"
            val_status = "pending"
            
        batches.append({
            "batch_id": batch_id,
            "category": cat,
            "subcategory": sc,
            "member_count": total_m,
            "member_paths": ";".join([m["origin_path"] for m in members]),
            "status": status,
            "batch_branch": branch,
            "batch_pr": pr,
            "checkpoint_commit": chk_commit,
            "integration_merge_commit": merge_commit,
            "validation_status": val_status,
            "_members": members
        })
    else:
        # Partition into chunks between 12 and 18 skills
        target_size = 15
        num_chunks = math.ceil(total_m / target_size)
        chunk_size = math.ceil(total_m / num_chunks)
        
        for i in range(num_chunks):
            chunk = members[i*chunk_size : (i+1)*chunk_size]
            if not chunk:
                continue
            batch_counter += 1
            part_id = i + 1
            slug = f"{cat}-{sc}-part{part_id:02d}"
            batch_id = f"batch-{batch_counter:02d}-{slug}"
            
            batches.append({
                "batch_id": batch_id,
                "category": cat,
                "subcategory": sc,
                "member_count": len(chunk),
                "member_paths": ";".join([m["origin_path"] for m in chunk]),
                "status": "pending",
                "batch_branch": f"phase-08/{batch_id}",
                "batch_pr": "pending",
                "checkpoint_commit": "pending",
                "integration_merge_commit": "pending",
                "validation_status": "pending",
                "_members": chunk
            })

# Verify total member count matches 2,103
total_partitioned = sum(b["member_count"] for b in batches)
print(f"Total batches planned: {len(batches)}")
print(f"Total skills covered across all batches: {total_partitioned}")
assert total_partitioned == 2103, f"Mismatch: expected 2103, got {total_partitioned}"

# Write phase08-batch-plan.csv
fieldnames = [
    "batch_id", "category", "subcategory", "member_count", "member_paths",
    "status", "batch_branch", "batch_pr", "checkpoint_commit",
    "integration_merge_commit", "validation_status"
]

with open(BATCH_PLAN_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for b in batches:
        row = {k: b[k] for k in fieldnames}
        writer.writerow(row)

print(f"Wrote {BATCH_PLAN_PATH} successfully with {len(batches)} batches.")
