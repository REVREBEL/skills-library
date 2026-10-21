# Task Spec — Phase 06: Deterministic Compilation, Project Materialization & Publication Pre-Flight

- **Status**: Authoritative (REV-132)
- **Work Order**: Phase 06 of Skills Library Implementation Roadmap
- **Enforced Gates**:
  - **Gate 7: Deterministic Compilation Idempotency** (INV-10)
  - **Gate 8: Project Materialization Completeness & Collision-Free Naming** (INV-9)
  - **Gate 9: Runtime Publication Pre-Flight & Target Compatibility**
- **Architecture Reference**: [ADR-004 (REV-130)](../docs/architecture/decisions/ADR-004-registry-router-alias-dependency-contracts.md), [ADR-005 (REV-131)](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)

---

## 1. Objective

Validate bit-for-bit idempotent catalog compilation, verify that standalone project materialization is self-contained and collision-free under the 6-stage runtime naming ladder, and perform a strictly non-destructive publication preflight to global agent discovery (`~/.agents/skills/`) with clean protected assets and an atomic rollback manifest.

---

## 2. Preconditions

1. Phases 01 through 05 completed with Gates 1 through 6 reporting `PASSED`.
2. Catalog registry and router markdown documents are compiled and stable.
3. Working tree under protected paths (`library/**`, `audit/taxonomy-census/**`) is completely clean.
4. Global discovery endpoint `~/.agents/skills/` is accessible for preflight verification.

---

## 3. Canonical Task Skills & Engine

- Implementation Module: `tools/skill_library/registry_contract.py` (`CatalogCompiler`, `ProjectMaterializer`)
- Migration Engine: `tools/skill_library/migration_gates.py` (Gate 7, Gate 8, Gate 9 Evaluators & `MigrationGateRunner`)
- Test Suite: `tests/test_migration_gates.py`, `tests/test_registry_router_contracts.py`, `tests/test_runtime_publication.py`

---

## 4. Step-by-Step Work

1. **Verify Deterministic Compilation Idempotency (Gate 7 Preflight)**:
   - Run two independent compiler executions over the source catalog.
   - Inject a pinned build timestamp or exclude volatile system clocks.
   - Compute cryptographic SHA-256 digests of compiled outputs:
     $$\text{SHA-256}(\text{Registry}_1) \equiv \text{SHA-256}(\text{Registry}_2)$$
     $$\text{SHA-256}(\text{SearchIndex}_1) \equiv \text{SHA-256}(\text{SearchIndex}_2)$$
   - Verify deterministic sorting of all keys, sets, and lists in compiled artifacts.
   - Run `MigrationGateEvaluator.evaluate_gate_7_deterministic_compilation(registry)`. Status must be `PASSED`.
2. **Validate Project Materialization & Collision-Free Naming (Gate 8 Preflight)**:
   - Simulate standalone project bundle materialization ($\mathcal{B}(S)$) for sample skill selections:
     - Verify transitive dependency closure completeness: $\forall s \in \mathcal{B}(S), \text{Dependencies}(s) \subseteq \mathcal{B}(S)$.
     - Reject bundles with missing transitive prerequisites (`MISSING_TRANSITIVE_DEPENDENCY`).
   - Test flattening hierarchical packages into flat runtime directories:
     - Apply the **6-stage collision-free naming ladder** implemented in `ProjectMaterializer._generate_flat_runtime_names()` (ADR-004 Section 9.2):
       - Stage 1: Natural leaf name (`<name>`, only if strictly unique across all entries in the bundle)
       - Stage 2: Category prefix (`<category>-<name>`)
       - Stage 3: Canonical scope prefix (`<scope>-<name>`)
       - Stage 4: Scope + category prefix (`<scope>-<category>-<name>`, if category exists and differs from scope)
       - Stage 5: Full canonical ID slug (`<canonical_id>.replace(":", "-")`)
       - Stage 6: Disambiguated canonical ID slug (`<cid_slug>-bundle-unique`)
     - Prove $|Names| = |Skills|$ with zero collisions across the entire active catalog (`RUNTIME_NAME_COLLISION`).
   - Run `MigrationGateEvaluator.evaluate_gate_8_project_materialization(registry)`. Status must be `PASSED`.
3. **Execute Runtime Publication Pre-Flight Simulation (Gate 9 Preflight)**:
   - Perform a dry-run simulation of publishing symbolic links and package manifests without mutating live destinations.
   - Verify that protected files in target environments (e.g., in `~/.agents/skills/`: `SKILL.md`, `github-operations`, `skills-create-manage-update`) are never overwritten or removed.
   - Confirm that working tree under protected paths (`library/**`, `audit/taxonomy-census/**`) is completely clean and unmutated (`PROTECTED_ASSETS_DIRTY`).
   - Generate forward execution journal ($\mathcal{J}_{\text{forward}}$) and reverse rollback journal ($\mathcal{J}_{\text{rollback}}$).
   - Run `MigrationGateEvaluator.evaluate_gate_9_publication_preflight(registry, repo_root)`. Status must be `PASSED`.
4. **Execute Full 9-Gate Catalog Evaluation**:
   - Run `MigrationGateRunner.run_all_gates()`.
   - Verify that all 9 gates return `PASSED` and `report.all_passed == True`.
   - Output `audit/migration-gate-report.json`.
5. **Post-Gate Live Cutover & Verification**:
   - Require explicit migration authorization (batch cutover approval) before initiating any live catalog modifications.
   - Execute atomic live cutover from authorized staging (`.staging/`) into live destinations in `library/**`.
   - Immediately re-run `MigrationGateRunner.run_all_gates()` against the live catalog; all 9 gates must pass.
   - Retain rollback capability ($\mathcal{J}_{\text{rollback}}$) to instantly restore pristine state if post-cutover verification detects any discrepancy.
6. **Decoupled Runtime Distribution (Optional Post-Validation Operation)**:
   - Define runtime distribution as a separate, optional, post-validation operation executed only after post-cutover live catalog certification.
   - Require independent publication authorization before distributing packages to destination environments.
   - Support three target destination types via the upcoming deterministic package builder and runtime adapters:
     - **Minimal Everyday Installation**: Curated global skills installed to `~/.agents/skills/`.
     - **Project-Specific Git-Synced Installation**: Workspace-isolated projection (e.g. `.agents/skills/`) with complete transitive closure (`INV-9`).
     - **External Upload Artifact**: Standalone archive (zip/tar.gz) or containerized bundle for external runtimes.

---

## 5. Artifacts

Create or update:
- Authoritative Catalog Registry: `audit/skills-registry.json`
- Inverted Token Search Index: `audit/search-index.json`
- Project Materialization Audit: `audit/materialization-audit.json`
- Publication Dry-Run & Rollback Manifest: `audit/publication-dry-run-report.json`
- Full 9-Gate Final Report: `audit/migration-gate-report.json`

---

## 6. Reconciliation Requirements

- Two consecutive compilations must produce identical SHA-256 hashes for all output artifacts.
- Zero runtime naming collisions across 100% of materialized catalog entries.
- 100% transitive dependency closure for all materialized bundles.
- Zero dirty files in `library/**` or `audit/taxonomy-census/**` during preflight.
- Full 9-gate report must show `passed_gates: 9`, `failed_gates: 0`, `all_passed: true`.

---

## 7. Repository Checkpoint

1. Branch name: `feature/migration-phase-06-compilation-and-preflight`.
2. Commit message: `feat(migration): complete phase 06 deterministic compilation, materialization and publication preflight`.
3. Pull Request must include:
   - Compilation idempotency proof with identical SHA-256 checksums.
   - Materialization test results showing zero collisions and complete closure.
   - Publication preflight dry-run log and rollback manifest.
   - Full 9-gate evaluation report certifying catalog readiness.
4. Approval boundary:
   - Migration authorization authorizes physical live catalog cutover into `library/**`.
   - Publication authorization is a separate, optional post-validation approval authorizing distribution across destination runtimes via the deterministic package builder and runtime adapters.

---

## 8. Completion Gate

Complete only when:
- [ ] Bit-for-bit compilation idempotency proven across consecutive runs.
- [ ] Collision-free naming ladder resolves 100% of catalog entries.
- [ ] Transitive dependency closure verified for project materialization.
- [ ] Publication preflight simulation completes with clean protected assets.
- [ ] Forward and rollback journals are generated.
- [ ] `MigrationGateRunner.run_all_gates().all_passed` is `True`.
- [ ] Automated test suite passes: `PYTHONPATH=tools python3 -m unittest discover -s tests`.
