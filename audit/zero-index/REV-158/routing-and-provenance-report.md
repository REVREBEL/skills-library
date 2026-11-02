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
- Variances between historical denominators and snapshot counts are preserved and explicitly explained.

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
| **DENOM-01** | Historical Pre-Rebuild Inventory | 2331 | 2101 | -230 | EXPLAINED_VARIANCE | 230 packages moved to quarantine/archive during historical rebuild. |
| **DENOM-02** | Historical Rebuilt Active Leaves | 2103 | 2102 | -1 | EXPLAINED_VARIANCE | 1 multi-path alias deduplicated in Task 13 Runtime Manifest. |
| **DENOM-03** | Runtime Manifest Managed Skills | 2102 | 2102 | 0 | RECONCILED | Exact 1:1 match with runtime-manifest.json. |
| **DENOM-04** | Authoritative Semantic Census | 2133 | 2133 | 0 | RECONCILED | Exact 1:1 match with semantic-role-census.json. |
| **DENOM-05** | Total Physical Routers | 28 | 28 | 0 | RECONCILED | 26 standard + 2 operational routers. |
| **DENOM-06** | Total Discovered SKILL.md | 5072 | 5072 | 0 | RECONCILED | 100% discovered-path coverage with zero silent exclusions. |

---

## 4. Parser and Module Comparison

1. **`tools/skill_library/config.py`**:
   - Accurately declares all 10 top-level categories, 3 deep categories (15 subcategories), and 7 flat categories (29 subcategories).
   - `get_all_routers()` successfully discovers all 26 standard routers on disk.
2. **`tools/skill_library/manifest.py` (`RuntimeManifest`)**:
   - Successfully loads `audit/runtime-manifest.json` (2102 managed entries).
   - Validated that `manifest.py` enforces flat naming collision resolution (`<cat>-<name>`).
3. **`tools/skill_library/ledger.py` (`ChangeLedger`)**:
   - Confirmed append-only provenance in `audit/change-ledger.jsonl`.
4. **`tools/skill_library/object_model.py` (`CanonicalIdentity`)**:
   - Validates path-independent URN format for all canonical census entries (`urn:skill:<scope>:<slug>` or `urn:skill:<slug>`).
   - Ensures zero manufactured URNs for non-canonical fixtures, nested references, and historical source files.
