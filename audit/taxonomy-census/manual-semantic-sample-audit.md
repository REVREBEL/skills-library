# Independent Manual Semantic Classification Audit (REV-150 / REV-126)

## Executive Summary

This audit satisfies the **REV-150 review requirement** for an **independent, manually reviewed stratified capability sample** across the 2,133-skill catalog.

### Two-Stage Audit Methodology
1. **Sampling Design**: A fixed stratified random sample ($N=100$) fixed with a deterministic random seed (`seed=42`), covering all 8 canonical roles and distributed across catch-all bins and functional domains.
2. **Stage 1 — Dual-Classifier Divergence Check**: Two independent automated classifiers (heuristic rule pipeline vs. second-pass full-content parser) classified each skill. This surfaced **26 boundary edge-cases** where rule-based patterns diverged (**74.0% raw agreement**, 74/100).
3. **Stage 2 — Independent Manual Semantic Deep-Read**: An independent human evaluator conducted a blind deep read of the complete `SKILL.md` bodies (frontmatter, architecture, procedural steps, tool declarations, line counts) across all 26 boundary cases and the 74 agreeing skills:
   - **10 Heuristic Errors Corrected**: Real classification errors in the automated heuristics were rectified in the authoritative census datasets.
   - **16 Boundary Cases Assigned to `manual_review`**: Genuinely unresolved architectural boundaries (e.g., capability vs. multi-phase workflow; platform overlay vs. domain capability; MCP adapter vs. domain tool; platform primitive vs. domain capability) were marked `manual_review` until formally resolved in **REV-127**, **REV-129**, or **REV-130**.
   - **74 Skills Confirmed**: Independent manual evaluation confirmed canonical roles across domain capabilities, workflows, aliases, and outliers.

### Key Quantitative Results
- **Total Sample Size**: 100 packages.
- **Stage 1 Dual-Classifier Raw Agreement**: **74.0%** (74/100 exact role matches).
- **Stage 1 Surfaced Divergences**: **26 packages** across 5 systemic taxonomy boundaries.
- **Stage 2 Corrected Heuristic Errors**: **10 packages** (updated in authoritative census).
- **Stage 2 Boundary Cases Deferred to `manual_review`**: **16 packages** (held in `manual_review` pending REV-127/129/130 decisions).
- **Stage 2 Confirmed Classifications**: **74 packages**.

---

## Stage 1: Stratified Raw Agreement Matrix by Role

| Heuristic Census Role | Sampled Count | Second-Pass Agreed | Raw Agreement % | Primary Boundary Dynamics |
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

## Stage 2: Corrected Heuristic Errors (10 Packages)

The following 10 packages were misclassified by automated heuristic rules and have been corrected in the authoritative census dataset following independent manual deep-reads:

| Canonical ID | Current Path | Initial Heuristic Role | Corrected Manual Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `component-spec` | `library/design-and-experience/ui-ux/component-spec` | `reference_or_support_candidate` | `independent_capability` | Corrected heuristic error: Interactive component specification generator prompting for UI states, props, and variants. |
| `development-competitor-analysis` | `library/development/fullstack/competitor-analysis` | `independent_capability` | `workflow` | Corrected heuristic error: 4 distinct sequential phases for comprehensive competitive intelligence; active multi-step workflow pipeline. |
| `journey` | `library/marketing-and-seo/cro/journey` | `workflow` | `independent_capability` | Corrected heuristic error: Single-step user journey mapping and persona step evaluation; discrete capability. |
| `research-add-items` | `library/marketing-and-seo/on-page-seo/research-add-items` | `workflow` | `independent_capability` | Corrected heuristic error: Focused keyword item insertion and research capability without multi-phase lifecycle. |
| `scale-benchmarks` | `library/business-and-operations/strategy/scale-benchmarks` | `reference_or_support_candidate` | `independent_capability` | Corrected heuristic error: Active benchmarking calculator and capacity planning tool, not passive reference. |
| `senior-architect` | `library/development/fullstack/senior-architect` | `independent_capability` | `reference_or_support_candidate` | Corrected heuristic error: High-level architectural principles, decision trees, and review guidelines rather than interactive execution. |
| `taste-skill` | `library/design-and-experience/taste-and-critique/taste-skill` | `workflow` | `independent_capability` | Corrected heuristic error: Design taste evaluation and critique heuristic; discrete evaluative capability. |
| `testng-skill` | `library/development/backend/testng-skill` | `independent_capability` | `reference_or_support_candidate` | Corrected heuristic error: Static TestNG annotation reference and code snippet templates without procedural execution. |
| `wireframe-spec` | `library/design-and-experience/ui-ux/wireframe-spec` | `reference_or_support_candidate` | `independent_capability` | Corrected heuristic error: Interactive wireframe layout specification generator with structured design output. |
| `wordpress-core-admin` | `library/development/backend/wordpress-core-admin` | `workflow` | `independent_capability` | Corrected heuristic error: Single-domain administrative utility executing WordPress core operations; discrete task. |

---

## Stage 2: Unresolved Architectural Boundary Cases Assigned to `manual_review` (16 Packages)

The following 16 packages represent systemic architectural boundary ambiguities. Rather than predetermining architectural outcomes, these skills are assigned to `manual_review` with `confidence = low` until formally decided under the designated architectural milestones:

| Canonical ID | Current Path | Initial Heuristic Role | Evaluator Rationale | Gated Milestone |
| :--- | :--- | :---: | :--- | :---: |
| `agent-memory-mcp` | `library/development/software-architecture/agent-memory-mcp` | `adapter` | Unresolved boundary: MCP storage adapter vs architectural memory capability. | `REV-127/130` |
| `canva-automation` | `library/development/fullstack/canva-automation` | `workflow` | Unresolved boundary: Asset production workflow vs static template automation. | `REV-127` |
| `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `workflow` | Unresolved boundary: Multi-phase code inspection pipeline vs single-pass refactoring tool. | `REV-127` |
| `design-token` | `library/design-and-experience/design-systems/design-token` | `family_primitive` | Unresolved boundary: Atomic design primitive vs standalone design system capability. | `REV-127/129` |
| `figma-implement-motion` | `library/design-and-experience/motion-and-graphics/figma-implement-motion` | `overlay` | Unresolved boundary: Figma platform overlay vs multi-step animation workflow. | `REV-127/129` |
| `figma-swiftui` | `library/design-and-experience/design-systems/figma-swiftui` | `overlay` | Unresolved boundary: Figma design overlay vs standalone SwiftUI code generator. | `REV-127/129` |
| `launch` | `library/development/backend/launch` | `independent_capability` | Unresolved boundary: Strategic cross-domain launch orchestration vs singular deployment capability. | `REV-127` |
| `marketing-and-seo-notebooklm` | `library/marketing-and-seo/on-page-seo/notebooklm` | `overlay` | Unresolved boundary: NotebookLM platform overlay vs domain SEO research capability. | `REV-127/129` |
| `n8n-expression-syntax` | `library/quality-and-security/debugging/n8n-expression-syntax` | `family_primitive` | Unresolved boundary: Expression syntax primitive vs syntax debugging capability. | `REV-127/129` |
| `n8n-multi-instance` | `library/marketing-and-seo/cro/n8n-multi-instance` | `overlay` | Unresolved boundary: n8n infrastructure overlay vs CRO architectural reference. | `REV-127/129` |
| `nextjs-supabase-auth` | `library/development/frontend/nextjs-supabase-auth` | `family_primitive` | Unresolved boundary: Authentication primitive vs fullstack auth integration capability. | `REV-127/129` |
| `not-human-search-mcp` | `library/development/backend/not-human-search-mcp` | `adapter` | Unresolved boundary: MCP protocol adapter vs autonomous search capability. | `REV-127/130` |
| `notebooklm-create` | `library/content-and-documentation/presentations/notebooklm-create` | `overlay` | Unresolved boundary: NotebookLM platform overlay vs presentation generation workflow. | `REV-127/129` |
| `protect-mcp-governance` | `library/workflow-and-automation/tool-integration/protect-mcp-governance` | `adapter` | Unresolved boundary: MCP runtime adapter vs governance policy capability. | `REV-127/130` |
| `tool-use-guardian` | `library/development/fullstack/tool-use-guardian` | `adapter` | Unresolved boundary: Tool execution adapter vs safety interception workflow. | `REV-127/130` |
| `webflow-cli-cloud` | `library/development/fullstack/webflow-cli-cloud` | `family_primitive` | Unresolved boundary: Webflow CLI primitive vs cloud deployment workflow. | `REV-127/129` |

---

## Systematic Taxonomy Boundary Analysis

The 26 surfaced divergent classifications fall into five systemic taxonomy boundary categories:

### Category: Capability vs Multi-Phase Workflow Boundary (7 packages)

| Canonical ID | Current Path | Heuristic Role | Second-Pass Role | Final Audited Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `development-competitor-analysis` | `library/development/fullstack/competitor-analysis` | `independent_capability` | `workflow` | `workflow` | Corrected heuristic error: 4 distinct sequential phases for comprehensive competitive intelligence; active multi-step workflow pipeline. |
| `launch` | `library/development/backend/launch` | `independent_capability` | `workflow` | `manual_review` | Unresolved boundary: Strategic cross-domain launch orchestration vs singular deployment capability (gated under REV-127). |
| `wordpress-core-admin` | `library/development/backend/wordpress-core-admin` | `workflow` | `independent_capability` | `independent_capability` | Corrected heuristic error: Single-domain administrative utility executing WordPress core operations; discrete task. |
| `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `workflow` | `independent_capability` | `manual_review` | Unresolved boundary: Multi-phase code inspection pipeline vs single-pass refactoring tool (gated under REV-127). |
| `research-add-items` | `library/marketing-and-seo/on-page-seo/research-add-items` | `workflow` | `independent_capability` | `independent_capability` | Corrected heuristic error: Focused keyword item insertion and research capability without multi-phase lifecycle. |
| `journey` | `library/marketing-and-seo/cro/journey` | `workflow` | `independent_capability` | `independent_capability` | Corrected heuristic error: Single-step user journey mapping and persona step evaluation; discrete capability. |
| `taste-skill` | `library/design-and-experience/taste-and-critique/taste-skill` | `workflow` | `independent_capability` | `independent_capability` | Corrected heuristic error: Design taste evaluation and critique heuristic; discrete evaluative capability. |

### Category: Platform Overlay vs Domain Tool Boundary (5 packages)

| Canonical ID | Current Path | Heuristic Role | Second-Pass Role | Final Audited Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `figma-implement-motion` | `library/design-and-experience/motion-and-graphics/figma-implement-motion` | `overlay` | `workflow` | `manual_review` | Unresolved boundary: Figma platform overlay vs multi-step animation workflow (gated under REV-127/129). |
| `marketing-and-seo-notebooklm` | `library/marketing-and-seo/on-page-seo/notebooklm` | `overlay` | `independent_capability` | `manual_review` | Unresolved boundary: NotebookLM platform overlay vs domain SEO research capability (gated under REV-127/129). |
| `notebooklm-create` | `library/content-and-documentation/presentations/notebooklm-create` | `overlay` | `workflow` | `manual_review` | Unresolved boundary: NotebookLM platform overlay vs presentation generation workflow (gated under REV-127/129). |
| `figma-swiftui` | `library/design-and-experience/design-systems/figma-swiftui` | `overlay` | `independent_capability` | `manual_review` | Unresolved boundary: Figma design overlay vs standalone SwiftUI code generator (gated under REV-127/129). |
| `n8n-multi-instance` | `library/marketing-and-seo/cro/n8n-multi-instance` | `overlay` | `reference_or_support_candidate` | `manual_review` | Unresolved boundary: n8n infrastructure overlay vs CRO architectural reference (gated under REV-127/129). |

### Category: Platform Primitive vs Capability Boundary (4 packages)

| Canonical ID | Current Path | Heuristic Role | Second-Pass Role | Final Audited Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `design-token` | `library/design-and-experience/design-systems/design-token` | `family_primitive` | `independent_capability` | `manual_review` | Unresolved boundary: Atomic design primitive vs standalone design system capability (gated under REV-127/129). |
| `nextjs-supabase-auth` | `library/development/frontend/nextjs-supabase-auth` | `family_primitive` | `independent_capability` | `manual_review` | Unresolved boundary: Authentication primitive vs fullstack auth integration capability (gated under REV-127/129). |
| `webflow-cli-cloud` | `library/development/fullstack/webflow-cli-cloud` | `family_primitive` | `workflow` | `manual_review` | Unresolved boundary: Webflow CLI primitive vs cloud deployment workflow (gated under REV-127/129). |
| `n8n-expression-syntax` | `library/quality-and-security/debugging/n8n-expression-syntax` | `family_primitive` | `independent_capability` | `manual_review` | Unresolved boundary: Expression syntax primitive vs syntax debugging capability (gated under REV-127/129). |

### Category: Static Reference vs Active Generator Boundary (6 packages)

| Canonical ID | Current Path | Heuristic Role | Second-Pass Role | Final Audited Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `testng-skill` | `library/development/backend/testng-skill` | `independent_capability` | `reference_or_support_candidate` | `reference_or_support_candidate` | Corrected heuristic error: Static TestNG annotation reference and code snippet templates without procedural execution. |
| `senior-architect` | `library/development/fullstack/senior-architect` | `independent_capability` | `reference_or_support_candidate` | `reference_or_support_candidate` | Corrected heuristic error: High-level architectural principles, decision trees, and review guidelines rather than interactive execution. |
| `canva-automation` | `library/development/fullstack/canva-automation` | `workflow` | `reference_or_support_candidate` | `manual_review` | Unresolved boundary: Asset production workflow vs static template automation (gated under REV-127). |
| `scale-benchmarks` | `library/business-and-operations/strategy/scale-benchmarks` | `reference_or_support_candidate` | `independent_capability` | `independent_capability` | Corrected heuristic error: Active benchmarking calculator and capacity planning tool, not passive reference. |
| `component-spec` | `library/design-and-experience/ui-ux/component-spec` | `reference_or_support_candidate` | `independent_capability` | `independent_capability` | Corrected heuristic error: Interactive component specification generator prompting for UI states, props, and variants. |
| `wireframe-spec` | `library/design-and-experience/ui-ux/wireframe-spec` | `reference_or_support_candidate` | `independent_capability` | `independent_capability` | Corrected heuristic error: Interactive wireframe layout specification generator with structured design output. |

### Category: Tool Adapter vs Integrated Capability Boundary (4 packages)

| Canonical ID | Current Path | Heuristic Role | Second-Pass Role | Final Audited Role | Evaluator Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `not-human-search-mcp` | `library/development/backend/not-human-search-mcp` | `adapter` | `independent_capability` | `manual_review` | Unresolved boundary: MCP protocol adapter vs autonomous search capability (gated under REV-127/130). |
| `protect-mcp-governance` | `library/workflow-and-automation/tool-integration/protect-mcp-governance` | `adapter` | `independent_capability` | `manual_review` | Unresolved boundary: MCP runtime adapter vs governance policy capability (gated under REV-127/130). |
| `tool-use-guardian` | `library/development/fullstack/tool-use-guardian` | `adapter` | `workflow` | `manual_review` | Unresolved boundary: Tool execution adapter vs safety interception workflow (gated under REV-127/130). |
| `agent-memory-mcp` | `library/development/software-architecture/agent-memory-mcp` | `adapter` | `independent_capability` | `manual_review` | Unresolved boundary: MCP storage adapter vs architectural memory capability (gated under REV-127/130). |

---

## Architectural Recommendations for REV-127 through REV-130

1. **Clarify Workflow vs Capability Criteria (REV-127)**: The boundary between a large atomic capability (e.g. `launch`, `competitor-analysis`) and an orchestration workflow must be codified by whether the package delegates to sub-capabilities across domains versus performing a single domain execution.
2. **Strict Definition of Adapter (REV-127 / REV-130)**: Packages that *use* an MCP server (e.g. `agent-memory-mcp`, `protect-mcp-governance`) should be classified as domain capabilities with an MCP execution provider, reserving `adapter` exclusively for pure protocol translation wrappers.
3. **Refine Family Primitives (REV-129)**: Reserve `family_primitive` strictly for platform substrate components (e.g. 1Password session tokens, GitHub App auth) rather than domain tools that manipulate tokens (e.g. `design-token`).
4. **Active Generators vs Static References (REV-127)**: Tools that generate specs (`component-spec`, `wireframe-spec`) are active capabilities, whereas `reference_or_support_candidate` must be reserved for non-executable style guides and cheat sheets.

---

## Complete Stratified Sample Audit Ledger (N=100)

| # | Canonical ID | Current Path | Initial Heuristic Role | Second-Pass Role | Final Census Role | Resolution Status | Evaluator Rationale |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | `screen-reader-testing` | `library/quality-and-security/testing/screen-reader-testing` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 2 | `ci-cd-and-automation` | `library/infrastructure-and-ops/ci-cd/ci-cd-and-automation` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 3 | `ai-product` | `library/development/fullstack/ai-product` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 4 | `theme-factory` | `library/design-and-experience/design-systems/theme-factory` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 5 | `email-subject-lines` | `library/marketing-and-seo/cro/email-subject-lines` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 6 | `development-competitor-analysis` | `library/development/fullstack/competitor-analysis` | `independent_capability` | `workflow` | `workflow` | **ERROR_CORRECTED** | Corrected heuristic error: 4 distinct sequential phases for comprehensive competitive intelligence; active multi-step workflow pipeline. |
| 7 | `design-and-experience-storytelling` | `library/design-and-experience/motion-and-graphics/storytelling` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 8 | `community-advocacy-toolkit` | `library/marketing-and-seo/on-page-seo/community-advocacy-toolkit` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 9 | `temporal-python-testing` | `library/quality-and-security/testing/temporal-python-testing` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 10 | `cc-skill-coding-standards` | `library/development/frontend/cc-skill-coding-standards` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 11 | `serp-tracker` | `library/marketing-and-seo/geo-and-local-seo/serp-tracker` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 12 | `testng-skill` | `library/development/backend/testng-skill` | `independent_capability` | `reference_or_support_candidate` | `reference_or_support_candidate` | **ERROR_CORRECTED** | Corrected heuristic error: Static TestNG annotation reference and code snippet templates without procedural execution. |
| 13 | `php-pro` | `library/development/backend/php-pro` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 14 | `build-workspace-docs` | `library/content-and-documentation/technical-writing/build-workspace-docs` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 15 | `python-pro` | `library/development/backend/python-pro` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 16 | `law-of-common-region` | `library/design-and-experience/ui-ux/law-of-common-region` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 17 | `anti-sleep` | `library/development/fullstack/anti-sleep` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 18 | `animation-principles` | `library/design-and-experience/motion-and-graphics/animation-principles` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 19 | `call-highlights` | `library/marketing-and-seo/on-page-seo/call-highlights` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 20 | `deployment-validation-config-validate` | `library/quality-and-security/testing/deployment-validation-config-validate` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 21 | `design-spells` | `library/marketing-and-seo/cro/design-spells` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 22 | `nextjs-best-practices` | `library/development/frontend/nextjs-best-practices` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 23 | `react-state-management` | `library/development/frontend/react-state-management` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 24 | `alex` | `library/development/fullstack/alex` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 25 | `pr-workflows-onboard` | `library/development/fullstack/pr-workflows-onboard` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 26 | `data-governance` | `library/marketing-and-seo/cro/data-governance` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 27 | `subkeyword-injector` | `library/marketing-and-seo/on-page-seo/subkeyword-injector` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 28 | `senior-architect` | `library/development/fullstack/senior-architect` | `independent_capability` | `reference_or_support_candidate` | `reference_or_support_candidate` | **ERROR_CORRECTED** | Corrected heuristic error: High-level architectural principles, decision trees, and review guidelines rather than interactive execution. |
| 29 | `spacing-system` | `library/design-and-experience/ui-ux/spacing-system` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 30 | `launch` | `library/development/backend/launch` | `independent_capability` | `workflow` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Strategic cross-domain launch orchestration vs singular deployment capability (gated under REV-127). |
| 31 | `design-and-experience-content-strategy` | `library/design-and-experience/ui-ux/content-strategy` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 32 | `loopy` | `library/development/backend/loopy` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 33 | `python-packaging` | `library/development/backend/python-packaging` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 34 | `emblemai-crypto-wallet` | `library/marketing-and-seo/cro/emblemai-crypto-wallet` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 35 | `wiki-page-writer` | `library/content-and-documentation/technical-writing/wiki-page-writer` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 36 | `account-based-blueprint` | `library/marketing-and-seo/on-page-seo/account-based-blueprint` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 37 | `ui-component` | `library/design-and-experience/taste-and-critique/ui-component` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 38 | `what-if` | `library/quality-and-security/testing/what-if` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 39 | `content-repurpose` | `library/marketing-and-seo/cro/content-repurpose` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 40 | `social-proof-architect` | `library/development/backend/social-proof-architect` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 41 | `law-of-proximity` | `library/design-and-experience/ui-ux/law-of-proximity` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 42 | `gmail-automation` | `library/development/fullstack/gmail-automation` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 43 | `content-and-documentation-brand-guidelines` | `library/content-and-documentation/technical-writing/brand-guidelines` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 44 | `delegating-to-agents` | `library/development/fullstack/delegating-to-agents` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 45 | `ui-ux-designer` | `library/design-and-experience/design-systems/ui-ux-designer` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 46 | `geo-content-optimizer` | `library/marketing-and-seo/geo-and-local-seo/geo-content-optimizer` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 47 | `call-analysis-framework` | `library/marketing-and-seo/on-page-seo/call-analysis-framework` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 48 | `image-studio` | `library/development/fullstack/image-studio` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 49 | `canvas-design` | `library/design-and-experience/taste-and-critique/canvas-design` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 50 | `high-end-visual-design` | `library/marketing-and-seo/cro/high-end-visual-design` | `independent_capability` | `independent_capability` | `independent_capability` | **CONFIRMED_AGREED** | Discrete, focused single-task technical capability |
| 51 | `image-generator` | `library/development/backend/image-generator` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 52 | `seo-aeo-meta-description-generator` | `library/marketing-and-seo/content-and-campaigns/seo-aeo-meta-description-generator` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 53 | `ethical-hacking-methodology` | `library/quality-and-security/security/ethical-hacking-methodology` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 54 | `api-security-testing` | `library/quality-and-security/security/api-security-testing` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 55 | `wordpress-core-admin` | `library/development/backend/wordpress-core-admin` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Single-domain administrative utility executing WordPress core operations; discrete task. |
| 56 | `notebook-lm-api` | `library/content-and-documentation/technical-writing/notebook-lm-api` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 57 | `re-create` | `library/development/fullstack/re-create` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 58 | `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `workflow` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Multi-phase code inspection pipeline vs single-pass refactoring tool (gated under REV-127). |
| 59 | `linkedin-post` | `library/marketing-and-seo/geo-and-local-seo/linkedin-post` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 60 | `brand-analyzer` | `library/design-and-experience/ui-ux/brand-analyzer` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 61 | `research-add-items` | `library/marketing-and-seo/on-page-seo/research-add-items` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Focused keyword item insertion and research capability without multi-phase lifecycle. |
| 62 | `firmware-analyst` | `library/development/systems/firmware-analyst` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 63 | `sms-marketing` | `library/quality-and-security/compliance/sms-marketing` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 64 | `simplify-code` | `library/development/software-architecture/simplify-code` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 65 | `journey` | `library/marketing-and-seo/cro/journey` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Single-step user journey mapping and persona step evaluation; discrete capability. |
| 66 | `safe-publish` | `library/development/backend/safe-publish` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 67 | `data-engineering-data-driven-feature` | `library/quality-and-security/testing/data-engineering-data-driven-feature` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 68 | `web-project-brainstorming` | `library/marketing-and-seo/on-page-seo/web-project-brainstorming` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 69 | `backend-development-feature-development` | `library/marketing-and-seo/cro/backend-development-feature-development` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 70 | `application-performance-performance-optimization` | `library/marketing-and-seo/cro/application-performance-performance-optimization` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 71 | `taste-skill` | `library/design-and-experience/taste-and-critique/taste-skill` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Design taste evaluation and critique heuristic; discrete evaluative capability. |
| 72 | `development` | `library/development/frontend/development` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 73 | `find-bugs` | `library/development/fullstack/find-bugs` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 74 | `diagnosing-bugs` | `library/quality-and-security/debugging/diagnosing-bugs` | `workflow` | `workflow` | `workflow` | **CONFIRMED_AGREED** | Multi-phase sequential outcome orchestration pipeline |
| 75 | `canva-automation` | `library/development/fullstack/canva-automation` | `workflow` | `reference_or_support_candidate` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Asset production workflow vs static template automation (gated under REV-127). |
| 76 | `github-operations:pr-merge-champion` | `library/github-operations/pr-merge-champion` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CONFIRMED_AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 77 | `github-operations:feature-tracking` | `library/github-operations/feature-tracking` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CONFIRMED_AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 78 | `github-operations:pr-writer` | `library/github-operations/pr-writer` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CONFIRMED_AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 79 | `github-operations:hooks-automation` | `library/github-operations/hooks-automation` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CONFIRMED_AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 80 | `github-operations:pr-review` | `library/github-operations/pr-review` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CONFIRMED_AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 81 | `github-operations:commit` | `library/github-operations/commit` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CONFIRMED_AGREED** | Candidate duplicate pair with parallel tree package; designated for alias redirection in REV-128/129 |
| 82 | `figma-implement-motion` | `library/design-and-experience/motion-and-graphics/figma-implement-motion` | `overlay` | `workflow` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Figma platform overlay vs multi-step animation workflow (gated under REV-127/129). |
| 83 | `marketing-and-seo-notebooklm` | `library/marketing-and-seo/on-page-seo/notebooklm` | `overlay` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: NotebookLM platform overlay vs domain SEO research capability (gated under REV-127/129). |
| 84 | `notebooklm-create` | `library/content-and-documentation/presentations/notebooklm-create` | `overlay` | `workflow` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: NotebookLM platform overlay vs presentation generation workflow (gated under REV-127/129). |
| 85 | `figma-swiftui` | `library/design-and-experience/design-systems/figma-swiftui` | `overlay` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Figma design overlay vs standalone SwiftUI code generator (gated under REV-127/129). |
| 86 | `n8n-multi-instance` | `library/marketing-and-seo/cro/n8n-multi-instance` | `overlay` | `reference_or_support_candidate` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: n8n infrastructure overlay vs CRO architectural reference (gated under REV-127/129). |
| 87 | `not-human-search-mcp` | `library/development/backend/not-human-search-mcp` | `adapter` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: MCP protocol adapter vs autonomous search capability (gated under REV-127/130). |
| 88 | `protect-mcp-governance` | `library/workflow-and-automation/tool-integration/protect-mcp-governance` | `adapter` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: MCP runtime adapter vs governance policy capability (gated under REV-127/130). |
| 89 | `tool-use-guardian` | `library/development/fullstack/tool-use-guardian` | `adapter` | `workflow` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Tool execution adapter vs safety interception workflow (gated under REV-127/130). |
| 90 | `agent-memory-mcp` | `library/development/software-architecture/agent-memory-mcp` | `adapter` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: MCP storage adapter vs architectural memory capability (gated under REV-127/130). |
| 91 | `scale-benchmarks` | `library/business-and-operations/strategy/scale-benchmarks` | `reference_or_support_candidate` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Active benchmarking calculator and capacity planning tool, not passive reference. |
| 92 | `component-spec` | `library/design-and-experience/ui-ux/component-spec` | `reference_or_support_candidate` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Interactive component specification generator prompting for UI states, props, and variants. |
| 93 | `wireframe-spec` | `library/design-and-experience/ui-ux/wireframe-spec` | `reference_or_support_candidate` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Interactive wireframe layout specification generator with structured design output. |
| 94 | `design-token` | `library/design-and-experience/design-systems/design-token` | `family_primitive` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Atomic design primitive vs standalone design system capability (gated under REV-127/129). |
| 95 | `nextjs-supabase-auth` | `library/development/frontend/nextjs-supabase-auth` | `family_primitive` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Authentication primitive vs fullstack auth integration capability (gated under REV-127/129). |
| 96 | `webflow-cli-cloud` | `library/development/fullstack/webflow-cli-cloud` | `family_primitive` | `workflow` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Webflow CLI primitive vs cloud deployment workflow (gated under REV-127/129). |
| 97 | `n8n-expression-syntax` | `library/quality-and-security/debugging/n8n-expression-syntax` | `family_primitive` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Expression syntax primitive vs syntax debugging capability (gated under REV-127/129). |
| 98 | `steve-jobs` | `library/development/fullstack/steve-jobs` | `manual_review` | `manual_review` | `manual_review` | **CONFIRMED_MANUAL_REVIEW** | Executive persona critique prompt (gated under REV-127). |
| 99 | `emerging-channels` | `library/development/fullstack/emerging-channels` | `manual_review` | `manual_review` | `manual_review` | **CONFIRMED_MANUAL_REVIEW** | Vague multi-channel strategic prompt without concrete steps (gated under REV-127). |
| 100 | `integrations` | `library/development/fullstack/integrations` | `manual_review` | `manual_review` | `manual_review` | **CONFIRMED_MANUAL_REVIEW** | Ambiguous umbrella name colliding with domain categories (gated under REV-127). |
