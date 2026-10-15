# Semantic Object Model and Stable Identity Architecture

- **Author**: REVREBEL Agent Architecture Team
- **Status**: Formally Specified (Gated under REV-127)
- **Target Audience**: Platform Engineers, Agent Developers, Tooling Maintainers
- **Related Issues**: [REV-126](https://linear.app/revrebel/issue/REV-126), [REV-150](https://linear.app/revrebel/issue/REV-150), [REV-127](https://linear.app/revrebel/issue/REV-127), [REV-128](https://linear.app/revrebel/issue/REV-128), [REV-129](https://linear.app/revrebel/issue/REV-129), [REV-130](https://linear.app/revrebel/issue/REV-130)
- **Normative References**: [ADR-001: Path-Independent Canonical Semantic Identity](file:///Users/garystringham/github-revrebel/skills-library/docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md)

---

## 1. Architectural Overview

The **REVREBEL Semantic Object Model** defines the formal taxonomy, entity types, relationship graphs, and validation invariants governing all agent skills, platform integrations, workflows, and runtime artifacts in the repository.

Historically, skills were treated uniformly as generic markdown files stored in arbitrary directory paths. The **REV-126** catalog census and **REV-150** empirical validation demonstrated that the 2,133-skill catalog naturally partitions into distinct semantic roles with widely differing execution behaviors, token densities (averaging a 36.9% differential between capabilities and workflows), and composition requirements.

```
       +-----------------------------------------------------------+
       |                       Family                              |
       |  (e.g., github, figma, webflow, n8n, wordpress, vercel)   |
       +-----------------------------------------------------------+
               |                  |                     |
               v                  v                     v
       +---------------+  +---------------+     +---------------+
       |   Primitive   |  |   Capability  |<----+    Overlay    |
       | (Token/Config)|  | (Atomic Task) |     |  (Specialized)|
       +---------------+  +---------------+     +---------------+
               |                  ^                     |
               |                  |                     |
               +--------+---------+                     |
                        |                               |
                        v                               v
       +-----------------------------------------------------------+
       |                        Workflow                           |
       |             (Multi-Phase Orchestration)                   |
       +-----------------------------------------------------------+
                                |
                                v
       +-----------------------------------------------------------+
       |                         Adapter                           |
       |             (Protocol / Transport Shim)                   |
       +-----------------------------------------------------------+
```

### The Four Architectural Planes

1. **Semantic Plane (REV-127)**: Governs entity definitions, role boundaries, canonical stable identities, and metadata contracts.
2. **Physical Storage Plane (REV-128)**: Governs filesystem directory structures, ownership models (`tools-and-platforms` vs dominant domain vs registry-first), and duplicate reconciliation.
3. **Composition & Family Plane (REV-129)**: Governs family eligibility criteria, multi-provider implementations, and overlay attachment.
4. **Execution & Discovery Plane (REV-130)**: Governs registry schemas, dynamic routers, alias resolution, runtime projection, and dependency closure.

---

## 2. Canonical Identity and Path-Independence

Pursuant to [ADR-001](file:///Users/garystringham/github-revrebel/skills-library/docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md), **canonical identity is strictly path-independent**.

### 2.1 Identity Syntax and RFC 8141 Compliance
Canonical identities are defined as scoped, lowercase strings:
- **Canonical URN**: `urn:skill:<scope>:<slug>` (e.g., `urn:skill:github:create-pull-request`)
- **Compact Scoped ID**: `<scope>:<slug>` (e.g., `github:create-pull-request`)

```text
           Scope                     Slug
        [a-z0-9-]+         :      [a-z0-9-]+
  (provenance namespace)       (capability name)
```

**Namespace Clarification**:
- `<scope>`: Represents the **permanent provenance identity namespace** assigned when the skill is minted (e.g., `github`, `development`, `figma`, `on-page-seo`). It is **immutable** and decoupled from mutable functional domain ownership (`domain`), physical storage path (`physical_path`), or platform family affiliations (`families`).
- `<slug>`: The unique capability name within that provenance scope.
- The formal URN representation follows the lexical syntax of RFC 8141 (`urn:<NID>:<NSS>`), where `skill` serves as the private/organization Namespace Identifier (NID) for the skills repository ecosystem. It provides unambiguous URI interoperability and schema referencing without asserting an official IANA-registered namespace.

### 2.2 Collision Prevention and Migration Compatibility

How does path-independent canonical identity survive category moves, family restructuring, duplicate resolution, and alias pointers without collisions?

1. **Category Moves & Storage Relocation (REV-128)**:
   - Physical filesystem restructuring (such as moving skills between functional bins or into family directories) only mutates the `physical_path` metadata field in the registry.
   - The canonical identifier `<scope>:<slug>` is an immutable semantic coordinate that remains unchanged across file moves.
2. **Platform Family Extraction & Multi-Provider Disambiguation (REV-129)**:
   - Platform ecosystems utilize their family name as scope (e.g., `github:*`, `figma:*`, `webflow:*`, `n8n:*`).
   - Generic domain capabilities use functional domain scopes (e.g., `software-architecture:*`, `on-page-seo:*`).
   - When identical leaf names exist across domains (such as the 15 GitHub duplicate pairs like `create-pr`), the scoped namespace guarantees complete collision separation (`github:create-pr` vs `development:create-pr`).
3. **Duplicate Resolution & Alias Pointers (REV-130)**:
   - When duplicate pairs are consolidated, one asset is retained as the authoritative owner (`github:create-pull-request`).
   - The secondary asset is converted to a first-class `alias` object (`development:create-pr` -> `aliased_to: "github:create-pull-request"`).
   - Because single-hop aliases resolve deterministically, client lookups for either identifier yield the canonical target without collisions or multi-hop chaining.

### 2.3 The Four Decoupled Axes of Identity, Ownership, Location, and Membership

A critical invariant established in REV-127 is that **immutable identity is decoupled from mutable semantic ownership, physical location, and family grouping**. A catalog asset exists across four independent axes:

| Architectural Axis | Field / Representation | Mutability | Role & Governance |
| :--- | :--- | :--- | :--- |
| **1. Permanent Identity Namespace** | `canonical_id` (`<scope>:<slug>`), `urn` (`urn:skill:<scope>:<slug>`) | **Strictly Immutable** | Permanent identity coordinate assigned at minting (provenance namespace). Never changes across the lifecycle of the object. |
| **2. Current Semantic Ownership** | `domain`, `owner` | **Mutable Metadata** | The functional domain (e.g. `platform`, `development`, `quality-and-security`) or team/subsystem currently responsible for maintaining the asset. |
| **3. Current Physical Location** | `physical_path` | **Mutable Metadata** | Filesystem storage path (e.g. `library/tools-and-platforms/github/create-pr/SKILL.md`), managed by compilers and registry manifests (REV-128). |
| **4. Family Memberships** | `families` | **Mutable Metadata** | Set of platform, vendor, or cross-cutting family groupings (e.g. `["github", "developer-tools"]`), governed by REV-129. |

#### Scenario: Semantic Reownership into a Platform Family
Consider what occurs when an existing capability originally minted in the general development domain (e.g., `development:create-pr`) is transferred into a universal platform family:
- **Permanent Canonical Identity**: Remains `development:create-pr` (`urn:skill:development:create-pr`). Existing dependency graphs, workflow step references, and external links remain intact without breaking changes.
- **Current Semantic Ownership**: Updates to `domain: "platform"`, `owner: "core-tooling"`.
- **Family Memberships**: Updates to `families: ["github", "developer-tools"]`.
- **Physical Location**: Updates to `physical_path: "library/tools-and-platforms/github/create-pr"`.
- **Alias / Router Resolution (REV-130)**: If users query `github:create-pr`, an alias or platform router resolves deterministically to `development:create-pr`. The canonical object does not need to be renamed or reminted.

### 2.4 Identity Invariants
1. **No Path Separators**: Canonical IDs must never contain `/` or `\`.
2. **No File Extensions**: Canonical IDs must never contain `.md`, `.json`, or `.yaml`.
3. **Physical Path Mutability**: The physical storage location (`physical_path`) may be modified during refactoring without altering the canonical ID.
4. **Relationship Target Exclusivity**: All inter-object references (`composed_of`, `extends`, `depends_on`, `aliased_to`) must reference canonical IDs, never physical paths.
5. **Decoupled Scope Immutability**: The canonical `<scope>` is an immutable provenance coordinate assigned at creation; it is decoupled from mutable `domain` ownership, `families` membership, and `physical_path` storage.

---

## 3. First-Class Object Types vs Lifecycle Review Status

### Exact 10 First-Class Object Types

The object model defines **exactly 10 first-class entity types**, partitioned into functional and structural entities:
- **7 Functional / Leaf Entities**: `capability`, `workflow`, `primitive`, `overlay`, `adapter`, `alias`, `reference`
- **3 Structural / Navigational Entities**: `family`, `router`, `generated_artifact`

### Governance Lifecycle Review Status (Not an Object Type)

**`manual_review` is NOT a runtime object type.** Rather, it is an analytical census disposition and governance lifecycle state (`ReviewStatus.MANUAL_REVIEW`) assigned to a skill object whose role classification requires human adjudication. A skill in `manual_review` has an underlying candidate object role (such as a disputed `capability` or `workflow`) and will transition to `ReviewStatus.ACTIVE` once reviewed.

Lifecycle review states include:
- `active`: Fully validated and active in the catalog.
- `manual_review`: Requires human architectural adjudication.
- `draft`: Incomplete or provisional skill definition.
- `deprecated`: Obsolete skill scheduled for sunsetting.
- `sunset`: Inactive, retained solely for historical audit telemetry.

### 3.1 `capability` (Independent Capability)
- **Role**: An atomic, self-contained unit of execution, domain analysis, or code generation. Executes within a single bounded domain context without orchestrating other skills across different domains.
- **Population Baseline**: Represents 79.7% of the catalog (1,701 skills).
- **Execution Model**: Single invocation, bounded input/output, stateless or contextually localized. Average token density: ~1,348 tokens.
- **Attributes**:
  - `canonical_id`: Required. Scoped ID (e.g., `seo:audit`, `react:component-spec`).
  - `name`: Required. Leaf slug.
  - `description`: Required. Must begin with a capitalized summary and contain explicit progressive disclosure triggers (`Use when...`).
  - `domain`: Primary functional domain (e.g., `development`, `marketing-and-seo`).
  - `execution_provider`: Optional. Indicates execution engine or protocol requirements (e.g. `mcp`, `bash`, `python`, `prompt`).
- **Permitted Relationships**:
  - Outbound: `depends_on` (other capabilities or primitives), `implements` (interface contract), `belongs_to_family` (optional family container).
  - Inbound: Referenced by `workflow` via `composed_of`, extended by `overlay` via `extends`, targeted by `alias` via `aliased_to`.

### 3.2 `workflow` (Multi-Phase Orchestration)
- **Role**: A multi-phase procedure or orchestration pipeline coordinating sequential, parallel, or conditional execution of multiple capabilities, tools, or human approval steps.
- **Population Baseline**: Represents 18.3% of the catalog (391 skills).
- **Execution Model**: Multi-phase pipeline. Typically $\ge 3$ distinct execution phases or explicit lifecycle stages (e.g., scan -> evaluate -> gate -> apply -> verify). Average token density: ~2,135 tokens (36.9% higher token density than capabilities).
- **Attributes**:
  - `canonical_id`: Required. Scoped ID (e.g., `workflow:launch`, `git:branch-pr-lifecycle`).
  - `steps`: Ordered list of composition elements (`composed_of`), specifying target canonical IDs and execution order.
  - `approval_gates`: Optional boolean or list of step names requiring human-in-the-loop intervention.
- **Permitted Relationships**:
  - Outbound: `composed_of` (ordered references to capabilities, primitives, or nested workflows), `depends_on`, `belongs_to_family`.
  - Inbound: Targeted by `alias` via `aliased_to`, extended by `overlay` via `extends`.

### 3.3 `family` (Platform / Vendor Container)
- **Role**: A first-class logical namespace, platform container, and governance boundary grouping capabilities, primitives, overlays, workflows, and adapters around a specific technology ecosystem.
- **Population Baseline**: 18 recognized catalog families (e.g., `github`, `figma`, `webflow`, `n8n`, `notebooklm`, `wordpress`, `vercel`, `aws`, `stripe`).
- **Attributes**:
  - `family_id`: Lowercase identifier (e.g., `github`, `webflow`).
  - `title`: Human-readable name (e.g., `GitHub Operations`, `Figma Design Platform`).
  - `description`: Scope and platform domain statement.
  - `vendor`: Platform provider name.
  - `members`: Set of member canonical IDs.
- **Permitted Relationships**:
  - Contains member objects via `belongs_to_family`.

### 3.4 `primitive` (Family Primitive / Reusable Building Block)
- **Role**: A minimal, atomic, reusable building block, schema fragment, token set, or configuration snippet designed to be composed into higher-level capabilities or workflows, rather than invoked as a standalone end-to-end user task.
- **Population Baseline**: Represents atomic building blocks (e.g., `design:design-token`, `auth:nextjs-supabase-auth`, `n8n:expression-syntax`).
- **Structural Invariant**: Primitives are leaf-level or composition-source components. A primitive **must not** compose workflows.
- **Attributes**:
  - `canonical_id`: Required. Scoped ID.
  - `primitive_type`: Category of primitive (`token`, `schema`, `syntax`, `config_template`).
- **Permitted Relationships**:
  - Outbound: `depends_on` (other primitives), `belongs_to_family`.
  - Inbound: Composed by `capability` or `workflow` via `composed_of` or `depends_on`.

### 3.5 `overlay` (Surface / Host Specialization)
- **Role**: A platform- or host-specific behavioral specialization that decorates, adapts, or extends a base capability or workflow for a target environment without reinventing core domain logic.
- **Population Baseline**: 6 recognized catalog overlays (e.g., `figma-implement-motion`, `notebooklm-create`, `figma-swiftui`).
- **Attributes**:
  - `canonical_id`: Required. Scoped ID (e.g., `figma:implement-motion`).
  - `target_id`: Required canonical ID of the extended base capability or workflow.
  - `platform`: Target surface or host (e.g., `figma`, `webflow`, `notebooklm`).
- **Structural Invariant (Depth Limit = 1)**: An overlay **must** target an active `capability` or `workflow`. An overlay **must not** extend another overlay.
- **Permitted Relationships**:
  - Outbound: `extends` (mandatory, points to base capability/workflow), `depends_on`, `belongs_to_family`.

### 3.6 `adapter` (Protocol / Transport Shim)
- **Role**: A pure protocol, transport, or execution-mechanism translation shim (such as an MCP server wrapper, CLI invoker, or API client) that translates agent tool calls into external system actions without embedding business workflow logic.
- **Population Baseline**: 4 pure catalog adapters (e.g., `not-human-search-mcp`, `protect-mcp-governance`).
- **Attributes**:
  - `canonical_id`: Required. Scoped ID.
  - `protocol`: Target protocol (`mcp`, `rest`, `graphql`, `cli`).
  - `interface_spec`: Tool schema or protocol contract.
- **Permitted Relationships**:
  - Outbound: `adapts` (points to protocol or tool definition).
  - Inbound: Invoked by capabilities via execution provider.

### 3.7 `alias` (Compatibility / Alternative Pointer)
- **Role**: A non-canonical pointer or redirect record preserving backward compatibility, legacy naming, or alternative search queries, pointing directly to a single canonical target.
- **Population Baseline**: 3 explicit compatibility aliases in the catalog (`create-pr`, `debugging-toolkit`, `python-development`).
- **Attributes**:
  - `canonical_id`: Required. Alias identifier.
  - `target_id`: Required canonical ID of the active target skill.
  - `alias_type`: `compatibility_redirect`, `deprecated_name`, or `shorthand`.
- **Structural Invariant (Single-Hop)**: An alias **must** point directly to an active canonical object (`capability`, `workflow`, `primitive`, `overlay`, `adapter`, `reference`). Alias chaining (`A -> B -> C`) and alias cycles are strictly forbidden.

### 3.8 `reference` (Static Support / Cheatsheet / Rubric)
- **Role**: Static, passive informational assets (style guides, cheatsheets, syntax references, prompt templates, persona rubrics) providing context or guidelines to an agent, rather than executable action instructions.
- **Population Baseline**: 5 catalog references (e.g., non-executable style guides and documentation templates).
- **Attributes**:
  - `canonical_id`: Required. Scoped ID.
  - `reference_format`: `cheatsheet`, `styleguide`, `rubric`, `syntax_guide`.

### 3.9 `router` (Hierarchical Navigation Node)
- **Role**: A navigational directory node (e.g., `category/SKILL.md` or subcategory router) that catalogs, classifies, and directs agent discovery to member skills and sub-routers using progressive disclosure.
- **Attributes**:
  - `router_id`: Identifier (e.g., `router:development`, `router:development:backend`).
  - `route_level`: `category` or `subcategory`.
  - `managed_skills`: List of registered member skills.

### 3.10 `generated_artifact` (Compiled Runtime Projection)
- **Role**: Deterministic build or runtime projections created by tooling from the canonical definitions (e.g., `audit/runtime-manifest.json`, symlinks in `~/.agents/skills/`, published `runtime` branch tree, search indices).
- **Attributes**:
  - `artifact_type`: `manifest`, `symlink_tree`, `git_branch`, `index`.
  - `source_commit`: Commit SHA from which the artifact was derived.
  - `deterministic`: Boolean (true).

---

## 4. Boundary Disambiguation Matrix

Based on the empirical evidence gathered during the REV-126 census and REV-150 validation, the following decision rules adjudicate boundary disputes:

| Object Role | Primary Criteria | Negative Boundary ("NOT this role when...") | Representative Catalog Example |
| :--- | :--- | :--- | :--- |
| **`capability`** | Performs a single domain task or self-contained transformation. | NOT if it orchestrates $\ge 3$ distinct phases across multiple domain tools. | `seo:audit`, `css:variables` |
| **`workflow`** | Coordinates $\ge 3$ sequential or conditional phases, pipelines, or human approval gates. | NOT if it executes a single-pass tool invocation without phase transitions. | `workflow:launch`, `git:branch-pr-lifecycle` |
| **`primitive`** | Minimal reusable token, configuration fragment, or base syntax not invoked as a standalone user goal. | NOT if it can be invoked standalone to deliver a complete user-facing result. | `design:design-token`, `auth:nextjs-supabase` |
| **`overlay`** | Platform specialization that injects surface-specific logic into an existing capability/workflow (`extends`). | NOT if it functions independently of any underlying generic capability. | `figma:implement-motion`, `notebooklm:create` |
| **`adapter`** | Pure protocol/transport translation shim (MCP, CLI) without business logic. | NOT if the package *uses* an external protocol to perform domain work. | `mcp:not-human-search`, `mcp:protect-governance` |
| **`reference`** | Passive information, cheatsheet, style manual, or evaluation rubric. | NOT if it actively generates code, specs, or designs (those are capabilities). | `ref:component-cheatsheet`, `ref:steve-jobs` |
| **`alias`** | Lightweight redirection pointer maintaining backward-compatible keys. | NOT if it contains its own distinct instructions, scripts, or execution logic. | `alias:create-pr` -> `github:create-pr` |

---

## 5. Relationship Graph Semantics

The object model defines eight directed relationship types:

```text
       Source                       Edge Type                      Target
   +---------------+                                          +---------------+
   |   Workflow    | ----------->  composed_of  ------------> |  Capability   |
   +---------------+                                          +---------------+
   |    Overlay    | ----------->    extends    ------------> |  Capability   |
   +---------------+                                          +---------------+
   |  Any Object   | ----------->   depends_on  ------------> |  Any Object   |
   +---------------+                                          +---------------+
   |     Alias     | ----------->   aliased_to  ------------> |  Any Target   |
   +---------------+                                          +---------------+
   |  Any Object   | -----------> belongs_to_fam -----------> |    Family     |
   +---------------+                                          +---------------+
   |    Adapter    | ----------->     adapts    ------------> |   Protocol    |
   +---------------+                                          +---------------+
   |  Capability   | ----------->   implements  ------------> |   Interface   |
   +---------------+                                          +---------------+
```

1. **`composed_of`**: Ordered composition edges in workflows. Source must be `workflow`. Target must be `capability`, `primitive`, or sub-`workflow`.
2. **`extends`**: Specialization edge. Source must be `overlay`. Target must be `capability` or `workflow`.
3. **`depends_on`**: Prerequisite execution or contextual requirement.
4. **`aliased_to`**: Unidirectional redirect. Source must be `alias`. Target must be an active canonical object.
5. **`belongs_to_family`**: Namespace membership edge. Target must be a `family`.
6. **`adapts`**: Protocol bridging edge. Source must be `adapter`. Target is an external protocol/tool specification.
7. **`implements`**: Contract conformance edge. Source must be `capability` or `adapter`. Target is a standardized capability interface.

---

## 6. Architectural Invariants and Integrity Rules

The object model partitions rules into **Foundational Invariants** (decided and enforced under REV-127) and **Provisional Design Guardrails** (baseline defaults open for refinement in REV-128 through REV-130):

### Part A: Foundational Invariants (Decided in REV-127)

#### Invariant 1: Directed Acyclic Graph (DAG) for Composition and Dependencies
The combined graph formed by `composed_of` and `depends_on` **must be strictly acyclic**:
$$\forall v \in V, \quad v \notin \text{Reachable}(v)$$
Any cycle ($A \to B \to A$) represents an unresolvable execution loop and fails compilation immediately.

#### Invariant 2: Single Canonical Owner
Every canonical ID resolves to exactly one active definition:
$$\text{Count}(\text{Owner}(\text{canonical\_id})) = 1$$
Duplicate IDs or un-namespaced collisions are strictly rejected.

#### Invariant 3: Single-Hop Alias Resolution
Aliases must resolve to a canonical target in exactly one hop:
$$\text{Type}(\text{Target}(\text{alias})) \neq \text{Alias}$$
Chained aliases ($A \to B \to C$) and alias loops ($A \to B \to A$) are invalid.

#### Invariant 6: Path Independence
No canonical ID or reference attribute may contain filesystem separators (`/`, `\`), file extensions, or disk paths. Physical relocation of a skill directory must not change its canonical ID or invalidate any edges.

#### Invariant 7: Catalog Non-Destruction
REV-127 defines schemas, contracts, and validators **without mutating physical skill files** under `library/**`. Physical restructuring and directory movements remain strictly deferred to REV-128 and REV-129.

---

### Part B: Provisional Design Guardrails (Assigned to REV-128 through REV-130)

The following structural rules are implemented as baseline safeguards in the validator but remain explicitly provisional to preserve flexibility for subsequent milestone decisions:

#### Guardrail 4 (Provisional): Shallow Overlay Specialization
Overlays cannot extend other overlays:
$$\text{Type}(\text{Target}(\text{overlay})) \in \{\text{Capability}, \text{Workflow}\}$$
Overlay extension chains ($O_1 \to O_2$) are forbidden as a baseline default to prevent combinatorial prompt pollution. *Subject to review during REV-129 (Family eligibility & provider-adapter rules).*

#### Guardrail 5 (Provisional): Leaf Primitives
Primitives cannot compose workflows:
$$\forall p \in \text{Primitives}, \quad \text{OutEdges}_{\text{composed\_of}}(p) = \emptyset$$
*Subject to review during REV-129 (Family eligibility).*

#### Allocation of Remaining Decisions:
- **REV-128**: Decides physical storage models (`tools-and-platforms` vs dominant domain vs registry-first) and duplicate-pair file management.
- **REV-129**: Decides family inclusion criteria, provider-adapter interfaces, and overlay attachment boundaries.
- **REV-130**: Decides registry manifest schema, router contracts, dynamic alias resolution, and runtime projections.

---

## 7. Resolution of Catalog Disputed Edge Cases

The REV-126/150 audit identified several boundary disputes that were placed in `manual_review` pending REV-127 closure. The semantic object model resolves them as follows:

1. **`launch` (`library/development/backend/launch`)**:
   - *Resolution*: Classified as a **`workflow`**. It orchestrates cross-domain infrastructure verification, pre-flight safety gates, deployment execution, and post-launch smoke tests across multiple domain boundaries.
2. **`code-refactoring-tech-debt` (`library/development/software-architecture/code-refactoring-tech-debt`)**:
   - *Resolution*: Classified as a **`workflow`**. It coordinates a multi-phase inspection pipeline: AST analysis $\to$ debt scoring $\to$ phased surgical refactor $\to$ automated regression test verification.
3. **`agent-memory-mcp` (`library/development/software-architecture/agent-memory-mcp`)**:
   - *Resolution*: Classified as a **`capability`** with `execution_provider: "mcp"`. It provides architectural persistent agent memory capabilities using an MCP protocol backend, rather than acting as an empty protocol bridge.
4. **`not-human-search-mcp` (`library/development/backend/not-human-search-mcp`)**:
   - *Resolution*: Classified as an **`adapter`**. It is a pure MCP protocol wrapper around an external search service without application business logic.
5. **`figma-implement-motion` (`library/design-and-experience/motion-and-graphics/figma-implement-motion`)**:
   - *Resolution*: Classified as an **`overlay`**. It extends the core motion design capability specifically for the Figma animation and prototype player surface.
6. **`design-token` (`library/design-and-experience/design-systems/design-token`)**:
   - *Resolution*: Classified as a **`primitive`**. It provides foundational design token schemas and variables intended to be consumed by design system components and workflows.
7. **`create-pr` (`library/development/fullstack/create-pr`)**:
   - *Resolution*: Classified as an **`alias`** with `target_id: "github:create-pull-request"`.
8. **`steve-jobs` (`library/development/fullstack/steve-jobs`)**:
   - *Resolution*: Classified as a **`reference`** (`rubric` / persona prompt). It provides high-standard product review principles without executable code tasks.
