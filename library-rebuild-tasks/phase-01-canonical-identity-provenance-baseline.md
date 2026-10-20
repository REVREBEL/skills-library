# Task Spec — Phase 01: Establish Canonical Identity Baseline & Reconcile Historical Provenance

- **Status**: Authoritative (REV-132)
- **Work Order**: Phase 01 of Skills Library Implementation Roadmap
- **Enforced Gates**: **Gate 1: Canonical Identity Uniqueness & Structure** (INV-2, INV-6), **Gate 7: Deterministic Baseline Compilation** (INV-10)
- **Architecture Reference**: [ADR-001 (REV-127)](../docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md), [ADR-005 (REV-131)](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)
- **Historical Evidence Protected**: `audit/rebuild-phase-1-12/` (CSVs, batch plans, split allocations)

---

## 1. Objective

Establish immutable, path-independent canonical identities conforming to RFC 8141 URN principles (`urn:skill:<scope>:<slug>`) for every living skill package, and reconcile 100% of historical Phase 01–12 rebuild records to modern canonical identities before any physical moves take place.

Historical origin paths remain immutable audit evidence. Provenance reconciliation preserves complete traceability back to Phase 01–12 batch migrations without rewriting history.

---

## 2. Preconditions

1. Working tree is clean on the migration integration branch.
2. Historical audit evidence files are present and unmutated:
   - `audit/rebuild-phase-1-12/phase08-canonical-registry.csv` (2,103 historical records)
   - `audit/rebuild-phase-1-12/phase08-batch-plan.csv` (162 batch migration allocations)
   - `audit/rebuild-phase-1-12/split-allocations.csv` (Phase 07 split allocations)
3. Living semantic role census is verified:
   - `audit/taxonomy-census/semantic-role-census.json` (2,133 classified skills)
4. Protected directories (`library/**`, `audit/taxonomy-census/**`) are clean and unmodified.

---

## 3. Canonical Task Skills & Engine

- Implementation Module: `tools/skill_library/migration_gates.py` (`ProvenanceReconciliationEngine`, `MigrationGateEvaluator`)
- Object Model: `tools/skill_library/object_model.py` (`CanonicalIdentity`, `SkillPackage`)
- Test Suite: `tests/test_migration_gates.py`, `tests/test_semantic_object_model.py`

---

## 4. Step-by-Step Work

1. **Scan Catalog & Generate Canonical Identifiers**:
   - Enumerate all active skill packages under `library/**`.
   - Parse each package's `SKILL.md` frontmatter.
   - Assign canonical ID `<scope>:<slug>` strictly matching regex `^[a-z0-9-]+:[a-z0-9-]+$`.
   - Reject any ID containing filesystem path separators (`/`, `\`), file extensions (`.md`, `.py`), or uppercase characters.
2. **Load & Reconcile Historical Phase 08 CSV Records**:
   - Ingest all 2,103 rows from `audit/rebuild-phase-1-12/phase08-canonical-registry.csv`.
   - Normalize historical paths (`task-folder/agents/skills-rebuild/<category>/<subcategory>/<name>`) to modern paths (`library/<category>/<subcategory>/<name>`).
   - Match 2,102 records directly to living packages on disk.
   - Reconcile documented historical renaming outlier: `design-md_v1` $\to$ `design-md`.
3. **Reconcile Platform Census Additions**:
   - Ingest the 30 platform family additions evaluated in REV-126/150 (15 `github-operations` and 15 `skills-create-manage-update` platform family candidates).
   - Track each addition as a typed `HistoricalProvenanceRecord` with `provenance_type: PLATFORM_CENSUS_ADDITION`.
4. **Compile Provenance Reconciliation Report**:
   - Run `ProvenanceReconciliationEngine.reconcile_all()`.
   - Verify that `reconciled_count == total_living_skills == 2,133`.
   - Verify that `unreconciled_count == 0` and `orphan_historical_count == 0`.
   - Output `audit/provenance-reconciliation-report.json`.
5. **Execute Gate 1 Validation**:
   - Run `MigrationGateEvaluator.evaluate_gate_1_canonical_identity(registry)`.
   - Verify zero duplicate canonical IDs across the entire catalog.
   - Verify RFC 8141 URN compliance: `urn:skill:<scope>:<slug>`.
6. **Non-Destructive Guarantee**:
   - Confirm zero files under `library/**` were created, moved, renamed, or modified.

---

## 5. Artifacts

Create or update:
- `audit/provenance-reconciliation-report.json`:
  Complete machine-readable record mapping every historical ID, historical path, batch ID, phase, and canonical URN to living packages.

---

## 6. Reconciliation Requirements

- Reconcile 2,103 historical Phase 08 registry entries to canonical IDs.
- Reconcile 30 platform census candidates to canonical IDs.
- Reconcile exactly 2,133 living skill packages with zero unmapped assets.
- Gate 1 must report `status: PASSED` with 0 violations.
- Working tree under `library/**` and `audit/taxonomy-census/**` must remain completely clean (`git diff --stat` is empty).

---

## 7. Repository Checkpoint

1. Branch name: `feature/migration-phase-01-provenance-baseline`.
2. Commit message: `feat(migration): complete phase 01 canonical identity baseline and provenance reconciliation`.
3. Pull Request must include:
   - Summary of reconciled historical records vs living census packages.
   - Gate 1 evaluation output showing 0 violations across 2,133 packages.
   - Diff confirmation showing only audit report artifacts created, zero live catalog file mutations.
4. Leave PR open for review; do not proceed to Phase 02 until approved.

---

## 8. Completion Gate

Complete only when:
- [ ] All 2,133 living packages have valid RFC 8141 canonical IDs.
- [ ] `ProvenanceReconciliationReport.is_fully_reconciled` is `True`.
- [ ] `audit/provenance-reconciliation-report.json` is generated and committed.
- [ ] `MigrationGateRunner.run_gate(GateID.GATE_1_CANONICAL_IDENTITY)` returns `PASSED`.
- [ ] Automated regression tests pass: `PYTHONPATH=tools python3 -m unittest tests/test_migration_gates.py`.
