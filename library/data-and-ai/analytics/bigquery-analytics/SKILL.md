---
name: "bigquery-analytics"
description: "Use this skill when the user asks about \\\"BigQuery\\\", \\\"analytics queries\\\", \\\"data warehouse\\\", \\\"partitioning\\\", \\\"clustering\\\", \\\"SQL queries\\\", or any BigQuery-related work. Covers BigQuery setup and basics (bq CLI, datasets, tables, queries), table design, query optimization, Node.js integration patterns, cost control, and BigQuery ML / Gemini AI functions. Use when working with bigquery analytics."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# BigQuery Analytics & Basics

BigQuery is a serverless, AI-ready data platform for high-speed analysis of large datasets using SQL and Python. Its disaggregated architecture separates compute and storage, allowing them to scale independently while providing built-in machine learning, geospatial analysis, and business intelligence capabilities.

## Getting Started

1. **Enable the BigQuery API:**

   ```bash
   gcloud services enable bigquery.googleapis.com
   ```

2. **Create a dataset:**

   ```bash
   bq mk --dataset --location=US my_dataset
   ```

3. **Create a table** — write a `schema.json`:

   ```json
   [
     { "name": "name", "type": "STRING", "mode": "REQUIRED" },
     { "name": "post_abbr", "type": "STRING", "mode": "NULLABLE" }
   ]
   ```

   ```bash
   bq mk --table my_dataset.mytable schema.json
   ```

4. **Run a query:**

   ```bash
   bq query --use_legacy_sql=false \
     'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` \
      WHERE state = "TX" LIMIT 10'
   ```

Reference material (if present in the skill): core concepts (storage types, analytics workflows, BigQuery Studio), CLI usage, client libraries (Python, Java, Node.js, Go), MCP usage (BigQuery remote MCP server + Gemini CLI extension), IaC (Terraform for datasets/tables/reservations), IAM & security (roles, permissions, governance). If product information is missing, use the Developer Knowledge MCP server `search_documents` tool.

## Table Design

### Partitioning (REQUIRED for tables > 1GB)

```sql
CREATE TABLE `project.dataset.events` (
  event_id STRING,
  shop_id STRING,
  event_type STRING,
  created_at TIMESTAMP,
  data JSON
)
PARTITION BY DATE(created_at)
CLUSTER BY shop_id, event_type;
```

| Data Size | Partition By |
|-----------|--------------|
| < 1GB | Not needed |
| 1GB - 1TB | DATE/TIMESTAMP |
| > 1TB | DATE + consider sharding |

---

## Query Patterns

### Always Use Partition Filter

```sql
-- ❌ BAD: No partition filter (full scan)
SELECT * FROM events WHERE shop_id = 'shop_123';

-- ✅ GOOD: Partition filter included
SELECT * FROM events
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-02-01'
  AND shop_id = 'shop_123';
```

### Select Only Needed Columns

```sql
-- ❌ BAD: SELECT *
SELECT * FROM events;

-- ✅ GOOD: Select specific columns
SELECT event_id, event_type, created_at FROM events;
```

---

## Node.js Integration

### Always Batch Inserts

```javascript
// ✅ GOOD: Single batch insert
await table.insert(batch.map(row => ({
  ...row,
  time: new Date()
})));

// ❌ BAD: Insert one row at a time
for (const row of batch) {
  await table.insert([row]);
}
```

| Scenario | Max Batch Size |
|----------|----------------|
| Streaming inserts | 500-1000 rows |
| High throughput | Up to 10,000 rows |

---

## Cost Control

```javascript
// Dry run before expensive queries
const [job] = await bigquery.createQueryJob({
  query: sql,
  dryRun: true
});
const estimatedCost = (job.statistics.totalBytesProcessed / 1e12) * 5;
```

---

## BigQuery AI & ML

BigQuery ML and Gemini bring AI into SQL. Key `AI_*` functions (see the BigQuery AI & ML skill references for full syntax):

- `AI.GENERATE` / `AI.GENERATE_BOOL` / `AI.GENERATE_DOUBLE` / `AI.GENERATE_INT` — generate text or structured values from a prompt.
- `AI.IF` — conditional logic over generated content.
- `AI.SCORE` — score how well a document matches a query.
- `AI.SIMILARITY` / `AI.SEARCH` — semantic similarity and vector search.
- `AI.CLASSIFY` — classify rows into labels.
- `AI.FORECAST` — time-series forecasting.
- `AI.DETECT_ANOMALIES` — anomaly detection.

Related skill: [BigQuery AI & ML](https://github.com/google/adk-python/tree/main/src/google/adk/tools/bigquery/skills/bigquery-ai-ml) with references for `bigquery_ai_classify.md`, `bigquery_ai_detect_anomalies.md`, `bigquery_ai_forecast.md`, `bigquery_ai_generate*.md`, `bigquery_ai_if.md`, `bigquery_ai_score.md`, `bigquery_ai_search.md`, `bigquery_ai_similarity.md`.

## Checklist

```
□ Large tables (>1GB) have partitioning
□ Queries include partition column in WHERE
□ Tables clustered by frequently filtered columns
□ No SELECT * - select specific columns
□ Using parameterized queries
□ Batch inserts (not row-by-row)
```

## Merged from

- `bigquery-basics` — BigQuery setup and basic usage (bq CLI, datasets, tables, queries), overview, reference directory, BigQuery AI & ML function index
