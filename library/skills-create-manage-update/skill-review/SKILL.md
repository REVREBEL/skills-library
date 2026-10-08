---
name: skill-review
description: 'Review one Agent Skill for purpose, relevance, quality, trigger clarity, size, overlap, dependencies, and library fit. Use when deciding whether to keep, refine, convert, split, merge, quarantine, or retire a skill after inventory and security audit.'
compatibility: 'Read-only by default. Requires access to neighboring skills when overlap or dependency decisions are needed.'
metadata:
  category: agent-skills
  type: disposition-review
  source: consolidated
---

# Skill Review

Evaluate one skill and assign a traceable primary disposition.

## When to Use

Use this skill when:

- Reviewing an ambiguous or high-impact skill individually
- Deciding whether a skill belongs in a library
- Comparing a skill with nearby or similarly triggered skills
- Determining whether a long skill should be split
- Determining whether similar skills should be merged
- Reviewing whether model-specific instructions can be generalized

Run `../skill-audit/SKILL.md` first when security or compatibility is unknown.
Run `../skill-check/SKILL.md` after changes are completed.

## Required Inputs

Resolve:

- Source path and current name
- Intended audience and library purpose
- Approved application stack
- Neighboring or similarly triggered skills
- Known dependencies and reverse dependencies
- Existing audit findings

## Workflow

### 1. Read the Complete Skill

Read `SKILL.md` and every referenced file. Record:

- Claimed purpose
- Actual instructions
- Trigger phrases
- Required inputs
- Expected outputs
- Tools and application dependencies
- Supporting resources
- Validation behavior

### 2. Test Purpose and Relevance

Ask:

- Does the skill solve a recurring, useful job?
- Does that job fit the target library?
- Is the capability already covered elsewhere?
- Is the skill current enough to retain?
- Would a generic agent already perform this reliably without the skill?

### 3. Review Trigger Quality

Check whether:

- The description explains what and when
- Trigger phrases match realistic requests
- The scope is neither vague nor overbroad
- Negative boundaries are clear when needed
- Another skill would trigger on the same request

### 4. Review Workflow Quality

Check:

- Steps form a complete executable workflow
- Prerequisites and permissions are explicit
- Instructions are capability-based where possible
- Failure handling and safeguards are present
- Outputs and completion checks are defined
- Repetition and narrative clutter are limited

### 5. Review Size and Structure

Split only when the skill contains independently triggered jobs or outputs.

Move detail into references when it supports the same job but overloads the main file.

Do not split solely because the file is long.

### 6. Review Overlap

Compare nearby skills by:

- Trigger phrases
- Required inputs
- Expected outputs
- Workflow stages
- Supporting resources
- Unique guidance

Merge when skills perform the same natural job and unique content can be preserved cleanly.

Do not merge merely because they share an application or broad topic.

### 7. Review Model and Application Coupling

Classify provider-specific content as:

- Required and legitimate
- Replaceable with capability-based language
- A removable example
- Fundamental and unsupported

A converted skill must not retain accidental proprietary paths, hooks, commands, or tool names.

### 8. Assign One Primary Disposition

Choose exactly one:

- **Keep as-is**
- **Refine**
- **Convert**
- **Split**
- **Merge**
- **Quarantine**
- **Retire**

Secondary actions may support the primary disposition, but do not leave the decision ambiguous.

## Decision Rules

### Keep as-is

Use when the skill is relevant, focused, current, distinct, and valid.

### Refine

Use when the core job is valuable but clarity, workflow, safety, or progressive disclosure needs repair.

### Convert

Use when the capability is useful but current implementation is tied unnecessarily to a provider, tool, or unsupported application.

### Split

Use when separate sections have independent triggers, prerequisites, or outcomes.

### Merge

Use when two or more skills perform the same job and can share one clear trigger boundary.

### Quarantine

Use when safety, provenance, or dependencies remain unresolved.

### Retire

Use when the skill is obsolete, fully superseded, intrinsically unsupported, or provides no meaningful unique value.

## Output Format

```markdown
## Skill Review: <name>

### Primary Disposition
Keep as-is | Refine | Convert | Split | Merge | Quarantine | Retire

### Rationale
<concise evidence-based explanation>

### Functional Profile
- Purpose:
- Triggers:
- Inputs:
- Outputs:
- Dependencies:
- Unique value:

### Overlap
- Related skills:
- Shared behavior:
- Unique behavior:

### Required Actions
1. ...

### Final Destination
<path or TBD>
```

## Completion Checks

- Complete skill and referenced files were read
- Relevance and uniqueness were evaluated
- Trigger and workflow quality were reviewed
- Size and overlap were assessed functionally
- Model/application coupling was classified
- One primary disposition was assigned
- Final destination or next action is explicit
