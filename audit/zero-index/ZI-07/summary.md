# ZI-07 — Semantic Identity, Lifecycle, Aliases and Metadata Schema

**Work order:** SKIL-10 (ZI-07), plus absorbed ZI-03 scope
**Baseline:** `origin/main` @ `f1ab2439`
**Status:** P0 items 1–3 implemented. P1/P2 remain.

---

## 1. Verdict

**10 implemented · 7 partial · 6 absent** (23 capabilities)

The contracts are well specified and the parts that exist are genuinely tested. What was missing was
the layer connecting specification to catalog — that is now implemented for identity and frontmatter.
Lifecycle remains a field rather than a governed transition.

| Verdict | Capabilities |
|---|---|
| **Implemented** | canonical ID syntax · scope derivation · canonical package coverage · path independence · identity immutability · alias single-hop · alias chaining rejection · four governed duplicate outcomes · single frontmatter parser · frontmatter vocabularies |
| **Partial** | scope+slug uniqueness · census ID conformance · lifecycle vocabulary · ledger evidence · alias sunset metadata · five-field coverage · CI validation |
| **Absent** | identity in package metadata · nested package classification · lifecycle transition API · registry status validation · field semantics · source→registry→view hierarchy |

## 2. Findings that matter

### 2.1 Canonical identity is now derivable, and the derivation is exact

`tools/skill_library/identity.py` implements the ZI-07 scope rule. Run against the live catalog it
produces **2,133 canonical packages**, and that set matches
`audit/taxonomy-census/semantic-role-census.json` **exactly — zero difference in either direction**.

That parity is the strongest available evidence that the rule is correct: an independently produced
census and a path-derived rule converge on the same population.

### 2.2 The census IDs still do not conform to the standard they feed

The census stores bare slugs. **2,102 of 2,133** are rejected by `CanonicalIdentity.parse()`; only 31
are scoped. Identity derivation now works, but the census remains the source of truth and remains
non-conforming. Migrating it is a separate, gated step.

### 2.3 Coverage is complete — the earlier gap was a measurement error

Two earlier statements in this document were wrong and are corrected here:

| Claim | Reality |
|---|---|
| "495 packages missing from the census" | **False.** Canonical coverage is 2,133 of 2,133. |
| "2,102 of 2,103; one package missing" | **False.** The apparent miss, `skills-create-manage-update/skill-writer/skill-writer`, sits at depth 3 under an operational root whose canonical depth is 2 — it is a nested sub-skill, not a canonical package. |

The 494 packages below canonical depth are sub-skills inside vendored packs: 357 under
`marketing-and-seo/technical-seo/seo-skills-main`, 44 under `design-it`, and the rest under
`geo-audit-report`, `super-code`, `wordpress`, and similar. They are not canonical and need a
`reference` or child classification.

### 2.4 The real metadata gap is semantic, not structural

Across all 2,656 packages, 543 lack at least one of `risk`, `source`, `license`. But that number is
misleading:

| Population | Packages | Missing a schema field |
|---|---:|---:|
| Canonical — 10 functional categories | 2,103 | **0** |
| Canonical — operational roots | 30 | **30** |
| Non-canonical nested packs | 523 | 513 |

**Every functional canonical package is structurally complete.** The gap is concentrated in one
operational root (`skills-create-manage-update`) and in non-canonical packs.

What is actually missing is meaning:

| Field | Canonical distribution |
|---|---|
| `risk` | 2,102 `unknown` · 1 `safe` · 1 `critical` · 29 absent |
| `license` | 2,102 `not_declared_upstream` · 1 `MIT` · 30 absent |

Structurally present, semantically empty. This — not missing fields — is the ZI-08 blocker: the
execution plane cannot make decisions from `risk: unknown`.

### 2.5 Validation covers 2,102 of 2,133 canonical packages

`validate_library_integrity` iterates the router-indexed set, which covers the ten functional
categories. The 31 operational packages (`github-operations`, `skills-create-manage-update`) are never
schema-checked.

Extending coverage to all 2,133 surfaces one pre-existing defect:
`library/github-operations/llms-maintain` has four broken relative links
(`README.md`, `docs/api.md`, and two more). That is a library content fix, not a schema fix, and is
left alone here.

### 2.6 Lifecycle is a label, not a transition

`ReviewStatus` defines `active, manual_review, deprecated, draft, sunset`. There is:

- no `retired` state, though ZI-07 names `active/deprecated/retired`;
- no transition function — `status` is a plain assignable field;
- no validation — `SkillObject` silently swallows unknown statuses
  (`except ValueError: pass  # Allow custom status strings`);
- no lifecycle evidence in the ledger — `ChangeLedger.record_change` records operation and decision,
  not state transitions.

Alias deprecation telemetry returns a notice with a target but **no sunset milestone**, which
ADR-004 explicitly requires.

## 3. What was implemented

### 3.1 One frontmatter parser

`tools/skill_library/frontmatter.py` now owns `parse_frontmatter`. The three copies in `scanner.py`,
`validator.py`, and `intake.py` are deleted and import from it.

The old scanner variant was genuinely different: it split on `content.split("---", 2)` and did not
skip comment lines, so it disagreed with the other two on real input. The shared parser is line-based
and requires an exact `---` delimiter.

### 3.2 Vocabularies and validation

```python
REQUIRED_FIELDS = ("name", "description", "risk", "source", "license")
RISK_LEVELS     = {safe, low, elevated, critical, unknown}
LICENSE_VALUES  = {MIT, Apache-2.0, BSD-*, GPL-3.0, LGPL-3.0, MPL-2.0,
                   CC-BY-4.0, CC0-1.0, Unlicense, proprietary, not_declared_upstream}
```

`validate_frontmatter(fm, strict=False)` returns `(errors, warnings)`:

- `name` / `description` missing → **error** always.
- `risk` / `source` / `license` missing → **warning** by default, **error** under `strict`.
- Out-of-vocabulary value → **error** always. A present-but-wrong value is unambiguous.
- A license naming a bundled file (`Complete terms in LICENSE.txt`) is accepted.

Strictness is opt-in because 30 canonical and 513 non-canonical packages still need backfilling.
`validate --strict-frontmatter` turns the warnings into errors.

### 3.3 Scope derivation

```python
scope = SCOPE_MAP.get(root, root)   # skills-create-manage-update -> skills-lifecycle
slug  = leaf directory name
id    = f"{scope}:{slug}"
```

Functional categories are canonical at depth 3; operational roots at depth 2. Routers and nested
sub-skills return `None` rather than raising, because they are legitimately outside the set.

Collision handling is `find_collisions()`, which reports duplicate claims for ADR-004 §5.2
adjudication. It does not resolve them.

### 3.4 Validator reporting

`ValidationResult` now carries `frontmatter_warnings` and the summary prints:

```
Frontmatter Schema Warnings: 0 (license: 0, risk: 0, source: 0)
```

## 4. Decisions

### 4.1 Canonical five fields: `name, description, risk, source, license`

Rejected `category` / `source_type`: `category` is a derived ownership axis, and storing it in the
package creates a second source of truth that rots on re-ownership — the failure mode ADR-002 exists
to prevent. `source_type` folds into `source`. `license` stays because it is a hard publication gate.

### 4.2 Scope derivation: ownership root + leaf, collisions adjudicated

Validated against the catalog:

| Scheme | Unique | Collisions |
|---|---:|---:|
| leaf only | 2,068 | 499 |
| category+subcategory scope, leaf | 2,483 | 114 |
| **ownership root + leaf (chosen)** | **2,132** | **1** |

The single collision is `marketing-and-seo:competitor-analysis` (`on-page-seo/` vs `cro/`) — a genuine
duplicate pair.

`canonical_id` is derived at compile time, never written into frontmatter, so exactly one source of
truth remains.

## 5. Remaining ZI-07 work

| # | Work | Priority | Notes |
|---|---|---|---|
| 1 | Adjudicate the single `competitor-analysis` pair | P1 | closes scope+slug uniqueness |
| 2 | Classify the 494 nested packages as reference or child | P1 | not canonical; do not mint |
| 3 | Add `retired` to `ReviewStatus` and an explicit transition API | P1 | reject invalid transitions |
| 4 | Extend `ChangeLedger` with lifecycle transition records | P1 | the evidence ZI-03 asked for |
| 5 | Enforce `status` against the enum in `RegistryEntry` and `SkillObject` | P1 | remove the silent `except ValueError: pass` |
| 6 | Backfill `risk` and `license` for the 30 operational packages | P1 | prerequisite for ZI-08 coverage |
| 7 | Decide how `risk` gets real values at scale | P1 | 2,102 `unknown`; blocks ZI-08 |
| 8 | Migrate the census to scoped canonical IDs | P2 | gated under Phase 04 |
| 9 | Extend per-skill validation to operational roots | P2 | would surface the `llms-maintain` link defect |
| 10 | Add the sunset milestone to deprecation telemetry | P2 | ADR-004 requirement |
| 11 | Define and document the source→registry→view hierarchy | P2 | prerequisite for ZI-10 |

## 6. What this does not do

- Does not rewrite skills or frontmatter. Enforcement is opt-in via `--strict-frontmatter`.
- Does not mint identities into files, and does not rewrite the census.
- Does not touch `library/`, the manifest, or the runtime.

## 7. Files

- `capability-matrix.csv` — 23 capabilities × implemented / tested / evidence / verdict / gap.
- `summary.md` — this document.
- `tools/skill_library/frontmatter.py`, `tools/skill_library/identity.py` — implementation.
- `tests/test_frontmatter.py`, `tests/test_identity.py` — 37 tests.