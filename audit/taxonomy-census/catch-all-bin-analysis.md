# Catch-All Bin Semantic Role Decomposition (REV-126 / REV-150)

## Overview

The current catalog contains **908 skills** concentrated in three massive catch-all subcategories:
- `development/fullstack`: 420 skills
- `marketing-and-seo/on-page-seo`: 279 skills
- `marketing-and-seo/cro`: 209 skills

## Semantic Role Breakdown Across Catch-All Bins

| Catch-All Bin | Total Skills | Independent Capabilities | Workflows | Aliases / Duplicates | Overlays / Adapters | References | Primitives | Manual Review |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `development/fullstack` | 420 | 326 | 83 | 1 | 0 | 1 | 1 | 8 |
| `marketing-and-seo/on-page-seo` | 279 | 246 | 30 | 0 | 2 | 0 | 0 | 1 |
| `marketing-and-seo/cro` | 209 | 167 | 38 | 0 | 2 | 1 | 0 | 1 |

---

## Key Findings & Rehousing Recommendations

### 1. `development/fullstack` (420 skills)
- Dominated by **326 independent capabilities**.
- Contains **83 multi-step workflows** (e.g. `fullstack-feature-lifecycle`, `database-migration-pipeline`).
- Contains **9 candidate duplicate pairs** mirroring github-operations (`advanced-workflows`, `commit`, `create-branch`, `create-issue-gate`, `hooks-automation`, `issue-creator`, `pr-review`, `pr-writer`, `review-requests`).
- Contains 1 compatibility alias (`create-pr`), 1 family primitive, 1 reference candidate, and **8 manual review outliers / boundary cases**.
- Contains platform tools that belong in platform families (`figma`, `webflow-automation`, `push-skill-to-github`).
- **Recommendation**: Partition into domain subcategories (`api-design`, `state-management`, `orm-and-database`) and rehouse platform tools into their respective Tier 1 families.

### 2. `marketing-and-seo/on-page-seo` (279 skills)
- Dominated by **246 independent capabilities** and **30 structured audit workflows**.
- Contains **2 platform CMS overlays** that specialize `tools-and-platforms/webflow` (`publish-blog`, `asset-audit`), and **1 manual review boundary case** (`notebooklm`).
- **Recommendation**: Separate into `content-optimization`, `structured-data`, and `editorial-workflows`.

### 3. `marketing-and-seo/cro` (209 skills)
- Contains **38 multi-step experimentation workflows** and **167 focused testing capabilities**.
- Contains 1 overlay, 1 adapter, 1 reference candidate, and **1 manual review boundary case** (`n8n-multi-instance`).
- Contains candidate duplicate pair `feature-tracking` mirroring github-operations.
- Contains n8n automation tools (`n8n-binary-and-data`, `n8n-multi-instance`) that belong in `tools-and-platforms/n8n`.
- **Recommendation**: Retain core experimentation capabilities in `marketing-and-seo/cro` while moving workflow automations to their platform homes.
