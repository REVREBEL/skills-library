---
name: meta-and-agent-skills
description: Category router for meta-and-agent-skills, dispatching 9 canonical skills across 3 subcategories.
type: category-router
version: 1.0.0
---

# Meta And Agent Skills Router

## Overview

The `meta-and-agent-skills` domain covers **9 active canonical skills** organized under 3 specialized subcategories.

## When to Use

Use this router when the user request involves agent architecture, skill authoring, progressive disclosure, and validation tooling.

## Scope Boundaries & Handoffs

- Return to [Root Router](../SKILL.md) if the task falls outside this domain.

## Subcategory Routing Index

### Agent Architecture

Manage 3 skills for agent architecture.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`aria`](../business-and-operations/legal-and-governance/aria/SKILL.md) | Autonomous agent coordination and squad orchestration for multi-step task execution. Use when orchestrating collaborative multi-agent workflows or task deleg... | Aria: Autonomous agent coordination and squad orchestration for multi-step task executio... |
| [`subagent-driven-development`](agent-architecture/subagent-driven-development/SKILL.md) | Use when executing implementation plans with independent tasks in the current session. | Subagent Driven Development: executing implementation plans with independent tasks in the current session |
| [`subagent-orchestrator`](agent-architecture/subagent-orchestrator/SKILL.md) | Coordinate quota-aware parallel subagents for large, multi-file Antigravity tasks. Use when working with subagent orchestrator. | Subagent Orchestrator: Coordinate quota-aware parallel subagents for large, multi-file Antigravity tasks.... |

### Skill Lifecycle

Manage 4 skills for skill lifecycle.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`agent-creator`](skill-lifecycle/agent-creator/SKILL.md) | Create custom AI subagents with proper plugin structure, persona generation, and companion routing skills. Use when working with agent creator. | Agent Creator: Create custom AI subagents with proper plugin structure, persona generation, and c... |
| [`codex-subagent`](skill-lifecycle/codex-subagent/SKILL.md) | Launch Codex CLI as an isolated subagent for bounded coding, review, or verification tasks. Use when working with codex subagent. | Codex Subagent: Launch Codex CLI as an isolated subagent for bounded coding, review, or verificati... |
| [`effective-agent-skills`](skill-lifecycle/effective-agent-skills/SKILL.md) | Author and review high-quality agent skills with triggers, progressive disclosure, and safety notes. Use when working with effective agent skills. | Effective Agent Skills: Author and review high-quality agent skills with triggers, progressive disclosure,... |
| [`orchestrate`](skill-lifecycle/orchestrate/SKILL.md) | Coordinate focused subagents on substantial work, keep their ownership non-overlapping, and integrate verified results. Use for large-scope Codex tasks; keep... | Orchestrate: Coordinate focused subagents on substantial work, keep their ownership non-overlap... |

### Skill Validation

Manage 2 skills for skill validation.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`llm-prompt-optimizer`](skill-validation/llm-prompt-optimizer/SKILL.md) | Use when improving prompts for any LLM. Applies proven prompt engineering techniques to boost output quality, reduce hallucinations, and cut token usage. | Llm Prompt Optimizer: improving prompts for any LLM. Applies proven prompt engineering techniques to boo... |
| [`project-skill-audit`](skill-validation/project-skill-audit/SKILL.md) | Audit a project and recommend the highest-value skills to add or update. Use when working with project skill audit. | Project Skill Audit: Audit a project and recommend the highest-value skills to add or update. Use when ... |

---
*Part of the Canonical Agent Skills Hierarchy.*
