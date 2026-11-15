#!/usr/bin/env python3
import os
import re

DESCRIPTIONS = {
    "n8n-workflow-patterns": "Select, structure, and implement proven architectural patterns for n8n workflows including webhook ingestion, scheduled polling, queue processing, API integration, and AI sub-execution routing when designing or refactoring automated workflows.",
    "n8n-node-configuration": "Configure n8n node parameters, resolve operation dependencies, determine required properties, and apply expression syntax across core and community node families when building or troubleshooting node operations.",
    "n8n-subworkflows": "Design, build, and integrate modular n8n subworkflows with typed inputs, item-by-item vs all-item execution modes, error delegation, and agent tool exposure when decomposing complex workflows or building reusable logic.",
    "n8n-code-python": "Write, debug, and optimize Python transformations in n8n 2.x native Python Code nodes using _items and _item data structures, handling Cloud sandbox constraints and self-hosted runner environments when processing workflow datasets.",
    "n8n-code-tool": "Author, validate, and secure custom code tools callable by AI agents in n8n, defining input JSON schemas, sandbox execution parameters, and output contracts when creating tools for LangChain and AI Agent nodes.",
    "n8n-validation-expert": "Diagnose, interpret, and remediate n8n workflow validation errors, missing required properties, expression syntax failures, and node connection schema mismatches when workflows fail to activate or run.",
    "n8n-mcp-tools-expert": "Utilize n8n-mcp server tools to discover node definitions, validate workflow configurations, search template libraries, and manage n8n workflows programmatically when operating in agent environments.",
    "mcp-builder-ms": "Design, build, and package Model Context Protocol (MCP) servers in Python (FastMCP) or TypeScript (MCP SDK v2) across stdio and streamable HTTP transports when exposing internal tools, data sources, and services to AI agents.",
    "protect-mcp-governance": "Govern AI agent Model Context Protocol (MCP) tool calls using Cedar access control policies, shadow-to-enforce rollout modes, and Ed25519 cryptographic receipt verification when securing tool invocation gateways.",
    "automated-triage": "Triage, assess, score, and troubleshoot Monte Carlo data reliability alerts interactively or via automated scheduled workflows using Monte Carlo MCP tools when investigating data freshness, volume, or schema incidents.",
    "bilig-workpaper": "Execute formula-backed spreadsheet calculations, verify computed cell readbacks, and persist WorkPaper JSON models using the @bilig/workpaper TypeScript API and MCP server when modeling business calculations without spreadsheet GUIs."
}

batch_base = "task-folder/agents/skills-rebuild/workflow-and-automation/tool-integration"

for sname, desc in DESCRIPTIONS.items():
    smfile = os.path.join(batch_base, sname, "SKILL.md")
    if not os.path.isfile(smfile):
        print(f"File not found: {smfile}")
        continue
    with open(smfile, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace description in frontmatter
    new_content = re.sub(r"description:\s*[^\n]+", f"description: {desc}", content, count=1)
    with open(smfile, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated description for {sname}")

print("All descriptions updated successfully.")
