# Current Implementation Coverage Analysis

**Task:** SKIL-13 | ZI-04: Validate existing code and CI from pinned SHA  
**Pinned Git SHA:** `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Execution Timestamp:** 2026-11-04T05:08:00Z  

---

## 1. Executive Capability Classification

Each architectural subsystem in `tools/skill_library/` and `tools/` is categorized into one of five maturity levels based on empirical testing from the pinned snapshot:
- **Tested & Verified:** Comprehensive unit/contract test coverage; operational code executes without errors.
- **Tested & Partial:** Implemented and largely functional; exhibits localized edge-case failures or environment coupling.
- **Docs-Only:** Defined in specifications or architecture ADRs without functional executable implementation.
- **Absent:** Required by architecture design but completely omitted from pinned codebase.
- **Blocked:** Implemented but blocked from successful execution due to external or state preconditions.

---

## 2. Detailed Capability Evaluation

| Architectural Capability | Module / Component | Status | Code Artifacts | Test Artifacts | Empirical Findings & Limitations |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Canonical Object Model & Invariants** | `object_model.py` | **Tested & Verified** | `SkillObject`, `CapabilityObject`, `WorkflowObject`, `PrimitiveObject`, `OverlayObject`, `AdapterObject`, `AliasObject`, `RouterObject` | `test_semantic_object_model.py` (35 tests) | Invariants INV-1 to INV-6 strictly enforced. Acyclicity, single canonical owner, and single-hop aliases verified. |
| **Family Contracts & Census Qualification** | `family_contract.py` | **Tested & Verified** | `AuthoritativeCensus`, `FamilyQualificationGate`, `FamilyCandidateEvaluator` | `test_family_eligibility.py` (40 tests) | Census-backed validation strictly enforces evidence. Correctly differentiates Tier 1, Tier 2, Disqualified sprawl, and PENDING holds. |
| **Semantic Census Compilation** | `tools/catalog_semantic_census.py` | **Tested & Verified** | Standalone compiler, tokenizer, heuristic auditor | `test_semantic_census.py` (10 tests) | Deterministic generation of 2,133-item census dataset (`semantic-role-census.json` & `.csv`). 100% byte-for-byte reproducible. |
| **Universal Catalog Registry & Multi-View** | `registry_contract.py` | **Tested & Verified** | `CatalogRegistry`, `CatalogCompiler`, `MultiViewProjector`, `AliasResolver`, `ProjectMaterializer` | `test_registry_router_contracts.py` (39 tests) | Implements REV-130 / ADR-004 contracts. All 4 projection modes operational. Project materializer candidate ladder tested. |
| **Physical Layout & Duplicate Governance** | `physical_layout.py` | **Tested & Verified** | `PhysicalLayoutValidator`, `DuplicateResolutionRegistry` | `test_physical_ownership.py` (19 tests) | Enforces REV-125 duplicate freeze. Prevents destructive deletion of frozen duplicates during transition hold. |
| **Migration Gates 1–9 & Provenance Ledger** | `migration_gates.py`, `ledger.py` | **Tested & Verified** | `MigrationGateRunner`, `HistoricalProvenanceMapper`, `ChangeLedger` | `test_migration_gates.py` (56 tests) | All 9 migration gates executable. Provenance mapper reconciles legacy CSV evidence. Change ledger records transitions. |
| **Migration Roadmap & Specification Integrity** | `docs/architecture/` | **Tested & Verified** | `MIGRATION_ROADMAP.md`, `library-rebuild-tasks/` | `test_migration_roadmap.py` (14 tests) | Roadmap covers all 9 gates and 10 invariants. Requires `PYTHONPATH=tools` for standalone execution due to missing path injection. |
| **Runtime Publication Engine** | `publisher.py` | **Tested & Partial** | `publish_runtime_branch`, tree hash helpers | `test_runtime_publication.py` (Tests 1–4) | Publishes `main:library/` tree to standalone `runtime` branch. Functional, but on fresh checkout `validate` fails until published. |
| **Target Synchronization & Sparse Checkout** | `sync.py` | **Tested & Verified** | `sync_target`, `sync_all_targets`, `detect_target_state` | `test_runtime_publication.py` (Tests 5–9, 13–20) | Fully manages physical clones and git sparse-checkout rules for subset targets. Prevents clobbering dirty working trees. |
| **Dirty Target Intake Capture** | `intake_capture.py` | **Tested & Partial** | `capture_dirty_target`, `convert_incoming_to_intake` | `test_runtime_publication.py` (Tests 10–12, 21–24) | Groups dirty workstation modifications into `incoming/*` branches. `test_21` fails due to unmocked `gh` CLI invocation. |
| **Intake Evaluation & Governance Gates** | `intake.py` | **Tested & Partial** | `evaluate_candidate`, `apply_candidate`, similarity engine | `test_runtime_publication.py` (Test 25), `test_scenarios.py` | Enforces human approval gates on new/overlapping candidates. `test_24` fails on external rename due to frontmatter/dir mismatch. |
| **Living Library Integrity Validator** | `validator.py` | **Tested & Blocked** | `validate_library`, `validate_library_integrity` | Invoked via CLI `tools/skill-library.py validate` | AST and link scanning work (2,102 active skills, 26 routers, 2,176 links verified). Fails on pinned commit due to unpublished runtime ref. |
| **CLI Unified Management Interface** | `tools/skill-library.py` | **Tested & Verified** | Subcommands: `scan`, `intake`, `apply`, `publish-runtime`, `sync`, `capture-intake`, `convert-incoming`, `validate`, `status`, `test` | Tested across 11 CLI subcommands | All subcommands parse arguments and execute cleanly. Exit codes correctly indicate validation/test status. |

---

## 3. Summary of Implementation Gaps

1. **Path Configuration in `test_migration_roadmap.py`:**  
   Unlike other test files that explicitly insert `tools` into `sys.path`, `test_migration_roadmap.py` relies on `PYTHONPATH` being externally set.
2. **External Process Mocking in `intake_capture.py` / `test_runtime_publication.py`:**  
   `capture_dirty_target()` shells out directly to `gh workflow run` without abstracting or mocking the call. When `gh` is authenticated, the call succeeds, breaking negative assertions in `test_21`.
3. **Directory-to-Frontmatter Coupling on External Renames:**  
   When a skill package is renamed in a runtime checkout, `validate_single_skill()` asserts that the directory name matches the `name:` attribute in `SKILL.md`. In an external rename proposal where the folder was moved but the frontmatter not yet edited, validation fails, setting `is_valid_package=False` and causing `test_24` to fail.
4. **Initial Repository State Coupling in `validator.py`:**  
   `validate_library_integrity()` expects the local git ref `refs/heads/runtime` to exist and point to the tree of `HEAD:library`. On a fresh clone or pinned checkout where `publish-runtime` has not yet been executed, `validate` immediately exits 1.
