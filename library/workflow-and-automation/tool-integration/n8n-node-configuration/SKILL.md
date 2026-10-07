---
name: "n8n-node-configuration"
description: "Configure n8n node parameters, resolve operation dependencies, determine required properties, and apply expression syntax across core and community node families. Use when configuring node operations or authoring dynamic expression bindings in n8n."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# n8n Node Configuration

Configure n8n node parameters, property dependencies, and expression syntax accurately across standard node families.

## When to Use

Use this skill when:
- Setting up specific resource operations on built-in or community n8n nodes.
- Resolving missing required fields, dynamic property dependencies, or type mismatches.
- Writing n8n expressions (e.g. `{{ $json.myField }}`, `{{ $('NodeName').item.json.id }}`).
- Troubleshooting node execution options (retry on fail, continue on fail, execute once).

Do not use this skill for:
- High-level workflow orchestration and topology design (use `n8n-workflow-patterns`).
- AI Custom Code Tool development (use `n8n-code-tool`).
- Writing standalone Python scripts in Code nodes (use `n8n-code-python`).

## Prerequisites

- n8n node name and target resource/operation identified.
- Contextual understanding of upstream node output data structure (`$json`).

## Workflow

### 1. Identify Resource and Operation
Every multi-operation n8n node requires setting the `resource` and `operation` properties first. Changing the operation dynamically alters required and optional parameter fields.

### 2. Configure Required Parameters
- Supply mandatory properties required by the specific operation.
- Use literal values for static configurations or expressions (`{{ ... }}`) for dynamic mapping.

### 3. Handle Expression Syntax & Data Access
- Current item property: `{{ $json.fieldName }}`
- Specific upstream node item: `{{ $('PreviousNodeName').item.json.fieldName }}`
- Global workflow context: `{{ $workflow.id }}`, `{{ $execution.id }}`
- Environment variables: `{{ $env.VARIABLE_NAME }}`

### 4. Configure Execution Settings
- `Continue on Fail`: Enable only when subsequent nodes explicitly handle null/error inputs.
- `Retry on Fail`: Set retry attempts (1–3) and wait intervals (milliseconds) for transient network calls.
- `Execute Once`: Enable for nodes that should run once per batch rather than once per item.

## Progressive Disclosure & Node Gotchas

Consult [Node Family Gotchas](./references/NODE_FAMILY_GOTCHAS.md) for detailed workarounds and property quirks across Google Sheets, Slack, Postgres, HTTP Request, and Airtable nodes.

## Safety & Governance

- Never hardcode API keys or bearer tokens in raw text fields; bind them to n8n Credentials.
- Treat data mapped into database queries with parameterized inputs to prevent injection.

## Completion Evidence

- Node parameters pass n8n validation schema without missing required field errors.
- Test execution against sample item returns expected `$json` structure.
