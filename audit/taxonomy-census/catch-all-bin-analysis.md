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
- Contains **87 multi-step workflows** (e.g. `fullstack-feature-lifecycle`, `database-migration-pipeline`).
- Contains **8 candidate duplicate pairs** mirroring github-operations (`advanced-workflows`, `commit`, `create-branch`, `create-issue-gate`, `hooks-automation`, `issue-creator`, `pr-review`, `pr-writer`, `review-requests`).
- Contains platform tools that belong in platform families (`figma`, `webflow-automation`, `push-skill-to-github`).
- **Recommendation**: Partition into domain subcategories (`api-design`, `state-management`, `orm-and-database`) and rehouse platform tools into their respective Tier 1 families.

### 2. `marketing-and-seo/on-page-seo` (279 skills)
- Dominated by **198 independent capabilities** and **76 structured audit workflows**.
- Contains platform CMS publishers that belong in `tools-and-platforms/webflow` (`publish-blog`, `asset-audit`).
- **Recommendation**: Separate into `content-optimization`, `structured-data`, and `editorial-workflows`.

### 3. `marketing-and-seo/cro` (209 skills)
- Contains **42 multi-step experimentation workflows** and **161 focused testing capabilities**.
- Contains n8n automation tools (`n8n-binary-and-data`, `n8n-multi-instance`) that belong in `tools-and-platforms/n8n`.
- Contains candidate duplicate pair `feature-tracking` mirroring github-operations.
- **Recommendation**: Retain core experimentation capabilities in `marketing-and-seo/cro` while moving workflow automations to their platform homes.
