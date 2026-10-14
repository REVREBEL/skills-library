# Manual Review & Architectural Boundary Register (REV-126 / REV-150)

## Overview

During the catalog census and independent manual semantic audit, exactly **22 skills** were flagged for manual architectural review and assigned `semantic_role = manual_review` with `confidence = low`.

These 22 packages comprise two distinct categories:
1. **Original Catalog Outliers (6 packages)**: Persona critique prompts, non-standard system configurations, and ambiguous multi-domain umbrella names.
2. **Unresolved Architectural Boundary Cases (16 packages)**: Genuinely disputed classification boundaries surfaced during the independent manual semantic audit, held in `manual_review` until authoritative architectural boundaries are established in REV-127 through REV-130.

---

## Summary Register (22 Packages)

| Canonical ID | Current Path | Category | Classification Trigger / Rationale | Gated Milestone |
| :--- | :--- | :--- | :--- | :---: |
| `007` | `library/quality-and-security/security/007` | `quality-and-security` | Persona/agent prompt without concrete technical tasks. | `REV-127` |
| `agent-memory-mcp` | `library/development/software-architecture/agent-memory-mcp` | `development` | Unresolved boundary: MCP storage adapter vs architectural memory capability. | `REV-127/130` |
| `canva-automation` | `library/development/fullstack/canva-automation` | `development` | Unresolved boundary: Asset production workflow vs static template automation. | `REV-127` |
| `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `development` | Unresolved boundary: Multi-phase code inspection pipeline vs single-pass refactoring tool. | `REV-127` |
| `design-token` | `library/design-and-experience/design-systems/design-token` | `design-and-experience` | Unresolved boundary: Atomic design primitive vs standalone design system capability. | `REV-127/129` |
| `emerging-channels` | `library/development/fullstack/emerging-channels` | `development` | Vague multi-channel strategic prompt without concrete steps. | `REV-127` |
| `figma-implement-motion` | `library/design-and-experience/motion-and-graphics/figma-implement-motion` | `design-and-experience` | Unresolved boundary: Figma platform overlay vs multi-step animation workflow. | `REV-127/129` |
| `figma-swiftui` | `library/design-and-experience/design-systems/figma-swiftui` | `design-and-experience` | Unresolved boundary: Figma design overlay vs standalone SwiftUI code generator. | `REV-127/129` |
| `geminiignore-finops` | `library/development/fullstack/geminiignore-finops` | `development` | Tool-specific configuration file generator. | `REV-127` |
| `integrations` | `library/development/fullstack/integrations` | `development` | Ambiguous umbrella name colliding with domain categories. | `REV-127` |
| `launch` | `library/development/backend/launch` | `development` | Unresolved boundary: Strategic cross-domain launch orchestration vs singular deployment capability. | `REV-127` |
| `marketing-and-seo-notebooklm` | `library/marketing-and-seo/on-page-seo/notebooklm` | `marketing-and-seo` | Unresolved boundary: NotebookLM platform overlay vs domain SEO research capability. | `REV-127/129` |
| `n8n-expression-syntax` | `library/quality-and-security/debugging/n8n-expression-syntax` | `quality-and-security` | Unresolved boundary: Expression syntax primitive vs syntax debugging capability. | `REV-127/129` |
| `n8n-multi-instance` | `library/marketing-and-seo/cro/n8n-multi-instance` | `marketing-and-seo` | Unresolved boundary: n8n infrastructure overlay vs CRO architectural reference. | `REV-127/129` |
| `nerdzao-elite-gemini-high` | `library/development/fullstack/nerdzao-elite-gemini-high` | `development` | Non-standard model system prompt configuration. | `REV-127` |
| `nextjs-supabase-auth` | `library/development/frontend/nextjs-supabase-auth` | `development` | Unresolved boundary: Authentication primitive vs fullstack auth integration capability. | `REV-127/129` |
| `not-human-search-mcp` | `library/development/backend/not-human-search-mcp` | `development` | Unresolved boundary: MCP protocol adapter vs autonomous search capability. | `REV-127/130` |
| `notebooklm-create` | `library/content-and-documentation/presentations/notebooklm-create` | `content-and-documentation` | Unresolved boundary: NotebookLM platform overlay vs presentation generation workflow. | `REV-127/129` |
| `protect-mcp-governance` | `library/workflow-and-automation/tool-integration/protect-mcp-governance` | `workflow-and-automation` | Unresolved boundary: MCP runtime adapter vs governance policy capability. | `REV-127/130` |
| `steve-jobs` | `library/development/fullstack/steve-jobs` | `development` | Executive persona critique prompt. | `REV-127` |
| `tool-use-guardian` | `library/development/fullstack/tool-use-guardian` | `development` | Unresolved boundary: Tool execution adapter vs safety interception workflow. | `REV-127/130` |
| `webflow-cli-cloud` | `library/development/fullstack/webflow-cli-cloud` | `development` | Unresolved boundary: Webflow CLI primitive vs cloud deployment workflow. | `REV-127/129` |

---

## 1. Original Catalog Outliers (6 Packages)

These packages were identified as structural or content outliers during the initial catalog intake:

| Canonical ID | Current Path | Outlier Nature | Architectural Recommendation | Gated Milestone |
| :--- | :--- | :--- | :--- | :---: |
| `007` | `library/quality-and-security/security/007` | Persona/agent prompt without concrete technical tasks | Move to agent personas or archive | `REV-127` |
| `steve-jobs` | `library/development/fullstack/steve-jobs` | Executive persona critique prompt | Move to critique personas or archive | `REV-127` |
| `nerdzao-elite-gemini-high` | `library/development/fullstack/nerdzao-elite-gemini-high` | Non-standard model system prompt configuration | Move to agent prompts or test configs | `REV-127` |
| `geminiignore-finops` | `library/development/fullstack/geminiignore-finops` | Tool-specific configuration file generator | Consolidate under cloud FinOps capability | `REV-127` |
| `emerging-channels` | `library/development/fullstack/emerging-channels` | Vague multi-channel strategic prompt without concrete steps | Refactor into specific social/ad capabilities | `REV-127` |
| `integrations` | `library/development/fullstack/integrations` | Ambiguous umbrella name colliding with domain categories | Rename to `third-party-integration-patterns` | `REV-127` |

---

## 2. Unresolved Architectural Boundary Cases (16 Packages)

These packages represent active architectural boundary decisions deferred to upcoming milestones:

### A. Capability vs. Multi-Phase Workflow (3 Packages, Gated under REV-127)
- `launch` (`library/development/backend/launch`): Strategic cross-domain launch orchestration vs. singular deployment capability.
- `code-refactoring-tech-debt` (`library/development/software-architecture/code-refactoring-tech-debt`): Multi-phase code inspection pipeline vs. single-pass refactoring tool.
- `canva-automation` (`library/development/fullstack/canva-automation`): Asset production workflow vs. static template automation.

### B. Platform Overlay vs. Domain Capability / Workflow (5 Packages, Gated under REV-127 / REV-129)
- `figma-implement-motion` (`library/design-and-experience/motion-and-graphics/figma-implement-motion`): Figma platform overlay vs. multi-step animation workflow.
- `marketing-and-seo-notebooklm` (`library/marketing-and-seo/on-page-seo/notebooklm`): NotebookLM platform overlay vs. domain SEO research capability.
- `notebooklm-create` (`library/content-and-documentation/presentations/notebooklm-create`): NotebookLM platform overlay vs. presentation generation workflow.
- `figma-swiftui` (`library/design-and-experience/design-systems/figma-swiftui`): Figma design overlay vs. standalone SwiftUI code generator.
- `n8n-multi-instance` (`library/marketing-and-seo/cro/n8n-multi-instance`): n8n infrastructure overlay vs. CRO architectural reference.

### C. Tool Execution Adapter vs. Domain Capability (4 Packages, Gated under REV-127 / REV-130)
- `not-human-search-mcp` (`library/development/backend/not-human-search-mcp`): MCP protocol adapter vs. autonomous search capability.
- `protect-mcp-governance` (`library/workflow-and-automation/tool-integration/protect-mcp-governance`): MCP runtime adapter vs. governance policy capability.
- `tool-use-guardian` (`library/development/fullstack/tool-use-guardian`): Tool execution adapter vs. safety interception workflow.
- `agent-memory-mcp` (`library/development/software-architecture/agent-memory-mcp`): MCP storage adapter vs. architectural memory capability.

### D. Platform Primitive vs. Domain Capability / Workflow (4 Packages, Gated under REV-127 / REV-129)
- `design-token` (`library/design-and-experience/design-systems/design-token`): Atomic design primitive vs. standalone design system capability.
- `nextjs-supabase-auth` (`library/development/frontend/nextjs-supabase-auth`): Authentication primitive vs. fullstack auth integration capability.
- `webflow-cli-cloud` (`library/development/fullstack/webflow-cli-cloud`): Webflow CLI primitive vs. cloud deployment workflow.
- `n8n-expression-syntax` (`library/quality-and-security/debugging/n8n-expression-syntax`): Expression syntax primitive vs. syntax debugging capability.

---
All 22 packages are preserved in the catalog census with `confidence = low` and `semantic_role = manual_review` until authoritative arbitration in REV-127 through REV-130.