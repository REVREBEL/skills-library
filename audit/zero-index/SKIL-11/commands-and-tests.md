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
* **Resources inspected**: 8,078 files

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
| `language-audit.csv` | 543,706 | `6eec55c35e2ee9d03740abc0f3c98c11e9e26c4cab8ecbc772c6e87386cdf25b` |
| `integrity-and-exposure-findings.csv` | 1,729,157 | `9e918a22504a551cb83efee802c6fe992cfa9e1dff89bec135b8237bdef0f1fb` |
| `quarantine-candidates.csv` | 19,774 | `d6076ca2c672136c786d6079627599fa73170745ead1c2bcc85596cd7adda50e` |
| `language-integrity-exposure-summary.json` | 1,386 | `de9687a6542ed94fef3a663b85f9796a59d47ce5f30d4d8a317f25e4a12aa06b` |

## Verification Gate Assertions
1. **100% Population Coverage**: Exactly 2,133 skills audited with zero unhandled exceptions.
2. **Deterministic Script Verification**: All 521 Python scripts parsed with Python AST parser (0 SyntaxErrors).
3. **Safe Static Execution**: Dangerous calls flagged for review without mutating on-disk packages.
4. **Zero Template Leaks**: Automated gate certified 0 template leaks or unresolved brackets across outputs.
5. **Non-Destructive Compliance**: Zero skills moved or deleted; all quarantine recommendations documented neutrally.
