# Design Move Plan — 70 misfiled skills

**Status:** proposal. Nothing has moved.
**Companion file:** `design-move-map.csv` — 70 rows, one per skill.

---

## Summary

| Destination | Skills |
|---|---:|
| content-and-documentation | 18 |
| design-and-experience *(internal)* | 15 |
| development | 14 |
| meta-and-agent-skills | 11 |
| business-and-operations | 6 |
| data-and-ai | 3 |
| quality-and-security | 2 |
| workflow-and-automation | 1 |
| **total** | **70** |

**55 skills leave design entirely. 15 move within it** — those are misfiled inside `design-and-experience`, not outside it.

## Where they go

### content-and-documentation (18)

`pptx`, `pdf`, `docx`, `pitch-deck`, `presentation-builder`, `frontend-slides`, `frontend-slides-frontend-slides` → `presentations/`
`copywriting`, `speech-adaptation`, `voice-analysis`, `storytelling` → `copywriting/`
`json-canvas`, `mermaid-expert`, `summarization`, `doc-coauthoring`, `blind-spot-detective`, `non-fiction-revision`, `content-strategy` → `technical-writing/`

### development (14)

`frontend-design`, `front-end-developer`, `frontend-dev`, `frontend-skill`, `frontend-enhancer`, `frontend-ui-dark-ts`, `react-nextjs-development`, `senior-frontend`, `antigravity-design-expert`, `ce-frontend-design`, `lovable-cleanup`, `algorithmic-art` → `frontend/`
`system-design`, `domain-driven-design` → `software-architecture/`

### meta-and-agent-skills (11)

`agent-to-agent`, `evaluate`, `fortify`, `investigate`, `organize`, `intent`, `include`, `output-skill`, `writing-skills`, `canvas-design`, `design-philosophy`

These are agent orchestration and meta guidance. They were sitting in design because they mention design.

### business-and-operations (6)

`product-inventor`, `product-design`, `jobs-to-be-done`, `value-proposition-canvas`, `strategize`, `travel-planner`

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

## Calls worth confirming

**`frontend-design` and `front-end-developer` move, but `frontend-design2` does not.** It is marked *merge* in the design-systems review, not *move*, so it would be left behind while its two duplicates move to `development/frontend/`. I'd add it to this batch so all three land together and can be merged in one place.

**`json-canvas` → technical-writing.** It is an Obsidian Canvas tool, not documentation. `workflow-and-automation` or a knowledge-management home might fit better.

**`travel-planner` → business-and-operations.** Weak fit. It is itinerary planning with no obvious home in the current taxonomy.

**`canvas-design` and `design-philosophy` → meta-and-agent-skills.** They are meta guidance about how to approach design, not design work. If you would rather keep design philosophy inside design, these two should stay.

## What this does not change

No skill content is rewritten. No merges happen. Every move is a `git mv` plus a router row removal in the source category and a row addition in the destination.

## After approval

1. Move the 70 (71 with `frontend-design2`).
5. Update the 13 source routers and the destination routers.
5. Update `audit/runtime-manifest.json` and regenerate the census.
5. Re-run `validate` — target is 0 broken links, 0 orphans, physical == router == manifest.