---
name: template-skill-enhanced
description: 'Provide a worked example of a complex Agent Skill package with progressive disclosure, references, examples, and a validation rubric. Use when an author needs a structural example for a multi-file skill after the skill architecture has already been chosen; do not use as the primary creation workflow.'
compatibility: 'Reference template only. Replace all placeholders and validate against the active repository rules before use.'
metadata:
  category: agent-skills
  type: example-template
  source: consolidated
---

# Enhanced Skill Template

Use this package as a structural example for complex skills that genuinely need bundled resources and measurable quality criteria.

## When to Use

Use this template when:

- A skill needs multiple references or examples
- A validation rubric is materially useful
- Progressive disclosure is required
- A parent or complex workflow has already been justified

Do not use it for a simple single-job skill. Use `../skill-make-template/SKILL.md`.
Do not copy placeholder content into production.

## Included Resources

- `examples/basic.md`: annotated example structure
- `references/README.md`: reference-organization guidance
- `validation/rubric.yaml`: example quality rubric

Treat these as examples. The target skill's requirements determine the final files and fields.

## Adaptation Workflow

### 1. Confirm Complexity Is Justified

Document why a normal `SKILL.md` is insufficient. Valid reasons include:

- Several detailed reference domains
- Reusable scripts or templates
- Multiple output examples
- A quality rubric used repeatedly

### 2. Copy Only Needed Pieces

Start with:

```text
<skill-name>/
├── SKILL.md
├── references/
├── examples/
└── validation/
```

Remove directories the target skill does not need. Add `scripts/`, `assets/`, or `templates/` only when justified.

### 3. Replace Frontmatter

Ensure the name matches the folder and the description explains both what and when.

```yaml
---
name: <skill-name>
description: '<Capability>. Use when <specific triggers and scenarios>.'
---
```

Do not copy optional metadata automatically.

### 4. Replace All Example Content

Replace:

- Placeholder names
- Generic code
- Example quality targets
- Sample paths
- Unsupported commands
- References to unrelated tools or repositories

### 5. Apply Progressive Disclosure

Keep in `SKILL.md`:

- Trigger boundary
- Prerequisites
- Core workflow
- Safety constraints
- Output format
- Completion checks

Move into bundled files:

- Detailed examples
- Schemas
- Long platform guidance
- Reusable templates
- Evaluation rubrics

### 6. Adapt the Rubric

Use a rubric only when outputs can be evaluated consistently. Define observable criteria rather than vague qualities.

Example:

```yaml
criteria:
  trigger_precision:
    target: pass
    evidence: positive and negative trigger cases
  path_integrity:
    target: pass
    evidence: all relative references resolve
  workflow_completion:
    target: pass
    evidence: completion checks executed
```

### 7. Validate

Use the repository's documented validator and `../skill-check/SKILL.md`.

Verify:

- No placeholder content remains
- Optional directories are used
- Relative paths resolve
- Rubric criteria match the actual skill
- The main file remains focused
- Trigger boundaries are distinct

## Anti-Patterns

- Copying the whole template for a simple skill
- Treating token volume as quality
- Leaving generic example code in production
- Inventing validator commands
- Adding a rubric that no workflow uses
- Duplicating the same guidance in `SKILL.md` and references

## Completion Checks

- Complex structure was justified
- Only necessary template elements were copied
- All placeholders and example assumptions were replaced
- Progressive disclosure was applied
- Rubric and examples support the target job
- The resulting package was validated
