# Test Matrix & Execution Assessment

**Task:** SKIL-13 | ZI-04: Validate existing code and CI from pinned SHA  
**Pinned Git SHA:** `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Execution Timestamp:** 2026-11-04T05:08:00Z  
**Isolation Method:** Detached read-only worktree at `/tmp/skil13-pinned-worktree`  

---

## 1. Architectural Plane Test Mapping

The test suite at pinned SHA `195eda775d7a8dcad1837a1990bcba8259da3ea0` is organized into 9 test modules spanning four primary architectural planes:
1. **Semantic Plane:** Object model entities, role classification, and census validation.
2. **Composition & Governance Plane:** Catalog registry, multi-view projections, alias resolution, and physical layout contracts.
3. **Lifecycle & Gates Plane:** Migration gates 1–9, provenance mapping, and scenario simulations.
4. **Deployment & Execution Plane:** Runtime branch publication, sparse checkout synchronization, and target intake capture.

To establish complete and transparent baseline accounting, test execution was evaluated under two distinct execution profiles:
- **Isolated Suite Execution:** Each test module executed in an independent subprocess with isolated environment and working directory (`python3 -m unittest <module>`).
- **Full-Batch Execution:** All test modules executed sequentially in a single process via the repository CLI test runner (`python3 tools/skill-library.py test`).

### 1.1 Isolated Suite Execution Matrix (Primary Defect Baseline)

In isolated suite execution, ephemeral filesystem lock contention is eliminated, isolating the authentic defects strictly to two test cases in `test_runtime_publication.py`:

| Architectural Plane | Module | File Path | Tests | Pass | Fail | Error | Duration (s) | Exit Code | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Semantic Plane** | `test_semantic_object_model` | `tests/test_semantic_object_model.py` | 35 | 35 | 0 | 0 | 0.006 | 0 | **PASS** |
| **Semantic Plane** | `test_family_eligibility` | `tests/test_family_eligibility.py` | 40 | 40 | 0 | 0 | 0.102 | 0 | **PASS** |
| **Semantic Plane** | `test_semantic_census` | `tests/test_semantic_census.py` | 10 | 10 | 0 | 0 | 0.095 | 0 | **PASS** |
| **Composition & Governance** | `test_registry_router_contracts` | `tests/test_registry_router_contracts.py` | 39 | 39 | 0 | 0 | 0.009 | 0 | **PASS** |
| **Composition & Governance** | `test_physical_ownership` | `tests/test_physical_ownership.py` | 19 | 19 | 0 | 0 | 0.002 | 0 | **PASS** |
| **Composition & Governance** | `test_migration_roadmap` | `tests/test_migration_roadmap.py` | 14 | 14 | 0 | 0 | 0.036 | 0 | **PASS** (*1) |
| **Lifecycle & Gates** | `test_migration_gates` | `tests/test_migration_gates.py` | 56 | 56 | 0 | 0 | 6.824 | 0 | **PASS** |
| **Lifecycle & Gates** | `test_scenarios` | `tests/test_scenarios.py` | 15 | 15 | 0 | 0 | 0.567 | 0 | **PASS** |
| **Deployment & Execution** | `test_runtime_publication` | `tests/test_runtime_publication.py` | 25 | 23 | 2 | 0 | 159.804 | 1 | **FAIL** (*2) |
| **TOTAL (Isolated Execution)** | **9 Modules** | — | **253** | **251** | **2** | **0** | **167.445** | **1** | **FAIL** |

### 1.2 Full-Batch Execution Matrix (`tools/skill-library.py test`)

In single-process sequential batch execution, three temporary Git repository setup collisions occur during rapid repository initialization on macOS APFS:

| Architectural Plane | Module | File Path | Tests | Pass | Fail | Error | Duration (s) | Exit Code | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Semantic Plane** | `test_semantic_object_model` | `tests/test_semantic_object_model.py` | 35 | 35 | 0 | 0 | — | 0 | **PASS** |
| **Semantic Plane** | `test_family_eligibility` | `tests/test_family_eligibility.py` | 40 | 40 | 0 | 0 | — | 0 | **PASS** |
| **Semantic Plane** | `test_semantic_census` | `tests/test_semantic_census.py` | 10 | 10 | 0 | 0 | — | 0 | **PASS** |
| **Composition & Governance** | `test_registry_router_contracts` | `tests/test_registry_router_contracts.py` | 39 | 39 | 0 | 0 | — | 0 | **PASS** |
| **Composition & Governance** | `test_physical_ownership` | `tests/test_physical_ownership.py` | 19 | 19 | 0 | 0 | — | 0 | **PASS** |
| **Composition & Governance** | `test_migration_roadmap` | `tests/test_migration_roadmap.py` | 14 | 14 | 0 | 0 | — | 0 | **PASS** (*1) |
| **Lifecycle & Gates** | `test_migration_gates` | `tests/test_migration_gates.py` | 56 | 56 | 0 | 0 | — | 0 | **PASS** |
| **Lifecycle & Gates** | `test_scenarios` | `tests/test_scenarios.py` | 15 | 15 | 0 | 0 | — | 0 | **PASS** |
| **Deployment & Execution** | `test_runtime_publication` | `tests/test_runtime_publication.py` | 25 | 20 | 2 | 3 | — | 1 | **FAIL** (*3) |
| **TOTAL (Batch Execution)** | **9 Modules** | — | **253** | **248** | **2** | **3** | **166.700** | **1** | **FAIL** |

*Execution Notes:*
- (*1) `test_migration_roadmap.py` requires `PYTHONPATH=tools` (or invocation via `tools/skill-library.py test`) because it omits `sys.path.insert(0, tools)`. When run via unconfigured `python3 -m unittest discover`, it fails at module load with `ModuleNotFoundError: No module named 'skill_library'`.
- (*2) Authentic defects in `test_runtime_publication.py`:
  - `test_21_accept_external_intake_enforcement_and_dispatch_failure`: Line 813 fails with `AssertionError: True is not false` because `capture_dirty_target` executes unmocked `gh workflow run runtime-intake.yml`. In an authenticated workstation environment, the command dispatches, causing `workflow_triggered` to return `True`.
  - `test_24_skill_directory_rename_preserves_old_and_new_paths`: Line 1122 fails with `AssertionError: False is not true` because physical rename of folder `bug-hunter` -> `bug-tracker` leaves frontmatter name as `bug-hunter`, causing `validate_single_skill` to set `is_valid_package=False`.
- (*3) Batch execution errors: In single-process batch execution, tests `test_01`, `test_02`, and `test_03` of `TestRuntimeGitClonePublication` encounter `CalledProcessError: Command '['git', 'commit', '-m', 'Initial baseline']' returned non-zero exit status 128` during `setUp` due to high-frequency temporary repository creation on macOS APFS in `/var/folders/`. When run in isolation, all three setup steps pass cleanly.

---

## 2. Test Execution Details & Claims Matrix

### 2.1 `tests/test_semantic_object_model.py` (35 Tests - PASS)
- **Claims Verified:**
  - Strict typing of canonical entities: `SkillObject`, `CapabilityObject`, `WorkflowObject`, `PrimitiveObject`, `OverlayObject`, `AdapterObject`, `AliasObject`, `RouterObject`, `GeneratedArtifactObject`.
  - Invariants INV-1 (Acyclicity), INV-2 (Single Canonical Owner), INV-3 (Single-Hop Alias), INV-4 (Shallow Overlay), INV-5 (Leaf Primitive Purity), INV-6 (Path Independence).
  - Validation that primitive objects cannot declare dependencies or composite workflows.
  - Verification that circular dependencies trigger `InvariantViolationError`.

### 2.2 `tests/test_family_eligibility.py` (40 Tests - PASS)
- **Claims Verified:**
  - Census-backed qualification evidence: reconciliation of candidate hubs against authoritative `audit/taxonomy-census/semantic-role-census.json`.
  - Rejection of fabricated categories, non-census paths, duplicate reductions without approved registry, and omitted manual reviews.
  - Tier 1 Meta-Family qualification (Multi-provider hub: Cloudflare, Google Cloud, AWS).
  - Tier 2 Technology Family qualification (Deep multi-surface ecosystem: GitHub, Figma, Docker).
  - Disqualification of single-tool sprawl (`curl`, `jq`) and domain density traps.
  - Strict evaluation of `notebooklm` into `PENDING_ADJUDICATION`.

### 2.3 `tests/test_semantic_census.py` (10 Tests - PASS)
- **Claims Verified:**
  - Population integrity of `semantic-role-census.json` (exactly 2,133 objects).
  - Schema conformity (all required fields present: canonical_id, role, confidence, category, subcategory, tokens, description).
  - Validated role distribution matching REV-150 publication standards.
  - Token density differential: workflow average (2,135 tokens) vs capability average (1,348 tokens).

### 2.4 `tests/test_registry_router_contracts.py` (39 Tests - PASS)
- **Claims Verified:**
  - Universal Catalog Registry (`CatalogRegistry`) lookup by canonical ID and URN (`urn:skill:*`).
  - Single-hop alias resolution (`AliasResolver`); rejection of chained aliases or cyclic aliases.
  - Shallow overlay specialization (`MultiViewProjector`); prohibition of overlay stacking.
  - Multi-view projection modes (`FUNCTIONAL_TAXONOMY`, `EXECUTION_PROVIDER`, `SEMANTIC_ROLE`, `FAMILY_ECOSYSTEM`).
  - Project materialization ladder (`ProjectMaterializer`): name collisions resolved via flat candidate ladder.

### 2.5 `tests/test_physical_ownership.py` (19 Tests - PASS)
- **Claims Verified:**
  - Enforcement of REV-125 duplicate pair resolution registry (`audit/duplicate-adjudication/`).
  - Physical plane non-destructive freeze: legacy duplicates preserved without physical deletion during hold.
  - Dual-ownership prevention: exactly one canonical owner per capability.

### 2.6 `tests/test_migration_roadmap.py` (14 Tests - PASS with PYTHONPATH)
- **Claims Verified:**
  - Master roadmap (`docs/architecture/MIGRATION_ROADMAP.md`) exists and references ADR-001 through ADR-005.
  - Full coverage of 9 migration gates (`GateID.GATE_1` through `GateID.GATE_9`).
  - Coverage of invariants INV-1 through INV-10.
  - Preservation of all 16 legacy task specs in `library-rebuild-tasks/legacy-rebuild-phase-1-13/`.
  - Direction-neutral hold on 15 GitHub duplicate pairs in Phase 03.
  - Phase 04 manifest authenticity (SHA-256) and path containment rules.

### 2.7 `tests/test_migration_gates.py` (56 Tests - PASS)
- **Claims Verified:**
  - Deterministic evaluation of Gates 1 through 9.
  - Gate 1: Canonical identity uniqueness & RFC 8141 URN compliance.
  - Gate 2: Family qualification & boundary adherence.
  - Gate 3: Graph topology, acyclicity, and alias purity.
  - Gate 4: Zero data loss and asset preservation.
  - Gate 5: Reference closure and dependency completeness.
  - Gate 6: Router link integrity and badge validation.
  - Gate 7: Deterministic compilation & idempotency.
  - Gate 8: Project materialization completeness.
  - Gate 9: Runtime publication preflight.
  - Provenance mapper (`HistoricalProvenanceMapper`): reconciliation of historical Phases 01–12 audit CSVs.

### 2.8 `tests/test_scenarios.py` (15 Tests - PASS)
- **Claims Verified:**
  - Scenario-based integration pipelines.
  - Candidate intake flow: scan -> intake evaluation -> approval gate -> apply.
  - Rejection of overlapping candidates without human approval.
  - Targeted pilot workflow simulations (`run_targeted_pilot`).

### 2.9 `tests/test_runtime_publication.py` (25 Tests - 23 PASS, 2 FAIL in Isolation)
- **Passes (23 Tests):**
  - Requirement 1: publish-runtime root tree matches `main:library/` exactly.
  - Requirement 2: non-canonical paths (`docs/`, `tools/`, `intake/`, `config/`, `audit/`) absent from runtime.
  - Requirement 3: unchanged library makes publish-runtime a no-op.
  - Requirement 4: modified skill updates runtime commit and tree.
  - Requirement 5: target configuration loading and schema validation.
  - Requirement 6: full target synchronization produces physical Git clone.
  - Requirement 7: subset target synchronization configures sparse-checkout.
  - Requirement 8: clean target fast-forwards on runtime update.
  - Requirement 9: dirty target conflict prevents destructive reset during sync.
  - Requirement 10: local intake collector groups dirty runtime files into `incoming/*` snapshot.
  - Requirement 11: local intake collector does not clear dirty working state if push fails.
  - Requirement 12: GitHub intake workflow conversion produces reviewed `intake/*` branch from main.
  - Requirements 13–20: bare upstream remote end-to-end capture, branch lifecycle, conflict handling.
  - Requirement 22: duplicate leaf name intake collision resolution.
  - Requirement 23: whole skill deletion preserved as intake event.
  - Requirement 25: intake CLI `--strict` gate fails on invalid/rejected candidates.
- **Failures (2 Tests):**
  - **Requirement 21 (`test_21_accept_external_intake_enforcement_and_dispatch_failure`):** Fails because `gh workflow run` is invoked without mocking. On authenticated workstations, the workflow is actually dispatched to GitHub Actions (observed Run ID `41776764840`, concluded in failure within 12s on remote runner without mutating repo assets).
  - **Requirement 24 (`test_24_skill_directory_rename_preserves_old_and_new_paths`):** Fails because physical directory rename triggers directory/frontmatter mismatch in `validate_single_skill`, marking `is_valid_package=False`.

---

## 3. External Side Effect Boundary & Isolation Guard

During baseline execution of `test_runtime_publication.py:test_21`, the unmocked execution of `capture_dirty_target()` triggered a real remote workflow dispatch via the host's authenticated `gh` CLI:
- **Dispatched Workflow:** `Runtime Intake Pipeline` (`.github/workflows/runtime-intake.yml`)
- **Remote Run ID:** `41776764840`
- **Dispatch Timestamp:** `2026-11-04T05:02:17Z`
- **Remote Conclusion:** `failure` (duration: 12 seconds; failed at step `Convert Incoming Snapshot to Intake Branch` due to non-existent incoming branch)
- **Repository Mutation Audit:** Confirmed zero remote mutations. No pull requests were opened, no remote branches created or modified, and zero repository files altered.

**Mandatory Diagnostic Isolation Guard:**
Any future diagnostic execution of `test_runtime_publication.py` must either:
1. Provide a mocked `subprocess.run` interceptor for `gh`, OR
2. Execute in an unauthenticated subshell where `GH_TOKEN` and `GITHUB_TOKEN` are unset, and a non-dispatching dummy stub for `gh` is prepended to `PATH`.
Do not rerun `test_21` on an authenticated workstation without an isolation harness.
