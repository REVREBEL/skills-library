# Zero-Index Routing & Provenance Report (SKIL-16)

**Pinned Commit**: `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Repository**: `REVREBEL/skills-library` (`origin/main`)  
**Baseline Date**: `2026-11-02`  
**Linear Issue**: [SKIL-16](https://linear.app/revrebel/issue/SKIL-16/zi-01-pin-canonical-source-and-zero-index-inventory) (Legacy: REV-158)  

---

## 1. Executive Summary & Zero-Index Methodology

- All baseline numbers are **discovered from disk and verified against git tracked source**, never assumed or hardcoded.
- Historical rebuild counts and ledgers are referenced as dated provenance rather than current live state.
- 100% of discovered `SKILL.md` files (5072 total) are categorized with zero silent exclusions.
- Variances between historical denominators and snapshot counts are preserved and explicitly explained with documented uncertainty.
- Pinned commit SHA `195eda775d7a8dcad1837a1990bcba8259da3ea0` is verified via `git rev-parse HEAD` on an isolated clean checkout.

---

## 2. Canonical Identity & RFC 8141 URN Contract

Under ADR-001 and the canonical object model (`tools/skill_library/object_model.py:CanonicalIdentity.parse`), a valid canonical URN strictly requires the format `urn:skill:<scope>:<slug>` or `<scope>:<slug>`. Unscoped single tokens (e.g. `urn:skill:<slug>`) are invalid and fail parsing.

- **Verified Scoped Canonical Identifiers**: Exactly **31** canonical census entries possess verified scoped IDs and receive valid URNs (`urn:skill:github-operations:<slug>`: 18, `urn:skill:skills-create-manage-update:<slug>`: 13).
- **Unscoped Canonical Identifiers**: Exactly **2,102** canonical census entries possess unscoped canonical IDs (e.g. `data-analytics-workflow-automation`). In accordance with work order requirements (*'Canonical identity must not be inferred from a physical path when missing'*), these entries have unassigned URNs (`canonical_urn: ""`) and are logged as informational entries in `discrepancies.csv` awaiting formal Phase 2 scope minting. Zero artificial URNs are manufactured from directory paths.
- **Routers & Nested References**: Routers (28) and nested sub-skill references (496) are not canonical skill packages and carry `canonical_urn: ""` by design.

---

## 3. Discovered Population & Provenance Reconciliation

The repository contains distinct historical and operational populations. The table below reconciles all denominators:

| Denominator ID | Population Name | Baseline Count | Snapshot Count | Variance | Disposition | Notes |
|---|---|:---:|:---:|:---:|---|---|
| **DENOM-01** | Historical Pre-Rebuild Inventory | 2331 | 2101 | -230 | UNVERIFIED_HISTORICAL_DELTA | Historical inventory ledger contains 2,331 rows. On disk, 2,101 active pre-rebuild packages are discovered in `task-folder/agents/skills`. 2,094 match directly, 45 match quarantine paths by substitution, and 192 reflect unlinked historical rows, restructuring, or deletions. Observed count delta (-230) and uncertainty are preserved without forced reconciliation. |
| **DENOM-02** | Historical Rebuilt Active Leaves | 2103 | 2102 | -1 | EXPLAINED_VARIANCE | 1 multi-path alias deduplicated in Task 13 Runtime Manifest. |
| **DENOM-03** | Runtime Manifest Managed Skills | 2102 | 2102 | 0 | RECONCILED | Exact 1:1 match with runtime-manifest.json. |
| **DENOM-04** | Authoritative Semantic Census | 2133 | 2133 | 0 | RECONCILED | Exact 1:1 match with semantic-role-census.json. |
| **DENOM-05** | Total Physical Routers | 28 | 28 | 0 | RECONCILED | 26 standard + 2 operational routers. |
| **DENOM-06** | Total Discovered SKILL.md | 5072 | 5072 | 0 | RECONCILED | 100% discovered-path coverage with zero silent exclusions verified against git ls-files. |

### Row-Level Historical Inventory Crosswalk Details (DENOM-01)
Inspection of `audit/rebuild-phase-1-12/skills-inventory.csv` (2,331 rows) against current on-disk paths reveals:
- **Direct Path Matches**: 2,094 rows match existing packages in `task-folder/agents/skills/`.
- **Quarantine Substitutions**: 45 rows match packages located in `task-folder/agents/not-needed/`.
- **Unlinked Historical Rows**: 192 rows do not map to active paths (reflecting deduplication, merges, restructuring, or deletions during Phases 01-12).
- **Disposition**: Classified as `UNVERIFIED_HISTORICAL_DELTA`. Because historical rebuild documentation does not provide an authoritative row-level reconciliation ledger, the -230 variance is preserved as an empirical observation rather than forcing artificial reconciliation.

---

## 4. Router Link Integrity & Graph Traversal

- **Total Configured Routers**: 26 standard hierarchical routers (via `tools/skill_library/config.py:get_all_routers`)
- **Operational Routers**: 2 operational routers (`library/github-operations/SKILL.md`, `library/skills-create-manage-update/SKILL.md`)
- **Total Library Routers Evaluated**: 28
- **Broken Inbound/Outbound Relative Links**: 0
- **Router Link Verification Status**: **PASS** (All internal relative markdown links resolve to valid on-disk targets).

---

## 5. Subtree Scope Distribution

| Scope Category | Discovered `SKILL.md` Count | Relative Percentage | Classification Purpose |
|---|:---:|:---:|---|
| `canonical_library` | 2133 | 42.1% | Active, managed canonical skills in `library/` |
| `library_router` | 28 | 0.6% | Category, subcategory & operational routing indexes in `library/` |
| `library_nested_reference` | 496 | 9.8% | Nested sub-skills and plugin reference definitions in `library/` |
| `historical_pre_rebuild` | 2101 | 41.4% | Pre-rebuild raw skill packages in `task-folder/agents/skills/` |
| `historical_quarantine` | 238 | 4.7% | Deprecated/unused packages in `task-folder/agents/not-needed/` |
| `historical_archived` | 20 | 0.4% | Archived packages in `task-folder/agents/archived/` |
| `test_fixture` | 49 | 1.0% | Task example test fixtures in `task-example/` |
| `agent_workflow_infrastructure` | 7 | 0.1% | Operational agent workflow tools in `.agents/` |
| **Total Discovered** | **5072** | **100.0%** | **Complete repository zero-index inventory** |
