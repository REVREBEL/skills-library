# Detailed Failures, Errors, and Architectural Gaps Register

**Task:** SKIL-13 | ZI-04: Validate existing code and CI from pinned SHA  
**Pinned Git SHA:** `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Execution Timestamp:** 2026-11-04T05:08:00Z  

---

## 1. Test Suite Defect Register

Testing from pinned SHA `195eda775d7a8dcad1837a1990bcba8259da3ea0` identified three distinct failure modes in the automated regression suite:

### Defect 1: Unmocked GitHub CLI Dispatch in `test_runtime_publication.py`
- **Location:** `tests/test_runtime_publication.py:813`, in `test_21_accept_external_intake_enforcement_and_dispatch_failure`
- **Test Objective:** Verify that `capture_dirty_target()` enforces intake policies and records workflow dispatch error states when dispatch fails.
- **Observed Behavior:**
  ```python
  cap_dispatch = capture_dirty_target(
      target, remote="origin", push=True, trigger_workflow=True, force=True
  )
  self.assertFalse(cap_dispatch["workflow_triggered"])  # Line 813 -> FAILS
  ```
  Stack Trace:
  ```text
  Traceback (most recent call last):
    File "tests/test_runtime_publication.py", line 813, in test_21_accept_external_intake_enforcement_and_dispatch_failure
      self.assertFalse(cap_dispatch["workflow_triggered"])
  AssertionError: True is not false
  ```
- **Root Cause:**
  In `tools/skill_library/intake_capture.py` (lines 383–395), `capture_dirty_target` executes:
  ```python
  subprocess.run(["gh", "workflow", "run", "runtime-intake.yml", ...], check=False)
  ```
  The test environment did not mock `subprocess.run` or `gh`. When executed on an authorized machine with GitHub CLI configured, `gh` returns exit code 0, causing `workflow_triggered` to be `True`. The test author hard-coded `self.assertFalse(cap_dispatch["workflow_triggered"])` assuming dispatch would fail without mock isolation.

---

### Defect 2: Package Name vs Directory Inconsistency on External Renames
- **Location:** `tests/test_runtime_publication.py:1122`, in `test_24_skill_directory_rename_preserves_old_and_new_paths`
- **Test Objective:** Verify that an external physical directory rename (e.g., `bug-hunter` -> `bug-tracker`) is captured as a review-only proposal without destructive overwrite.
- **Observed Behavior:**
  ```python
  ev = evaluate_candidate(candidate_name="bug-tracker", ...)
  self.assertTrue(ev.is_valid_package)  # Line 1122 -> FAILS
  ```
  Stack Trace:
  ```text
  Traceback (most recent call last):
    File "tests/test_runtime_publication.py", line 1122, in test_24_skill_directory_rename_preserves_old_and_new_paths
      self.assertTrue(ev.is_valid_package)
  AssertionError: False is not true
  ```
- **Root Cause:**
  In `test_24`, step 4 renames the physical folder from `bug-hunter` to `bug-tracker`, but leaves `SKILL.md` frontmatter with `name: bug-hunter`.
  During `evaluate_candidate()` in `tools/skill_library/intake.py`:
  ```python
  val_rep = validate_single_skill(candidate_path)
  if not val_rep.is_valid:
      eval_result.is_valid_package = False
  ```
  `validate_single_skill()` asserts that the package directory name must strictly match the frontmatter name:
  `"Package directory 'bug-tracker' does not match frontmatter name 'bug-hunter'"`.
  Consequently, `val_rep.is_valid` becomes `False`, which marks `ev.is_valid_package = False`. The test author intended to assert that the proposal is recognized as a valid package structure, but the validator rejected it due to the mismatched frontmatter name.

---

### Defect 3: Missing Module Path Injection in `test_migration_roadmap.py`
- **Location:** `tests/test_migration_roadmap.py:18`
- **Test Objective:** Verify architecture contracts in `docs/architecture/MIGRATION_ROADMAP.md`.
- **Observed Behavior:**
  When executed via standard unittest runner without `PYTHONPATH`:
  ```bash
  python3 -m unittest tests/test_migration_roadmap.py
  ```
  Output:
  ```text
  ImportError: Failed to import test module: test_migration_roadmap
  ModuleNotFoundError: No module named 'skill_library'
  ```
- **Root Cause:**
  Unlike `tests/test_registry_router_contracts.py` and `tests/test_migration_gates.py`, which include:
  ```python
  sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
  ```
  `test_migration_roadmap.py` omits `sys.path.insert()`. When run with `PYTHONPATH=tools`, all 14 tests in the suite pass.

---

## 2. Operational & Validator Gaps Register

### Gap 1: Validation State Divergence on Baseline Checkouts
- **Tool:** `python3 tools/skill-library.py validate`
- **Observed Behavior:** Exits with code 1 and reports:
  ```text
  Publication Error: Runtime branch tree (418c857507) does not match HEAD:library (66a84f272f).
  Target Error: Target 'universal-global' HEAD commit does not match published runtime commit.
  ```
- **Root Cause:**
  1. The git reference `refs/heads/runtime` in the local checkout points to an earlier tree (`418c857507`) rather than `HEAD:library` (`66a84f272f`).
  2. The configured target `universal-global` points to `~/.agents/skills`, which is evaluated during validation unless `--skip-targets` is supplied.

### Gap 2: High-Concurrency Subprocess Git Locking in Batch Tests
- **Observed Behavior:**
  Running all 253 tests sequentially inside a single Python process via `python3 tools/skill-library.py test` triggers intermittent `exit status 128` on `git commit` in `TestRuntimeGitClonePublication.setUp` (`test_01`–`test_03`).
- **Root Cause:**
  Subprocess execution of temporary git repositories in `/var/folders/...` under high frequency encounters file handle or lock contention on macOS APFS. Running test modules in isolated processes completely eliminates this contention.
