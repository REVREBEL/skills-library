# Design Batch Review — All Four Subcategories

**Scope:** 294 canonical skills under `library/design-and-experience/`
**Mode:** Read-only review. Verdicts are proposals; nothing moved.
**Basis:** descriptions, headings, word counts, and exact content hashes. Not a full read of every body.

---

## 1. Result

| Subcategory | Skills | keep | merge | move | drop |
|---|---:|---:|---:|---:|---:|
| ui-ux | 134 | 89 | 13 | 28 | 4 |
| taste-and-critique | 75 | 55 | 5 | 14 | 1 |
| design-systems | 56 | 35 | 7 | 12 | 2 |
| motion-and-graphics | 29 | 11 | 1 | 16 | 1 |
| **total** | **294** | **190** | **26** | **70** | **8** |

**Design goes from 294 to ~191** (190 kept + one new `ux-laws`), a 35% reduction.

## 2. Routing is the largest lever, again

**70 skills (24%) do not belong in design:**

| Destination | Skills |
|---|---:|
| development | 20 |
| content-and-documentation | 18 |
| business-and-operations | 8 |
| meta-and-agent-skills | 7 |
| ui-ux / design-systems / taste (internal moves) | 8 |
| quality-and-security | 3 |
| data-and-ai | 2 |

`motion-and-graphics` is the extreme case: **16 of 29 (55%) are not motion** — product
canvases, journey maps, storytelling, presentations, a JSON Canvas tool, a Gemini video API.

## 3. The same job exists three times

The review surfaced a concrete cross-subcategory duplicate:

| Skill | Subcategory | Words |
|---|---|---:|
| `front-end-design` | taste-and-critique | 534 |
| `frontend-design` | ui-ux | 608 |
| `frontend-design2` | design-systems | 1,462 |

Three skills, one job: "create distinctive, production-grade frontend interfaces". They should be
**one skill in development**, with the best content from each.

The same pattern appears with `ui-ux-designer` / `user-interface-designer`, and with
`taste-skill` / `design-taste-frontend` (both exactly 12,777 words).

## 4. Consolidations

| Cluster | Resolution |
|---|---|
| 7 cognitive laws (Fitts, Hick, Miller, Doherty, proximity, common region, Von Restorff) | → one `ux-laws` |
| `brandkit2` | → `brandkit` (identical 2,053-word bodies) |
| `design-brief-ux-strategy` | → `design-brief` (identical descriptions) |
| `click-test-plan`, `test-scenario` | → `usability-test-plan` |
| `uxui-principles` | → `heuristic-evaluation` |
| `presentation-deck` | → `presentation-design` |
| `shadcn-ui` | → `shadcn` |
| `core-components` | → `code-showcase-core-components` |
| `artifacts-builder-reports` | → `artifacts-builder` |
| `design-system-patterns`, `design-system-generator` | → `design-system-architect` |
| `remotion-best-practices` | → `remotion` |
| `taste-skill-v1`, `design-taste-frontend` | → `taste-skill` |
| `flat-design-2` | → `flat-design` |
| `spatial-design` | → `spatial-computing-ui` |

## 5. Drops

Eight templated stubs of 114–138 words whose entire body is "Execute X tasks, workflows, and
automated procedures", each fully covered by a substantive neighbour:

`design-review_2`, `design-consultation`, `documentation-template`, `shader-dev`,
`brand-guidelines`, `color-expert`, `imagegen`, `imagen`.

## 6. What is healthy

`taste-and-critique` is the strongest subcategory: 55 of 75 kept, and most of those are the
**design-it style catalog** — 40-odd single-aesthetic implementation guides, each with a distinct
trigger. They share a template but not content, which is the correct shape for a reference library.
`design-it` is the router and should stay.

`design-systems` is coherent too: the Figma MCP family (10 skills) and the design-system
foundation skills are genuinely distinct.

## 7. Recommended sequence

1. **Move the 70 misfiled skills first.** Highest value, lowest risk, no content judgement needed.
2. **Resolve the three-way `frontend-design` duplicate** — pick one home, merge the best content.
3. **Apply the 13 merge clusters**, reading each pair before merging.
4. **Drop the 8 stubs.**
5. **Create `ux-laws`** from the seven cognitive-law skills.

## 8. Files

- `review-design-ui-ux.csv` — 134 rows
- `review-design-taste-and-critique.csv` — 75 rows
- `review-design-design-systems.csv` — 56 rows
- `review-design-motion-and-graphics.csv` — 29 rows