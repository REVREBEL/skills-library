# Implementation Traceability Matrix: Contracts, Symbols, Tests, and Runtime Boundaries

## 1. Executive Summary

This matrix establishes the comprehensive, empirical mapping between architectural contracts (ADR-000 through ADR-005, Migration Roadmap) and the existing codebase across five primary core modules:
1. `tools/skill_library/object_model.py` (`CanonicalIdentity`, `ObjectGraph`)
2. `tools/skill_library/registry_contract.py` (Registry, Router, and Alias contracts)
3. `tools/skill_library/ledger.py` (`ChangeLedger`)
4. `tools/skill_library/config.py` (Path, Category, and Security contracts)
5. `tools/skill_library/physical_layout.py` (Physical planes, syntax, and duplicate pairs)

Additionally, this matrix rigorously delineates **implemented and test-verified invariants** from **unverified runtime integrations**.

---

## 2. Invariant Implementation Status Delineation

To maintain absolute architectural integrity, contracts are classified into two rigorous categories:

### A. Implemented & Test-Verified Invariants
These contracts are fully implemented in core modules, enforced via fail-closed validation logic, and proven with 218 passing automated unit tests in `tests/test_*.py`.
- **INV-1 (DAG Acyclicity)**: Enforced via `ObjectGraph.validate_invariants()` and `DependencyResolver.resolve_dependencies()`. Tested in `test_semantic_object_model.py` and `test_registry_router_contracts.py`.
- **INV-2 (Single Canonical Owner)**: Enforced via `ObjectGraph.register_node()`. Tested in `test_semantic_object_model.py` and `test_migration_gates.py`.
- **INV-3 (Single-Hop Alias Purity)**: Enforced via `AliasResolver.resolve_alias()` and `ObjectGraph.validate_invariants()`. Tested in `test_semantic_object_model.py` and `test_registry_router_contracts.py`.
- **INV-4 (Physical Plane Separation)**: Enforced via `PhysicalPathContract.validate_path()`. Tested in `test_physical_ownership.py`.
- **INV-5 (Census-Grounded Family Eligibility)**: Enforced via `FamilyCandidateEvaluator` and `AuthoritativeCensus`. Tested across 14 tests in `test_family_eligibility.py`.
- **INV-6 (Path Independence)**: Enforced via `CanonicalIdentity` syntax validation and `RegistryEntry`. Tested in `test_semantic_object_model.py` and `test_registry_router_contracts.py`.
- **INV-7 (Reference Closure)**: Enforced via `MigrationGateEvaluator.evaluate_gate5()`. Tested in `test_migration_gates.py`.
- **INV-8 (Asset Integrity Preservation)**: Enforced via `compare_package_manifests()` and `MigrationGateEvaluator.evaluate_gate4()`. Tested across 27 tests in `test_migration_gates.py`.
- **INV-9 (Transitive Runtime Completeness)**: Enforced via `ProjectMaterializer.materialize_project()`. Tested in `test_registry_router_contracts.py`.
- **INV-10 (Path Containment Safety)**: Enforced via `check_path_containment()` and `is_subpath()`. Tested in `test_migration_gates.py`.
- **Provisional Guardrail 4 (Overlay Depth 1)**: Enforced via `ObjectGraph.validate_invariants()`. Tested in `test_semantic_object_model.py`.
- **Provisional Guardrail 5 (Primitive Composition Discipline)**: Enforced via `ObjectGraph.validate_invariants()`. Tested in `test_semantic_object_model.py`.

### B. Unverified / Partially Implemented Runtime Integrations
These capabilities define contracts that are structurally complete in code and specifications, but possess incomplete automated end-to-end integration or pending live deployment verification (as cataloged in the SKIL-13 failure register):
1. **Live Remote Git Workflow Dispatch (`ROAD-002`, `publisher.py:publish_runtime_branch`)**:
   - *Status*: **PARTIALLY_IMPLEMENTED (UNVERIFIED_RUNTIME)**
   - *Issue*: `tests/test_runtime_publication.py:test_21_dispatch_remote_workflow_success` calls host `gh workflow run` without mock interception, causing external CI runs and failure in isolated test environments.
   - *Remediation Required*: Inject mock execution stub for `gh` subprocess calls during test execution.
2. **Directory-to-Frontmatter External Rename Sync (`validator.py:validate_single_skill`)**:
   - *Status*: **PARTIALLY_IMPLEMENTED (UNVERIFIED_RUNTIME)**
   - *Issue*: `tests/test_runtime_publication.py:test_24` encounters directory-to-frontmatter mismatch when external tools rename folders without updating `SKILL.md` frontmatter `name`.
   - *Remediation Required*: Add automated frontmatter reconciliation hook or strict fail-closed rejection.
3. **Target Git Checkout Scope Verification (`validator.py:validate_library_integrity`)**:
   - *Status*: **PARTIALLY_IMPLEMENTED (UNVERIFIED_RUNTIME)**
   - *Issue*: Running `tools/skill-library.py validate` on a pristine clone fails target checkout verification because the local branch `runtime-targets` is not checked out by default.
   - *Remediation Required*: Decouple target checkout verification into optional pre-flight step or clone isolated worktree.

---

## 3. Module-by-Module Symbol and Test Mapping

### 1. `tools/skill_library/object_model.py`
| Symbol | Architectural Role | Associated Invariants / ADRs | Unit Test Linkage |
| :--- | :--- | :--- | :--- |
| `CanonicalIdentity` | Immutable RFC 8141 URN & compact `<scope>:<slug>` parser | ADR-001, INV-6 | `tests/test_semantic_object_model.py:TestCanonicalIdentity` (5 tests) |
| `SkillRole` | 10 first-class object roles enum (Capability, Workflow, Primitive, Overlay, Adapter, Router, Reference, GeneratedArtifact, Family, Alias) | ADR-000 | `tests/test_semantic_object_model.py:TestFirstClassObjectTypes.test_all_ten_first_class_roles_exist_and_normalize` |
| `ReviewStatus` | Analytical review lifecycle status (active, provisional, manual_review) | ADR-000 | `tests/test_semantic_object_model.py:TestFirstClassObjectTypes.test_manual_review_is_review_status_not_object_type` |
| `RelationshipType` | 8 typed graph edges (composed_of, extends, depends_on, adapts, aliased_to, etc.) | ADR-000 | `tests/test_semantic_object_model.py:TestFirstClassObjectTypes` |
| `SkillObject` | Base dataclass holding 4 decoupled architectural axes | ADR-000, ADR-001 | `tests/test_semantic_object_model.py:TestCatalogBoundaryCaseStudies` |
| `ObjectGraph` | In-memory graph engine with fail-closed invariant validation | INV-1, INV-2, INV-3, Guardrails 4 & 5 | `tests/test_semantic_object_model.py:TestObjectGraphInvariants` (9 tests) |

### 2. `tools/skill_library/registry_contract.py`
| Symbol | Architectural Role | Associated Invariants / ADRs | Unit Test Linkage |
| :--- | :--- | :--- | :--- |
| `RegistryEntry` | Authoritative single-skill record with 4 axes, relationships, and metadata | ADR-004, INV-6 | `tests/test_registry_router_contracts.py:TestRegistryEntryAndIdentity` (3 tests) |
| `CatalogRegistry` | Full catalog state container with index lookups | ADR-004 | `tests/test_registry_router_contracts.py:TestCatalogRegistryCompilation` |
| `CatalogCompiler` | Deterministic compiler transforming raw files and census into registry | ADR-004, Gate 7 | `tests/test_registry_router_contracts.py:TestCatalogRegistryCompilation.test_compile_deterministic_hash_equality` |
| `MultiViewProjector` | Compiler generating Functional, Family, Semantic Group, Provider views & Search Index | ADR-004, Gate 6 | `tests/test_registry_router_contracts.py:TestMultiViewProjection` (6 tests) |
| `AliasResolver` | Single-hop alias dereferencing engine | ADR-004, INV-3 | `tests/test_registry_router_contracts.py:TestAliasResolution` (5 tests) |
| `DependencyResolver` | Topological sorter and cycle detector for DAG dependencies | ADR-004, INV-1 | `tests/test_registry_router_contracts.py:TestDependencyResolver` (4 tests) |
| `ProjectMaterializer` | Flat runtime symlink materializer with collision-free naming ladder | ADR-004, INV-9, Gate 8 | `tests/test_registry_router_contracts.py:TestProjectMaterializerAndTransitiveCompleteness` (4 tests) |
| `SemanticGroupObject`| Logical cross-cutting grouping structure | ADR-004 | `tests/test_registry_router_contracts.py:TestSemanticGroups` (2 tests) |

### 3. `tools/skill_library/ledger.py`
| Symbol | Architectural Role | Associated Invariants / ADRs | Unit Test Linkage |
| :--- | :--- | :--- | :--- |
| `ChangeLedger` | Append-only audit logger writing to `audit/change-ledger.jsonl` | Roadmap, OPS-001 | `tests/test_scenarios.py:TestSkillLibraryIsolatedScenarios.test_scenario_a_manual_intake_end_to_end` |
| `get_current_iso_timestamp` | ISO 8601 UTC timestamp generator | OPS-001 | `tests/test_scenarios.py` |

### 4. `tools/skill_library/config.py`
| Symbol | Architectural Role | Associated Invariants / ADRs | Unit Test Linkage |
| :--- | :--- | :--- | :--- |
| `REPO_ROOT`, `LIBRARY_DIR`, `RUNTIME_DIR`, `AUDIT_DIR` | Centralized filesystem path constants | OPS-002 | `tests/test_scenarios.py:TestGlobalRuntimePath` (3 tests) |
| `CATEGORIES`, `DEEP_CATEGORIES`, `FLAT_CATEGORIES` | 10 canonical domain taxonomy categories | ADR-002, INV-4 | `tests/test_physical_ownership.py:TestPhysicalPathContract` |
| `TRIGGER_CONTRACT_PATTERN` | Regex ensuring frontmatter contains `Use when:` trigger contract | Frontmatter Contract | `tools/skill_library/validator.py:validate_single_skill` |
| `DESTRUCTIVE_COMMAND_PATTERNS`, `SECRET_PATTERNS`, `WORKSTATION_PATH_PATTERNS` | Security, privacy, and sanitization regex filters | OPS-003, INV-10 | `tests/test_scenarios.py:TestSkillLibraryIsolatedScenarios.test_scenario_b_external_installer_simulation` |

### 5. `tools/skill_library/physical_layout.py`
| Symbol | Architectural Role | Associated Invariants / ADRs | Unit Test Linkage |
| :--- | :--- | :--- | :--- |
| `PhysicalPlane` | Enum defining 3 storage planes (Domain Tree, Platform Hub, Meta-Infrastructure) | ADR-002, INV-4 | `tests/test_physical_ownership.py:TestPhysicalPathContract` |
| `ParsedPhysicalPath` | Structured representation of validated physical path | ADR-002 | `tests/test_physical_ownership.py:TestPhysicalPathContract` |
| `PhysicalPathContract` | Path normalization, POSIX syntax, and max-depth bounds | ADR-002, INV-4, INV-10 | `tests/test_physical_ownership.py:TestPhysicalPathContract` (10 tests) |
| `PhysicalLayoutValidator` | Structural validator enforcing adapter/overlay physical directories | ADR-002, Gate 2 | `tests/test_physical_ownership.py:TestPhysicalLayoutValidator` (4 tests) |
| `DuplicateCandidateRegistry` | Direction-neutral container for 15 candidate duplicate pairs | ADR-002, Gate 2 | `tests/test_physical_ownership.py:TestDuplicateCandidateRegistry` (5 tests) |
