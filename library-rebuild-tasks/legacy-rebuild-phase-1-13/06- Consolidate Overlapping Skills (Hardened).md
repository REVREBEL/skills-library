# Implementation Plan — Phase 06: Consolidate Overlapping Skills (Hardened)

Phase 06 systematically resolves retained skills that share substantially the same user triggers, execution workflows, or functional outputs. Following the principle of **provenance-preserving consolidation**, this phase normalizes candidate overlap pools into tightly bounded functional clusters, selects canonical skill owners using multi-factor quality/risk criteria, consolidates unique valid material, relocates superseded sources to `task-folder/agents/not-needed/`, and establishes an exhaustive, fully reconciled audit ledger.

---

## User Review & Architecture Principles

> [!IMPORTANT]
> **Core Consolidation Principles**:
> 1. **Bounded Functional Clustering (Not Broad Candidate Pools)**: Candidate pools (such as the 231 CRO and 69 Design-System candidates from Phase 05, alongside 178 folder name collisions) are not monolithic clusters. They are decomposed into distinct, tightly bounded functional clusters based strictly on **same trigger + same workflow + same output**.
> 2. **Deduplicated Candidate Universe (`merge-members.csv`)**: All candidate signals (folder name collisions, Phase 05 merge candidates, semantic overlaps) are unified and deduplicated into a normalized candidate member ledger before clustering.
> 3. **Canonical Owner Selection Criteria**: Canonical owners are selected based on technical accuracy, trigger precision, workflow completeness, **risk/authorization gate quality**, and **validation/completion evidence quality**—not merely file size or word count.
> 4. **Zero Undocumented Loss of Unique Valid Material**: High-value instructions, code examples, or assets from superseded skills are integrated into the canonical owner or preserved in `references/`. Every non-preserved item must have an explicit disposition reason (`preserved`, `superseded by canonical instruction`, `obsolete`, `invalid`, `unsafe`, `duplicate`, `moved to reference`).
> 5. **Reversible Quarantine / Retirement (`task-folder/agents/not-needed/`)**: Superseded source skills are never deleted. They are relocated via `git mv` to `task-folder/agents/not-needed/`, preserving full Git history.
> 6. **Strict Alias Constraints**: Any temporary compatibility alias must be a thin redirect router only (no duplicate execution workflows, single target, no alias chaining, recorded milestone removal).
> 7. **Phase 05 Provenance Preservation**: The destination map preserves Phase 05 proposed paths alongside Phase 06 consolidation decisions.
> 8. **Strict Phase Boundary**: Phase 06 handles consolidation and duplicate retirement only. Functional splitting is deferred to Phase 07, and broad canonical rewriting/normalization is deferred to Phase 08.

---

## 1. Candidate Universe Normalization & Clustering

### A. Candidate Ingestion & Deduplication
We aggregate all overlap signals into a single deduplicated universe of candidate source paths:
- **Direct folder/slug name collisions**: 178 collision groups spanning 388 source paths.
- **Phase 05 candidate pools**: 231 CRO skills and 69 Design System skills.
- **Semantic / subcategory overlap signals**: identified across the remaining 1,598 retained skills.

### B. Bounded Sub-Clustering Strategy
Candidate pools are partitioned into concrete, fine-grained functional clusters. For example:
- **CRO Candidate Pool (231 skills)** partitioned into bounded clusters:
  - `cro-checkout-optimization`: Checkout flow, step reduction, friction removal.
  - `cro-cart-abandonment`: Exit modals, cart recovery prompts, session triggers.
  - `cro-pricing-psychology`: Tier framing, anchoring, discount psychology.
  - `cro-social-proof-testimonials`: Review widgets, trust badges, customer proof.
  - `cro-urgency-scarcity`: Countdown timers, low-stock notifications, deadline framing.
  - `cro-form-optimization`: Lead forms, inline validation, field reduction.
  - `cro-landing-page-hero`: Headline testing, above-the-fold value proposition.
  - `cro-cta-button-optimization`: Microcopy, CTA placement, action triggers.
  - `cro-ab-testing-experimentation`: Hypothesis framing, sample size calculations, variant evaluation.
- **Design Systems Pool (69 skills)** partitioned into bounded clusters:
  - `ds-tailwind-presets`: Tailwind configuration, theme extensions, utility tokens.
  - `ds-figma-tokens`: Figma variable sync, design-to-code token pipelines.
  - `ds-shadcn-component-patterns`: Accessible primitive integrations, Radix-based UI recipes.
  - `ds-component-auditing`: Accessibility audits, token consistency checks, design debt review.
  - `ds-iconography-typography`: Font scaling systems, SVG sprite automation.

---

## 2. Decision Taxonomy & Ledger Specifications

For every cluster, `merge-decisions.csv` records one primary decision:

| Decision | Definition | Resulting Action |
|---|---|---|
| **`Keep separately`** | Skills have distinct triggers, prerequisites, or tool sets despite topic similarity. | Retained as distinct canonical child skills. |
| **`Merge into one canonical skill`** | Skills execute the same core workflow; one canonical owner absorbs unique instructions. | Superseded sources moved to `task-folder/agents/not-needed/`. |
| **`Convert one source into a reference or template`** | Source skill contains specialized data, prompts, or templates supporting a broader skill. | Converted into a referenced resource under the canonical skill package. |
| **`Preserve a temporary compatibility alias`** | Widely-referenced legacy skill name preserved as a thin redirect router. | Registered as a thin redirect pointing to the canonical owner. |
| **`Retire a true duplicate`** | Source skill is a 100% byte-for-byte or semantic duplicate with no unique value. | Moved to `task-folder/agents/not-needed/`. |
| **`Defer for manual review`** | Ambiguous boundary requiring manual domain review before consolidation. | Preserved separately with documented review rationale. |

---

## 3. Deliverables & Artifacts

All artifact paths and internal links are repository-relative:

1. **`task-folder/agents/skills-rebuild/_audit/merge-members.csv`** [NEW]:
   - Tracks every candidate source path, its assigned `cluster_id`, `candidate_signal`, and `membership_disposition` (`clustered_for_merge`, `retained_as_canonical`, `standalone_canonical`).
2. **`task-folder/agents/skills-rebuild/_audit/merge-decisions.csv`** [NEW]:
   - Decision log recording `cluster_id`, `cluster_name`, `category`, `subcategory`, `canonical_source_path`, `canonical_destination_path`, `merged_source_paths`, `decision`, `rationale`, `unique_material_disposition`, `resources_moved`, `aliases_retained`, `retired_paths`.
3. **`task-folder/agents/skills-rebuild/_audit/consolidation-map.md`** [NEW]:
   - Comprehensive markdown report detailing methodology, cluster inventory, canonical selection rationale, unique material preservation logs, and reconciliation matrices.
4. **`task-folder/agents/skills-rebuild/_audit/destination-map.csv`** [UPDATE]:
   - Updated to record Phase 06 consolidation status (`phase06_consolidation_status`, `phase06_canonical_destination`, `phase06_superseded_by`) while strictly preserving `phase05_proposed_final_path`.
5. **`task-folder/agents/skills-rebuild/_audit/verify_phase_06.py`** [NEW]:
   - 18-point verification suite.

---

## 4. Full 18-Point Verification Suite Specification

`verify_phase_06.py` implements 18 deterministic checks:

1. **[CHECK 1] Phase 05 Precondition & Baseline Re-validation**: Confirms inventory has 2,331 rows and 2,286 retained skills.
2. **[CHECK 2] Candidate Universe Normalization**: Confirms all 178 name collisions and Phase 05 candidates are deduplicated without omission in `merge-members.csv`.
3. **[CHECK 3] Full Candidate Disposition Coverage**: Proves every row in `merge-members.csv` has an explicit disposition (`candidate source paths = clustered + standalone_canonical`).
4. **[CHECK 4] Cluster Membership Bijectivity**: Asserts no source skill belongs to multiple conflicting clusters.
5. **[CHECK 5] Decision Taxonomy Validity**: Enforces that all cluster decisions belong to the 6 allowed taxonomy values.
6. **[CHECK 6] Single Canonical Owner per Cluster**: Proves every merge cluster designates exactly one canonical owner.
7. **[CHECK 7] Canonical Destination Taxonomy Adherence**: Validates that all canonical destination paths strictly obey the 10 categories and 44 subcategories established in Phase 05.
8. **[CHECK 8] Source-to-Canonical Destination Mapping**: Asserts every merged source path resolves to a valid, unique canonical destination.
9. **[CHECK 9] Material Disposition Ledger**: Verifies all identified unique instructions and resources have an explicit, documented disposition reason.
10. **[CHECK 10] Physical Retirement Verification**: Asserts that all superseded source folders physically reside in `task-folder/agents/not-needed/` and are removed from active skill discovery.
11. **[CHECK 11] Alias Integrity Gate**: Verifies that every compatibility alias is a thin redirect, has a valid target, contains no cycles, and contains no alias-to-alias chaining.
12. **[CHECK 12] Router Link Integrity**: Verifies that no planned or existing router references a superseded/retired skill path.
13. **[CHECK 13] Destination Map Provenance Preservation**: Asserts `destination-map.csv` retains Phase 05 paths while recording Phase 06 canonical destinations.
14. **[CHECK 14] Relative Link & Reference Integrity**: Confirms internal references and moved bundled resources resolve without broken paths.
15. **[CHECK 15] Library Count Reconciliation**: Asserts:
    $$\text{Retained Active Canonical Skills} + \text{Superseded Merged Skills} = 2,286$$
16. **[CHECK 16] Zero Unreviewed Merge Conflicts**: Confirms all clusters marked `Defer for manual review` have documented rationales and no ambiguous unhandled states.
17. **[CHECK 17] Multi-OS Workstation Path Leak Detection**: Regex audit across all Phase 06 files for workstation path leaks.
18. **[CHECK 18] Physical Immutability & Merge-Base Scope Gate**: Dynamically resolves merge-base against `7c2ceb4e` (fail-closed) and confirms clean, scoped changes.

---

## 5. Execution Steps & Batch Commit Strategy

1. **Step 1: Build Candidate Universe & Clustering Scripts**:
   - Extract and normalize candidate pools into `merge-members.csv`.
   - Cluster by trigger, workflow, and output into bounded functional clusters.
2. **Step 2: Cluster Review & Canonical Selection**:
   - Evaluate triggers, workflows, risk/authorization quality, and validation evidence to select canonical owners.
   - Formulate explicit merge instructions and asset preservation plans.
3. **Step 3: Generate Artifacts & Relocate Superseded Sources**:
   - Generate `merge-decisions.csv` and `consolidation-map.md`.
   - Update `destination-map.csv` with Phase 06 provenance fields.
   - Relocate superseded sources to `task-folder/agents/not-needed/` via `git mv`.
4. **Step 4: Execute Full 18-Point Verification Suite**:
   - Run `verify_phase_06.py` and ensure 18/18 checks pass.
5. **Step 5: Publish & PR**:
   - Commit changes on branch `skills-rebuild/phase-06-consolidation`.
   - Push and open a draft PR on GitHub targeting `main`.
