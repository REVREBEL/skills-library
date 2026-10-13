# Catalog-Wide Platform & Tool Family Register (REV-126 / REV-150)

## Summary Register

| Candidate Family | Tier | Validated Members | Categories Spanned | Subcategories Spanned | Proposed Ownership Home | Architectural Notes |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **GitHub Operations** | Tier 1 | 22 | 3 (development, github-operations) | 2 | `tools-and-platforms/github-operations` | 18 consolidated operations + 4 core main-tree integrations. 27 keyword mentions pruned. |
| **Webflow** | Tier 1 | 22 | 4 (design-and-experience, development) | 9 | `tools-and-platforms/webflow` | 16 named webflow-* + 12 dedicated Webflow Designer/CMS tools. Zero false positives. |
| **Figma** | Tier 1 | 14 | 2 (design-and-experience, development) | 3 | `tools-and-platforms/figma` | 14 dedicated Figma/FigJam tools spanning 2 categories and 3 subcategories. 2 generic design skills pruned. |
| **n8n** | Tier 1 | 14 | 5 (business-and-operations, data-and-ai) | 5 | `tools-and-platforms/n8n` | 14 dedicated n8n node, syntax, and workflow tools scattered across 5 categories. |
| **Hugging Face** | Tier 1 | 19 | 2 (data-and-ai, quality-and-security) | 4 | `tools-and-platforms/hugging-face` | 18 dedicated model/dataset tools within data-and-ai. |
| **WordPress** | Tier 1 | 7 | 2 (development, marketing-and-seo) | 2 | `tools-and-platforms/wordpress` | 7 dedicated WordPress/WooCommerce skills across development and marketing. |
| **NotebookLM** | Tier 1 | 4 | 2 (content-and-documentation, marketing-and-seo) | 3 | `tools-and-platforms/notebooklm` | 4 dedicated NotebookLM research, synthesis, and audio overview tools. |
| **1Password** | Tier 1 | 5 | 1 (infrastructure-and-ops) | 1 | `tools-and-platforms/1password` | 4 dedicated 1Password CLI and Kubernetes operator skills. |
| **Skills Lifecycle** | Tier 1 | 13 | 1 (skills-create-manage-update) | 0 | `meta-and-agent-skills/skill-lifecycle` | Architectural Counterexample: Internal meta-capability family, NOT a tools-and-platforms vendor platform. |

---

## Member-Level Validation Details

### 1. GitHub Operations (22 Validated Members)
- **Consolidated Operations (18)**: `actions-advanced`, `actions-debugger`, `advanced-workflows`, `commit`, `create-branch`, `create-issue-gate`, `feature-tracking`, `github`, `hooks-automation`, `issue-creator`, `llms-maintain`, `pr-merge-champion`, `pr-review`, `pr-writer`, `presence`, `publish-changes`, `review-requests`, `security-review`.
- **Platform Integrations (4)**: `address-github-comments`, `push-skill-to-github`, `openclaw-github-repo-commander`, `actions-templates`.
- **Pruned False Positives (27)**: Skills that merely execute git commands or reference GitHub repos (e.g., `high-contrast`, `high-end-visual-design`, `image`, `javascript-mastery`) were reclassified as `independent_capability`.

### 2. Figma (14 Validated Members)
- **Categories Spanned**: Physically spans **2 top-level categories** (`design-and-experience`, `development`) across **3 subcategories** (`design-systems`, `motion-and-graphics`, `fullstack`).
- **Validated Members (14)**: `figma`, `figma-code-connect`, `figma-create-new-file`, `figma-design-to-code`, `figma-generate-design`, `figma-generate-diagram`, `figma-generate-library`, `figma-implement-motion`, `figma-swiftui`, `figma-use`, `figma-use-figjam`, `figma-use-motion`, `figma-use-slides`, `generate-project-plan`.
- **Pruned Non-Platform Mentions (2)**: `design-system-architect` and `product-design` were confirmed as broad design methodologies that merely reference Figma variables, and remain `independent_capability`.

### 3. Skills Lifecycle (13 Validated Members)
- **Architectural Classification**: Universal meta-capability family.
- **Physical Ownership**: `meta-and-agent-skills/skill-lifecycle`.
- **Rationale**: Does not represent an external tool vendor (like Figma or Webflow), but core agent engineering infrastructure.
