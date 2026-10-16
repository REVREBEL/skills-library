# ADR-002: Physical Ownership Model for Families and Overlays

- **Status**: Accepted
- **Deciders**: Architecture Working Group, REVREBEL Agent Platform Team
- **Date**: 2026-10-15
- **Related Issues**: [REV-126](https://linear.app/revrebel/issue/REV-126), [REV-150](https://linear.app/revrebel/issue/REV-150), [REV-127](https://linear.app/revrebel/issue/REV-127), [REV-128](https://linear.app/revrebel/issue/REV-128), [REV-129](https://linear.app/revrebel/issue/REV-129), [REV-130](https://linear.app/revrebel/issue/REV-130)
- **Normative References**: [ADR-001: Path-Independent Canonical Semantic Identity](file:///Users/garystringham/github-revrebel/skills-library/docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md), [Semantic Object Model Specification](file:///Users/garystringham/github-revrebel/skills-library/docs/architecture/semantic-object-model.md)

---

## 1. Context and Problem Statement

The REV-126 catalog census and REV-150 validation established that the repository contains 2,133 active skills organized across 10 functional top-level categories. However, physical repository organization suffers from four structural tensions:

1. **Cross-Cutting Platform Families**:
   External technology platforms and ecosystems (e.g., GitHub, Webflow, Figma, n8n, Hugging Face, 1Password, WordPress) naturally cut across multiple functional domains. For example:
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
   The census identified 15 duplicate leaf directory names between `library/github-operations/*` and the main category tree (`development/`, `infrastructure-and-ops/`, etc.), such as `commit`, `create-branch`, `feature-tracking`, `security-review`, and `pr-review`. While ADR-001 guarantees path-independent canonical identity disambiguation via immutable scopes (`github:commit` vs `development:commit`), their physical repository co-existence requires an unambiguous ownership and consolidation contract.

4. **Placement of Overlays and Adapters**:
   Overlays (`extends`) and Adapters (`adapts`) specialize or interface existing capabilities. The repository lacks a standard physical placement rule: should an overlay live beside its platform family, beside the base capability it extends, or in a global overlays registry?

How should physical repository storage be organized to maximize cohesion for platform maintainers, discoverability for domain practitioners, and stability for runtime tooling without violating path-independent canonical identity?

---

## 2. Decision: Hybrid Governed Physical Ownership Model

The architecture working group selects the **Hybrid Governed Physical Ownership Model**.

Under this model, the physical repository is organized into three standardized planes:
1. **Platform Hubs (`library/tools-and-platforms/<family-slug>/`)**: For qualifying platform ecosystems.
2. **Domain-Centric Functional Trees (`library/<category>/<subcategory>/`)**: For domain-general capabilities and workflows.
3. **Internal Meta Infrastructure (`library/meta-and-agent-skills/`)**: For universal agent workflows and lifecycle tooling.

```text
library/
├── tools-and-platforms/                # [Platform Hubs] Cohesive platform ecosystems
│   ├── github/                         # Former github-operations
│   │   ├── primitives/                 # Auth tokens, connection configs
│   │   ├── adapters/                   # gh CLI and MCP shims
│   │   ├── overlays/                   # GitHub-specific surface overlays
│   │   └── <operational-skills>/       # commit, create-branch, pr-writer...
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

### 2.5 Resolution Architecture for the 15 GitHub Duplicate Pairs

The 15 duplicate leaf pairs between `library/github-operations/*` and the main category tree are physically reconciled as follows:

| Duplicate Leaf Name | Main Tree Path | Proposed Physical Home | Canonical Identity | Semantic Resolution |
| :--- | :--- | :--- | :--- | :--- |
| `actions-debugger` | `infrastructure-and-ops/ci-cd` | `tools-and-platforms/github/actions-debugger` | `github:actions-debugger` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `advanced-workflows`| `workflow-and-automation/git-and-vcs` | `tools-and-platforms/github/advanced-workflows` | `github:advanced-workflows` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `commit` | `development/systems` | `tools-and-platforms/github/commit` & `development/systems/commit` | `github:commit` & `development:commit` | Dual-retention: `github:commit` owns GitHub PR/review commit integration; `development:commit` owns generic local Git staging. |
| `create-branch` | `development/systems` | `tools-and-platforms/github/create-branch` & `development/systems/create-branch` | `github:create-branch` & `development:create-branch` | Dual-retention: `github:create-branch` enforces repo issue-branch policies; `development:create-branch` provides generic VCS branching. |
| `create-issue-gate` | `business-and-operations/product-management` | `tools-and-platforms/github/create-issue-gate` | `github:create-issue-gate` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `feature-tracking` | `business-and-operations/product-management` | `tools-and-platforms/github/feature-tracking` | `github:feature-tracking` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `github` | `development/fullstack` | `tools-and-platforms/github/general-operations` | `github:general-operations` | Renamed to avoid root package collision; main tree instance aliased to canonical. |
| `hooks-automation` | `infrastructure-and-ops/ci-cd` | `tools-and-platforms/github/hooks-automation` | `github:hooks-automation` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `issue-creator` | `business-and-operations/product-management` | `tools-and-platforms/github/issue-creator` | `github:issue-creator` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `pr-merge-champion`| `development/fullstack` | `tools-and-platforms/github/pr-merge-champion` | `github:pr-merge-champion` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `pr-review` | `quality-and-security/code-review` | `tools-and-platforms/github/pr-review` | `github:pr-review` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `pr-writer` | `development/fullstack` | `tools-and-platforms/github/pr-writer` | `github:pr-writer` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `presence` | `marketing-and-seo/cro` | `tools-and-platforms/github/presence` | `github:presence` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `review-requests` | `development/fullstack` | `tools-and-platforms/github/review-requests` | `github:review-requests` | Platform operational workflow. Main-tree instance aliased to canonical. |
| `security-review` | `quality-and-security/security` | `tools-and-platforms/github/security-review` | `github:security-review` | Dual-retention: `github:security-review` owns Actions workflow exploit audit; `quality-and-security` owns generic code security analysis. |

**Key Invariant**:
- In all 15 cases, ADR-001 guarantees that canonical identities remain path-independent and globally unique across scopes (`github:*` vs `development:*` vs `quality-and-security:*`).
- For redundant cases, the secondary path is replaced with a single-hop `alias` object.
- For legitimate dual-domain cases (e.g. `commit`), both exist harmoniously because their identities are separated by provenance scope.

### 2.6 Migration Path for Anomalous Root Directories

1. **`library/github-operations/` -> `library/tools-and-platforms/github/`**:
   - The entire directory will be migrated into the structured platform hub.
   - Backward-compatible router references and alias manifests ensure existing targets and scripts continue operating during the migration window.
2. **`library/skills-create-manage-update/` -> `library/meta-and-agent-skills/skill-lifecycle/`**:
   - Lifecycle tooling is recognized as internal meta infrastructure, not a third-party vendor platform.
   - Migrates cleanly into `meta-and-agent-skills/skill-lifecycle/`.

### 2.7 Catalog Non-Destruction and Tooling Phasing

Pursuant to **Invariant 7 (Catalog Non-Destruction)**:
- REV-128 formulates the architectural decision, directory specifications, path contracts, and validation engine.
- **Physical disk movements under `library/**` are strictly deferred** to the execution tooling phases (REV-129 / REV-130).
- This ensures that active development, living library validation, and CI checks remain 100% green and unbroken while architectural consensus is established.

---

## 3. Evaluation of Alternatives

| Evaluation Dimension | Option 1: Strict Platform-First | Option 2: Strict Domain-First | Option 3: Hybrid Governed (Selected) | Option 4: Registry-First Flat |
| :--- | :--- | :--- | :--- | :--- |
| **Platform Maintainer DX** | High (all tools together) | Poor (tools scattered across 9 categories) | **High** (platform hub houses platform tools) | Poor (flat directory of 2,133 folders) |
| **Domain Discoverability** | Poor (domain tools hollowed out) | High (all tools in functional bins) | **High** (domain capabilities stay in domain) | None (requires compiler/tool query) |
| **Overlay Placement** | Forced into platform | Forced into domain | **Governed by lifecycle** (platform vs domain) | Flat/Virtual |
| **CODEOWNERS Alignment** | Good for platforms, poor for domains | Good for domains, poor for platforms | **Optimal** (clean platform and domain ownership) | Unusable |
| **Runtime Publication Compatibility** | Requires rewriting routers | Requires complex family queries | **Direct mapping** via registry compilation | High compilation overhead |

---

## 4. Consequences

### Positive Consequences
- **Platform Hub Cohesion**: Platform maintainers have a single, unified filesystem root for primitives, adapters, and dedicated platform workflows.
- **Domain Integrity**: Domain trees remain rich and discoverable, containing clean, vendor-agnostic capabilities.
- **Deterministic Overlay & Adapter Rules**: Overlays and adapters have strict, unambiguous physical homes preventing rogue, orphaned shims.
- **Duplicate Disambiguation**: The 15 GitHub duplicate pairs have clear, documented ownership and alias redirection mappings.
- **Elimination of Root Anomalies**: `github-operations` and `skills-create-manage-update` have structured, standardized target homes.

### Negative Consequences & Mitigation
- **Filesystem Migration Overhead**: Physical relocations require updating registry metadata (`physical_path`).
  * *Mitigation*: The path-independent canonical identity model (ADR-001) guarantees zero breakage of external references or URNs when files move.
- **Two Locations for Certain Concepts**: A developer might look for GitHub actions in either `tools-and-platforms/github` or `infrastructure-and-ops/ci-cd`.
  * *Mitigation*: Comprehensive router entries and automated search indexing in REV-130 ensure instant cross-referencing.
