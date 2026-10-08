---
name: 1password-cli
description: 'Execute 1Password CLI (op) operations for local development, secret retrieval, item/vault CRUD, configuration injection, shell plugins, and git credential workflows. Use when running op read, op run, op inject, managing items/vaults/documents, or configuring developer shell plugins.'
compatibility: 'Requires 1Password CLI v2+ installed and authenticated via op signin.'
metadata:
  category: infrastructure-and-ops
  type: execution-child
  source: custom
---

# 1Password CLI

Retrieve secrets and manage 1Password items, vaults, and documents using the native `op` CLI.

## When to Use

- Reading individual secret fields (`op read`)
- Running local processes with injected secrets (`op run`)
- Populating configuration templates (`op inject`)
- Creating, editing, or inspecting vaults, items, and documents
- Configuring developer shell plugins (AWS, GitHub, Stripe) and Git credential helpers

## Quick Reference & Command Structure

```bash
# Authentication
op whoami || eval $(op signin)

# Secret Retrieval
op read "op://<vault>/<item>/<field>"
op run --env-file=.env.template -- <command>
op inject -i template.env -o .env

# Item & Vault Management
op item list --vault "<vault>"
op item get "<item>"
op item create --category login --title "<title>" --vault "<vault>"
op item edit "<item>" "<field>=<value>"
op vault list
op vault get "<vault>"
op document get "<doc-name>" --out-file ./secret.pem
```

## Secret Retrieval

### Secret Reference Format
The canonical URI structure is: `op://<vault>/<item>/[section/]<field>`.

### Reading Secrets Directly
```bash
# Read specific field
op read "op://Development/Database/password"

# Read formatted JSON
op item get "Database" --format json
```

### Injecting Secrets into Commands
Use `.env.tpl` references:
```bash
AWS_ACCESS_KEY_ID=op://Development/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Development/AWS/secret_access_key
```
Execute with:
```bash
op run --env-file=.env.tpl -- npm start
```

### Injecting Secrets into Files
```bash
op inject -i config.tpl.yaml -o config.yaml
```

## Item Management

### Creating Items
Create items from the CLI or item template JSON:
```bash
op item create --category login --title "Database Admin" --vault "Development"
```

### Item Template (JSON)
Export or apply item templates in standard 1Password JSON schema.

### Editing Items
```bash
op item edit "Database Admin" "password=new-secret-value"
```

## Shell Plugins

### Available Plugins
Plugins available for AWS, GitHub, Stripe, Vercel, and Fly.

### Plugin Setup
```bash
op plugin init aws
op plugin init gh
```

## Git Workflow with 1Password

### Quick Setup & Manual Setup
- **Step 1: Initialize the gh plugin**: `op plugin init gh`.
- **Step 2: Configure git credential helper**:
  ```bash
  git config --global credential.helper ""
  git config --global credential.https://github.com.helper "!gh auth git-credential"
  ```
- **Step 3: Add shell integration**: Add `source ~/.config/op/plugins.sh` to shell rc.

### How It Works
The Git credential helper intercepts HTTPS authorization requests and delegates authentication directly to the authenticated 1Password CLI session.

### Multiple GitHub Accounts
Use conditional includes in `~/.gitconfig` based on repository directory path.

### Fixing Common Issues
- **"Item not found in vault" error**: Run `op item list --vault "<vault>"` to find UUID.
- **gh aliased to op plugin run**: Run `\gh` or execute full binary path to bypass alias.
- **Git prompting for username/password**: Check credential helper configuration with `git config -l`.

## Troubleshooting

### Common Issues
- **Session Expired**: Run `eval $(op signin)`.
- **Item Not Found**: Check item ID with `op item list --vault "<vault>"`. Use item UUID instead of name for deterministic lookup.
- **Broken Plugin Configuration**: Reset configuration with `op plugin init <plugin> --reset`.

## Completion Evidence

- Exit code 0 from `op` command.
- Verified secret injection without stdout/terminal exposure.
