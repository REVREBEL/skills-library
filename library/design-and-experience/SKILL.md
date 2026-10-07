---
name: design-and-experience
description: Category router for design-and-experience, dispatching requests across 4 specialized subcategory routers.
type: category-router
version: 1.0.0
---

# Design And Experience Router

## Overview

The `design-and-experience` domain covers 282 active canonical skills across 4 subcategories.
To optimize context efficiency and classification precision, requests are dispatched via dedicated Subcategory Routers below.

## When to Use

Use this router when the user request involves ui/ux design, design systems, motion graphics, and aesthetic critique.

## Scope Boundaries & Handoffs

- Return to [Root Router](../SKILL.md) if the task falls outside this domain.
- For cross-cutting concerns, verify subcategory router boundaries below before selecting a leaf skill.

## Subcategory Routing Index

| Subcategory | Router Link | Skills Managed | Functional Scope |
|---|---|---|---|
| `design-systems` | [`design-systems/SKILL.md`](./design-systems/SKILL.md) | 60 skills | Design Systems engineering, tooling, and workflows. |
| `motion-and-graphics` | [`motion-and-graphics/SKILL.md`](./motion-and-graphics/SKILL.md) | 29 skills | Motion And Graphics engineering, tooling, and workflows. |
| `taste-and-critique` | [`taste-and-critique/SKILL.md`](./taste-and-critique/SKILL.md) | 75 skills | Taste And Critique engineering, tooling, and workflows. |
| `ui-ux` | [`ui-ux/SKILL.md`](./ui-ux/SKILL.md) | 118 skills | Ui Ux engineering, tooling, and workflows. |

---
*Part of the Canonical Agent Skills Hierarchy.*
