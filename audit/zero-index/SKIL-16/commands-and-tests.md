# Verification Commands, Hashes, and Test Log (SKIL-16)

**Pinned Commit**: `195eda775d7a8dcad1837a1990bcba8259da3ea0`  
**Test Execution Date**: `2026-11-02`  
**Execution Environment**: macOS Python 3.12+ (Standard Library Only)  
**Linear Issue**: [SKIL-16](https://linear.app/revrebel/issue/SKIL-16/zi-01-pin-canonical-source-and-zero-index-inventory)  
**Legacy Reference**: REV-158  

---

## 1. Live Pinned Source Snapshot Verification

The test harness executes live git commands directly against the isolated pinned source repository at `/private/tmp/skil16-pinned-source` to guarantee that evidence is generated strictly from the immutable canonical snapshot.

| Target | Command | Real Exit Code | Actual Output / Live Result | Calculated Status |
|---|---|:---:|---|:---:|
| `origin/main` SHA Verification | `git rev-parse HEAD` | `0` | `195eda775d7a8dcad1837a1990bcba8259da3ea0` | **PASS** |
| Repository Index Cleanliness | `git status --porcelain` | `0` | `0` uncommitted modifications | **PASS** |
| Tracked File Enumeration | `git ls-files` | `0` | `5072` tracked `SKILL.md` / `skill.md` files | **PASS** |

---

## 2. Cryptographic Manifest Content Integrity

The harness validates 100% of discovered packages and constituent files against disk content at `/private/tmp/skil16-pinned-source`:

| Metric | Measured Value | Requirement | Status |
|---|:---:|:---:|:---:|
| **Total Package Manifests Checked** | `5072` | Equal to total discovered packages | **PASS** |
| **Package Manifests Cryptographically Verified** | `5072` | 100% digest match | **PASS** |
| **Constituent Files Checked on Disk** | `40191` | All package files exist | **PASS** |
| **File SHA-256 Hashes Verified** | `40191` | 100% byte-for-byte SHA-256 match | **PASS** |
| **Mismatches / Unresolved Files** | `0` | 0 mismatches allowed | **PASS** |

---

## 3. Negative-Path Fail-Closed Test Suite

To prove that the verification harness and generator fail closed rather than producing unverified evidence, a suite of negative-path tests was executed:

| Test Case | Injected Fault | Expected Behavior | Actual Observation | Status |
|---|---|---|---|:---:|
| **Wrong Commit SHA** | Query SHA `0000000000000000000000000000000000000000` | Refuse generation / fail verification | Correctly rejected mismatch (expected 00000..., actual 195eda775d7a8dcad1837a1990bcba8259da3ea0) | **PASS** |
| **Non-Git Directory** | Point source to empty temp directory | Fail with non-zero git exit code | Correctly returned git exit code 128 | **PASS** |
| **Manifest Content Tampering** | Mutate file hash in `package-manifests.json` | Detect file hash & digest mismatch | Caught 2 deliberate tampering mismatch(es) | **PASS** |

---

## 4. Independent Reproduction Commands & Execution Log

The zero-index inventory is 100% reproducible directly from the pinned source checkout using only the Python standard library. The generator and harness reside in the task deliverables branch (`audit/zero-index/SKIL-16/scripts/`) and are executed against an isolated read-only source checkout.

### Runtime Environment & Dependencies
- **Runtime**: Python 3.12+ (or 3.14+)
- **Dependencies**: Python standard library exclusively (`sys`, `os`, `json`, `csv`, `hashlib`, `re`, `pathlib`, `collections`, `argparse`, `subprocess`, `tempfile`). No third-party packages required.
- **Normalization Rules**:
  - JSON artifacts formatted with `indent=2`, keys sorted alphabetically (`sort_keys=True`), LF line endings (`\n`).
  - CSV artifacts formatted with standard comma delimiters, UTF-8 encoding, deterministic row ordering by `object_id` (`OBJ-00001` through `OBJ-05072`), LF line endings.
  - Reproducibility verification evaluates normalized payload files: `objects.csv`, `package-manifests.json`, `population-reconciliation.csv`, `discrepancies.csv`, and `routing-and-provenance-report.md`.

### Executable Reproduction Shell Commands
```bash
# 1. Create a clean pinned source worktree or clone
SOURCE_ROOT="/tmp/skil16-pinned-source"
git worktree add --detach "$SOURCE_ROOT" 195eda775d7a8dcad1837a1990bcba8259da3ea0

# 2. Path to generator script (located in the task branch)
SCRIPT_DIR="audit/zero-index/SKIL-16/scripts"

# 3. Generate Run 1 into isolated directory
python3 "$SCRIPT_DIR/generate_zero_index_inventory.py" \
  --source "$SOURCE_ROOT" \
  --output /tmp/skil16-repro-run1 \
  --pinned-sha "195eda775d7a8dcad1837a1990bcba8259da3ea0" \
  --baseline-date "2026-11-02"

# 4. Generate Run 2 into distinct directory for repeatability check
python3 "$SCRIPT_DIR/generate_zero_index_inventory.py" \
  --source "$SOURCE_ROOT" \
  --output /tmp/skil16-repro-run2 \
  --pinned-sha "195eda775d7a8dcad1837a1990bcba8259da3ea0" \
  --baseline-date "2026-11-02"

# 5. Execute live git verification, cryptographic manifest audit, repeatability check, and negative tests
python3 "$SCRIPT_DIR/verify_inventory.py" \
  --source "$SOURCE_ROOT" \
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

## 5. Deliverable Evidence Hashes (Run 1 Primary Output)

| Deliverable Artifact | File Bytes | SHA-256 Checksum |
|---|:---:|---|
| `baseline.json` | 4669 | `a6de4a0364835855635e5f7ee435e85cbe70422ba3bc2a842577ee93e1ab7885` |
| `objects.csv` | 2281683 | `a02f78f8cc526848cd96e7c915829e81fd0e7c14d99637dcbb41560efccf9414` |
| `package-manifests.json` | 12126045 | `01d8ff3e3d5edbe744f046b0fe4398a089a78f0cee1073fc2005666b9baa269f` |
| `population-reconciliation.csv` | 2637 | `ef74c395aa0e5080a8c94f4c45fe069542eb5a7b9a09a8d72e5e90b7c62b6336` |
| `discrepancies.csv` | 774427 | `617f1e79b534786b1b864fe925df7325351ce356f0b04b32b2ee2782875ebab2` |
| `routing-and-provenance-report.md` | 6072 | `18b6537b58f33972be49d1b88840baa78870f8e98637c6d0b35b9dbd448e922c` |

---

## 6. Double-Run Cross-Directory Deterministic Repeatability Check

Checksums for normalized payload files were computed and compared across the two distinct directories:

```text
Run 1 objects.csv:               a02f78f8cc526848cd96e7c915829e81fd0e7c14d99637dcbb41560efccf9414
Run 2 objects.csv:               a02f78f8cc526848cd96e7c915829e81fd0e7c14d99637dcbb41560efccf9414
Result:                          MATCH (Byte-Equal)

Run 1 package-manifests.json:    01d8ff3e3d5edbe744f046b0fe4398a089a78f0cee1073fc2005666b9baa269f
Run 2 package-manifests.json:    01d8ff3e3d5edbe744f046b0fe4398a089a78f0cee1073fc2005666b9baa269f
Result:                          MATCH (Byte-Equal)

Run 1 population-reconciliation: ef74c395aa0e5080a8c94f4c45fe069542eb5a7b9a09a8d72e5e90b7c62b6336
Run 2 population-reconciliation: ef74c395aa0e5080a8c94f4c45fe069542eb5a7b9a09a8d72e5e90b7c62b6336
Result:                          MATCH (Byte-Equal)

Run 1 discrepancies.csv:         617f1e79b534786b1b864fe925df7325351ce356f0b04b32b2ee2782875ebab2
Run 2 discrepancies.csv:         617f1e79b534786b1b864fe925df7325351ce356f0b04b32b2ee2782875ebab2
Result:                          MATCH (Byte-Equal)

Run 1 routing-report:            18b6537b58f33972be49d1b88840baa78870f8e98637c6d0b35b9dbd448e922c
Run 2 routing-report:            18b6537b58f33972be49d1b88840baa78870f8e98637c6d0b35b9dbd448e922c
Result:                          MATCH (Byte-Equal)
```

Overall Cross-Directory Repeatability Status: **PASS**

---

## 7. Security & Workstation Path Sanitization Check

Executed regular expression inspection across all generated deliverables under `audit/zero-index/SKIL-16/`:
- **Workstation Path Pattern**: 0 occurrences detected.
- **Private Key / Secret Token Patterns**: 0 occurrences detected.
- **Git Working Tree Mutation**: 0 protected files touched; zero edits outside `audit/zero-index/`.

Calculated Sanitization Status: **PASS**
