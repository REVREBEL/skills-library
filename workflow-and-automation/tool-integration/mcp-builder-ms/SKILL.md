---
name: "mcp-builder-ms"
description: "Design, build, and package Model Context Protocol (MCP) servers in Python (FastMCP) or TypeScript (MCP SDK v2) across stdio and streamable HTTP transports. Use when exposing internal tools, data sources, and services to AI agents."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# MCP Server Development Guide (v2 Protocol)

Build robust, production-grade Model Context Protocol (MCP) servers implementing the 2026-07-28 protocol in Python (FastMCP) or TypeScript (`@modelcontextprotocol/server` v2).

## When to Use

Use this skill when:
- Designing and implementing a custom MCP server to expose databases, internal microservices, or developer utilities to AI coding assistants.
- Authoring MCP tools, resources, and prompts in TypeScript using the official v2 `@modelcontextprotocol/server` API.
- Authoring fast Python MCP servers using the `fastmcp` library.
- Implementing standard `stdio` process transports or remote streamable HTTP / SSE endpoints.
- Structuring tool input schemas, validation handlers, and error boundaries for LLM tool calling.

Do not use this skill for:
- Configuring pre-built n8n MCP tools (use `n8n-mcp-tools-expert`).
- Setting up Cedar policy authorization or signed receipt verification for MCP tools (use `protect-mcp-governance`).

## Prerequisites

- Python 3.10+ (for Python FastMCP) or Node.js 20+ / Bun / TypeScript (for TypeScript SDK v2).
- Clear specification of exposed tool names, descriptions, input schemas, and return structures.

---

## Architecture & Transport Patterns

MCP servers communicate with client AI agents across two standard transport mechanisms:
1. **`stdio` (Standard I/O)**: Spawns the MCP server as a local child process. Best for desktop IDEs, CLI tools, and local single-user development.
2. **Streamable HTTP / SSE**: Runs as a standalone network service over HTTP/HTTPS. Best for multi-tenant services, cloud agents, and shared microservices.

---

## Implementation Guide

### Pattern A: Modern TypeScript Server (v2 `@modelcontextprotocol/server`)

The modern 2026-07-28 protocol separates server definitions from transport listeners. In v2, tools are registered using `server.registerTool(name, config, callback)` with a Zod schema object. The SDK derives JSON Schema specifications and type-safe handler arguments automatically. Pass a `createServer` factory function to `serveStdio` for process execution or `createMcpHandler` for HTTP endpoints.

```typescript
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";

function createServer(): McpServer {
  const server = new McpServer({
    name: "customer-tools-mcp",
    version: "2.0.0",
  });

  server.registerTool(
    "lookup_customer",
    {
      description: "Lookup customer account profile and status by email address.",
      inputSchema: z.object({
        email: z.string().email().describe("The customer email address"),
        include_history: z.boolean().default(false).describe("Include recent order history"),
      }),
    },
    async ({ email, include_history }) => {
      // Perform database / API lookup
      const customer = {
        id: "CUST-4819",
        email,
        status: "active",
        plan: "enterprise",
        orders: include_history ? [{ id: "ORD-902", total: 450.0 }] : undefined,
      };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(customer, null, 2),
          },
        ],
      };
    }
  );

  return server;
}

// Serve over stdio transport using the official v2 listener factory
void serveStdio(createServer);
```

### Pattern B: Python FastMCP Server

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(
    name="DatabaseMCP",
    dependencies=["pydantic"]
)

class QueryFilter(BaseModel):
    table_name: str = Field(description="Target table name (e.g. 'users', 'invoices')")
    limit: int = Field(default=10, ge=1, le=100, description="Max records to retrieve")

@mcp.tool(name="query_records", description="Execute structured read queries against database tables.")
def query_records(table_name: str, limit: int = 10) -> dict:
    # Validate and sanitize table name
    allowed_tables = {"users", "invoices", "products"}
    if table_name not in allowed_tables:
        return {"error": f"Table '{table_name}' is not in allowed query set."}

    # Execute query logic
    return {
        "table": table_name,
        "count": 1,
        "records": [{"id": 1, "status": "active"}]
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Progressive Disclosure & Reference

- [Legacy v1 MCP Migration Guide](./references/LEGACY_V1_MIGRATION.md): Guide for upgrading 2025-era v1 `new Server(...)` and removed `.tool(...)` implementations to v2.

---

## Tool Design Best Practices

1. **Explicit Parameter Descriptions**: Models use property descriptions to construct arguments accurately.
2. **Deterministic Return Payload**: Return JSON strings wrapped in `content: [{ type: "text", text: "..." }]`.
3. **Structured Errors in Content**: Return informative error JSON within the text content rather than throwing unhandled transport errors.

## Safety & Governance

- Sanitize all parameters before executing shell commands or database queries to prevent injection.
- Never write debug or logging statements directly to `stdout` in stdio mode (use `stderr` or MCP logging notifications), as writing to stdout corrupts JSON-RPC framing.
- For fine-grained access control, integrate Cedar policy governance via `protect-mcp-governance`.

## Completion Evidence

- Server responds to `tools/list` with complete JSON schemas and parameter descriptions.
- `tools/call` invocations return valid content payloads conforming to the MCP specification.
