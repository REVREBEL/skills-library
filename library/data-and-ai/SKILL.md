---
name: data-and-ai
description: Category router for data-and-ai, dispatching 134 canonical skills across 5 subcategories.
type: category-router
version: 1.0.0
---

# Data And Ai Router

## Overview

The `data-and-ai` domain covers **134 active canonical skills** organized under 5 specialized subcategories.

## When to Use

Use this router when the user request involves data engineering, analytics, machine learning, llm/rag pipelines, and vector databases.

## Scope Boundaries & Handoffs

- Return to [Root Router](../SKILL.md) if the task falls outside this domain.

## Subcategory Routing Index

### Analytics

Manage 36 skills for analytics.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`analytics-insights`](analytics/analytics-insights/SKILL.md) | Analyze marketing performance. Use when: KPI frameworks, attribution modeling, anomaly investigation, measurement strategy. | Analytics Insights: Analyze marketing performance. Use when: KPI frameworks, attribution modeling, ano... |
| [`analytics-tracking`](analytics/analytics-tracking/SKILL.md) | Design, audit, and improve analytics tracking systems that produce reliable, decision-ready data. Use when working with analytics tracking. | Analytics Tracking: Design, audit, and improve analytics tracking systems that produce reliable, decis... |
| [`bigquery-analytics`](analytics/bigquery-analytics/SKILL.md) | Use this skill when the user asks about \\\"BigQuery\\\", \\\"analytics queries\\\", \\\"data warehouse\\\", \\\"partitioning\\\", \\\"clustering\\\", \\\"SQ... | Bigquery Analytics: the user asks about \\\"BigQuery\\\", \\\"analytics queries\\\", \\\"data warehous... |
| [`business-analyst`](analytics/business-analyst/SKILL.md) | Master modern business analysis with AI-powered analytics, real-time dashboards, and data-driven insights. Build comprehensive KPI frameworks, predictive mod... | Business Analyst: Master modern business analysis with AI-powered analytics, real-time dashboards, a... |
| [`business-analytics-reporter`](analytics/business-analytics-reporter/SKILL.md) | This skill should be used when analyzing business sales and revenue data from CSV files to identify weak areas, generate statistical insights, and provide strategic improvement recommendations. Use when the user requests a business performance report, asks to analyze sales data, wants to identify areas of weakness, or needs recommendations on business improvement strategies. | Business Analytics Reporter: This skill should be used when analyzing business sales and revenue data from CSV files to identify weak areas... |
| [`xlsx`](analytics/xlsx/SKILL.md) | Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas. Use when working with xlsx. | Xlsx: Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis... |
| [`cash-flow-forecasting`](analytics/cash-flow-forecasting/SKILL.md) | Forecast cash flow using historical sales patterns, payment terms, seasonal trends, and receivables modeling with scenario planning and runway tracking. Use ... | Cash Flow Forecasting: Forecast cash flow using historical sales patterns, payment terms, seasonal trends... |
| [`cc-skill-clickhouse-io`](analytics/cc-skill-clickhouse-io/SKILL.md) | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. Use when working ... | Cc Skill Clickhouse Io: ClickHouse database patterns, query optimization, analytics, and data engineering ... |
| [`churn-risk`](analytics/churn-risk/SKILL.md) | Assess customer churn risk. Use when: churn scoring, at-risk segment identification, intervention playbook generation. | Churn Risk: Assess customer churn risk. Use when: churn scoring, at-risk segment identificatio... |
| [`cohort-analysis`](analytics/cohort-analysis/SKILL.md) | Analyze customer cohorts. Use when: acquisition cohorts, retention curves, LTV by cohort, behavioral segmentation. | Cohort Analysis: Analyze customer cohorts. Use when: acquisition cohorts, retention curves, LTV by ... |
| [`data-scientist`](analytics/data-scientist/SKILL.md) | Expert data scientist for advanced analytics, machine learning, and statistical modeling. Handles complex data analysis, predictive modeling, and business in... | Data Scientist: Expert data scientist for advanced analytics, machine learning, and statistical mo... |
| [`data-storytelling`](analytics/data-storytelling/SKILL.md) | Transform raw data into compelling narratives that drive decisions and inspire action. Use when working with data storytelling. | Data Storytelling: Transform raw data into compelling narratives that drive decisions and inspire act... |
| [`ecommerce-budgeting-forecasting`](analytics/ecommerce-budgeting-forecasting/SKILL.md) | Build rolling operating budgets for marketing spend, inventory purchases, and operations with variance analysis, scenario modeling, and budget utilization al... | Ecommerce Budgeting Forecasting: Build rolling operating budgets for marketing spend, inventory purchases, and oper... |
| [`ecommerce-data-warehouse`](analytics/ecommerce-data-warehouse/SKILL.md) | Build a commerce data warehouse with star-schema tables, ETL pipelines, and dbt models for BigQuery, Snowflake, or Redshift analytics. Use when working with ... | Ecommerce Data Warehouse: Build a commerce data warehouse with star-schema tables, ETL pipelines, and dbt mo... |
| [`financial-analytics-dashboard`](analytics/financial-analytics-dashboard/SKILL.md) | Build interactive financial KPI dashboards with customizable metrics, drill-down analysis, variance explanations, and automated threshold-based alerting. Use... | Financial Analytics Dashboard: Build interactive financial KPI dashboards with customizable metrics, drill-down a... |
| [`lifecycle-marketing-automation`](analytics/lifecycle-marketing-automation/SKILL.md) | Map customer journey stages from first visit to loyal advocate with personalized messaging, triggered workflows, and segment-based campaign automation. Use w... | Lifecycle Marketing Automation: Map customer journey stages from first visit to loyal advocate with personalized m... |
| [`marketplace-fee-reconciliation`](analytics/marketplace-fee-reconciliation/SKILL.md) | Reconcile and analyze seller fees from Amazon, eBay, Walmart, and Etsy with net revenue calculation, fee categorization, and optimization recommendations. Us... | Marketplace Fee Reconciliation: Reconcile and analyze seller fees from Amazon, eBay, Walmart, and Etsy with net re... |
| [`posthog-automation`](analytics/posthog-automation/SKILL.md) | Automate PostHog tasks via Rube MCP (Composio): events, feature flags, projects, user profiles, annotations. Always search tools first for current schemas. U... | Posthog Automation: Automate PostHog tasks via Rube MCP (Composio): events, feature flags, projects, u... |
| [`product-analytics`](analytics/product-analytics/SKILL.md) | Track product performance with sell-through rates, views-to-purchase conversion, dead stock identification, and category-level reporting. Use when working wi... | Product Analytics: Track product performance with sell-through rates, views-to-purchase conversion, d... |
| [`profit-margin-analysis`](analytics/profit-margin-analysis/SKILL.md) | Analyze gross and net profit margins by product, category, channel, and customer segment with cost attribution, benchmarking, and trend visualization. Use wh... | Profit Margin Analysis: Analyze gross and net profit margins by product, category, channel, and customer s... |
| [`segment-cdp`](analytics/segment-cdp/SKILL.md) | Expert patterns for Segment Customer Data Platform including. Use when working with segment cdp. | Segment Cdp: Expert patterns for Segment Customer Data Platform including. Use when working wit... |
| [`statsmodels`](../marketing-and-seo/cro/statsmodels/SKILL.md) | Statsmodels is Python's premier library for statistical modeling, providing tools for estimation, inference, and diagnostics across a wide range of statistic... | Statsmodels: Statsmodels is Python's premier library for statistical modeling, providing tools ... |
| [`unit-economics-tracking`](analytics/unit-economics-tracking/SKILL.md) | Track customer acquisition cost, lifetime value, payback period, and contribution margin by cohort and channel with profitability benchmarks and trend analys... | Unit Economics Tracking: Track customer acquisition cost, lifetime value, payback period, and contribution ... |

### Data Engineering

Manage 10 skills for data engineering.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`bigquery-query-optimization`](../development/backend/bigquery-query-optimization/SKILL.md) | Use when writing BigQuery queries, optimizing query performance, analyzing execution plans, or avoiding common SQL gotchas. Covers parameterized queries, UDF... | Bigquery Query Optimization: writing BigQuery queries, optimizing query performance, analyzing execution plans,... |
| [`bigquery-table-creator`](../infrastructure-and-ops/cloud-platforms/bigquery-table-creator/SKILL.md) | Execute bigquery-table-creator tasks, workflows, and automated procedures. Use when working with bigquery table creator. | Bigquery Table Creator: Execute bigquery-table-creator tasks, workflows, and automated procedures. Use whe... |
| [`bigquery-view-generator`](../infrastructure-and-ops/cloud-platforms/bigquery-view-generator/SKILL.md) | Execute bigquery-view-generator tasks, workflows, and automated procedures. Use when working with bigquery view generator. | Bigquery View Generator: Execute bigquery-view-generator tasks, workflows, and automated procedures. Use wh... |
| [`data-quality-frameworks`](../business-and-operations/legal-and-governance/data-quality-frameworks/SKILL.md) | Implement data quality assertions, schema validation, and pipeline monitoring frameworks. Use when building automated data quality checks or profiling data p... | Data Quality Frameworks: Implement data quality assertions, schema validation, and pipeline monitoring fram... |
| [`mlops-engineer`](data-engineering/mlops-engineer/SKILL.md) | Build comprehensive ML pipelines, experiment tracking, and model registries with MLflow, Kubeflow, and modern MLOps tools. Use when working with mlops engineer. | Mlops Engineer: Build comprehensive ML pipelines, experiment tracking, and model registries with M... |
| [`recsys-pipeline-architect`](data-engineering/recsys-pipeline-architect/SKILL.md) | Designs composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework. Use when work... | Recsys Pipeline Architect: Designs composable recommendation, ranking, and feed pipelines using the six-stage... |
| [`scikit-learn`](data-engineering/scikit-learn/SKILL.md) | Machine learning in Python with scikit-learn. Use for classification, regression, clustering, model evaluation, and ML pipelines. Use when working with sciki... | Scikit Learn: Machine learning in Python with scikit-learn. Use for classification, regression, ... |

### Llm And Rag

Manage 55 skills for llm and rag.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`advanced-evaluation`](llm-and-rag/advanced-evaluation/SKILL.md) | This skill should be used when the user asks to \\\"implement LLM-as-judge\\\", \\\"compare model outputs\\\", \\\"create evaluation rubrics\\\", \\\"mitigat... | Advanced Evaluation: This skill should be used when the user asks to \\\"implement LLM-as-judge\\\", \\... |
| [`audio-transcriber`](llm-and-rag/audio-transcriber/SKILL.md) | Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration. Use when working with audio transcriber. | Audio Transcriber: Transform audio recordings into professional Markdown documentation with intellige... |
| [`ce-optimize`](../design-and-experience/ui-ux/ce-optimize/SKILL.md) | Run metric-driven iterative optimization loops -- define a measurable goal, run parallel experiments, measure each against hard gates or LLM-as-judge scores,... | Ce Optimize: Run metric-driven iterative optimization loops -- define a measurable goal, run pa... |
| [`clarity-gate`](llm-and-rag/clarity-gate/SKILL.md) | Execute clarity-gate tasks, workflows, and automated procedures. Use when working with clarity gate. | Clarity Gate: Execute clarity-gate tasks, workflows, and automated procedures. Use when working ... |
| [`earllm-build`](llm-and-rag/earllm-build/SKILL.md) | Build, maintain, and extend the EarLLM One Android project — a Kotlin/Compose app that connects Bluetooth earbuds to an LLM via voice pipeline. Use when work... | Earllm Build: Build, maintain, and extend the EarLLM One Android project — a Kotlin/Compose app ... |
| [`huggingface-spaces`](../quality-and-security/debugging/huggingface-spaces/SKILL.md) | Build, deploy, and maintain applications on Hugging Face Spaces — Gradio / Docker / Static SDKs, ZeroGPU and dedicated hardware, model loading, debugging, bu... | Huggingface Spaces: Build, deploy, and maintain applications on Hugging Face Spaces — Gradio / Docker ... |
| [`infinite-gratitude`](llm-and-rag/infinite-gratitude/SKILL.md) | Multi-agent research skill for parallel research execution (10 agents, battle-tested with real case studies). Use when working with infinite gratitude. | Infinite Gratitude: Multi-agent research skill for parallel research execution (10 agents, battle-test... |
| [`langgraph`](llm-and-rag/langgraph/SKILL.md) | Expert in LangGraph - the production-grade framework for building. Use when working with langgraph. | Langgraph: LangGraph - the production-grade framework for building. Use when working with lan... |
| [`llm-council`](llm-and-rag/llm-council/SKILL.md) | Run Fireworks-hosted open-weight model councils that compare responses and synthesize a final answer. Use when working with llm council. | Llm Council: Run Fireworks-hosted open-weight model councils that compare responses and synthes... |
| [`local-llm-expert`](llm-and-rag/local-llm-expert/SKILL.md) | Master local LLM inference, model selection, VRAM optimization, and local deployment using Ollama, llama.cpp, vLLM, and LM Studio. Expert in quantization for... | Local Llm Expert: Master local LLM inference, model selection, VRAM optimization, and local deployme... |
| [`mcp-builder`](llm-and-rag/mcp-builder/SKILL.md) | Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is ... | Mcp Builder: Create MCP (Model Context Protocol) servers that enable LLMs to interact with exte... |
| [`project-development`](llm-and-rag/project-development/SKILL.md) | This skill covers the principles for identifying tasks suited to LLM processing, designing effective project architectures, and iterating rapidly using agent... | Project Development: This skill covers the principles for identifying tasks suited to LLM processing, d... |
| [`prompt-engineering-patterns`](llm-and-rag/prompt-engineering-patterns/SKILL.md) | Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability. Use when working with prompt engineering patterns. | Prompt Engineering Patterns: Master advanced prompt engineering techniques to maximize LLM performance, reliabi... |
| [`quant-analyst`](llm-and-rag/quant-analyst/SKILL.md) | Build financial models, backtest trading strategies, and analyze market data. Implements risk metrics, portfolio optimization, and statistical arbitrage. Use... | Quant Analyst: Build financial models, backtest trading strategies, and analyze market data. Impl... |
| [`rag-implementation`](llm-and-rag/rag-implementation/SKILL.md) | RAG (Retrieval-Augmented Generation) implementation workflow covering embedding selection, vector database setup, chunking strategies, and retrieval optimiza... | Rag Implementation: RAG (Retrieval-Augmented Generation) implementation workflow covering embedding se... |
| [`routerbase-model-gateway`](llm-and-rag/routerbase-model-gateway/SKILL.md) | Integrate RouterBase as an OpenAI-compatible model gateway for routing GPT, Claude, Gemini, media, audio, and embedding requests. Use when working with route... | Routerbase Model Gateway: Integrate RouterBase as an OpenAI-compatible model gateway for routing GPT, Claude... |
| [`train-sentence-transformers`](../marketing-and-seo/cro/train-sentence-transformers/SKILL.md) | Train or fine-tune sentence-transformers models across `SentenceTransformer` (bi-encoder; dense or static embedding model; for retrieval, similarity, cluster... | Train Sentence Transformers: Train or fine-tune sentence-transformers models across `SentenceTransformer` (bi-e... |

### Machine Learning

Manage 28 skills for machine learning.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`ai-wrapper-product`](machine-learning/ai-wrapper-product/SKILL.md) | Expert in building products that wrap AI APIs (OpenAI, Anthropic,. Use when working with ai wrapper product. | Ai Wrapper Product: building products that wrap AI APIs (OpenAI, Anthropic,. Use when working with ai ... |
| [`computer-use-agents`](machine-learning/computer-use-agents/SKILL.md) | Build AI agents that interact with computers like humans do -. Use when working with computer use agents. | Computer Use Agents: Build AI agents that interact with computers like humans do -. Use when working wi... |
| [`exa-search`](machine-learning/exa-search/SKILL.md) | Semantic search, similar content discovery, and structured research using Exa API. Use when you need semantic/embeddings-based search, finding similar conten... | Exa Search: Semantic search, similar content discovery, and structured research using Exa API.... |
| [`gemini-api`](machine-learning/gemini-api/SKILL.md) | Guides the usage of the Gemini API on Agent Platform with the Google Gen AI SDK. Use when the user asks about using Gemini in an enterprise environment or ex... | Gemini Api: the usage of the Gemini API on Agent Platform with the Google Gen AI SDK. Use when... |
| [`hugging-face-cli`](machine-learning/hugging-face-cli/SKILL.md) | Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more on the Hugging Face Hub... | Hugging Face Cli: Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datas... |
| [`hugging-face-gradio`](machine-learning/hugging-face-gradio/SKILL.md) | Build Gradio web UIs and demos in Python. Use when creating or editing Gradio apps, components, event listeners, layouts, or chatbots. | Hugging Face Gradio: Build Gradio web UIs and demos in Python. Use when creating or editing Gradio apps... |
| [`hugging-face-model-trainer`](machine-learning/hugging-face-model-trainer/SKILL.md) | Train or fine-tune language and vision models using TRL (Transformer Reinforcement Learning) or Unsloth with Hugging Face Jobs infrastructure. Covers SFT, DP... | Hugging Face Model Trainer: Train or fine-tune language and vision models using TRL (Transformer Reinforcement... |
| [`hugging-face-papers`](machine-learning/hugging-face-papers/SKILL.md) | Look up and read Hugging Face paper pages in markdown, and use the papers API for structured metadata such as authors, linked models/datasets/spaces, Github ... | Hugging Face Papers: Look up and read Hugging Face paper pages in markdown, and use the papers API for ... |
| [`hugging-face-trackio`](machine-learning/hugging-face-trackio/SKILL.md) | Track and visualize ML training experiments with Trackio. Use when logging metrics during training (Python API), firing alerts for training diagnostics, or r... | Hugging Face Trackio: Track and visualize ML training experiments with Trackio. Use when logging metrics... |
| [`huggingface-tool-builder`](machine-learning/huggingface-tool-builder/SKILL.md) | Use this skill when the user wants to build tool/scripts or achieve a task where using data from the Hugging Face API would help. This is especially useful w... | Huggingface Tool Builder: the user wants to build tool/scripts or achieve a task where using data from the H... |
| [`ml-engineer`](../quality-and-security/testing/ml-engineer/SKILL.md) | Build production ML systems with PyTorch 2.x, TensorFlow, and modern ML frameworks. Implements model serving, feature engineering, A/B testing, and monitorin... | Ml Engineer: Build production ML systems with PyTorch 2.x, TensorFlow, and modern ML frameworks... |
| [`transformers-js`](machine-learning/transformers-js/SKILL.md) | Use Transformers.js to run state-of-the-art machine learning models directly in JavaScript/TypeScript. Supports NLP (text classification, translation, summar... | Transformers Js: Use Transformers.js to run state-of-the-art machine learning models directly in Ja... |

### Vector Databases

Manage 5 skills for vector databases.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`arrowspace`](vector-databases/arrowspace/SKILL.md) | Spectral vector search using graph Laplacian eigenstructure. Use when cosine/L2 similarity misses latent structure in your embeddings. | Arrowspace: Spectral vector search using graph Laplacian eigenstructure. Use when cosine/L2 si... |
| [`embedding-strategies`](vector-databases/embedding-strategies/SKILL.md) | Guide to selecting and optimizing embedding models for vector search applications. Use when working with embedding strategies. | Embedding Strategies: to selecting and optimizing embedding models for vector search applications. Use w... |
| [`weaviate`](vector-databases/weaviate/SKILL.md) | Search, query, inspect, create, and import data into Weaviate vector database collections using official scripts and references. Use when working with weaviate. | Weaviate: Search, query, inspect, create, and import data into Weaviate vector database coll... |

---
*Part of the Canonical Agent Skills Hierarchy.*
- [`computer-vision-expert`](machine-learning/computer-vision-expert/SKILL.md) — Computer vision and model training expertise.
- [`hugging-face-vision-trainer`](machine-learning/hugging-face-vision-trainer/SKILL.md) — Hugging Face vision model training workflow.
- [`context-manager`](../development/fullstack/context-manager/SKILL.md) — Context management for LLM applications.
- [`llms-txt`](llm-and-rag/llms-txt/SKILL.md) — Create and maintain an llms.txt file following the llms.txt specification.
- [`ai-engineering-toolkit`](llm-and-rag/ai-engineering-toolkit/SKILL.md) — Canonical AI engineering toolkit covering agent development, LLM ops, and app patterns.
- [`data-engineering-data-pipeline`](data-engineering/data-engineering-data-pipeline/SKILL.md) — Canonical data pipeline architecture skill.
