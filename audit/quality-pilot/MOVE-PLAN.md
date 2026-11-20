# Design Move Plan — 68 misfiled skills

**Status:** proposal. Nothing has moved.
**Companion file:** `design-move-map.csv` — 68 rows, one per skill.

---

## Summary

| Destination | Skills |
|---|---:|
| content-and-documentation | 18 |
| design-and-experience *(internal)* | 15 |
| development | 15 |
| meta-and-agent-skills | 9 |
| business-and-operations | 5 |
| data-and-ai | 3 |
| quality-and-security | 2 |
| workflow-and-automation | 1 |
| **total** | **68** |

**53 skills leave design entirely. 15 move within it** — misfiled inside `design-and-experience`, not outside.

## Where they go

### content-and-documentation (18)

`pptx`, `pitch-deck`, `presentation-builder`, `frontend-slides`, `frontend-slides-frontend-slides` → `presentations/`
`pdf`, `docx` → `technical-writing/`
`copywriting`, `speech-adaptation`, `voice-analysis`, `storytelling` → `copywriting/`
`json-canvas`, `mermaid-expert`, `summarization`, `doc-coauthoring`, `blind-spot-detective`, `non-fiction-revision`, `content-strategy` → `technical-writing/`

### development (15)

`frontend-design`, `frontend-design2`, `front-end-developer`, `frontend-dev`, `frontend-skill`, `frontend-enhancer`, `frontend-ui-dark-ts`, `react-nextjs-development`, `senior-frontend`, `antigravity-design-expert`, `ce-frontend-design`, `lovable-cleanup`, `algorithmic-art` → `frontend/`
`system-design`, `domain-driven-design` → `software-architecture/`

`frontend-design`, `frontend-design2`, and `front-end-developer` are the three-way duplicate. They land together so the merge can happen in one place.

### meta-and-agent-skills (9)

`agent-to-agent`, `evaluate`, `fortify`, `investigate`, `organize`, `intent`, `include`, `output-skill`, `writing-skills`

Agent orchestration and skill-authoring guidance that was sitting in design because it mentions design.

### business-and-operations (5)

`product-inventor`, `product-design`, `jobs-to-be-done`, `value-proposition-canvas`, `strategize`

### data-and-ai (3)

`business-analytics-reporter`, `xlsx` → `analytics/`; `gemini-omni-flash-api` → `machine-learning/`

### quality-and-security (2)

`threat-modeling-expert`, `transilience-report-style`

### workflow-and-automation (1)

`version-control-strategy` → `git-and-vcs/`

### Internal design moves (15)

`affinity-diagram`, `summarize-interview`, `ui-ux-designer`, `journey-map` → `ui-ux/`
`interface-kit`, `ui-component`, `ui-page`, `ui-tokens`, `ui-update`, `webflow-ui-skills` → `design-systems/`
`minimalist-ui`, `soft-skill` → `taste-and-critique/`
`ui-motion`, `email-design-eng`, `review-animations` → `motion-and-graphics/`

## Calls settled

**Stays in design (3):**

- `travel-planner` — it is about designing travel-planning applications, so it is design work, not itinerary planning.
- `canvas-design` and `design-philosophy` — design philosophy, kept in `taste-and-critique/`.

**Added to the batch (1):**

- `frontend-design2` — joins `frontend-design` and `front-end-developer` in `development/frontend/` so the three-way duplicate can be merged in one place.

**Accepted as-is (1):**

- `json-canvas` → `technical-writing/` is a compromise; it is an Obsidian Canvas format rather than documentation, but nothing better exists.

## Validation of the map

- Every destination parent exists on disk
- Every destination path is unique
- Every source still exists
- 68 rows, matching the 68 approved moves

## What this does not change

No skill content is rewritten. No merges happen. Every move is a `git mv` plus a router row removal in the source category and a row addition in the destination.

## After approval

1. Move the 68.
2. Update the 4 source routers (`design-systems`, `motion-and-graphics`, `taste-and-critique`, `ui-ux`) and the destination routers.
3. Update `audit/runtime-manifest.json` and regenerate the census.
4. Re-run `validate` — target is 0 broken links, 0 orphans, physical == router == manifest.
