# Task 07: Split Oversized Skills (Hardened & Refined Specification)

## Objective

Split retained skills only when they contain independently triggered jobs with different workflows, tools, outputs, risks, or validation paths.

## Preconditions

- Inventory, taxonomy, destination, consolidation, and merge-decision artifacts exist and reconcile.
- `.agents/skills` is the verified canonical task-workflow path.
- Canonical owners for overlap clusters are established.
- Candidate skills have been reviewed for true multi-job behavior rather than length alone.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-library-restructure/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-writer/SKILL.md`

Use `skill-review` for split approval, `skill-library-restructure` for parent-child architecture and destination updates, and `skill-writer` for substantial source-backed child or router authoring. Use `.agents/skills/github-operations/SKILL.md` for repository operations and reviewable publication batches.

---

## 1. Candidate Screening & Review Ledger Architecture

### A. 100% Screening Coverage Ledger (`split-decisions.csv`)
To prevent candidate loss between initial screening and deep review, **all 2,094 Phase 06 active canonical skills** are indexed in `split-decisions.csv` with the following schema:
- `source_path`: Canonical source path from Phase 06.
- `canonical_name`: Skill folder/frontmatter name.
- `category`: Functional category (from 10x44 taxonomy).
- `subcategory`: Functional subcategory.
- `lines`: Line count of `SKILL.md`.
- `bytes`: File size of `SKILL.md`.
- `screening_status`: `not_candidate` or `screened_candidate`.
- `candidate_signals`: Specific triggers (e.g. `lines >= 400`, `modes >= 3`, `subcommands >= 3`, `fsc == router_candidate`).
- `requires_deep_review`: `true` or `false`.
- `review_status`: `screened_out`, `deep_reviewed`, or `deferred`.
- `split_decision`: Explicit decision from the approved taxonomy.
- `rationale`: Comprehensive rationale for the decision.
- `parent_router_path`: Path of the thin parent router (if applicable).
- `child_destination_paths`: Semicolon-separated list of created child skill paths.
- `retired_source_path`: Path where monolithic source is quarantined in `task-folder/agents/not-needed/superseded/` (if split).
- `content_allocation_count`: Number of sections/files mapped in the content ledger.
- `resources_moved`: Preserved bundled resources.

### B. 5-Option Split Decision Taxonomy
Every skill in `split-decisions.csv` receives one of 5 mutually exclusive decisions:
1. **`Split into child skills with parent router`**: Multi-job skill decomposed into >= 2 focused execution children coordinated by a thin parent category router.
2. **`Split into standalone child skills`**: Multi-job skill decomposed into >= 2 independent child skills without requiring a dedicated router.
3. **`Retain as singular skill with references`**: Singular job with extensive documentation; non-workflow reference details extracted to `references/`.
4. **`Retain as singular skill without modification`**: Singular job already cohesive and focused.
5. **`Defer for manual review`**: Complex or ambiguous trigger/domain boundary requiring manual domain review before splitting. Skill remains active and untouched, with documented ambiguities.

---

## 2. Parent-Child Architecture & Default Path Conventions

### A. Default Parent-Router Pattern (Family Cohesion)
When a multi-job monolith is split into a coherent skill family:
1. **Original Canonical Path**: Converted into a **thin parent router** containing:
   - Routing decision table / trigger matrix.
   - Category-wide policies, prerequisites, and shared limitations.
   - **Zero** duplicated child execution workflows or inline scripts.
2. **Original Monolithic Contents**: Archived and relocated to `task-folder/agents/not-needed/superseded/<category>/<skill-name>/` to preserve complete audit history without polluting discovery.
3. **Focused Children**: Created as dedicated child skill packages (e.g., `<original-path>/<child-job>/` or sibling folders) adhering to `.agents/skills/skills-create-manage-update/skill-writer/SKILL.md`.

### B. Standalone Children Pattern (Unrelated Jobs)
When a monolith contains completely disjoint, unrelated capabilities:
1. **Original Path**: Fully retired and moved to `task-folder/agents/not-needed/superseded/`.
2. **Standalone Children**: Created at their respective functional destination paths without a parent router.

---

## 3. Section & Package-Level Material Accounting

For every approved split, a deterministic content allocation ledger is recorded in `task-folder/agents/skills-rebuild/_audit/split-map.md` and `task-folder/agents/skills-rebuild/_audit/split-allocations.csv`:
- `source_path`: Monolith source path.
- `section_or_file`: Section heading (e.g., `## Developer Environments`) or bundled file path (e.g., `tools/src/op-env-create.ts`).
- `disposition`: One of:
  - `child`: Moved to specific child skill.
  - `parent-shared-policy`: General policy/preflight preserved in parent router.
  - `reference`: Extracted to `references/<topic>.md`.
  - `duplicate`: Redundant boilerplate subsumed by child/parent.
  - `obsolete`: Obsolete instruction retired with rationale.
  - `retired-with-rationale`: Explicitly retired with evidence.
- `destination`: Specific destination file/section path.
- `rationale`: Non-trivial explanation of allocation decision.
- `validation`: Deterministic check proving existence at destination.

---

## 4. Destination Map & Inventory Provenance (Plural Model)

### A. Destination Map Updates (`destination-map.csv`)
Maintains the existing 2,286 historical rows and adds Phase 07 plural tracking fields:
- `phase07_split_status`:
  - `retained_singular`: Retained canonical skill (with or without references).
  - `split_parent_router`: Canonical path converted to thin router coordinating child skills.
  - `split_standalone`: Monolith retired and split into independent standalone children.
  - `deferred_manual_review`: Active skill deferred for manual review.
  - `not_applicable_phase06_superseded`: The 192 rows already superseded/retired in Phase 06.
- `phase07_parent_router`: Path to parent router (or `none`).
- `phase07_child_destinations`: Semicolon-separated list of child paths (or `none`).
- `phase07_retired_source_path`: Quarantined path under `task-folder/agents/not-needed/superseded/` (or `none`).

### B. Inventory Immutability (`skills-inventory.csv`)
The historical 2,331-source inventory remains the fixed baseline provenance ledger. No new rows will be appended to represent Phase 07 child skills. Historical source rows will record their split destination and current state without inflating the baseline population.

---

## 5. Complete 18-Point Verification Suite Specification (`verify_phase_07.py`)

1. **[CHECK 1] Full 2,094 Screening Coverage & Baseline Re-validation**:
   - Asserts inventory has 2,331 rows, 2,286 retained skills, and `split-decisions.csv` contains exactly 2,094 canonical active skill rows.
2. **[CHECK 2] Flagged Candidate Deep-Review Coverage**:
   - Proves every flagged candidate (`requires_deep_review == True`) has `review_status in ['deep_reviewed', 'deferred']` and a non-empty rationale.
3. **[CHECK 3] Split Decision Taxonomy Validity**:
   - Validates that 100% of decisions in `split-decisions.csv` conform to the 5 allowed taxonomy values.
4. **[CHECK 4] One-to-Many Split Source-to-Child Reconciliation**:
   - Proves every approved split maps to >= 2 children, and every child traces back to exactly one canonical split source.
5. **[CHECK 5] Child Trigger Uniqueness & Semantic Review Evidence**:
   - Asserts all children define valid frontmatter descriptions and triggers, with documented distinctness evidence.
6. **[CHECK 6] Parent Router Architectural Boundary**:
   - Asserts parent routers contain routing tables, shared policy, and zero inline child execution workflows.
7. **[CHECK 7] Parent & Child Link Integrity**:
   - Asserts parent routers link exclusively to existing child skills, and children reference their parent router where applicable.
8. **[CHECK 8] Section & Material Content Allocation Ledger**:
   - Proves 100% of sections and files in split monoliths are accounted for across `child`, `parent-shared-policy`, `reference`, `duplicate`, `obsolete`, or `retired-with-rationale`.
9. **[CHECK 9] Bundled Resource Package-Level Preservation**:
   - Compares package manifests (relative path + SHA256) proving all preserved bundled resources match quarantined sources byte-for-byte.
10. **[CHECK 10] Physical Source Retirement & Router Replacement Gate**:
    - For splits with parent routers: Asserts the original path contains the new thin parent router, and the original monolithic package exists in `task-folder/agents/not-needed/superseded/`.
    - For standalone splits: Asserts the original monolithic path is completely removed from active skills and exists in `task-folder/agents/not-needed/superseded/`.
11. **[CHECK 11] Destination Map Plural Provenance Preservation**:
    - Asserts all 2,286 rows in `destination-map.csv` have valid `phase07_*` fields reconciling with `split-decisions.csv`, including the 192 rows marked `not_applicable_phase06_superseded`.
12. **[CHECK 12] Inventory Provenance Integrity**:
    - Asserts `skills-inventory.csv` contains exactly 2,331 rows and is not inflated by child skills.
13. **[CHECK 13] Active Library Count Reconciliation**:
    - Asserts:
      Total Active Skills = 2,094 - S_standalone + C_router + C_standalone
      where S_standalone is the count of monoliths fully removed for standalone splits, C_router is child skills under parent routers, and C_standalone is standalone child skills.
14. **[CHECK 14] Zero Stale References to Retired Monoliths**:
    - Scans all active skills, routers, and markdown files to assert zero references point to retired monolithic source paths.
15. **[CHECK 15] Relative Link & Reference Path Existence**:
    - Asserts every relative markdown link across all active and router files resolves to an existing file.
16. **[CHECK 16] Multi-OS Workstation Path Leak Detection**:
    - Asserts zero absolute workstation path leaks (`/Users/...`, `/home/...`, Windows drive letters).
17. **[CHECK 17] Phase 07 Diff Scope Gate**:
    - Asserts git diff against merge-base contains strictly approved split files, routers, children, references, audit artifacts, and mapping updates.
18. **[CHECK 18] Merge-Base & Clean Checkpoint Verification**:
    - Asserts branch is on `skills-rebuild/phase-07-splits` targeting `main` with clean working tree.
