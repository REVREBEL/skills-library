---
name: publish-changes
description: 'Move completed repository changes through review, validation, branch preparation, commits, push, and pull-request creation. Use when asked to publish changes, commit and push work, save changes to GitHub, open a pull request, or take a completed implementation from the working tree to a verified remote PR.'
compatibility: 'Requires a local Git repository plus authenticated GitHub access through GitHub MCP, a connector, or gh CLI.'
metadata:
  category: github
  type: publication-workflow
  source: consolidated
---

# Publish Changes

Publish completed work through a guarded, reviewable GitHub workflow without bypassing repository policy or absorbing unrelated files.

## When to Use

Use when the user wants a complete route such as:

- commit and push these changes
- save this work to GitHub
- publish the branch
- open a draft pull request
- take completed work through validation and PR creation

Use `commit` for a local commit only. Use `pr-writer` when the branch already exists remotely and only the PR needs creation or editing.

## Control and Handoff

Keep control in `publish-changes` while the same completed change is moving through review, validation, branch preparation, commit, push, PR creation, and remote verification.

- Use `github`, `create-branch`, `commit`, and `pr-writer` as delegated capabilities, then return here to continue the end-to-end workflow.
- Hand control back to `github` when publication is complete and the new request is only a separate remote query or small metadata operation, such as reading PR state, adding a label, assigning someone, or posting a standalone comment.
- Hand off to `actions-debugger` when a live check fails. Return here only when the failure has been resolved and publication-state verification must continue.
- End this workflow and route to `pr-review` for an independent code review or `pr-merge-champion` for an authorized merge. Do not repeat branch, commit, push, or PR-creation steps that already succeeded.

## Workflow

### 1. Resolve repository policy and scope

Read applicable repository instructions and identify:

- target repository and base branch
- current branch and upstream
- intended changed files
- required tests, lint, build, security, and documentation checks
- branch, commit, and PR conventions
- required issue links, reviewers, labels, templates, or merge queue

Repository policy wins over user shorthand such as “push to main.”

### 2. Capture the exact working state

```bash
git status --short --branch
git diff --stat
git diff --cached --stat
git branch --show-current
git remote -v
```

Review the full relevant diff. Preserve unrelated dirty or staged work.

### 3. Review and validate

Perform an appropriate self-review for:

- correctness and regression risk
- secrets and security issues
- missing tests or documentation
- debugging artifacts and accidental files
- repository-policy compliance

Run the repository's required checks. Fix only in-scope source or policy defects, then rerun the failed check and the required suite.

Do not weaken gates or mark checks complete when they were skipped.

### 4. Prepare the branch

If the current branch is the protected or default branch, use `create-branch` to create a topic branch from the correct base.

Fetch the base when concurrent changes are plausible. Do not rewrite a shared branch or force-push without explicit authorization.

### 5. Create focused commits

Use the `commit` workflow for each logical change set. Confirm the working tree after every commit.

### 6. Push the branch

Resolve the remote and upstream rather than assuming `origin`.

```bash
git push -u <remote> <branch>
```

If the push is rejected:

- protected branch: switch to the required topic-branch and PR route
- non-fast-forward: fetch and inspect divergence before rebasing or merging
- authentication or permission failure: stop and report it

Never retry with force automatically.

### 7. Create or update the pull request

Use `pr-writer` to prepare the title and body from the actual branch diff and repository template.

Create a draft PR by default for broad work unless the user or repository policy requires ready-for-review status.

The PR must truthfully state:

- what changed and why
- validation actually run
- risks, migration, deployment, rollback, or breaking-change notes when relevant
- issue links and screenshots when applicable
- known gaps or blockers

### 8. Verify remote state

Read back:

- remote branch head SHA
- PR number and URL
- base and head branches
- draft or ready state
- current checks and mergeability

Bind the report to the current head SHA. If the branch changes, previous review and check conclusions may be stale.

## Safety Rules

- Never commit or publish secrets
- Never bypass branch protection, required checks, reviews, or merge queues
- Never hide unrelated changes in the branch or PR
- Never claim a workflow, deployment, or merge succeeded without remote verification
- Never delete local or remote branches unless requested
- Never perform a release or deployment merely because a PR was created

## Completion

Report:

- branch and remote
- commits published
- pull-request URL and state
- validation and checks
- preserved unrelated work
- exact remaining blocker, when one exists
