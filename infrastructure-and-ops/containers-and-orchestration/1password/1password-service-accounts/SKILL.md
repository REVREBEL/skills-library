---
name: 1password-service-accounts
description: 'Configure 1Password Service Accounts for CI/CD automation, GitHub Actions, GitLab CI, CircleCI, and container environments. Use when provisioning service account tokens and configuring automated secret injection.'
compatibility: 'Requires 1Password CLI v2+ with service account admin permissions.'
metadata:
  category: infrastructure-and-ops
  type: execution-child
  source: custom
---

# 1Password Service Accounts

Automate secret access in CI/CD pipelines and automated environments using Service Account tokens.

## When to Use

- Provisioning service account tokens with scoped vault permissions
- Integrating 1Password into GitHub Actions workflows
- Configuring GitLab CI/CD, CircleCI, or Docker container secret injection
- Managing service account token rotation and access policies

## Service Accounts

### Prerequisites
- 1Password Developer or Business account
- Administrative rights to create Service Accounts and issue access tokens

### Creating Service Accounts
1. Create a service account in 1Password Developer Settings with explicit vault access.
2. Run setup script: `bash ./scripts/setup-service-account.sh`.
3. Set token in target environment: `export OP_SERVICE_ACCOUNT_TOKEN="<token>"`.

### Using Service Accounts
Service accounts automatically authenticate `op` CLI commands when `OP_SERVICE_ACCOUNT_TOKEN` is present in the environment.

### Service Account Limitations
- Service accounts cannot perform interactive operations requiring user biometric authorization.
- Token scope is restricted strictly to explicitly authorized vaults.

## CI/CD Integration

### GitHub Actions
```yaml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: 1password/load-secrets-action@v2
        with:
          export-env: true
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
          DB_PASSWORD: "op://Production/Database/password"
          API_KEY: "op://Production/Stripe/api_key"
      - run: npm run deploy
```

### GitLab CI
```yaml
deploy:
  image: 1password/op:2
  script:
    - export OP_SERVICE_ACCOUNT_TOKEN=$OP_SERVICE_ACCOUNT_TOKEN
    - op read "op://Production/Database/password"
```

### CircleCI
Configure `OP_SERVICE_ACCOUNT_TOKEN` in Project Environment Variables and use the `1password` orb.

## Troubleshooting

- **Token Invalid**: Verify `OP_SERVICE_ACCOUNT_TOKEN` matches 1Password Developer settings.
- **Vault Access Denied**: Verify service account is granted read permissions on target vault.
- **Diagnostics**: Run `bash ./scripts/sync-check.sh` to verify service account token status.

## Completion Evidence

- Verified workflow execution with secrets injected in CI runner.
- Zero secret exposure in CI build logs.
