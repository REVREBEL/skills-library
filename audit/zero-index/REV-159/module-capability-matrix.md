# Module Capability Matrix: Repository-Native Core Modules

This document details the 14 explicitly named repository-native core modules under `tools/skill_library/` (plus the CLI entrypoint and scanner), their architectural responsibilities, key classes and callable functions, existing capabilities, limitations/guardrails, and how historical Drive-archived scripts map into or conflict with them.

---

## 1. Executive Summary of Core Cohort

The repository-native architecture formalized under ADR-001 through ADR-005 establishes a path-independent, contract-governed semantic object model for the skills library. Unlike the historical rebuild scripts—which operated primarily as linear procedural batch mutators and static phase verifiers—the core `tools/skill_library/` modules provide idempotent, read-safe, and verifiable operations.

| Module | Core Responsibility | Primary Contract / ADR | Key Classes & Callable Entrypoints |
| :--- | :--- | :--- | :--- |
| `object_model.py` | Canonical Identity & Object Graph | ADR-001 | `CanonicalIdentity.parse`, `ObjectGraph.add_object`, `ObjectGraph.validate_invariants` |
| `ledger.py` | Change Ledger Management | Living Library Contract | `ChangeLedger.record_change`, `ChangeLedger.list_changes`, `ChangeLedger.get_history` |
| `registry_contract.py` | Catalog & Multi-View Projections | ADR-004 | `CatalogCompiler.compile`, `CatalogRegistry.add_entry`, `AliasResolver.resolve`, `DependencyResolver.detect_cycle`, `ProjectMaterializer.materialize_bundle` |
| `config.py` | Runtime Configuration & Targets | Runtime Distribution | `load_runtime_targets`, `get_all_routers`, `RuntimeTarget.resolved_path` |
| `family_contract.py` | Family Qualification & Provider Bindings | ADR-003 | `FamilyQualificationGate.is_tier_1_eligible`, `FamilyCandidateEvaluator.evaluate`, `ExecutionProviderBinding.validate`, `ExecutionProviderContract.validate_capability_providers` |
| `physical_layout.py` | Physical Plane Boundaries | ADR-002 | `PhysicalPathContract.normalize`, `PhysicalPathContract.parse`, `PhysicalLayoutValidator.validate_object_placement`, `DuplicateCandidateRegistry.get_all_pairs` |
| `migration_gates.py` | Architecture Migration Gates | ADR-005 | `MigrationGateRunner.run_all_gates`, `SkillPackageManifest.from_directory`, `HistoricalProvenanceMapper.reconcile` |
| `manifest.py` | Runtime Distribution Manifest | Runtime Publication | `RuntimeManifest.load`, `RuntimeManifest.save`, `RuntimeManifest.build_from_library` |
| `sync.py` | Target Synchronization | Runtime Distribution | `sync_target`, `sync_all_targets`, `migrate_legacy_symlink_target` |
| `intake.py` | Reusable Intake Pipeline | Living Library Intake | `evaluate_candidate`, `compute_dice_similarity`, `apply_candidate`, `normalize_package_content` |
| `intake_capture.py` | Target State Capture | Living Library Intake | `scan_target_dirty_state`, `capture_dirty_target`, `convert_incoming_to_intake` |
| `publisher.py` | Runtime Branch Publication | Runtime Publication | `publish_runtime_branch`, `get_library_tree_sha`, `get_commit_tree_sha` |
| `validator.py` | Library Integrity Validation | Living Library Governance | `validate_library_integrity`, `validate_single_skill`, `parse_frontmatter` |
| `pilot.py` | Targeted Operational Pilot | Pilot Review Protocol | `run_targeted_pilot` |
| `scanner.py` | Filesystem Inventory Scanner | Inventory Discovery | `scan_candidate_directory`, `scan_runtime`, `run_full_scan` |
| `tools/skill-library.py` | Unified CLI Entrypoint | Operator Interface | Top-level CLI `main()` dispatching to `scan`, `intake`, `validate`, `sync`, `publish` |

### 1.1 Methodological Definition of Test Linkage (`has_test`)

In all crosswalk tables and audit deliverables:
- **`has_test = TRUE`**: Represents **static call linkage** to passing core contract test suites. The mapped callable or test class is confirmed via AST call and receiver tracing to be invoked within the 213 unit tests (`tests/test_*.py`). It does **NOT** denote dynamic runtime code coverage or line-by-line branch coverage instrumentation.
- **`has_test = UNVERIFIED`**: Represents architectural conceptual equivalence where modern core classes have contract tests, but the specific historical script entrypoint or utility lacks direct unit test execution, or the historical script is retired/prohibited from execution.
- **`has_test = FALSE`**: Represents historical batch writers, in-place regex mutators, or ad-hoc scripts with no test coverage whatsoever.

---

## 2. Detailed Module Inspection & API Verification

### 2.1 `object_model.py`
- **Location:** `tools/skill_library/object_model.py`
- **Architectural Invariant:** Under ADR-001, identity is path-independent and scoped at minting. The identifier format is strictly `<scope>:<slug>` or `urn:skill:<scope>:<slug>` (with prefix `urn:skill:`).
  - Scope is an immutable identity namespace / provenance scope.
  - Path separators (`/`, `\`) and file extensions (`.md`, `.json`, etc.) are prohibited in canonical identities.
  - Scope and slug must match lowercase alphanumeric regex: `^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$`.
- **Key Classes & Methods:**
  - `CanonicalIdentity`: `parse(identifier: str) -> CanonicalIdentity`, `compact` property (`<scope>:<slug>`), `urn` property (`urn:skill:<scope>:<slug>`), `__post_init__()`.
  - `SkillRole`: Typed role enum: `INDEPENDENT_CAPABILITY`, `FAMILY_PRIMITIVE`, `WORKFLOW`, `OVERLAY`, `ADAPTER`, `ALIAS_CANDIDATE`, `REFERENCE_OR_SUPPORT_CANDIDATE`, `MANUAL_REVIEW`.
  - `ReviewStatus`: Lifecycle status enum: `DRAFT`, `IN_REVIEW`, `APPROVED`, `RETIRED`.
  - `RelationshipType`: Typed graph edge enum: `DEPENDS_ON`, `COMPOSED_OF`, `ADAPTS`, `OVERLAYS`, `REFERENCES`, `ALIASED_TO`.
  - `ObjectGraph`: In-memory DAG of skill objects. Callable entrypoints: `add_object(obj)`, `get_object(id)`, `resolve_alias(id)`, `validate_invariants()`, `export_catalog()`.
- **Existing Capabilities:** Enforces graph acyclicity (INV-1), single canonical ownership (INV-2), referential closure (INV-3).
- **Limitations & Guardrails:** Operates purely as an in-memory data model; does not perform direct filesystem mutation. Unscoped legacy identifiers cannot be coerced to URNs without formal minting.
- **Crosswalk Mapping:**
  - Replaces historical string-based classification in `classify_compatibility.py` and `build_phase_08_artifacts.py`.
  - Replaces `semantic_cleanup.py`'s destructive field deletions with formal data validation invariants.

### 2.2 `ledger.py`
- **Location:** `tools/skill_library/ledger.py`
- **Architectural Role:** Append-only JSONL recording of catalog and skill lifecycle changes into `audit/change-ledger.jsonl`.
- **Key Classes & Methods:**
  - `ChangeLedger`: `record_change(entry: dict) -> None`, `list_changes(skill_id: Optional[str] = None) -> list[dict]`, `get_history(skill_id: str) -> list[dict]`.
  - `get_current_iso_timestamp() -> str`: Generates deterministic UTC ISO-8601 timestamps.
- **Existing Capabilities:** Idempotent event logging, sequential event auditing, schema validation of change records.
- **Limitations & Guardrails:** Strictly append-only. No method exists to delete, overwrite, or mutate recorded historical entries.
- **Crosswalk Mapping:**
  - Modernizes `generate_ledger.py` and supersedes ad-hoc ledger patches in `fix_cumulative_reconciliation.py`.

### 2.3 `registry_contract.py`
- **Location:** `tools/skill_library/registry_contract.py`
- **Architectural Role:** Multi-view projection compiler, registry indexer, and alias adjudication engine conforming to ADR-004.
- **Key Classes & Methods:**
  - `CatalogCompiler`: `compile(catalog_registry: Optional[CatalogRegistry] = None) -> dict`. Compiles functional, family, semantic group, and provider views deterministically.
  - `CatalogRegistry`: `add_entry(entry: RegistryEntry)`, `get_entry(canonical_id: str)`, `add_semantic_group(group: SemanticGroupObject)`, `to_dict()`, `to_json()`, `from_json()`.
  - `AliasResolver`: `resolve(alias_id: str) -> str`, `adjudicate_duplicate_pair(...)`, `build_direction_neutral_duplicate_pair(...)`.
  - `DependencyResolver`: `validate_invariants()`, `detect_cycle() -> Optional[list[str]]`, `compute_transitive_closure(start_id: str) -> set[str]`, `compute_execution_plan() -> list[str]`.
  - `ProjectMaterializer`: `materialize_bundle(target_dir: str, canonical_ids: list[str]) -> dict`.
  - `FamilyRouterGenerator`: `generate_tier_1_hub_router(hub_name: str, members: list[RegistryEntry]) -> str`, `generate_tier_2_virtual_router(family_name: str, members: list[RegistryEntry]) -> str`.
- **Enums & Types:**
  - `ProjectionMode`: `FUNCTIONAL`, `FAMILY`, `SEMANTIC_GROUP`, `PROVIDER`.
  - `DuplicateAdjudicationOutcome`: `KEEP_CANONICAL`, `MERGE`, `SUPERSEDE`, `SPLIT`, `QUARANTINE`.
- **Existing Capabilities:** Idempotent compilation with zero variance across repeated runs on identical input.
- **Limitations & Guardrails:** Projections are generated dynamically in-memory or into designated build artifacts; does not mutate live skill directories.
- **Crosswalk Mapping:**
  - Replaces `build_phase_05_artifacts.py`, `build_phase_06_artifacts.py`, `build_phase_08_artifacts.py`, and `generate_batch_plan.py`.

### 2.4 `config.py`
- **Location:** `tools/skill_library/config.py`
- **Architectural Role:** Centralized configuration provider for runtime publication targets and repository paths.
- **Key Classes & Methods:**
  - `RuntimeTarget`: Dataclass with `name`, `path`, `mode`, `enabled`, and `resolved_path()` method.
  - `load_runtime_targets() -> list[RuntimeTarget]`: Parses target configuration from environment or repository settings.
  - `get_all_routers(root_path: Path) -> list[Path]`: Discovers all valid `ROUTER.md` and hub router files.
- **Crosswalk Mapping:**
  - Replaces hardcoded path constants scattered across historical phase verifiers (`verify_phase_04.py` through `verify_phase_12.py`).

### 2.5 `family_contract.py`
- **Location:** `tools/skill_library/family_contract.py`
- **Architectural Role:** Governs family qualification gates, evidence integrity, and provider neutrality (ADR-003).
- **Key Classes & Methods:**
  - `FamilyQualificationGate`: `is_tier_1_eligible(record: FamilyQualificationRecord) -> bool`, `is_tier_2_eligible(record: FamilyQualificationRecord) -> bool`.
  - `FamilyCandidateEvaluator`: `evaluate(record: FamilyQualificationRecord) -> FamilyTier`, `validate_record_integrity(record)`.
  - `ExecutionProviderBinding`: `validate() -> bool`.
  - `ExecutionProviderContract`: `validate_capability_providers(skill: SkillObject, bindings: list[ExecutionProviderBinding])`, `validate_adapter_purity(adapter: AdapterObject)`.
- **Enums & Types:**
  - `FamilyTier`: `TIER_1_CANONICAL`, `TIER_2_VIRTUAL`, `UNQUALIFIED`.
  - `EvidenceStatus`: `VERIFIED`, `INSUFFICIENT`, `CONTRADICTORY`.
  - `ProviderType`: `ANTHROPIC`, `BEDROCK`, `VERTEX`, `LOCAL`, `GENERIC_OPENAI`.
- **Existing Capabilities:** Enforces Tier 1 qualification threshold (>=5 verified members across multiple categories, shared primitives, tool surface, coordinated lifecycle).
- **Limitations & Guardrails:** Enforces provider neutrality contractually via structured bindings; does not perform blind regex string replacements in skill bodies.
- **Crosswalk Mapping:**
  - Replaces `analyze_provider_coupling_detailed.py`, `analyze_provider_dependencies.py`, and `classify_compatibility.py`.
  - Prohibits historical mutators: `execute_provider_conversion*.py` and `neutralize_claude_dependencies*.py`.

### 2.6 `physical_layout.py`
- **Location:** `tools/skill_library/physical_layout.py`
- **Architectural Role:** Enforces namespace containment and physical plane boundaries (ADR-002).
- **Key Classes & Methods:**
  - `PhysicalPlane`: Plane enum: `CANONICAL`, `HUB`, `TIER_2_VIRTUAL`, `ADAPTER`, `SCRATCH`, `QUARANTINE`.
  - `PhysicalPathContract`: `normalize(path: str) -> str`, `parse(path: str) -> ParsedPhysicalPath`.
  - `PhysicalLayoutValidator`: `validate_object_placement(obj: SkillObject, path: str) -> bool`, `verify_path_independent_relocation(old_path, new_path) -> bool`.
  - `DuplicateCandidateRegistry`: `is_candidate_leaf(path)`, `get_candidate_hypothesis(path)`, `get_all_pairs()`.
- **Existing Capabilities:** Validates that skill packages adhere to designated planes without rogue symlinks or unauthorized subdirectories.
- **Crosswalk Mapping:**
  - Replaces `build_phase_07_artifacts.py` and `verify_phase_07.py`.

### 2.7 `migration_gates.py`
- **Location:** `tools/skill_library/migration_gates.py`
- **Architectural Role:** Comprehensive architecture migration gate runner (G01–G09) and manifest generator (ADR-005).
- **Key Classes & Methods:**
  - `SkillPackageManifest`: `from_directory(path: Path) -> SkillPackageManifest`, `root_path -> Path`, `to_dict() -> dict`. Computes root manifest SHA-256 and individual file asset digests.
  - `HistoricalProvenanceMapper`: `reconcile(historical_path: str) -> HistoricalProvenanceRecord`, `normalize_historical_destination(dest)`, `load_phase08_canonical_registry(path)`, `load_census(path)`.
  - `MigrationGateRunner`: `run_gate(gate_id: GateID) -> GateResult`, `run_all_gates() -> MigrationGateReport`.
- **Gate Definitions:**
  - `G01`: Canonical Identity Validation
  - `G02`: Family Qualification Gate
  - `G03`: Graph Topology & Acyclicity
  - `G04`: Resource Preservation
  - `G05`: Reference Closure
  - `G06`: View Reconciliation
  - `G07`: Deterministic Compilation
  - `G08`: Project Materialization
  - `G09`: Runtime Publication Pre-Flight
- **Crosswalk Mapping:**
  - Formalizes and supersedes `generate_inventory.py`, `verify_phase_08_cumulative.py`, and `verify_phase_09.py`.

### 2.8 `manifest.py`
- **Location:** `tools/skill_library/manifest.py`
- **Architectural Role:** Generates and maintains runtime publication manifests.
- **Key Classes & Methods:**
  - `RuntimeManifest`: `load(path: Path)`, `save(path: Path)`, `add_skill(skill: dict)`, `build_from_library(library_path: Path)`.

### 2.9 `sync.py`
- **Location:** `tools/skill_library/sync.py`
- **Architectural Role:** Multi-target synchronization for local runtime distributions using git sparse-checkout.
- **Key Classes & Methods:**
  - `sync_target(target: RuntimeTarget)`, `sync_all_targets()`, `migrate_legacy_symlink_target(target)`.

### 2.10 `intake.py` & `intake_capture.py`
- **Location:** `tools/skill_library/intake.py` and `intake_capture.py`
- **Architectural Role:** Living library intake pipeline for discovering, evaluating, and safely importing candidate skills.
- **Key Classes & Methods:**
  - `evaluate_candidate(candidate_path: Path) -> IntakeEvaluation`: Checks frontmatter schema and calculates Dice similarity against existing catalog.
  - `scan_target_dirty_state(target_path: Path)`: Captures external runtime modifications safely into staging.

### 2.11 `publisher.py`
- **Location:** `tools/skill_library/publisher.py`
- **Architectural Role:** Publication gate and branch publisher for runtime distribution branches.
- **Key Classes & Methods:**
  - `publish_runtime_branch()`, `get_library_tree_sha()`, `get_commit_tree_sha(commit)`.

### 2.12 `validator.py`
- **Location:** `tools/skill_library/validator.py`
- **Architectural Role:** Production whole-library frontmatter and integrity validation.
- **Key Classes & Methods:**
  - `validate_library_integrity(library_path: Path) -> ValidationResult`, `validate_single_skill(skill_path: Path)`.
- **Crosswalk Mapping:**
  - Replaces `fix_registry_check.py`, `gen_phase11_artifacts.py`, and `verify_phase_11.py`.

### 2.13 `pilot.py`
- **Location:** `tools/skill_library/pilot.py`
- **Architectural Role:** Targeted operational pilot execution and validation.
- **Key Classes & Methods:**
  - `run_targeted_pilot(skill_path: Path) -> PilotResult`.
- **Crosswalk Mapping:**
  - Replaces `gen_phase12_artifacts.py` and `verify_phase_12.py`.
