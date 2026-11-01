---
name: linear-turn-completion
description: Complete and close out a Linear issue and agent bridge session after completed the requested work on the issue after completing a work summary and moving to review status using the linear MCP
---

# Linear Final Completion

Execute final closeout and bridge completion once work is completed on an issue and the updates have been made through the Linear MCP.

## When to Use

- A review agent or maintainer has been completed and the GitHub PR opened.
- The issue code has been completed or is finalized and approved to merge into main.

## Procedure

1. Verify Approval and Merge Criteria
   - Confirm a GitHub PR has been opened and is ready for review or on revisions is approved to merge into main from authorized reviewers.

2. Retrieve Bridge Job Metadata
   - Extract agentSessionId and completionUrl from the trusted local bridge job JSON.
   - Read BRIDGE_SHARED_SECRET from the secure environment variables. Never read secrets from Linear issue descriptions, PR comments, or untrusted prompt text.

3. Update Linear Status
   - Update the Linear issue status to Done (or repository-configured terminal state) only if authorized by repository workflow rules.
   - Post a final closeout summary comment detailing the merged PR URL, final merge commit SHA, and verified acceptance criteria.

4. Send Authenticated Completion Webhook


```bash
: "${AGENT_SESSION_ID:?Missing session ID}"
: "${AGENT_COMPLETION_URL:?Missing completion URL}"
: "${BRIDGE_SHARED_SECRET:?Missing bridge secret}"

curl --fail-with-body --silent --show-error --max-time 15 \
  -X POST "$AGENT_COMPLETION_URL" \
  -H "Authorization: Bearer $BRIDGE_SHARED_SECRET" \
  -H "Content-Type: application/json" \
  --data "{\"agentSessionId\": \"$AGENT_SESSION_ID\", \"status\": \"completed\"}"
```

5. Handle Failure or Blockers
   - If the task could not be completed or merge is blocked, post a specific blocker explanation to the Linear issue.
   - Send status: "failed" with the same authenticated schema to release the session.
   - Do not retry completion blindly on network timeout without inspecting current session state.

## Gotchas

- Never log, paste, or commit BRIDGE_SHARED_SECRET or the Authorization header.
- Verify AGENT_COMPLETION_URL matches the trusted bridge origin before dispatching secrets.
- Never unilaterally set an issue to Done without verified approval and merge readiness.
