---
name: "protect-mcp-governance"
description: "Govern AI agent Model Context Protocol (MCP) tool calls using Cedar access control policies, shadow-to-enforce rollout modes, and Ed25519 cryptographic receipt verification. Use when securing and auditing AI agent tool execution gateways with Cedar policies."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# MCP Agent Governance with protect-mcp

Enforce fine-grained authorization, Cedar policy evaluation, and cryptographic audit receipts for AI agent MCP tool executions.

## When to Use

Use this skill when:
- Restricting which MCP tools an AI agent can invoke and under what specific argument conditions.
- Implementing tamper-evident audit trails for agent tool executions using Ed25519 signed receipts.
- Rolling out governance policies gradually from shadow mode (observe without blocking) to enforce mode.
- Authoring and testing Cedar policies for local WASM-evaluated access control.
- Verifying receipt authenticity and audit bundles after security incidents or compliance reviews.

Do not use this skill for:
- General static code vulnerability scanning (use security audit tools).
- Network firewall configuration outside MCP tool invocation gateways.

## Prerequisites

- Node.js 18+ runtime.
- Target MCP server and client configuration.
- `protect-mcp` CLI / package available via `npx protect-mcp` or project dependency.

## Governance Architecture

```
Agent → protect-mcp Gateway → Cedar Policy Evaluation → Target MCP Server
                 ↓
         Ed25519 Signed Receipt
```

### Operational Modes
1. **Shadow Mode (Default)**: Evaluates policies, logs decisions, and emits receipts without blocking tool calls.
2. **Enforce Mode**: Evaluates policies and blocks any tool call that violates Cedar rules.
3. **Hooks Mode**: Integrates with agent execution hooks for pre/post tool-call verification.

## Step-by-Step Workflow

### 1. Initialize Project Governance
```bash
# Initialize governance configuration and starter policy
npx protect-mcp init-hooks

# Or launch as a standalone MCP gateway
npx protect-mcp serve
```

### 2. Author Cedar Authorization Policies
Create `policy.cedar` in your project root:
```cedar
// Allow read-only file and search operations
permit(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name in ["read_file", "list_directory", "search_files"]
};

// Forbid destructive operations unless explicitly allowlisted
forbid(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name in ["execute_command", "delete_file", "drop_table"]
};
```

### 3. Observe in Shadow Mode
```bash
# Run wrapped server in shadow mode to observe traffic without disruption
npx protect-mcp --policy policy.cedar -- node your-mcp-server.js
```

### 4. Switch to Enforce Mode
```bash
# Enforce policy decisions and block forbidden tool calls
npx protect-mcp --policy policy.cedar --enforce -- node your-mcp-server.js
```

### 5. Verify Cryptographic Receipts
```bash
# Verify a single signed receipt
npx @veritasacta/verify receipt.json --key <public-key-hex>

# Verify a full session audit bundle
npx @veritasacta/verify bundle.json --bundle
```

## Safety & Governance Rules

- Always observe agent behavior in Shadow Mode before enforcing restrictive policies in production.
- Note that Cedar evaluates `forbid` rules with precedence over `permit` rules.
- Pin verifier dependencies (`@veritasacta/verify@0.2.5`) in CI/CD pipeline verification jobs.

## Completion Evidence

- `protect-mcp.config.json` and valid `policy.cedar` generated.
- Shadow mode logs show policy evaluations with corresponding `policy_digest`.
- Receipt verification command exits with code 0 (signature valid).
