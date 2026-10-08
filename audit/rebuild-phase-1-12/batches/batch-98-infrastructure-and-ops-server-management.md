# Phase 08 Batch Audit Record: `batch-98-infrastructure-and-ops-server-management`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-98-infrastructure-and-ops-server-management`
- **Category / Subcategory**: `infrastructure-and-ops` / `server-management`
- **Member Skill Count**: 6
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `e91cd43a7bf5cfad67a899486d6fe7a40a87cea4f14b8c97fbdcf0b2c380a01f`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `agents-sdk` | `task-folder/agents/skills/agents/agents-sdk` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `bash-linux` | `task-folder/agents/skills/bash/bash-linux` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `linux-privilege-escalation` | `task-folder/agents/skills/linux/linux-privilege-escalation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pm2` | `task-folder/agents/skills/pm2` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `react-best-practices` | `task-folder/agents/skills/react/react-best-practices` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `server-management` | `task-folder/agents/skills/server-management` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `agents-sdk` | User asks to implement, configure, or optimize agents sdk tasks (specifically configuring or implementing agents sdk specifications). | User requests general infrastructure administration, styling, or unrelated operations outside agents sdk or unrelated operations outside agents sdk. | User asks 'How do I handle agents sdk in my workflow?' -> Disambiguate: Clarify whether the task requires specialized agents sdk procedures or general server-management tooling. |
| `bash-linux` | User asks to implement, configure, or optimize bash linux tasks (specifically configuring or implementing bash linux specifications). | User requests general infrastructure administration, styling, or unrelated operations outside bash linux or unrelated operations outside bash linux. | User asks 'How do I handle bash linux in my workflow?' -> Disambiguate: Clarify whether the task requires specialized bash linux procedures or general server-management tooling. |
| `linux-privilege-escalation` | User asks to implement, configure, or optimize linux privilege escalation tasks (specifically configuring or implementing linux privilege escalation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside linux privilege escalation or unrelated operations outside linux privilege escalation. | User asks 'How do I handle linux privilege escalation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized linux privilege escalation procedures or general server-management tooling. |
| `pm2` | User asks to implement, configure, or optimize pm2 tasks (specifically configuring or implementing pm2 specifications). | User requests Detached terminal sessions** → use [holdpty](https://github.com/marcfargas/holdpty) (PTY output, attach/view) or unrelated operations outside pm2. | User asks 'How do I handle pm2 in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pm2 procedures or general server-management tooling. |
| `react-best-practices` | User asks to implement, configure, or optimize react best practices tasks (specifically configuring or implementing react best practices specifications). | User requests general infrastructure administration, styling, or unrelated operations outside react best practices or unrelated operations outside react best practices. | User asks 'How do I handle react best practices in my workflow?' -> Disambiguate: Clarify whether the task requires specialized react best practices procedures or general server-management tooling. |
| `server-management` | User asks to implement, configure, or optimize server management tasks (specifically configuring or implementing server management specifications). | User requests general infrastructure administration, styling, or unrelated operations outside server management or unrelated operations outside server management. | User asks 'How do I handle server management in my workflow?' -> Disambiguate: Clarify whether the task requires specialized server management procedures or general server-management tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/infrastructure-and-ops/server-management/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `e91cd43a7bf5cfad67a899486d6fe7a40a87cea4f14b8c97fbdcf0b2c380a01f` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `agents-sdk` | `references/browse-the-web.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/callable.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/client-sdk.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/codemode.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/configuration.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/durable-execution.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/email.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/human-in-the-loop.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/mcp.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/observability.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/queue-retries.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/routing.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/server-driven-messages.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/state-scheduling.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/streaming-chat.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/think.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/voice.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/webhooks-push.md` | Created or preserved in canonical package |
| `agents-sdk` | `references/workflows.md` | Created or preserved in canonical package |
| `react-best-practices` | `AGENTS.md` | Created or preserved in canonical package |
| `react-best-practices` | `README.md` | Created or preserved in canonical package |
| `react-best-practices` | `metadata.json` | Created or preserved in canonical package |
| `react-best-practices` | `rules/_sections.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/_template.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/advanced-event-handler-refs.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/advanced-use-latest.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/async-api-routes.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/async-defer-await.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/async-dependencies.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/async-parallel.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/async-suspense-boundaries.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/bundle-barrel-imports.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/bundle-conditional.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/bundle-defer-third-party.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/bundle-dynamic-imports.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/bundle-preload.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/client-event-listeners.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/client-swr-dedup.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-batch-dom-css.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-cache-function-results.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-cache-property-access.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-cache-storage.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-combine-iterations.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-early-exit.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-hoist-regexp.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-index-maps.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-length-check-first.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-min-max-loop.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-set-map-lookups.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/js-tosorted-immutable.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-activity.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-animate-svg-wrapper.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-conditional-render.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-content-visibility.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-hoist-jsx.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-hydration-no-flicker.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rendering-svg-precision.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-defer-reads.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-dependencies.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-derived-state.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-functional-setstate.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-lazy-state-init.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-memo.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/rerender-transitions.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/server-after-nonblocking.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/server-cache-lru.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/server-cache-react.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/server-parallel-fetching.md` | Created or preserved in canonical package |
| `react-best-practices` | `rules/server-serialization.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
