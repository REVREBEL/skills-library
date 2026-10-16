# ADR-003: Platform Family Eligibility & Provider-Adapter Implementation Rules

- **Status**: Proposed
- **Date**: 2026-10-16
- **Work Order**: REV-129 (`67203557-c1e1-46bb-9a8e-6b2bb76238ee`)
- **Author**: Architecture & Infrastructure Team
- **Preceding Decisions**:
  - [ADR-001: Path-Independent Canonical Identity Contract](ADR-001-path-independent-canonical-identity.md) (REV-127)
  - [ADR-002: Physical Ownership Model](ADR-002-physical-ownership-model.md) (REV-128)
- **Downstream Decisions**:
  - ADR-004: Universal Registry, Router Navigation & Runtime Compatibility (REV-130)

---

## 1. Executive Summary & Context

Under **REV-127** ([ADR-001](ADR-001-path-independent-canonical-identity.md)) and **REV-128** ([ADR-002](ADR-002-physical-ownership-model.md)), the skills library established a 4-axis semantic architecture (identity, ownership, physical storage, family membership) and a hybrid physical ownership model with dedicated platform hubs under `library/tools-and-platforms/<family-slug>/`.

However, without explicit qualification gates and execution boundaries, the catalog faces two critical architectural failure modes:
1. **Vendor-Bucket Sprawl**: Every third-party library, API endpoint, or CLI mentioned in a skill might claim its own top-level platform hub (e.g. creating trivial 1-skill directories for `curl`, `docker`, `stripe`, `supabase`, `slack`), destroying the discoverability and governance of the functional taxonomy.
2. **Execution Provider Proliferation (Semantic Duplication)**: When a domain capability (e.g. `github:create-pull-request` or `postgres:run-query`) can be executed via multiple mechanisms—such as the GitHub CLI (`gh`), a Model Context Protocol (MCP) server, direct REST API calls, or a Python SDK—naive catalog growth produces 4 separate, duplicate canonical skills for the exact same conceptual task. This confuses agents during progressive disclosure and fragments prompt tuning and evaluation benchmarks.

This Architectural Decision Record (**ADR-003**) resolves both failure modes by establishing:
1. **The 4-Gate Family Qualification Framework**: Enforceable qualitative and quantitative gates governing when platform behavior earns a first-class family hub vs. logical family tagging vs. rejection.
2. **The 3-Tier Family Classification**: Tier 1 (First-Class Physical Platform Hubs), Tier 2 (Domain-Anchored Logical Families), and Disqualified Sprawl.
3. **The Execution Provider Contract**: A strict separation where a capability retains a single canonical identity, and execution providers (CLI, MCP, REST, SDK) attach as transport shims via `execution_provider` attributes and `AdapterObject` shims.
4. **Boundary Disambiguation**: Crystal-clear operational contracts separating base capabilities, overlays (`extends`), and provider-adapters (`adapts`).

---

## 2. Platform Family Eligibility Architecture

### 2.1 The 4-Gate Family Qualification Framework

To establish a dedicated first-class platform hub under `library/tools-and-platforms/<family-slug>/`, a candidate ecosystem must satisfy **all 4 qualification gates**:

```text
+----------------------------------------------------------------------------------------------------+
|                               4-GATE FAMILY QUALIFICATION PIPELINE                                 |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ Candidate Tool / Vendor ]                                                                      |
|             |                                                                                      |
|             v                                                                                      |
|   Gate 1: Tool Surface & Protocol Cohesion                                                         |
|           Does the platform provide a unified CLI, MCP server, SDK, or structured API surface?    |
|           [ NO ]  ---------> REJECT (Vendor Sprawl)                                                |
|             | [ YES ]                                                                              |
|             v                                                                                      |
|   Gate 2: Shared Reusable Primitives                                                               |
|           Are there shared auth tokens, connection profiles, session handlers, or design tokens?   |
|           [ NO ]  ---------> REJECT / RETAIN AS ISOLATED CAPABILITIES                              |
|             | [ YES ]                                                                              |
|             v                                                                                      |
|   Gate 3: Critical Mass & Cross-Domain Footprint                                                   |
|           >= 3 distinct capabilities/workflows spanning >= 2 functional categories,               |
|           OR >= 5 cohesive operations within a complex dedicated platform ecosystem?               |
|           [ NO ]  ---------> TIER 2: Domain-Anchored Logical Family (Metadata Tagging Only)        |
|             | [ YES ]                                                                              |
|             v                                                                                      |
|   Gate 4: Coordinated Lifecycle Maintenance                                                        |
|           Do member skills evolve in lockstep with platform API releases, deprecations & auth?     |
|           [ NO ]  ---------> TIER 2: Domain-Anchored Logical Family                                |
|             | [ YES ]                                                                              |
|             v                                                                                      |
|   TIER 1 PLATFORM HUB GRANTED (library/tools-and-platforms/<family-slug>/)                         |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

#### Gate 1: Tool Surface & Protocol Cohesion
- **Requirement**: The candidate ecosystem must expose a cohesive, dedicated programmatic execution surface—such as an official CLI (`gh`, `webflow-cli`, `op`), an MCP server (`github-mcp`, `figma-mcp`), an official SDK, or a structured REST/GraphQL API.
- **Negative Boundary**: Tools that merely invoke standard POSIX shell commands (e.g. `curl`, `jq`, `grep`) or generic programming language idioms without a platform-specific surface fail Gate 1.

#### Gate 2: Shared Reusable Primitives
- **Requirement**: The ecosystem must possess platform-wide primitives that are reused across multiple skills—such as authentication tokens (`AUTH_TOKEN`, API keys), credential vaults, session handlers, rate-limiting handlers, or shared design token sets.
- **Negative Boundary**: A collection of tools that share only generic domain parameters (e.g. an arbitrary URL or string) without shared platform state fails Gate 2.

#### Gate 3: Critical Mass & Cross-Domain Footprint
- **Quantitative Threshold**:
  - **Standard Threshold**: $\ge 3$ distinct validated capabilities or workflows spanning $\ge 2$ canonical functional categories (e.g. GitHub spanning `development`, `infrastructure-and-ops`, and `quality-and-security`).
  - **Single-Domain High-Density Threshold**: $\ge 5$ tightly coupled, distinct operations within a single domain that require a dedicated primitive/adapter harness to avoid cluttering domain trees (e.g. 1Password secret injection and Kubernetes operator in `infrastructure-and-ops`).
- **Negative Boundary**: A vendor with 1 or 2 isolated capabilities fails Gate 3 for Tier 1 and is classified as Tier 2 or an independent capability.

#### Gate 4: Coordinated Lifecycle Maintenance
- **Requirement**: Member skills must share an upgrade and deprecation lifecycle. When the upstream vendor updates an API version, breaks an authentication protocol, or releases new CLI syntax, all member skills must be tested, versioned, and maintained together.
- **Negative Boundary**: Generic tasks whose implementations are independent of vendor API versioning fail Gate 4.

---

### 2.2 Tier Classification Hierarchy

| Classification Tier | Criteria | Physical Storage Representation | Family Metadata Tagging | Concrete Catalog Examples |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: First-Class Platform Hub** | Meets **all 4 gates**.<br>$\ge 3$ capabilities across $\ge 2$ domains (or $\ge 5$ complex domain operations). Dedicated primitives and adapters. | Dedicated physical hub:<br>`library/tools-and-platforms/<family-slug>/` | Required in metadata:<br>`families: ["<family-slug>"]` | `github` (22)<br>`webflow` (22)<br>`figma` (14)<br>`n8n` (14)<br>`hugging-face` (19)<br>`wordpress` (7)<br>`1password` (5) |
| **Tier 2: Domain-Anchored Logical Family** | Meets Gates 1 and 2, but has **sub-critical mass** (<3 skills or <5 single-domain skills). Strong vendor affinity. | Resides in primary functional category:<br>`library/<category>/<subcategory>/<skill>/` | Tagged in metadata:<br>`families: ["<family-slug>"]` | `notebooklm` (4, content/marketing)<br>`stripe` (2, business/e-commerce)<br>`supabase` (2, dev/databases) |
| **Disqualified / Vendor Sprawl** | Fails Gate 1 or Gate 2.<br>Incidental API mention, generic CLI wrapper, or arbitrary technology brand. | Resides strictly in functional domain:<br>`library/<category>/<subcategory>/<skill>/` | **Forbidden**.<br>Must NOT create family tags or platform folders. | `docker-basics`<br>`slack-notifier`<br>`curl-helper`<br>`json-formatter` |
| **Tier 1 Meta-Family** | Universal agent engineering infrastructure internal to the library, not third-party SaaS/vendor tooling. | Dedicated meta infrastructure hub:<br>`library/meta-and-agent-skills/<family-slug>/` | Tagged in metadata:<br>`families: ["<family-slug>"]` | `skill-lifecycle` (13 skills) |

---

### 2.3 Catalog Empirical Qualification Audit

Applying the 4-gate criteria to the REV-126/150 census register yields the following authoritative determinations:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                    CENSUS FAMILY QUALIFICATION AUDIT MATRIX                                          |
+--------------------+--------+---------+------------+---------------+--------------------------------+----------------+
| Candidate Ecosystem| Members| Domains | Gate 1-4   | Qualification | Physical Placement             | Rationale      |
+--------------------+--------+---------+------------+---------------+--------------------------------+----------------+
| GitHub Operations  |   22   |    3    | PASS (All) | Tier 1 Hub    | tools-and-platforms/github/    | 22 ops, gh CLI |
| Webflow            |   22   |    4    | PASS (All) | Tier 1 Hub    | tools-and-platforms/webflow/   | 22 ops, CLI/API|
| Hugging Face       |   19   |    2    | PASS (All) | Tier 1 Hub    | tools-and-platforms/hugging-face/ 19 ops, CLI/SDK|
| Figma              |   14   |    2    | PASS (All) | Tier 1 Hub    | tools-and-platforms/figma/     | 14 ops, Plugin |
| n8n                |   14   |    5    | PASS (All) | Tier 1 Hub    | tools-and-platforms/n8n/       | 14 ops, Nodes  |
| WordPress          |    7   |    2    | PASS (All) | Tier 1 Hub    | tools-and-platforms/wordpress/ | 7 ops, WP-CLI  |
| 1Password          |    5   |    1    | PASS (All) | Tier 1 Hub    | tools-and-platforms/1password/ | 5 ops, op CLI  |
| Skills Lifecycle   |   13   |    1    | PASS (Meta)| Tier 1 Meta   | meta-and-agent-skills/lifecycle/ Internal meta |
| NotebookLM         |    4   |    2    | PASS (1,2) | Tier 2 Logical| content-and-documentation/...  | Sub-critical   |
| Stripe             |    2   |    1    | PASS (1,2) | Tier 2 Logical| business-and-operations/...    | Sub-critical   |
| Supabase           |    2   |    1    | PASS (1,2) | Tier 2 Logical| development/databases/...      | Sub-critical   |
| Docker / Generic   |    1   |    1    | FAIL (2,3) | Disqualified  | infrastructure-and-ops/...     | Anti-sprawl    |
+--------------------+--------+---------+------------+---------------+--------------------------------+----------------+
```

---

## 3. Provider-Adapter Implementation Architecture

### 3.1 The Canonical Capability vs. Execution Provider Invariant

> **Architectural Invariant (Provider Decoupling)**:
> A capability represents a single abstract operational task, domain transformation, or code generation activity. It possesses **exactly ONE canonical identity** (`urn:skill:<scope>:<slug>`).
> 
> A capability **MUST NOT** be duplicated across multiple skill definitions simply because it can be executed via different protocols or tooling mechanisms (CLI, MCP, REST API, Python SDK).

```text
    WRONG (Anti-Pattern: Duplicate Canonical Skills for Each Mechanism):
    x  github:create-pr-via-cli   (CLI wrapper)
    x  github:create-pr-via-mcp   (MCP wrapper)
    x  github:create-pr-via-rest  (REST API wrapper)
    x  github:create-pr-via-sdk   (Python SDK wrapper)

    CORRECT (Single Canonical Identity with Pluggable Execution Providers):
    v  Canonical Capability: github:create-pr
       |
       +--> Execution Provider: gh_cli (default local CLI)
       +--> Execution Provider: github_mcp (remote agent MCP)
       +--> Execution Provider: octokit_rest (REST fallback)
```

### 3.2 Provider Types and Contract Definition

Every executable capability defines its supported execution providers in its frontmatter or object model definition:

```yaml
---
name: create-pr
canonical_id: github:create-pr
role: capability
domain: development
families: [github]
execution_provider:
  default: gh_cli
  supported:
    - name: gh_cli
      provider_type: cli
      command: gh pr create
      adapter_ref: github:gh-cli-adapter
    - name: github_mcp
      provider_type: mcp
      tool_name: create_pull_request
      adapter_ref: github:mcp-adapter
    - name: github_rest
      provider_type: rest
      endpoint: POST /repos/{owner}/{repo}/pulls
      adapter_ref: github:rest-adapter
---
```

#### Supported `provider_type` Values
1. **`cli`**: Invokes a local command-line binary (e.g. `gh`, `op`, `wp`, `webflow-cli`). Requires verifying local executable availability.
2. **`mcp`**: Invokes a tool exposed by an active Model Context Protocol (MCP) server (e.g. `mcp__github__create_pull_request`).
3. **`rest`**: Dispatches an HTTP/REST or GraphQL request against a remote platform API endpoint.
4. **`sdk`**: Executes a programmatic client library invocation in Python, TypeScript, or Go.
5. **`prompt`**: Natural language reasoning and generative transformation requiring no external tool transport.

---

### 3.3 Pluggable Adapter Objects (`adapts`)

Adapters are first-class `AdapterObject` entities (SkillRole `adapter`) whose sole purpose is **protocol and transport translation**.

#### Adapter Responsibilities & Invariants:
1. **Zero Business Logic**: Adapters must not contain domain analysis, approval workflows, or multi-step reasoning. They strictly translate structured parameters into tool calls and normalize error responses.
2. **Protocol Schema Definition**: Adapters encapsulate the input schema, tool definitions, environment variable declarations, and authentication bindings required by the underlying provider.
3. **Physical Storage**:
   - Platform-specific adapters reside in `library/tools-and-platforms/<family-slug>/adapters/<adapter-slug>/`.
   - General-purpose adapters (e.g. generic REST invoker, Postgres driver) reside in `library/meta-and-agent-skills/adapters/<adapter-slug>/`.
4. **Relationship Target**: An adapter declares `adapts: <protocol_or_platform_surface>`.

```text
+----------------------------------------------------------------------------------+
|                     CAPABILITY -> ADAPTER EXECUTION FLOW                         |
+----------------------------------------------------------------------------------+
|                                                                                  |
|   Agent Task Prompt                                                              |
|          |                                                                       |
|          v                                                                       |
|   [ Canonical Capability: github:create-pr ]                                     |
|   (Defines domain requirements, PR description template, validation checklist)  |
|          |                                                                       |
|          | (Dispatches via Execution Provider Selection)                         |
|          |                                                                       |
|          +-----------------------+-----------------------+                       |
|          |                       |                       |                       |
|          v                       v                       v                       |
|   [ Adapter: gh-cli ]     [ Adapter: github-mcp ]  [ Adapter: github-rest ]     |
|   (Translates args to     (Maps JSON args to MCP   (Translates args to HTTP      |
|    gh pr create --title)   tool call payload)       POST payload with Bearer)    |
|          |                       |                       |                       |
|          v                       v                       v                       |
|   Local Subprocess        MCP Server Daemon        GitHub REST API               |
|                                                                                  |
+----------------------------------------------------------------------------------+
```

---

## 4. Boundary Disambiguation Matrix: Capabilities vs Overlays vs Adapters

A recurring friction point in skills engineering is deciding whether a new artifact should be authored as a base capability, an overlay, or an adapter. The following decision matrix provides unambiguous operational boundaries:

| Entity Type | Primary Architectural Purpose | Required Inbound / Outbound Relations | Contains Business / Domain Logic? | Contains Protocol / Tool Transport? | Valid Examples | Invalid Anti-Patterns |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`capability`** | Performs an atomic domain task or transformation. | `depends_on`, `implements`, `belongs_to_family` | **YES** (Core domain logic, instructions, prompt rubrics). | **NO** (Delegates transport to execution providers/adapters). | `development:commit`<br>`seo:audit`<br>`github:create-pr` | x Writing separate capabilities for CLI vs MCP.<br>x Embedding raw curl commands in prompt. |
| **`overlay`** | Decorates or specializes a base capability for a specific surface/host. | **Mandatory** `extends: <base_id>`. Single-hop depth limit = 1. | **YES** (Surface-specific overrides, host nuances). | **NO** (Inherits or specializes execution configuration). | `figma:implement-motion` (extends `motion:implement-motion`) | x Extending another overlay (depth > 1).<br>x Overlays that function without a base skill. |
| **`adapter`** | Pure protocol/transport translation shim. | **Mandatory** `adapts: <protocol_or_tool_surface>`. | **NO** (Strictly zero business or workflow logic). | **YES** (CLI args, MCP tool declarations, REST endpoints). | `github:gh-cli-adapter`<br>`figma:mcp-adapter`<br>`mcp:postgres` | x Putting review guidelines inside an adapter.<br>x Performing multi-step workflow inside an adapter. |

---

## 5. Decision Consequences

### 5.1 Positive Architectural Consequences
- **Elimination of Vendor Sprawl**: Clear 4-gate quantitative and qualitative criteria prevent premature directory creation for every one-off tool or API mentioned in the catalog.
- **Deduplication of Execution Mechanisms**: Common operations (like creating issues, running tests, or committing code) maintain a single authoritative prompt and specification, regardless of whether executed via CLI or MCP.
- **Composable Transport Layer**: Upgrading from CLI to MCP or REST requires modifying or adding an adapter, leaving high-level capabilities, workflows, and prompts untouched.
- **Progressive Discovery Optimization**: Agent prompt routing trees remain compact and focused on domain objectives rather than low-level protocol variants.

### 5.2 Negative & Neutral Consequences
- **Metadata Rigor**: Skill frontmatter must explicitly declare execution provider mappings when multi-provider execution is supported.
- **Adapter Maintenance**: Dedicated adapter shims must be authored and maintained for platform hubs that expose multiple protocols.

---

## 6. Implementation & Compliance Plan

1. **Tooling & Validation Updates (`tools/skill_library/`)**:
   - Author `tools/skill_library/family_contract.py` implementing `FamilyTier`, `FamilyQualificationGate`, `FamilyCandidateEvaluator`, and `ExecutionProviderContract`.
   - Update `tools/skill_library/object_model.py` to enforce provider-adapter relationships and forbid multi-provider canonical ID duplication.
2. **Documentation Synchronization**:
   - Update `docs/architecture/semantic-object-model.md` to integrate ADR-003 family qualification gates, provider contracts, and the disambiguation matrix.
3. **Comprehensive Test Suite**:
   - Author `tests/test_family_eligibility.py` verifying:
     - Positive Tier 1 qualification for verified platforms (GitHub, Webflow, Figma, n8n, Hugging Face, WordPress, 1Password).
     - Proper Tier 2 logical family tagging for sub-critical mass platforms (NotebookLM, Stripe, Supabase).
     - Strict rejection of vendor sprawl (arbitrary single tools claiming family hubs).
     - Execution provider binding without canonical ID duplication.
     - Pure adapter contracts (zero business logic invariant, single-hop overlay invariant).
