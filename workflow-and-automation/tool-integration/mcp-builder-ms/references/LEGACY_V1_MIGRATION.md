# Legacy v1 MCP TypeScript Migration Guide

This document details how to migrate legacy 2025-era v1 MCP TypeScript code to the modern 2026-era v2 `@modelcontextprotocol/server` API.

## API Comparison

| Feature | Legacy v1 (2025) | Modern v2 (2026-07-28 Protocol) |
|---|---|---|
| Runtime | Node.js 18+ | Node.js 20+ |
| Package | `@modelcontextprotocol/sdk` | `@modelcontextprotocol/server` |
| Server class | `new Server({ ... }, { capabilities: { ... } })` | `new McpServer({ name, version })` |
| Tool registration | `server.tool(...)` or `setRequestHandler(ListToolsRequestSchema, ...)` | `server.registerTool(name, { description, inputSchema: z.object(...) }, callback)` |
| Transport serving | `await server.connect(new StdioServerTransport())` | `void serveStdio(createServer)` |
| HTTP serving | Custom SSE / Express handlers | `createMcpHandler(server)` |

## Legacy v1 Pattern

```typescript
// Legacy v1 Pattern (Deprecated)
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "legacy", version: "1.0.0" }, { capabilities: { tools: {} } });
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Migration Steps to v2

1. Upgrade Node.js runtime to version 20+.
2. Install `@modelcontextprotocol/server` and `zod`.
3. Replace removed `.tool(...)` or low-level request handlers with `server.registerTool(name, { description, inputSchema: z.object(...) }, callback)`.
4. Wrap server construction in a `createServer()` factory and pass it to `void serveStdio(createServer)` for stdio or `createMcpHandler(server)` for HTTP.
