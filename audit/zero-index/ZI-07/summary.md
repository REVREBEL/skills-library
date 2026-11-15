# ZI-07 — Semantic Identity, Lifecycle, Aliases and Metadata Schema

**Work order:** SKIL-10 (ZI-07), plus absorbed ZI-03 scope
**Baseline:** `origin/main` @ `f1ab2439`
**Mode:** Read-only assessment. No production code changed.

---

## 1. Verdict

**6 implemented · 7 partial · 6 absent**

The contracts are well specified and the parts that exist are genuinely tested. What is missing is the
layer that connects the specification to the catalog: identity is defined but never materialised, and
lifecycle is a field rather than a governed transition.

| Verdict | Capabilities |
|---|---|
| **Implemented** | Canonical ID syntax · path independence · identity immutability · alias single-hop · alias chaining rejection · four governed duplicate outcomes |
| **Partial** | Census ID conformance · census coverage · lifecycle vocabulary · ledger evidence · alias sunset metadata · frontmatter coverage · CI frontmatter validation |
| **Absent** | Identity in package metadata · scope derivation · lifecycle transition API · registry status validation · single frontmatter parser · source→registry→view hierarchy |

## 2. The four findings that matter

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

### 2.3 Coverage has a hole

2,133 census records against 2,656 library packages. **495 packages have no census record** — 451 of
them outside the `design-it` reference package, e.g. `library/development/backend/wordpress/*` and
`library/development/frontend/development/developer/*`. These have no canonical ID at all.

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

Two things follow. First, the effective five-field set is `name, description, risk, source, license`
— not the `category/risk/source/source_type` set in the original task objective. Second, **543 packages
are missing at least one of those five**, so even the de facto contract is not met.

`argument-hint`, `allowed-tools`, and `user-invokable` are Claude Code slash-command metadata. They
belong in the conversion backlog, not the canonical schema.

### Frontmatter parsing is implemented three times

`scanner.py`, `validator.py`, and `intake.py` each define their own `parse_frontmatter`. The scanner
variant is not equivalent: it splits on `content.split("---", 2)` and does not skip comment lines, so
it disagrees with the other two on real input.

## 4. Proposed ZI-07 work

Ordered by dependency. P0 items are prerequisites for the capability matrix being meaningful at all.

| # | Work | Priority | Notes |
|---|---|---|---|
| 1 | Adopt one frontmatter parser, delete the other two | **P0** | Behaviour must be fixed before any schema work; scanner variant is the odd one out |
| 2 | Define the canonical five fields and enforce them in the validator | **P0** | Resolve `license` vs `category/source_type` explicitly, in the ADR |
| 3 | Introduce a scope derivation rule and mint scoped IDs for the 2,102 unscoped census records | **P0** | Deterministic, testable, and reversible; ADR-001 permits derivation |
| 4 | Close the 495-package coverage gap or record a documented exclusion | P1 | `design-it` is the likely exclusion; 451 others are not |
| 5 | Add `retired` to `ReviewStatus` and an explicit transition API | P1 | Reject invalid transitions; keep aliases on the deprecated path |
| 6 | Extend `ChangeLedger` with lifecycle transition records | P1 | Append-only; this is the evidence ZI-03 asked for |
| 7 | Enforce `status` against the enum in `RegistryEntry` and `SkillObject` | P1 | Remove the silent `except ValueError: pass` |
| 8 | Add the sunset milestone to deprecation telemetry | P2 | ADR-004 requirement |
| 9 | Define and document the source→registry→view hierarchy | P2 | Prerequisite for ZI-10, not for ZI-07 |

## 5. What this does not do

- Does not rewrite skills or frontmatter. Item 2 produces a validator change, not a bulk edit.
- Does not mint identities yet. Item 3 is a rule plus tests; applying it to the catalog is a separate,
  gated migration under Phase 04.
- Does not touch `library/`, the manifest, or the runtime.

## 6. Files

- `capability-matrix.csv` — 19 capabilities × implemented / tested / evidence / verdict / gap.