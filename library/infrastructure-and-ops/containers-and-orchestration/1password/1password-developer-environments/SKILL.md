---
name: 1password-developer-environments
description: 'Manage 1Password Developer Environments for project environment variables using TypeScript (Bun) and Python SDK tools. Use when creating, updating, exporting, or resolving project secrets programmatically across development environments.'
compatibility: 'Requires Bun or Python 3.9+ with OP_SERVICE_ACCOUNT_TOKEN.'
metadata:
  category: infrastructure-and-ops
  type: execution-child
  source: custom
---

# 1Password Developer Environments

Manage project secrets and environment variables using TypeScript (Bun) and Python SDK tooling.

## Feature Overview

1Password Developer Environments enable multi-variable secret synchronization, masking, and export across project workspaces.

## When to Use

- Creating, listing, inspecting, updating, exporting, and deleting developer environments
- Exporting environments to `.env`, Docker-compatible, or `op://` reference formats
- Programmatic secret resolution via `SecretsManager` in Python services and TypeScript tools

## Tool Setup

### CLI Tools Setup (TypeScript)
```bash
cd tools
bun run create -- --help
bun run list -- --help
bun run show -- --help
bun run update -- --help
bun run export -- --help
bun run delete -- --help
```

### CLI Tools Setup (Python SDK)
```bash
cd tools-python
uv sync
uv run op-env-create --help
uv run op-env-list --help
uv run op-env-show --help
uv run op-env-update --help
uv run op-env-export --help
uv run op-env-delete --help
```

### When to Use SDK vs CLI
Use TypeScript (Bun) tools for rapid local scripting and CLI workflows. Use Python SDK (`SecretsManager`) for direct application integration and Python automated services.

### SecretsManager (Python SDK)
```python
from op_env.secrets_manager import SecretsManager

async def main():
    sm = await SecretsManager.create()
    api_key = await sm.get("op://Production/API/key")
    env = await sm.resolve_environment("my-app-prod", "Production")
```

## Environment Workflow

### 1. Create Environment
```bash
bun run create --name my-app-dev --vault Development --env-file .env.dev
```

### 2. List Environments
```bash
bun run list --vault Development
```

### 3. Show Environment Details
```bash
bun run show --name my-app-dev --reveal
```

### 4. Update Environment
```bash
bun run update --name my-app-dev --set "NEW_KEY=value" --merge-file .env.updates
```

### 5. Export Environment
```bash
bun run export --name my-app-dev --format op-refs --output .env.template
```

### 6. Delete Environment
```bash
bun run delete --name my-app-dev --force
```

## Environment Secret Reference
Reference environment variables with `op://<vault>/<env-item>/<var-name>`.

## Integration Patterns

- **With op run (recommended)**: Export environment as `op://` reference template and launch with `op run --env-file=.env.template -- npm start`.
- **With op inject**: Populate runtime config files before container launch.
- **With Docker Compose**: Populate environment variables using `./templates/docker-compose-env.yaml`.
- **In CI/CD (GitHub Actions)**: Inject environment secrets into workflows via `1password/load-secrets-action`.

## Current Environments (Barbosa Account)
Documented project environments and vault assignments are detailed in `./references/environments/inventory.md`.

## Completion Evidence

- Validated environment creation or export.
- Verified secret resolution matching `.env.template`.
