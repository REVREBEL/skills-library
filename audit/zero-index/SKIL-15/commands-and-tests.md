# Commands, Tests, and Verification Log: SKIL-15

This document records the exact executable commands, AST parsing results, test suite execution outputs, negative-path fail-closed checks, sanitization scans, and dual-run reproducibility evidence for SKIL-15 (`ZI-02 | Reconcile 52 archived scripts against current code`).

---

## 1. Pinned Snapshot & Environment Verification

```bash
# Repo Root: skills-library
# Active Branch: issue/skil-15-reconcile-52-archived-scripts
# Base Branch: origin/main
# Python Version: 3.14.7

$ git rev-parse HEAD
ae2c93a51ba530983d35a3d7422cc327a298f587

# Pinned git snapshot coordinating with SKIL-16 and SKIL-13:
195eda775d7a8dcad1837a1990bcba8259da3ea0
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
Ran 213 tests in 4.599s - OK
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

---

## 5. Negative-Path Fail-Closed Verification

Four negative-path validation checks were executed to prove that the harness fails closed when encountering invalid inputs:

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

---

## 6. Dual-Run Reproducibility Verification

The generator was run independently into two separate directories (`/tmp/skil15-repro-run1` and `/tmp/skil15-repro-run2`). Independent SHA-256 digests were computed for each run to verify bit-for-bit determinism:

| Artifact | Run 1 SHA-256 Digest | Run 2 SHA-256 Digest | Match Status |
| :--- | :--- | :--- | :---: |
| `archive-source-manifest.csv` | `c1d68ec8340f7188888cc14930f3076159d0836c0911514bbfe606f7980eeb7f` | `c1d68ec8340f7188888cc14930f3076159d0836c0911514bbfe606f7980eeb7f` | **MATCH** |
| `script-reuse-crosswalk.csv` | `d892a73c72db6dcfd1cabf789d406edd05aa0f0cb668293eca83e405ffd49ed2` | `d892a73c72db6dcfd1cabf789d406edd05aa0f0cb668293eca83e405ffd49ed2` | **MATCH** |
| `module-capability-matrix.md` | `cd76e1e59de1323da660b8365bb9c1dcd7d88c30113c0f272a4cc10ad3eb687a` | `cd76e1e59de1323da660b8365bb9c1dcd7d88c30113c0f272a4cc10ad3eb687a` | **MATCH** |
| `gaps-and-collisions.md` | `3355cadea784be9ce1eb70579a6c2552f6493deaaff2f7dd7484630d5444cc29` | `3355cadea784be9ce1eb70579a6c2552f6493deaaff2f7dd7484630d5444cc29` | **MATCH** |

**Reproducibility Verdict:** 100% BIT-FOR-BIT IDENTICAL (0 variance across runs).

---

## 7. Sanitization & Workstation Path Audit

A full regex sweep was performed across all generated deliverables:
- Personal workstation path patterns (`/Users/*`): **0 detected**
- Secret key or token patterns (API tokens, private keys, PATs): **0 detected**
