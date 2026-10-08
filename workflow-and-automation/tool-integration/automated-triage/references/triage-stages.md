# Monte Carlo Triage Stages & Customization Guide

Detailed reference for customizing alert triage stages, filter criteria, and scoring thresholds.

## 1. Fetching Alerts
- Time window defaults: 3 hours for real-time monitoring; 24 hours for daily health checks.
- Filter criteria: `status: UNACKNOWLEDGED`, domain tags, table priority tiers.

## 2. Assessment & Scoring Matrix
- **Likelihood Scoring**: Evaluates anomaly deviation magnitude, historical query stability, and recurrence frequency.
- **Impact Scoring**: Evaluates downstream dashboard usage, lineage fan-out, and SLA tier.

## 3. Deep Troubleshooting
- Evaluates recent DDL changes, partition ingestion gaps, ETL job error logs, and upstream schema modifications.

## 4. Remediation Mapping
- Low Likelihood / Low Impact: Log recommendation or auto-resolve if transient noise.
- High Likelihood / High Impact: Escalate to on-call channel, declare severity incident, and assign domain owner.
