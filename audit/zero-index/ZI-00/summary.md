# ZI-00 — Program State Reconciliation

**Generated:** 2026-11-15T18:15:02Z
**Work order:** ZI-00 (new; not present in the P-SKIL-27 issue set)
**Mode:** Read-only assessment. No canonical library content, manifest, or runtime state was modified.

---

## 1. Why this work order exists

P-SKIL-27 requires every claim to be tied to a newly recorded Git SHA, and forbids importing old
statuses or acceptance claims. This pass checks whether the existing zero-index evidence still holds
against the current tree. It does not re-run the historical rebuild.

## 2. Baseline state

| Item | Value |
|---|---|
| Worktree HEAD | `da83ca84` (detached) |
| `origin/main` | `f1ab2439` |
| Worktree behind `origin/main` | **7 commits** |
| Previously pinned SHA (SKIL-16) | `195eda77` |
| Pinned SHA behind `origin/main` | **61 commits** |
| Working tree | Clean |

The assessment was run from a detached HEAD that is **not** the pinned baseline and **not** the
current tip. Any evidence compared below was cross-checked against both `HEAD` and `origin/main`.

## 3. Population integrity

Measured at `origin/main` by enumerating tracked files:

| Population | SKIL-16 claim | Measured | Delta |
|---|---:|---:|---:|
| Total `SKILL.md` | 5,072 | **5,070** | −2 |
| `library/` | 2,657 | **2,656** | −1 |
| `task-folder/agents/skills/` | 2,101 | **2,100** | −1 |
| `task-folder/agents/not-needed/` | 238 | **238** | 0 |
| `task-folder/agents/archived/` | 20 | **20** | 0 |

`audit/runtime-manifest.json` is internally inconsistent: it declares
`total_managed_skills: 2103` but contains **2,102** skill entries.

## 4. Validation and test results at HEAD

```
=== Living Library Validation: FAILED ===
Set Reconciliation (Physical == Router == Manifest): PASSED
Runtime Publication Validation: PASSED
Target Checkout Validation: FAILED (Checked: 1)
Total Routers Verified: 26
Total Router Links Verified: 2176 (Broken: 0)
Total Canonical Active Skills: 2102 (Orphans: 0)
Workstation Path Leaks: 0
Potential Secret Leaks: 0

  - Target Error: Target 'universal-global' HEAD commit (b5f4af2f0d) does not match published runtime commit (3ede2dfb07).
  - Target Error: Target 'universal-global' tree (17d8651a10) does not match published runtime tree (f010636bbd).
```

Test suite: **253 tests, 1 failure, 0 errors**, exit 1.
Failing test: `test_runtime_publication.TestRuntimeGitClonePublication.test_24_skill_directory_rename_preserves_old_and_new_paths`.

The suite was run with a `gh` stub on `PATH` and all `GH_*` tokens unset, so the `test_21`
live-dispatch hazard recorded in SKIL-13 could not fire. Working tree was verified clean afterwards.

## 5. Issue status reconciliation

| Issue | Title | Linear status | Artifact at HEAD | Artifact at `origin/main` | Verdict |
|---|---|---|---|---|---|
| SKIL-16 | ZI-01 Pin canonical source and zero-index inventory | Done | Present | Present | Holds, counts off |
| SKIL-15 | ZI-02 Reconcile 52 archived scripts | Done | Present | Present | Holds |
| SKIL-13 | ZI-04 Validate existing code and CI | Done | Present | Present | Holds |
| SKIL-11 | ZI-06 Language, integrity and exposure audit | Done | **Missing** | Present | Stale at HEAD only |
| SKIL-14 | ZI-03 Architecture and contract ledger | In Review | **Missing** | **Missing** | **False status** |
| SKIL-12 | ZI-05 Discovery and context benchmark | In Review | **Missing** | **Missing** | **Unsupported status** |
| SKIL-57 | Linear workflow and PR scripts | Done | Present | Present | Holds |

Two findings matter:

1. **SKIL-14's entire diff was reverted** at `da83ca84`. The ledger, the traceability matrix, the
   generator and verifier scripts, and the two `gh` skills are all gone. "In Review" describes a
   state that no longer exists.
2. **SKIL-12 has no repository trace at all** — no artifact directory, no branch, no PR. Its
   "In Review" status is not backed by anything in this repo.

## 6. Scope leak worth recording

The SKIL-14 commit added `library/github-operations/gh/SKILL.md` and
`library/github-operations/gh-skill/SKILL.md` to the canonical library. A contract-ledger work order
should not be adding canonical skills; the revert removed them, which is the correct outcome, but the
inclusion indicates the issue boundary was not enforced.

## 7. Recommended next actions

1. Re-pin the baseline to `origin/main` (`f1ab2439`) and restate the population counts from this file.
2. Correct the manifest's declared total, or make the validator assert declared == actual.
3. Reconcile the checked-in `audit/validation-report.md` with observed output, or generate it.
4. Resolve SKIL-14 (closed into SKIL-10) and re-baseline or close SKIL-12.
5. Then proceed to the capability matrix (7 target capabilities × implemented / partial / docs-only / absent / regressed).

## 8. Files

- `baseline.json` — machine-readable measurements, SHAs, exit codes.
- `drift-register.csv` — one row per checked claim, with severity.