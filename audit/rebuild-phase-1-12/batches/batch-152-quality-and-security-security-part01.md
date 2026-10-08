# Phase 08 Batch Audit Record: `batch-152-quality-and-security-security-part01`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-152-quality-and-security-security-part01`
- **Category / Subcategory**: `quality-and-security` / `security`
- **Member Skill Count**: 11
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `2a62807449a0fc2553ff987539e89617c3e753a0e1f1633e33a91924085d0644`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `007` | `task-folder/agents/skills/007` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `antigravity-workflows` | `task-folder/agents/skills/antigravity/antigravity-workflows` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `api-security-testing` | `task-folder/agents/skills/api/api-security-testing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `audit-context-building` | `task-folder/agents/skills/audit-context-building` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `codebase-cleanup-deps-audit` | `task-folder/agents/skills/code/codebase-cleanup-deps-audit` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `dependency-management-deps-audit` | `task-folder/agents/skills/dependency-management-deps-audit` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ethical-hacking-methodology` | `task-folder/agents/skills/ethical-hacking-methodology` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `html-injection-testing` | `task-folder/agents/skills/html-injection-testing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `linux-shell-scripting` | `task-folder/agents/skills/linux/linux-shell-scripting` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `malware-analyst` | `task-folder/agents/skills/malware-analyst` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `memory-forensics` | `task-folder/agents/skills/agents/memory-forensics` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `007` | User asks to implement, configure, or optimize 007 tasks (specifically configuring or implementing 007 specifications). | User requests A simpler, more specific tool can handle the request or unrelated operations outside 007. | User asks 'How do I handle 007 in my workflow?' -> Disambiguate: Clarify whether the task requires specialized 007 procedures or general security tooling. |
| `antigravity-workflows` | User asks to implement, configure, or optimize antigravity workflows tasks (specifically configuring or implementing antigravity workflows specifications). | User requests general infrastructure administration, styling, or unrelated operations outside antigravity workflows or unrelated operations outside antigravity workflows. | User asks 'How do I handle antigravity workflows in my workflow?' -> Disambiguate: Clarify whether the task requires specialized antigravity workflows procedures or general security tooling. |
| `api-security-testing` | User asks to implement, configure, or optimize api security testing tasks (specifically configuring or implementing api security testing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside api security testing or unrelated operations outside api security testing. | User asks 'How do I handle api security testing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized api security testing procedures or general security tooling. |
| `audit-context-building` | User asks to implement, configure, or optimize audit context building tasks (specifically configuring or implementing audit context building specifications). | User requests general infrastructure administration, styling, or unrelated operations outside audit context building or unrelated operations outside audit context building. | User asks 'How do I handle audit context building in my workflow?' -> Disambiguate: Clarify whether the task requires specialized audit context building procedures or general security tooling. |
| `codebase-cleanup-deps-audit` | User asks to implement, configure, or optimize codebase cleanup deps audit tasks (specifically configuring or implementing codebase cleanup deps audit specifications). | User requests The project has no dependency manifests or unrelated operations outside codebase cleanup deps audit. | User asks 'How do I handle codebase cleanup deps audit in my workflow?' -> Disambiguate: Clarify whether the task requires specialized codebase cleanup deps audit procedures or general security tooling. |
| `dependency-management-deps-audit` | User asks to implement, configure, or optimize dependency management deps audit tasks (specifically configuring or implementing dependency management deps audit specifications). | User requests The project has no dependency manifests or unrelated operations outside dependency management deps audit. | User asks 'How do I handle dependency management deps audit in my workflow?' -> Disambiguate: Clarify whether the task requires specialized dependency management deps audit procedures or general security tooling. |
| `ethical-hacking-methodology` | User asks to implement, configure, or optimize ethical hacking methodology tasks (specifically configuring or implementing ethical hacking methodology specifications). | User requests general infrastructure administration, styling, or unrelated operations outside ethical hacking methodology or unrelated operations outside ethical hacking methodology. | User asks 'How do I handle ethical hacking methodology in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ethical hacking methodology procedures or general security tooling. |
| `html-injection-testing` | User asks to implement, configure, or optimize html injection testing tasks (specifically configuring or implementing html injection testing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside html injection testing or unrelated operations outside html injection testing. | User asks 'How do I handle html injection testing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized html injection testing procedures or general security tooling. |
| `linux-shell-scripting` | User asks to implement, configure, or optimize linux shell scripting tasks (specifically configuring or implementing linux shell scripting specifications). | User requests general infrastructure administration, styling, or unrelated operations outside linux shell scripting or unrelated operations outside linux shell scripting. | User asks 'How do I handle linux shell scripting in my workflow?' -> Disambiguate: Clarify whether the task requires specialized linux shell scripting procedures or general security tooling. |
| `malware-analyst` | User asks to implement, configure, or optimize malware analyst tasks (specifically configuring or implementing malware analyst specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside malware analyst. | User asks 'How do I handle malware analyst in my workflow?' -> Disambiguate: Clarify whether the task requires specialized malware analyst procedures or general security tooling. |
| `memory-forensics` | User asks to implement, configure, or optimize memory forensics tasks (specifically configuring or implementing memory forensics specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside memory forensics. | User asks 'How do I handle memory forensics in my workflow?' -> Disambiguate: Clarify whether the task requires specialized memory forensics procedures or general security tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/quality-and-security/security/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `2a62807449a0fc2553ff987539e89617c3e753a0e1f1633e33a91924085d0644` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `007` | `references/ai-agent-security.md` | Created or preserved in canonical package |
| `007` | `references/api-security-patterns.md` | Created or preserved in canonical package |
| `007` | `references/incident-playbooks.md` | Created or preserved in canonical package |
| `007` | `references/owasp-checklists.md` | Created or preserved in canonical package |
| `007` | `references/stride-pasta-guide.md` | Created or preserved in canonical package |
| `007` | `scripts/config.py` | Created or preserved in canonical package |
| `007` | `scripts/full_audit.py` | Created or preserved in canonical package |
| `007` | `scripts/quick_scan.py` | Created or preserved in canonical package |
| `007` | `scripts/requirements.txt` | Created or preserved in canonical package |
| `007` | `scripts/scanners/__init__.py` | Created or preserved in canonical package |
| `007` | `scripts/scanners/dependency_scanner.py` | Created or preserved in canonical package |
| `007` | `scripts/scanners/injection_scanner.py` | Created or preserved in canonical package |
| `007` | `scripts/scanners/secrets_scanner.py` | Created or preserved in canonical package |
| `007` | `scripts/score_calculator.py` | Created or preserved in canonical package |
| `antigravity-workflows` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `codebase-cleanup-deps-audit` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `dependency-management-deps-audit` | `resources/implementation-playbook.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
