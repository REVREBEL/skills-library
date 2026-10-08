---
name: security-review
description: 'Review GitHub Actions workflows and local actions for exploitable security weaknesses involving untrusted triggers, token permissions, secrets, expression injection, privileged checkouts, third-party actions, artifacts, caches, and runners. Use when asked for a GitHub Actions security review or workflow hardening assessment.'
compatibility: 'Read-only by default. Requires access to workflow files, local actions, and referenced scripts. Applying fixes requires repository write access.'
metadata:
  category: github
  type: actions-security-review
  source: consolidated
---

# GitHub Actions Security Review

Report concrete, externally exploitable workflow risks. Do not inflate the report with theoretical patterns that cannot reach an impact.

## When to Use

Use when reviewing:

- `.github/workflows/*.yml` or `.yaml`
- local composite or JavaScript actions
- workflow-related shell or repository scripts
- token permissions and secret exposure
- fork PR, issue comment, or other untrusted event handling
- reusable workflow trust boundaries
- third-party action pinning and supply-chain risk
- self-hosted runners, caches, artifacts, and environments

## Threat Model

By default, model an external attacker without repository write access who can create fork pull requests, issues, comments, branch names in their fork, and other public GitHub content.

Expand the threat model only when the user requests insider, compromised-maintainer, or runner-host scenarios.

## Workflow

### 1. Inventory the attack surface

For each workflow record:

- triggers and filters
- token `permissions`
- secrets and environments
- checkout refs
- `run` steps and interpolated expressions
- third-party actions and pinning
- local actions and referenced scripts
- artifacts, caches, and self-hosted runners
- deployment or release capabilities

### 2. Trace attacker-controlled data

Follow untrusted values such as:

- PR titles, bodies, branch names, and labels
- issue and comment bodies
- fork-controlled files and scripts
- workflow inputs callable by less-trusted repositories
- artifact or cache contents from untrusted jobs

Trace the value from entry point to execution, credential access, write permission, or deployment impact.

### 3. Check high-risk classes

Review for:

- `pull_request_target` combined with fork checkout or execution
- attacker-controlled expressions interpolated into shell `run` blocks
- comment-triggered commands without authorization checks
- privileged tokens or long-lived credentials exposed to untrusted code
- local actions or configuration loaded from a PR checkout
- overbroad workflow or job permissions
- unpinned or compromised third-party actions
- artifact or cache poisoning across trust boundaries
- persistent compromise of self-hosted runners
- unsafe reusable workflow callers or secret inheritance

### 4. Confirm mitigations

Before reporting, check:

- event and branch filters
- `if` authorization conditions
- safe use of expressions through `env` or typed action inputs
- read-only token context
- environment approvals
- immutable action SHAs
- separate privileged and untrusted jobs
- sandboxing and runner cleanup

### 5. Grade confidence

Report only findings with a plausible attack path.

- **High:** complete entry-to-impact path confirmed
- **Medium:** material risk with one unresolved environmental dependency
- **Low:** theoretical or already mitigated, omit from findings and optionally note as hardening

### 6. Write each finding

Include:

- severity and confidence
- workflow and exact location
- attacker entry point
- payload or controlled value
- execution path
- impact and token or secret scope
- concrete remediation
- verification step

If the attack path cannot be explained, do not report it as a vulnerability.

## Safe Patterns That Need Context

Do not automatically flag:

- `pull_request_target` without fork checkout or untrusted execution
- expressions used in `if` or action `with` fields
- numeric PR identifiers
- schedule or manual inputs restricted to trusted writers
- GitHub-hosted runner use by itself
- secrets references that never reach untrusted jobs

## Completion

Return:

- reviewed workflow set
- findings ordered by severity
- needs-verification items
- reviewed-and-cleared high-risk areas
- hardening suggestions separated from exploitable findings
- limitations in repository or organization visibility
