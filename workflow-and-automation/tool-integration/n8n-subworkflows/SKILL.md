---
name: "n8n-subworkflows"
description: "Design, build, and integrate modular n8n subworkflows with typed inputs, item-by-item vs all-item execution modes, error delegation, and agent tool exposure. Use when decomposing complex workflows into reusable subworkflows in n8n."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# n8n Sub-workflows

Build modular, reusable n8n sub-workflows with strict input typing, flexible execution modes, and clean parent-child error boundaries.

## When to Use

Use this skill when:
- Extracting shared logic (e.g. customer lookup, notification delivery, payload sanitization) across multiple parent workflows.
- Exposing an n8n workflow as a callable tool for an AI Agent node.
- Managing complex multi-step pipelines by decomposing them into independently testable units.
- Isolating error handling and retry policies for specific sub-tasks.

Do not use this skill for:
- Writing raw inline Python/JavaScript transformations within a single node (use `n8n-code-python` or `n8n-code-tool`).
- Discovering n8n-mcp server tools (use `n8n-mcp-tools-expert`).

## Prerequisites

- Parent and child workflows created in the same n8n environment (or accessible via workflow ID / webhook).
- Defined input schema and expected output contract for the sub-workflow.

## Workflow

### 1. Construct the Sub-workflow
1. **Execute Sub-workflow Trigger**: Place as the first node. Define required input properties and mock data for standalone testing.
2. **Business Logic Nodes**: Execute processing, validation, and transformations.
3. **Respond / Output Node**: Ensure the terminal node returns a clean, predictable `$json` object.

### 2. Configure the Parent Call
1. In the parent workflow, insert the `Execute Sub-workflow` node.
2. Select the sub-workflow by ID or name.
3. Choose **Execution Mode**:
   - `Each Item`: Invokes the child workflow once per inbound item (useful for row-by-row isolation).
   - `All Items`: Passes the full item array to the child workflow in a single batch invocation.

### 3. Expose as AI Agent Tool
When exposing a sub-workflow to an AI Agent:
- Name the workflow descriptively with clear verb-noun semantics (e.g. `tool-lookup-customer-by-email`).
- Provide an explicit input schema describing each argument for the LLM tool-calling parser.

## Supporting References

- [Sub-workflow Architectural Patterns](./references/SUBWORKFLOW_PATTERNS.md): Advanced batching, recursion guards, and error delegation.
- [Naming & Discovery Standards](./references/NAMING_AND_DISCOVERY.md): Organization conventions for sub-workflow libraries.

## Safety & Governance

- Never expose unrestricted database delete or broad update operations as unauthenticated subworkflows.
- Enforce recursion limits when subworkflows invoke other subworkflows.
- Sanitize inputs to prevent SQL or command injection when passing raw agent arguments.

## Completion Evidence

- Sub-workflow executes successfully when triggered standalone with mock data.
- Parent workflow successfully invokes the sub-workflow and captures expected output fields.
