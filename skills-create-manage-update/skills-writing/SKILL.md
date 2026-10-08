---
name: skills-writing
description: 'Reference advanced Agent Skill architecture, discovery optimization, anti-rationalization, testing, and tiered design patterns while authoring or restructuring complex skills. Use as a pattern library when skill-writer or skill-improver needs deeper guidance; do not use as the primary creation workflow.'
compatibility: 'Reference-only. Some bundled material originated in provider-specific environments and must be adapted before reuse.'
metadata:
  category: agent-skills
  type: pattern-library
  source: consolidated-community
---

# Skills Writing Pattern Library

Consult focused architecture and testing references without introducing another competing creation workflow.

## When to Use

Use this skill as supporting guidance when:

- A complex skill needs an architecture tier
- Agents ignore or rationalize around important rules
- Skill discovery descriptions need deeper optimization
- A team needs metadata and structural standards
- A skill needs behavior-focused testing guidance
- `../skill-writer/SKILL.md` or `../skill-improver/SKILL.md` requires a specific pattern

Do not use this skill to scaffold a new skill directly. Use `../skill-make-template/SKILL.md`.
Do not load every reference. Select only the material needed for the current decision.

## Reference Index

### Architecture Tiers

- `references/tier-1-simple/README.md`: focused single-job skills
- `references/tier-2-expanded/README.md`: skills with several supporting concepts or resources
- `references/tier-3-platform/README.md`: parent routers and broad platform families

Choose a tier based on independent capabilities and context-loading needs, not prestige or word count.

### Discovery and Metadata

- `references/cso/README.md`: description and trigger optimization
- `references/standards/README.md`: naming, metadata, and folder conventions
- `references/standards/metadata-standard.md`: detailed metadata guidance

Treat bundled metadata recommendations as proposals. The active Agent Skills specification and repository rules take precedence.

### Discipline and Rule Reliability

- `references/anti-rationalization/README.md`: writing concrete rules agents are less likely to evade

Use anti-rationalization patterns only for real safety, correctness, or process risks. Do not turn ordinary preferences into shrill mandatory language.

### Testing

- `references/testing/README.md`: behavior-oriented skill testing
- `testing-skills-with-subagents.md`: delegation-based testing concepts

Replace provider-specific subagent syntax with the active environment's supported delegation mechanism.

### Templates

- `references/templates/technique.md`
- `references/templates/reference.md`
- `references/templates/discipline.md`
- `references/templates/pattern.md`
- `references/templates/tier-3-platform.md`

Templates are structural examples, not content authority. Remove placeholders and unsupported assumptions before use.

### Additional Guidance

- `examples.md`: representative patterns
- `gotchas.md`: common failure modes
- `persuasion-principles.md`: communication principles requiring careful use
- `anthropic-best-practices.md`: provider-originated guidance that must be generalized unless the target is explicitly Claude-specific

## Selection Workflow

1. Define the current authoring or repair decision.
2. Select one or two relevant references.
3. Identify provider-specific or outdated assumptions.
4. Extract the reusable principle.
5. Adapt it to the active specification and environment.
6. Apply it through `skill-writer` or `skill-improver`.
7. Validate the resulting skill with `skill-check`.

## Guardrails

- Do not copy provider-specific paths, hooks, slash commands, or tool names accidentally
- Do not require `metadata.triggers` unless the active specification or repository does
- Do not force every skill into a tiered architecture
- Do not add anti-rationalization language where ordinary clear instructions suffice
- Do not use subagents unless delegation is available and useful
- Do not let references contradict the parent workflow

## Completion Checks

- Only relevant references were loaded
- Reusable principles were separated from platform-specific implementation
- Active specification and repository rules took precedence
- Applied guidance improved a concrete authoring decision
- Resulting skill was validated independently
