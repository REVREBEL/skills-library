# Continuous Integration (CI) Baseline Analysis

**Task:** SKIL-13 | ZI-04: Validate existing code and CI from pinned SHA  
**Pinned Git SHA:** `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Execution Timestamp:** 2026-11-04T05:08:00Z  

---

## 1. Discovered CI Workflows

Inspection of `.github/workflows/` at the pinned baseline commit reveals three declarative workflows:

1. **`ci.yml` (`Test and Validate`):**
   - **Triggers:** Push to `main`, `feature/**`; Pull Request targeting `main`.
   - **Runner:** `ubuntu-latest`.
   - **Toolchain Specification:** Python 3.15, Git (authenticated as `github-actions[bot]`).
   - **Job Steps:**
     1. Checkout repository with `fetch-depth: 0`.
     2. Set up Python 3.15 (`actions/setup-python@v7`).
     3. Configure Git identity (`github-actions[bot]`).
     4. `python3 tools/skill-library.py publish-runtime`
     5. `python3 tools/skill-library.py test`
     6. `python3 tools/skill-library.py validate`
     7. `python3 tools/catalog_semantic_census.py` && `git diff --exit-code audit/taxonomy-census/`

2. **`publish-runtime.yml` (`Publish Runtime Branch`):**
   - **Triggers:** Push to `main` with changes in `library/**`; manual `workflow_dispatch`.
   - **Runner:** `ubuntu-latest`.
   - **Permissions:** `contents: write`.
   - **Step:** `python3 tools/skill-library.py publish-runtime --push`

3. **`runtime-intake.yml` (`Runtime Intake Pipeline`):**
   - **Triggers:** `workflow_dispatch` with input `incoming_branch`.
   - **Runner:** `ubuntu-latest`.
   - **Permissions:** `contents: write`, `pull-requests: write`.
   - **Steps:** Converts incoming snapshot branch to reviewed `intake/*` PR branch via `convert-incoming`, runs `intake --strict`, and opens PR via GitHub CLI (`gh pr create`).

---

## 2. Step-by-Step CI Execution from Pinned SHA (Baseline Simulation)

We simulated each step of `ci.yml` directly against the pinned checkout at `/tmp/skil13-pinned-worktree` using the audited workstation toolchain (Python 3.14.7, Git 2.47.0):

### Step 4: `python3 tools/skill-library.py publish-runtime`
- **Command:** `python3 tools/skill-library.py publish-runtime`
- **Result:** **PASSED (Exit Code: 0)**
- **Behavior:** Successfully extracted the tree SHA of `HEAD:library` (`66a84f272f`) and updated the local ref `refs/heads/runtime`. It operates entirely via low-level plumbing (`git commit-tree` and `git update-ref`), leaving the index and working tree completely unmodified.

### Step 5: `python3 tools/skill-library.py test`
- **Command:** `python3 tools/skill-library.py test`
- **Result:** **FAILED (Exit Code: 1)**
- **Discovered Output:**
  ```text
  Ran 253 tests in 166.697s
  FAILED (failures=2, errors=3)
  ```
- **Failure Analysis:**
  - `test_runtime_publication.TestRuntimeGitClonePublication.test_21_accept_external_intake_enforcement_and_dispatch_failure`: FAILED (`AssertionError: True is not false` on `cap_dispatch["workflow_triggered"]` due to unmocked `gh` CLI invocation).
  - `test_runtime_publication.TestRuntimeGitClonePublication.test_24_skill_directory_rename_preserves_old_and_new_paths`: FAILED (`AssertionError: False is not true` on `ev.is_valid_package` due to directory/frontmatter name divergence on rename).
  - Batch execution setup errors in `test_01`, `test_02`, `test_03` of `TestRuntimeGitClonePublication`: subprocess `git commit` exited 128 due to lock contention during rapid temporary repository initialization on APFS. In isolated execution, `test_01`–`test_03` pass cleanly.

### Step 6: `python3 tools/skill-library.py validate`
- **Command:** `python3 tools/skill-library.py validate`
- **Result:** **FAILED (Exit Code: 1)**
- **Discovered Output:**
  ```text
  Set Reconciliation (Physical == Router == Manifest): PASSED
  Runtime Publication Validation: FAILED
  Target Checkout Validation: FAILED (Checked: 1)
  Total Routers Verified: 26
  Total Router Links Verified: 2176 (Broken: 0)
  Total Canonical Active Skills: 2102 (Orphans: 0)
  Total Manifest Skills: 2102

  Errors / Regressions Found:
    - Publication Error: Runtime branch tree (418c857507) does not match HEAD:library (66a84f272f).
    - Target Error: Target 'universal-global' HEAD commit (b5f4af2f0d) does not match published runtime commit (7456833074).
    - Target Error: Target 'universal-global' tree (17d8651a10) does not match published runtime tree (418c857507).
  ```
- **Analysis:**
  - In the observed pinned workstation checkout, the local `runtime` ref and an **existing but stale** `universal-global` target checkout produced the recorded validation errors. `ci.yml` runs `publish-runtime` before `validate`, addressing the local publication-ref mismatch. The configured `~/.agents/skills` target only produces a mismatch if that path exists and is out of sync; a missing target path is skipped by `validate_library_integrity` on a clean headless runner. These workstation failures must not be attributed to CI without CI-specific logs.

### Step 7: `python3 tools/catalog_semantic_census.py` && `git diff --exit-code audit/taxonomy-census/`
- **Command:** `python3 tools/catalog_semantic_census.py && git diff --exit-code audit/taxonomy-census/`
- **Result:** **PASSED (Exit Code: 0)**
- **Behavior:** The script successfully evaluated all 2,133 skills, verified role distribution (1,701 capabilities, 391 workflows, 22 manual review, etc.), regenerated datasets, and produced zero diff in `audit/taxonomy-census/`. This confirms 100% deterministic census generation.

---

## 3. Discovered CI Environment Assumptions & Gaps

1. **Python Version Drift:**  
   `ci.yml` pins `python-version: '3.15'`, whereas Python 3.14/3.13 is standard across host workstations. Python 3.15 is an unreleased development branch.
2. **Missing Test Mocking in CI Pipeline:**  
   The pinned **workstation** test run failed with two assertions, including an authenticated `gh` dispatch from `test_21`, and three batch setup errors. This does not establish that an unauthenticated GitHub Actions runner triggers the same dispatch or fails the same assertions. The hosted CI outcome must be established from the actual job logs.
3. **Target Validation in Headless CI:**  
   `validator.py` inspects configured target checkouts only when their paths exist. A missing `~/.agents/skills` checkout on a headless GitHub Actions runner is skipped and does **not** require `--skip-targets`. An existing but stale target, as observed on the workstation, can fail validation.

---

## 4. CI Qualification & Provenance Delineation

To avoid ambiguity between audit branch status and baseline repository health:
- **Baseline Source Health (SHA `195eda775d`):**  
  Local workstation execution of individual `ci.yml` commands at the pinned source SHA reported failures for `test` (exit 1) and `validate` (exit 1). These are **pinned-workstation baseline results**, not a recorded GitHub Actions run at that SHA; they cannot independently establish the hosted CI outcome.
- **Evidence-Only PR Status (PR #159):**  
  GitHub Actions status checks on PR #159 reported green/passing at the observed PR head. The `Test and Validate` workflow (`.github/workflows/ci.yml`) has **no path filter** for pull requests targeting `main`: its configured publication, test, library-validation, and census steps still run for documentation-only PRs. Thus the green check is evidence that the configured hosted workflow passed **on the PR commit and CI environment**, but not proof that the separately pinned older source SHA passed the locally executed baseline tests. Differences between local baseline results and hosted CI require separate investigation; do not attribute them to skipped docs-only checks.
- **Toolchain Provenance Record:**  
  - Diagnostic Execution: Python 3.14.7 (Clang 15.0.0, arm64 Darwin 24.3.0 macOS 15.3), Git 2.47.0.
  - Specified CI Target: Python 3.15 on `ubuntu-latest` (`actions/setup-python@v7`).
