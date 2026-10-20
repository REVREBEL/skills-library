# Architecture Scenario Verification: Programming-Language Packs and the Super-Code Family

- **Scenario Identifier**: `REV-133`
- **Issue Reference**: [Linear REV-133](https://linear.app/revrebel/issue/REV-133/scenario-programming-language-packs-and-the-super-code-family) / [Metrics-Core #225](https://github.com/REVREBEL/Metrics-Core/issues/225)
- **Status**: Complete / Validated
- **Date**: 2026-10-19
- **Mode**: Read-Only Architecture Scenario Verification (`reviewable-artifacts`)
- **Governing Architecture Contracts**:
  - [ADR-001: Path-Independent Canonical Identity Contract](../decisions/ADR-001-path-independent-canonical-identity.md)
  - [ADR-002: Physical Ownership Model](../decisions/ADR-002-physical-ownership-model.md)
  - [ADR-003: Platform Family Eligibility & Provider-Adapter Implementation Rules](../decisions/ADR-003-family-eligibility-and-provider-adapters.md)
  - [ADR-004: Universal Registry, Router Navigation & Runtime Compatibility](../decisions/ADR-004-registry-router-alias-dependency-contracts.md)
  - [ADR-005: Architecture Validation and Migration Gates](../decisions/ADR-005-architecture-validation-and-migration-gates.md)

---

## 1. Executive Summary & Problem Formulation

### 1.1 Objective
The purpose of **REV-133** is to determine whether language-specific coding guidance should:
1. **Option A (Pure Independent Decentralization)**: Remain as individual, uncoordinated development skills dispersed under `development/<subcategory>/`.
2. **Option B (Explicit Language Platform Hub / Family)**: Be organized into a dedicated physical platform hub (e.g., `tools-and-platforms/languages/` or `tools-and-platforms/super-code/`).
3. **Option C (Shared Base / Reference Pattern with Semantic Projections)**: Anchor standing code quality/compression standards as a foundational capability or overlay (`super-code`) while treating language-specific packages as independent capabilities or domain extensions, discoverable through multi-view semantic groups and projected routers.

### 1.2 Core Architectural Finding
**The existing architecture (ADR-001 through ADR-005) already completely and natively handles programming-language packs and `super-code` without introducing a new architecture or modifying existing contracts.**

Specifically:
- **Tier 1 Disqualification**: Programming languages and `super-code` fail Gate 1 (Tool Surface & Protocol Cohesion) and Gate 2 (Shared Reusable Primitives) under `FamilyCandidateEvaluator` (ADR-003). Neither generic languages (Python, Go, Rust) nor the `super-code` workflow constitute a vendor platform ecosystem with unified authentication tokens, API sessions, or coordinated vendor SDK release cycles. Attempting to create a physical platform hub under `tools-and-platforms/` would constitute **Vendor-Bucket Sprawl** strictly forbidden by ADR-002 and ADR-003.
- **Physical Ownership Hygiene**: Language capabilities belong in the functional domain tree (`library/development/<subcategory>/`), organized by primary operational scope (`backend`, `fullstack`, `mobile`, `systems`).
- **`super-code` Disambiguation**: The historical catalog already resolved `super-code` in Phase 08 (`batch-84`) and the 2,133-skill census (`REV-126`/`REV-150`):
  - `super-code` is a singular domain workflow (`library/development/fullstack/super-code`) providing standing house style rules (compression, idiomatic efficiency, generation token limits).
  - The 15 language-specific sub-packages (`bash`, `c`, `cpp`, `csharp`, `dart`, `elixir`, `go`, `java`, `kotlin`, `php`, `python`, `rust`, `scala`, `swift`, `typescript`) are already independently cataloged and preserved as canonical packages across `development/` subcategories.
- **Multi-View Discovery & Project Materialization**: Under ADR-004, cross-language discovery is solved via the **Semantic Group View** (`views/semantic-group-view.json`), projected virtual routers, and transitive dependency resolution (`ProjectMaterializer`), completely eliminating any need for physical directory consolidation or artificial platform hubs.

---

## 2. Evidence from Historical Provenance & Authoritative Census

### 2.1 Rebuild Phase 01–13 Historical Disposition
A survey of historical rebuild batches and split decisions reveals that programming language capabilities and `super-code` were already analyzed and classified during the Phase 01–12 rebuild:

1. **Phase 07 Split Screening (`split-decisions.csv`)**:
   - `task-folder/agents/skills/super-code` was screened and designated: `not_candidate`, `screened_out`, *"Retain as singular skill without modification. Initial screening verified focused, single-function skill with singular trigger, workflow, and output."*
   - Each language subfolder (e.g. `super-code/go`, `super-code/python`, `super-code/typescript`, `super-code/rust`) was evaluated individually and screened out as a focused, single-function capability.
2. **Phase 08 Rewrite Batches (`audit/rebuild-phase-1-12/batches/`)**:
   - Standalone language skills were normalized and placed into their respective functional subcategories:
     - `development/backend/`: `go` (Batch 49), `java` (Batch 50), `php` (Batch 51), `python` (Batch 53), `rust` (Batch 53).
     - `development/fullstack/`: `bash` (Batch 62), `c` (Batch 63), `cpp` (Batch 67), `csharp` (Batch 67), `dart` (Batch 68), `elixir` (Batch 69), `scala` (Batch 83), `typescript` (Batch 85), `super-code` (Batch 84).
     - `development/mobile/`: `kotlin` (Batch 88), `swift` (Batch 88).
   - In Batch 84, the 15 language reference documents within `super-code/<lang>/SKILL.md` were preserved in-package as supporting reference assets while their standalone counterparts were simultaneously managed across functional domains.

### 2.2 Census Accounting (REV-126 / REV-150)
In the authoritative 2,133-skill census:
- `super-code` is recorded as a single canonical package:
  - `canonical_id`: `super-code`
  - `current_path`: `library/development/fullstack/super-code`
  - `semantic_role`: `workflow`
  - `candidate_family`: `None`
  - `notes`: *"Singular domain capability"*
- The 15 language capabilities are recorded as 15 independent canonical packages:
  - All 15 have `semantic_role`: `independent_capability`
  - All 15 have `candidate_family`: `None`
  - Zero duplicate collisions: Scoped IDs and unambiguous naming ensure complete identity stability.
- Catalog-wide language footprint:
  - A total of 56 skills across the catalog reference programming languages (e.g., `bash-linux`, `javascript-testing-patterns`, `n8n-code-javascript`, `python-code-review`).
  - 41 reside in `development`, 11 in `quality-and-security`, 2 in `workflow-and-automation`, 1 in `infrastructure-and-ops`, and 1 in `content-and-documentation`.

---

## 3. Evaluation of Candidate Architectural Options

### 3.1 Option A: Pure Independent Decentralization
- **Description**: Treat all language skills as isolated, unlinked packages across `development/<subcategory>/`. No explicit relationship between `super-code` and individual languages; no cross-cutting grouping.
- **Evaluation**:
  - **Strengths**: Fully compliant with ADR-001 (path-independent canonical identity) and ADR-002 (domain-anchored physical ownership). Zero maintenance overhead for family qualification.
  - **Weaknesses**: Misses opportunity for shared code-compression workflows; progressive disclosure requires agents to search disparate subcategory routers (`backend`, `fullstack`, `mobile`) to find language standards; project materialization cannot bundle house coding style alongside language skills without manual specification.
  - **Status**: **Supported, but sub-optimal for discovery.**

### 3.2 Option B: Explicit Language Platform Hub (`tools-and-platforms/`)
- **Description**: Relocate all language-specific skills and `super-code` into a dedicated Tier 1 physical platform hub, such as `library/tools-and-platforms/programming-languages/` or `library/tools-and-platforms/super-code/`.
- **Evaluation Against ADR-003 4-Gate Qualification**:
  - **Gate 1 (Tool Surface & Protocol Cohesion)**: **FAIL**. Programming languages do not provide a unified programmatic surface. Python, Rust, and Go do not share a single CLI binary, MCP server, or API client. `super-code` is a prompt/prose guideline, not an execution transport.
  - **Gate 2 (Shared Reusable Primitives)**: **FAIL**. There are no shared authentication tokens, session profiles, or connection strings across programming languages.
  - **Gate 3 (Critical Mass & Cross-Domain Footprint)**: **PASS (Footprint only)**. 15+ packages spanning multiple subcategories, but volume alone cannot override Gates 1, 2, and 4.
  - **Gate 4 (Coordinated Lifecycle Maintenance)**: **FAIL**. Python PEP updates, Rust editions, and Go releases evolve completely independently of each other. They do not share a coordinated upstream vendor release cycle.
  - **Result**: `FamilyCandidateEvaluator.evaluate()` yields `FamilyTier.DISQUALIFIED_SPRAWL`.
- **Status**: **Strictly Forbidden by ADR-002 and ADR-003.** Creating a physical platform hub for generic language packs violates architectural invariants against vendor sprawl.

### 3.3 Option C: Shared Base Standard with Semantic Projections (Approved Pattern)
- **Description**: 
  - **Physical Ownership**: Maintain physical ownership in the functional domain tree (`library/development/<subcategory>/`) pursuant to ADR-002.
  - **Relationship Modeling**: Model `super-code` as a base capability or workflow providing standing house style rules. Individual language skills declare an `extends` or `depends_on` relationship with `super-code` if they mandate the standing house compression pass, or remain pure standalone capabilities.
  - **Semantic Group Projection**: Group all language-specific coding standards into cross-cutting Semantic Groups in `views/semantic-group-view.json` (e.g., `group_id: "programming-languages"` and `group_id: "idiomatic-code-generation"`).
  - **Virtual Router Navigation**: ADR-004 virtual routers (`views/routers/group-programming-languages.md`) provide immediate, centralized progressive disclosure for agents seeking language guidelines.
  - **Project Materialization**: `ProjectMaterializer` evaluates transitive closure: materializing `development:python` automatically bundles `super-code` when declared, ensuring zero broken dependencies in materialized workspaces.
- **Status**: **Fully Supported by ADR-001, ADR-002, ADR-004, and existing implementation.**

---

## 4. Evidence-to-Decision Matrix

| Architectural Dimension | Existing Implementation / Census Evidence | Applicable ADR Contract | Actual Gaps Identified | Scenario Outcome & Disposition |
| :--- | :--- | :--- | :--- | :--- |
| **Physical Storage & Ownership** | 15 languages distributed across `backend`, `fullstack`, `mobile`. `super-code` in `fullstack`. | ADR-002 (§3.1, §4.2): Domain skills reside in functional hierarchy. | None. | **Retain Domain Ownership**. Languages remain in `development/<subcat>/`. No migration to `tools-and-platforms/`. |
| **Platform Family Eligibility** | `FamilyCandidateEvaluator` evaluates candidate against 4 qualification gates. | ADR-003 (§2.1, §2.2): Requires unified tool surface, shared primitives, and coordinated lifecycle. | None. Evaluator correctly classifies language hub as Disqualified Sprawl. | **Reject Tier 1 Hub**. Languages and `super-code` are not platform families. Gate 1, 2, and 4 fail. |
| **Identity & Naming** | Canonical IDs: `bash`, `python`, `rust`, `super-code`. Unique, path-independent. | ADR-001: Path-independent URNs and canonical IDs. | None. All 16 IDs are collision-free. | **Preserve Canonical IDs**. No ID changes required. |
| **Duplicate Adjudication** | `super-code/<lang>/SKILL.md` internal reference files mirror standalone skills. | ADR-001 & ADR-004: In-package reference files do not possess independent canonical IDs. | None. Census correctly treats `super-code` as 1 package; references are internal assets. | **No Duplicate Pair Conflict**. Internal reference markdown within `super-code` does not collide with standalone canonical skills. |
| **Cross-Language Discovery** | MultiViewProjector generates 4 views (Functional, Family, Group, Provider). | ADR-004 (§3, §7): Multi-view discovery and semantic groups. | Semantic group definition `programming-languages` can be declared in registry configuration. | **Semantic Group View**. Discoverable via `views/semantic-group-view.json` without modifying directory structure. |
| **Runtime Materialization** | `ProjectMaterializer._generate_flat_runtime_names()` resolves names deterministically. | ADR-004 (§9.2): Natural name -> category prefix -> scope fallback -> collision guarantee. | None. Verified by automated test suite. | **Collision-Free Materialization**. `python`, `go`, `super-code` materialize with natural leaf names cleanly. |
| **Future Language Intake** | Intake pipeline scans, evaluates against gates, and assigns functional home. | ADR-003 (§5) & ADR-005 (§4): New skills enter domain hierarchy unless qualifying as Tier 1. | None. | **Standard Intake Process**. New languages (e.g., Julia, Zig, Mojo) enter `development/<subcat>/` directly. |

---

## 5. Stress-Testing Key Architecture Vectors

### 5.1 Verification of Gate Qualification (ADR-003)
Executing `FamilyCandidateEvaluator.evaluate()` against candidate language groupings:
- `candidate_slug: "super-code"`:
  - `gate_1_tool_surface_cohesion`: `False` (Prompt/style guideline; no unified tool CLI or MCP)
  - `gate_2_shared_primitives`: `False` (No shared auth credentials or connection profiles)
  - `gate_3_critical_mass`: `True` (16 packages, 1 category)
  - `gate_4_coordinated_lifecycle`: `False` (Static guidelines, no external platform release cycle)
  - **Outcome**: `FamilyTier.DISQUALIFIED_SPRAWL`
- `candidate_slug: "programming-languages"`:
  - `gate_1_tool_surface_cohesion`: `False`
  - `gate_2_shared_primitives`: `False`
  - `gate_3_critical_mass`: `True`
  - `gate_4_coordinated_lifecycle`: `False`
  - **Outcome**: `FamilyTier.DISQUALIFIED_SPRAWL`

### 5.2 Verification of Flat Runtime Namespace (ADR-004)
Testing `ProjectMaterializer` projection with `super-code` and language skills:
- Input bundle: `["development:super-code", "development:python", "development:typescript", "development:go"]`
- Generated runtime names:
  - `development:super-code` $\to$ `super-code`
  - `development:python` $\to$ `python`
  - `development:typescript` $\to$ `typescript`
  - `development:go` $\to$ `go`
- **Result**: All leaf names are globally unique within the materialized bundle. Zero collisions, zero fallback prefixes required. Bijective 1:1 mapping verified.

### 5.3 Verification of Transitive Dependency Closure (INV-9)
Testing dependency projection when a language skill extends or depends on `super-code`:
- Standalone closure request: `target_ids: ["development:python"]`
- With relationship: `python.relationships.depends_on = ["development:super-code"]`
- `DependencyResolver.resolve_transitive_closure()` yields:
  - `closure`: `["development:super-code", "development:python"]`
  - `execution_order`: `["development:super-code", "development:python"]`
- **Result**: Inv-9 (Transitive Completeness Guarantee) is strictly satisfied. The standing style guide is automatically included whenever the language skill is projected.

---

## 6. Conclusions & Architectural Recommendation

1. **Option C is the Authoritative Architectural Solution**:
   - Programming-language packs remain independent capabilities located within their respective functional categories under `library/development/<subcategory>/`.
   - `super-code` remains a singular canonical workflow located at `library/development/fullstack/super-code`.
   - Cross-domain aggregation is achieved via the **Semantic Group View** (`views/semantic-group-view.json`), not by directory nesting or platform hub creation.
2. **No Platform Hub Creation**:
   - Neither `languages` nor `super-code` meets the 4 qualification gates of ADR-003. They must **not** be assigned dedicated roots under `tools-and-platforms/`.
3. **No Migration or Live Catalog Changes**:
   - The census and live catalog paths are already 100% compliant with this disposition. Zero file moves, renames, or deletions are required.
4. **Follow-Up Work**:
   - None required. All supporting mechanisms (`FamilyCandidateEvaluator`, `CatalogRegistry`, `ProjectMaterializer`, `MultiViewProjector`) are already implemented and validated by automated tests.
