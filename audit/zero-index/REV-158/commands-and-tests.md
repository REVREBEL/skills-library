# Verification Commands, Hashes, and Test Log (SKIL-16)

**Pinned Commit**: `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Test Execution Date**: `2026-11-02`  
**Execution Environment**: Sandboxed macOS Python 3.12  
**Linear Issue**: [SKIL-16](https://linear.app/revrebel/issue/SKIL-16/zi-01-pin-canonical-source-and-zero-index-inventory)  
**Legacy Reference**: REV-158  

---

## 1. Pinned Source Snapshot Integrity

| Target | Command | Expected Output | Exit Code | Calculated Status |
|---|---|---|:---:|:---:|
| `origin/main` SHA Verification | `git rev-parse HEAD` | `195eda775d7a8dcad1837a1990bcba8259da3ea0` | 0 | **PASS** |
| Snapshot Read-Only Lock | `ls -ld scratch/pinned-snapshot` | Permissions locked (`a-w` content dirs) | 0 | **PASS** |
| Repository Index Cleanliness | `git status --porcelain` | Clean (no untracked source files) | 0 | **PASS** |

---

## 2. Deliverable Evidence Hashes (Run 1 Primary Output)

| Deliverable Artifact | File Bytes | SHA-256 Checksum |
|---|:---:|---|
| `baseline.json` | 2512 | `38d1956fb61cb85b7deca03556e19f965d0a88de61266f37bf665cfc40b577dc` |
| `objects.csv` | 2340390 | `7e688dff6cbf700d6607945e993c9abcfa722b1c4671c1e94d96317f1a9cb12b` |
| `package-manifests.json` | 12184752 | `4e6b7ce219e0ac030b024cdbeefbd22feafdcaff08902597921177ca1e2984d9` |
| `population-reconciliation.csv` | 2167 | `80f8ca23f75891419f9d896aff32ede2c0a833ed6b78a662c8e7c311571d6a6b` |
| `discrepancies.csv` | 894043 | `0214b3b9b244cfbbbc70106595d6a25daf07968114e0861e7087c25f3cde17c7` |
| `routing-and-provenance-report.md` | 5159 | `6fee7079800cfd64dd634e363819fc72c9124fa908d0f36402538d3ccb102d0a` |

---

## 3. Double-Run Cross-Directory Deterministic Repeatability Check

A secondary verification run was executed into an isolated scratch directory (`skil16-run2`).
Checksums for normalized payload files were computed and compared across the two distinct directories:

```text
Run 1 objects.csv:               7e688dff6cbf700d6607945e993c9abcfa722b1c4671c1e94d96317f1a9cb12b
Run 2 objects.csv:               7e688dff6cbf700d6607945e993c9abcfa722b1c4671c1e94d96317f1a9cb12b
Result:                          MATCH (Byte-Equal)

Run 1 package-manifests.json:    4e6b7ce219e0ac030b024cdbeefbd22feafdcaff08902597921177ca1e2984d9
Run 2 package-manifests.json:    4e6b7ce219e0ac030b024cdbeefbd22feafdcaff08902597921177ca1e2984d9
Result:                          MATCH (Byte-Equal)

Run 1 population-reconciliation: 80f8ca23f75891419f9d896aff32ede2c0a833ed6b78a662c8e7c311571d6a6b
Run 2 population-reconciliation: 80f8ca23f75891419f9d896aff32ede2c0a833ed6b78a662c8e7c311571d6a6b
Result:                          MATCH (Byte-Equal)

Run 1 discrepancies.csv:         0214b3b9b244cfbbbc70106595d6a25daf07968114e0861e7087c25f3cde17c7
Run 2 discrepancies.csv:         0214b3b9b244cfbbbc70106595d6a25daf07968114e0861e7087c25f3cde17c7
Result:                          MATCH (Byte-Equal)
```

Overall Cross-Directory Repeatability Status: **PASS**

---

## 4. Security & Workstation Path Sanitization Check

Executed regular expression inspection across all generated deliverables under `audit/zero-index/SKIL-16/`:
- **Workstation Path Pattern**: 0 occurrences detected.
- **Private Key / Secret Token Patterns**: 0 occurrences detected.
- **Git Working Tree Mutation**: 0 protected files touched; zero edits outside `audit/zero-index/SKIL-16/`.

Calculated Sanitization Status: **PASS**
