# Verification Commands, Hashes, and Test Log (SKIL-16)

**Pinned Commit**: `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Test Execution Date**: `2026-11-02`  
**Execution Environment**: macOS Python 3.12+ (Standard Library Only)  
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

## 2. Independent Reproduction Commands & Execution Log

The zero-index inventory is 100% reproducible directly from the pinned source snapshot using only the Python standard library.

### Runtime Environment & Dependencies
- **Runtime**: Python 3.12+ (or 3.14+)
- **Dependencies**: Python standard library exclusively (`sys`, `os`, `json`, `csv`, `hashlib`, `re`, `pathlib`, `collections`, `argparse`). No third-party packages required.
- **Normalization Rules**:
  - JSON artifacts formatted with `indent=2`, keys sorted alphabetically (`sort_keys=True`), LF line endings (`\n`).
  - CSV artifacts formatted with standard comma delimiters, UTF-8 encoding, deterministic row ordering by `object_id` (`OBJ-00001` through `OBJ-05072`), LF line endings.
  - Reproducibility verification evaluates normalized payload files: `objects.csv`, `package-manifests.json`, `population-reconciliation.csv`, and `discrepancies.csv`.

### Executable Reproduction Shell Commands
```bash
# Set source root to pinned snapshot
SOURCE_ROOT="."

# Generate Run 1 into isolated temporary directory
python3 audit/zero-index/SKIL-16/scripts/generate_zero_index_inventory.py \
  --source "$SOURCE_ROOT" \
  --output /tmp/skil16-repro-run1 \
  --pinned-sha "195eda775d7a8dcad1837a1990bcba8259da3ea0" \
  --baseline-date "2026-11-02"

# Generate Run 2 into distinct clean directory for repeatability check
python3 audit/zero-index/SKIL-16/scripts/generate_zero_index_inventory.py \
  --source "$SOURCE_ROOT" \
  --output /tmp/skil16-repro-run2 \
  --pinned-sha "195eda775d7a8dcad1837a1990bcba8259da3ea0" \
  --baseline-date "2026-11-02"

# Execute cross-directory byte-for-byte SHA-256 verification and sanitization audit
python3 audit/zero-index/SKIL-16/scripts/verify_inventory.py \
  --run1 /tmp/skil16-repro-run1 \
  --run2 /tmp/skil16-repro-run2 \
  --pinned-sha "195eda775d7a8dcad1837a1990bcba8259da3ea0" \
  --baseline-date "2026-11-02"
```

### Execution Log & Exit Codes
- Generation Run 1 Exit Code: `0`
- Generation Run 2 Exit Code: `0`
- Verification Harness Exit Code: `0`

---

## 3. Deliverable Evidence Hashes (Run 1 Primary Output)

| Deliverable Artifact | File Bytes | SHA-256 Checksum |
|---|:---:|---|
| `baseline.json` | 3128 | `33fb90bb4658443466cf76ce4a71146de8c647621a469d999cb1f854205ff190` |
| `objects.csv` | 2281851 | `e01d0fb31416566e5f360e62a4e26a3f4dbd3330566671eedcd4293acf7300ab` |
| `package-manifests.json` | 12133699 | `10a71334a6abdac1bb850a5497e453260ce4955a3717fb0d7cc16be751f2ada5` |
| `population-reconciliation.csv` | 2581 | `fa48b5d3f70d75a7729171ec27b8f5a6d7f6403625a431b6b1f4022114a2faf7` |
| `discrepancies.csv` | 1669399 | `a294b6b29767f0249e5ea0486942ae9d9496cee4cfbb16817d156a556e32af3b` |
| `routing-and-provenance-report.md` | 7231 | `921a3be714c7e8c1afaaf947984892c72cc0cdeaa66c2f70611ecbf56879ffeb` |

---

## 4. Double-Run Cross-Directory Deterministic Repeatability Check

A secondary verification run was executed into an isolated scratch directory (`skil16-run2`).
Checksums for normalized payload files were computed and compared across the two distinct directories:

```text
Run 1 objects.csv:               e01d0fb31416566e5f360e62a4e26a3f4dbd3330566671eedcd4293acf7300ab
Run 2 objects.csv:               e01d0fb31416566e5f360e62a4e26a3f4dbd3330566671eedcd4293acf7300ab
Result:                          MATCH (Byte-Equal)

Run 1 package-manifests.json:    10a71334a6abdac1bb850a5497e453260ce4955a3717fb0d7cc16be751f2ada5
Run 2 package-manifests.json:    10a71334a6abdac1bb850a5497e453260ce4955a3717fb0d7cc16be751f2ada5
Result:                          MATCH (Byte-Equal)

Run 1 population-reconciliation: fa48b5d3f70d75a7729171ec27b8f5a6d7f6403625a431b6b1f4022114a2faf7
Run 2 population-reconciliation: fa48b5d3f70d75a7729171ec27b8f5a6d7f6403625a431b6b1f4022114a2faf7
Result:                          MATCH (Byte-Equal)

Run 1 discrepancies.csv:         a294b6b29767f0249e5ea0486942ae9d9496cee4cfbb16817d156a556e32af3b
Run 2 discrepancies.csv:         a294b6b29767f0249e5ea0486942ae9d9496cee4cfbb16817d156a556e32af3b
Result:                          MATCH (Byte-Equal)
```

Overall Cross-Directory Repeatability Status: **PASS**

---

## 5. Security & Workstation Path Sanitization Check

Executed regular expression inspection across all generated deliverables under `audit/zero-index/SKIL-16/`:
- **Workstation Path Pattern**: 0 occurrences detected.
- **Private Key / Secret Token Patterns**: 0 occurrences detected.
- **Git Working Tree Mutation**: 0 protected files touched; zero edits outside `audit/zero-index/`.

Calculated Sanitization Status: **PASS**
