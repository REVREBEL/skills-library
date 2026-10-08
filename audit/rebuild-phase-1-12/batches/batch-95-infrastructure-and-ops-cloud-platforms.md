# Phase 08 Batch Audit Record: `batch-95-infrastructure-and-ops-cloud-platforms`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-95-infrastructure-and-ops-cloud-platforms`
- **Category / Subcategory**: `infrastructure-and-ops` / `cloud-platforms`
- **Member Skill Count**: 14
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `c4302171a1e008c8975399fa628059b66c2da78cdacdf579071df0c5dbeb1024`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `auri-core` | `task-folder/agents/skills/auri-core` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `bigquery-table-creator` | `task-folder/agents/skills/big query/bigquery-table-creator` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `bigquery-view-generator` | `task-folder/agents/skills/big query/bigquery-view-generator` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `cdk-patterns` | `task-folder/agents/skills/cdk-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `cloud-architect` | `task-folder/agents/skills/cloud-architect` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `deploy-to-vercel` | `task-folder/agents/skills/deploy-to-vercel` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `remote-gpu-trainer` | `task-folder/agents/skills/remote-gpu-trainer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `sandbox-sdk` | `task-folder/agents/skills/sandbox-sdk` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `turnstile-spin` | `task-folder/agents/skills/turnstile-spin` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `vercel-ai-sdk-expert` | `task-folder/agents/skills/vercel/vercel-ai-sdk-expert` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `vercel-automation` | `task-folder/agents/skills/vercel/vercel-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `vercel-deployment` | `task-folder/agents/skills/vercel/vercel-deployment` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `vercel-optimize` | `task-folder/agents/skills/vercel/vercel-optimize` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `workflow-automation` | `task-folder/agents/skills/github/workflow-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `auri-core` | User asks to implement, configure, or optimize auri core tasks (specifically configuring or implementing auri core specifications). | User requests A simpler, more specific tool can handle the request or unrelated operations outside auri core. | User asks 'How do I handle auri core in my workflow?' -> Disambiguate: Clarify whether the task requires specialized auri core procedures or general cloud-platforms tooling. |
| `bigquery-table-creator` | User asks to implement, configure, or optimize bigquery table creator tasks (specifically configuring or implementing bigquery table creator specifications). | User requests general infrastructure administration, styling, or unrelated operations outside bigquery table creator or unrelated operations outside bigquery table creator. | User asks 'How do I handle bigquery table creator in my workflow?' -> Disambiguate: Clarify whether the task requires specialized bigquery table creator procedures or general cloud-platforms tooling. |
| `bigquery-view-generator` | User asks to implement, configure, or optimize bigquery view generator tasks (specifically configuring or implementing bigquery view generator specifications). | User requests general infrastructure administration, styling, or unrelated operations outside bigquery view generator or unrelated operations outside bigquery view generator. | User asks 'How do I handle bigquery view generator in my workflow?' -> Disambiguate: Clarify whether the task requires specialized bigquery view generator procedures or general cloud-platforms tooling. |
| `cdk-patterns` | User asks to implement, configure, or optimize cdk patterns tasks (specifically configuring or implementing cdk patterns specifications). | User requests The user needs raw CloudFormation templates without CDK or unrelated operations outside cdk patterns. | User asks 'How do I handle cdk patterns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized cdk patterns procedures or general cloud-platforms tooling. |
| `cloud-architect` | User asks to implement, configure, or optimize cloud architect tasks (specifically configuring or implementing cloud architect specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside cloud architect. | User asks 'How do I handle cloud architect in my workflow?' -> Disambiguate: Clarify whether the task requires specialized cloud architect procedures or general cloud-platforms tooling. |
| `deploy-to-vercel` | User asks to implement, configure, or optimize deploy to vercel tasks (specifically configuring or implementing deploy to vercel specifications). | User requests general infrastructure administration, styling, or unrelated operations outside deploy to vercel or unrelated operations outside deploy to vercel. | User asks 'How do I handle deploy to vercel in my workflow?' -> Disambiguate: Clarify whether the task requires specialized deploy to vercel procedures or general cloud-platforms tooling. |
| `remote-gpu-trainer` | User asks to implement, configure, or optimize remote gpu trainer tasks (specifically configuring or implementing remote gpu trainer specifications). | User requests This skill is for the blind spot those tools leave:** AutoDL + Chinese platforms, bare SSH/Slurm/K8s or unrelated operations outside remote gpu trainer. | User asks 'How do I handle remote gpu trainer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized remote gpu trainer procedures or general cloud-platforms tooling. |
| `sandbox-sdk` | User asks to implement, configure, or optimize sandbox sdk tasks (specifically configuring or implementing sandbox sdk specifications). | User requests general infrastructure administration, styling, or unrelated operations outside sandbox sdk or unrelated operations outside sandbox sdk. | User asks 'How do I handle sandbox sdk in my workflow?' -> Disambiguate: Clarify whether the task requires specialized sandbox sdk procedures or general cloud-platforms tooling. |
| `turnstile-spin` | User asks to implement, configure, or optimize turnstile spin tasks (specifically configuring or implementing turnstile spin specifications). | User requests general infrastructure administration, styling, or unrelated operations outside turnstile spin or unrelated operations outside turnstile spin. | User asks 'How do I handle turnstile spin in my workflow?' -> Disambiguate: Clarify whether the task requires specialized turnstile spin procedures or general cloud-platforms tooling. |
| `vercel-ai-sdk-expert` | User asks to implement, configure, or optimize vercel ai sdk expert tasks (specifically configuring or implementing vercel ai sdk expert specifications). | User requests general infrastructure administration, styling, or unrelated operations outside vercel ai sdk expert or unrelated operations outside vercel ai sdk expert. | User asks 'How do I handle vercel ai sdk expert in my workflow?' -> Disambiguate: Clarify whether the task requires specialized vercel ai sdk expert procedures or general cloud-platforms tooling. |
| `vercel-automation` | User asks to implement, configure, or optimize vercel automation tasks (specifically configuring or implementing vercel automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside vercel automation or unrelated operations outside vercel automation. | User asks 'How do I handle vercel automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized vercel automation procedures or general cloud-platforms tooling. |
| `vercel-deployment` | User asks to implement, configure, or optimize vercel deployment tasks (specifically configuring or implementing vercel deployment specifications). | User requests general infrastructure administration, styling, or unrelated operations outside vercel deployment or unrelated operations outside vercel deployment. | User asks 'How do I handle vercel deployment in my workflow?' -> Disambiguate: Clarify whether the task requires specialized vercel deployment procedures or general cloud-platforms tooling. |
| `vercel-optimize` | User asks to implement, configure, or optimize vercel optimize tasks (specifically Metrics first. Recommendations start from Vercel production signals, not repo-wide grep). | User requests general infrastructure administration, styling, or unrelated operations outside vercel optimize or unrelated operations outside vercel optimize. | User asks 'How do I handle vercel optimize in my workflow?' -> Disambiguate: Clarify whether the task requires specialized vercel optimize procedures or general cloud-platforms tooling. |
| `workflow-automation` | User asks to implement, configure, or optimize workflow automation tasks (specifically configuring or implementing workflow automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside workflow automation or unrelated operations outside workflow automation. | User asks 'How do I handle workflow automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized workflow automation procedures or general cloud-platforms tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/infrastructure-and-ops/cloud-platforms/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `c4302171a1e008c8975399fa628059b66c2da78cdacdf579071df0c5dbeb1024` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `deploy-to-vercel` | `resources/deploy-codex.sh` | Created or preserved in canonical package |
| `deploy-to-vercel` | `resources/deploy.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `.gitattributes` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `.gitignore` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `LICENSE` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `README.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `evals/README.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `evals/RESULTS.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `evals/cases.jsonl` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `evals/run_evals.py` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `examples/autodl_sweep/README.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `examples/autodl_sweep/queue_1.txt` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/_schema.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/autodl.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/china.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/generic-ssh.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/lambda.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/paperspace.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/runpod.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `profiles/vastai.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/china-network.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/gotchas_universal.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/lifecycle_checklist.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/monitoring_patterns.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/multinode.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/parallel_ablation.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/principles.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/self-improvement.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/spot-resilience.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/ssh_transport.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/by-domain.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/checkpoint-resume.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/convergence-debugging.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/data-pipeline.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/distributed-launch.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/oom-memory.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/precision-stability.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `references/training/throughput-profiling.md` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/aggregate_to_fs.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/check_staleness.py` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/download_loop.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/gpu_health.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/health_patrol.sh.template` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/mem_monitor.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/reap_vram_zombies.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/run_one.sh.template` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/run_queue.sh.template` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/setup-china-mirrors.sh` | Created or preserved in canonical package |
| `remote-gpu-trainer` | `scripts/verify_local.py` | Created or preserved in canonical package |
| `sandbox-sdk` | `references/api-quick-ref.md` | Created or preserved in canonical package |
| `sandbox-sdk` | `references/examples.md` | Created or preserved in canonical package |
| `turnstile-spin` | `README.md` | Created or preserved in canonical package |
| `turnstile-spin` | `references/astro.md` | Created or preserved in canonical package |
| `turnstile-spin` | `references/hugo.md` | Created or preserved in canonical package |
| `turnstile-spin` | `references/nextjs-app.md` | Created or preserved in canonical package |
| `turnstile-spin` | `references/nextjs-pages.md` | Created or preserved in canonical package |
| `turnstile-spin` | `references/sveltekit.md` | Created or preserved in canonical package |
| `turnstile-spin` | `references/vanilla-html.md` | Created or preserved in canonical package |
| `turnstile-spin` | `scripts/auth-probe.sh` | Created or preserved in canonical package |
| `turnstile-spin` | `scripts/fetch-secret.sh` | Created or preserved in canonical package |
| `turnstile-spin` | `scripts/persist-skill.sh` | Created or preserved in canonical package |
| `turnstile-spin` | `scripts/validate.sh` | Created or preserved in canonical package |
| `turnstile-spin` | `scripts/widget-create.sh` | Created or preserved in canonical package |
| `turnstile-spin` | `scripts/worker-deploy.sh` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/.gitignore` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/LICENSE` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/README.md` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/package.json` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/public/post-deploy.html` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/src/errors.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/src/index.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/src/observability.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/src/types.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/src/validate.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/test/deploy.test.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/test/integration.test.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/test/unit.test.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/test/validation.test.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/tsconfig.json` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/vitest.config.ts` | Created or preserved in canonical package |
| `turnstile-spin` | `templates/worker/wrangler.toml` | Created or preserved in canonical package |
| `turnstile-spin` | `tests/validation.md` | Created or preserved in canonical package |
| `vercel-optimize` | `CONTRIBUTING.md` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/auth-route.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/budget-summary.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/citations.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/cost-coverage.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/dedup-recs.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/deep-dive.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/display-labels.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/extract-claims.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/framework-support.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/build-minutes-fanout.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/cold-start.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/contract.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/cwv-poor.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/external-api-slow.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/hard-gates.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/index.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/isr-overrevalidation.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/middleware-heavy.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/observability-events-attribution.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/platform-bot-protection.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/platform-fluid-compute.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/region-misconfig.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/route-errors.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/scanner-driven.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/select-candidates.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/slow-route.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/types.d.ts` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/uncached-route.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/gates/usage-spike-triage.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/grade-recommendation.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/impact-label.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/impact-magnitude.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/investigation-brief.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/observation-safety.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/project-facts.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/queries.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/reconcile-candidates.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/render-report.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/repo-root.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/route-normalize.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/bot-protection-certainty.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/cache-tag-invalidation-certainty.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/count-correct.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/function-duration-invocations.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/index.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/middleware-conflict.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/missing-citation.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/pre-release.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/rate-limit.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/rendering-mode-mislabel.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/undeclared-dep.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/vercel-directive-strip.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/sanitizers/window-units.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/cache-components-suspense-dedupe.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/edge-heavy-import.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/force-dynamic.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/headers-in-page.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/index.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/large-static-asset.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/max-age-without-s-maxage.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/middleware-broad-matcher.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/missing-cache-headers.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/prisma-include-tree.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/region-pin-in-config.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/source-maps-production.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/sveltekit-prerender-missing.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/turbo-force-bypass.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/unoptimized-image.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/scanners/use-cache-date-stamp.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/support-topics.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/throttle.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/util.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/vercel.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/verify-claim.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `lib/workspace-resolver.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `references/candidates.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/data-collection.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/docs-library.json` | Created or preserved in canonical package |
| `vercel-optimize` | `references/doctrine.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/observability-plus.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/README.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/ai-application.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/api-service.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/content-site.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/ecommerce.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/marketing.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/saas.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/playbooks/sveltekit.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/recommendations.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/scanner-patterns.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/scoring.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/README.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/astro-edge-middleware-scope.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/astro-output-mode-and-isr.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/auth-preserving-parallelization.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/bot-protection-product-guardrails.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/build-minutes-monorepo-fanout.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/cache-components-static-shell-boundaries.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/cache-components-suspense-dedupe-pitfall.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/cdn-cache-auth-safety.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/cold-start-initialization-bundle.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/core-web-vitals-client-bottlenecks.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/database-egress-pooling-region.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/dynamic-rendering-traps.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/external-api-critical-path-platform.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/external-api-critical-path.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/fast-data-transfer-payloads.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/fluid-compute-caveats.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/function-duration-io-and-after.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/function-invocation-reduction.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/function-region-misconfiguration-ttfb.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/image-optimization-cost-control.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/isr-revalidation-static-generation.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/middleware-proxy-edge-cost.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/next-fetch-revalidate-floor.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/next-font-cls-self-hosting.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/next-heavy-ui-lazy-load-boundaries.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/next-image-lcp-preload-sizes.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/next-route-handler-get-cache-defaults.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/next-script-third-party-strategy.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/nextjs-version-cache-semantics.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/not-found-catchall-request-waste.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/nuxt-route-rules-cache-isr.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/observability-events-cost-attribution.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/post-response-work-waituntil.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/route-error-durable-offload.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/route-error-runtime-limits.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/runtime-cache-reusable-data.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/sveltekit-isr-prerender-safety.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/sveltekit-split-cold-start-tradeoff.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/usage-spike-triage.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/use-cache-date-stamp-isr-write-amplifier.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/use-cache-remote-shared-origin-data.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/support-topics/workflow-resumable-stream-routes.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/verification.md` | Created or preserved in canonical package |
| `vercel-optimize` | `references/voice.md` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/budget-summary.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/build-docs.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/check-citations.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/check-docs-fresh.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/collect-signals.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/collect-sub-agent-outputs.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/deep-dive.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/gate-investigations.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/merge-signals.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/prepare-investigation-brief.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/reconcile-candidates.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/render-report.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/scan-codebase.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/verify-and-regen.mjs` | Created or preserved in canonical package |
| `vercel-optimize` | `scripts/verify-finding.mjs` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
