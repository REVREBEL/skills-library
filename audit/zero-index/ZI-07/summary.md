# ZI-07 — Semantic Identity, Lifecycle, Aliases and Metadata Schema

**Work order:** SKIL-10 (ZI-07), plus absorbed ZI-03 scope
**Baseline:** `origin/main` @ `f1ab2439`
**Mode:** Read-only assessment. No production code changed.

---

## 1. Verdict

**6 implemented · 8 partial · 8 absent** (22 capabilities)

The contracts are well specified and the parts that exist are genuinely tested. What is missing is the
layer that connects the specification to the catalog: identity is defined but never derived from disk,
and lifecycle is a field rather than a governed transition.

| Verdict | Capabilities |
|---|---|
| **Implemented** | Canonical ID syntax · path independence · identity immutability · alias single-hop · alias chaining rejection · four governed duplicate outcomes |
| **Partial** | census ID conformance · canonical package coverage · scope+slug uniqueness · lifecycle vocabulary · ledger evidence · alias sunset metadata · frontmatter coverage · CI frontmatter validation |
| **Absent** | identity in package metadata · scope derivation · nested package classification · lifecycle transition API · registry status validation · frontmatter vocabularies · single frontmatter parser · source→registry→view hierarchy |

## 2. Findings that matter

### 2.1 Canonical identity is defined but not materialised

`CanonicalIdentity` is a correct, tested implementation of ADR-001. But **0 of 2,656** library
`SKILL.md` files carry a `canonical_id` or `urn:skill:` value. Identity exists only at runtime, in
memory, and nothing on disk supplies it.

### 2.2 The census IDs do not conform to the standard they feed

`audit/taxonomy-census/semantic-role-census.json` holds 2,133 records with unique `canonical_id`
values. Only **31** are scoped. The other **2,102** are bare slugs (`007`, `1password`,
`1password-cli`). Fed to the real parser:

```
census ids parseable: 31, rejected: 2102
  ('007', "Invalid canonical identifier '007'. Must be formatted as '<scope>:<slug>' ...")
```

So INV-6 holds for 1.5% of the catalog. Every downstream gate that consumes the census inherits this.

### 2.3 Coverage is nearly complete

Earlier in this pass I recorded 495 packages as missing from the census. **That was wrong** and is
corrected here. The census is scoped to *canonical packages*, which are the 2,103 packages at
`library/<root>/<subroot>/<skill>`:

| Population | Count |
|---|---:|
| Library packages at canonical depth | 2,103 |
| Census records at that depth | 2,102 |
| **Missing** | **1** — `library/skills-create-manage-update/skill-writer/skill-writer` |

The 494 deeper packages are **not canonical skills**. They are sub-skills nested inside vendored packs:
357 under `marketing-and-seo/technical-seo/seo-skills-main`, 44 under `design-it`, and the rest under
`geo-audit-report`, `super-code`, `wordpress`, and similar. They have no census record by design, not by
oversight. They need a `reference` or child classification, which is a separate decision.

### 2.4 Lifecycle is a label, not a transition

`ReviewStatus` defines `active, manual_review, deprecated, draft, sunset`. There is:

- no `retired` state, though ZI-07 names `active/deprecated/retired`;
- no transition function — `status` is a plain assignable field;
- no validation — `SkillObject` silently swallows unknown statuses
  (`except ValueError: pass  # Allow custom status strings`);
- no lifecycle evidence in the ledger — `ChangeLedger.record_change` records operation and decision,
  not state transitions.

Alias deprecation telemetry returns a notice with a target but **no sunset milestone**, which
ADR-004 explicitly requires.

## 3. Metadata and frontmatter

Observed across all 2,656 packages:

| Field | Present |
|---|---:|
| `name`, `description` | 2,656 (100%) |
| `license` | 2,208 (83%) |
| `source` | 2,196 (83%) |
| `risk` | 2,196 (83%) |
| `metadata` | 147 |
| `date_added` | 91 |
| `source_type` | 55 (2%) |
| `category` | 13 |
| `argument-hint` | 39 |
| `allowed-tools` | 15 |
| `user-invokable` | 19 |

**543 packages** are missing at least one of the five. More importantly, the fields that are present
mostly carry sentinel values:

| Field | Distribution |
|---|---|
| `risk` | 2,113 `unknown` · 75 `safe` · 7 `critical` |
| `license` | 2,101 `not_declared_upstream` · 87 `MIT` · 19 `Apache-2.0` · 2 other |

Enforcing presence without fixing vocabulary would be theatre. `argument-hint`, `allowed-tools`, and
`user-invokable` are Claude Code slash-command metadata and belong in the conversion backlog.

### Frontmatter parsing is implemented three times

`scanner.py`, `validator.py`, and `intake.py` each define their own `parse_frontmatter`. The scanner
variant is not equivalent: it splits on `content.split("---", 2)` and does not skip comment lines, so
it disagrees with the other two on real input.

## 4. Decisions

### 4.1 Canonical five fields: `name, description, risk, source, license`

**Chosen:** the observed de facto set. **Rejected:** `category` and `source_type`.

- `category`/`subcategory` are **derived** ownership axes. ADR-004 compiles the registry from
  frontmatter *plus* the census; storing category in the package would create a second source of truth
  that silently rots on re-ownership, which is the failure mode ADR-002 exists to prevent.
- `source_type` is a refinement of `source` and folds into it.
- `license` is a **publication gate**. The program goal includes version-pinned project packaging and
  optional runtime publication, and redistribution rights are a hard blocker. `not_declared_upstream`
  on 2,101 packages is exactly the signal that must stay visible.

Consequence: `risk` and `license` need real vocabularies before enforcement means anything. That is a
ZI-07 deliverable, and `risk` is a hard dependency for ZI-08 (execution plane).

### 4.2 Scope derivation: ownership root + leaf, with adjudication on collision

**Chosen:**

1. **Scope** = the top-level ownership root under `library/`, mapped through an explicit `SCOPE_MAP`
   for roots whose curated name differs from the folder name (`skills-create-manage-update` →
   `skills-lifecycle`, matching the existing census convention).
2. **Slug** = the leaf directory name.
3. **Uniqueness**: `Count(owner(<scope>:<slug>)) == 1` (ADR-001 §2.2 rule 5).
4. **On collision**: ADR-004 §5.2 duplicate adjudication. A collision means two packages claim the
   same capability, so it is a semantic decision, not a naming problem to paper over.

**Validated against the catalog:**

| Scheme | Unique | Collisions |
|---|---:|---:|
| leaf name only | 2,068 | 499 |
| category + subcategory scope, leaf | 2,483 | 114 |
| category scope + full subpath slug | 2,597 | 0 |
| **ownership root + leaf (chosen)** | **2,102** | **1** |

The chosen rule is collision-free except for **one** pair:
`marketing-and-seo:competitor-analysis` at `on-page-seo/competitor-analysis` and `cro/competitor-analysis`.
That is a genuine duplicate pair and belongs in adjudication, not in a naming ladder.

**Why not materialise `canonical_id` into frontmatter.** ADR-001 permits deterministic scope
derivation, and the program's own hard invariant forbids generated values from being independently
hand-maintained across surfaces. Deriving at compile time keeps one source of truth; writing 2,102 IDs
into 2,102 files would create a second one that must be reconciled forever.

**Nested packages.** The 494 packages below canonical depth are not minted. They are classified as
`reference` or as children of their pack, which is a separate decision from scope derivation.

## 5. Proposed ZI-07 work

Ordered by dependency. P0 items are prerequisites for anything downstream.

| # | Work | Priority | Notes |
|---|---|---|---|
| 1 | Adopt one frontmatter parser, delete the other two | **P0** | behaviour must be fixed before schema work; scanner variant is the odd one out |
| 2 | Define `risk` and `license` vocabularies, then enforce the five fields | **P0** | presence alone is meaningless while values are `unknown` / `not_declared_upstream` |
| 3 | Implement scope derivation + `SCOPE_MAP`, with tests | **P0** | rule is decided (4.2); code plus fixtures |
| 4 | Adjudicate the single `competitor-analysis` pair | P1 | one decision, closes scope+slug uniqueness |
| 5 | Add the 1 missing package to the census | P1 | `library/skills-create-manage-update/skill-writer/skill-writer` |
| 6 | Classify the 494 nested packages as reference or child | P1 | not canonical; do not mint |
| 7 | Add `retired` to `ReviewStatus` and an explicit transition API | P1 | reject invalid transitions; aliases stay on the deprecated path |
| 8 | Extend `ChangeLedger` with lifecycle transition records | P1 | append-only; this is the evidence ZI-03 asked for |
| 9 | Enforce `status` against the enum in `RegistryEntry` and `SkillObject` | P1 | remove the silent `except ValueError: pass` |
| 10 | Add the sunset milestone to deprecation telemetry | P2 | ADR-004 requirement |
| 11 | Define and document the source→registry→view hierarchy | P2 | prerequisite for ZI-10, not for ZI-07 |

## 6. What this does not do

- Does not rewrite skills or frontmatter. Item 2 produces a validator change, not a bulk edit.
- Does not mint identities. Item 3 is a rule plus tests; applying it to the catalog is a separate,
  gated migration under Phase 04.
- Does not touch `library/`, the manifest, or the runtime.

## 7. Files

- `capability-matrix.csv` — 22 capabilities × implemented / tested / evidence / verdict / gap.
- `summary.md` — this document.