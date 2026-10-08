---
name: hooks-automation
description: 'Create, update, or troubleshoot version-controlled Git hook automation for linting, formatting, tests, secret checks, and commit-message validation. Use when asked to add pre-commit, commit-msg, pre-push, Husky, lint-staged, or pre-commit framework checks.'
compatibility: 'Requires Git and the repository runtime needed by the selected hook framework. Prefer repository-supported frameworks over local-only .git/hooks files.'
metadata:
  category: github
  type: git-hooks
  source: consolidated
---

# Git Hooks Automation

Add fast local quality gates that complement rather than replace CI.

## When to Use

Use for:

- pre-commit linting, formatting, or secret detection
- commit-message validation
- pre-push tests or type checks
- Husky and lint-staged configuration
- Python or polyglot `pre-commit` framework setup
- troubleshooting hooks that do not run consistently

Do not add hooks merely because they are fashionable. Use them when the repository benefits from fast, deterministic local feedback.

## Workflow

### 1. Inspect the repository

Determine:

- language and package manager
- existing hooks and configuration
- CI checks that should be mirrored locally
- supported operating systems
- acceptable hook runtime

Read existing files such as:

- `package.json`
- `.husky/`
- `.lintstagedrc*`
- `.pre-commit-config.yaml`
- commitlint configuration
- contribution documentation

### 2. Choose the smallest appropriate framework

- **Husky + lint-staged:** JavaScript or TypeScript repositories
- **pre-commit:** Python or polyglot repositories
- **repository script + core.hooksPath:** custom cross-language needs
- **local `.git/hooks`:** personal-only automation that should not be shared

Do not introduce multiple hook frameworks for the same job without a documented reason.

### 3. Define the gate

Each hook should have:

- a single clear purpose
- deterministic commands
- bounded runtime
- useful failure messages
- no hidden network or deployment side effects
- a documented bypass policy, when bypass is permitted

Prefer staged-file checks for pre-commit. Keep full test suites in pre-push or CI when they are slow.

### 4. Implement through repository scripts

Prefer hook files that call existing package or repository scripts rather than duplicating long command sequences.

Example Husky pre-commit:

```sh
npx lint-staged
```

Example pre-commit configuration:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: <pinned-version>
    hooks:
      - id: check-yaml
      - id: check-merge-conflict
      - id: detect-private-key
```

Pin third-party hook versions and review their source and permissions.

### 5. Test each hook directly

Run the underlying command first, then test the hook with representative pass and fail cases.

For `pre-commit`:

```bash
pre-commit run --all-files
```

For package scripts, run the exact command the hook invokes.

### 6. Verify team usability

Confirm:

- installation steps are documented
- CI still enforces critical checks
- hook paths work from the repository root
- shell syntax is portable for supported environments
- failure output tells contributors how to fix the problem

## Safety Rules

- Never place credentials in hook files or command arguments
- Never auto-commit or auto-push from a quality hook
- Never deploy, publish, or mutate remote state from pre-commit hooks
- Never silently rewrite broad file sets without showing the resulting diff
- Never make a hook depend on an undocumented local path
- Never disable existing hooks to make a commit pass without authorization

## Completion

Report:

- hook events configured
- framework and files changed
- commands executed
- pass and fail validation results
- installation or compatibility requirements
