---
name: skills-rebuild
description: Master root router for the canonical Agent Skills library, directing incoming user intents to the appropriate functional category router.
type: master-router
version: 1.0.0
---

# Agent Skills Library: Master Root Router

## Overview

Welcome to the canonical Agent Skills library. This master router directs incoming coding, infrastructure, design, data, business, and workflow requests to the appropriate functional category router.

The library is organized across **10 functional categories** and **44 specialized subcategories**, covering **2,103 canonical skills**, each indexed exactly once by physical path, with precise progressive disclosure.

## Functional Category Dispatch

Evaluate the user request against the 10 top-level functional categories below:

| Category | Purpose & Capabilities | Subcategories | Routing Depth |
|---|---|---|---|
| [`business-and-operations`](./business-and-operations/SKILL.md) | Business modeling, product management, startup finance, governance, and strategy. | 4 | Direct (routes directly to leaf skills) |
| [`content-and-documentation`](./content-and-documentation/SKILL.md) | Technical writing, presentations, research synthesis, and editorial copywriting. | 4 | Direct (routes directly to leaf skills) |
| [`data-and-ai`](./data-and-ai/SKILL.md) | Data engineering, analytics, machine learning, LLM/RAG pipelines, and vector databases. | 5 | Direct (routes directly to leaf skills) |
| [`design-and-experience`](./design-and-experience/SKILL.md) | UI/UX design, design systems, motion graphics, and aesthetic critique. | 4 | Deep (routes to 4 Subcategory Routers) |
| [`development`](./development/SKILL.md) | Software architecture, backend, frontend, fullstack, mobile, and low-level systems programming. | 6 | Deep (routes to 6 Subcategory Routers) |
| [`infrastructure-and-ops`](./infrastructure-and-ops/SKILL.md) | CI/CD pipelines, cloud platforms, container orchestration, observability, and sysadmin. | 5 | Direct (routes directly to leaf skills) |
| [`marketing-and-seo`](./marketing-and-seo/SKILL.md) | SEO strategy, technical crawlability, conversion rate optimization, and advertising campaigns. | 5 | Deep (routes to 5 Subcategory Routers) |
| [`meta-and-agent-skills`](./meta-and-agent-skills/SKILL.md) | Agent architecture, skill authoring, progressive disclosure, and validation tooling. | 3 | Direct (routes directly to leaf skills) |
| [`quality-and-security`](./quality-and-security/SKILL.md) | Automated testing, debugging, software security, and regulatory compliance. | 4 | Direct (routes directly to leaf skills) |
| [`workflow-and-automation`](./workflow-and-automation/SKILL.md) | Workflow automation, web scraping, Git version control, and MCP tool integration. | 4 | Direct (routes directly to leaf skills) |

## Cross-Category Disambiguation & Boundary Rules

When a request appears to touch multiple functional categories, apply the following deterministic disambiguation rules:

- **Code vs Architecture**: If designing system boundaries or DDD domain models, route to [`development`](./development/SKILL.md); for high-level cloud topologies, route to [`infrastructure-and-ops`](./infrastructure-and-ops/SKILL.md).
- **UI/UX Design vs Frontend Code**: If crafting design tokens, aesthetic critiques, or Figma designs, route to [`design-and-experience`](./design-and-experience/SKILL.md); for React/Next.js/Vue code implementation, route to [`development`](./development/SKILL.md).
- **SEO vs Marketing Copy**: If auditing technical crawlability, schema, or indexing, route to [`marketing-and-seo`](./marketing-and-seo/SKILL.md); for editorial non-promotional prose, route to [`content-and-documentation`](./content-and-documentation/SKILL.md).
- **Security vs Testing**: If conducting penetration testing, threat modeling, or vulnerability mitigation, route to [`quality-and-security`](./quality-and-security/SKILL.md); for unit/integration/E2E testing suites, route to [`quality-and-security`](./quality-and-security/SKILL.md).
- **Agent Meta Skills**: If authoring new SKILL.md files, building evaluation harnesses, or designing subagents, route strictly to [`meta-and-agent-skills`](./meta-and-agent-skills/SKILL.md).

---
*Maintained by the Agent Skills Architecture Team.*
