# ZI-08 — Runtime Execution, Security and Context Contracts

**Work order:** SKIL-9 (ZI-08)
**Baseline:** `origin/main` @ `f1ab2439`
**Status:** Declarations and load plans implemented. Health probes deferred by design.

---

## 1. Verdict

**8 implemented · 2 partial · 2 absent** (12 capabilities)

The contract layer is real and tested. What is missing is not mechanism but data: the catalog
declares almost nothing about how skills execute, so the provider views have nothing to project.

| Verdict | Capabilities |
|---|---|
| **Implemented** | risk declaration · side-effect declaration · permission declaration · environment requirement · runtime load plan · destructive-command detection · credential-reference detection · Phase 09 evidence reuse |
| **Partial** | execution provider bindings · provider/transport view |
| **Absent** | health probes (deferred by design) · runtime enforcement (out of scope) |

## 2. What was built

### 2.1 Typed execution contract

`tools/skill_library/execution.py` defines the declarations ZI-08 asks for:

```python
class SideEffect:  none, reads_files, writes_files, executes_commands,
                  network, external_state, destructive
class Permission:  none, filesystem_read, filesystem_write, shell,
                  network, credentials
EnvironmentRequirement(runtimes, tools, needs_network, env_vars)
ExecutionProfile(canonical_id, risk, side_effects, permissions,
                 environment, evidence, tier)
```

Profiles are **derived from evidence, not hand-written**. `risk` is `unknown` on 2,102 of 2,133
canonical packages, so manual backfill would not scale. The derivation chain is:

1. **code-presence tier** — bundled scripts → elevated, executable blocks → low, illustrative or
   prose → safe
2. **destructive-command scan** — overrides to critical
3. **credential-reference scan** — adds the credentials permission
4. **Phase 09 refinement** — shell / remote / dependency statuses from the historical resource
   registry

Every profile carries an `evidence` list naming which signals produced it, so a reviewer can see why
a skill was rated the way it was.

### 2.2 Load plan, distinct from availability closure

`LoadPlan` answers a different question from "is this skill present and indexed":

| | Availability closure | Load plan |
|---|---|---|
| Question | is the package here and discoverable | what must be read or executed to run it |
| Contains | canonical ids, router paths, manifest entries | entrypoint, resources, scripts, runtimes, network |

That separation is deliberate. A skill can be perfectly available and still be impossible to execute
because its Python runtime or network access is missing.

### 2.3 Health probes — deferred, not forgotten

ZI-08 says health probes are optional and only where a concrete execution consumer exists. None does.
Implementing probes now would invent a dependency on services the library cannot vouch for, so this is
recorded as a deliberate omission with a clear trigger: **build probes when the first consumer that
actually invokes a skill lands.**

## 3. Results

Derived across all 2,133 canonical packages:

| Dimension | Distribution |
|---|---|
| tier | 1: 150 · 2: 512 · 3: 575 · 4: 896 |
| risk | critical 33 · elevated 144 · low 490 · safe 1,466 |
| side effect | destructive 33 · executes_commands 662 · network 24 · reads_files 1,495 · writes_files 17 |
| permission | credentials 454 · filesystem_read 1,621 · network 24 · shell 662 |
| Phase 09 evidence | 616 packages |

**No package is left at `unknown`.** That is the point of the exercise: ZI-08 now has a defensible
risk basis for the whole catalog.

### On the 33 critical packages

Every sampled detection is a genuine command inside a code block or inline code span — `rm -rf`,
`rm -f`, `DROP TABLE`. The first pass produced 53, including false positives such as "auto-start on
reboot" in prose; detection is now scoped to code spans, which removed them without losing real hits.

### On the 454 credential references

This is a broad keyword match (api key, secret, token, password, credential). It marks skills that
*mention* credentials, not skills that mishandle them. Treat it as a review queue, not a verdict.

## 4. Phase 09 is reusable

The historical registry records 5,397 resources across 596 owning skills. All **596 of 596** owner
slugs match a current canonical slug, so the evidence joins cleanly — 616 packages gain execution
evidence from it.

The strongest-status-per-owner rule keeps the most permissive record when a skill owns several
resources, so a single flagged script is not hidden by a dozen clean ones.

## 5. The gap that remains

Provider data is almost absent:

| Declaration | Packages (of 2,656) |
|---|---:|
| `tools` | 12 |
| `allowed-tools` | 13 |
| `mcp` | 2 |

`ExecutionProviderContract` and `MultiViewProjector.project_provider_view` are implemented and
tested, but there is nothing to project. This is a data problem, not a code problem, and it is the
same shape as the `risk: unknown` problem ZI-07 solved by derivation.

## 6. Remaining work

| # | Work | Priority | Notes |
|---|---|---|---|
| 1 | Derive provider bindings from code and metadata | P1 | mirror the risk-derivation approach |
| 2 | Decide whether credentials permission needs a narrower signal | P1 | 454 is a review queue, not a verdict |
| 3 | Build health probes when the first execution consumer exists | P2 | blocked on a consumer, by design |
| 4 | Define how load plans are consumed at runtime | P2 | ZI-10 territory |
| 5 | Backfill `risk` into frontmatter from the derived profiles | P2 | derived values are the source until then |

## 7. Files

- `capability-matrix.csv` — 12 capabilities × implemented / tested / evidence / verdict / gap.
- `execution-profiles.csv` — 2,133 derived profiles.
- `summary.md` — this document.
- `tools/skill_library/execution.py`, `tools/execution_contract_report.py` — implementation.
- `tests/test_execution.py` — 15 tests.