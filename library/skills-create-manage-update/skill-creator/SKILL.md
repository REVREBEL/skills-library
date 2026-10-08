---
name: skill-creator
description: 'Create and evaluate an advanced Agent Skill package using bundled analyzers, graders, benchmark scripts, reports, packaging tools, and review assets. Use when a skill requires repeatable evaluation infrastructure, baseline-versus-skill comparisons, automated packaging, or a multi-file quality loop beyond a normal scaffold.'
compatibility: 'Requires Python for bundled evaluation scripts and filesystem write access. Inspect script dependencies before execution.'
metadata:
  category: agent-skills
  type: advanced-creation
  source: consolidated-community
---

# Skill Creator

Build an evaluation-backed skill package when a standard `SKILL.md` and a few references are not enough.

## When to Use

Use this skill when the task explicitly requires one or more of:

- Automated skill evaluation
- Baseline-versus-with-skill comparison
- Graders or analyzers
- Benchmark aggregation
- Generated review reports
- Packaging a distributable skill archive
- Repeatable iterative evaluation across examples

Do not use this skill for a straightforward new skill. Use `../skill-make-template/SKILL.md`.
Do not use it solely to improve prose. Use `../skill-writer/SKILL.md` or `../skill-improver/SKILL.md`.

## Bundled Resources

This package contains:

- `agents/analyzer.md`: analyze skill behavior and quality signals
- `agents/comparator.md`: compare baseline and skill-assisted outcomes
- `agents/grader.md`: score outputs against defined criteria
- `references/`: schemas, workflows, and output patterns
- `scripts/init_skill.py`: initialize a skill package
- `scripts/quick_validate.py`: perform quick structural checks
- `scripts/run_eval.py`: run evaluation cases
- `scripts/aggregate_benchmark.py`: aggregate evaluation results
- `scripts/generate_report.py`: create a review report
- `scripts/improve_description.py`: refine discovery descriptions
- `scripts/package_skill.py`: package a completed skill
- `eval-viewer/` and `assets/`: render and inspect evaluation output

Read a script before executing it. Do not assume bundled scripts match the active repository layout.

## Prerequisites

Resolve:

1. Skill purpose and trigger boundary
2. Evaluation question
3. Baseline behavior to compare
4. Representative positive, negative, and edge cases
5. Scoring criteria
6. Required scripts and outputs
7. Runtime and dependency availability

Do not add evaluation infrastructure without a clear decision it will support.

## Workflow

### 1. Define the Evaluation Contract

Specify:

- What success means
- What the baseline is
- Which behaviors should improve
- Which behaviors must not regress
- What evidence will be collected
- How results will be scored

### 2. Create the Core Skill

Use the same fundamentals as `../skill-make-template/SKILL.md`:

- Folder and frontmatter names match
- Description explains what and when
- Main workflow is focused
- Supporting detail uses progressive disclosure
- Completion checks are explicit

### 3. Select Only Necessary Resources

Choose the smallest useful subset of bundled analyzers, graders, scripts, and report assets.

Remove unused scaffolding from the created skill package. Do not copy the entire evaluation framework by default.

### 4. Prepare Evaluation Cases

Include:

- Typical should-trigger examples
- Should-not-trigger examples
- Difficult edge cases
- One or more failure cases from real usage when available
- Holdout cases not used during authoring

Anonymize sensitive session or user data.

### 5. Run a Baseline

Evaluate the task without the skill or with the prior version. Record:

- Output quality
- Workflow completion
- Errors or omissions
- Trigger behavior
- Cost or context usage when measurable

### 6. Run With the Skill

Apply the same cases and scoring criteria. Keep environment and inputs consistent enough for a meaningful comparison.

### 7. Analyze and Improve

Use analyzers, comparators, and graders only as evidence. Inspect false positives and questionable scores manually.

Apply improvements through `../skill-improver/SKILL.md`, then repeat only the affected evaluations.

### 8. Validate and Package

Before packaging:

- Run `../skill-check/SKILL.md`
- Verify references and scripts
- Remove temporary data and secrets
- Confirm licensing and provenance
- Inspect archive contents
- Generate a concise evaluation report

## Script Safety

- Inspect dependencies before installation
- Do not execute scripts from an untrusted skill package
- Keep generated data inside the workspace
- Do not include transcripts, credentials, or personal information in archives
- Treat graders as fallible heuristics
- Report unavailable evaluation data honestly

## Output Format

```markdown
## Advanced Skill Creation

### Skill
- Name:
- Purpose:
- Trigger boundary:

### Evaluation Contract
- Baseline:
- Cases:
- Scoring:

### Resources Used
- ...

### Results
- Baseline:
- With skill:
- Regressions:

### Validation and Package
- Validator result:
- Package path:
- Open limitations:
```

## Completion Checks

- Advanced evaluation infrastructure was justified
- Core skill is independently understandable
- Evaluation cases include positive, negative, and holdout examples
- Baseline and skill-assisted runs use consistent criteria
- Grader results were reviewed rather than accepted blindly
- Unused scaffolding was removed
- Validation passed or failures were disclosed
- Package contents contain no secrets or temporary data
