# Skills Library Migration & Rebuild Tasks

- **Status**: Authoritative (REV-132)
- **Architecture Contract**: [ADR-001](../docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md) through [ADR-005](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)
- **Master Roadmap**: [docs/architecture/MIGRATION_ROADMAP.md](../docs/architecture/MIGRATION_ROADMAP.md)
- **Historical Archive**: [legacy-rebuild-phase-1-13/](legacy-rebuild-phase-1-13/README.md)

---

## Overview

This directory contains the authoritative, gate-governed task specifications for executing the skills library migration. It replaces the legacy unstructured restructuring tasks (Phases 01–13) and the suspended duplicate-cleanup plan ([REV-125](https://linear.app/revrebel/issue/REV-125/hold-bulk-duplicate-reconciliation-until-taxonomy-architecture-is-approved)).

All phases are strictly derived from the approved architecture:
- **ADR-001**: Path-Independent Canonical Identity (RFC 8141 URNs: `urn:skill:<scope>:<slug>`)
- **ADR-002**: Physical Ownership Model (Tier 1 Platform Hubs vs. Domain Trees)
- **ADR-003**: Platform Family Eligibility & Pure Protocol Adapters
- **ADR-004**: Registry Compilation, Deterministic Multi-View Routers, Single-Hop Aliases & DAG Invariants
- **ADR-005**: 9 Formal Architecture Validation and Migration Gates

---

## The 6 Gated Migration Phases

Every phase corresponds 1-to-1 with specific validation gates in `tools/skill_library/migration_gates.py` and must pass its prerequisite gates before any physical execution is authorized:

| Phase | Specification | Enforced Gates | Primary Deliverables |
| :--- | :--- | :--- | :--- |
| **01** | [phase-01-canonical-identity-provenance-baseline.md](phase-01-canonical-identity-provenance-baseline.md) | Gate 1, Gate 7 | Canonical IDs, 100% Phase 01–12 historical CSV reconciliation, zero live moves. |
| **02** | [phase-02-family-qualification-physical-layout.md](phase-02-family-qualification-physical-layout.md) | Gate 2 | Census-backed 4-gate family qualification, Tier 1 hubs vs Tier 2 virtual domains, adapter cycle check. |
| **03** | [phase-03-duplicate-adjudication-alias-contracts.md](phase-03-duplicate-adjudication-alias-contracts.md) | Gate 3 | Adjudicated duplicates, single-hop aliases, direction-neutral hold on 15 GitHub pairs, DAG acyclicity. |
| **04** | [phase-04-manifest-authenticity-staged-migration.md](phase-04-manifest-authenticity-staged-migration.md) | Gate 4 | Three-tier SHA-256 manifest verification, authorized staging preflight, path containment, atomic moves. |
| **05** | [phase-05-multi-view-routers-reference-closure.md](phase-05-multi-view-routers-reference-closure.md) | Gate 5, Gate 6 | 3-view router generation, relative link purity, provider badges, search index, 100% reference closure. |
| **06** | [phase-06-compilation-materialization-publication-preflight.md](phase-06-compilation-materialization-publication-preflight.md) | Gate 7, Gate 8, Gate 9 | Idempotent registry compilation, collision-free naming ladder, dry-run publication preflight. |

---

## Directory Structure

```text
library-rebuild-tasks/
├── README.md                                                        # This navigation hub
├── phase-01-canonical-identity-provenance-baseline.md               # Phase 01 Task Spec
├── phase-02-family-qualification-physical-layout.md                 # Phase 02 Task Spec
├── phase-03-duplicate-adjudication-alias-contracts.md               # Phase 03 Task Spec
├── phase-04-manifest-authenticity-staged-migration.md               # Phase 04 Task Spec
├── phase-05-multi-view-routers-reference-closure.md                 # Phase 05 Task Spec
├── phase-06-compilation-materialization-publication-preflight.md    # Phase 06 Task Spec
├── artifacts/                                                       # Historical scripts & analysis
└── legacy-rebuild-phase-1-13/                                       # Archived legacy task specs (01–13)
```

---

## Execution Guidelines for Engineers & Autonomous Agents

1. **Strictly Non-Destructive Preflight**:
   - Never move, delete, or rewrite live catalog files (`library/**`) without running the relevant migration gate preflight.
   - For physical relocations in Phase 04, use authorized staging directories (`.staging/`) and supply cryptographically verified `SkillPackageManifest` objects.
2. **Preserve Historical Provenance**:
   - Historical CSV files in `audit/rebuild-phase-1-12/` are immutable audit evidence. Do not edit, delete, or rewrite historical origin paths.
3. **Respect Direction-Neutral Holds**:
   - The 15 unresolved GitHub duplicate pairs in `DuplicateCandidateRegistry.CANDIDATE_HYPOTHESES` must not be aliased, deleted, or merged without explicit, documented architectural adjudication.
4. **Automated Verification**:
   - Run the contract validation suite after each phase:
     ```bash
     PYTHONPATH=tools python3 -m unittest \
       tests/test_migration_gates.py \
       tests/test_registry_router_contracts.py \
       tests/test_family_eligibility.py \
       tests/test_physical_ownership.py \
       tests/test_semantic_object_model.py \
       tests/test_semantic_census.py
     ```
