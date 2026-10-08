---
name: create-branch
description: 'Create a safe local or remote task branch using the repository branching policy. Use when asked to create, start, switch to, or name a branch for new work, including feature, fix, refactor, documentation, release, or hotfix work.'
compatibility: 'Requires Git for local branches. Remote branch creation requires authenticated GitHub access or an existing Git remote.'
metadata:
  category: github
  type: branch-operation
  source: consolidated
---

# Create Branch

Create a branch from an explicitly resolved base without losing or absorbing unrelated work.

## When to Use

Use when the user wants to:

- Start a branch for a task
- Generate an appropriate branch name
- Switch from the default branch before implementation
- Create a feature, fix, refactor, release, or hotfix branch
- Create a remote branch from a known commit

Use `advanced-workflows` instead for history rewriting, cherry-picking, bisecting, reflog recovery, or complex branch surgery.

## Workflow

### 1. Read repository policy

Inspect repository instructions and discover:

- default branch
- branching model
- naming convention
- protected branches
- required issue or ticket references

Do not assume Git Flow, trunk-based development, username prefixes, or `main` when the repository already defines a policy.

### 2. Inspect current state

For a local repository, read:

```bash
git status --short --branch
git branch --show-current
git remote -v
git rev-parse --show-toplevel
```

Identify uncommitted and staged work. Do not stash, discard, or move it without authorization.

### 3. Resolve the base

Choose the base in this order:

1. user-specified base
2. repository-defined branch for the requested work type
3. repository default branch
4. current commit only when intentionally branching from detached HEAD or an existing task branch

Fetch the remote base when stale local state could matter.

### 4. Generate the name

Follow the repository convention. When none exists, use:

```text
<type>/<short-kebab-description>
```

Recommended types:

- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `ci`
- `chore`
- `release`
- `hotfix`

Include an issue or ticket key when supplied or required. Keep the description concise and meaningful.

### 5. Check for collisions

Confirm the proposed branch does not already exist locally or remotely.

```bash
git show-ref --verify --quiet refs/heads/<branch>
git ls-remote --exit-code --heads origin <branch>
```

Do not silently switch to or overwrite an existing branch.

### 6. Create the branch

For a local task branch:

```bash
git switch -c <branch> <resolved-base>
```

For remote-only creation through GitHub, use the exact resolved commit SHA as the branch source.

### 7. Verify

Confirm:

```bash
git branch --show-current
git status --short --branch
```

When a remote branch was created or pushed, read the remote ref back.

## Git Flow Handling

Use Git Flow names such as `feature/`, `release/`, and `hotfix/` only when repository policy or the user explicitly requires Git Flow. Do not introduce a `develop` branch into a repository that does not use one.

## Safety Rules

- Never create work directly on a protected default branch when a task branch is expected
- Never discard or absorb unrelated dirty files
- Never force-update an existing remote branch without explicit authorization
- Never invent issue keys, usernames, or release versions
- Stop when the intended base cannot be resolved safely

## Completion

Report the created branch, exact base ref or SHA, local or remote location, and any preserved uncommitted work.
