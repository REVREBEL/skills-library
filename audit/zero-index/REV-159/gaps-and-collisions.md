# Gaps, Collisions, and Historical Safety Analysis

This document identifies capabilities present in the 52 historical Drive-archived scripts that are absent or modified in the current codebase, highlights dangerous historical migration writers that must **NEVER** be run against the live catalog, and documents legacy path 404s and deprecated contracts.

---

## 1. Capabilities Present in Historical Scripts but Missing in Current Codebase (Gaps)

While the modern `tools/skill_library/` architecture provides superior governance and type safety, specific diagnostic and analytical capabilities from the historical archive have not yet been formalized:

### 1.1 Cumulative Multi-Phase Discrepancy Auditing (`verify_phase_08_cumulative.py`)
- **Historical Capability:** `verify_phase_08_cumulative.py` tracked discrepancy reconciliation across successive transformation passes (splits, merges, renames) against historical baselines.
- **Current State:** `migration_gates.py` checks point-in-time gate rules (G01–G08) and provenance records, but does not provide an automated historical delta matrix comparing arbitrary historical CSV baselines against current zero-index snapshots.
- **Recommendation:** Adapt the discrepancy matrix calculation logic into `ZI-03` for continuous historical reconciliation reporting without reviving historical mutation passes.

### 1.2 Heuristic Column Discovery (`analyze_inventory_columns.py`)
- **Historical Capability:** Evaluated variance and nullity across unstructured legacy metadata columns.
- **Current State:** Current models expect strict typed schemas (`SkillObject`, `RegistryEntry`).
- **Recommendation:** Maintain as a standalone read-only diagnostic utility for evaluating raw external intake packages that lack canonical frontmatter.

### 1.3 Automated Batch Execution Planning (`generate_batch_plan.py`)
- **Historical Capability:** Partitioned 2,100+ skills into balanced batches for batch processing.
- **Current State:** Modern catalog operations are compiled atomically via `CatalogCompiler`.
- **Recommendation:** Batch planning is no longer needed for catalog compilation, but similar partitioning logic may assist downstream distributed testing in `ZI-05`.

---

## 2. Retired Migration Writers: Safety Guardrails (Collisions & Prohibited Scripts)

A critical outcome of this audit is identifying historical scripts that performed destructive or in-place file modifications. Under approved ADR-000 and Zero-Index governance, **THESE SCRIPTS MUST NEVER BE RUN AGAINST THE LIVE CATALOG OR REPOSITORY CODEBASE**:

| Dangerous Script | Historical Function | Risk / Prohibited Behavior | Current Safe Counterpart |
| :--- | :--- | :--- | :--- |
| `execute_phase08_batches.py` | Rewrote skill files across 160 batches | In-place regex modification of live skill files; violates zero-index immutability | `CatalogCompiler` (read-only projection compiler) |
| `execute_provider_conversion.py` | Pass 1 Claude provider syntax neutralization | Blind string replacements in code samples; strips valid multi-provider syntax | `family_contract.py` (`ExecutionProviderBinding`) |
| `execute_provider_conversion_pass2.py` | Pass 2 provider syntax neutralization | Blind regex replacements; potential file corruption | `family_contract.py` (`ExecutionProviderBinding`) |
| `execute_provider_conversion_pass3.py` | Pass 3 provider syntax neutralization | Blind regex replacements; potential file corruption | `family_contract.py` (`ExecutionProviderBinding`) |
| `neutralize_claude_dependencies.py` | Regex prompt neutralizer | Destructive edits to frontmatter and body | `ExecutionProviderContract` |
| `neutralize_claude_dependencies_v2.py` | Enhanced regex prompt neutralizer | Destructive edits to frontmatter and body | `ExecutionProviderContract` |
| `patch_phase_08_batch1.py` | Hardcoded batch 1 hotfix | Re-imposes superseded Phase 08 path assumptions | Read-only zero-index baseline |
| `update_phase_08_batch1.py` | Hardcoded batch 1 updater | Destructive disk writes | Read-only zero-index baseline |
| `run_all_batches.py` | Automated batch orchestrator | Uncontrolled mass re-writing of catalog tree | Pure read-only CLI (`skill-library.py`) |
| `fix_mcp_zod.py` | AST patcher for MCP schemas | Arbitrary code mutation | Static validation (`validator.py`) |
| `semantic_cleanup.py` | Ad-hoc metadata cleaner | Destructive field deletions | Invariant checking (`object_model.py`) |
| `update_descriptions.py` | Mass frontmatter description updater | Destructive overwrites of curated descriptions | Safe candidate intake (`intake.py`) |

> [!CAUTION]
> **Enforcement Rule:** All 12 scripts listed above are classified as `HISTORICAL-ONLY`. CI pipelines and operational scripts must block any execution of these files.

---

## 3. Legacy Path 404s and Deprecated Routing Contracts

Historical scripts frequently hardcoded filesystem paths and assumptions that are invalid in the current repository layout:

### 3.1 Legacy Workstation and Task Paths (`task-folder/`)
- **Historical Reference:** Historical scripts (`verify_phase_04.py`, `build_phase_05_artifacts.py`, etc.) contain hardcoded references to `/task-folder/agents/skills/` and local scratch locations.
- **Status:** **404 / Nonexistent**. Current canonical root is strictly `library/` governed by `PhysicalPathContract`.

### 3.2 Obsolete Static Taxonomy Categories
- **Historical Reference:** `build_phase_05_artifacts.py` and `verify_phase_10.py` hardcoded 12 top-level category folders and expected an exact count of 2,103 leaves.
- **Status:** **Superseded**. ADR-004 establishes dynamic multi-view projections. Category counts are discovered, never assumed.

### 3.3 Flat Legacy Symlink Targets
- **Historical Reference:** Historical pilot and publication scripts assumed symlinks pointing directly into `library/`.
- **Status:** **Deprecated / Migrated**. ADR-002 and `sync.py` enforce git sparse-checkout and clone targets, eliminating fragile cross-volume symlinks.

### 3.4 Outdated Evidence File Targets
- **Historical Reference:** References to `audit/rebuild-phase-1-12/skills-inventory.csv`, `phase08-canonical-registry.csv`, and `phase10-functional-routing-map.csv`.
- **Status:** **Archived Evidence Only**. These files serve as dated provenance records, not live operational registries.
