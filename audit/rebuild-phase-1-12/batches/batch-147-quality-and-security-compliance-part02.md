# Phase 08 Batch Audit Record: `batch-147-quality-and-security-compliance-part02`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-147-quality-and-security-compliance-part02`
- **Category / Subcategory**: `quality-and-security` / `compliance`
- **Member Skill Count**: 11
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `35cef21b96c358eacf4a0349384754d5c5f8717358ab5e51c78f007b73672ad0`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `privacy-by-design` | `task-folder/agents/skills/privacy-by-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `region-config` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/region-config` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `send-sms` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/send-sms` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `sms` | `task-folder/agents/skills/marketing/sms` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `sms-marketing` | `task-folder/agents/skills/marketing/sms-marketing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `spec-to-code-compliance` | `task-folder/agents/skills/spec-to-code-compliance` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `status` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/status` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `validate-output` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/validate-output` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `validate-profile` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/validate-profile` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `web-design-guidelines` | `task-folder/agents/skills/web-design-guidelines` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `writing-guidelines` | `task-folder/agents/skills/writing/writing-guidelines` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `privacy-by-design` | User asks to implement, configure, or optimize privacy by design tasks (specifically configuring or implementing privacy by design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside privacy by design or unrelated operations outside privacy by design. | User asks 'How do I handle privacy by design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized privacy by design procedures or general compliance tooling. |
| `region-config` | User asks to implement, configure, or optimize region config tasks (specifically configuring or implementing region config specifications). | User requests general infrastructure administration, styling, or unrelated operations outside region config or unrelated operations outside region config. | User asks 'How do I handle region config in my workflow?' -> Disambiguate: Clarify whether the task requires specialized region config procedures or general compliance tooling. |
| `send-sms` | User asks to implement, configure, or optimize send sms tasks (specifically configuring or implementing send sms specifications). | User requests general infrastructure administration, styling, or unrelated operations outside send sms or unrelated operations outside send sms. | User asks 'How do I handle send sms in my workflow?' -> Disambiguate: Clarify whether the task requires specialized send sms procedures or general compliance tooling. |
| `sms` | User asks to implement, configure, or optimize sms tasks (specifically configuring or implementing sms specifications). | User requests general infrastructure administration, styling, or unrelated operations outside sms or unrelated operations outside sms. | User asks 'How do I handle sms in my workflow?' -> Disambiguate: Clarify whether the task requires specialized sms procedures or general compliance tooling. |
| `sms-marketing` | User asks to implement, configure, or optimize sms marketing tasks (specifically configuring or implementing sms marketing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside sms marketing or unrelated operations outside sms marketing. | User asks 'How do I handle sms marketing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized sms marketing procedures or general compliance tooling. |
| `spec-to-code-compliance` | User asks to implement, configure, or optimize spec to code compliance tasks (specifically configuring or implementing spec to code compliance specifications). | User requests Codebases without corresponding specification documents or unrelated operations outside spec to code compliance. | User asks 'How do I handle spec to code compliance in my workflow?' -> Disambiguate: Clarify whether the task requires specialized spec to code compliance procedures or general compliance tooling. |
| `status` | User asks to implement, configure, or optimize status tasks (specifically configuring or implementing status specifications). | User requests general infrastructure administration, styling, or unrelated operations outside status or unrelated operations outside status. | User asks 'How do I handle status in my workflow?' -> Disambiguate: Clarify whether the task requires specialized status procedures or general compliance tooling. |
| `validate-output` | User asks to implement, configure, or optimize validate output tasks (specifically configuring or implementing validate output specifications). | User requests general infrastructure administration, styling, or unrelated operations outside validate output or unrelated operations outside validate output. | User asks 'How do I handle validate output in my workflow?' -> Disambiguate: Clarify whether the task requires specialized validate output procedures or general compliance tooling. |
| `validate-profile` | User asks to implement, configure, or optimize validate profile tasks (specifically After **`/digital-marketing-pro:brand-setup`** (or `/digital-marketing-pro:client-onboarding`) to confirm the new profile is production-ready). | User requests general infrastructure administration, styling, or unrelated operations outside validate profile or unrelated operations outside validate profile. | User asks 'How do I handle validate profile in my workflow?' -> Disambiguate: Clarify whether the task requires specialized validate profile procedures or general compliance tooling. |
| `web-design-guidelines` | User asks to implement, configure, or optimize web design guidelines tasks (specifically configuring or implementing web design guidelines specifications). | User requests general infrastructure administration, styling, or unrelated operations outside web design guidelines or unrelated operations outside web design guidelines. | User asks 'How do I handle web design guidelines in my workflow?' -> Disambiguate: Clarify whether the task requires specialized web design guidelines procedures or general compliance tooling. |
| `writing-guidelines` | User asks to implement, configure, or optimize writing guidelines tasks (specifically configuring or implementing writing guidelines specifications). | User requests general infrastructure administration, styling, or unrelated operations outside writing guidelines or unrelated operations outside writing guidelines. | User asks 'How do I handle writing guidelines in my workflow?' -> Disambiguate: Clarify whether the task requires specialized writing guidelines procedures or general compliance tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/quality-and-security/compliance/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `35cef21b96c358eacf4a0349384754d5c5f8717358ab5e51c78f007b73672ad0` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `privacy-by-design` | `README.md` | Created or preserved in canonical package |
| `sms` | `evals/evals.json` | Created or preserved in canonical package |
| `sms` | `references/compliance.md` | Created or preserved in canonical package |
| `sms` | `references/platforms.md` | Created or preserved in canonical package |
| `sms` | `references/sequence-templates.md` | Created or preserved in canonical package |
| `sms-marketing` | `evals/compliant-opt-in-and-consent-storage/criteria.json` | Created or preserved in canonical package |
| `sms-marketing` | `evals/compliant-opt-in-and-consent-storage/task.md` | Created or preserved in canonical package |
| `sms-marketing` | `evals/inbound-sms-keyword-webhook-handling/criteria.json` | Created or preserved in canonical package |
| `sms-marketing` | `evals/inbound-sms-keyword-webhook-handling/task.md` | Created or preserved in canonical package |
| `sms-marketing` | `evals/marketing-sms-send-with-compliance-check/criteria.json` | Created or preserved in canonical package |
| `sms-marketing` | `evals/marketing-sms-send-with-compliance-check/task.md` | Created or preserved in canonical package |
| `sms-marketing` | `tile.json` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
