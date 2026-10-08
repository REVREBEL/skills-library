---
name: skills-create-manage-update
description: 'Route Agent Skill inventory, audit, review, validation, creation, advanced authoring, iterative improvement, evidence-based optimization, lifecycle management, and functional library restructuring. Use when working on SKILL.md files or reorganizing an Agent Skills library.'
compatibility: 'Requires read access to target skills. Creation, repair, lifecycle, and restructuring workflows require filesystem write access.'
metadata:
  category: agent-skills
  type: master-router
  source: custom
---

# Skills Create, Manage & Update

Route Agent Skill lifecycle work to the narrowest child skill. This parent defines boundaries and common workflow sequences; child skills own execution.

## Routing Table

| User goal | Use |
|---|---|
| Catalog every skill before decisions | [Skill Inventory](./skill-inventory/SKILL.md) |
| Audit security, compatibility, permissions, or provider coupling | [Skill Audit](./skill-audit/SKILL.md) |
| Decide whether one skill should be kept, refined, merged, split, or retired | [Skill Review](./skill-review/SKILL.md) |
| Validate a finished skill package | [Skill Check](./skill-check/SKILL.md) |
| Scaffold a straightforward new skill | [Skill Make Template](./skill-make-template/SKILL.md) |
| Author a complex source-backed skill | [Skill Writer](./skill-writer/SKILL.md) |
| Create an evaluation-backed skill package | [Skill Creator](./skill-creator/SKILL.md) |
| Repair an existing skill through a review-fix-verify loop | [Skill Improver](./skill-improver/SKILL.md) |
| Diagnose trigger behavior and skill economics from real usage | [Skill Optimizer](./skill-optimizer/SKILL.md) |
| List, move, sync, enable, disable, or retire installed skills | [Skill Manage](./skill-manage/SKILL.md) |
| Merge, split, categorize, convert, and rebuild an entire library | [Skill Library Restructure](./skill-library-restructure/SKILL.md) |
| Consult advanced architecture and testing patterns | [Skills Writing Pattern Library](./skills-writing/SKILL.md) |
| Use a worked multi-file template example | [Enhanced Template](./template-skill-enhanced/SKILL.md) |

## Boundary Guide

### Audit vs Review vs Check

- **Skill Audit**: Is the source safe, compatible, and appropriately scoped?
- **Skill Review**: Does it belong, and what primary disposition should it receive?
- **Skill Check**: Does the finished package comply and validate?

### Create vs Writer vs Creator

- **Skill Make Template**: Direct, focused creation from clear requirements
- **Skill Writer**: Complex authoring from multiple sources, examples, or architecture decisions
- **Skill Creator**: Evaluation-backed creation using analyzers, graders, benchmarks, reports, or packaging tools

### Improver vs Optimizer

- **Skill Improver**: Writes repairs to one skill
- **Skill Optimizer**: Read-only analysis using usage data and static quality dimensions

### Manage vs Restructure

- **Skill Manage**: Lifecycle operations on installed or located skills
- **Skill Library Restructure**: Repository-wide merge, split, conversion, categorization, and router work

## Universal Rules

- Inventory before broad moves
- Read the complete skill and referenced files before deciding
- Use one documented primary disposition per source skill
- Preserve provenance and source-to-final traceability
- Evaluate primary dependencies, not incidental examples
- Group by functional job rather than application name alone
- Split by independent triggers or outcomes, not length alone
- Merge only true workflow duplicates
- Parent skills route; child skills execute
- Prefer capability-based language over accidental model coupling
- Do not execute untrusted scripts during audit
- Do not claim validation passed unless it ran
- Confirm before destructive or irreversible lifecycle operations

## Recommended Workflows

### Rebuild a Skills Library

1. [Skill Inventory](./skill-inventory/SKILL.md)
2. [Skill Audit](./skill-audit/SKILL.md) for application, provider, and safety gates
3. [Skill Review](./skill-review/SKILL.md) for primary dispositions
4. [Skill Library Restructure](./skill-library-restructure/SKILL.md)
5. [Skill Improver](./skill-improver/SKILL.md) for canonical repairs
6. [Skill Check](./skill-check/SKILL.md) for final validation
7. [Skill Manage](./skill-manage/SKILL.md) for installation or lifecycle changes

### Create a Simple Skill

1. [Skill Make Template](./skill-make-template/SKILL.md)
2. [Skill Check](./skill-check/SKILL.md)

### Create a Complex Skill

1. [Skill Writer](./skill-writer/SKILL.md)
2. Consult [Skills Writing](./skills-writing/SKILL.md) only for needed patterns
3. Use [Enhanced Template](./template-skill-enhanced/SKILL.md) only as a structural example
4. [Skill Check](./skill-check/SKILL.md)

### Create an Evaluated Skill Package

1. [Skill Writer](./skill-writer/SKILL.md) or [Skill Make Template](./skill-make-template/SKILL.md) for the core skill
2. [Skill Creator](./skill-creator/SKILL.md) for benchmarks, graders, reports, and packaging
3. [Skill Improver](./skill-improver/SKILL.md) for evidence-driven repairs
4. [Skill Check](./skill-check/SKILL.md)

### Improve One Skill

1. [Skill Review](./skill-review/SKILL.md)
2. [Skill Improver](./skill-improver/SKILL.md)
3. [Skill Check](./skill-check/SKILL.md)

### Diagnose Underperforming Skills

1. [Skill Optimizer](./skill-optimizer/SKILL.md)
2. [Skill Review](./skill-review/SKILL.md) for disposition decisions
3. [Skill Improver](./skill-improver/SKILL.md) for approved changes
4. [Skill Check](./skill-check/SKILL.md)

## Active Child Index

- [Skill Inventory](./skill-inventory/SKILL.md)
- [Skill Audit](./skill-audit/SKILL.md)
- [Skill Review](./skill-review/SKILL.md)
- [Skill Check](./skill-check/SKILL.md)
- [Skill Make Template](./skill-make-template/SKILL.md)
- [Skill Writer](./skill-writer/SKILL.md)
- [Skill Creator](./skill-creator/SKILL.md)
- [Skill Improver](./skill-improver/SKILL.md)
- [Skill Optimizer](./skill-optimizer/SKILL.md)
- [Skill Manage](./skill-manage/SKILL.md)
- [Skill Library Restructure](./skill-library-restructure/SKILL.md)
- [Skills Writing Pattern Library](./skills-writing/SKILL.md)
- [Enhanced Template](./template-skill-enhanced/SKILL.md)

## Completion Checks

Before completing any lifecycle workflow, confirm:

- Target and scope are explicit
- Source revision and paths are recorded
- Relevant child skill was selected
- Required dependencies and permissions are known
- Source-to-final traceability is preserved
- Router links and relative paths resolve
- Provider-specific assumptions are intentional
- Validation results are truthful
- Destructive actions were confirmed and verified
