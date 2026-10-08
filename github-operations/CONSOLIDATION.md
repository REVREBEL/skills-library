# GitHub Operations Consolidation

## Purpose

This record documents the consolidation of `task-skills/github-operations` from 31 discoverable child skills into 18 focused workflows.

The review compared each source skill by:

- trigger language
- primary user job
- required tools and environment
- expected output
- overlap with other workflows
- provider or organization coupling
- safety and validation behavior
- supporting files

Source history remains recoverable through Git.

## Active Workflows

### Core Git and Repository Operations

- `github`: general repository reads and small scoped mutations
- `create-branch`: safe branch creation using repository policy
- `commit`: local staging and commit creation
- `publish-changes`: end-to-end review, validation, commit, push, and PR creation
- `advanced-workflows`: rebase, cherry-pick, bisect, worktrees, reflog, and recovery
- `hooks-automation`: version-controlled local Git quality gates

### Issues and Feature Memory

- `issue-creator`: draft, create, or update actionable GitHub issues
- `create-issue-gate`: issue-first readiness and acceptance-criteria gate
- `feature-tracking`: repository-native long-lived feature memory

### Pull Requests

- `pr-writer`: create or update PR title and body
- `review-requests`: find and rank PRs awaiting review
- `pr-review`: review code and risk at a specific head SHA
- `pr-merge-champion`: verify merge gates and merge or queue an authorized PR

### GitHub Actions

- `actions-advanced`: create, update, and optimize Actions workflows
- `actions-debugger`: diagnose a specific failing or stuck run
- `security-review`: exploit-focused Actions security review

### Repository Discovery

- `presence`: human-facing README and repository discoverability
- `llms-maintain`: machine-facing `llms.txt` creation and maintenance

## Merge and Retirement Decisions

### Merged into canonical workflows

| Retired source | Final destination | Reason |
|---|---|---|
| `actions-templates` | `actions-advanced` | Same workflow-authoring job; source examples included unsupported and stale platform assumptions |
| `workflow-automation` | `actions-advanced` | Useful provider-neutral automation patterns belong in Actions authoring; Anthropic-specific implementation removed |
| `flow-branch-creator` | `create-branch` | Git Flow is one optional repository policy, not a separate universal branch workflow |
| `pushing` | `publish-changes` | Duplicated staging and commit behavior; publication now owns push and remote verification |
| `create-pr` | `pr-writer` | Alias only; no independent behavior |
| `pr-workflows-pr-enhance` | `pr-writer`, `pr-review`, and `publish-changes` | PR narrative, preflight, risk, and validation responsibilities now have explicit owners |
| `pr-workflows-workflow` | `publish-changes` | Strong end-to-end workflow retained under a clear functional name |
| `pr-merge-champion` source behavior | rewritten canonical `pr-merge-champion` | Previous content prepared PRs but did not safely perform merges |
| `llms-create` and `llms-update` | `llms-maintain` | Create and update modes share one natural repository-documentation workflow |
| `workflow-versioning` | `create-branch`, `commit`, `publish-changes`, and `advanced-workflows` | Broad principles duplicated the operational children and triggered on nearly every code change |
| `push-skill-to-github` | `publish-changes` | Environment-specific publication path duplicated the generic repository workflow |

### Retired as unsupported, unsafe, or unrelated

| Retired source | Reason |
|---|---|
| `automation` | Required Rube MCP and Composio-specific tools not part of the active GitHub stack |
| `image` | Required a third-party extension and full-account session cookie; plugin metadata marked Codex and Claude blocked |
| `global-chat-agent-discovery` | MCP marketplace discovery is not a GitHub repository-operation workflow |
| `pr-workflows-onboard` | Employee onboarding workflow mislabeled as a PR workflow |

## Corrected Semantic Mismatches

- `pr-review` previously generated PR descriptions; it now performs actual code and risk review.
- `review-requests` previously depended on a missing Sentry-specific script and hardcoded organization; it now builds a generic GitHub review queue.
- `issue-creator` previously wrote Markdown files under `/issues/`; it now creates or updates actual GitHub issues by default.
- `create-branch` previously imposed Sentry branch naming; it now follows discovered repository policy.
- `pr-writer` previously ignored repository PR templates; it now preserves required templates and checklists.
- `actions-debugger` previously depended mainly on pasted logs; it now resolves exact runs, jobs, steps, workflow definitions, and head SHAs.
- `security-review` previously referenced absent supporting files; it is now self-contained.

## Supporting Files

- `presence/README.md` remains as supporting project-presence documentation.
- `github/agents/openai.yaml` remains as connector or agent metadata.
- The retired `pushing/scripts/smart_commit.sh` and PR enhancement playbook remain recoverable through Git history.

## Final Boundaries

- MCP and connectors provide GitHub operations; skills provide workflow and safety.
- `github` is the general fallback, not a substitute for complete workflows.
- Local commit creation stops at `commit`; remote publication belongs to `publish-changes`.
- PR authoring, review queue, code review, and merge are separate jobs.
- Actions authoring, debugging, and security review are separate jobs.
- Human repository presence and machine-oriented `llms.txt` navigation are separate jobs.

## Deferred Review

- `feature-tracking` is retained unchanged because its repository-memory job is distinct, but it remains lengthy and could later be evaluated for progressive disclosure.
- `presence/README.md` may contain material duplicated by the rewritten `presence/SKILL.md`; a later supporting-file cleanup can compare unique content before removal.
- Runtime skill validation was not executed through the GitHub connector. Folder/frontmatter alignment and link existence should be checked by the repository validator when available.
