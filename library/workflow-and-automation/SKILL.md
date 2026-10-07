---
name: workflow-and-automation
description: Category router for workflow-and-automation, dispatching 25 canonical skills across 4 subcategories.
type: category-router
version: 1.0.0
---

# Workflow And Automation Router

## Overview

The `workflow-and-automation` domain covers **25 active canonical skills** organized under 4 specialized subcategories.

## When to Use

Use this router when the user request involves workflow automation, web scraping, git version control, and mcp tool integration.

## Scope Boundaries & Handoffs

- Return to [Root Router](../SKILL.md) if the task falls outside this domain.

## Subcategory Routing Index

### Git And Vcs

Manage 4 skills for git and vcs.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`repo-maintainer`](../marketing-and-seo/cro/repo-maintainer/SKILL.md) | Audit and repair repository hygiene across artifacts, dependencies, CI, docs, Git state, and code-quality signals. Use for repository maintenance, cleanup, h... | Repo Maintainer: Audit and repair repository hygiene across artifacts, dependencies, CI, docs, Git ... |
| [`resolving-merge-conflicts`](../development/fullstack/resolving-merge-conflicts/SKILL.md) | Use when you need to resolve an in-progress git merge/rebase conflict. | Resolving Merge Conflicts: you need to resolve an in-progress git merge/rebase conflict |
| [`using-git-worktrees`](git-and-vcs/using-git-worktrees/SKILL.md) | Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching. Use when working w... | Using Git Worktrees: Git worktrees create isolated workspaces sharing the same repository, allowing wor... |
| [`version-control-strategy`](../design-and-experience/ui-ux/version-control-strategy/SKILL.md) | Define version control strategies for design files, components, and libraries. Use when working with version control strategy. | Version Control Strategy: Define version control strategies for design files, components, and libraries. Use... |

### Task Orchestration

Manage 6 skills for task orchestration.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`go-rod-master`](task-orchestration/go-rod-master/SKILL.md) | Comprehensive guide for browser automation and web scraping with go-rod (Chrome DevTools Protocol) including stealth anti-bot-detection patterns. Use when wo... | Go Rod Master: Comprehensive guide for browser automation and web scraping with go-rod (Chrome De... |
| [`hasdata`](task-orchestration/hasdata/SKILL.md) | Use HasData APIs for web scraping and structured web data extraction. Use when working with hasdata. | Hasdata: Use HasData APIs for web scraping and structured web data extraction. Use when wor... |
| [`n8n-code-javascript`](../quality-and-security/debugging/n8n-code-javascript/SKILL.md) | Write JavaScript code in n8n Code nodes. Use when writing JavaScript in n8n, using $input/$json/$node syntax, making HTTP requests with $helpers, working wit... | N8N Code Javascript: Write JavaScript code in n8n Code nodes. Use when writing JavaScript in n8n, using... |
| [`n8n-error-handling`](../business-and-operations/legal-and-governance/n8n-error-handling/SKILL.md) | Configure error workflows, retry policies, and alert routing in n8n automation pipelines. Use when handling execution failures or building resilient n8n work... | N8N Error Handling: Configure error workflows, retry policies, and alert routing in n8n automation pip... |
| [`open-dynamic-workflows`](task-orchestration/open-dynamic-workflows/SKILL.md) | Plan, orchestrate, and adversarially verify parallel AI coding agents with a dynamic multi-agent workflow engine. Use when working with open dynamic workflows. | Open Dynamic Workflows: Plan, orchestrate, and adversarially verify parallel AI coding agents with a dynam... |
| [`workflow-automation`](task-orchestration/workflow-automation/SKILL.md) | Workflow automation is the infrastructure that makes AI agents. Use when working with workflow automation. | Workflow Automation: Workflow automation is the infrastructure that makes AI agents. Use when working w... |

### Tool Integration

Manage 11 skills for tool integration.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`bilig-workpaper`](tool-integration/bilig-workpaper/SKILL.md) | Execute formula-backed spreadsheet calculations, verify computed cell readbacks, and persist WorkPaper JSON models using the @bilig/workpaper TypeScript API ... | Bilig Workpaper: Execute formula-backed spreadsheet calculations, verify computed cell readbacks, a... |
| [`mcp-builder-ms`](tool-integration/mcp-builder-ms/SKILL.md) | Design, build, and package Model Context Protocol (MCP) servers in Python (FastMCP) or TypeScript (MCP SDK v2) across stdio and streamable HTTP transports. U... | Mcp Builder Ms: Design, build, and package Model Context Protocol (MCP) servers in Python (FastMCP... |
| [`mcp-tool-developer`](../quality-and-security/testing/mcp-tool-developer/SKILL.md) | Build Model Context Protocol (MCP) servers and tools from scratch. Full-stack MCP development with TypeScript/Python, testing, deployment, and registry publi... | Mcp Tool Developer: Build Model Context Protocol (MCP) servers and tools from scratch. Full-stack MCP ... |
| [`n8n-code-python`](tool-integration/n8n-code-python/SKILL.md) | Write, debug, and optimize Python transformations in n8n 2.x native Python Code nodes using _items and _item data structures, handling Cloud sandbox constrai... | N8N Code Python: Write, debug, and optimize Python transformations in n8n 2.x native Python Code no... |
| [`n8n-code-tool`](tool-integration/n8n-code-tool/SKILL.md) | Author, validate, and secure custom code tools callable by AI agents in n8n, defining input JSON schemas, sandbox execution parameters, and output contracts.... | N8N Code Tool: Author, validate, and secure custom code tools callable by AI agents in n8n, defin... |
| [`n8n-mcp-tools-expert`](tool-integration/n8n-mcp-tools-expert/SKILL.md) | Utilize n8n-mcp server tools to discover node definitions, validate workflow configurations, search template libraries, and manage n8n workflows programmatic... | N8N Mcp Tools Expert: Utilize n8n-mcp server tools to discover node definitions, validate workflow confi... |
| [`n8n-node-configuration`](tool-integration/n8n-node-configuration/SKILL.md) | Configure n8n node parameters, resolve operation dependencies, determine required properties, and apply expression syntax across core and community node fami... | N8N Node Configuration: Configure n8n node parameters, resolve operation dependencies, determine required ... |
| [`n8n-subworkflows`](tool-integration/n8n-subworkflows/SKILL.md) | Design, build, and integrate modular n8n subworkflows with typed inputs, item-by-item vs all-item execution modes, error delegation, and agent tool exposure.... | N8N Subworkflows: Design, build, and integrate modular n8n subworkflows with typed inputs, item-by-i... |
| [`n8n-validation-expert`](tool-integration/n8n-validation-expert/SKILL.md) | Diagnose, interpret, and remediate n8n workflow validation errors, missing required properties, expression syntax failures, and node connection schema mismat... | N8N Validation Expert: Diagnose, interpret, and remediate n8n workflow validation errors, missing require... |
| [`n8n-workflow-patterns`](tool-integration/n8n-workflow-patterns/SKILL.md) | Select, structure, and implement proven architectural patterns for n8n workflows including webhook ingestion, scheduled polling, queue processing, API integr... | N8N Workflow Patterns: Select, structure, and implement proven architectural patterns for n8n workflows i... |
| [`protect-mcp-governance`](tool-integration/protect-mcp-governance/SKILL.md) | Govern AI agent Model Context Protocol (MCP) tool calls using Cedar access control policies, shadow-to-enforce rollout modes, and Ed25519 cryptographic recei... | Protect Mcp Governance: Govern AI agent Model Context Protocol (MCP) tool calls using Cedar access control... |

### Web Scraping

Manage 4 skills for web scraping.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`firecrawl-scraper`](../marketing-and-seo/technical-seo/firecrawl-scraper/SKILL.md) | Deep web scraping, screenshots, PDF parsing, and website crawling using Firecrawl API. Use when you need deep content extraction from web pages, page interac... | Firecrawl Scraper: Deep web scraping, screenshots, PDF parsing, and website crawling using Firecrawl ... |
| [`puppeteer-skill`](web-scraping/puppeteer-skill/SKILL.md) | Generates Puppeteer scripts for browser automation, scraping, and PDF generation. Triggers on: \\\"Puppeteer\\\", \\\"headless Chrome\\\", \\\"page.goto\\\",... | Puppeteer Skill: Generates Puppeteer scripts for browser automation, scraping, and PDF generation. ... |
| [`web-scraper`](../marketing-and-seo/on-page-seo/web-scraper/SKILL.md) | Extract structured data from websites. Use when: collecting competitor pricing; scraping product listings; extracting contact information; gathering research... | Web Scraper: Extract structured data from websites. Use when: collecting competitor pricing; sc... |
| [`web-scraper`](web-scraping/web-scraper/SKILL.md) | Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas web (tabelas, listas, precos). Paginacao, monitoramento e export CSV/JSON. Us... | Web Scraper: Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas we... |

---
*Part of the Canonical Agent Skills Hierarchy.*
