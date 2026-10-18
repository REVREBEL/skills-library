# Task Spec — Phase 04: Manifest Authenticity, Resource Preservation & Staged Physical Migration

- **Status**: Authoritative (REV-132)
- **Work Order**: Phase 04 of Skills Library Implementation Roadmap
- **Enforced Gates**: **Gate 4: Resource & Asset Preservation (Zero Data Loss)**
- **Architecture Reference**: [ADR-005 (REV-131)](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)
- **Security Invariant**: Canonical Path Containment & Cryptographic Manifest Authenticity

---

## 1. Objective

Execute physical package relocations under strict non-destructive preflight authorization. Verify 100% preservation of all executable scripts, references, templates, schemas, and markdown documentation through cryptographic SHA-256 manifest authenticity, authorized staging preflight, and strict canonical path containment.

---

## 2. Preconditions

1. Phases 01, 02, and 03 completed with Gates 1, 2, and 3 reporting `PASSED`.
2. Clean working tree on the dedicated migration branch.
3. Dedicated, authorized staging root configured (e.g. `.staging/moves-<batch>/`).
4. Staging directory must be isolated and included in `.gitignore`.
5. Living catalog files (`library/**`) are pristine.

---

## 3. Canonical Task Skills & Engine

- Implementation Module: `tools/skill_library/migration_gates.py` (`SkillPackageManifest`, `MigrationGateEvaluator`, `MigrationGateRunner`)
- Migration Engine Methods: `evaluate_gate_4_resource_preservation()`
- Test Suite: `tests/test_migration_gates.py`

---

## 4. Step-by-Step Work

1. **Formulate Migration Plan & Manifest Declarations**:
   - For every planned package move:
     - Identify source path (`source_dir`) and target destination (`dest_dir`).
     - Generate source manifest `SkillPackageManifest` with declared file inventory and SHA-256 checksums.
     - Generate planned destination manifest with expected file inventory and checksums.
2. **Stage Candidate Packages in Authorized Staging Root**:
   - Copy candidate packages into an isolated staging directory (`staged_dir`) under an approved `staging_root`.
   - Never move, delete, or modify live catalog files in `library/**` during preflight staging.
3. **Execute Three-Tier Manifest Evidence Verification (Gate 4 Preflight)**:
   - **Tier 1 (Manifest Presence & Alignment)**:
     - Verify source manifest and destination manifest are supplied for every planned move. Missing manifests fail closed with `MISSING_SOURCE_MANIFEST` or `MISSING_DESTINATION_MANIFEST`.
     - Confirm manifest `skill_id` matches planned move (`MANIFEST_IDENTITY_MISMATCH`) and canonical paths align (`MANIFEST_PATH_MISMATCH`).
   - **Tier 2 (Fresh On-Disk Generation & Cross-Examination)**:
     - Independently scan actual files on disk at source and staged destination.
     - Compute fresh recursive SHA-256 digests and file sizes.
     - Cross-examine on-disk inventory against supplied manifests:
       - Mismatched digest fails with `FABRICATED_MANIFEST_CHECKSUM`.
       - On-disk file omitted from manifest fails with `MANIFEST_OMITTED_FILE`.
       - Manifest file missing on disk fails with `MANIFEST_PHANTOM_FILE`.
   - **Tier 3 (Source-to-Destination Preservation)**:
     - Compare verified source inventory 1-to-1 against staged destination inventory:
       $$\text{SHA-256}(\text{Asset}_{\text{source}}) \equiv \text{SHA-256}(\text{Asset}_{\text{staged\_dest}})$$
     - Any missing asset fails with `MISSING_SUPPORTING_ASSET`.
     - Any modified content fails with `RESOURCE_CHECKSUM_MISMATCH`.
     - Any unexpected file in destination fails with `UNEXPECTED_DESTINATION_FILE`.
4. **Enforce Canonical Path Containment & Security Boundaries**:
   - All source, destination, and staging paths must resolve strictly within authorized boundaries.
   - Staging roots are trusted **only** when supplied through independently approved configuration (`staging_root` or `staging_directories`). Caller-supplied directories cannot self-authorize.
   - Any path traversal sequence (`..`), unauthorized absolute path, or symlink pointing outside allowed boundaries is rejected with `PATH_TRAVERSAL_DETECTED`.
5. **Verify Non-Destructive Preflight Clearance**:
   - Run `MigrationGateRunner.run_gate(GateID.GATE_4_RESOURCE_PRESERVATION)`.
   - Ensure status is `PASSED`.
6. **Execute Atomic Physical Relocation**:
   - Generate forward execution journal ($\mathcal{J}_{\text{forward}}$) and reverse rollback journal ($\mathcal{J}_{\text{rollback}}$).
   - Atomically move verified packages from staging into target live directories in `library/`.
   - Re-run disk checksum verification on the live destination.
   - If any step fails, execute $\mathcal{J}_{\text{rollback}}$ to restore exact prior state.

---

## 5. Artifacts

Create or update:
- `audit/migration-manifest.json`:
  Complete list of planned moves, source manifests, destination manifests, and staging paths.
- `audit/package-checksum-ledger.json`:
  Cryptographic SHA-256 ledger recording hashes of every file across all moved packages.
- `audit/migration-rollback-journal.json`:
  Reversible rollback journal for atomic recovery.

---

## 6. Reconciliation Requirements

- 100% of files in source packages must exist in destination packages with identical SHA-256 checksums.
- Zero truncated files (file size > 0 bytes).
- Zero path traversal or symlink boundary escapes.
- Gate 4 must report `status: PASSED` with 0 violations.

---

## 7. Repository Checkpoint

1. Branch name: `feature/migration-phase-04-physical-relocation`.
2. Commit message: `feat(migration): complete phase 04 verified physical relocation and resource preservation`.
3. Pull Request must include:
   - Summary of moved packages, source paths, and destination paths.
   - Cryptographic SHA-256 verification log proving zero asset loss.
   - Gate 4 validation output showing 0 violations.
4. Leave PR open for review; do not proceed to Phase 05 until approved.

---

## 8. Completion Gate

Complete only when:
- [ ] Complete source and destination manifests supplied for all planned moves.
- [ ] Fresh recursive SHA-256 generation matches supplied manifests 100%.
- [ ] Source and destination inventories match bit-for-bit.
- [ ] Staging preflight passes without mutating live files.
- [ ] Canonical path containment is verified for all paths.
- [ ] `MigrationGateRunner.run_gate(GateID.GATE_4_RESOURCE_PRESERVATION)` returns `PASSED`.
- [ ] Automated regression tests pass: `PYTHONPATH=tools python3 -m unittest tests/test_migration_gates.py`.
