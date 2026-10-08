---
name: actions-advanced
description: 'Create, update, optimize, or modernize GitHub Actions workflows for testing, building, deployment, release, issue triage, and repository automation. Use when working with .github/workflows, reusable workflows, matrices, caching, artifacts, environments, OIDC, permissions, or workflow orchestration.'
compatibility: 'Requires repository write access to modify workflow files. Live validation requires permission to push or dispatch GitHub Actions runs.'
metadata:
  category: github
  type: actions-authoring
  source: consolidated
---

# GitHub Actions Workflows

Design secure, maintainable Actions workflows that fit the repository's actual stack and delivery model.

## When to Use

Use when the user wants to:

- add or change CI checks
- automate tests, builds, deployments, or releases
- create reusable workflows or composite actions
- configure matrices, caching, artifacts, concurrency, or environments
- add issue or PR automation through Actions
- migrate deprecated action versions or workflow syntax
- improve workflow performance or maintainability

Use `actions-debugger` for a failing run and `security-review` for an exploit-focused security assessment.

## Control and Handoff

Keep control in `actions-advanced` while designing, editing, validating, and documenting the workflow change.

- Use `github` for repository reads and narrowly scoped workflow-file mutations, then return here to continue authoring and validation.
- Hand control back to `github` when the workflow change is complete and the new request is only a separate repository query or metadata operation.
- Hand off to `actions-debugger` when a published workflow run fails or stalls. Return here only when the diagnosis requires a workflow design change.
- Hand off to `security-review` for an independent exploit-focused assessment of privileged or externally triggered workflows.
- Use `publish-changes` when the workflow edits are ready to move through commit, push, PR creation, and remote verification. Do not duplicate that publication sequence here.

## Workflow

### 1. Inspect repository context

Read:

- existing `.github/workflows/*.yml` and `.yaml`
- local composite actions
- package manifests and supported runtimes
- deployment and release documentation
- branch protection and required checks
- existing secret, environment, or OIDC conventions

Do not introduce AWS, Kubernetes, Windows, or another platform unless the repository actually uses it or the user requests it.

### 2. Define the workflow contract

Resolve:

- events and branch or path filters
- required jobs and dependencies
- runner operating systems and versions
- inputs, outputs, secrets, and environments
- permissions and approval gates
- artifacts, caches, and retention
- failure, retry, and concurrency behavior
- success evidence

### 3. Apply secure defaults

- declare least-privilege `permissions`
- pin third-party actions to reviewed immutable SHAs when repository policy requires it
- set `timeout-minutes`
- use `concurrency` where duplicate runs waste resources or create deployment races
- keep untrusted data out of shell-expanded `run` commands
- avoid checking out fork code in privileged `pull_request_target` workflows
- prefer OIDC or short-lived credentials over long-lived cloud keys
- isolate deployment jobs behind GitHub Environments when approvals are needed

### 4. Keep workflows composable

Use reusable workflows for repeated multi-job pipelines and composite actions for repeated step sequences.

Avoid one enormous workflow that combines unrelated validation, deployment, release, and maintenance behavior.

### 5. Implement from repository scripts

Prefer workflows that call tested repository scripts or package commands rather than duplicating complex shell logic in YAML.

Use expressions in `if`, `with`, or `env` deliberately. Quote shell values and write multiline outputs through supported environment files.

### 6. Optimize execution

Use:

- dependency caches with precise keys
- job outputs and `needs`
- matrices only for supported combinations
- path filters when they do not hide required checks
- artifacts for handoff between isolated jobs
- fail-fast behavior appropriate to the matrix
- pinned runner images when reproducibility matters

## Minimal Secure Patterns

These examples demonstrate structure, not universal project commands. Confirm the repository's supported runtime and refresh the immutable action SHAs against its approved versions before copying them.

### Typical Node.js CI

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  verify:
    runs-on: ubuntu-24.04
    timeout-minutes: 15

    steps:
      - name: Check out repository
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
        with:
          persist-credentials: false

      - name: Set up Node.js
        uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: '22'
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint --if-present

      - name: Test
        run: npm test
```

This pattern keeps the token read-only, prevents checkout from persisting credentials, cancels superseded runs, caches npm data through `setup-node`, and pins third-party actions to immutable commits.

### Reusable Verification Workflow

```yaml
name: Reusable verification

on:
  workflow_call:
    inputs:
      node-version:
        description: Node.js version to test
        required: false
        default: '22'
        type: string

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-24.04
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
        with:
          persist-credentials: false

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm

      - run: npm ci
      - run: npm test
```

Call the reusable workflow from another workflow with a local path:

```yaml
jobs:
  verify:
    uses: ./.github/workflows/_verify.yml
    with:
      node-version: '22'
```

Do not pass secrets to a reusable workflow unless it genuinely requires them. Declare each required secret explicitly rather than using broad inheritance by default.

### 7. Validate locally and remotely

Validate syntax and referenced scripts. Run available workflow linters such as `actionlint` when the repository supports them.

After publication, verify a real run or dispatch when authorized. Read job and step status rather than assuming the YAML is valid.

## Automation Boundaries

Provider-neutral issue triage, PR labeling, release notes, and scheduled maintenance may live in Actions. Do not hardcode a particular AI provider, model, or secret into a generic workflow. Treat AI-generated issue or PR content as untrusted and require bounded permissions.

## Completion

Report:

- workflows and triggers added or changed
- permissions and secret requirements
- validation run
- live run status, when available
- deployment or release actions that remain intentionally unexecuted
