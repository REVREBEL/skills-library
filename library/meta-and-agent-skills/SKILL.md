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
| [`agent-to-agent`](agent-architecture/agent-to-agent/SKILL.md) | Agent-to-Agent (A2A) communication protocol. Connect two or more Claude agents that pass messages, share context, delegate tasks, and collaborate. Implements structured handoffs, shared memory, and multi-agent conversations. Use when working with agent to agent. | Agent To Agent: Agent-to-Agent (A2A) communication protocol. Connect two or more Claude agents that pass messages, share conte... |
| [`aria`](../business-and-operations/legal-and-governance/aria/SKILL.md) | Autonomous agent coordination and squad orchestration for multi-step task execution. Use when orchestrating collaborative multi-agent workflows or task deleg... | Aria: Autonomous agent coordination and squad orchestration for multi-step task executio... |
| [`evaluate`](agent-architecture/evaluate/SKILL.md) | Execute evaluate tasks, workflows, and automated procedures. Use when working with evaluate. | Evaluate: Execute evaluate tasks, workflows, and automated procedures. Use when working with evaluate.... |
| [`fortify`](agent-architecture/fortify/SKILL.md) | Execute fortify tasks, workflows, and automated procedures. Use when working with fortify. | Fortify: Execute fortify tasks, workflows, and automated procedures. Use when working with fortify.... |
| [`include`](agent-architecture/include/SKILL.md) | Execute include tasks, workflows, and automated procedures. Use when working with include. | Include: Execute include tasks, workflows, and automated procedures. Use when working with include.... |
| [`intent`](agent-architecture/intent/SKILL.md) | Execute intent tasks, workflows, and automated procedures. Use when working with intent. | Intent: Execute intent tasks, workflows, and automated procedures. Use when working with intent.... |
| [`investigate`](agent-architecture/investigate/SKILL.md) | Execute investigate tasks, workflows, and automated procedures. Use when working with investigate. | Investigate: Execute investigate tasks, workflows, and automated procedures. Use when working with investigate.... |
| [`organize`](agent-architecture/organize/SKILL.md) | Execute organize tasks, workflows, and automated procedures. Use when working with organize. | Organize: Execute organize tasks, workflows, and automated procedures. Use when working with organize.... |
| [`output-skill`](agent-architecture/output-skill/SKILL.md) | Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any task requiring exhaustive, unabridged output. Use when working with output skill. | Output Skill: Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and h... |
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
| [`writing-skills`](skill-lifecycle/writing-skills/SKILL.md) | Use when creating, updating, or improving agent skills. | Writing Skills: Use when creating, updating, or improving agent skills.... |

### Skill Validation

Manage 2 skills for skill validation.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`llm-prompt-optimizer`](skill-validation/llm-prompt-optimizer/SKILL.md) | Use when improving prompts for any LLM. Applies proven prompt engineering techniques to boost output quality, reduce hallucinations, and cut token usage. | Llm Prompt Optimizer: improving prompts for any LLM. Applies proven prompt engineering techniques to boo... |
| [`project-skill-audit`](skill-validation/project-skill-audit/SKILL.md) | Audit a project and recommend the highest-value skills to add or update. Use when working with project skill audit. | Project Skill Audit: Audit a project and recommend the highest-value skills to add or update. Use when ... |

---
*Part of the Canonical Agent Skills Hierarchy.*
