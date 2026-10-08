---
name: skill-make-template
description: 'Scaffold a straightforward Agent Skill folder and write a valid SKILL.md from clear requirements. Use when asked to create a skill, make a new skill, convert a focused task into Agent Skills format, generate frontmatter, or explain the basic Agent Skills structure. Use skill-writer for complex source synthesis and skill-creator for evaluation-heavy packages.'
compatibility: 'Requires filesystem write access. Use the repository-provided validator when available.'
metadata:
  category: agent-skills
  type: creation
  source: custom
---

# Skill Make Template

Create a focused, specification-aligned Agent Skill without adding machinery the task does not need.

## When to Use

Use this skill when:

- The requested capability is clear and bounded
- A new skill folder and `SKILL.md` are needed
- Existing instructions should be converted into Agent Skills format
- A simple skill needs optional references, scripts, assets, or templates
- The user needs the basic Agent Skills specification explained

Do not use this skill for:

- Large source-backed synthesis or extensive iterative authoring; use `../skill-writer/SKILL.md`
- Benchmarking, graders, packaging, or evaluation harnesses; use `../skill-creator/SKILL.md`
- Improving an existing skill with several issues; use `../skill-improver/SKILL.md`

## Required Inputs

Resolve:

1. The single job the skill performs
2. Trigger phrases and scenarios
3. Expected inputs and outputs
4. Required tools, files, and permissions
5. Explicit exclusions
6. Completion checks

Check whether an existing skill already performs the same job before creating another.

## Workflow

### 1. Define the Skill Boundary

Write a compact design note containing:

- Primary job
- When to use
- When not to use
- Required inputs
- Expected outputs
- Dependencies
- Validation requirements

Split the request only when parts have independent triggers or outcomes.

### 2. Choose the Name

Use a lowercase kebab-case name that matches the folder exactly.

```text
skills/<skill-name>/
└── SKILL.md
```

Name rules:

- 1–64 characters
- Lowercase letters, numbers, and hyphens only
- No spaces, underscores, consecutive hyphens, or leading/trailing hyphens
- Prefer a concrete functional name over `helper`, `utilities`, or `general`

### 3. Write Frontmatter

Every skill requires `name` and `description`.

```yaml
---
name: <skill-name>
description: '<What it does>. Use when <specific triggers, scenarios, keywords, applications, or file types>.'
---
```

Optional fields may include:

```yaml
license: MIT
compatibility: 'Requires Node.js and filesystem access.'
metadata:
  category: development
  type: workflow
allowed-tools: Read Write Bash
```

Include optional fields only when they affect routing, provenance, compatibility, or execution.

### 4. Optimize the Description

The description must explain both **what** the skill does and **when** it should trigger.

Strong example:

```yaml
description: 'Test local web applications with Playwright. Use when asked to verify frontend behavior, reproduce UI defects, capture screenshots, inspect browser console errors, or test responsive flows.'
```

Weak example:

```yaml
description: 'Web testing helpers.'
```

Use realistic prompt language and keep neighboring skills distinguishable.

### 5. Write the Body

Use only the sections that improve execution:

```markdown
# Skill Title

Purpose and outcome.

## When to Use
Trigger conditions and boundaries.

## Prerequisites
Required tools, permissions, and inputs.

## Workflow
Ordered execution steps.

## Validation
Checks required before completion.

## Troubleshooting
Common failures and recovery actions.
```

Workflows should:

- Start by grounding the target and inputs
- Separate read, plan, execute, and verify stages
- State safeguards for destructive actions
- Define outputs and failure handling
- End with explicit completion checks

### 6. Add Bundled Resources Only When Needed

| Folder | Purpose |
|---|---|
| `scripts/` | Repeatable executable automation |
| `references/` | Detailed documentation loaded when needed |
| `assets/` | Static files used as-is |
| `templates/` | Starter files the agent modifies |

Keep `SKILL.md` concise. Move deep examples, schemas, and platform documentation into references.

### 7. Validate

Run the repository validator when available. Discover the documented command rather than assuming one.

Verify:

- Folder and frontmatter names match
- YAML parses correctly
- Description contains what and when
- Relative paths resolve
- Bundled resources are actually referenced
- Scripts contain no embedded secrets
- Trigger boundaries do not collide with another skill
- The workflow includes completion checks
- No placeholders remain

Do not claim validation passed unless it was executed.

## Parent and Child Skills

Use a parent router when several related children have different triggers.

```text
category/
├── SKILL.md
├── first-job/
│   └── SKILL.md
└── second-job/
    └── SKILL.md
```

The parent routes and defines shared constraints. Each child owns one complete execution workflow.

## Completion Output

Return:

1. Created or updated paths
2. Skill purpose and trigger summary
3. Bundled resources added
4. Validation performed and results
5. Any unresolved assumptions or dependencies

## Reference

Agent Skills specification: https://agentskills.io/specification
