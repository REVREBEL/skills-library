# Phase 08 Batch Audit Record: `batch-01-workflow-and-automation-tool-integration`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-01-workflow-and-automation-tool-integration`
- **Category / Subcategory**: `workflow-and-automation` / `tool-integration`
- **Member Skill Count**: 11
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `c9da3eeb8425a4ddd8b80b82e13fa73c139a6f8a647f7a148920c9b542f8d9ad`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `automated-triage` | `task-folder/agents/skills/automated-triage` | `skill-writer` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `bilig-workpaper` | `task-folder/agents/skills/bilig-workpaper` | `skill-writer` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `mcp-builder-ms` | `task-folder/agents/skills/mcp/mcp-builder-ms` | `skill-writer` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-code-python` | `task-folder/agents/skills/n8n/n8n-code-python` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-code-tool` | `task-folder/agents/skills/n8n/n8n-code-tool` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-mcp-tools-expert` | `task-folder/agents/skills/n8n/n8n-mcp-tools-expert` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-node-configuration` | `task-folder/agents/skills/n8n/n8n-node-configuration` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-subworkflows` | `task-folder/agents/skills/n8n/n8n-subworkflows` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-validation-expert` | `task-folder/agents/skills/n8n/n8n-validation-expert` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-workflow-patterns` | `task-folder/agents/skills/n8n/n8n-workflow-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `protect-mcp-governance` | `task-folder/agents/skills/protect-mcp-governance` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `automated-triage` | User asks to triage, score, or troubleshoot Monte Carlo data reliability alerts regarding table freshness delays, volume drops, or schema mutations via Monte Carlo MCP tools. | User asks to configure Prometheus alertmanager rules or debug Kubernetes pod crash loops. | User asks 'How do I triage data incidents in our warehouse?' -> Disambiguate: Determine whether the incident is detected via Monte Carlo data reliability monitors or raw BigQuery/Snowflake pipeline execution logs. |
| `bilig-workpaper` | User asks to author, calculate, or verify formula-backed spreadsheet models and cell readbacks programmatically using the @bilig/workpaper TypeScript engine or MCP server. | User asks to format frontend React table CSS styles or build an interactive HTML canvas spreadsheet UI. | User asks 'How do I run spreadsheet formula calculations without Excel?' -> Disambiguate: Clarify whether they require headless Node.js WorkPaper formula evaluations or client-side Google Sheets API automation. |
| `mcp-builder-ms` | User asks to design, develop, and register Model Context Protocol tools in Python (FastMCP) or TypeScript (MCP SDK v2 with Zod schemas) across stdio or SSE/HTTP transports. | User asks to configure an OpenAPI client generator or deploy a standalone Django REST framework service. | User asks 'How do I expose my backend tools to AI models?' -> Disambiguate: Confirm whether they are building a standard Model Context Protocol (MCP) server or authoring custom OpenAI function calling definitions. |
| `n8n-code-python` | User asks to write data transformation scripts inside n8n native Python Code nodes using `_items` and `_item` collections, or debug Python runner sandbox constraints. | User asks to write JavaScript Code nodes using n8n `$helpers` or author standalone Python Flask microservices. | User asks 'How do I process array items in an n8n Code node?' -> Disambiguate: Check if the Code node is configured with Python (using `_items`/`_item`) or JavaScript (using `$input.all()`). |
| `n8n-code-tool` | User asks to author, test, and expose schema-constrained custom code tools for LangChain AI Agent nodes within n8n workflows. | User asks to author standard n8n workflow transformation nodes or write general utility functions outside n8n AI agent workflows. | User asks 'How do I create a custom tool in n8n?' -> Disambiguate: Clarify if the tool is an AI Agent Custom Code Tool with JSON Schema inputs or a standard data-processing Code node. |
| `n8n-mcp-tools-expert` | User asks to query n8n-mcp server tools to inspect node schemas, search public template libraries, or validate workflow JSON definitions programmatically. | User asks to manually build visual workflows inside the n8n web browser canvas. | User asks 'How do I inspect n8n node properties from an agent?' -> Disambiguate: Verify if they want programmatic MCP tool inspection via n8n-mcp or manual node parameter configuration guidance. |
| `n8n-node-configuration` | User asks to configure node properties, resolve operation dependencies, set resource locators, or write dynamic expression bindings (`{{ $json.field }}`) for specific n8n node types. | User asks to author custom community node TypeScript packages from scratch. | User asks 'How do I pass parameters to an n8n node?' -> Disambiguate: Determine if they need parameter configuration on an existing node or expression data mapping between connected nodes. |
| `n8n-subworkflows` | User asks to architect modular n8n subworkflows with Execute Workflow triggers, item-by-item batching, or subworkflow error delegation. | User asks to write monolithic single-canvas workflows without modular decomposition. | User asks 'How do I call another workflow from n8n?' -> Disambiguate: Check if they are using the Execute Workflow node for synchronous modular logic or triggering external workflows via HTTP webhooks. |
| `n8n-validation-expert` | User asks to diagnose, interpret, and resolve n8n workflow validation errors, schema connection mismatches, or missing required parameter violations. | User asks to run Jest unit test suites for React frontend components. | User asks 'Why is my n8n workflow failing to run?' -> Disambiguate: Clarify whether the issue is pre-execution validation/schema misconfiguration or runtime third-party API errors. |
| `n8n-workflow-patterns` | User asks to design architectural patterns for n8n workflows such as idempotent webhook ingestion, fan-out polling queues, or retry backoff orchestrations. | User asks to write low-level Python data manipulation scripts inside single nodes. | User asks 'What is the best way to structure an n8n workflow?' -> Disambiguate: Confirm whether they need high-level orchestration pattern architecture (polling, webhooks, queues) or specific node configuration. |
| `protect-mcp-governance` | User asks to define Cedar authorization policies, enforce least-privilege tool execution rules, or verify Ed25519 cryptographic receipts on MCP agent gateways. | User asks to implement OAuth2 authorization flows for web users in a Ruby on Rails application. | User asks 'How do I secure tool calls made by AI agents?' -> Disambiguate: Verify whether they require MCP gateway policy enforcement (Cedar/Ed25519) or standard API token authentication. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/workflow-and-automation/tool-integration/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `c9da3eeb8425a4ddd8b80b82e13fa73c139a6f8a647f7a148920c9b542f8d9ad` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `automated-triage` | `references/triage-example.md` | Created or preserved in canonical package |
| `automated-triage` | `references/triage-stages.md` | Created or preserved in canonical package |
| `mcp-builder-ms` | `references/LEGACY_V1_MIGRATION.md` | Created or preserved in canonical package |
| `n8n-code-python` | `references/LEGACY_PYODIDE_COMPATIBILITY.md` | Created or preserved in canonical package |
| `n8n-code-tool` | `references/ERROR_PATTERNS.md` | Created or preserved in canonical package |
| `n8n-code-tool` | `references/INPUT_SCHEMA.md` | Created or preserved in canonical package |
| `n8n-node-configuration` | `references/NODE_FAMILY_GOTCHAS.md` | Created or preserved in canonical package |
| `n8n-subworkflows` | `references/NAMING_AND_DISCOVERY.md` | Created or preserved in canonical package |
| `n8n-subworkflows` | `references/SUBWORKFLOW_PATTERNS.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
