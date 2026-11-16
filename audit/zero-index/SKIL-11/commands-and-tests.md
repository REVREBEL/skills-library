# Commands and Tests Log: SKIL-11 (ZI-06)

## Overview
This document records the exact reproduction commands, verification outputs, and cryptographic digests for the Language, Integrity, and Exposure Audit (**SKIL-11 / ZI-06**).

## Reproduction Commands

### 1. Execute Full Language, Resource & AST Audit
```bash
python3 tools/validate_semantic_census.py
```
* **Exit code**: `0`
* **Execution time**: ~18s
* **Population processed**: 2,133 skills
* **Resources inspected**: 7,881 files

### 2. Run Test Suite
```bash
python3 -m unittest tests/test_language_integrity_audit.py
```
* **Exit code**: `0`
* **Coverage**: Invariant verification, scanner unit correctness, regeneration parity, and fault-injection gate tests.

```bash
python3 -m unittest tests/test_semantic_census.py tests/test_semantic_object_model.py tests/test_physical_ownership.py tests/test_migration_gates.py
```
* **Exit code**: `0`
* **Test results**: 120 regression suite tests passed.

## Evidence Artifact Hashes (SHA-256)

| Artifact File | Size (Bytes) | SHA-256 Digest |
|---|---|---|
| `language-audit.csv` | 530,233 | `0d7039a2efd46919e7065fbc38b15eeac90729534dfca9d8fe4d7132b95ca563` |
| `integrity-and-exposure-findings.csv` | 1,686,336 | `de9db0ccfff86a2a9f8edbc9951cd72535ad0e5418a835fc444f3d7da4ad1fa8` |
| `quarantine-candidates.csv` | 6,408 | `17d93135c539f18c2f136953f7182d3651823833acd2331ddbf269564ae9373d` |
| `language-integrity-exposure-summary.json` | 1,302 | `51e04566ea98dda5a12eb28d75655b3adc1c2a467fd62ced1d85af1f66d1dfc1` |

## Verification Gate Assertions
1. **100% Population Coverage**: Exactly 2,133 skills audited with zero unhandled exceptions.
2. **Deterministic Script Verification**: All 508 Python scripts parsed with Python AST parser (0 SyntaxErrors).
3. **Safe Static Execution**: Dangerous calls flagged for review without mutating on-disk packages.
4. **Zero Template Leaks**: Automated gate certified 0 template leaks or unresolved brackets across outputs.
5. **Non-Destructive Compliance**: Zero skills moved or deleted; all quarantine recommendations documented neutrally.
