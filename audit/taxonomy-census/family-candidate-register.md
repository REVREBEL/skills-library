# Catalog-Wide Platform & Tool Family Register (REV-126 / REV-150)

## Summary Register

| Candidate Family | Tier | Validated Members | Categories Spanned | Subcategories Spanned | Proposed Ownership Home | Architectural Notes |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **GitHub Operations** | Tier 1 | 22 | 3 (development, github-operations) | 2 | `tools-and-platforms/github-operations` | 22 validated members: 18 consolidated operations + 4 core main-tree integrations. 27 keyword mentions pruned. |
| **Webflow** | Tier 1 | 22 | 4 (design-and-experience, development) | 9 | `tools-and-platforms/webflow` | 22 validated members: 16 named webflow-* + 6 dedicated Webflow tools. 6 generic audit mentions pruned. |
| **Figma** | Tier 1 | 14 | 2 (design-and-experience, development) | 3 | `tools-and-platforms/figma` | 14 validated members spanning 2 top-level categories and 3 subcategories. 2 generic design skills pruned. |
| **n8n** | Tier 1 | 14 | 5 (business-and-operations, data-and-ai) | 5 | `tools-and-platforms/n8n` | 14 validated members: dedicated n8n node, syntax, and multi-instance tools scattered across 5 categories. |
| **Hugging Face** | Tier 1 | 19 | 2 (data-and-ai, quality-and-security) | 4 | `tools-and-platforms/hugging-face` | 19 validated members: 13 hugging-face-* + 6 huggingface-* dedicated model/dataset tools within data-and-ai. |
| **WordPress** | Tier 1 | 7 | 2 (development, marketing-and-seo) | 2 | `tools-and-platforms/wordpress` | 7 validated members: dedicated WordPress/WooCommerce skills across development and marketing. |
| **NotebookLM** | Tier 1 | 4 | 2 (content-and-documentation, marketing-and-seo) | 3 | `tools-and-platforms/notebooklm` | 4 validated members: dedicated NotebookLM research, synthesis, and audio overview tools. |
| **1Password** | Tier 1 | 5 | 1 (infrastructure-and-ops) | 1 | `tools-and-platforms/1password` | 5 validated members: dedicated 1Password CLI and Kubernetes operator skills. |
| **Skills Lifecycle** | Tier 1 | 13 | 1 (skills-create-manage-update) | 0 | `meta-and-agent-skills/skill-lifecycle` | 13 validated members: Internal meta-capability family, NOT a tools-and-platforms third-party vendor platform. |

---

## Member-Level Validation Details

### 1. GitHub Operations (22 Validated Members)
- **Consolidated Operations (18)**: `actions-advanced`, `actions-debugger`, `advanced-workflows`, `commit`, `create-branch`, `create-issue-gate`, `feature-tracking`, `github`, `hooks-automation`, `issue-creator`, `llms-maintain`, `pr-merge-champion`, `pr-review`, `pr-writer`, `presence`, `publish-changes`, `review-requests`, `security-review`.
- **Platform Integrations (4)**: `actions-templates`, `address-github-comments`, `openclaw-github-repo-commander`, `push-skill-to-github`.
- **Pruned False Positives (27)**: Skills that merely execute git commands or reference GitHub repos (e.g., `high-contrast`, `high-end-visual-design`, `image`, `javascript-mastery`) were reclassified as `independent_capability`.

### 2. Webflow (22 Validated Members)
- **Prefix Packages (16)**: `webflow-automation`, `webflow-cli-cloud`, `webflow-cli-code-component`, `webflow-cli-designer-extension`, `webflow-cli-devlink`, `webflow-cli-troubleshooter`, `webflow-code-component-component-audit`, `webflow-code-component-component-scaffold`, `webflow-code-component-convert-component`, `webflow-code-component-deploy-guide`, `webflow-code-component-local-dev-setup`, `webflow-code-component-pre-deploy-check`, `webflow-code-component-troubleshoot-deploy`, `webflow-code-components`, `webflow-designer-api`, `webflow-ui-skills`.
- **Dedicated Platform Tools (6)**: `bulk-cms-update`, `cms-collection-setup`, `designer-tools`, `flowkit-naming`, `publish-blog`, `safe-publish`.
- **Pruned Generic Audit Skills (6)**: Skills like `site-audit`, `custom-code-management`, and `asset-audit` that mention Webflow alongside other CMS platforms remain domain capabilities.

### 3. Figma (14 Validated Members)
- **Categories Spanned**: Physically spans **2 top-level categories** (`design-and-experience`, `development`) across **3 subcategories** (`design-systems` [11], `motion-and-graphics` [2], `fullstack` [1]).
- **Validated Members (14)**: `figma`, `figma-code-connect`, `figma-create-new-file`, `figma-design-to-code`, `figma-generate-design`, `figma-generate-diagram`, `figma-generate-library`, `figma-implement-motion`, `figma-swiftui`, `figma-use`, `figma-use-figjam`, `figma-use-motion`, `figma-use-slides`, `generate-project-plan`.
- **Pruned Non-Platform Mentions (2)**: `design-system-architect` and `product-design` were confirmed as broad design methodologies that merely reference Figma variables, and remain `independent_capability`.

### 4. Hugging Face (19 Validated Members)
- **Validated Members (19)**: `hugging-face-cli`, `hugging-face-community-evals`, `hugging-face-dataset-viewer`, `hugging-face-datasets`, `hugging-face-evaluation`, `hugging-face-gradio`, `hugging-face-jobs`, `hugging-face-model-trainer`, `hugging-face-paper-publisher`, `hugging-face-papers`, `hugging-face-tool-builder`, `hugging-face-trackio`, `hugging-face-vision-trainer`, `huggingface-best`, `huggingface-local-models`, `huggingface-lora-space-builder`, `huggingface-spaces`, `huggingface-tool-builder`, `huggingface-zerogpu`.

### 5. 1Password (5 Validated Members)
- **Validated Members (5)**: `1password`, `1password-cli`, `1password-developer-environments`, `1password-kubernetes`, `1password-service-accounts`.

### 6. Skills Lifecycle (13 Validated Members)
- **Architectural Classification**: Universal meta-capability family.
- **Physical Ownership**: `meta-and-agent-skills/skill-lifecycle`.
- **Rationale**: Does not represent an external tool vendor (like Figma or Webflow), but core agent engineering infrastructure.

---

## Family Eligibility Principles

Candidate platform families are evaluated against qualitative architectural criteria rather than arbitrary numerical thresholds:
1. **Cohesive Platform Tool Surface**: Shared CLI, MCP server, API client, or platform designer extension.
2. **Shared Reusable Primitives**: Common authentication, session handling, environment tokens, or runtime configuration.
3. **Cross-Domain Consumers**: Required by multiple downstream domains with structured handoffs.
4. **Coordinated Maintenance & Versioning**: Benefits from unified lifecycle management and regression testing.

Formal family eligibility decisions are strictly gated under **REV-129**. This register serves as an evidence base, not an automatic promotion mechanism.