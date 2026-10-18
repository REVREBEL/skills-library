# Task Spec — Phase 05: Multi-View Router Generation & Universal Reference Closure

- **Status**: Authoritative (REV-132)
- **Work Order**: Phase 05 of Skills Library Implementation Roadmap
- **Enforced Gates**: **Gate 5: Reference Closure & Dependency Completeness** (INV-7), **Gate 6: Generated-View Reconciliation & Router Integrity**
- **Architecture Reference**: [ADR-004 (REV-130)](../docs/architecture/decisions/ADR-004-registry-router-alias-dependency-contracts.md), [ADR-005 (REV-131)](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)

---

## 1. Objective

Deterministically compile multi-view router projections and inverted token search indexes while guaranteeing universal reference closure across all dependencies, compositions, extensions, and aliases in the catalog. Enforce strict relative-path link purity and provider badging across all router documents.

---

## 2. Preconditions

1. Phases 01 through 04 completed with Gates 1 through 4 reporting `PASSED`.
2. Physical skill packages are stable at their verified locations.
3. Catalog registry contains all active packages, canonical IDs, and relationship edges.
4. Working tree under `audit/taxonomy-census/**` is clean.

---

## 3. Canonical Task Skills & Engine

- Implementation Module: `tools/skill_library/registry_contract.py` (`MultiViewProjector`, `FamilyRouterGenerator`, `DependencyResolver`)
- Migration Engine: `tools/skill_library/migration_gates.py` (Gate 5 & Gate 6 Evaluators)
- Test Suite: `tests/test_registry_router_contracts.py`, `tests/test_migration_gates.py`

---

## 4. Step-by-Step Work

1. **Verify Universal Reference Closure (Gate 5 Preflight)**:
   - For every active skill package $u \in V$:
     - Check each dependency $d \in \text{depends\_on}(u)$: verify $d \in V$. Dangling dependency fails with `DANGLING_DEPENDENCY_REFERENCE`.
     - Check each component $c \in \text{composed\_of}(u)$: verify $c \in V$. Dangling component fails with `DANGLING_COMPOSITION_REFERENCE`.
     - Check each base $b \in \text{extends}(u)$: verify $b \in V$. Dangling overlay target fails with `DANGLING_OVERLAY_TARGET`.
     - Check each target $a \in \text{aliased\_to}(u)$: verify $a \in V$. Dangling alias target fails with `DANGLING_ALIAS_TARGET`.
   - Run `MigrationGateEvaluator.evaluate_gate_5_reference_closure(registry)`. Ensure status is `PASSED`.
2. **Generate Multi-View Router Projections**:
   - Execute `MultiViewProjector.generate_projections(registry)`.
   - **View 1 (Functional Domain Hierarchy)**:
     - Generate router `SKILL.md` for each functional category (e.g. `library/development/SKILL.md`, `library/development/backend/SKILL.md`).
     - Group children by subcategory and progressive trigger boundaries.
   - **View 2 (Platform Family Hubs)**:
     - Generate hub `SKILL.md` for each qualified Tier 1 platform family (e.g. `library/tools-and-platforms/github/SKILL.md`).
     - Display execution provider badges (`CLI`, `MCP`, `REST`, `SDK`, `Prompt`).
   - **View 3 (Capability Overlays & Semantic Groups)**:
     - Compile virtual cross-cutting indices and pack definitions.
3. **Enforce Relative Link Purity in Router Documents**:
   - Verify that all hyperlinks in generated router documents use strictly relative paths (e.g. `backend/database-migration/SKILL.md` or `../../development/git/SKILL.md`).
   - Reject any absolute filesystem path (`/Users/...`, `C:\...`) with `ABSOLUTE_PATH_IN_ROUTER`.
   - Reject any repository-root pseudo-URL (`file:///...`) with `FORBIDDEN_FILE_PROTOCOL_LINK`.
4. **Generate Inverted Token Search Index**:
   - Run `CatalogCompiler.generate_search_index(registry)`.
   - Index 100% of active skills by name, title, keywords, tags, category, and tokens.
   - Output `audit/search-index.json`.
5. **Execute Gate 6 Validation**:
   - Run `MigrationGateEvaluator.evaluate_gate_6_view_reconciliation(registry)`.
   - Confirm 100% catalog coverage across projections.
   - Confirm zero broken links, zero dead routes, and zero forbidden link schemes.

---

## 5. Artifacts

Create or update:
- Root router: `library/SKILL.md`
- Category and Subcategory routers: `library/<category>/SKILL.md`, `library/<category>/<subcategory>/SKILL.md`
- Platform Family Hub routers: `library/tools-and-platforms/<family-slug>/SKILL.md`
- Inverted search index: `audit/search-index.json`
- Reference audit log: `audit/reference-closure-report.json`

---

## 6. Reconciliation Requirements

- 100% of reference edges across all active skills must resolve to active catalog entries ($u \to \emptyset$ count: 0).
- 100% of active skills must appear in at least one router projection.
- 100% of router links must be relative paths and resolve to valid on-disk files.
- Gates 5 and 6 must report `status: PASSED` with 0 violations.

---

## 7. Repository Checkpoint

1. Branch name: `feature/migration-phase-05-routers-and-closure`.
2. Commit message: `feat(migration): complete phase 05 multi-view router generation and universal reference closure`.
3. Pull Request must include:
   - Summary of generated domain and platform router hierarchies.
   - Reference closure audit showing 0 dangling references across all relationships.
   - Gates 5 and 6 validation reports showing 0 violations.
4. Leave PR open for review; do not proceed to Phase 06 until approved.

---

## 8. Completion Gate

Complete only when:
- [ ] Universal reference closure verified across 100% of catalog edges.
- [ ] Multi-view projections cover 100% of active skills.
- [ ] All router markdown links are strictly relative and resolve on disk.
- [ ] `audit/search-index.json` is generated and committed.
- [ ] `MigrationGateRunner.run_gate(GateID.GATE_5_REFERENCE_CLOSURE)` returns `PASSED`.
- [ ] `MigrationGateRunner.run_gate(GateID.GATE_6_VIEW_RECONCILIATION)` returns `PASSED`.
- [ ] Automated regression tests pass: `PYTHONPATH=tools python3 -m unittest tests/test_registry_router_contracts.py tests/test_migration_gates.py`.
