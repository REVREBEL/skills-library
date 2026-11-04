# Routing and Provenance Audit Report (SKIL-16)

**Pinned Commit SHA**: `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Target Repository**: `REVREBEL/skills-library` (`origin/main`)  
**Audit Baseline Date**: `2026-11-02`  
**Linear Issue**: [SKIL-16](https://linear.app/revrebel/issue/SKIL-16/zi-01-pin-canonical-source-and-zero-index-inventory) (`40277fb5-9590-43a2-9a7f-3a6d0c8c0401`)  
**Legacy Work Order Reference**: REV-158  

---

## 1. Executive Summary & Objective

This report details the comprehensive zero-index routing and provenance audit conducted under **SKIL-16**.
In accordance with the work order:
- All baseline numbers are **discovered from disk**, never assumed or hardcoded.
- Historical rebuild work is preserved as dated provenance rather than current live state.
- 100% of discovered `SKILL.md` files (5072 total) are categorized with zero silent exclusions.
- Variances between historical denominators and snapshot counts are preserved and explicitly explained with documented uncertainty.

---

## 2. Router Hierarchy & Routing Contracts

The repository's navigation structure is defined across **28 total routers** under `library/`:
- **1 Root Master Router**: `library/SKILL.md`
- **10 Primary Category Routers**:
  - `library/business-and-operations/SKILL.md`
  - `library/content-and-documentation/SKILL.md`
  - `library/data-and-ai/SKILL.md`
  - `library/design-and-experience/SKILL.md`
  - `library/development/SKILL.md`
  - `library/infrastructure-and-ops/SKILL.md`
  - `library/marketing-and-seo/SKILL.md`
  - `library/meta-and-agent-skills/SKILL.md`
  - `library/quality-and-security/SKILL.md`
  - `library/workflow-and-automation/SKILL.md`
- **15 Deep Subcategory Routers**:
  - `design-and-experience/design-systems/SKILL.md`
  - `design-and-experience/motion-and-graphics/SKILL.md`
  - `design-and-experience/taste-and-critique/SKILL.md`
  - `design-and-experience/ui-ux/SKILL.md`
  - `development/backend/SKILL.md`
  - `development/frontend/SKILL.md`
  - `development/fullstack/SKILL.md`
  - `development/mobile/SKILL.md`
  - `development/software-architecture/SKILL.md`
  - `development/systems/SKILL.md`
  - `marketing-and-seo/content-and-campaigns/SKILL.md`
  - `marketing-and-seo/cro/SKILL.md`
  - `marketing-and-seo/geo-and-local-seo/SKILL.md`
  - `marketing-and-seo/on-page-seo/SKILL.md`
  - `marketing-and-seo/technical-seo/SKILL.md`
- **2 Operational System Routers**:
  - `library/github-operations/SKILL.md` (18 managed operational leaf skills)
  - `library/skills-create-manage-update/SKILL.md` (13 managed lifecycle leaf skills)

### Router Traversability & Link Integrity
- **Total Inbound Router Links Mapped**: 2277
- **Broken Relative Links in Router Definitions**: 0 (all destination paths resolve to active filesystem targets).
- **Nested Sub-Skills**: 496 `SKILL.md` files exist nested inside complex multi-module leaf packages (e.g. `super-code/<lang>/SKILL.md`, `gtm-agents-main/plugins/*`, `design-it/*`). These are classified as `nested_reference` and preserve their parent package context.

---

## 3. Provenance & Denominator Reconciliation

The repository contains distinct historical and operational populations. The table below delineates their explicit provenance and measured variance:

| Denominator ID | Population Name | Baseline Count | Snapshot Count | Variance | Disposition | Notes |
|---|---|:---:|:---:|:---:|---|---|
| **DENOM-01** | Historical Pre-Rebuild Inventory | 2331 | 2101 | -230 | UNVERIFIED_HISTORICAL_DELTA | Historical inventory ledger contains 2,331 rows. On disk, 2,101 active pre-rebuild packages are discovered in `task-folder/agents/skills`. 2,094 match directly, 45 match quarantine paths by substitution, and 192 reflect unlinked historical rows, restructuring, or deletions. Observed count delta (-230) and uncertainty are preserved without forced reconciliation. |
| **DENOM-02** | Historical Rebuilt Active Leaves | 2103 | 2102 | -1 | EXPLAINED_VARIANCE | 1 multi-path alias deduplicated in Task 13 Runtime Manifest. |
| **DENOM-03** | Runtime Manifest Managed Skills | 2102 | 2102 | 0 | RECONCILED | Exact 1:1 match with runtime-manifest.json. |
| **DENOM-04** | Authoritative Semantic Census | 2133 | 2133 | 0 | RECONCILED | Exact 1:1 match with semantic-role-census.json. |
| **DENOM-05** | Total Physical Routers | 28 | 28 | 0 | RECONCILED | 26 standard + 2 operational routers. |
| **DENOM-06** | Total Discovered SKILL.md | 5072 | 5072 | 0 | RECONCILED | 100% discovered-path coverage with zero silent exclusions. |

### Row-Level Historical Inventory Crosswalk Details (DENOM-01)
Inspection of `audit/rebuild-phase-1-12/skills-inventory.csv` (2,331 rows) against current on-disk paths reveals:
- **Direct Path Matches**: 2,094 rows match existing `task-folder/agents/skills/` directories on disk.
- **Quarantine Path Matches**: 45 rows match existing `task-folder/agents/not-needed/` directories when substituting the parent path.
- **Archive Path Matches**: 0 rows match `task-folder/agents/archived/` via direct substitution.
- **Unlinked Rows / Structural Moves**: 192 rows represent historical ledger items that were moved, merged, renamed, or deleted during historical Phases 03–08 without an authoritative row-level mapping ledger.
- **Conclusion**: The -230 variance is an observed historical delta with documented uncertainty. It is preserved as `UNVERIFIED_HISTORICAL_DELTA` rather than coerced to a zero-variance match.

---

## 4. Parser and Module Comparison & Canonical URN Contract

1. **`tools/skill_library/config.py`**:
   - Accurately declares all 10 top-level categories, 3 deep categories (15 subcategories), and 7 flat categories (29 subcategories).
   - `get_all_routers()` successfully discovers all 26 standard routers on disk.
2. **`tools/skill_library/manifest.py` (`RuntimeManifest`)**:
   - Successfully loads `audit/runtime-manifest.json` (2102 managed entries).
   - Validated that `manifest.py` enforces flat naming collision resolution (`<cat>-<name>`).
3. **`tools/skill_library/ledger.py` (`ChangeLedger`)**:
   - Confirmed append-only provenance in `audit/change-ledger.jsonl`.
4. **`tools/skill_library/object_model.py` (`CanonicalIdentity`)**:
   - Conforms strictly to ADR-001 and RFC 8141 URN structure: `urn:skill:<scope>:<slug>` (compact `<scope>:<slug>`).
   - `CanonicalIdentity.parse()` enforces that an immutable scope namespace and a kebab-case slug must be present, separated by a colon (`:`). It explicitly **rejects** unscoped `urn:skill:<slug>`.
   - **Provenance Verification**: In the pinned census (`semantic-role-census.json`), exactly 31 items (under `library/github-operations/` and `library/skills-create-manage-update/`) possess verified scoped canonical IDs that parse into valid URNs.
   - **Zero Manufactured IDs**: The remaining 2,102 canonical census entries possess unscoped canonical IDs (slugs without a scope prefix). Under ADR-001 and work order requirements ("Canonical identity must not be inferred from a physical path when missing"), their canonical URNs are recorded as empty (`""`) and classified as unassigned/unscoped in `discrepancies.csv`, awaiting formal scope minting in Phase 2. Zero artificial scopes are inferred from directory paths.
