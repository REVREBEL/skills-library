# ADR-004: Registry, Router, Alias, Dependency, and Semantic Group Contracts

- **Status**: Proposed
- **Date**: 2026-10-17
- **Work Order**: REV-130 (`f1a000e3-f3a6-4acb-9fa1-2e142d8bea6c`)
- **Author**: Architecture & Infrastructure Team
- **Preceding Decisions**:
  - [ADR-001: Path-Independent Canonical Identity Contract](ADR-001-path-independent-canonical-identity.md) (REV-127)
  - [ADR-002: Physical Ownership Model](ADR-002-physical-ownership-model.md) (REV-128)
  - [ADR-003: Platform Family Eligibility & Provider-Adapter Implementation Rules](ADR-003-family-eligibility-and-provider-adapters.md) (REV-129)

---

## 1. Executive Summary & Context

Under **REV-127** ([ADR-001](ADR-001-path-independent-canonical-identity.md)), **REV-128** ([ADR-002](ADR-002-physical-ownership-model.md)), and **REV-129** ([ADR-003](ADR-003-family-eligibility-and-provider-adapters.md)), the skills ecosystem established:
1. A 4-axis semantic architecture separating permanent identity, current semantic ownership, physical location, and family membership.
2. A hybrid physical storage model preserving functional taxonomy (`library/<category>/<subcategory>/`) while establishing dedicated platform hubs (`library/tools-and-platforms/<family-slug>/`).
3. A 4-gate qualification framework and multi-provider execution contracts (supporting multiple providers of the same transport type).

However, a library of over 2,100 skills cannot be effectively operated, discovered, or deployed by autonomous AI agents, developer tooling, or runtime environments without a formal **Execution and Discovery Plane**.

Without rigorous registry, router, alias, dependency, and grouping contracts, the system risks four catastrophic operational failures:
1. **Discovery Fragmentation**: Agents querying skills across domains or platforms must guess physical disk paths or scan thousands of flat files, leading to context-window exhaustion and hallucinated dependencies.
2. **Alias Loops and Broken Chaining**: Renaming, moving, or deprecating duplicate skills (such as the 15 GitHub duplicate pairs) risks introducing multi-hop alias chains ($A \to B \to C$) or circular alias loops ($A \to B \to A$), breaking downstream tool execution.
3. **Execution-Time Dependency Breakage**: Materializing a skill into an isolated runtime or project without its prerequisites (e.g. workflows lacking their composed steps, overlays missing base capabilities, or tools missing shared authentication primitives) causes silent runtime failures.
4. **Non-Deterministic Projections**: Compiling runtime manifests or router trees from non-deterministic traversal creates git churn, dirty repository states, and unreproducible deployments.

This Architectural Decision Record (**ADR-004**) resolves these challenges by establishing:
- **The Universal Catalog Registry Schema**: A machine-readable, typed specification capturing all 4 axes, 10 first-class object roles, execution providers, and directed relationships.
- **The Multi-View Discovery Architecture**: 4 distinct projection views (Functional Domain, Platform Family, Semantic Group, Execution Provider) plus a tokenized inverted search index.
- **The Single-Hop Alias Resolution Contract**: Invariant-enforced alias resolution with deprecation telemetry and direction-neutral duplicate consolidation rules.
- **Transitive Dependency Closure & DAG Invariants**: Acyclicity verification, topological sort execution plans, and orphan/dead-reference detection.
- **Semantic Group Contracts**: First-class multi-skill capability clusters spanning domains for cohesive workflow deployment.
- **Recursive Family Routers**: Hierarchical markdown routing contracts for physical platform hubs and virtual logical families.
- **Deterministic Project Materialization**: Complete, self-contained project projection ensuring zero missing dependencies and collision-free runtime naming.

---

## 2. Universal Catalog Registry Schema

### 2.1 Design Principles & Storage
The registry is the authoritative, compiled, machine-readable manifest of the entire skills ecosystem (`audit/skills-registry.json`).
- **Canonical Derivation**: The registry is strictly compiled from authoritative canonical skill packages, frontmatters, the census (`semantic-role-census.json`), and validated ledgers. It is never manually edited.
- **Path-Independence**: All inter-object references use canonical identifiers (`<scope>:<slug>` or `urn:skill:<scope>:<slug>`), never filesystem paths.
- **Typed Invariants**: Every registry entry conforms to strict JSON schema validation.

### 2.2 Comprehensive Registry Entry Fields

```json
{
  "$schema": "https://json-schema.revrebel.io/v1/skills-registry.schema.json",
  "version": "1.0.0",
  "generated_at": "2026-10-17T02:00:00Z",
  "total_skills": 2133,
  "skills": {
    "github:create-pull-request": {
      "canonical_id": "github:create-pull-request",
      "urn": "urn:skill:github:create-pull-request",
      "name": "create-pull-request",
      "role": "capability",
      "description": "Creates a GitHub pull request with branch verification and template formatting.",
      "domain": "tools-and-platforms",
      "category": "tools-and-platforms",
      "subcategory": "github",
      "owner": "core-tooling",
      "families": ["github", "developer-tools"],
      "semantic_groups": ["git-automation", "code-review"],
      "physical_path": "library/tools-and-platforms/github/create-pull-request",
      "version": "1.2.0",
      "status": "active",
      "confidence": "high",
      "tags": ["git", "github", "pr", "code-review"],
      "keywords": ["pull request", "merge request", "gh pr create"],
      "relationships": {
        "composed_of": [],
        "extends": null,
        "depends_on": ["github:auth-profile"],
        "adapts": null,
        "aliased_to": null,
        "belongs_to_family": "github"
      },
      "execution_providers": [
        {
          "provider_id": "github-cli",
          "provider_type": "cli",
          "transport": "bash",
          "command": "gh pr create",
          "is_default": true,
          "config": {"min_version": "2.40.0"}
        },
        {
          "provider_id": "github-mcp-official",
          "provider_type": "mcp",
          "transport": "mcp",
          "server_name": "github",
          "tool_name": "create_pull_request",
          "is_default": false,
          "config": {"schema": "tools/mcp/github/create_pull_request.json"}
        },
        {
          "provider_id": "github-mcp-enterprise",
          "provider_type": "mcp",
          "transport": "mcp",
          "server_name": "github-enterprise",
          "tool_name": "create_pull_request",
          "is_default": false,
          "config": {"schema": "tools/mcp/github-enterprise/create_pull_request.json"}
        }
      ],
      "provenance": {
        "source_hash": "sha256:7f83b165...",
        "content_hash": "sha256:e3b0c442...",
        "commit_sha": "7174297530427fa1652dd366db94f9ffe1dc2a82",
        "last_validated": "2026-10-17T02:00:00Z"
      }
    }
  }
}
```

### 2.3 The 4 Axes and Field Partitioning

| Axis | Field(s) | Mutability | Authority / Specification |
| :--- | :--- | :--- | :--- |
| **1. Identity** | `canonical_id`, `urn`, `name` | **Immutable** | Minted coordinate (RFC 8141). Never changes across migrations. |
| **2. Semantic Ownership** | `domain`, `category`, `subcategory`, `owner` | **Mutable** | Functional categorization in catalog hierarchy. |
| **3. Physical Location** | `physical_path` | **Mutable** | Filesystem location under `library/**` (REV-128). |
| **4. Family Memberships** | `families`, `belongs_to_family` | **Mutable** | Platform/vendor affiliations (REV-129). |
| **Operational Plane** | `semantic_groups`, `execution_providers` | **Mutable** | Task grouping & execution bindings (REV-130). |

---

## 3. Multi-View Discovery Architecture

A monolithic flat directory or single hierarchy fails to serve diverse operational needs. REV-130 defines **4 canonical projection views** compiled deterministically from the central registry:

```text
+----------------------------------------------------------------------------------------------------+
|                                    MULTI-VIEW DISCOVERY PLANE                                      |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|                                     [ Central Registry ]                                           |
|                                              |                                                     |
|         +-------------------+----------------+-------------------+-------------------+             |
|         |                   |                                    |                   |             |
|         v                   v                                    v                   v             |
|  [ Functional View ]  [ Family View ]                    [ Group View ]     [ Provider View ]      |
|  Hierarchical         Platform-centric                   Cross-domain        Execution runtime     |
|  taxonomy:            discovery:                         task clusters:      filtering:            |
|  development/         tools-and-platforms/               git-automation      mcp (189)             |
|    backend/             github/ (22)                     auth-primitives     cli (1,240)           |
|    frontend/            webflow/ (22)                    seo-publishing      python (684)          |
|  marketing-and-seo/     figma/ (14)                      cloud-migration     prompt (20)           |
|                                                                                                    |
|                                              |                                                     |
|                                              v                                                     |
|                              [ Inverted Search Index (search-index.json) ]                         |
|                              Tokenized triggers, capability intents & keywords                     |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### 3.1 The 4 Projections
1. **Functional / Domain View (`views/functional-view.json`)**:
   - Organizes skills by primary business/technical domain (`domain` $\to$ `category` $\to$ `subcategory`).
   - Primary view for general catalog browsing, taxonomy audits, and broad functional specialization.
2. **Platform / Family View (`views/family-view.json`)**:
   - Organizes skills by platform ecosystem (`github`, `webflow`, `figma`, `supabase`, `n8n`).
   - Indexes both Tier 1 physical hubs (`library/tools-and-platforms/<family-slug>/`) and Tier 2 logical family members across the catalog.
   - Primary view for platform engineers, ecosystem integrations, and vendor-specific pilots.
3. **Semantic Group View (`views/semantic-group-view.json`)**:
   - Organizes skills into cross-cutting, task-oriented capability clusters (e.g. `git-automation`, `database-migrations`, `seo-optimization`, `fullstack-auth`).
   - Groups cut across domains (e.g. `git-automation` spans `development/software-architecture`, `tools-and-platforms/github`, and `infrastructure-and-ops`).
   - Primary view for workflow orchestrators and high-level agent plan decomposition.
4. **Execution / Provider View (`views/provider-view.json`)**:
   - Organizes capabilities by transport protocol (`mcp`, `cli`, `bash`, `python_script`, `rest`).
   - Allows agents to discover what capabilities can be executed given currently loaded MCP servers or local environment CLI availability.

### 3.2 Inverted Search Index (`audit/search-index.json`)
To enable agent progressive disclosure without loading thousands of full skill definitions:
- Tokenizes `name`, `description`, `tags`, `keywords`, and frontmatter trigger clauses.
- Emits compact inverted index:
  ```json
  {
    "pull request": ["github:create-pull-request", "github:review-pull-request"],
    "supabase": ["supabase:manage-database", "supabase:nextjs-auth"]
  }
  ```
- Permits fast, low-overhead keyword lookups before pulling full markdown instruction packages into context.

---

## 4. Deterministic Compiler & Generation Rules

The registry and all its projection views must be produced by an idempotent, single-source compiler (`CatalogCompiler`):

### 4.1 Compilation Pipeline
```text
  [ Raw Canonical Skills ] + [ Semantic Census ] + [ Family Ledgers ]
                            |
                            v
               Stage 1: Ingestion & Parsing
                            |
                            v
         Stage 2: Invariant Verification (DAG, Single-Hop)
                            |
                            v
        Stage 3: Alias Resolution & Deprecation Graph
                            |
                            v
       Stage 4: Transitive Dependency Closure Evaluation
                            |
                            v
         Stage 5: View Projection & Search Indexing
                            |
                            v
  [ Deterministic Output: registry.json, views/**, search-index.json ]
```

### 4.2 Idempotency and Zero-Drift Invariant
- **Rule**: Given identical input repository contents, `CatalogCompiler` must emit byte-for-byte identical output files across runs, operating systems, and platforms.
- **Sorting Requirement**: All dictionary keys, object arrays, dependency lists, and relationship collections must be deterministically sorted by canonical ID.
- **Timestamp Governance**: Production manifests record git commit SHAs rather than execution wall-clock timestamps for cache keys to prevent spurious diff churn.

---

## 5. Single-Hop Alias Resolution Architecture

### 5.1 Foundational Invariant 3
Pursuant to REV-127:
$$\forall a \in \text{Aliases}, \quad \text{Type}(\text{Target}(a)) \neq \text{Alias}$$
- **Direct Resolution**: An alias points directly to a canonical capability, workflow, primitive, overlay, or adapter.
- **Zero Chaining**: Chained aliases ($A \to B \to C$) are strictly prohibited.
- **Zero Cycles**: Alias loops ($A \to B \to A$) fail compilation immediately.

### 5.2 Direction-Neutral Candidate Duplicate Resolution Protocol
Under REV-128 and REV-129, 15 GitHub duplicate pairs (e.g. `library/tools-and-platforms/github/create-pr` vs `library/development/backend/create-pr`) were held direction-neutral.

ADR-004 defines the formal resolution protocol:
1. **Authoritative Owner Selection**: The canonical identity is assigned to the platform hub capability (`github:create-pull-request`) because GitHub is a validated Tier 1 Platform Family under ADR-003.
2. **First-Class Alias Creation**: The legacy functional domain path mints an `AliasObject` (`development:create-pr` $\to$ `aliased_to: "github:create-pull-request"`).
3. **Zero Runtime Disruption**: Clients, workflows, or subagents referencing `development:create-pr` resolve deterministically to `github:create-pull-request` in a single hop.
4. **Lifecycle Deprecation**: The alias object is flagged as `status: "deprecated"`, warning developers while preserving 100% backward compatibility.

### 5.3 Deprecation Lifecycle
1. **Active**: Fully supported canonical skill or direct alias.
2. **Deprecated**: Backward-compatible alias. Emits telemetry/warning on invocation. `deprecation_notice` specifies target canonical ID and sunset milestone.
3. **Sunset**: Retired alias retained in archival tombstone ledger; rejected by runtime execution runners.

---

## 6. Transitive Dependency Closure & DAG Invariants

### 6.1 Foundational Invariant 1 (Strict DAG Acyclicity)
The directed graph $G = (V, E)$ formed by vertices $V$ (canonical objects) and edges $E$ (where $E \subseteq \text{COMPOSED\_OF} \cup \text{DEPENDS\_ON} \cup \text{EXTENDS} \cup \text{ADAPTS}$) **must be strictly acyclic**:
$$\forall v \in V, \quad v \notin \text{Reachable}(v)$$
Any cycle ($A \to B \to A$ or $A \to B \to C \to A$) triggers an immediate compilation halt (`InvariantViolationError`).

### 6.2 Transitive Dependency Closure Algorithm
When an agent or deployment environment requests a target skill $s$, the materialization engine must compute the full transitive dependency closure:

$$\text{Closure}(S) = S \cup \bigcup_{s \in S} \left( \text{DependsOn}(s) \cup \text{ComposedOf}(s) \cup \text{Extends}(s) \cup \text{Adapts}(s) \right)$$

The engine then performs a **topological sort** on the closure subgraph to yield the deterministic initialization/execution order:
$$\text{TopologicalSort}(\text{Closure}(S)) = [v_1, v_2, \dots, v_k]$$
such that if edge $(u, v) \in E$, then $u$ appears before $v$ in execution precedence.

### 6.3 Reachability, Dead Reference, and Orphan Invariants
- **Dead Reference Invariant (Invariant 8)**: Every target ID specified in `depends_on`, `composed_of`, `extends`, `adapts`, or `aliased_to` must exist as a registered canonical ID in the registry. Dangling pointers fail validation immediately.
- **Orphan Primitive Detection**: Primitives (`role: primitive`) and adapters (`role: adapter`) with in-degree 0 (no capability, workflow, or family referencing them) are flagged with compiler warnings to prevent dead code buildup.
- **Leaf Primitive Guardrail (Guardrail 5)**: Primitives must not declare outbound `composed_of` edges.

---

## 7. Semantic Group Contracts

### 7.1 Concept & Purpose
A **Semantic Group** is a cohesive, cross-domain cluster of skills designed to be consumed together for a complex business or technical capability (e.g. `fullstack-auth`, `database-migrations`, `seo-campaign-launch`).
- Unlike **Categories** (which are hierarchical, exclusive filesystem partitions), semantic groups are **cross-cutting and non-exclusive**. A skill may belong to multiple semantic groups.
- Unlike **Platform Families** (which require vendor/platform cohesion), semantic groups represent **functional solutions** combining tools across different vendors and domains.

### 7.2 Semantic Group Schema
```json
{
  "group_id": "fullstack-auth",
  "name": "Fullstack Authentication & Authorization",
  "description": "Unified skills for implementing secure user authentication, session management, and RBAC across frontend and backend.",
  "domain_scope": "cross-domain",
  "members": [
    "supabase:manage-auth",
    "nextjs:setup-auth-middleware",
    "security:audit-jwt-tokens"
  ],
  "tags": ["auth", "security", "rbac", "jwt"],
  "materialization_policy": "transitive_closure"
}
```

### 7.3 Group Materialization Policy
When a semantic group is materialized into a developer workspace or agent runtime, the materializer evaluates:
$$\text{GroupClosure}(G) = \bigcup_{m \in \text{Members}(G)} \text{Closure}(\{m\})$$
This guarantees that all shared primitives, adapters, workflows, and platform tools required by any member of the group are automatically materialized into the target environment.

---

## 8. Recursive Family Routers & Markdown Navigation

### 8.1 Multi-Tier Router Architecture
Navigation across the catalog follows a standardized markdown router contract:
1. **Root Router (`library/SKILL.md`)**:
   - High-level directory linking to all canonical functional categories (`development`, `content-and-documentation`, `marketing-and-seo`, `infrastructure-and-ops`, `quality-and-security`) and dedicated platform hubs (`tools-and-platforms`).
2. **Category / Subcategory Routers (`library/<category>/SKILL.md`)**:
   - Provide thematic navigation, describing sub-domains and directly listing member capabilities with trigger guidelines.
3. **Tier 1 Platform Family Routers (`library/tools-and-platforms/<family-slug>/SKILL.md`)**:
   - Dedicated physical hub routers.
   - **Recursive Routing Structure**:
     - Root family router (`SKILL.md`): Directs agents to family primitives (auth/sessions), leaf capabilities, and platform workflows.
     - Sub-family routers (e.g. `library/tools-and-platforms/github/workflows/SKILL.md`): Group complex multi-step orchestrations.
4. **Tier 2 Logical Family Virtual Routers**:
   - For logical families anchored across domain trees (e.g. `supabase`), a projected router is generated at build time (`views/routers/family-supabase.md`) aggregating member skills across `development/databases` and `ai-and-data/data-engineering`.

### 8.2 Markdown Router Formatting Contract
All generated router markdown documents must conform to strict rules:
- **Valid Relative Links**: Every referenced child skill must link to its relative `SKILL.md` (e.g. `[create-pull-request](create-pull-request/SKILL.md)`).
- **Trigger Contract Excerpts**: Include the formal operational trigger sentence from each member skill's frontmatter.
- **Provider Badge Indicators**: Display icons/badges for supported execution transports (`[CLI]`, `[MCP]`, `[Python]`).
- **Zero Absolute Paths**: Absolute workstation filesystem paths (`/Users/...`, `/home/...`) are strictly forbidden.

---

## 9. Runtime Publication & Project Materialization

### 9.1 Projection Modes
When projecting canonical skills into target runtimes or client workspaces, the engine supports 5 modes:
1. `full`: Complete catalog projection (all 2,133 skills).
2. `subset`: Explicit category or path filter (e.g. only `quality-and-security`).
3. `family`: Complete platform family slice (e.g. all `github` skills + primitives).
4. `semantic_group`: Complete task cluster slice (e.g. `database-migrations`).
5. `standalone_closure`: Specific target skill(s) plus their full transitive dependency closure.

### 9.2 Deterministic Flat Runtime Naming
In flat runtime target directories (such as `.agents/skills/`), skills cannot share leaf directory names.
- When two skills share a slug (e.g. `development:ad-creative` and `marketing:ad-creative`), the materializer deterministically prefixes the scope: `development-ad-creative` vs `marketing-ad-creative`.
- Registered unique slugs remain un-prefixed for brevity.
- Mappings are published to `audit/runtime-manifest.json`.

### 9.3 Self-Contained Dependency Guarantee
- **Rule**: A materialized target directory or branch must **never** contain unresolved relative links or dangling dependencies.
- If skill $A$ depends on primitive $B$, materializing $A$ automatically includes $B$.

---

## 10. Architectural Invariants & Verification Matrix

The following matrix establishes the enforceable invariants for REV-130:

| ID | Invariant Name | Scope | Formal Mathematical Condition | Violation Action |
| :--- | :--- | :--- | :--- | :--- |
| **INV-1** | DAG Acyclicity | Dependencies & Composition | $\forall v \in V, v \notin \text{Reachable}(v)$ | Immediate compilation failure (`InvariantViolationError`). |
| **INV-2** | Single Canonical Owner | Canonical Identity | $\text{Count}(\text{Owner}(\text{canonical\_id})) = 1$ | Duplicate registration rejected. |
| **INV-3** | Single-Hop Alias | Alias Resolution | $\forall a \in \text{Aliases}, \text{Type}(\text{Target}(a)) \neq \text{Alias}$ | Alias chaining or alias loops rejected. |
| **INV-4** | Shallow Overlay | Overlay Specialization | $\forall o \in \text{Overlays}, \text{Type}(\text{Target}(o)) \in \{\text{Cap}, \text{Wf}\}$ | Overlay extending overlay rejected. |
| **INV-5** | Leaf Primitives | Primitive Purity | $\forall p \in \text{Primitives}, \text{Out}_{\text{composed\_of}}(p) = \emptyset$ | Primitive composing workflow rejected. |
| **INV-6** | Path Independence | Canonical Identifiers | $\forall id \in \text{IDs}, id \cap \{'/', '\\', '.md', '.json'\} = \emptyset$ | Path syntax in ID rejected. |
| **INV-7** | Catalog Non-Destruction | Protected Assets | $\Delta(\text{library/}) = \emptyset, \Delta(\text{audit/taxonomy-census/}) = \emptyset$ | PR blocked; zero unauthorized drift. |
| **INV-8** | Dead Reference Prevention | Relationship Targets | $\forall e = (u, v) \in E, v \in V_{\text{registered}}$ | Dangling target pointer rejected. |
| **INV-9** | Transitive Completeness | Project Materialization | $\text{Materialized}(S) \supseteq \text{Closure}(S)$ | Incomplete runtime bundle rejected. |
| **INV-10** | Deterministic Compilation | Compiler Pipeline | $\text{Compiler}(C)_{t_1} \equiv \text{Compiler}(C)_{t_2}$ | Non-deterministic diff rejected. |

---

## 11. Conclusion & Next Steps

ADR-004 establishes the definitive contracts for the catalog's Execution and Discovery Plane.
Following this decision:
1. `tools/skill_library/` implements the registry schema, compiler, alias resolver, dependency closure graph, semantic group manager, and materializer.
2. Exhaustive positive and negative regression tests verify Invariants 1 through 10.
3. The catalog remains 100% untouched while execution tooling gains deterministic multi-view discovery and reliable project projection.
