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
| `baseline.json` | 3579 | `f13dd905e9360b32806057ed20a57fdaaae7dc3dddc6905889214106b9ca68f0` |
| `objects.csv` | 2281851 | `06a9416dc0c6dc7948178f7627aa31b9b28ee8c72d109ccbbe69b76fa364f49e` |
| `package-manifests.json` | 12126213 | `47b9041a0f5e2c317af2cb7354418b535ef350fcbecd2327cf35023228fa2688` |
| `population-reconciliation.csv` | 2598 | `e938353a7932efc25f1229f23cfe4d4b51d0e536efe3ac226909baa5d2a6f9e4` |
| `discrepancies.csv` | 1669399 | `81bd43f2b0e26891e3a7d45e0525891ac2647d259c814598002a19d5fe538424` |
| `routing-and-provenance-report.md` | 7432 | `99337b93a51975e66b91118025e58b13e890d29a96f55a71d994c572ca6e8a0a` |

---

## 4. Double-Run Cross-Directory Deterministic Repeatability Check

A secondary verification run was executed into an isolated scratch directory (`skil16-run2`).
Checksums for normalized payload files were computed and compared across the two distinct directories:

```text
Run 1 objects.csv:               06a9416dc0c6dc7948178f7627aa31b9b28ee8c72d109ccbbe69b76fa364f49e
Run 2 objects.csv:               06a9416dc0c6dc7948178f7627aa31b9b28ee8c72d109ccbbe69b76fa364f49e
Result:                          MATCH (Byte-Equal)

Run 1 package-manifests.json:    47b9041a0f5e2c317af2cb7354418b535ef350fcbecd2327cf35023228fa2688
Run 2 package-manifests.json:    47b9041a0f5e2c317af2cb7354418b535ef350fcbecd2327cf35023228fa2688
Result:                          MATCH (Byte-Equal)

Run 1 population-reconciliation: e938353a7932efc25f1229f23cfe4d4b51d0e536efe3ac226909baa5d2a6f9e4
Run 2 population-reconciliation: e938353a7932efc25f1229f23cfe4d4b51d0e536efe3ac226909baa5d2a6f9e4
Result:                          MATCH (Byte-Equal)

Run 1 discrepancies.csv:         81bd43f2b0e26891e3a7d45e0525891ac2647d259c814598002a19d5fe538424
Run 2 discrepancies.csv:         81bd43f2b0e26891e3a7d45e0525891ac2647d259c814598002a19d5fe538424
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
