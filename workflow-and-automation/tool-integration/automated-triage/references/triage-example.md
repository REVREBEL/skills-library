# Working Example: Monte Carlo Alert Triage Workflow

A complete end-to-end walkthrough for executing automated alert triage.

## Scenario: Daily Freshness Anomaly Triage

1. **Query Unacknowledged Alerts**:
   `get_alerts(time_window_hours=24, status="UNACKNOWLEDGED")`
2. **Execute Alert Assessment**:
   `alert_assessment(alert_ids=[...])`
3. **Inspect Output**:
   - Alert `freshness_prod_orders`: Likelihood=HIGH, Impact=HIGH
   - Alert `volume_staging_temp`: Likelihood=LOW, Impact=LOW
4. **Trigger Deep Troubleshooting**:
   `run_troubleshooting_agent(alert_id="freshness_prod_orders")`
5. **Post Triage Summary**:
   Post comment with root cause findings and notify data engineering on-call.
