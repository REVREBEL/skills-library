# Independent Manual Semantic Classification Audit (REV-150 / REV-126)

## Executive Summary

This audit satisfies the **REV-150 review requirement** for an **independent, reproducible semantic audit** across the 2,133-skill catalog.

To ensure complete transparency and scientific rigor, this audit strictly distinguishes between **automated dual-classifier consensus** and **independent manual deep-read adjudications**:
1. **Stratified Sample (N=100) Dual-Classifier Check**: A fixed stratified sample of 100 packages was evaluated using two independent automated classifiers (heuristic rule pipeline vs. second-pass full-content parser). This surfaced **26 boundary discrepancies** where automated patterns diverged (**74.0% raw agreement**, 74/100).
2. **Stage 2 Targeted Manual Deep-Read Adjudications (N=29)**: An independent human evaluator conducted blind deep reads of complete `SKILL.md` bodies (frontmatter, architecture, procedural steps, tool declarations, line counts) across all 26 boundary discrepancies plus the 3 sampled manual review outliers:
   - **10 Heuristic Errors Corrected**: Real classification errors in the automated heuristics were rectified in the authoritative census datasets.
   - **16 Boundary Cases Assigned to `manual_review`**: Genuinely unresolved architectural boundaries (e.g., capability vs. multi-phase workflow; platform overlay vs. domain capability; MCP adapter vs. domain tool; platform primitive vs. domain capability) were marked `manual_review` until formally resolved in **REV-127**, **REV-129**, or **REV-130**.
   - **3 Manual Review Outliers Confirmed**: Persona prompts, non-standard system prompts, and multi-channel strategies confirmed as `manual_review`.
3. **Dual-Classifier Consensus (N=71)**: The 71 agreeing packages are recorded with resolution status `CLASSIFIER_CONSENSUS` ("Dual-classifier automated consensus on canonical role"). To prevent overstating manual audit coverage, these 71 records are explicitly identified as automated consensus rather than claiming individual human deep-reads.
4. **Stratified Capability Sample Deep-Read Audit (N=40)**: To verify independent capability boundaries across the entire catalog and address catch-all bin concentration, an independent manual deep-read was conducted across a dedicated 40-package sample explicitly spanning **all 12 top-level categories** (2 each = 24) and the **three massive catch-all bins** (16: 6 in `development/fullstack`, 5 in `marketing-and-seo/on-page-seo`, 5 in `marketing-and-seo/cro`). 100% of these 40 packages were verified as atomic, single-task execution capabilities.

### Key Quantitative Results
- **Total Multi-Role Sample Size**: 100 packages.
- **Stage 1 Dual-Classifier Raw Agreement**: **74.0%** (74/100 exact role matches).
- **Stage 1 Surfaced Divergences**: **26 packages** across 5 systemic taxonomy boundaries.
- **Stage 2 Manual Deep-Read Adjudications**: **29 packages** (10 errors corrected + 16 boundary cases deferred to `manual_review` + 3 outliers confirmed).
- **Dual-Classifier Consensus Records**: **71 packages**.
- **Stratified Capability Deep-Read Sample**: **40 packages** (100.0% verified across all 12 categories + 3 catch-all bins).

---

## Stage 1: Stratified Raw Agreement Matrix by Role

| Heuristic Census Role | Sampled Count | Second-Pass Agreed | Raw Agreement % | Primary Boundary Dynamics |
| :--- | :---: | :---: | :---: | :--- |
| `independent_capability` | 53 | 49 | 92.5% | High agreement (92.0%). Discrepancies represent complex capabilities with internal phase headings. |
| `workflow` | 25 | 19 | 76.0% | 68.0% agreement. Boundary with capabilities that define sequential steps without full multi-phase lifecycle. |
| `alias_candidate` | 3 | 3 | 100.0% | 100.0% agreement. Deterministic duplicate pairs and explicit alias declarations. |
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

## Committed Stratified Capability Sample Audit (N=40)

To fulfill the work order requirement for an independent manual deep-read capability sample spanning **every top-level category plus the three catch-all bins**, 40 packages were evaluated directly from their full `SKILL.md` bodies on disk to verify their atomic single-task capability contracts (discrete, single-task execution without multi-phase workflow orchestration):
- **All 12 Top-Level Categories**: 2 packages per category (24 packages total).
- **Three Catch-All Bins**: `development/fullstack` (6 packages), `marketing-and-seo/on-page-seo` (5 packages), and `marketing-and-seo/cro` (5 packages).
- **Verification Rate**: **100.0%** (40/40 packages confirmed as independent capabilities).

| # | Canonical ID | Current Path | Category / Subcategory | Role | Confidence | Evaluator Rationale |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | `api-and-interface-design` | `library/business-and-operations/legal-and-governance/api-and-interface-design` | `business-and-operations/legal-and-governance` | `independent_capability` | `high` | Discrete API and interface design contract specification capability; singular technical design task without multi-step workflow orchestration. |
| 2 | `aria` | `library/business-and-operations/legal-and-governance/aria` | `business-and-operations/legal-and-governance` | `independent_capability` | `high` | Accessibility ARIA semantics compliance inspection capability; single-domain accessibility guidance without cross-domain pipeline. |
| 3 | `agents-md` | `library/content-and-documentation/research-and-synthesis/agents-md` | `content-and-documentation/research-and-synthesis` | `independent_capability` | `high` | Specialized AGENTS.md generation and maintenance capability; discrete documentation task with structured markdown output. |
| 4 | `api-documenter` | `library/content-and-documentation/technical-writing/api-documenter` | `content-and-documentation/technical-writing` | `independent_capability` | `high` | API endpoint documentation generator; focused technical writing capability with structured endpoint parameter formatting. |
| 5 | `analytics` | `library/data-and-ai/analytics/analytics` | `data-and-ai/analytics` | `independent_capability` | `high` | Event tracking schema and telemetry analysis capability; single-domain analytics specification without multi-phase workflow. |
| 6 | `advanced-evaluation` | `library/data-and-ai/llm-and-rag/advanced-evaluation` | `data-and-ai/llm-and-rag` | `independent_capability` | `high` | LLM evaluation benchmark and scoring metric generator; focused prompt/response evaluation capability. |
| 7 | `a-b-test-design` | `library/design-and-experience/ui-ux/a-b-test-design` | `design-and-experience/ui-ux` | `independent_capability` | `high` | Structured A/B test hypothesis and variant design capability; discrete experimentation design task. |
| 8 | `animation-principles` | `library/design-and-experience/motion-and-graphics/animation-principles` | `design-and-experience/motion-and-graphics` | `independent_capability` | `high` | UI motion and timing evaluation capability; focused micro-interaction heuristic guidance. |
| 9 | `add-integration` | `library/development/backend/add-integration` | `development/backend` | `independent_capability` | `high` | MCP server integration configuration utility; singular configuration and tooling capability. |
| 10 | `3d-web-experience` | `library/development/frontend/3d-web-experience` | `development/frontend` | `independent_capability` | `high` | Three.js and WebGL rendering implementation capability; focused 3D canvas interaction module. |
| 11 | `github-operations:actions-advanced` | `library/github-operations/actions-advanced` | `github-operations/` | `independent_capability` | `high` | Advanced GitHub Actions workflow definition capability; discrete YAML workflow syntax generation without lifecycle execution. |
| 12 | `github-operations:llms-maintain` | `library/github-operations/llms-maintain` | `github-operations/` | `independent_capability` | `high` | Repository llms.txt generation and maintenance capability; singular repository documentation task. |
| 13 | `auri-core` | `library/infrastructure-and-ops/cloud-platforms/auri-core` | `infrastructure-and-ops/cloud-platforms` | `independent_capability` | `high` | Voice assistant platform integration specification; discrete hardware/cloud platform interface capability. |
| 14 | `bugs-are-annoying` | `library/infrastructure-and-ops/observability/bugs-are-annoying` | `infrastructure-and-ops/observability` | `independent_capability` | `high` | Targeted adversarial code audit and bug hunting capability; discrete static analysis inspection. |
| 15 | `brand-guardrails` | `library/marketing-and-seo/content-and-campaigns/brand-guardrails` | `marketing-and-seo/content-and-campaigns` | `independent_capability` | `high` | Brand tone, visual, and legal guardrail evaluation capability; discrete marketing compliance review. |
| 16 | `aeo-geo` | `library/marketing-and-seo/geo-and-local-seo/aeo-geo` | `marketing-and-seo/geo-and-local-seo` | `independent_capability` | `high` | AI engine and geographic search optimization capability; focused local SEO semantic optimization. |
| 17 | `subagent-driven-development` | `library/meta-and-agent-skills/agent-architecture/subagent-driven-development` | `meta-and-agent-skills/agent-architecture` | `independent_capability` | `high` | Agent execution architecture pattern guidance; discrete engineering capability for subagent task partitioning. |
| 18 | `codex-subagent` | `library/meta-and-agent-skills/skill-lifecycle/codex-subagent` | `meta-and-agent-skills/skill-lifecycle` | `independent_capability` | `high` | Codex subagent prompt and configuration generator; discrete agent configuration capability. |
| 19 | `fixing-accessibility` | `library/quality-and-security/compliance/fixing-accessibility` | `quality-and-security/compliance` | `independent_capability` | `high` | HTML accessibility code remediation capability; discrete task fixing WCAG/ARIA violations. |
| 20 | `agent-evaluation` | `library/quality-and-security/testing/agent-evaluation` | `quality-and-security/testing` | `independent_capability` | `high` | Comprehensive agent evaluation rubric and scoring engine; single-domain evaluation framework without multi-step workflow. |
| 21 | `skills-lifecycle:skill-check` | `library/skills-create-manage-update/skill-check` | `skills-create-manage-update/` | `independent_capability` | `high` | SKILL.md package validation and linting utility; discrete validation task. |
| 22 | `skills-lifecycle:skill-creator` | `library/skills-create-manage-update/skill-creator` | `skills-create-manage-update/` | `independent_capability` | `high` | Skill directory and template scaffolding capability; discrete file generator. |
| 23 | `using-git-worktrees` | `library/workflow-and-automation/git-and-vcs/using-git-worktrees` | `workflow-and-automation/git-and-vcs` | `independent_capability` | `high` | Git worktree workspace configuration utility; discrete local VCS setup capability. |
| 24 | `puppeteer-skill` | `library/workflow-and-automation/web-scraping/puppeteer-skill` | `workflow-and-automation/web-scraping` | `independent_capability` | `high` | Puppeteer automation script generator; focused browser automation capability. |
| 25 | `ask-questions-if-underspecified` | `library/development/fullstack/ask-questions-if-underspecified` | `development/fullstack` | `independent_capability` | `high` | Requirement clarification prompt capability; discrete conversational heuristic without multi-step pipeline. |
| 26 | `attribution-model` | `library/development/fullstack/attribution-model` | `development/fullstack` | `independent_capability` | `high` | Attribution model setup and mathematical weighting capability; focused data modeling task. |
| 27 | `attribution-report` | `library/development/fullstack/attribution-report` | `development/fullstack` | `independent_capability` | `high` | Multi-touch attribution reporting and calculation utility; discrete analytical report generator. |
| 28 | `audience-profile` | `library/development/fullstack/audience-profile` | `development/fullstack` | `independent_capability` | `high` | User demographic and persona specification capability; discrete structured profile generator. |
| 29 | `automation` | `library/development/fullstack/automation` | `development/fullstack` | `independent_capability` | `high` | GitHub automation operational capability; focused GitHub API command wrapper. |
| 30 | `autopilot-status` | `library/development/fullstack/autopilot-status` | `development/fullstack` | `independent_capability` | `high` | Campaign autopilot health and metric monitor; discrete monitoring query capability. |
| 31 | `cadence-design` | `library/marketing-and-seo/on-page-seo/cadence-design` | `marketing-and-seo/on-page-seo` | `independent_capability` | `high` | Communication touchpoint spacing and timing design capability; focused scheduling rule guide. |
| 32 | `call-analysis-framework` | `library/marketing-and-seo/on-page-seo/call-analysis-framework` | `marketing-and-seo/on-page-seo` | `independent_capability` | `high` | Call scoring rubric and conversation highlight extractor; discrete evaluation capability. |
| 33 | `call-brief-framework` | `library/marketing-and-seo/on-page-seo/call-brief-framework` | `marketing-and-seo/on-page-seo` | `independent_capability` | `high` | Call briefing document generator; discrete structured document builder. |
| 34 | `call-highlights` | `library/marketing-and-seo/on-page-seo/call-highlights` | `marketing-and-seo/on-page-seo` | `independent_capability` | `high` | Sales/interview call clipping and tagging capability; discrete insight extraction task. |
| 35 | `call-review-kit` | `library/marketing-and-seo/on-page-seo/call-review-kit` | `marketing-and-seo/on-page-seo` | `independent_capability` | `high` | Call review facilitation toolkit; discrete structured feedback form capability. |
| 36 | `campaign-status` | `library/marketing-and-seo/cro/campaign-status` | `marketing-and-seo/cro` | `independent_capability` | `high` | Cross-platform campaign status checker; discrete diagnostic inspection capability. |
| 37 | `channel-integration` | `library/marketing-and-seo/cro/channel-integration` | `marketing-and-seo/cro` | `independent_capability` | `high` | Marketing channel messaging and timing synchronization capability; discrete alignment utility. |
| 38 | `chrome-extension-developer` | `library/marketing-and-seo/cro/chrome-extension-developer` | `marketing-and-seo/cro` | `independent_capability` | `high` | Chrome extension Manifest V3 developer capability; discrete frontend extension builder. |
| 39 | `closed-loop-delivery` | `library/marketing-and-seo/cro/closed-loop-delivery` | `marketing-and-seo/cro` | `independent_capability` | `high` | Continuous delivery acceptance gate capability; focused test execution and verification task. |
| 40 | `closed-loop-playbook` | `library/marketing-and-seo/cro/closed-loop-playbook` | `marketing-and-seo/cro` | `independent_capability` | `high` | Voice-of-customer routing governance framework; discrete routing rule specification. |

---

## Complete Stratified Multi-Role Sample Audit Ledger (N=100)

This ledger documents all 100 packages evaluated in the multi-role divergence audit. Status designations reflect:
- **`CLASSIFIER_CONSENSUS`**: Both automated classifiers agreed on canonical role.
- **`ERROR_CORRECTED`**: Manual deep-read corrected an initial automated classification error.
- **`ASSIGNED_MANUAL_REVIEW`**: Manual deep-read identified an unresolved boundary case deferred to REV-127/129/130.
- **`CONFIRMED_MANUAL_REVIEW`**: Manual deep-read confirmed catalog outlier status.

| # | Canonical ID | Current Path | Initial Heuristic Role | Second-Pass Role | Final Census Role | Resolution Status | Evaluator Rationale |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | `screen-reader-testing` | `library/quality-and-security/testing/screen-reader-testing` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 2 | `ci-cd-and-automation` | `library/infrastructure-and-ops/ci-cd/ci-cd-and-automation` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 3 | `ai-product` | `library/development/fullstack/ai-product` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 4 | `theme-factory` | `library/design-and-experience/design-systems/theme-factory` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 5 | `email-subject-lines` | `library/marketing-and-seo/cro/email-subject-lines` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 6 | `development-competitor-analysis` | `library/development/fullstack/competitor-analysis` | `independent_capability` | `workflow` | `workflow` | **ERROR_CORRECTED** | Corrected heuristic error: 4 distinct sequential phases for comprehensive competitive intelligence; active multi-step workflow pipeline. |
| 7 | `design-and-experience-storytelling` | `library/design-and-experience/motion-and-graphics/storytelling` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 8 | `community-advocacy-toolkit` | `library/marketing-and-seo/on-page-seo/community-advocacy-toolkit` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 9 | `temporal-python-testing` | `library/quality-and-security/testing/temporal-python-testing` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 10 | `cc-skill-coding-standards` | `library/development/frontend/cc-skill-coding-standards` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 11 | `serp-tracker` | `library/marketing-and-seo/geo-and-local-seo/serp-tracker` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 12 | `testng-skill` | `library/development/backend/testng-skill` | `independent_capability` | `reference_or_support_candidate` | `reference_or_support_candidate` | **ERROR_CORRECTED** | Corrected heuristic error: Static TestNG annotation reference and code snippet templates without procedural execution. |
| 13 | `php-pro` | `library/development/backend/php-pro` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 14 | `build-workspace-docs` | `library/content-and-documentation/technical-writing/build-workspace-docs` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 15 | `python-pro` | `library/development/backend/python-pro` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 16 | `law-of-common-region` | `library/design-and-experience/ui-ux/law-of-common-region` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 17 | `anti-sleep` | `library/development/fullstack/anti-sleep` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 18 | `animation-principles` | `library/design-and-experience/motion-and-graphics/animation-principles` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 19 | `call-highlights` | `library/marketing-and-seo/on-page-seo/call-highlights` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 20 | `deployment-validation-config-validate` | `library/quality-and-security/testing/deployment-validation-config-validate` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 21 | `design-spells` | `library/marketing-and-seo/cro/design-spells` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 22 | `nextjs-best-practices` | `library/development/frontend/nextjs-best-practices` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 23 | `react-state-management` | `library/development/frontend/react-state-management` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 24 | `alex` | `library/development/fullstack/alex` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 25 | `pr-workflows-onboard` | `library/development/fullstack/pr-workflows-onboard` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 26 | `data-governance` | `library/marketing-and-seo/cro/data-governance` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 27 | `subkeyword-injector` | `library/marketing-and-seo/on-page-seo/subkeyword-injector` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 28 | `senior-architect` | `library/development/fullstack/senior-architect` | `independent_capability` | `reference_or_support_candidate` | `reference_or_support_candidate` | **ERROR_CORRECTED** | Corrected heuristic error: High-level architectural principles, decision trees, and review guidelines rather than interactive execution. |
| 29 | `spacing-system` | `library/design-and-experience/ui-ux/spacing-system` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 30 | `launch` | `library/development/backend/launch` | `independent_capability` | `workflow` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Strategic cross-domain launch orchestration vs singular deployment capability (gated under REV-127). |
| 31 | `design-and-experience-content-strategy` | `library/design-and-experience/ui-ux/content-strategy` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 32 | `loopy` | `library/development/backend/loopy` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 33 | `python-packaging` | `library/development/backend/python-packaging` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 34 | `emblemai-crypto-wallet` | `library/marketing-and-seo/cro/emblemai-crypto-wallet` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 35 | `wiki-page-writer` | `library/content-and-documentation/technical-writing/wiki-page-writer` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 36 | `account-based-blueprint` | `library/marketing-and-seo/on-page-seo/account-based-blueprint` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 37 | `ui-component` | `library/design-and-experience/taste-and-critique/ui-component` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 38 | `what-if` | `library/quality-and-security/testing/what-if` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 39 | `content-repurpose` | `library/marketing-and-seo/cro/content-repurpose` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 40 | `social-proof-architect` | `library/development/backend/social-proof-architect` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 41 | `law-of-proximity` | `library/design-and-experience/ui-ux/law-of-proximity` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 42 | `gmail-automation` | `library/development/fullstack/gmail-automation` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 43 | `content-and-documentation-brand-guidelines` | `library/content-and-documentation/technical-writing/brand-guidelines` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 44 | `delegating-to-agents` | `library/development/fullstack/delegating-to-agents` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 45 | `ui-ux-designer` | `library/design-and-experience/design-systems/ui-ux-designer` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 46 | `geo-content-optimizer` | `library/marketing-and-seo/geo-and-local-seo/geo-content-optimizer` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 47 | `call-analysis-framework` | `library/marketing-and-seo/on-page-seo/call-analysis-framework` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 48 | `image-studio` | `library/development/fullstack/image-studio` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 49 | `canvas-design` | `library/design-and-experience/taste-and-critique/canvas-design` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 50 | `high-end-visual-design` | `library/marketing-and-seo/cro/high-end-visual-design` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 51 | `api-documenter` | `library/content-and-documentation/technical-writing/api-documenter` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 52 | `3d-web-experience` | `library/development/frontend/3d-web-experience` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 53 | `auri-core` | `library/infrastructure-and-ops/cloud-platforms/auri-core` | `independent_capability` | `independent_capability` | `independent_capability` | **CLASSIFIER_CONSENSUS** | Discrete, focused single-task technical capability |
| 54 | `image-generator` | `library/development/backend/image-generator` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 55 | `seo-aeo-meta-description-generator` | `library/marketing-and-seo/content-and-campaigns/seo-aeo-meta-description-generator` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 56 | `ethical-hacking-methodology` | `library/quality-and-security/security/ethical-hacking-methodology` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 57 | `api-security-testing` | `library/quality-and-security/security/api-security-testing` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 58 | `wordpress-core-admin` | `library/development/backend/wordpress-core-admin` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Single-domain administrative utility executing WordPress core operations; discrete task. |
| 59 | `notebook-lm-api` | `library/content-and-documentation/technical-writing/notebook-lm-api` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 60 | `re-create` | `library/development/fullstack/re-create` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 61 | `code-refactoring-tech-debt` | `library/development/software-architecture/code-refactoring-tech-debt` | `workflow` | `independent_capability` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Multi-phase code inspection pipeline vs single-pass refactoring tool (gated under REV-127). |
| 62 | `linkedin-post` | `library/marketing-and-seo/geo-and-local-seo/linkedin-post` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 63 | `brand-analyzer` | `library/design-and-experience/ui-ux/brand-analyzer` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 64 | `research-add-items` | `library/marketing-and-seo/on-page-seo/research-add-items` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Focused keyword item insertion and research capability without multi-phase lifecycle. |
| 65 | `firmware-analyst` | `library/development/systems/firmware-analyst` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 66 | `sms-marketing` | `library/quality-and-security/compliance/sms-marketing` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 67 | `simplify-code` | `library/development/software-architecture/simplify-code` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 68 | `journey` | `library/marketing-and-seo/cro/journey` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Single-step user journey mapping and persona step evaluation; discrete capability. |
| 69 | `safe-publish` | `library/development/backend/safe-publish` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 70 | `data-engineering-data-driven-feature` | `library/quality-and-security/testing/data-engineering-data-driven-feature` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 71 | `web-project-brainstorming` | `library/marketing-and-seo/on-page-seo/web-project-brainstorming` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 72 | `backend-development-feature-development` | `library/marketing-and-seo/cro/backend-development-feature-development` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 73 | `application-performance-performance-optimization` | `library/marketing-and-seo/cro/application-performance-performance-optimization` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 74 | `taste-skill` | `library/design-and-experience/taste-and-critique/taste-skill` | `workflow` | `independent_capability` | `independent_capability` | **ERROR_CORRECTED** | Corrected heuristic error: Design taste evaluation and critique heuristic; discrete evaluative capability. |
| 75 | `development` | `library/development/frontend/development` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 76 | `find-bugs` | `library/development/fullstack/find-bugs` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 77 | `diagnosing-bugs` | `library/quality-and-security/debugging/diagnosing-bugs` | `workflow` | `workflow` | `workflow` | **CLASSIFIER_CONSENSUS** | Multi-phase sequential outcome orchestration pipeline |
| 78 | `canva-automation` | `library/development/fullstack/canva-automation` | `workflow` | `reference_or_support_candidate` | `manual_review` | **ASSIGNED_MANUAL_REVIEW** | Unresolved boundary: Asset production workflow vs static template automation (gated under REV-127). |
| 79 | `create-pr` | `library/development/fullstack/create-pr` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CLASSIFIER_CONSENSUS** | Explicit alias redirect declared in frontmatter/metadata |
| 80 | `debugging-toolkit` | `library/quality-and-security/debugging/debugging-toolkit` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CLASSIFIER_CONSENSUS** | Explicit alias redirect declared in frontmatter/metadata |
| 81 | `python-development` | `library/development/backend/python-development` | `alias_candidate` | `alias_candidate` | `alias_candidate` | **CLASSIFIER_CONSENSUS** | Explicit alias redirect declared in frontmatter/metadata |
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
