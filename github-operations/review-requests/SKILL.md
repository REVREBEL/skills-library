---
name: review-requests
description: 'Find and triage GitHub pull requests awaiting review from the authenticated user, a named reviewer, or a team. Use when asked what needs review, to show pending review requests, build a review queue, or identify stale requested reviews.'
compatibility: 'Requires authenticated GitHub access and permission to view the target repositories or organization teams.'
metadata:
  category: github
  type: review-queue
  source: consolidated
---

# Pull Request Review Queue

Build a current, deduplicated queue of pull requests that need review.

## When to Use

Use when the user asks:

- what PRs need my review?
- show pending review requests
- find PRs assigned to this team
- identify stale or blocked reviews
- summarize the current review queue

Use `pr-review` to analyze one selected pull request.

## Workflow

### 1. Resolve the reviewer scope

Identify one of:

- authenticated user
- named GitHub login
- organization team slug
- repository or organization scope

Do not assume a hardcoded organization or team.

### 2. Query current PR state

Prefer GitHub MCP or the connected GitHub app. When using `gh`, query review-request and PR data through supported search or API endpoints.

Include only pull requests that are:

- open
- not merged
- currently requesting the user or team's review, or explicitly assigned for review by repository policy

Distinguish requested review from authored, mentioned, assigned, or merely subscribed PRs.

### 3. Gather useful triage context

For each PR capture:

- repository and PR number
- title and URL
- author
- requested reviewer or team
- draft state
- age and last update
- changed-file or diff size when available
- check status
- existing review state
- merge conflicts or blockers

Paginate until the requested scope is complete.

### 4. Rank the queue

Prioritize using transparent signals such as:

1. security or production urgency
2. explicit due date or release blocker
3. ready-for-review with green checks
4. oldest unanswered request
5. smaller unblocked reviews before large or draft work

Do not invent urgency from labels or titles without evidence.

### 5. Present the queue

Use a compact table or grouped summary. Flag:

- draft PRs
- failed or pending checks
- stale requests
- already reviewed but re-requested after new commits
- PRs where the current head changed after the last review

### 6. Verify selected items

Before handing a PR to `pr-review`, refresh its current head SHA and review-request state.

## Completion

Return the total queue, ranking method, repository scope, and the top items with URLs and blockers. Say explicitly when no current review requests were found.
