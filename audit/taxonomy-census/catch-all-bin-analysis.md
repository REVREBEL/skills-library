# Catch-All Bin Semantic Role Decomposition (REV-126 / REV-150)

## Overview

The current catalog contains **908 skills** concentrated in three massive catch-all subcategories:
- `development/fullstack`: 420 skills
- `marketing-and-seo/on-page-seo`: 279 skills
- `marketing-and-seo/cro`: 209 skills

## Semantic Role Breakdown Across Catch-All Bins

| Catch-All Bin | Total Skills | Independent Capabilities | Workflows | Aliases / Duplicates | Overlays / Adapters | Manual Review |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `development/fullstack` | 420 | 328 | 84 | 1 | 1 | 4 |
| `marketing-and-seo/on-page-seo` | 279 | 245 | 31 | 0 | 3 | 0 |
| `marketing-and-seo/cro` | 209 | 166 | 39 | 0 | 3 | 0 |

---

## Key Findings & Rehousing Recommendations

### 1. `development/fullstack` (420 skills)
- Dominated by **328 independent capabilities**.
- Contains **84 multi-step workflows** (e.g. `fullstack-feature-lifecycle`, `database-migration-pipeline`).
- Contains **9 candidate duplicate pairs** mirroring github-operations (`advanced-workflows`, `commit`, `create-branch`, `create-issue-gate`, `hooks-automation`, `issue-creator`, `pr-review`, `pr-writer`, `review-requests`).
- Contains 1 compatibility alias (`create-pr`), 2 family primitives, 1 adapter, and 4 manual review outliers.
- Contains platform tools that belong in platform families (`figma`, `webflow-automation`, `push-skill-to-github`).
- **Recommendation**: Partition into domain subcategories (`api-design`, `state-management`, `orm-and-database`) and rehouse platform tools into their respective Tier 1 families.

### 2. `marketing-and-seo/on-page-seo` (279 skills)
- Dominated by **245 independent capabilities** and **31 structured audit workflows**.
- Contains **3 platform CMS overlays** that specialize `tools-and-platforms/webflow` (`publish-blog`, `asset-audit`).
- **Recommendation**: Separate into `content-optimization`, `structured-data`, and `editorial-workflows`.

### 3. `marketing-and-seo/cro` (209 skills)
- Contains **39 multi-step experimentation workflows** and **166 focused testing capabilities**.
- Contains 2 overlays, 1 adapter, and 1 reference candidate.
- Contains candidate duplicate pair `feature-tracking` mirroring github-operations.
- Contains n8n automation tools (`n8n-binary-and-data`, `n8n-multi-instance`) that belong in `tools-and-platforms/n8n`.
- **Recommendation**: Retain core experimentation capabilities in `marketing-and-seo/cro` while moving workflow automations to their platform homes.
