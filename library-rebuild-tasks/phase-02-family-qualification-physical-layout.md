# Task Spec — Phase 02: Platform Family Qualification & Physical Ownership Layout

- **Status**: Authoritative (REV-132)
- **Work Order**: Phase 02 of Skills Library Implementation Roadmap
- **Enforced Gates**: **Gate 2: Family Qualification & Boundary Adherence** (INV-8)
- **Architecture Reference**: [ADR-002 (REV-128)](../docs/architecture/decisions/ADR-002-physical-ownership-model.md), [ADR-003 (REV-129)](../docs/architecture/decisions/ADR-003-family-eligibility-and-provider-adapters.md), [ADR-005 (REV-131)](../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)
- **Authoritative Census**: `audit/taxonomy-census/semantic-role-census.json`

---

## 1. Objective

Apply the census-backed 4-Gate Family Qualification Framework to establish Tier 1 physical platform hubs while strictly confining Tier 2 logical families and pending candidates to virtual domain routing. Decouple execution provider dependencies into pure protocol adapters (`adapts: provider:<name>`) and eliminate adapter cycles.

---

## 2. Preconditions

1. Phase 01 completed with Gate 1 reported `PASSED`.
2. Provenance reconciliation report exists (`audit/provenance-reconciliation-report.json`).
3. Authoritative semantic role census is available at `audit/taxonomy-census/semantic-role-census.json`.
4. Working tree under `library/**` and `audit/taxonomy-census/**` is clean.

---

## 3. Canonical Task Skills & Engine

- Implementation Module: `tools/skill_library/family_contract.py` (`FamilyCandidateEvaluator`, `FamilyQualificationRecord`)
- Physical Layout: `tools/skill_library/physical_layout.py` (`PhysicalLayoutValidator`, `DuplicateCandidateRegistry`)
- Migration Engine: `tools/skill_library/migration_gates.py` (Gate 2 Evaluator)
- Test Suite: `tests/test_family_eligibility.py`, `tests/test_physical_ownership.py`

---

## 4. Step-by-Step Work

1. **Execute 4-Gate Family Qualification Evaluation**:
   - For every platform family candidate, run `FamilyCandidateEvaluator.evaluate_from_ledger(family_slug, census=census_inst)` against the authoritative semantic role census.
   - Evaluate against the 4 mandatory qualification gates:
     - **Gate 1 (Tool Surface Cohesion)**: Verified official public surface (CLI, MCP, REST, SDK).
     - **Gate 2 (Shared Configuration)**: Shared auth credentials, tokens, or environment configuration.
     - **Gate 3 (Critical Mass)**: $\ge 3$ distinct capabilities across $\ge 2$ functional domains OR $\ge 5$ operations in 1 complex domain ($\ge 5$ for internal meta-families).
     - **Gate 4 (Lifecycle Coordination)**: Coordinated release lifecycle.
2. **Classify Family Tiers**:
   - **Tier 1 Platform Hubs**: Families satisfying all 4 gates (e.g. `github`, `webflow`, `figma`) are authorized to establish physical hubs under `library/tools-and-platforms/<family-slug>/`.
   - **Tier 2 Logical Domain Families**: Cross-cutting families that do not satisfy Tier 1 critical mass (e.g. `supabase`, `browser-automation`) are designated as Tier 2 logical families. They remain virtual routers physically stored within functional domain directories (`library/development/backend/`, `library/workflow-and-automation/`).
   - **Pending Adjudication Hold**: Candidates with pending review (e.g. `notebooklm`) are classified as `PENDING_ADJUDICATION` and strictly confined to domain virtual routing (`library/data-and-ai/`).
3. **Enforce Direction-Neutral Duplicate Hold**:
   - Verify that all 15 unresolved GitHub duplicate pairs in `DuplicateCandidateRegistry.CANDIDATE_HYPOTHESES` remain direction-neutral.
   - Gate 2 must fail closed (`UNADJUDICATED_DUPLICATE_ALIAS`) if any unadjudicated candidate pair is converted to an alias before formal review.
4. **Decouple Execution Providers into Protocol Adapters**:
   - Identify vendor tool couplings (Claude Code, OpenAI Codex, Gemini CLI).
   - Normalize packages to declare pure protocol adapters: `adapts: provider:<name>`.
   - Run Tarjan's cycle detection across all adapter edges to verify zero circular adapter relationships ($A \xrightarrow{\text{adapts}} B \xrightarrow{\text{adapts}} A$).
5. **Execute Gate 2 Preflight Validation**:
   - Run `MigrationGateEvaluator.evaluate_gate_2_family_qualification(registry, census_records)`.
   - Confirm zero unqualified families placed in physical platform hubs.
   - Confirm zero unadjudicated duplicate alias conversions.
   - Confirm zero adapter cycles.

---

## 5. Artifacts

Create or update:
- `audit/family-qualification-report.json`:
  Machine-readable qualification report recording gate scores, evidence status, evaluated tier, physical directory boundary assignment, and adapter dependencies for each candidate family.

---

## 6. Reconciliation Requirements

- 100% of physical directories under `library/tools-and-platforms/` must belong to approved Tier 1 qualified families.
- All Tier 2 families and pending candidates must reside exclusively within `library/<category>/<subcategory>/`.
- All 15 unresolved GitHub candidate pairs must remain direction-neutral.
- Adapter cycles must be exactly 0.
- Gate 2 must report `status: PASSED` with 0 violations.

---

## 7. Repository Checkpoint

1. Branch name: `feature/migration-phase-02-family-qualification`.
2. Commit message: `feat(migration): complete phase 02 platform family qualification and physical ownership layout`.
3. Pull Request must include:
   - Summary of qualified Tier 1 platform hubs vs Tier 2 logical domain families.
   - Census evaluation evidence for `github`, `webflow`, `figma`, `supabase`, and `notebooklm`.
   - Gate 2 validation output showing 0 violations.
4. Leave PR open for review; do not proceed to Phase 03 until approved.

---

## 8. Completion Gate

Complete only when:
- [ ] `FamilyCandidateEvaluator` confirms qualification for all platform families against census records.
- [ ] `audit/family-qualification-report.json` is generated and committed.
- [ ] No unqualified family creates a physical hub under `tools-and-platforms/`.
- [ ] All 15 GitHub duplicate pairs are verified as direction-neutral.
- [ ] `MigrationGateRunner.run_gate(GateID.GATE_2_FAMILY_QUALIFICATION)` returns `PASSED`.
- [ ] Automated regression tests pass: `PYTHONPATH=tools python3 -m unittest tests/test_family_eligibility.py tests/test_physical_ownership.py`.
