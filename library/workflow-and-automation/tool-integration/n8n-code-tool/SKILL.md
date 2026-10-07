---
name: "n8n-code-tool"
description: "Author, validate, and secure custom code tools callable by AI agents in n8n, defining input JSON schemas, sandbox execution parameters, and output contracts. Use when creating custom AI agent tools for LangChain and AI Agent nodes in n8n."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# n8n Custom Code Tool

Design and implement secure, schema-constrained custom code tools for AI agents in n8n.

## When to Use

Use this skill when:
- Creating custom programmatic tools attached to n8n AI Agent nodes (LangChain/AutoGPT agents).
- Defining strict JSON Schema input definitions for model tool-call generation.
- Executing isolated JavaScript or Python operations on behalf of an AI reasoning loop.
- Handling agent tool execution errors gracefully to prevent agent loop crashes.

Do not use this skill for:
- Standard workflow Code nodes in linear workflows (use `n8n-code-python` or JavaScript nodes).
- Building standalone MCP servers outside n8n (use `mcp-builder-ms`).

## Prerequisites

- n8n AI Agent node connected to a supported LLM model.
- Tool name, description, and input parameters determined.

## Workflow

### 1. Define Tool Metadata & Description
The LLM selects tools based entirely on the tool `name` and `description`:
- **Name**: Use snake_case with clear action verbs (e.g., `calculate_shipping_rate`, `lookup_inventory`).
- **Description**: State what the tool calculates or retrieves, required input formats, and explicit error cases.

### 2. Define Input Schema (JSON Schema)
Constrain tool arguments using standard JSON Schema. Never allow unstructured arbitrary inputs when types are known:
```json
{
  "type": "object",
  "properties": {
    "sku": {
      "type": "string",
      "description": "Product SKU code (e.g. PRD-1029)"
    },
    "quantity": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of items to check"
    }
  },
  "required": ["sku", "quantity"]
}
```

### 3. Implement Tool Execution Code
```javascript
// Access arguments parsed by n8n
const sku = $fromAI('sku');
const quantity = $fromAI('quantity');

if (!sku || quantity <= 0) {
  return JSON.stringify({ error: "Invalid SKU or non-positive quantity provided." });
}

// Perform calculation or data retrieval
const inStock = sku === 'PRD-1029' ? 45 : 0;
const available = inStock >= quantity;

return JSON.stringify({
  sku: sku,
  requested: quantity,
  in_stock: inStock,
  can_fulfill: available
});
```

## Progressive Disclosure & Reference Guides

- [Input Schema Reference](./references/INPUT_SCHEMA.md): Complete parameter type definitions and validation patterns.
- [Error Patterns & Troubleshooting](./references/ERROR_PATTERNS.md): Remediation for sandbox timeouts, type coercion, and LLM hallucination handling.

## Safety & Governance

- Do not expose write/delete capabilities to AI tools without human-in-the-loop confirmation or strict authorization checks.
- Always validate and sanitize inputs inside the tool code even if schema validation is enabled.
- Return structured error JSON strings rather than throwing unhandled exceptions so the agent can self-correct.

## Completion Evidence

- AI Agent successfully invokes tool with compliant arguments.
- Tool returns stringified JSON output matching expected schema.
