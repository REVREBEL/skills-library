# ADR-002: Physical Ownership Model for Families and Overlays

- **Status**: Proposed (In Review)
- **Deciders**: Architecture Working Group, REVREBEL Agent Platform Team
- **Date**: 2026-10-15
- **Related Issues**: [REV-126](https://linear.app/revrebel/issue/REV-126), [REV-150](https://linear.app/revrebel/issue/REV-150), [REV-127](https://linear.app/revrebel/issue/REV-127), [REV-128](https://linear.app/revrebel/issue/REV-128), [REV-129](https://linear.app/revrebel/issue/REV-129), [REV-130](https://linear.app/revrebel/issue/REV-130)
- **Normative References**: [ADR-001: Path-Independent Canonical Semantic Identity](ADR-001-path-independent-canonical-identity.md), [Semantic Object Model Specification](../semantic-object-model.md)

---

## 1. Context and Problem Statement

The REV-126 catalog census and REV-150 validation established that the repository contains 2,133 active skills organized across 10 functional top-level categories. However, physical repository organization faces several structural tensions:

1. **Cross-Cutting Platform Families**:
   External technology platforms and ecosystems (e.g., GitHub, Webflow, Figma, n8n, Hugging Face, WordPress, Vercel, NotebookLM) naturally span multiple functional domains:
   - Webflow spans `design-and-experience`, `development`, `marketing-and-seo`, and `quality-and-security` (22 validated members across 9 subcategories).
   - Figma spans `design-and-experience` and `development` (14 validated members).
   - n8n spans 5 categories (14 validated members).
   Scattering a platform's tools across disparate directories hinders platform developer experience (DX), prevents shared authentication/primitive reuse, and complicates `CODEOWNERS` boundaries.

2. **Legacy Anomalous Top-Level Directories**:
   Two operational packages currently reside at the root of `library/` outside the 10 canonical categories:
   - `library/github-operations/*` (18 consolidated operational workflows).
   - `library/skills-create-manage-update/*` (13 lifecycle management skills).
   These directories bypass standard router hierarchies and require special-cased handling in runtime synchronizers.

3. **Physical Duplicate Leaf Collisions (The 15 GitHub Duplicate Pairs)**:
   The census identified 15 duplicate leaf directory names between `library/github-operations/*` and the main category tree (`development/`, `infrastructure-and-ops/`, etc.), such as `commit`, `create-branch`, `feature-tracking`, `security-review`, and `pr-review`. While ADR-001 guarantees path-independent canonical identity disambiguation via immutable scopes (`github:commit` vs `development:commit`), their physical repository co-existence requires an unambiguous ownership and consolidation framework.

4. **Placement of Overlays and Adapters**:
   Overlays (`extends`) and Adapters (`adapts`) specialize or interface existing capabilities. The repository lacks a standard physical placement rule: should an overlay live beside its platform family, beside the base capability it extends, or in a global overlays registry?

### Work-Order Scope Boundaries

To prevent premature closure of downstream architecture decisions, the responsibilities are strictly partitioned across work orders:

- **REV-128 (Current Work Order)**: Decides physical storage planes, directory structure conventions, overlay and adapter directory rules, path normalization contracts, and physical layout validation. Formulates candidate hypotheses for candidate duplicate collisions without issuing executable migration instructions or irreversible asset reclassifications.
- **REV-129 (Downstream)**: Decides formal platform family eligibility criteria, provider-adapter interface standards, and overlay attachment boundaries. All family listings in REV-128 are provisional candidates pending REV-129 adoption.
- **REV-130 (Downstream)**: Decides registry manifest schemas, router hierarchy contracts, dynamic alias resolution mechanics, and runtime projections. Any alias or router assumptions in REV-128 are provisional design models.

---

## 2. Decision: Hybrid Governed Physical Ownership Model

The architecture working group proposes the **Hybrid Governed Physical Ownership Model** as the candidate architecture for physical layout.

Under this model, the physical repository is partitioned into three standardized planes:
1. **Platform Hubs (`library/tools-and-platforms/<family-slug>/`)**: For qualifying platform ecosystems.
2. **Domain-Centric Functional Trees (`library/<category>/<subcategory>/`)**: For domain-general capabilities and workflows.
3. **Internal Meta Infrastructure (`library/meta-and-agent-skills/`)**: For universal agent workflows and lifecycle tooling.

```text
library/
├── tools-and-platforms/                # [Platform Hubs] Cohesive platform ecosystems
│   ├── github/                         # Candidate GitHub platform hub
│   │   ├── primitives/                 # Auth tokens, connection configs
│   │   ├── adapters/                   # gh CLI and MCP shims
│   │   ├── overlays/                   # GitHub-specific surface overlays
│   │   └── <operational-skills>/       # Platform operational workflows
│   ├── webflow/
│   ├── figma/
│   └── n8n/
├── development/                        # [Domain-Centric Trees] Functional disciplines
│   ├── frontend/
│   ├── backend/
│   ├── systems/
│   │   ├── commit/                     # Generic VCS commit (independent capability)
│   │   └── overlays/                   # Domain-hosted workflow specializations
│   └── ...
├── design-and-experience/
├── marketing-and-seo/
└── meta-and-agent-skills/              # [Meta Infrastructure]
    ├── skill-lifecycle/                # Former skills-create-manage-update
    └── adapters/                       # Shared platform-agnostic protocol shims
```

### 2.1 Platform Hub Specification (`library/tools-and-platforms/<family-slug>/`)

Platform ecosystems meeting Tier 1 Family criteria (defined in REV-126/150 and finalized in REV-129) are allocated a dedicated directory under `library/tools-and-platforms/<family-slug>/`.

**Contents of a Platform Hub**:
1. **`primitives/`**: Atomic building blocks, authentication schemas, connection configs, and environment templates shared across the platform's tools (e.g., `github:auth-token`, `webflow:api-client`).
2. **`adapters/`**: Protocol/transport bridges encapsulating the platform's API, CLI, or MCP servers (e.g., `github:gh-cli-adapter`, `webflow:designer-api-adapter`).
3. **`overlays/`**: Surface specializations extending generic cross-domain capabilities specifically for this platform host (e.g., `figma:implement-motion` extending `motion:implement-motion`).
4. **Platform Operations & Workflows**: Dedicated end-to-end tasks and operational workflows intrinsic to that platform (e.g., `github:pr-merge-champion`, `webflow:publish-blog`).

*(Note: Platform family eligibility and final qualification thresholds are governed by REV-129.)*

### 2.2 Domain-Centric Functional Trees (`library/<category>/<subcategory>/`)

The 10 canonical categories remain the authoritative physical home for all **domain-general** capabilities, primitives, references, and workflows.

**Rules for Domain Storage**:
- Capabilities that operate independently of a specific vendor platform (e.g., standard SQL parsing, CSS layout, accessibility auditing, algorithmic refactoring) MUST reside in their respective domain subcategories.
- Generic multi-provider workflows (e.g., generic VCS branching, continuous deployment pipelines, copy generation) reside in their respective functional domains.

### 2.3 Physical Placement Contracts for Overlays (`extends`)

An overlay decorates or specializes a base capability or workflow (`extends`). Its physical placement is governed by its primary maintenance lifecycle:

1. **Platform-Hosted Overlays**:
   - When an overlay exists primarily to adapt an external capability to a specific platform surface (e.g., `figma-implement-motion` or `webflow-code-component`), it resides in the platform hub:
     ```text
     library/tools-and-platforms/<family-slug>/overlays/<overlay-slug>/SKILL.md
     ```
   - Rationale: The overlay is maintained by the platform team and depends on platform-specific APIs and design tokens.
2. **Domain-Hosted Overlays**:
   - When an overlay specializes a domain workflow for an internal domain variant (e.g., a high-security variant of a standard backend deployment workflow), it resides in an `overlays/` subfolder within that subcategory:
     ```text
     library/<category>/<subcategory>/overlays/<overlay-slug>/SKILL.md
     ```
3. **Overlay Depth Invariant (Physical & Semantic)**:
   - Overlays MUST NOT be nested within other overlays on disk. No directory path may contain multiple `overlays/` segments (`.../overlays/.../overlays/...` is strictly forbidden).

### 2.4 Physical Placement Contracts for Adapters (`adapts`)

Adapters provide pure transport or protocol translation (MCP, CLI, REST):
1. **Platform-Specific Adapters**: Reside in `library/tools-and-platforms/<family-slug>/adapters/<adapter-slug>/`.
2. **Platform-Agnostic Adapters**: Reside in `library/meta-and-agent-skills/adapters/<adapter-slug>/`.
3. **Encapsulation Rule**: Adapters must contain zero domain business logic. They encapsulate protocol manifests, command-line arguments, and error-handling shims.

### 2.5 Direction-Neutral Duplicate Evaluation Framework (The 15 GitHub Duplicate Pairs)

The 15 duplicate leaf directory names between `library/github-operations/*` and the main category tree are treated as **unresolved candidate collision pairs**. 

REV-128 establishes a direction-neutral evaluation framework that formulates explicit candidate hypotheses for each pair. **REV-128 does not issue final authoritative adjudications or executable migration instructions for individual catalog assets.** Each candidate pair remains unresolved until a separately documented, source-backed semantic review is adjudicated and approved in downstream work orders (REV-129/REV-130).

The 15 candidate collision pairs and their evaluation hypotheses:

| Candidate Leaf Name | Main-Tree Path | Candidate Platform Path | Candidate Canonical ID Hypotheses | Candidate Evaluation Hypotheses |
| :--- | :--- | :--- | :--- | :--- |
| `actions-debugger` | `infrastructure-and-ops/ci-cd` | `tools-and-platforms/github/actions-debugger` | `infrastructure-and-ops:actions-debugger` vs `github:actions-debugger` | **Hypothesis A**: Consolidate into platform hub as specialized GitHub Actions debugger, aliasing main-tree path.<br>**Hypothesis B**: Retain in CI/CD domain if tool generalizes across multiple CI runners. |
| `advanced-workflows` | `workflow-and-automation/git-and-vcs` | `tools-and-platforms/github/advanced-workflows` | `workflow-and-automation:advanced-workflows` vs `github:advanced-workflows` | **Hypothesis A**: Platform operational workflow owned by GitHub hub with alias in git-and-vcs.<br>**Hypothesis B**: Generic Git recovery/rebase workflow retained in git-and-vcs with platform overlay. |
| `commit` | `development/systems` | `tools-and-platforms/github/commit` | `development:commit` and `github:commit` | **Hypothesis A (Dual-Retention)**: Distinct functional semantics: `development:commit` provides generic Git staging/commit primitives, while `github:commit` handles PR review commit integration and issue linking.<br>**Hypothesis B**: Merge into single generic commit capability with GitHub adapter. |
| `create-branch` | `development/systems` | `tools-and-platforms/github/create-branch` | `development:create-branch` and `github:create-branch` | **Hypothesis A (Dual-Retention)**: Distinct functional semantics: `development:create-branch` provides generic VCS branch creation, while `github:create-branch` enforces repo-level branch-naming rules, issue linking, and remote tracking.<br>**Hypothesis B**: Generalize into single branch workflow with platform config. |
| `create-issue-gate` | `business-and-operations/product-management` | `tools-and-platforms/github/create-issue-gate` | `business-and-operations:create-issue-gate` vs `github:create-issue-gate` | **Hypothesis A**: Consolidate into GitHub hub as issue-first delivery workflow, aliasing product-management path.<br>**Hypothesis B**: Retain in product-management as vendor-neutral requirement gate interfacing via adapters. |
| `feature-tracking` | `business-and-operations/product-management` | `tools-and-platforms/github/feature-tracking` | `business-and-operations:feature-tracking` vs `github:feature-tracking` | **Hypothesis A**: Consolidate into GitHub hub as repo-native project/issue tracking workflow.<br>**Hypothesis B**: Retain in product-management as generic feature memory capability. |
| `github` | `development/fullstack` | `tools-and-platforms/github/general-operations` | `development:github` vs `github:general-operations` | **Hypothesis A**: Rename leaf to `general-operations` to eliminate package root collision (`github:general-operations`).<br>**Hypothesis B**: Split into atomic capability components distributed across platform hub. |
| `hooks-automation` | `infrastructure-and-ops/ci-cd` | `tools-and-platforms/github/hooks-automation` | `infrastructure-and-ops:hooks-automation` vs `github:hooks-automation` | **Hypothesis A**: Consolidate into GitHub hub as Actions/webhook automation workflow.<br>**Hypothesis B**: Retain in CI/CD as local/server Git hooks orchestrator. |
| `issue-creator` | `business-and-operations/product-management` | `tools-and-platforms/github/issue-creator` | `business-and-operations:issue-creator` vs `github:issue-creator` | **Hypothesis A**: Consolidate into GitHub hub with main-tree alias.<br>**Hypothesis B**: Retain in product-management with issue tracker adapter interface. |
| `pr-merge-champion` | `development/fullstack` | `tools-and-platforms/github/pr-merge-champion` | `development:pr-merge-champion` vs `github:pr-merge-champion` | **Hypothesis A**: Consolidate into GitHub hub as platform PR merge workflow.<br>**Hypothesis B**: Retain in development/fullstack as generic code review champion. |
| `pr-review` | `quality-and-security/code-review` | `tools-and-platforms/github/pr-review` | `quality-and-security:pr-review` vs `github:pr-review` | **Hypothesis A**: Consolidate into GitHub hub with alias in code-review.<br>**Hypothesis B**: Retain in quality-and-security as core code review capability, using GitHub adapter for API transport. |
| `pr-writer` | `development/fullstack` | `tools-and-platforms/github/pr-writer` | `development:pr-writer` vs `github:pr-writer` | **Hypothesis A**: Consolidate into GitHub hub as PR description authoring workflow.<br>**Hypothesis B**: Retain in development as generic changeset documentation generator. |
| `presence` | `marketing-and-seo/cro` | `tools-and-platforms/github/presence` | `marketing-and-seo:presence` vs `github:presence` | **Hypothesis A**: Consolidate into GitHub hub as repository README/discoverability workflow.<br>**Hypothesis B**: Retain in marketing-and-seo as digital footprint optimization skill. |
| `review-requests` | `development/fullstack` | `tools-and-platforms/github/review-requests` | `development:review-requests` vs `github:review-requests` | **Hypothesis A**: Consolidate into GitHub hub as PR review assignment workflow.<br>**Hypothesis B**: Retain in development as peer review routing workflow. |
| `security-review` | `quality-and-security/security` | `tools-and-platforms/github/security-review` | `quality-and-security:security-review` and `github:security-review` | **Hypothesis A (Dual-Retention)**: Distinct functional semantics: `quality-and-security:security-review` provides deep static application code audit, while `github:security-review` audits GitHub Actions workflow exploit vectors and repository permission postures.<br>**Hypothesis B**: Generalize security audit into single workflow with platform-specific checklists. |

**Invariants Upheld**:
- In all candidate scenarios, ADR-001 path-independent canonical identities (`<scope>:<slug>`) prevent collision even if files temporarily share a leaf directory name.
- No directory moves, alias links, or file renames are executed in REV-128.
- Downstream adjudication in REV-129/REV-130 will decide each pair on its empirical merits based on source text analysis.

### 2.6 Proposed Migration Path for Anomalous Root Directories

1. **`library/github-operations/` -> `library/tools-and-platforms/github/`**:
   - The 18 consolidated workflows are planned to transition to the structured platform hub.
   - Backward-compatible router references and alias manifests in REV-130 will guarantee zero runtime breakage.
2. **`library/skills-create-manage-update/` -> `library/meta-and-agent-skills/skill-lifecycle/`**:
   - Lifecycle tooling represents internal meta-infrastructure, not a third-party vendor platform.
   - Planned relocation under `meta-and-agent-skills/skill-lifecycle/`.

### 2.7 Catalog Non-Destruction and Tooling Phasing

Pursuant to **Invariant 7 (Catalog Non-Destruction)**:
- REV-128 formulates the architectural decision, directory specifications, path contracts, and validation engine.
- **Physical disk movements under `library/**` are strictly deferred** to the execution tooling phases (REV-129 / REV-130).
- This ensures that active development, living library validation, and CI checks remain 100% green and unbroken while architectural consensus is established.

---

## 3. Platform Stress-Test Matrix and Evaluation of Alternatives

To evaluate the robustness of the Hybrid Governed Model, we analyze how it and three alternative physical storage architectures handle seven diverse platform ecosystems representing varying maturity, domain dispersion, and technical integration profiles:

1. **Archetype 1: Centralized Platform-First Ownership** (`library/platforms/<platform>/*` for all platform-mentioning skills)
2. **Archetype 2: Functional-Domain Ownership** (`library/<category>/<subcategory>/*` with zero platform hubs)
3. **Archetype 3: Registry-First Flat Storage** (`library/skills/<slug>/` with all relationships in metadata)
4. **Archetype 4: Hybrid Governed Ownership (Proposed)** (Platform hubs for platform-specific assets; domain trees for vendor-neutral capabilities; lifecycle-governed overlays)

### 3.1 Comparative Evaluation by Platform

```text
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| Platform & Profile| 1. Centralized Platform    | 2. Functional-Domain        | 3. Registry-First Flat      | 4. Hybrid Governed          |
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| NotebookLM        | Absorbs generic markdown   | NotebookLM shims scattered  | 2,133 flat directories;     | Hub: NotebookLM MCP & API   |
| (AI, Research,    | & summarization tools;     | across data-and-ai, writing;| impossible manual browsing; | shims; Domain: Generic RAG  |
| Content)          | hollows out domain trees.  | breaks shared auth tokens.  | high metadata overhead.     | & summarization capabilities|
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| Figma             | Design-system domain lost; | Motion, tokens, and plugins | Flat storage obscures       | Hub: Figma REST/Plugin shims|
| (Design, Tokens,  | design-token primitives    | split across 3 categories;  | component relationships and | & overlays; Domain: Generic |
| Frontend Motion)  | inaccessible to generic UI.| no unified figma DX root.   | design-system primitives.   | design-system & motion tools|
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| Webflow           | All CMS, CRO, and CSS moved| 22 skills scattered across  | Tooling must parse JSON to  | Hub: Webflow designer shims |
| (CMS, Frontend,   | to Webflow; vendor lock-in | 9 subcategories; team cannot| identify Webflow bundle; no | & sync workflows; Domain:   |
| SEO, Marketing)   | for generic web publishing.| set CODEOWNERS cleanly.     | filesystem cohesion.        | Vendor-neutral CSS/HTML/SEO |
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| n8n               | Generic webhook & cron     | Workflow automation tools   | Flat structure fails to     | Hub: n8n node templates &   |
| (Automation, API, | pipelines pulled into n8n; | split from devops; no shared| reflect hub-and-spoke       | server shims; Domain:       |
| Integration)      | obscures open standards.   | credential management.      | integration patterns.       | General ETL & API pipelines |
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| GitHub            | Sucks all Git, CI, and PR  | 18 operational workflows    | Doesn't resolve duplicate   | Hub: GitHub Actions/PR hub; |
| (VCS, CI/CD, PRs, | capabilities into vendor   | scattered or left in root   | directory leaf collisions   | Domain: Generic VCS/review; |
| Operations)       | hub; breaks generic VCS.   | anomaly (github-operations).| on disk.                    | Dual-retention candidates.  |
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| WordPress         | Pulls all blogging, theme, | PHP, SEO, and CMS tools     | High search indexing cost   | Hub: WP-CLI/REST adapters;  |
| (CMS, PHP, SEO,   | and SEO tools into WP hub; | fragmented; maintenance of  | for simple platform         | Domain: Core content, PHP,  |
| Publishing)       | duplicates general SEO.    | WP ecosystem is cumbersome. | updates.                    | and general SEO audits.     |
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
| Vercel            | Absorbs generic serverless | Edge, serverless, and CI    | Lacks clear boundary        | Hub: Vercel deployment CLI  |
| (Deployment, Edge,| and DNS routing tools;     | tools split across ops/dev; | between cloud providers     | & preview shims; Domain:    |
| Serverless, Next) | conflates host with domain.| hard to track deployment.   | and local toolchains.       | Core cloud & serverless dev.|
+-------------------+----------------------------+-----------------------------+-----------------------------+-----------------------------+
```

### 3.2 Deep-Dive Stress Tests with Counterexamples

#### 1. NotebookLM (Research, Notes, AI Synthesis)
- **Profile**: Spans `data-and-ai/llm-and-rag`, `content-and-documentation/writing`, and `business-and-operations/research`.
- **Hybrid Placement**:
  - `tools-and-platforms/notebooklm/adapters/` hosts the NotebookLM MCP and unofficial API bridges.
  - `tools-and-platforms/notebooklm/primitives/` hosts notebook session configurations and source upload templates.
- **Counterexample (Must stay in Domain Tree)**:
  - `content-and-documentation/writing/source-synthesis`: Generic academic source synthesis must remain vendor-agnostic in the domain tree. It must NOT be moved into the NotebookLM hub.
- **Domain Overlay Placement**:
  - `content-and-documentation/writing/overlays/notebooklm-brief`: An overlay generating NotebookLM-tailored audio podcast briefs lives as a domain overlay or platform overlay depending on whether it relies on proprietary NotebookLM audio-overview formatting.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Swallows generic note-taking and source synthesis, forcing non-NotebookLM users into a vendor directory.
  - *Functional Domain*: Forces platform maintainers to patch MCP connectors across three separate functional subcategories.

#### 2. Figma (Design Systems, Vector Graphics, Motion)
- **Profile**: Spans `design-and-experience/design-systems`, `design-and-experience/motion-and-graphics`, and `development/frontend`.
- **Hybrid Placement**:
  - `tools-and-platforms/figma/adapters/` hosts Figma REST API tokens and plugin execution bridges.
  - `tools-and-platforms/figma/primitives/` hosts design token schemas and FigJam template parsers.
  - `tools-and-platforms/figma/overlays/` hosts `figma-implement-motion` specializing generic motion design for Figma prototypes.
- **Counterexample (Must stay in Domain Tree)**:
  - `design-and-experience/motion-and-graphics/motion-principles`: Core animation curve mathematics, easing functions, and choreographic rules are completely platform-independent and must remain in the domain tree.
- **Domain Overlay Placement**:
  - `development/frontend/overlays/tailwind-from-figma`: Frontend component scaffold specialized for Figma token export.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Strips design-system foundations from developers who do not use Figma (e.g., developers using Penpot, Sketch, or pure code).
  - *Functional Domain*: Scatters Figma token sync scripts, plugin builders, and canvas helpers across disparate folders.

#### 3. Webflow (Visual CMS, No-Code Development, Landing Pages)
- **Profile**: Spans 22 skills across 9 subcategories in `development`, `design-and-experience`, and `marketing-and-seo`.
- **Hybrid Placement**:
  - `tools-and-platforms/webflow/` houses Webflow Designer API shims, CMS collections synchronization scripts, and Webflow Apps CLI tooling.
- **Counterexample (Must stay in Domain Tree)**:
  - `marketing-and-seo/cro/landing-page-audit`: Generic conversion rate optimization principles, visual hierarchy checklists, and readability rubrics must remain in `marketing-and-seo`.
  - `development/frontend/responsive-grid`: Pure CSS grid layout algorithms must never be vendorized into Webflow.
- **Domain Overlay Placement**:
  - `marketing-and-seo/cro/overlays/webflow-slider-audit`: An overlay auditing Webflow's specific native slider DOM structure for mobile responsiveness.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Creates severe vendor capture where general web design and CRO principles are conflated with Webflow's proprietary CMS limitations.
  - *Functional Domain*: Severely degrades Webflow developer DX by fragmenting 22 tightly integrated site-building skills across 4 parent categories.

#### 4. n8n (Visual Node Automation, Integration Pipelines)
- **Profile**: Spans `workflow-and-automation`, `data-and-ai`, and `infrastructure-and-ops` (14 skills).
- **Hybrid Placement**:
  - `tools-and-platforms/n8n/` houses custom node scaffolding tools, n8n instance deployment configurations, and workflow export/import validators.
- **Counterexample (Must stay in Domain Tree)**:
  - `workflow-and-automation/task-orchestration/dag-scheduler`: Fundamental directed acyclic graph execution logic and retry/backoff policies belong strictly in the domain tree.
- **Domain Overlay Placement**:
  - `data-and-ai/data-engineering/overlays/n8n-webhook-ingest`: Ingestion pipeline overlay adapting webhook payloads via n8n's expression syntax.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Conflates standard workflow automation with n8n's specific node execution engine.
  - *Functional Domain*: Makes it impossible to package a comprehensive n8n node developer toolkit in a single git directory.

#### 5. GitHub (VCS, CI/CD, Code Review, Repository Governance)
- **Profile**: Spans `infrastructure-and-ops/ci-cd`, `development/systems`, `quality-and-security/security`, `quality-and-security/code-review`, and `workflow-and-automation/git-and-vcs`.
- **Hybrid Placement**:
  - `tools-and-platforms/github/` provides a coherent home for GitHub Actions workflows, `gh` CLI adapters, Octokit integration shims, and PR automation workflows.
- **Counterexample (Must stay in Domain Tree)**:
  - `development/systems/commit`: Generic Git staging, interactive rebase, and tree hash calculations belong to standard VCS and must remain independent of GitHub.
  - `quality-and-security/security/code-audit`: Static taint analysis, dependency vulnerability scanning, and secret detection belong in the domain tree, agnostic of GitHub Advanced Security.
- **Domain Overlay Placement**:
  - `quality-and-security/code-review/overlays/github-pr-comments`: Code review rubric specialized to generate inline GitHub PR review comment payloads.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Conflates open-source Git protocols with GitHub commercial enterprise features.
  - *Functional Domain*: Leaves the 18 consolidated workflows in `library/github-operations` as an unintegrated anomaly or fractures them across 5 directories.

#### 6. WordPress (Headless & Traditional CMS, Theme/Plugin Engineering)
- **Profile**: Spans `development/backend` (PHP/WP-CLI), `development/frontend` (Gutenberg blocks), and `marketing-and-seo/on-page-seo`.
- **Hybrid Placement**:
  - `tools-and-platforms/wordpress/` houses WP-CLI adapters, theme boilerplate scaffolds, and REST API sync tooling.
- **Counterexample (Must stay in Domain Tree)**:
  - `development/backend/php-psr-standards`: General PHP coding standards, PSR-12 formatters, and Composer dependency practices belong in `development/backend`.
  - `marketing-and-seo/on-page-seo/schema-org-markup`: JSON-LD semantic markup generation must remain vendor-neutral.
- **Domain Overlay Placement**:
  - `marketing-and-seo/on-page-seo/overlays/yoast-rankmath-schema`: Overlay generating Schema specifically tailored for WordPress SEO plugin filters.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Pulls generic PHP engineering and standard SEO practices into legacy CMS silos.
  - *Functional Domain*: Forces WordPress plugin developers to manage files spread across backend, frontend, and marketing trees.

#### 7. Vercel (Edge Functions, Preview Deployments, Serverless Frameworks)
- **Profile**: Spans `infrastructure-and-ops/cloud-platforms`, `infrastructure-and-ops/ci-cd`, and `development/frontend`.
- **Hybrid Placement**:
  - `tools-and-platforms/vercel/` houses Vercel CLI wrappers, preview deployment comment bots, and project link adapters.
- **Counterexample (Must stay in Domain Tree)**:
  - `development/frontend/nextjs-app-router`: Next.js core application router architecture belongs in `development/frontend` (can be deployed on Node, AWS, or Docker, not solely Vercel).
  - `infrastructure-and-ops/server-management/dns-propagation`: Generic DNS record management belongs in ops.
- **Domain Overlay Placement**:
  - `infrastructure-and-ops/ci-cd/overlays/vercel-preview-gate`: CI/CD pipeline overlay that gates staging promotion on Vercel preview URLs.
- **Reason for Rejecting Alternatives**:
  - *Centralized Platform*: Falsely couples Next.js/React framework capabilities exclusively to Vercel hosting.
  - *Functional Domain*: Spreads deployment scripts, edge middleware adapters, and CLI tooling across separate devops trees.

---

## 4. Consequences and Governance

### Positive Consequences
- **Platform Hub Cohesion**: Platform maintainers have a single, unified filesystem root for primitives, adapters, and dedicated platform workflows.
- **Domain Integrity**: Domain trees remain rich and discoverable, containing clean, vendor-agnostic capabilities.
- **Deterministic Overlay & Adapter Rules**: Overlays and adapters have strict, unambiguous physical homes preventing rogue, orphaned shims.
- **Direction-Neutral Duplicate Protection**: The 15 GitHub candidate collision pairs are explicitly modeled with candidate hypotheses without forcing premature or irreversible catalog changes.
- **Pathway to Eliminate Root Anomalies**: `github-operations` and `skills-create-manage-update` have structured, standardized proposed target homes.

### Negative Consequences & Mitigation
- **Filesystem Migration Overhead**: Physical relocations require updating registry metadata (`physical_path`).
  * *Mitigation*: The path-independent canonical identity model (ADR-001) guarantees zero breakage of external references or URNs when files move.
- **Two Locations for Certain Concepts**: A developer might look for GitHub actions in either `tools-and-platforms/github` or `infrastructure-and-ops/ci-cd`.
  * *Mitigation*: Comprehensive router entries and automated search indexing in REV-130 ensure instant cross-referencing.
