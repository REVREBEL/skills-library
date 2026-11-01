---
name: linear-review-submissions
description: Submit verified Pull Requests to Linear issues for independent review. Use after code is pushed to GitHub, to post the structured Antigravity submission comment, update the Linear issue to In Review, and complete the agent bridge session.
---

# Linear Review Submissions

Handoff completed GitHub Pull Requests to Linear for peer and automated review. This skill enforces strict execution ordering: confirming pushed commits, posting the standardized ANTIGRAVITY SUBMISSION comment, moving the issue to In Review, and signaling agent session completion.

## When to Use

- Code has been pushed to GitHub and the PR URL and HEAD commit SHA are verified.
- Ready to hand off initial implementation or revision work for review.
- Do NOT use before code is pushed and verified on GitHub (use github-pr-submissions).
- After completing the steps below, follow the directions and use linear-turn-completion.
- If the code has been **approved to merge into main**, skip the below steps and move directly to the linear-final-completion skill.

## Procedure

1. Verify Prerequisites
   - Verify that the branch is pushed to remote and the PR exists on GitHub.
   - Retrieve the exact PR URL and the full remote HEAD commit SHA. Never use placeholder URLs or truncated commit hashes.

2. Post Linear Submission Comment
   - Post a comment on the active Linear issue using the exact submission format using the Linear MCP:

```markdown
**ANTIGRAVITY SUBMISSION**

- **Submission:** Initial / Revision
- **PR:** <verified PR URL>
- **Commit:** <actual head SHA>
- **Completed:** <brief implementation summary>
- **Acceptance criteria:** <met / unmet with evidence>
- **Validation:** <commands and actual results>
- **Open items:** <none or details>
- **Prior review:** <link, if revision>
```

3. Update Linear Issue Status
   - Move the Linear issue status to In Review and tag @CHATGPT on the comment for code review. 
   - Wait for the review to complete. It will indicate if revisions are need or if ready to merge into main. 


## Gotchas

- Order matters strictly: push code -> verify PR and SHA -> post Linear submission comment -> set issue to In Review -> signal session completion.
- Avoid redundant progress comments on Linear to prevent triggering bridge webhook loops.
- Do not mark the issue as Done. The agent transitions issues to In Review; review agents or human leads handle Done.
