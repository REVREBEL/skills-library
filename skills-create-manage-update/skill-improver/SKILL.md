---
name: skill-improver
description: 'Repair and iteratively improve an existing Agent Skill while preserving its intended capability. Use when a skill has multiple quality issues, weak triggers, broken references, excessive size, unclear workflows, model-specific assumptions, or failed validation that requires a review-fix-verify loop.'
compatibility: 'Requires filesystem write access. Pair with skill-review for diagnosis and skill-check for final validation.'
metadata:
  category: agent-skills
  type: improvement
  source: consolidated
---

# Skill Improver

Apply a controlled review, repair, and verification loop to one existing skill.

## When to Use

Use this skill when:

- Several related issues must be fixed together
- A skill does not trigger reliably
- Frontmatter, structure, links, or resources are broken
- A monolithic skill needs progressive disclosure
- Provider-specific instructions should be generalized
- A review or validator produced actionable findings

Do not use for read-only diagnostics across many skills; use `../skill-optimizer/SKILL.md`.
Do not use for a single trivial edit that can be applied and verified directly.

## Inputs

Resolve:

- Target skill path
- Intended capability and audience
- Review, audit, or validation findings
- Neighboring skills and overlap risks
- Repository conventions and validator
- Constraints that must be preserved

## Improvement Loop

### 1. Establish the Baseline

Read the full skill and bundled resources. Record:

- Current purpose and triggers
- Required inputs and outputs
- Dependencies and tools
- Existing workflow
- Known issues
- Behaviors that must not change

### 2. Prioritize Findings

Classify issues as:

- **Blocking**: Invalid frontmatter, missing files, unsafe behavior, broken paths, or unsupported intrinsic dependency
- **Major**: Weak triggers, incomplete workflow, missing safeguards, excessive coupling, or severe duplication
- **Minor**: Clarity, formatting, or maintainability improvements

Fix blocking and major issues first. Apply minor changes only when they provide concrete value.

### 3. Plan the Smallest Coherent Repair

For each change, identify:

- Finding addressed
- File and section changed
- Behavior preserved
- New behavior or boundary introduced
- Validation method

Avoid broad rewrites when targeted repairs are sufficient.

### 4. Apply Repairs

Common repairs include:

- Correct name and frontmatter syntax
- Rewrite descriptions with explicit what-and-when triggers
- Add negative trigger boundaries
- Replace proprietary assumptions with capability-based instructions
- Remove unsupported commands, paths, hooks, and tool claims
- Move deep detail into `references/`
- Add missing prerequisites, safeguards, outputs, and completion checks
- Repair relative links
- Consolidate repeated guidance
- Split only when independent jobs exist

Preserve source attribution where relevant.

### 5. Re-Read the Live Files

After index-shifting or structural changes, read the resulting files rather than relying on the planned patch.

Check for:

- Accidental omissions
- Duplicate sections
- Stale links
- New contradictions
- Leftover placeholders
- Unintended trigger overlap

### 6. Validate

Run `../skill-check/SKILL.md` or the repository validator.

When conversion was involved, search for residual provider-specific terms and inspect each match manually.

Do not declare completion while blocking or major findings remain unresolved.

### 7. Repeat Only When Needed

Run another repair cycle when validation identifies a material defect. Stop when:

- Blocking findings are resolved
- Major findings are resolved or explicitly accepted
- Remaining minor items do not justify more complexity
- The skill passes its completion checks

Avoid infinite polishing loops.

## Output Format

```markdown
## Skill Improvement: <name>

### Baseline
- Purpose:
- Preserved behavior:
- Findings addressed:

### Changes Made
1. <file>: <change and rationale>

### Validation
- Validator:
- Result:
- Remaining warnings:

### Open Decisions
- ...
```

## Completion Checks

- Intended capability was preserved
- Blocking and major findings were addressed
- Description and trigger boundaries are clear
- Provider-specific assumptions are intentional or removed
- References and bundled files resolve
- Completion safeguards are present
- Live files were re-read after changes
- Validation was executed or its unavailability disclosed
