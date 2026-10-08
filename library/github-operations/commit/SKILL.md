---
name: commit
description: 'Review a Git working tree, stage one logical change set, and create a clear commit that follows repository conventions. Use when asked to commit changes, prepare a commit, write a commit message, or separate mixed work into reviewable commits.'
compatibility: 'Requires a local Git repository and permission to modify the index and create commits.'
metadata:
  category: github
  type: commit-operation
  source: consolidated
---

# Commit Changes

Create a truthful, reviewable commit without including secrets or unrelated user work.

## When to Use

Use when the user asks to:

- Commit current changes
- Stage and commit selected files
- Generate or improve a commit message
- Split mixed changes into logical commits
- Prepare committed work before a push or pull request

This skill stops after local commit creation. Use `publish-changes` when the user also wants the branch pushed or a pull request opened.

## Workflow

### 1. Read repository policy

Inspect applicable instructions, commit conventions, required hooks, and generated-file rules.

### 2. Inspect all change states

```bash
git status --short --branch
git diff --stat
git diff --cached --stat
git diff
git diff --cached
```

Include untracked files in the review. Determine which files belong to the requested change.

### 3. Define one logical commit

Separate unrelated concerns. A commit should represent one coherent behavior, fix, refactor, documentation change, or maintenance operation.

Do not stage everything by default when the working tree contains unrelated work.

### 4. Check for sensitive or generated content

Before staging, reject or exclude:

- `.env` files and credentials
- private keys and certificates
- access tokens or session cookies
- local databases and dumps
- temporary files and editor artifacts
- generated files that repository policy says not to commit

When a suspicious value appears in the diff, stop and surface it rather than committing it.

### 5. Stage explicit paths

Prefer explicit paths:

```bash
git add -- path/to/file-a path/to/file-b
```

Use interactive staging when one file contains mixed concerns:

```bash
git add -p
```

Review the staged diff after staging:

```bash
git diff --cached --check
git diff --cached
```

### 6. Run required validation

Run repository-required checks appropriate to the staged change. Do not bypass hooks with `--no-verify` unless the user explicitly authorizes it and repository policy permits it.

### 7. Write the message

Follow repository conventions. When none exist, use Conventional Commits:

```text
<type>(<optional-scope>): <imperative summary>
```

Common types:

- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `ci`
- `build`
- `chore`
- `revert`

Keep the subject concise. Add a body when the reason, migration impact, risk, or breaking change is not obvious from the diff.

### 8. Commit and verify

```bash
git commit -m "<message>"
git show --stat --oneline --decorate HEAD
git status --short --branch
```

Do not amend an existing commit unless explicitly requested and safe for the branch.

## Safety Rules

- Never update global or repository Git configuration unless requested
- Never reset, clean, discard, or overwrite unrelated work
- Never commit merge-conflict markers
- Never claim validation passed unless it ran successfully
- Never create an empty commit unless explicitly requested
- Never rewrite published history without explicit authorization

## Completion

Report:

- commit SHA and message
- files included
- validation run
- remaining uncommitted changes
