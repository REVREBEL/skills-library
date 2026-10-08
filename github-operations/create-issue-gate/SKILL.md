---
name: create-issue-gate
description: 'Create or verify an issue-first execution gate with explicit, testable acceptance criteria before implementation begins. Use when the user or repository requires work to be tracked in GitHub and blocked until scope, non-goals, dependencies, and acceptance criteria are ready.'
compatibility: 'Requires authenticated GitHub access to create or update issues. Repository labels and project fields are optional and must be discovered rather than assumed.'
metadata:
  category: github
  type: issue-gate
  source: consolidated
---

# Create Issue Gate

Establish a durable GitHub issue as the source of truth before implementation when the workflow explicitly requires issue-first delivery.

## When to Use

Use when:

- repository policy requires an issue before code changes
- the user requests issue-first planning
- acceptance criteria must gate execution
- work needs a traceable link across issue, branch, commits, and pull request

Do not impose this gate on repositories or users that do not require it.

## Readiness Criteria

An issue is ready for execution only when it includes:

- problem or opportunity
- intended outcome
- in-scope work
- non-goals
- testable acceptance criteria
- dependencies and blockers
- relevant evidence or source links

Acceptance criteria must be observable and pass/fail checkable.

Weak:

```text
Improve the dashboard.
```

Ready:

```text
When the user selects a source filter, every KPI and table updates to the same source without a page reload.
```

## Workflow

### 1. Resolve repository policy

Inspect issue templates, labels, project fields, contribution guidance, and links required by branch or PR conventions.

### 2. Search for an existing issue

Avoid creating duplicate tracking objects. When an issue already covers the work, evaluate and update that issue instead.

### 3. Draft the gate issue

Use the repository template when present. Otherwise include:

```markdown
## Problem

## Goal

## Scope

## Non-Goals

## Acceptance Criteria

## Dependencies and Blockers

## Evidence

## Execution Readiness
Not Ready | Ready | Blocked
```

GitHub issues do not have a universal draft state. Represent readiness in the body and use labels or project status only when the repository already supports them.

### 4. Evaluate readiness

Set:

- **Not Ready:** missing or ambiguous criteria
- **Ready:** explicit scope and testable criteria
- **Blocked:** definition is ready but an external dependency prevents execution

Do not invent acceptance criteria solely to advance the workflow. Record visible placeholders and obtain the missing decision when it materially affects the result.

### 5. Create or update the issue

Create the issue through GitHub MCP, the connected app, or `gh`. Apply the repository's supported labels and fields.

### 6. Verify and hand off

Read the issue back and record:

- repository and issue number
- readiness state
- acceptance criteria
- blockers
- required branch or PR linkage

Begin implementation only when the gate is Ready or the user explicitly overrides the issue-first policy within their authority.

## Completion

Return the issue URL, readiness decision, missing criteria or blockers, and the next permitted action.
