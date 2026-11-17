# Design Batch Review — `ui-ux`

**Scope:** 134 canonical skills in `library/design-and-experience/ui-ux/`
**Mode:** Read-only review. Verdicts are proposals; nothing moved.
**Basis:** descriptions, headings, and word counts. Not a full read of every body.

---

## 1. Result

| Verdict | Skills | Share |
|---|---:|---:|
| keep | 89 | 66% |
| merge | 13 | 10% |
| move | 28 | 21% |
| drop | 4 | 3% |

After merges, the subcategory holds **90 skills** (89 kept + 1 new `ux-laws`), down from 134.

## 2. The biggest win is routing, not deduplication

**28 skills (21%) do not belong in design at all:**

| Destination | Skills |
|---|---|
| content-and-documentation | 14 — `pptx`, `pdf`, `docx`, `xlsx`*, `copywriting`, `content-strategy`, `pitch-deck`, `speech-adaptation`, `summarization`, `mermaid-expert`, `voice-analysis`, `blind-spot-detective`, `non-fiction-revision`, `doc-coauthoring` |
| meta-and-agent-skills | 7 — `evaluate`, `fortify`, `investigate`, `organize`, `strategize`, `output-skill`, `agent-to-agent` |
| development | 4 — `front-end-developer`, `frontend-design`, `frontend-skill`, `domain-driven-design`, `version-control-strategy` |
| data-and-ai | 2 — `business-analytics-reporter`, `xlsx` |
| business-and-operations | 2 — `travel-planner`, `strategize` |

This is the same pattern the data pilot found. The category is not padded with weak design skills —
it is **a design category with other domains' skills parked in it**, which makes design look broader
and shallower than it is.

## 3. Consolidations

**Seven cognitive-law skills → one.** `doherty-threshold`, `fitts-law`, `hicks-law`, `millers-law`,
`law-of-proximity`, `law-of-common-region`, `von-restorff-effect` are each a single explainer of one
principle. They share a trigger shape ("apply X to Y") and belong in one `ux-laws` reference.

**Four smaller merges:**

| Cluster | Merged into |
|---|---|
| `brandkit2` | `brandkit` — identical 2,053-word bodies |
| `design-brief-ux-strategy` | `design-brief` — identical descriptions |
| `click-test-plan`, `test-scenario` | `usability-test-plan` — three ways to plan one test |
| `uxui-principles` | `heuristic-evaluation` |
| `presentation-deck` | `presentation-design` |

## 4. Drops

Four templated stubs of 115–138 words whose entire body is "Execute X tasks, workflows, and
automated procedures": `brand-guidelines`, `color-expert`, `imagegen`, `imagen`. Each is fully
covered by a substantive neighbour.

## 5. What this means for the other subcategories

If `ui-ux` is representative, design's 294 in-category skills will land near **200 after routing and
merging** — not because the design skills are weak, but because a fifth of the folder is other
domains' work.

The remaining three subcategories to review:

| Subcategory | Skills |
|---|---:|
| taste-and-critique | 75 |
| design-systems | 56 |
| motion-and-graphics | 29 |

## 6. Files

- `review-design-ui-ux.csv` — 134 rows: skill, verdict, target, reason.