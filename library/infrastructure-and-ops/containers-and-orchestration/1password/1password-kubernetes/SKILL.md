---
name: 1password-kubernetes
description: 'Configure and deploy Kubernetes secret synchronization using the native 1Password Operator and External Secrets Operator (ESO). Use when injecting 1Password secrets into Kubernetes cluster secrets, CRDs, or pod volumes.'
compatibility: 'Requires Kubernetes cluster access, Helm, and 1Password Connect or ESO CRDs.'
metadata:
  category: infrastructure-and-ops
  type: execution-child
  source: custom
---

# 1Password Kubernetes Integration

Synchronize 1Password secrets with Kubernetes clusters using External Secrets Operator (ESO) or native 1Password Operator.

## When to Use

- Deploying 1Password Connect server in Kubernetes
- Configuring External Secrets Operator (ESO) `SecretStore`, `ClusterSecretStore`, and `ExternalSecret` manifests
- Configuring PushSecret (Kubernetes to 1Password)
- Deploying the native 1Password Kubernetes Operator with `OnePasswordItem` CRDs and auto-restart annotations

## Prerequisites

- Active Kubernetes cluster (v1.24+)
- `kubectl` and `helm` v3 installed
- 1Password Connect credentials token (`1password-credentials.json`)

## External Secrets Operator Integration

### Connect Server Setup & Deploy Connect Server
1. Create automation environment credentials: generates `1password-credentials.json` and access token.
2. Create Kubernetes secrets:
   ```bash
   kubectl create secret generic op-connect-token --from-literal=token="<TOKEN>"
   kubectl create secret generic op-credentials --from-file=1password-credentials.json
   ```
3. Deploy Connect server via Helm:
   ```bash
   helm repo add 1password https://1password.github.io/connect-helm-charts/
   helm install connect 1password/connect --set connect.credentials=op-credentials
   ```

### ClusterSecretStore Configuration & ExternalSecret Examples
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: onepassword
spec:
  provider:
    onepassword:
      connectHost: http://onepassword-connect:8080
      vaults:
        Production: 1
      auth:
        secretRef:
          connectTokenSecretRef:
            name: op-connect-token
            namespace: default
            key: token
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: onepassword
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: Production/Database
        property: password
```

### PushSecret (Kubernetes to 1Password)
Synchronize Kubernetes-generated secrets back to 1Password vaults using `PushSecret` CRDs.

## 1Password Kubernetes Operator

### Installation via Helm
```bash
helm repo add 1password https://1password.github.io/connect-helm-charts/
helm install op-operator 1password/onepassword-operator
```

### OnePasswordItem CRD
```yaml
apiVersion: onepassword.com/v1
kind: OnePasswordItem
metadata:
  name: database-credentials
spec:
  itemPath: "vaults/Production/items/Database"
```

### Auto-Restart Configuration
- Add deployment annotation: `operator.1password.io/auto-restart: "true"` to trigger pod rollout on secret update.

## Troubleshooting

- Check ExternalSecret status: `kubectl get externalsecret -A`.
- Check Connect Server logs: `kubectl logs -l app.kubernetes.io/name=connect`.

## Completion Evidence

- Kubernetes secret created and synchronized.
- Verified status `Synced` in `kubectl get externalsecret app-secrets`.
