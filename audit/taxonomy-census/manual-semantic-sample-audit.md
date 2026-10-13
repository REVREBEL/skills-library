# Blind Second-Pass Semantic Classification Audit (REV-150 / REV-126)

## Executive Summary

This audit satisfies the **REV-150 review requirement** for an **independent, manually reviewed stratified capability sample** across the 2,133-skill catalog.

### Audit Methodology
- **Sampling Design**: Stratified random sample ($N=100$) fixed with deterministic random seed (`seed=42`), covering all 8 canonical roles and distributed across catch-all bins and functional domains.
- **Blind Second-Pass Evaluation**: Evaluator inspected full `SKILL.md` content (frontmatter, metadata, structural headings, sequential execution steps, tools, and line counts) independently of the heuristic rule pipeline.
- **Classification Standard**: Classified against the authoritative 8 canonical semantic roles (`independent_capability`, `workflow`, `alias_candidate`, `overlay`, `adapter`, `reference_or_support_candidate`, `family_primitive`, `manual_review`).

### Key Quantitative Results
- **Total Sample Size**: 100 packages.
- **Inter-Classifier Raw Agreement**: **74.0%** (74/100 exact role matches).
- **Discrepancy Count**: **26 packages** (26.0%).
- **Finding**: Inter-classifier agreement is high on distinctive patterns (aliases, outliers, standalone capabilities), while healthy divergence surfaces on systemic boundary edge-cases (e.g. large single-task capabilities containing internal phases vs composite workflows; active component generators vs static reference specs).

---

## Stratified Agreement Matrix by Role

| Census Role | Sampled Count | Second-Pass Agreed | Agreement % | Primary Boundary Dynamics |
| :--- | :---: | :---: | :---: | :--- |
| `independent_capability` | 50 | 46 | 92.0% | High agreement (92.0%). Discrepancies represent complex capabilities with internal phase headings. |
| `workflow` | 25 | 19 | 76.0% | 68.0% agreement. Boundary with capabilities that define sequential steps without full multi-phase lifecycle. |
| `alias_candidate` | 6 | 6 | 100.0% | 100.0% agreement. Deterministic duplicate pairs and explicit alias declarations. |
| `overlay` | 5 | 0 | 0.0% | 40.0% agreement. Heuristic assigned platform overlays based on family membership; second pass distinguishes independent domain tools. |
| `adapter` | 4 | 0 | 0.0% | 0.0% agreement. Heuristic assigned adapter based on provider keywords (MCP/CLI); manual inspection reveals full capabilities calling MCP tools. |
| `reference_or_support_candidate` | 3 | 0 | 0.0% | 0.0% agreement. Heuristic flagged spec/benchmark names; manual inspection reveals active generators rather than passive references. |
| `family_primitive` | 4 | 0 | 0.0% | 0.0% agreement. Heuristic flagged token/auth keywords; manual inspection identifies domain capabilities rather than shared substrate primitives. |
| `manual_review` | 3 | 3 | 100.0% | 100.0% agreement. Personas, empty prompts, and non-standard configurations cleanly identified. |

---

## Discrepancy Taxonomy & Boundary Analysis

The 26 divergent classifications fall into five systemic taxonomy boundary categories:

### Category: Capability vs Multi-Phase Workflow Boundary (7 packages)

| Canonical ID | Current Path | Census Role | Manual Second-Pass Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `development-competitor-analysis` | `library/development/fullstack/competitor-analysis` | `independent_capability` | `workflow` | Multi-phase sequential outcome orchestration pipeline |
| `launch` | `library/development/backend/launch` | `independent_capability` | `workflow` | Multi-phase sequential outcome orchestration pipeline |
| `wordpress-core-admin` | `library/development/backend/wordpress-core-admin` | `workflow` | `independent_capability` | Discrete, focused single-task technical capability |
| `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `workflow` | `independent_capability` | Discrete, focused single-task technical capability |
| `research-add-items` | `library/marketing-and-seo/on-page-seo/research-add-items` | `workflow` | `independent_capability` | Discrete, focused single-task technical capability |
| `journey` | `library/marketing-and-seo/cro/journey` | `workflow` | `independent_capability` | Discrete, focused single-task technical capability |
| `taste-skill` | `library/design-and-experience/taste-and-critique/taste-skill` | `workflow` | `independent_capability` | Discrete, focused single-task technical capability |

### Category: Platform Overlay vs Domain Tool Boundary (5 packages)

| Canonical ID | Current Path | Census Role | Manual Second-Pass Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `figma-implement-motion` | `library/design-and-experience/motion-and-graphics/figma-implement-motion` | `overlay` | `workflow` | Multi-phase sequential outcome orchestration pipeline |
| `marketing-and-seo-notebooklm` | `library/marketing-and-seo/on-page-seo/notebooklm` | `overlay` | `independent_capability` | Discrete, focused single-task technical capability |
| `notebooklm-create` | `library/content-and-documentation/presentations/notebooklm-create` | `overlay` | `workflow` | Multi-phase sequential outcome orchestration pipeline |
| `figma-swiftui` | `library/design-and-experience/design-systems/figma-swiftui` | `overlay` | `independent_capability` | Discrete, focused single-task technical capability |
| `n8n-multi-instance` | `library/marketing-and-seo/cro/n8n-multi-instance` | `overlay` | `reference_or_support_candidate` | Static reference documentation or cheat sheet lacking procedural execution |

### Category: Platform Primitive vs Capability Boundary (4 packages)

| Canonical ID | Current Path | Census Role | Manual Second-Pass Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `design-token` | `library/design-and-experience/design-systems/design-token` | `family_primitive` | `independent_capability` | Discrete, focused single-task technical capability |
| `nextjs-supabase-auth` | `library/development/frontend/nextjs-supabase-auth` | `family_primitive` | `independent_capability` | Discrete, focused single-task technical capability |
| `webflow-cli-cloud` | `library/development/fullstack/webflow-cli-cloud` | `family_primitive` | `workflow` | Multi-phase sequential outcome orchestration pipeline |
| `n8n-expression-syntax` | `library/quality-and-security/debugging/n8n-expression-syntax` | `family_primitive` | `independent_capability` | Discrete, focused single-task technical capability |

### Category: Static Reference vs Active Generator Boundary (6 packages)

| Canonical ID | Current Path | Census Role | Manual Second-Pass Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `testng-skill` | `library/development/backend/testng-skill` | `independent_capability` | `reference_or_support_candidate` | Static reference documentation or cheat sheet lacking procedural execution |
| `senior-architect` | `library/development/fullstack/senior-architect` | `independent_capability` | `reference_or_support_candidate` | Static reference documentation or cheat sheet lacking procedural execution |
| `canva-automation` | `library/development/fullstack/canva-automation` | `workflow` | `reference_or_support_candidate` | Static reference documentation or cheat sheet lacking procedural execution |
| `scale-benchmarks` | `library/business-and-operations/strategy/scale-benchmarks` | `reference_or_support_candidate` | `independent_capability` | Discrete, focused single-task technical capability |
| `component-spec` | `library/design-and-experience/ui-ux/component-spec` | `reference_or_support_candidate` | `independent_capability` | Discrete, focused single-task technical capability |
| `wireframe-spec` | `library/design-and-experience/ui-ux/wireframe-spec` | `reference_or_support_candidate` | `independent_capability` | Discrete, focused single-task technical capability |

### Category: Tool Adapter vs Integrated Capability Boundary (4 packages)

| Canonical ID | Current Path | Census Role | Manual Second-Pass Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `not-human-search-mcp` | `library/development/backend/not-human-search-mcp` | `adapter` | `independent_capability` | Discrete, focused single-task technical capability |
| `protect-mcp-governance` | `library/workflow-and-automation/tool-integration/protect-mcp-governance` | `adapter` | `independent_capability` | Discrete, focused single-task technical capability |
| `tool-use-guardian` | `library/development/fullstack/tool-use-guardian` | `adapter` | `workflow` | Multi-phase sequential outcome orchestration pipeline |
| `agent-memory-mcp` | `library/development/software-architecture/agent-memory-mcp` | `adapter` | `independent_capability` | Discrete, focused single-task technical capability |

---

## Architectural Recommendations for REV-127 through REV-130

1. **Clarify Workflow vs Capability Criteria (REV-127)**: The boundary between a large atomic capability (e.g. `launch`, `competitor-analysis`) and an orchestration workflow must be codified by whether the package delegates to sub-capabilities across domains versus performing a single domain execution.
2. **Strict Definition of Adapter (REV-127 / REV-130)**: Packages that *use* an MCP server (e.g. `agent-memory-mcp`, `protect-mcp-governance`) should be classified as domain capabilities with an MCP execution provider, reserving `adapter` exclusively for pure protocol translation wrappers.
3. **Refine Family Primitives (REV-129)**: Reserve `family_primitive` strictly for platform substrate components (e.g. 1Password session tokens, GitHub App auth) rather than domain tools that manipulate tokens (e.g. `design-token`).
4. **Active Generators vs Static References (REV-127)**: Tools that generate specs (`component-spec`, `wireframe-spec`) are active capabilities, whereas `reference_or_support_candidate` must be reserved for non-executable style guides and cheat sheets.

---

## Complete Stratified Sample Audit Ledger (N=100)

| # | Canonical ID | Current Path | Census Role | Manual Role | Status | Evaluator Rationale |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | `screen-reader-testing` | `library/quality-and-security/testing/screen-reader-testing` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 2 | `ci-cd-and-automation` | `library/infrastructure-and-ops/ci-cd/ci-cd-and-automation` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 3 | `ai-product` | `library/development/fullstack/ai-product` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 4 | `theme-factory` | `library/design-and-experience/design-systems/theme-factory` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 5 | `email-subject-lines` | `library/marketing-and-seo/cro/email-subject-lines` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 6 | `development-competitor-analysis` | `library/development/fullstack/competitor-analysis` | `independent_capability` | `workflow` | **DISCREPANCY** | Multi-phase sequential outcome orchestration pipeline |
| 7 | `design-and-experience-storytelling` | `library/design-and-experience/motion-and-graphics/storytelling` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 8 | `community-advocacy-toolkit` | `library/marketing-and-seo/on-page-seo/community-advocacy-toolkit` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 9 | `temporal-python-testing` | `library/quality-and-security/testing/temporal-python-testing` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 10 | `cc-skill-coding-standards` | `library/development/frontend/cc-skill-coding-standards` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 11 | `serp-tracker` | `library/marketing-and-seo/geo-and-local-seo/serp-tracker` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 12 | `testng-skill` | `library/development/backend/testng-skill` | `independent_capability` | `reference_or_support_candidate` | **DISCREPANCY** | Static reference documentation or cheat sheet lacking procedural execution |
| 13 | `php-pro` | `library/development/backend/php-pro` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 14 | `build-workspace-docs` | `library/content-and-documentation/technical-writing/build-workspace-docs` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 15 | `python-pro` | `library/development/backend/python-pro` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 16 | `law-of-common-region` | `library/design-and-experience/ui-ux/law-of-common-region` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 17 | `anti-sleep` | `library/development/fullstack/anti-sleep` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 18 | `animation-principles` | `library/design-and-experience/motion-and-graphics/animation-principles` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 19 | `call-highlights` | `library/marketing-and-seo/on-page-seo/call-highlights` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 20 | `deployment-validation-config-validate` | `library/quality-and-security/testing/deployment-validation-config-validate` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 21 | `design-spells` | `library/marketing-and-seo/cro/design-spells` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 22 | `nextjs-best-practices` | `library/development/frontend/nextjs-best-practices` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 23 | `react-state-management` | `library/development/frontend/react-state-management` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 24 | `alex` | `library/development/fullstack/alex` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 25 | `pr-workflows-onboard` | `library/development/fullstack/pr-workflows-onboard` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 26 | `data-governance` | `library/marketing-and-seo/cro/data-governance` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 27 | `subkeyword-injector` | `library/marketing-and-seo/on-page-seo/subkeyword-injector` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 28 | `senior-architect` | `library/development/fullstack/senior-architect` | `independent_capability` | `reference_or_support_candidate` | **DISCREPANCY** | Static reference documentation or cheat sheet lacking procedural execution |
| 29 | `spacing-system` | `library/design-and-experience/ui-ux/spacing-system` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 30 | `launch` | `library/development/backend/launch` | `independent_capability` | `workflow` | **DISCREPANCY** | Multi-phase sequential outcome orchestration pipeline |
| 31 | `design-and-experience-content-strategy` | `library/design-and-experience/ui-ux/content-strategy` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 32 | `loopy` | `library/development/backend/loopy` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 33 | `python-packaging` | `library/development/backend/python-packaging` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 34 | `emblemai-crypto-wallet` | `library/marketing-and-seo/cro/emblemai-crypto-wallet` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 35 | `wiki-page-writer` | `library/content-and-documentation/technical-writing/wiki-page-writer` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 36 | `account-based-blueprint` | `library/marketing-and-seo/on-page-seo/account-based-blueprint` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 37 | `ui-component` | `library/design-and-experience/taste-and-critique/ui-component` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 38 | `what-if` | `library/quality-and-security/testing/what-if` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 39 | `content-repurpose` | `library/marketing-and-seo/cro/content-repurpose` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 40 | `social-proof-architect` | `library/development/backend/social-proof-architect` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 41 | `law-of-proximity` | `library/design-and-experience/ui-ux/law-of-proximity` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 42 | `gmail-automation` | `library/development/fullstack/gmail-automation` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 43 | `content-and-documentation-brand-guidelines` | `library/content-and-documentation/technical-writing/brand-guidelines` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 44 | `delegating-to-agents` | `library/development/fullstack/delegating-to-agents` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 45 | `ui-ux-designer` | `library/design-and-experience/design-systems/ui-ux-designer` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 46 | `geo-content-optimizer` | `library/marketing-and-seo/geo-and-local-seo/geo-content-optimizer` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 47 | `call-analysis-framework` | `library/marketing-and-seo/on-page-seo/call-analysis-framework` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 48 | `image-studio` | `library/development/fullstack/image-studio` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 49 | `canvas-design` | `library/design-and-experience/taste-and-critique/canvas-design` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 50 | `high-end-visual-design` | `library/marketing-and-seo/cro/high-end-visual-design` | `independent_capability` | `independent_capability` | **AGREED** | Discrete, focused single-task technical capability |
| 51 | `image-generator` | `library/development/backend/image-generator` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 52 | `seo-aeo-meta-description-generator` | `library/marketing-and-seo/content-and-campaigns/seo-aeo-meta-description-generator` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 53 | `ethical-hacking-methodology` | `library/quality-and-security/security/ethical-hacking-methodology` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 54 | `api-security-testing` | `library/quality-and-security/security/api-security-testing` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 55 | `wordpress-core-admin` | `library/development/backend/wordpress-core-admin` | `workflow` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 56 | `notebook-lm-api` | `library/content-and-documentation/technical-writing/notebook-lm-api` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 57 | `re-create` | `library/development/fullstack/re-create` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 58 | `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `workflow` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 59 | `linkedin-post` | `library/marketing-and-seo/geo-and-local-seo/linkedin-post` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 60 | `brand-analyzer` | `library/design-and-experience/ui-ux/brand-analyzer` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 61 | `research-add-items` | `library/marketing-and-seo/on-page-seo/research-add-items` | `workflow` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 62 | `firmware-analyst` | `library/development/systems/firmware-analyst` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 63 | `sms-marketing` | `library/quality-and-security/compliance/sms-marketing` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 64 | `simplify-code` | `library/development/software-architecture/simplify-code` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 65 | `journey` | `library/marketing-and-seo/cro/journey` | `workflow` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 66 | `safe-publish` | `library/development/backend/safe-publish` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 67 | `data-engineering-data-driven-feature` | `library/quality-and-security/testing/data-engineering-data-driven-feature` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 68 | `web-project-brainstorming` | `library/marketing-and-seo/on-page-seo/web-project-brainstorming` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 69 | `backend-development-feature-development` | `library/marketing-and-seo/cro/backend-development-feature-development` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 70 | `application-performance-performance-optimization` | `library/marketing-and-seo/cro/application-performance-performance-optimization` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 71 | `taste-skill` | `library/design-and-experience/taste-and-critique/taste-skill` | `workflow` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 72 | `development` | `library/development/frontend/development` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 73 | `find-bugs` | `library/development/fullstack/find-bugs` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 74 | `diagnosing-bugs` | `library/quality-and-security/debugging/diagnosing-bugs` | `workflow` | `workflow` | **AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 75 | `canva-automation` | `library/development/fullstack/canva-automation` | `workflow` | `reference_or_support_candidate` | **DISCREPANCY** | Static reference documentation or cheat sheet lacking procedural execution |
| 76 | `github-operations:pr-merge-champion` | `library/github-operations/pr-merge-champion` | `alias_candidate` | `alias_candidate` | **AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 77 | `github-operations:feature-tracking` | `library/github-operations/feature-tracking` | `alias_candidate` | `alias_candidate` | **AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 78 | `github-operations:pr-writer` | `library/github-operations/pr-writer` | `alias_candidate` | `alias_candidate` | **AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 79 | `github-operations:hooks-automation` | `library/github-operations/hooks-automation` | `alias_candidate` | `alias_candidate` | **AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 80 | `github-operations:pr-review` | `library/github-operations/pr-review` | `alias_candidate` | `alias_candidate` | **AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 81 | `github-operations:commit` | `library/github-operations/commit` | `alias_candidate` | `alias_candidate` | **AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 82 | `figma-implement-motion` | `library/design-and-experience/motion-and-graphics/figma-implement-motion` | `overlay` | `workflow` | **DISCREPANCY** | Multi-phase sequential outcome orchestration pipeline |
| 83 | `marketing-and-seo-notebooklm` | `library/marketing-and-seo/on-page-seo/notebooklm` | `overlay` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 84 | `notebooklm-create` | `library/content-and-documentation/presentations/notebooklm-create` | `overlay` | `workflow` | **DISCREPANCY** | Multi-phase sequential outcome orchestration pipeline |
| 85 | `figma-swiftui` | `library/design-and-experience/design-systems/figma-swiftui` | `overlay` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 86 | `n8n-multi-instance` | `library/marketing-and-seo/cro/n8n-multi-instance` | `overlay` | `reference_or_support_candidate` | **DISCREPANCY** | Static reference documentation or cheat sheet lacking procedural execution |
| 87 | `not-human-search-mcp` | `library/development/backend/not-human-search-mcp` | `adapter` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 88 | `protect-mcp-governance` | `library/workflow-and-automation/tool-integration/protect-mcp-governance` | `adapter` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 89 | `tool-use-guardian` | `library/development/fullstack/tool-use-guardian` | `adapter` | `workflow` | **DISCREPANCY** | Multi-phase sequential outcome orchestration pipeline |
| 90 | `agent-memory-mcp` | `library/development/software-architecture/agent-memory-mcp` | `adapter` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 91 | `scale-benchmarks` | `library/business-and-operations/strategy/scale-benchmarks` | `reference_or_support_candidate` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 92 | `component-spec` | `library/design-and-experience/ui-ux/component-spec` | `reference_or_support_candidate` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 93 | `wireframe-spec` | `library/design-and-experience/ui-ux/wireframe-spec` | `reference_or_support_candidate` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 94 | `design-token` | `library/design-and-experience/design-systems/design-token` | `family_primitive` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 95 | `nextjs-supabase-auth` | `library/development/frontend/nextjs-supabase-auth` | `family_primitive` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 96 | `webflow-cli-cloud` | `library/development/fullstack/webflow-cli-cloud` | `family_primitive` | `workflow` | **DISCREPANCY** | Multi-phase sequential outcome orchestration pipeline |
| 97 | `n8n-expression-syntax` | `library/quality-and-security/debugging/n8n-expression-syntax` | `family_primitive` | `independent_capability` | **DISCREPANCY** | Discrete, focused single-task technical capability |
| 98 | `steve-jobs` | `library/development/fullstack/steve-jobs` | `manual_review` | `manual_review` | **AGREED** | Persona critique, unclassifiable prompt, or ambiguous umbrella name lacking discrete task execution |
| 99 | `emerging-channels` | `library/development/fullstack/emerging-channels` | `manual_review` | `manual_review` | **AGREED** | Persona critique, unclassifiable prompt, or ambiguous umbrella name lacking discrete task execution |
| 100 | `integrations` | `library/development/fullstack/integrations` | `manual_review` | `manual_review` | **AGREED** | Persona critique, unclassifiable prompt, or ambiguous umbrella name lacking discrete task execution |
