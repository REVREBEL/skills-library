---
name: "1password"
description: "Route 1Password secrets management requests across CLI retrieval, Developer Environments, Kubernetes integrations, and Service Account CI/CD workflows. Use when determining the correct 1Password workflow for local development, environment variable sync, Kubernetes secret injection, or automated deployments."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# 1Password

Route secrets management tasks to the appropriate specialized 1Password child skill.

## Overview

1Password provides centralized secrets management across local development workstations, developer project environments, Kubernetes clusters, and automated CI/CD pipelines.

## Quick Reference & Routing Switchboard

### Command Structure

- `op read "op://<vault>/<item>/<field>"` -> Secret retrieval in CLI
- `bun run create / uv run op-env-create` -> Developer environment variable synchronization
- `kubectl apply -f externalsecret.yaml` -> Kubernetes secret injection
- `1password/load-secrets-action` -> GitHub Actions & CI/CD pipeline automation

## Workflow Decision Tree

| User Goal | Tool / Runtime | Specialized Child Skill |
|---|---|---|
| Retrieve single secret (`op read`), run commands with env vars (`op run`), manage items/vaults, configure shell plugins | `op` CLI | [1Password CLI](./1password-cli/SKILL.md) |
| Manage project environment variables, sync `.env` files, bulk resolve via Python SDK/TypeScript CLI | Bun / Python SDK CLI | [1Password Developer Environments](./1password-developer-environments/SKILL.md) |
| Inject secrets into Kubernetes pods, configure ExternalSecret or OnePasswordItem CRDs | K8s Operator / ESO | [1Password Kubernetes](./1password-kubernetes/SKILL.md) |
| CI/CD pipeline automation (GitHub Actions, GitLab CI) with scoped service account tokens | Service Account Token | [1Password Service Accounts](./1password-service-accounts/SKILL.md) |

## Best Practices

- **Zero Credential Exposure**: Never log, print, or commit raw tokens or secrets.
- **Principle of Least Privilege**: Grant service accounts access only to the specific vaults required.
- **Environment Isolation**: Separate Production, Staging, and Development secrets into distinct vaults.
- **Troubleshooting & Support**: Refer to individual child skills for service-specific troubleshooting, error codes, and health checks.

## Resources

- **References**: Standard CLI command syntax and Python SDK references in child packages.
- **Tools**: Bundled TypeScript and Python environment sync tools in `1password-developer-environments/tools`.
- **Templates**: Docker Compose, environment file, and GitHub Actions templates in child directories.
- **Scripts**: Helper provisioning scripts in `1password-service-accounts/scripts` and `1password-cli/scripts`.
- **External Documentation**: 1Password Developer Documentation and 1Password CLI reference.
