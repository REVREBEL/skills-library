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
* **Resources inspected**: 8,172 files

### 2. Run Test Suite
```bash
python3 -m unittest tests/test_semantic_census.py
```
* **Exit code**: `0`
* **Test results**: 10 tests passed in 0.095s.

```bash
python3 -m unittest tests/test_semantic_object_model.py tests/test_physical_ownership.py
```
* **Exit code**: `0`
* **Test results**: 54 tests passed.

## Evidence Artifact Hashes (SHA-256)

| Artifact File | Size (Bytes) | SHA-256 Digest |
|---|---|---|
| `language-audit.csv` | 543,706 | `6eec55c35e2ee9d03740abc0f3c98c11e9e26c4cab8ecbc772c6e87386cdf25b` |
| `integrity-and-exposure-findings.csv` | 1,746,072 | `1dff50c0eee74edcbb2c225e971bb7bd87c6f2e739d6a3b53a55eccb51d72174` |
| `quarantine-candidates.csv` | 19,949 | `20d220e37d4c527d7903563c907a40e553daf2dfbf50fecdabde5e24141b9999` |
| `language-integrity-exposure-summary.json` | 1,296 | `ea67b096c54f57fad70e319d70f3c3b198dcb1b37039eb21a83bc02624d01047` |

## Verification Gate Assertions
1. **100% Population Coverage**: Exactly 2,133 skills audited with zero unhandled exceptions.
2. **Deterministic Script Verification**: All 521 Python scripts parsed with Python AST parser (0 SyntaxErrors).
3. **Safe Static Execution**: Dangerous calls flagged for review without mutating on-disk packages.
4. **Zero Template Leaks**: Automated gate certified 0 template leaks or unresolved brackets across outputs.
5. **Non-Destructive Compliance**: Zero skills moved or deleted; all quarantine recommendations documented neutrally.
