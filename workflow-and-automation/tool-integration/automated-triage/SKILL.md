---
name: "automated-triage"
description: "Triage, assess, score, and troubleshoot Monte Carlo data reliability alerts interactively or via automated scheduled workflows using Monte Carlo MCP tools. Use when investigating data freshness delays, volume anomalies, or schema incidents."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Monte Carlo Automated Triage

Design, execute, and automate data reliability alert triage workflows using Monte Carlo Model Context Protocol (MCP) tools.

## When to Use

Use this skill when:
- Investigating recent Monte Carlo data observability alerts (freshness, volume, schema changes, SQL rules).
- Performing automated alert assessment to score incident likelihood and business impact (HIGH, MEDIUM, LOW).
- Running root-cause troubleshooting agents on high-signal data anomalies.
- Building scheduled triage automation workflows that post recommendations or update alert status.

Do not use this skill for:
- Writing raw database migration scripts (use database migration skills).
- General infrastructure metrics monitoring outside Monte Carlo (use observability skills).

## Prerequisites

- Monte Carlo MCP server configured and authenticated in agent environment.
- Available MCP tools: `get_alerts`, `alert_assessment`, `run_troubleshooting_agent`, `get_troubleshooting_agent_results`, `update_alert`, `set_alert_owner`, `create_or_update_alert_comment`, `mark_event_as_normal`.

## Triage Workflow

### 1. Fetch & Filter Inbound Alerts
Call `get_alerts` with a targeted time window and optional status filter:
- Retrieve unacknowledged alerts from the last 3–24 hours.
- Filter by domain or table criticality if specified by the user.

### 2. Initial Assessment & Scoring
Execute `alert_assessment` across retrieved alerts to obtain structured scoring:
- **Incident Likelihood**: `HIGH` | `MEDIUM` | `LOW`
- **Potential Impact**: `HIGH` | `MEDIUM` | `LOW`

### 3. Deep Troubleshooting (High-Signal Alerts)
For alerts where both likelihood and impact are `MEDIUM` or `HIGH`:
- Invoke `run_troubleshooting_agent` with the alert identifier.
- Retrieve asynchronous analysis results via `get_troubleshooting_agent_results`.
- Extract upstream lineage changes, query failures, or anomalous volume shifts.

### 4. Determine Actions & Remediation
- **Recommendation Mode (Default)**: Post draft findings and recommended actions in comments without applying destructive mutations.
- **Action Mode (Verified / Approved)**: Update alert status via `update_alert`, assign incident owner via `set_alert_owner`, or calibrate thresholds via `mark_event_as_normal`.

## Supporting Reference Guides

- [Triage Stages & Customization Guide](./references/triage-stages.md): Detailed stage-by-stage configuration, threshold tuning, and filter parameters.
- [Working Triage Example Workflow](./references/triage-example.md): Walkthrough of end-to-end alert assessment and automated reporting.

## Safety & Governance

- **Action Guard**: Default to read-only recommendation mode during workflow development and testing.
- Obtain explicit confirmation before updating production alert status, declaring high-severity incidents, or suppressing alert monitors.

## Completion Evidence

- Summary report detailing alerts evaluated, assigned scores, and root-cause summaries.
- Exported triage workflow definition or audit record of alert comments posted.
