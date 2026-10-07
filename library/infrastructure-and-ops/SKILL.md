---
name: infrastructure-and-ops
description: Category router for infrastructure-and-ops, dispatching 59 canonical skills across 5 subcategories.
type: category-router
version: 1.0.0
---

# Infrastructure And Ops Router

## Overview

The `infrastructure-and-ops` domain covers **59 active canonical skills** organized under 5 specialized subcategories.

## When to Use

Use this router when the user request involves ci/cd pipelines, cloud platforms, container orchestration, observability, and sysadmin.

## Scope Boundaries & Handoffs

- Return to [Root Router](../SKILL.md) if the task falls outside this domain.

## Subcategory Routing Index

### Ci Cd

Manage 5 skills for ci cd.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`ci-cd-and-automation`](ci-cd/ci-cd-and-automation/SKILL.md) | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test ... | Ci Cd And Automation: Automates CI/CD pipeline setup. Use when setting up or modifying build and deploym... |
| [`cicd-automation-workflow-automate`](ci-cd/cicd-automation-workflow-automate/SKILL.md) | You are a workflow automation expert specializing in creating efficient CI/CD pipelines, GitHub Actions workflows, and automated development processes. Desig... | Cicd Automation Workflow Automate: You are a workflow automation expert specializing in creating efficient CI/CD pipe... |
| [`monorepo-architect`](ci-cd/monorepo-architect/SKILL.md) | Expert in monorepo architecture, build systems, and dependency management at scale. Masters Nx, Turborepo, Bazel, and Lerna for efficient multi-project devel... | Monorepo Architect: monorepo architecture, build systems, and dependency management at scale. Masters ... |
| [`security-review`](ci-cd/security-review/SKILL.md) | Find exploitable vulnerabilities in GitHub Actions workflows. Every finding MUST include a concrete exploitation scenario — if you can't build the attack, do... | Security Review: Find exploitable vulnerabilities in GitHub Actions workflows. Every finding MUST i... |
| [`turborepo-caching`](ci-cd/turborepo-caching/SKILL.md) | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipelines, or implementing d... | Turborepo Caching: Configure Turborepo for efficient monorepo builds with local and remote caching. U... |

### Cloud Platforms

Manage 15 skills for cloud platforms.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`auri-core`](cloud-platforms/auri-core/SKILL.md) | Auri: assistente de voz inteligente (Alexa + modelo-inteligente). Visao do produto, persona Vitoria Neural, stack AWS, modelo Free/Pro/Business/Enterprise, r... | Auri Core: Auri: assistente de voz inteligente (Alexa + modelo-inteligente). Visao do produto... |
| [`cdk-patterns`](cloud-platforms/cdk-patterns/SKILL.md) | Common AWS CDK patterns and constructs for building cloud infrastructure with TypeScript, Python, or Java. Use when designing reusable CDK stacks and L3 cons... | Cdk Patterns: Common AWS CDK patterns and constructs for building cloud infrastructure with Type... |
| [`cloud-architect`](cloud-platforms/cloud-architect/SKILL.md) | Expert cloud architect specializing in AWS/Azure/GCP multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and ... | Cloud Architect: Expert cloud architect specializing in AWS/Azure/GCP multi-cloud infrastructure de... |
| [`cost-optimization`](../marketing-and-seo/cro/cost-optimization/SKILL.md) | Strategies and patterns for optimizing cloud costs across AWS, Azure, and GCP. Use when working with cost optimization. | Cost Optimization: Strategies and patterns for optimizing cloud costs across AWS, Azure, and GCP. Use... |
| [`database-cloud-optimization-cost-optimize`](../marketing-and-seo/cro/database-cloud-optimization-cost-optimize/SKILL.md) | You are a cloud cost optimization expert specializing in reducing infrastructure expenses while maintaining performance and reliability. Analyze cloud spendi... | Database Cloud Optimization Cost Optimize: You are a cloud cost optimization expert specializing in reducing infrastructure e... |
| [`deploy-to-vercel`](cloud-platforms/deploy-to-vercel/SKILL.md) | Deploy applications and websites to Vercel. Use when the user requests deployment actions like \\\\"deploy my app\\\\", \\\\"deploy and give me the link\\\\"... | Deploy To Vercel: Deploy applications and websites to Vercel. Use when the user requests deployment ... |
| [`multi-cloud-architecture`](../marketing-and-seo/cro/multi-cloud-architecture/SKILL.md) | Decision framework and patterns for architecting applications across AWS, Azure, and GCP. Use when working with multi cloud architecture. | Multi Cloud Architecture: Decision framework and patterns for architecting applications across AWS, Azure, a... |
| [`remote-gpu-trainer`](cloud-platforms/remote-gpu-trainer/SKILL.md) | Deploy, monitor, and debug long GPU jobs on RENTED/remote instances (AutoDL, RunPod, vast.ai, Lambda, Slurm, K8s): teardown/billing safety, spot resilience, ... | Remote Gpu Trainer: Deploy, monitor, and debug long GPU jobs on RENTED/remote instances (AutoDL, RunPo... |
| [`sandbox-sdk`](cloud-platforms/sandbox-sdk/SKILL.md) | Build sandboxed applications for secure code execution. Load when building AI code execution, code interpreters, CI/CD systems, interactive dev environments,... | Sandbox Sdk: Build sandboxed applications for secure code execution. Load when building AI code... |
| [`turnstile-spin`](cloud-platforms/turnstile-spin/SKILL.md) | Set up Cloudflare Turnstile end-to-end in a project — scan the codebase, create the widget via the Cloudflare API, deploy the managed siteverify Worker, writ... | Turnstile Spin: Set up Cloudflare Turnstile end-to-end in a project — scan the codebase, create th... |
| [`vercel-ai-sdk-expert`](cloud-platforms/vercel-ai-sdk-expert/SKILL.md) | Expert in the Vercel AI SDK. Covers Core API (generateText, streamText), UI hooks (useChat, useCompletion), tool calling, and streaming UI components with Re... | Vercel Ai Sdk Expert: the Vercel AI SDK. Covers Core API (generateText, streamText), UI hooks (useChat, ... |
| [`vercel-automation`](cloud-platforms/vercel-automation/SKILL.md) | Automate Vercel tasks via Rube MCP (Composio): manage deployments, domains, DNS, env vars, projects, and teams. Always search tools first for current schemas... | Vercel Automation: Automate Vercel tasks via Rube MCP (Composio): manage deployments, domains, DNS, e... |
| [`vercel-deployment`](cloud-platforms/vercel-deployment/SKILL.md) | Expert knowledge for deploying to Vercel with Next.js. Use when working with vercel deployment. | Vercel Deployment: Expert knowledge for deploying to Vercel with Next.js. Use when working with verce... |
| [`vercel-optimize`](cloud-platforms/vercel-optimize/SKILL.md) | Audit deployed Vercel apps for cost and performance issues using metrics, project config, code scans, and version-aware recommendations. Use when working wit... | Vercel Optimize: Audit deployed Vercel apps for cost and performance issues using metrics, project ... |
| [`workflow-automation`](cloud-platforms/workflow-automation/SKILL.md) | Patterns for automating GitHub workflows with AI assistance, inspired by Gemini CLI and modern DevOps practices. Use when working with workflow automation. | Workflow Automation: Patterns for automating GitHub workflows with AI assistance, inspired by Gemini CL... |

### Containers And Orchestration

Manage 18 skills for containers and orchestration.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`1password`](containers-and-orchestration/1password/SKILL.md) | Route 1Password secrets management requests across CLI retrieval, Developer Environments, Kubernetes integrations, and Service Account CI/CD workflows. Use w... | 1Password: Route 1Password secrets management requests across CLI retrieval, Developer Enviro... |
| [`1password-cli`](containers-and-orchestration/1password-cli/SKILL.md) | Execute 1Password CLI (op) operations for local development, secret retrieval, item/vault CRUD, configuration injection, shell plugins, and git credential wo... | 1Password Cli: Execute 1Password CLI (op) operations for local development, secret retrieval, ite... |
| [`1password-developer-environments`](containers-and-orchestration/1password-developer-environments/SKILL.md) | Manage 1Password Developer Environments for project environment variables using TypeScript (Bun) and Python SDK tools. Use when creating, updating, exporting... | 1Password Developer Environments: Manage 1Password Developer Environments for project environment variables using Ty... |
| [`1password-kubernetes`](containers-and-orchestration/1password-kubernetes/SKILL.md) | Configure and deploy Kubernetes secret synchronization using the native 1Password Operator and External Secrets Operator (ESO). Use when injecting 1Password ... | 1Password Kubernetes: Configure and deploy Kubernetes secret synchronization using the native 1Password ... |
| [`1password-service-accounts`](containers-and-orchestration/1password-service-accounts/SKILL.md) | Configure 1Password Service Accounts for CI/CD automation, GitHub Actions, GitLab CI, CircleCI, and container environments. Use when provisioning service acc... | 1Password Service Accounts: Configure 1Password Service Accounts for CI/CD automation, GitHub Actions, GitLab ... |
| [`agents-v2-py`](containers-and-orchestration/agents-v2-py/SKILL.md) | Build container-based Foundry Agents with Azure AI Projects SDK (ImageBasedHostedAgentDefinition). Use when creating hosted agents with custom container imag... | Agents V2 Py: Build container-based Foundry Agents with Azure AI Projects SDK (ImageBasedHostedA... |
| [`apple-container`](containers-and-orchestration/apple-container/SKILL.md) | Build, run, and manage OCI/Linux containers as lightweight per-container VMs on Apple-silicon macOS using Apple's open-source container CLI, no Docker daemon... | Apple Container: Build, run, and manage OCI/Linux containers as lightweight per-container VMs on Ap... |
| [`cloud-devops`](containers-and-orchestration/cloud-devops/SKILL.md) | Cloud infrastructure and DevOps workflow covering AWS, Azure, GCP, Kubernetes, Terraform, CI/CD, monitoring, and cloud-native development. Use when working w... | Cloud Devops: Cloud infrastructure and DevOps workflow covering AWS, Azure, GCP, Kubernetes, Ter... |
| [`container-security-hardening`](containers-and-orchestration/container-security-hardening/SKILL.md) | Execute container-security-hardening tasks, workflows, and automated procedures. Use when working with container security hardening. | Container Security Hardening: Execute container-security-hardening tasks, workflows, and automated procedures. U... |
| [`docker-expert`](containers-and-orchestration/docker-expert/SKILL.md) | You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds,... | Docker Expert: You are an advanced Docker containerization expert with comprehensive, practical k... |
| [`gcp-cloud-run`](containers-and-orchestration/gcp-cloud-run/SKILL.md) | Specialized skill for building production-ready serverless. Use when working with gcp cloud run. | Gcp Cloud Run: Specialized skill for building production-ready serverless. Use when working with ... |
| [`hosted-agents-v2-py`](containers-and-orchestration/hosted-agents-v2-py/SKILL.md) | Build hosted agents using Azure AI Projects SDK with ImageBasedHostedAgentDefinition. Use when creating container-based agents in Azure AI Foundry. | Hosted Agents V2 Py: Build hosted agents using Azure AI Projects SDK with ImageBasedHostedAgentDefiniti... |
| [`istio-traffic-management`](containers-and-orchestration/istio-traffic-management/SKILL.md) | Comprehensive guide to Istio traffic management for production service mesh deployments. Use when working with istio traffic management. | Istio Traffic Management: Comprehensive guide to Istio traffic management for production service mesh deploy... |
| [`linkerd-patterns`](containers-and-orchestration/linkerd-patterns/SKILL.md) | Production patterns for Linkerd service mesh - the lightweight, security-first service mesh for Kubernetes. Use when working with linkerd patterns. | Linkerd Patterns: Production patterns for Linkerd service mesh - the lightweight, security-first ser... |
| [`service-mesh-expert`](containers-and-orchestration/service-mesh-expert/SKILL.md) | Expert service mesh architect specializing in Istio, Linkerd, and cloud-native networking patterns. Masters traffic management, security policies, observabil... | Service Mesh Expert: Expert service mesh architect specializing in Istio, Linkerd, and cloud-native net... |
| [`service-mesh-observability`](containers-and-orchestration/service-mesh-observability/SKILL.md) | Complete guide to observability patterns for Istio, Linkerd, and service mesh deployments. Use when working with service mesh observability. | Service Mesh Observability: Complete guide to observability patterns for Istio, Linkerd, and service mesh depl... |
| [`sshepherd`](containers-and-orchestration/sshepherd/SKILL.md) | Zero-knowledge SSH ops CLI — server health checks, docker/systemd control, log tailing, Postgres introspection, and declarative deploys, without ever exposin... | Sshepherd: Zero-knowledge SSH ops CLI — server health checks, docker/systemd control, log tai... |
| [`wrangler`](containers-and-orchestration/wrangler/SKILL.md) | Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelin... | Wrangler: Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1... |

### Observability

Manage 15 skills for observability.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`bugs-are-annoying`](observability/bugs-are-annoying/SKILL.md) | Adversarial code auditor that hunts down bugs, logic errors, and security flaws. Use for deep correctness passes, not style reviews. Use when working with bu... | Bugs Are Annoying: Adversarial code auditor that hunts down bugs, logic errors, and security flaws. U... |
| [`build-dashboard`](observability/build-dashboard/SKILL.md) | Build an interactive HTML dashboard with charts, filters, and tables. Use when creating an executive overview with KPI cards, turning query results into a sh... | Build Dashboard: Build an interactive HTML dashboard with charts, filters, and tables. Use when cre... |
| [`database-migrations-migration-observability`](observability/database-migrations-migration-observability/SKILL.md) | Migration monitoring, CDC, and observability infrastructure. Use when working with database migrations migration observability. | Database Migrations Migration Observability: Migration monitoring, CDC, and observability infrastructure. Use when working with... |
| [`distributed-tracing`](../marketing-and-seo/cro/distributed-tracing/SKILL.md) | Implement distributed tracing with Jaeger and Tempo for request flow visibility across microservices. Use when working with distributed tracing. | Distributed Tracing: Implement distributed tracing with Jaeger and Tempo for request flow visibility ac... |
| [`grpc-golang`](observability/grpc-golang/SKILL.md) | Build production-ready gRPC services in Go with mTLS, streaming, and observability. Use when designing Protobuf contracts with Buf or implementing secure ser... | Grpc Golang: Build production-ready gRPC services in Go with mTLS, streaming, and observability... |
| [`incident-responder`](observability/incident-responder/SKILL.md) | Expert SRE incident responder specializing in rapid problem resolution, modern observability, and comprehensive incident management. Use when working with in... | Incident Responder: Expert SRE incident responder specializing in rapid problem resolution, modern obs... |
| [`multi-agent-task-orchestrator`](observability/multi-agent-task-orchestrator/SKILL.md) | Route tasks to specialized AI agents with anti-duplication, quality gates, and 30-minute heartbeat monitoring. Use when working with multi agent task orchest... | Multi Agent Task Orchestrator: Route tasks to specialized AI agents with anti-duplication, quality gates, and 30-... |
| [`observability-and-instrumentation`](observability/observability-and-instrumentation/SKILL.md) | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when shipping any feature tha... | Observability And Instrumentation: Instruments code so production behavior is visible and diagnosable. Use when addin... |
| [`observability-monitoring-monitor-setup`](observability/observability-monitoring-monitor-setup/SKILL.md) | You are a monitoring and observability expert specializing in implementing comprehensive monitoring solutions. Set up metrics collection, distributed tracing... | Observability Monitoring Monitor Setup: You are a monitoring and observability expert specializing in implementing compreh... |
| [`observability-monitoring-slo-implement`](observability/observability-monitoring-slo-implement/SKILL.md) | You are an SLO (Service Level Objective) expert specializing in implementing reliability standards and error budget-based engineering practices. Design compr... | Observability Monitoring Slo Implement: You are an SLO (Service Level Objective) expert specializing in implementing relia... |
| [`performance-engineer`](observability/performance-engineer/SKILL.md) | Expert performance engineer specializing in modern observability,. Use when working with performance engineer. | Performance Engineer: Expert performance engineer specializing in modern observability,. Use when workin... |
| [`shipping-and-launch`](observability/shipping-and-launch/SKILL.md) | Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning... | Shipping And Launch: Prepares production launches. Use when preparing to deploy to production. Use when... |
| [`site-activity`](observability/site-activity/SKILL.md) | Query and summarize site activity logs for a Webflow enterprise site. Surfaces recent changes, identifies who made them, and generates human-readable activit... | Site Activity: Query and summarize site activity logs for a Webflow enterprise site. Surfaces rec... |
| [`vercel-cli-with-tokens`](observability/vercel-cli-with-tokens/SKILL.md) | Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login — e... | Vercel Cli With Tokens: Deploy and manage projects on Vercel using token-based authentication. Use when wo... |
| [`workers-best-practices`](observability/workers-best-practices/SKILL.md) | Reviews and authors Cloudflare Workers code against production best practices. Load when writing new Workers, reviewing Worker code, configuring wrangler.jso... | Workers Best Practices: Reviews and authors Cloudflare Workers code against production best practices. Loa... |

### Server Management

Manage 6 skills for server management.

| Skill | Description | Primary Outcome |
|---|---|---|
| [`agents-sdk`](server-management/agents-sdk/SKILL.md) | Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks,... | Agents Sdk: Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating sta... |
| [`bash-linux`](server-management/bash-linux/SKILL.md) | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. | Bash Linux: Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting... |
| [`linux-privilege-escalation`](server-management/linux-privilege-escalation/SKILL.md) | Execute systematic privilege escalation assessments on Linux systems to identify and exploit misconfigurations, vulnerable services, and security weaknesses ... | Linux Privilege Escalation: Execute systematic privilege escalation assessments on Linux systems to identify a... |
| [`pm2`](server-management/pm2/SKILL.md) | Execute pm2 tasks, workflows, and automated procedures. Use when working with pm2. | Pm2: Execute pm2 tasks, workflows, and automated procedures. Use when working with pm2 |
| [`react-best-practices`](server-management/react-best-practices/SKILL.md) | Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Use when writing new React components or Next.js pages... | React Best Practices: Comprehensive performance optimization guide for React and Next.js applications, m... |
| [`server-management`](server-management/server-management/SKILL.md) | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. Use when wo... | Server Management: Server management principles and decision-making. Process management, monitoring s... |

---
*Part of the Canonical Agent Skills Hierarchy.*
