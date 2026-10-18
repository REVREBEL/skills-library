# Task Spec — Phase 03: Adjudicated Duplicate Reconciliation & Single-Hop Alias Contracts

- **Status**: Authoritative (REV-132)
- **Work Order**: Phase 03 of Skills Library Implementation Roadmap
- **Enforced Gates**: **Gate 3: Graph Topology, Acyclicity & Alias Purity** (INV-1, INV-3, INV-4, INV-5)
- **Supersedes**: Held 470-group / 488-loser duplicate deletion plan ([REV-125](https://linear.app/revrebel/issue/REV-125/hold-bulk-duplicate-reconciliation-until-taxonomy-architecture-is-approved))
- **Architecture Reference**: [ADR-002 (REV-128)](../docs/architecture/decisions/ADR-002-physical-ownership-model.md), [ADR-004 (REV-130)](../docs/architecture/decisions/ADR-004-registry-router-alias-dependency-contracts.md), [ADR-005 (REV-131)](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)

---

## 1. Objective

Replace the suspended, mechanical duplicate deletion plan from REV-125 with semantic, gate-governed duplicate adjudication. Resolve verified duplicate clusters into single canonical owners backed by non-destructive, single-hop alias pointers (`points_to`, `alias_type`), while holding the 15 unresolved GitHub candidate pairs strictly direction-neutral until formal review. Enforce strict DAG acyclicity and structural bounds across all catalog relationships.

---

## 2. Preconditions

1. Phase 01 and Phase 02 completed with Gate 1 and Gate 2 reporting `PASSED`.
2. Provenance reconciliation report (`audit/provenance-reconciliation-report.json`) and family qualification report (`audit/family-qualification-report.json`) are committed.
3. Candidate duplicate pairs ledger is loaded from `DuplicateCandidateRegistry.CANDIDATE_HYPOTHESES`.
4. Working tree under `library/**` and `audit/taxonomy-census/**` is clean.

---

## 3. Canonical Task Skills & Engine

- Implementation Module: `tools/skill_library/registry_contract.py` (`AliasResolver`, `DependencyResolver`, `DuplicateAdjudicationOutcome`)
- Object Model: `tools/skill_library/object_model.py` (`ObjectGraph`, `SkillRole`)
- Migration Engine: `tools/skill_library/migration_gates.py` (Gate 3 Evaluator)
- Test Suite: `tests/test_registry_router_contracts.py`, `tests/test_migration_gates.py`

---

## 4. Step-by-Step Work

1. **Enforce Direction-Neutral Protection for GitHub Candidate Pairs**:
   - Verify that all 15 unresolved GitHub candidate pairs in `DuplicateCandidateRegistry.CANDIDATE_HYPOTHESES` remain direction-neutral.
   - Forbid automated or heuristic alias assignment to these pairs without documented human architectural adjudication.
2. **Review & Adjudicate Candidate Duplicate Clusters**:
   - For candidate duplicate clusters undergoing adjudication:
     - Compare functional triggers, parameter schemas, bundled scripts, and instructions.
     - Reject mechanical path-depth winner rules.
     - Choose the canonical winner based on semantic completeness and platform family alignment.
   - For retired or superseded candidates, do **not** delete directories; construct a typed alias pointer:
     - `points_to: <canonical-id>`
     - `alias_type: TOMBSTONE | DEPRECATED | SHORTCUT`
     - `adjudication_rationale: "..."`
3. **Enforce Single-Hop Alias Purity (INV-3)**:
   - For every alias $a$, resolve target $t = \text{AliasResolver.resolve}(a)$.
   - Verify $t$ is an active canonical capability or workflow.
   - Reject any chained aliases ($a_1 \to a_2 \to t$) with `ALIAS_CHAIN_DETECTED`.
   - Reject self-referencing aliases ($a \to a$) with `ALIAS_SELF_LOOP`.
4. **Validate Graph Acyclicity across All Relationship Edges (INV-1)**:
   - Construct composite directed graph $G = (V, E)$ combining:
     - `depends_on` (prerequisite dependency)
     - `composed_of` (workflow step composition)
     - `extends` (overlay specialization)
     - `adapts` (provider protocol adaptation)
   - Execute Tarjan's strongly connected components algorithm.
   - Halt with `CYCLIC_DEPENDENCY_DETECTED` if any cycle $v \to \dots \to v$ is discovered.
5. **Enforce Shallow Overlays & Leaf Primitive Purity (INV-4, INV-5)**:
   - Verify that overlay objects only specialize base capabilities or workflows ($\text{depth} \le 1$). Overlays extending overlays are rejected with `OVERLAY_CHAIN_DETECTED`.
   - Verify that primitive objects declare empty composition (`composed_of: []`). Composite primitives are rejected with `COMPOSITE_PRIMITIVE`.
6. **Execute Gate 3 Preflight Validation**:
   - Run `MigrationGateEvaluator.evaluate_gate_3_graph_topology(registry)`.
   - Confirm zero graph cycles, zero alias chains, zero unadjudicated aliases, and zero structural invariant violations.

---

## 5. Artifacts

Create or update:
- `audit/duplicate-adjudication-journal.json`:
  Complete log of adjudicated duplicate clusters, canonical winners, retired loser paths, single-hop alias targets, and human review sign-offs.
- `audit/alias-registry.json`:
  Authoritative machine-readable registry of all active single-hop aliases, types, and target canonical IDs.

---

## 6. Reconciliation Requirements

- Reconcile 100% of reviewed duplicate candidates to either distinct packages or single-hop aliases.
- Direction-neutral hold on all 15 GitHub duplicate pairs must be verified.
- Graph cycles must be exactly 0.
- Chained aliases ($a_1 \to a_2$) must be exactly 0.
- Gate 3 must report `status: PASSED` with 0 violations.

---

## 7. Repository Checkpoint

1. Branch name: `feature/migration-phase-03-duplicate-adjudication`.
2. Commit message: `feat(migration): complete phase 03 adjudicated duplicate reconciliation and alias contracts`.
3. Pull Request must include:
   - Summary of adjudicated duplicate clusters and canonical owners.
   - Verification that 15 GitHub duplicate pairs remain direction-neutral.
   - Gate 3 validation report confirming acyclic DAG and single-hop alias purity.
4. Leave PR open for review; do not proceed to Phase 04 until approved.

---

## 8. Completion Gate

Complete only when:
- [ ] No unadjudicated duplicate pair is converted to an alias.
- [ ] Every active alias resolves in exactly one hop to a canonical target.
- [ ] `audit/duplicate-adjudication-journal.json` and `audit/alias-registry.json` are committed.
- [ ] Relationship graph is proven strictly acyclic.
- [ ] `MigrationGateRunner.run_gate(GateID.GATE_3_GRAPH_TOPOLOGY)` returns `PASSED`.
- [ ] Automated regression tests pass: `PYTHONPATH=tools python3 -m unittest tests/test_registry_router_contracts.py tests/test_migration_gates.py`.
