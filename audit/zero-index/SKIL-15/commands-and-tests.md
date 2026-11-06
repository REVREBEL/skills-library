# Commands, Tests, and Verification Log: SKIL-15

This document records the exact executable commands, AST parsing results, test suite execution outputs, negative-path fail-closed checks, sanitization scans, and dual-run reproducibility evidence for SKIL-15 (`ZI-02 | Reconcile 52 archived scripts against current code`).

---

## 1. Pinned Snapshot & Environment Verification

### Commit & Snapshot Disambiguation
| Artifact / Pointer | Git Commit SHA | Description |
| :--- | :--- | :--- |
| **Audited Pinned Source Snapshot** | `195eda775d7a8dcad1837a1990bcba8259da3ea0` | Canonical repository snapshot coordinated with SKIL-16 and SKIL-13 |
| **Verification Execution Base Commit** | `d050cc97b404b54924ffeff62fdbf01d4b32a927` | Commit checked out during verification execution (`git rev-parse HEAD`) |
| **Prior Review Target PR Head** | `1539e925751ef03c81b102f2cf7a70449be9da97` | Head of PR #158 evaluated in pull request review 5802535665 |
| **Submitted Revision PR Head** | *(updated on branch push)* | Target head commit of PR #158 incorporating review fixes |

### Environment Verification Execution
```bash
# Repo Root: skills-library
# Active Branch: issue/skil-15-reconcile-52-archived-scripts
# Base Branch: origin/main
# Python Version: 3.15.2
# Timestamp: 2026-11-06T16:00:39Z

$ git rev-parse HEAD
d050cc97b404b54924ffeff62fdbf01d4b32a927
# Exit Code: 0

$ git status --porcelain
(clean working tree)
# Exit Code: 0
```

---

## 2. 52-Script Discovery and Source Byte Hashing

The 52 archived scripts were retrieved from local repository archive `tools/all_scripts/` (grounding the authoritative Drive archive folder `1RvGogKBhpAzodN-nEvOEYig3cP5uKwDK`).

```bash
$ python3 audit/zero-index/SKIL-15/scripts/generate_skil15_crosswalk.py --source-root . --output-dir /tmp/skil15-repro-run1
# Exit Code: 0
# 52/52 scripts verified byte-for-byte; SHA-256 and byte sizes cataloged in archive-source-manifest.csv
# All mapped callable symbols validated dynamically via AST against current codebase
```

---

## 3. Python AST Analysis Execution

AST analysis was executed programmatically and via CLI across all 52 archived scripts and the 14 core modules:

```bash
$ python3 audit/zero-index/SKIL-15/scripts/verify_skil15_crosswalk.py --ast-only
# Exit Code: 0
```

### AST Parsing Results:
- **Archived Scripts (52 files in `tools/all_scripts/`):**
  - Syntactic Validity: 100% valid Python AST (0 syntax errors)
  - Total Classes Defined: 37
  - Total Functions Defined: 131
  - Top-Level CLI Entrypoints (`if __name__ == '__main__':`): 39
- **Core Repository Modules (14 files in `tools/skill_library/`):**
  - Syntactic Validity: 100% valid Python AST (0 syntax errors)
  - Total Classes Defined: 70
  - Total Functions Defined: 38

---

## 4. Test Suite Execution & Contract Verification

The 7 core architecture and contract test suites were executed:

```bash
$ python3 -m unittest tests/test_semantic_census.py tests/test_semantic_object_model.py tests/test_registry_router_contracts.py tests/test_physical_ownership.py tests/test_migration_gates.py tests/test_family_eligibility.py tests/test_migration_roadmap.py
Ran 213 tests in 1.424s - OK
# Exit Code: 0
```

### Test Results Breakdown (213 Passing Tests):
1. `tests/test_family_eligibility.py`: 40 tests passed (**OK**)
2. `tests/test_migration_gates.py`: 56 tests passed (**OK**)
3. `tests/test_migration_roadmap.py`: 14 tests passed (**OK**)
4. `tests/test_physical_ownership.py`: 19 tests passed (**OK**)
5. `tests/test_registry_router_contracts.py`: 39 tests passed (**OK**)
6. `tests/test_semantic_census.py`: 10 tests passed (**OK**)
7. `tests/test_semantic_object_model.py`: 35 tests passed (**OK**)

**Total:** **213 tests ran, 213 PASSED, 0 failures, 0 errors.**

> **Methodological Clarification (`has_test`):** In all crosswalk tables and audit deliverables, `has_test=TRUE` denotes verified **static call linkage** to passing core contract test suites via AST call and receiver tracing. It does **NOT** denote dynamic runtime code coverage or line-by-line branch instrumentation.

---

## 5. Negative-Path Fail-Closed Verification

Eight negative-path validation checks were executed to prove that the harness fails closed when encountering invalid inputs, corrupt metadata, or invalid call sequences:

```bash
$ python3 audit/zero-index/SKIL-15/scripts/verify_skil15_crosswalk.py --negative-only
# Exit Code: 0
```

| Check | Target / Condition Tested | Expected Negative Behavior | Observed Result | Verdict |
| :--- | :--- | :--- | :--- | :---: |
| 1. Unit Test Failure | Deliberately failing test (`self.assertTrue(False)`) | Non-zero exit code, caught `AssertionError` | Caught with non-zero exit code | **PASS** |
| 2. Malformed Script AST | Unparseable Python syntax (`def broken(\n`) | `SyntaxError` raised | Caught `SyntaxError` | **PASS** |
| 3. Missing Archive Script | Querying nonexistent script filename | Recorded as `FILE_NOT_FOUND_IN_ARCHIVE` | Flagged as missing | **PASS** |
| 4. Nonexistent Symbol | Checking fake symbol `NonexistentClass.fake_method` | `verify_symbol_in_file` returns `False` | Rejected with clear reason | **PASS** |
| 5. Untested Symbol Linkage | Checking untested symbol `validate_library_integrity` | `verify_test_linkage` returns `False` | Rejected with `NO_DIRECT_CORE_UNIT_TEST_COVERAGE` | **PASS** |
| 6. False-Positive Test Linkage | AST check with class import + unrelated receiver method call (`other.record_change()`) | `is_callable_invoked_in_ast` returns `False` | Disconnected call rejected; no false-positive test linkage | **PASS** |
| 7. Non-Git Directory Provenance | `get_git_metadata` invoked on non-Git scratch directory | `RuntimeError` raised | Caught `RuntimeError`; fail-closed with zero fallback | **PASS** |
| 8. Statement Order & Reassignment | Reassigned receiver call & pre-assignment call in AST | `is_callable_invoked_in_ast` returns `False` | Out-of-order & reassigned calls rejected; linear order enforced | **PASS** |

---

## 6. Dual-Run Reproducibility Verification

The generator was run independently into two separate directories (`/tmp/skil15-repro-run1` and `/tmp/skil15-repro-run2`). Independent SHA-256 digests were computed for each run to verify bit-for-bit determinism:

| Artifact | Run 1 SHA-256 Digest | Run 2 SHA-256 Digest | Match Status |
| :--- | :--- | :--- | :---: |
| `archive-source-manifest.csv` | `c1d68ec8340f7188888cc14930f3076159d0836c0911514bbfe606f7980eeb7f` | `c1d68ec8340f7188888cc14930f3076159d0836c0911514bbfe606f7980eeb7f` | **MATCH** |
| `script-reuse-crosswalk.csv` | `db1722ca9196bdb512df8822e3148a7205b007a72058bf4358310a0d76e0f2d3` | `db1722ca9196bdb512df8822e3148a7205b007a72058bf4358310a0d76e0f2d3` | **MATCH** |
| `module-capability-matrix.md` | `475ebcad1d5ff3955886f13577b024c1c867801db1e1f4bf8fcb35a3998c3372` | `475ebcad1d5ff3955886f13577b024c1c867801db1e1f4bf8fcb35a3998c3372` | **MATCH** |
| `gaps-and-collisions.md` | `3355cadea784be9ce1eb70579a6c2552f6493deaaff2f7dd7484630d5444cc29` | `3355cadea784be9ce1eb70579a6c2552f6493deaaff2f7dd7484630d5444cc29` | **MATCH** |

**Reproducibility Verdict:** 100% BIT-FOR-BIT IDENTICAL (0 variance across runs).

---

## 7. Sanitization & Workstation Path Audit

A full regex sweep was performed across all generated deliverables:
- Personal workstation path patterns (`/Users/*`): **0 detected**
- Secret key or token patterns (API tokens, private keys, PATs): **0 detected**
