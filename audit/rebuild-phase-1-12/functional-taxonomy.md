# Functional Taxonomy & Destination Architecture (Phase 05)

## 1. Executive Summary

Phase 05 establishes the destination functional taxonomy for the Agent Skills library rebuild. Adhering strictly to the architectural directive of **map first, move later**, this phase designs a clean, shallow, capability-driven category hierarchy without performing premature physical file moves, merges, splits, or rewrites.

### Reconciliation Summary

- **Total Source Skills in Inventory**: **2,331**
- **Quarantined Skills (Excluded from Active Destinations)**: **45**
- **Retained Skills Mapped**: exactly **2,286** (100% coverage)
- **Top-Level Functional Categories**: **10**
- **Planned Routers**: **55** (1 Master Root Router, 10 Category Routers, 44 Subcategory Routers)

## 2. The Classification Constitution & Core Rules

> [!IMPORTANT]
> **The Primary Operating Rule**: Classify by the skill's primary user outcome, not by the tool it uses or the mechanism by which it performs the work.

### Single Canonical Home (No Duplication)
Each retained skill is assigned exactly one canonical destination directory. Cross-domain relationships (e.g. accessibility audits spanning testing and design, full-stack design systems, automated CI deployments) are represented cleanly through routers, metadata, and cross-references rather than duplicating skills.

## 3. Disambiguation Decision Rules

To prevent classification drift across overlapping boundaries, the following concrete decision rules govern domain placement:

| Workflow / Intent | Assigned Category | Exclusion Reason (Where It Does NOT Go) |
|---|---|---|
| **Figma component creation & UI kit** | `design-and-experience` | *Not `workflow-and-automation`* (Visual design is the primary user outcome; Figma is a design tool). |
| **GitHub Actions deployment pipeline** | `infrastructure-and-ops` | *Not `workflow-and-automation`* (Application deployment and hosting are the primary outcome). |
| **Linear issue triage automation** | `workflow-and-automation` | *Not `business-and-operations`* (Automated multi-step process orchestration is the primary job). |
| **Agent skill auditor & validator** | `meta-and-agent-skills` | *Not `quality-and-security`* (Governs agent skill lifecycle, not application software). |
| **SEO analytics pipeline & tracking** | `marketing-and-seo` | *Not `data-and-ai`* (Primary outcome is search ranking and audience growth analysis). |
| **Playwright E2E accessibility testing** | `quality-and-security` | *Not `design-and-experience`* (Verification and test suite execution is the primary job). |
| **PostgreSQL schema & query optimization** | `development` / `backend` | *Not `infrastructure-and-ops`* (Application database schema and data logic). |
| **Microservices architecture pattern** | `development` / `software-architecture` | *Not `design-and-experience`* (Software/system architecture belongs under development). |

## 4. Category Definitions & Boundaries

### `development`

- **Purpose**: Create, build, modify, and refactor software architectures, backend services, frontend applications, APIs, database schemas, and language idioms.
- **Exclusion Boundary**: Testing/verification workflows (belongs in `quality-and-security`) and pure visual styling design (belongs in `design-and-experience`).
- **Proposed Subcategories**: `fullstack`, `backend`, `frontend`, `software-architecture`, `systems`, `mobile`
- **Skill Count**: **715**

### `design-and-experience`

- **Purpose**: Craft visual interfaces, UI/UX workflows, design systems (Tailwind, Radix, Figma), styling taste, animations, motion graphics, and 3D assets.
- **Exclusion Boundary**: Backend system architecture (belongs in `development`) or pure application logic.
- **Proposed Subcategories**: `ui-ux`, `taste-and-critique`, `design-systems`, `motion-and-graphics`
- **Skill Count**: **385**

### `infrastructure-and-ops`

- **Purpose**: Provision, configure, deploy, host, and monitor cloud platforms, servers, CI/CD pipelines, containers, and operating systems.
- **Exclusion Boundary**: Standalone task workflow automation unrelated to hosting/cloud infrastructure.
- **Proposed Subcategories**: `cloud-platforms`, `containers-and-orchestration`, `server-management`, `observability`, `ci-cd`
- **Skill Count**: **56**

### `data-and-ai`

- **Purpose**: Model, fine-tune, analyze, query, and serve data, machine learning pipelines, LLM/RAG systems, embeddings, and analytics tracking.
- **Exclusion Boundary**: Agent skill lifecycle management or general application development.
- **Proposed Subcategories**: `llm-and-rag`, `analytics`, `machine-learning`, `data-engineering`, `vector-databases`
- **Skill Count**: **133**

### `quality-and-security`

- **Purpose**: Verify, test (unit, integration, E2E), diagnose, systematically debug, audit security, scan vulnerabilities, and ensure compliance.
- **Exclusion Boundary**: Feature creation and refactoring (belongs in `development`).
- **Proposed Subcategories**: `testing`, `debugging`, `compliance`, `security`
- **Skill Count**: **144**

### `marketing-and-seo`

- **Purpose**: Drive audience acquisition, search engine visibility (SEO/GEO), conversion rate optimization (CRO), social presence, and digital ads.
- **Exclusion Boundary**: General copywriting without marketing or search intent (belongs in `content-and-documentation`).
- **Proposed Subcategories**: `on-page-seo`, `cro`, `technical-seo`, `geo-and-local-seo`, `content-and-campaigns`
- **Skill Count**: **703**

### `business-and-operations`

- **Purpose**: Manage products, analyze market opportunities, model financial projections, optimize pricing, and ensure business/legal compliance.
- **Exclusion Boundary**: Internal engineering or agent development workflows.
- **Proposed Subcategories**: `strategy`, `startup-finance`, `legal-and-governance`, `product-management`
- **Skill Count**: **62**

### `content-and-documentation`

- **Purpose**: Produce technical documentation, articles, presentations, research summaries, and structured knowledge artifacts.
- **Exclusion Boundary**: Marketing copy and search optimization (belongs in `marketing-and-seo`).
- **Proposed Subcategories**: `technical-writing`, `presentations`, `research-and-synthesis`, `copywriting`
- **Skill Count**: **62**

### `workflow-and-automation`

- **Purpose**: Orchestrate multi-step task workflows, integrate external APIs/MCP tools, automate Git operations, and bridge external services.
- **Exclusion Boundary**: Domain-specific skills that merely use an automation script as a secondary tool.
- **Proposed Subcategories**: `tool-integration`, `task-orchestration`, `web-scraping`, `git-and-vcs`
- **Skill Count**: **18**

### `meta-and-agent-skills`

- **Purpose**: Author, audit, validate, optimize, benchmark, package, and govern agent skills and multi-agent systems.
- **Exclusion Boundary**: Application software development or external workflow tools.
- **Proposed Subcategories**: `skill-lifecycle`, `agent-architecture`, `skill-validation`
- **Skill Count**: **8**

## 5. Category Reconciliation Matrix

| Category | Subcategory | Count | % of Retained Library |
|---|---|---|---|
| **`business-and-operations`** | *(Total)* | **62** | **2.7%** |
| `business-and-operations` | `legal-and-governance` | 11 | 0.5% |
| `business-and-operations` | `product-management` | 9 | 0.4% |
| `business-and-operations` | `startup-finance` | 14 | 0.6% |
| `business-and-operations` | `strategy` | 28 | 1.2% |
| **`content-and-documentation`** | *(Total)* | **62** | **2.7%** |
| `content-and-documentation` | `copywriting` | 4 | 0.2% |
| `content-and-documentation` | `presentations` | 13 | 0.6% |
| `content-and-documentation` | `research-and-synthesis` | 5 | 0.2% |
| `content-and-documentation` | `technical-writing` | 40 | 1.7% |
| **`data-and-ai`** | *(Total)* | **133** | **5.8%** |
| `data-and-ai` | `analytics` | 40 | 1.7% |
| `data-and-ai` | `data-engineering` | 6 | 0.3% |
| `data-and-ai` | `llm-and-rag` | 52 | 2.3% |
| `data-and-ai` | `machine-learning` | 30 | 1.3% |
| `data-and-ai` | `vector-databases` | 5 | 0.2% |
| **`design-and-experience`** | *(Total)* | **385** | **16.8%** |
| `design-and-experience` | `design-systems` | 69 | 3.0% |
| `design-and-experience` | `motion-and-graphics` | 33 | 1.4% |
| `design-and-experience` | `taste-and-critique` | 86 | 3.8% |
| `design-and-experience` | `ui-ux` | 197 | 8.6% |
| **`development`** | *(Total)* | **715** | **31.3%** |
| `development` | `backend` | 159 | 7.0% |
| `development` | `frontend` | 57 | 2.5% |
| `development` | `fullstack` | 434 | 19.0% |
| `development` | `mobile` | 8 | 0.3% |
| `development` | `software-architecture` | 34 | 1.5% |
| `development` | `systems` | 23 | 1.0% |
| **`infrastructure-and-ops`** | *(Total)* | **56** | **2.4%** |
| `infrastructure-and-ops` | `ci-cd` | 6 | 0.3% |
| `infrastructure-and-ops` | `cloud-platforms` | 14 | 0.6% |
| `infrastructure-and-ops` | `containers-and-orchestration` | 14 | 0.6% |
| `infrastructure-and-ops` | `observability` | 16 | 0.7% |
| `infrastructure-and-ops` | `server-management` | 6 | 0.3% |
| **`marketing-and-seo`** | *(Total)* | **703** | **30.8%** |
| `marketing-and-seo` | `content-and-campaigns` | 40 | 1.7% |
| `marketing-and-seo` | `cro` | 231 | 10.1% |
| `marketing-and-seo` | `geo-and-local-seo` | 59 | 2.6% |
| `marketing-and-seo` | `on-page-seo` | 295 | 12.9% |
| `marketing-and-seo` | `technical-seo` | 78 | 3.4% |
| **`meta-and-agent-skills`** | *(Total)* | **8** | **0.3%** |
| `meta-and-agent-skills` | `agent-architecture` | 2 | 0.1% |
| `meta-and-agent-skills` | `skill-lifecycle` | 4 | 0.2% |
| `meta-and-agent-skills` | `skill-validation` | 2 | 0.1% |
| **`quality-and-security`** | *(Total)* | **144** | **6.3%** |
| `quality-and-security` | `compliance` | 24 | 1.0% |
| `quality-and-security` | `debugging` | 48 | 2.1% |
| `quality-and-security` | `security` | 22 | 1.0% |
| `quality-and-security` | `testing` | 50 | 2.2% |
| **`workflow-and-automation`** | *(Total)* | **18** | **0.8%** |
| `workflow-and-automation` | `git-and-vcs` | 1 | 0.0% |
| `workflow-and-automation` | `task-orchestration` | 4 | 0.2% |
| `workflow-and-automation` | `tool-integration` | 11 | 0.5% |
| `workflow-and-automation` | `web-scraping` | 2 | 0.1% |
| **TOTAL** | **All Categories** | **2286** | **100.0%** |

## 6. Structural Router Architecture

The rebuilt library will utilize a shallow, two-level routing architecture:

1. **Master Root Router** (`task-folder/agents/skills/SKILL.md`): Dispatches incoming high-level user tasks to the appropriate functional category router.
2. **Category Routers** (`task-folder/agents/skills/<category>/SKILL.md`): Parent routers that define category boundaries and route to specific subcategory routers or child skills.
3. **Subcategory Routers** (`task-folder/agents/skills/<category>/<subcategory>/SKILL.md`): Specialized cluster routers routing to focused child skills.

See [`router-map.csv`](./router-map.csv) for the complete directory inventory of planned routers.

## 7. Review Concerns & Future Structural Candidates

- **Medium Confidence Placements**: Broad fullstack skills assigned to `development/fullstack` that may benefit from future domain splitting during Phase 06.
- **Future Merge Candidates**: Highly similar CRO, UI kit, and SEO sub-techniques identified for potential consolidation during Phase 06/07.
- **Zero Unresolved Blockers**: All 2,286 skills possess a clear, unambiguous top-level functional category.
