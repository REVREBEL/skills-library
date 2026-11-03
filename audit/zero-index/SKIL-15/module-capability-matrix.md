# Module Capability Matrix: Repository-Native Core Modules

This document details the 14 explicitly named repository-native core modules under `tools/skill_library/` (plus the CLI entrypoint and scanner), their architectural responsibilities, key classes and functions, existing capabilities, limitations/guardrails, and how historical Drive-archived scripts map into or conflict with them.

---

## 1. Executive Summary of Core Cohort

The repository-native architecture formalized under ADR-001 through ADR-005 establishes a path-independent, contract-governed semantic object model for the skills library. Unlike the historical rebuild scripts—which operated primarily as linear procedural batch mutators and static phase verifiers—the core `tools/skill_library/` modules provide idempotent, read-safe, and verifiable operations.

| Module | Core Responsibility | Primary Contract / ADR | Key Capabilities |
| :--- | :--- | :--- | :--- |
| `object_model.py` | Canonical Identity & Object Graph | ADR-001 | Path-independent URNs, immutable objects, relationship graph |
| `ledger.py` | Change Ledger Management | Living Library Contract | Append-only JSONL recording, UTC ISO timestamps |
| `registry_contract.py` | Catalog & Multi-View Projections | ADR-004 | CatalogCompiler, RegistryEntry, Dependency/Alias resolvers |
| `config.py` | Runtime Configuration & Targets | Runtime Distribution | Target definitions, router catalog loading |
| `family_contract.py` | Family Qualification & Provider Bindings | ADR-003 | Census-backed gates, provider neutrality enforcement |
| `physical_layout.py` | Physical Plane Boundaries | ADR-002 | Namespace containment, duplicate candidate tracking |
| `migration_gates.py` | Architecture Migration Gates | ADR-005 | G01–G08 evaluation, package manifests, provenance mapper |
| `manifest.py` | Runtime Distribution Manifest | Runtime Publication | Runtime manifest generation, tree integrity hashing |
| `sync.py` | Target Synchronization | Runtime Distribution | Git sparse-checkout sync, legacy symlink migration |
| `intake.py` | Reusable Intake Pipeline | Living Library Intake | Candidate evaluation, Dice similarity, router updates |
| `intake_capture.py` | Target State Capture | Living Library Intake | Dirty target scanning, external provenance capture |
| `publisher.py` | Runtime Branch Publication | Runtime Publication | Tree-SHA comparison, push gates, publication logging |
| `validator.py` | Library Integrity Validation | Living Library Governance | Frontmatter schema, router references, integrity checks |
| `pilot.py` | Targeted Operational Pilot | Pilot Review Protocol | Targeted skill execution, pilot reporting |
| `scanner.py` | Filesystem Inventory Scanner | Inventory Discovery | Package discovery, SHA-256 manifest computation |
| `tools/skill-library.py` | Unified CLI Entrypoint | Operator Interface | Top-level CLI for intake, scan, validate, sync, publish |

---

## 2. Detailed Module Inspection

### 2.1 `object_model.py`
- **Location:** `tools/skill_library/object_model.py`
- **Responsibilities:** Enforces path-independent canonical identity (ADR-001), typed skill roles (`SkillRole`), review states (`ReviewStatus`), relationship graphs (`RelationshipType`, `Relationship`), and the semantic object model (`SkillObject`, `CapabilityObject`, `FamilyObject`, `RouterObject`, etc.).
- **Key Classes:** `CanonicalIdentity`, `SkillObject`, `ObjectGraph`, `Relationship`, `InvariantViolationError`.
- **Existing Capabilities:** Validates canonical URNs (`urn:revrebel:skill:<slug>`), enforces invariant contracts, prevents identity degradation when physical folders move.
- **Limitations & Guardrails:** Does not perform filesystem I/O directly; operates purely on memory models. Cannot coerce malformed URNs.
- **Crosswalk Mapping:**
  - Supersedes historical ad-hoc path parsing in `classify_compatibility.py` and `build_phase_08_artifacts.py`.
  - Replaces `semantic_cleanup.py`'s one-time string sanitization with formal data invariants.

### 2.2 `ledger.py`
- **Location:** `tools/skill_library/ledger.py`
- **Responsibilities:** Append-only recording of catalog and skill lifecycle changes into `audit/change-ledger.jsonl`.
- **Key Classes:** `ChangeLedger`.
- **Existing Capabilities:** Idempotent event logging, deterministic ISO-8601 UTC timestamps, schema validation of ledger records.
- **Limitations & Guardrails:** Append-only; forbids retroactive mutation or row deletion.
- **Crosswalk Mapping:**
  - Codifies and replaces `generate_ledger.py` and `fix_cumulative_reconciliation.py`.
  - Prohibits destructive ledger rewrites attempted by historical scripts.

### 2.3 `registry_contract.py`
- **Location:** `tools/skill_library/registry_contract.py`
- **Responsibilities:** Implements ADR-004 registry, router, alias, and dependency contracts. Houses `CatalogCompiler`, `CatalogRegistry`, `DependencyResolver`, `AliasResolver`, `MultiViewProjector`, and `FamilyRouterGenerator`.
- **Key Classes:** `CatalogCompiler`, `CatalogRegistry`, `RegistryEntry`, `AliasResolver`, `DependencyResolver`, `MultiViewProjector`.
- **Existing Capabilities:** Compiles catalog into multi-view projections (flat, hierarchical, family-centric); resolves cyclic dependencies; generates deterministic router markdown tables.
- **Limitations & Guardrails:** Rejects unregistered aliases and unrouted canonical leaves.
- **Crosswalk Mapping:**
  - Supersedes `build_phase_05_artifacts.py`, `build_phase_06_artifacts.py`, `build_phase_08_artifacts.py`, and `verify_phase_10.py`.
  - Prohibits legacy Phase 05/10 static category assumptions and hardcoded 2,103 leaf counts.

### 2.4 `config.py`
- **Location:** `tools/skill_library/config.py`
- **Responsibilities:** Central configuration for runtime distribution targets (e.g. Claude Desktop, Cursor, Windsurf, Roo Code).
- **Key Classes:** `RuntimeTarget`.
- **Existing Capabilities:** Loads target definitions, parses runtime distribution paths, enumerates known catalog routers.
- **Limitations & Guardrails:** Configuration loader only; execution delegated to `sync.py` and `publisher.py`.
- **Crosswalk Mapping:**
  - Replaces scattered hardcoded paths in historical phase scripts with structured target declarations.

### 2.5 `family_contract.py`
- **Location:** `tools/skill_library/family_contract.py`
- **Responsibilities:** Implements ADR-003 family eligibility and execution provider contracts.
- **Key Classes:** `FamilyTier`, `FamilyQualificationGate`, `FamilyQualificationRecord`, `ExecutionProviderBinding`, `ExecutionProviderContract`, `AuthoritativeCensus`.
- **Existing Capabilities:** Validates census-backed candidate records; classifies Tier 1 (Meta), Tier 2 (Super-Code), Tier 3 (Domain Hub); isolates execution provider bindings from canonical skill definitions.
- **Limitations & Guardrails:** Requires census alignment; rejects fabricated paths or unsupported deduplications.
- **Crosswalk Mapping:**
  - Formalizes and supersedes `classify_compatibility.py`, `analyze_provider_coupling_detailed.py`, and `analyze_provider_dependencies.py`.
  - Eliminates the need for historical in-place mutators (`neutralize_claude_dependencies.py`, `execute_provider_conversion.py`).

### 2.6 `physical_layout.py`
- **Location:** `tools/skill_library/physical_layout.py`
- **Responsibilities:** Implements ADR-002 physical ownership model, separating canonical skills, routers, nested resources, and runtime targets.
- **Key Classes:** `PhysicalPlane`, `PhysicalPathContract`, `ParsedPhysicalPath`, `PhysicalLayoutValidator`, `DuplicateCandidateRegistry`.
- **Existing Capabilities:** Validates path containment, detects rogue nested skill packages, identifies duplicate naming collisions.
- **Limitations & Guardrails:** Read-only validator; does not move files automatically.
- **Crosswalk Mapping:**
  - Supersedes `build_phase_07_artifacts.py` and `verify_phase_07.py`.

### 2.7 `migration_gates.py`
- **Location:** `tools/skill_library/migration_gates.py`
- **Responsibilities:** Implements ADR-005 architecture migration gates (G01–G08) and package manifest hashing.
- **Key Classes:** `GateID`, `GateResult`, `SkillPackageManifest`, `HistoricalProvenanceRecord`, `MigrationGateEvaluator`, `MigrationGateRunner`.
- **Existing Capabilities:** Computes deterministic package manifests; verifies integrity against historical provenance ledgers; evaluates gates G01 through G08.
- **Limitations & Guardrails:** Blocks migration if any gate G01–G08 fails; strictly read-only evaluation.
- **Crosswalk Mapping:**
  - Modern replacement for all legacy phase verifiers (`verify_phase_04.py` through `verify_phase_12.py`).
  - Incorporates the package manifest hashing logic from `generate_inventory.py`.

### 2.8 `manifest.py`
- **Location:** `tools/skill_library/manifest.py`
- **Responsibilities:** Generates and validates `audit/runtime-manifest.json` for runtime distribution.
- **Key Classes:** `RuntimeManifest`.
- **Existing Capabilities:** Hashes runtime packages, records commit SHAs and distribution targets, ensures runtime authenticity.
- **Limitations & Guardrails:** Requires valid git tree state.
- **Crosswalk Mapping:**
  - Replaces ad-hoc CSV evidence updaters (`update_csv_evidence.py`, `update_check16.py`).

### 2.9 `sync.py`
- **Location:** `tools/skill_library/sync.py`
- **Responsibilities:** Synchronizes runtime target checkouts using git sparse-checkout and migrates legacy symlinks.
- **Key Classes:** `TargetSyncReport`, `MultiTargetSyncReport`.
- **Existing Capabilities:** Safe non-destructive target updates, detects dirty states, validates target checkout integrity.
- **Limitations & Guardrails:** Refuses to overwrite dirty uncommitted files without explicit force flag.
- **Crosswalk Mapping:**
  - Operational distribution tooling replacing legacy manual symlink generation.

### 2.10 `intake.py`
- **Location:** `tools/skill_library/intake.py`
- **Responsibilities:** Evaluates external incoming skill candidates, computes Dice token similarity against existing catalog, and appends links to appropriate routers.
- **Key Classes:** `IntakeEvaluation`.
- **Existing Capabilities:** Frontmatter parsing, tokenization, duplicate candidate detection, router link generation.
- **Limitations & Guardrails:** Rejects duplicate leaves; prevents unclassified skills from entering root.
- **Crosswalk Mapping:**
  - Living library intake engine replacing manual phase rebuild merges.

### 2.11 `intake_capture.py`
- **Location:** `tools/skill_library/intake_capture.py`
- **Responsibilities:** Scans runtime targets for local modifications and captures them as candidate intake packages.
- **Key Functions:** `scan_target_dirty_state`, `capture_dirty_target`, `convert_incoming_to_intake`.
- **Existing Capabilities:** Captures external skill edits, preserves provenance, creates staged intake branches.
- **Limitations & Guardrails:** Requires git repository context; strictly sandboxed capture.
- **Crosswalk Mapping:**
  - Modern bidirectional runtime capture replacing historical manual script dumps.

### 2.12 `publisher.py`
- **Location:** `tools/skill_library/publisher.py`
- **Responsibilities:** Publishes verified runtime trees to the `runtime` git branch.
- **Key Functions:** `publish_runtime_branch`, `get_library_tree_sha`, `get_commit_tree_sha`.
- **Existing Capabilities:** Compares git tree hashes; creates clean commits on `runtime` branch without touching working tree files.
- **Limitations & Guardrails:** Requires all validation gates to pass before publishing.
- **Crosswalk Mapping:**
  - Automated release publisher replacing manual phase PR generation scripts (`pr_12_body.md`, `pr_78_body.md`).

### 2.13 `validator.py`
- **Location:** `tools/skill_library/validator.py`
- **Responsibilities:** Comprehensive validation of the living skill library.
- **Key Classes:** `SkillValidationReport`, `ValidationResult`.
- **Key Functions:** `validate_library_integrity`, `validate_single_skill`, `parse_frontmatter`.
- **Existing Capabilities:** Validates frontmatter schemas, checks router broken links, verifies package manifests and URN formats.
- **Limitations & Guardrails:** Strictly read-only validation.
- **Crosswalk Mapping:**
  - Direct successor to `gen_phase11_artifacts.py` and `verify_phase_11.py`.

### 2.14 `pilot.py`
- **Location:** `tools/skill_library/pilot.py`
- **Responsibilities:** Conducts targeted pilot evaluations of skills across diverse execution contexts.
- **Key Classes:** `PilotResult`.
- **Key Functions:** `run_targeted_pilot`.
- **Existing Capabilities:** Samples representative skills, verifies execution prerequisites, compiles pilot summary.
- **Limitations & Guardrails:** Safe dry-run execution harness.
- **Crosswalk Mapping:**
  - Modern replacement for `gen_phase12_artifacts.py` and `verify_phase_12.py`.

### 2.15 Auxiliary Components: `scanner.py` & `tools/skill-library.py`
- **`scanner.py`:** Discovers all `SKILL.md` packages on disk, extracts metadata, computes file hashes. Forms the underlying engine for zero-index discovery.
- **`tools/skill-library.py`:** Unified CLI integrating `intake`, `scan`, `validate`, `sync`, and `publish`. Direct entrypoint for all library automation.
