---
name: "n8n-mcp-tools-expert"
description: "Utilize n8n-mcp server tools to discover node definitions, validate workflow configurations, search template libraries, and manage n8n workflows programmatically. Use when inspecting node parameters, searching templates, or managing n8n workflows via MCP tools."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# n8n MCP Tools Expert

Leverage Model Context Protocol (`n8n-mcp`) tools to discover, configure, validate, and manage n8n workflows programmatically.

## When to Use

Use this skill when:
- Operating in an agent environment equipped with the `n8n-mcp` tool server.
- Searching for available n8n nodes, supported operations, and required properties programmatically.
- Validating n8n node configurations against live node schemas before deployment.
- Searching and retrieving community workflow templates from the n8n template library.

Do not use this skill for:
- Writing custom FastMCP servers in Python or TypeScript (use `mcp-builder-ms`).
- Direct manual editing in the n8n visual UI without MCP tools.

## Prerequisites

- Active `n8n-mcp` server configured in the agent runtime.
- Network connectivity to target n8n instance API.

## Core Tool Capabilities

### 1. Node Discovery & Documentation
- `search_nodes`: Search for nodes by keyword, category, or service name (e.g. "airtable", "postgres", "slack").
- `get_node_info`: Retrieve comprehensive metadata, supported resources, operations, and property schemas for a specific node type.

### 2. Configuration Validation
- `validate_node_config`: Submit proposed node parameters to verify compliance against required fields, valid enum values, and type expectations.
- `validate_workflow`: Validate an entire exported workflow JSON structure for disconnected nodes or invalid parameter bindings.

### 3. Template Search & Deployment
- `search_templates`: Search over 2,700+ verified workflow templates by use case, integrated apps, or categories.
- `get_template`: Retrieve full workflow JSON for a template ID ready for customization.

## Recommended Tool Calling Workflow

1. **Discover**: Call `search_nodes` to identify exact node type names (e.g. `n8n-nodes-base.httpRequest`).
2. **Inspect**: Call `get_node_info` with the specific `resource` and `operation` to inspect required properties.
3. **Draft**: Construct the node parameter payload.
4. **Validate**: Call `validate_node_config` with the drafted payload to assert correctness before applying.

## Safety & Governance

- Never pass production secrets or unmasked API credentials into public template search queries.
- Validate workflow JSON schemas prior to executing programmatic deployment or activation calls.

## Completion Evidence

- Successful discovery and validation responses returned by `n8n-mcp` tools.
- Generated workflow configurations pass validation without schema rejections.
