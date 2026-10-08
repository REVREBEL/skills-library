# Agent Skills Library & Runtime Workflow Guide

This guide describes the operational architecture, lifecycle workflows, command-line interface, and recovery procedures for the **REVREBEL Agent Skills Library**.

---

## 1. Architectural Model

The Agent Skills platform enforces a strict separation of concerns between canonical Git version control and agent runtime discovery:

```text
External Install / User Staged Candidate
                  ↓
          intake/ (staging)
                  ↓
       review / normalize / classify
                  ↓
     library/ (canonical source of truth)
                  ↓
            symbolic link
                  ↓
          ~/.agents/skills/ (global discovery runtime)
```

### Canonical Source of Truth (`library/`)
- All approved, production-grade agent skills reside exclusively under `library/` within this repository.
- No duplicate physical copies of active skills exist in the repository.
- Structured across **10 top-level functional categories**:
  - **Deep Categories** (with subcategory router hierarchies):
    - `development/` (6 subcategories: backend, frontend, fullstack, mobile, software-architecture, systems)
    - `marketing-and-seo/` (5 subcategories: content-and-campaigns, cro, geo-and-local-seo, on-page-seo, technical-seo)
    - `design-and-experience/` (4 subcategories: design-systems, motion-and-graphics, taste-and-critique, ui-ux)
  - **Flat Categories** (with direct leaf skill listings grouped by subcategory header):
    - `business-and-operations/` (4 subcategories: hospitality-domain, product-management, startup-finance, strategy)
    - `content-and-documentation/` (4 subcategories: brand-voice, copy-and-messaging, presentations, technical-writing)
    - `data-and-ai/` (5 subcategories: analytics, data-engineering, llm-and-rag, machine-learning, vector-databases)
    - `infrastructure-and-ops/` (5 subcategories: ci-cd, cloud-platforms, containers-and-orchestration, observability, server-management)
    - `meta-and-agent-skills/` (3 subcategories: agent-architecture, skill-lifecycle, skill-validation)
    - `quality-and-security/` (4 subcategories: compliance, debugging, security, testing)
    - `workflow-and-automation` (4 subcategories: git-and-vcs, task-orchestration, tool-integration, web-scraping)

### Global Runtime Discovery Layer (`~/.agents/skills/`)
- `~/.agents/skills/` is the global active discovery endpoint used by agents, tools, CLIs, and IDE extensions on macOS.
- Every canonical skill in `library/` is exposed in `~/.agents/skills/` as an **individual relative symbolic link** (e.g., `~/.agents/skills/bug-hunter -> ../../github-revrebel/skills-library/library/quality-and-security/debugging/bug-hunter`).
- Repo-local `.agents/skills` is deprecated, removed from git tracking, and added to `.gitignore`.
- **Protected Entries**:
  - `~/.agents/skills/SKILL.md` (root agent task discovery router)
  - `~/.agents/skills/github-operations` (canonical git/PR workflow skills)
  - `~/.agents/skills/skills-create-manage-update` (canonical skill authoring/audit skills)
  These entries are protected and will never be overwritten, unmanaged, or modified by sync.

### Runtime Manifest (`audit/runtime-manifest.json`)
- Serves as the authoritative index mapping flat runtime names to their canonical locations and parent routers.
- Automatically handles skill-name collisions across categories by prefixing category namespaces (e.g. `data-and-ai-analytics` vs `marketing-and-seo-analytics`).

### Permanent Change Ledger (`audit/change-ledger.jsonl`)
- Append-only audit record tracking every addition, modification, deprecation, and synchronization event.
- Records timestamp, operator, source, canonical path, runtime name, decision rationale, and validation status.

---

## 2. Intake Pipeline & Lifecycle

New skills enter the repository through the temporary staging directory: `intake/`.

```text
Staged in intake/ -> Scanned -> Evaluated -> Human Approval Gate -> Installed to library/ -> Symlinked
```

### Entry Channels
1. **Manual Staging**: An engineer or author places a skill package into `intake/<candidate-name>`.
2. **External Installers (`skills.sh`, etc.)**: When an external tool creates a physical directory in `~/.agents/skills/`, running `python3 tools/skill-library.py sync` automatically detects the unmanaged folder, copies it safely into `intake/<candidate-name>`, preserves installer metadata (`.installer-metadata.json`), and queues it for intake.

### Evaluation Criteria
When running `python3 tools/skill-library.py intake`, candidates undergo automated evaluation:
1. **Package Integrity**: Must contain valid YAML frontmatter in `SKILL.md` with `name` and `description`.
2. **Discovery Trigger Contract**: Description must satisfy progressive disclosure syntax (`^[A-Z].*\.\s+Use when\b`).
3. **Provider Decoupling**: Scans for vendor couplings (e.g. `Claude`, `Anthropic`). During application, packages are normalized to vendor-neutral terms (`Agent`, `AI Platform`).
4. **Workstation Leaks & Secret Scanning**: Rejects packages with hardcoded personal user directories (`/Users/...`, `/home/...`) or cryptographic credentials.
5. **Semantic Overlap & Competitor Analysis**: Evaluates candidate description and triggers against all canonical skills using Dice similarity metrics. Identifies closest existing skills.
6. **Decision Recommendation**:
   - `NEW`: Valid, distinct, no conflict.
   - `KEEP_SEPARATE`: Moderate overlap with an existing skill, but distinct scope.
   - `MERGE`: High overlap (>55%) with existing skill; recommend consolidating into existing package.
   - `RENAME`: Name collision with distinct functional scope.
   - `REJECT`: True duplicate (>75% overlap + name collision) or invalid package.
   - `REVIEW_REQUIRED`: Ambiguous routing, destructive actions, or syntax errors.

---

## 3. Human Approval Gate

The pipeline prevents autonomous overwriting or silent duplicates. The human approval gate halts execution when:
- **High Semantic Overlap**: When a candidate significantly overlaps with an existing canonical skill.
- **Merge Recommendations**: When consolidating instructions rather than adding redundant files.
- **Runtime Name Collisions**: When a candidate package name conflicts with an existing runtime link.
- **Destructive Commands**: When candidate scripts execute destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`).

The gate outputs:
- **Candidate Name** and directory
- **Issue Detected**
- **Recommended Action** (`NEW`, `MERGE`, `KEEP_SEPARATE`, `RENAME`, `REJECT`)
- **Reason & Similarity Score**
- **Affected Canonical Skills**
- **Operator Options**

---

## 4. CLI Command Reference

All operations are executed via `tools/skill-library.py`:

### `scan`
Non-destructively inspects `intake/` and `~/.agents/skills/`.
```bash
python3 tools/skill-library.py scan
python3 tools/skill-library.py scan --json
```

### `intake`
Evaluates staged candidates in `intake/`, computes overlap scores, and checks approval gates.
```bash
python3 tools/skill-library.py intake
python3 tools/skill-library.py intake --candidate my-new-skill
python3 tools/skill-library.py intake --json
```

### `apply`
Installs an approved candidate from `intake/` into its permanent location in `library/`, updates the parent router markdown, updates `audit/runtime-manifest.json`, and records the transaction in `audit/change-ledger.jsonl`.
```bash
python3 tools/skill-library.py apply \
  --candidate my-new-skill \
  --category infrastructure-and-ops \
  --subcategory observability
```

### `sync`
Reconciles runtime symlinks in `~/.agents/skills/` against `audit/runtime-manifest.json`.
- Creates missing symlinks.
- Verifies and repairs broken symlinks.
- Stages external physical folders into `intake/`.
- Preserves protected system skills.
- Fully idempotent.
```bash
python3 tools/skill-library.py sync
python3 tools/skill-library.py sync --dry-run
python3 tools/skill-library.py sync --no-stage
```

### `validate`
Runs the living library validator across all routers, links, leaf skills, manifest entries, and symlinks.
```bash
python3 tools/skill-library.py validate
python3 tools/skill-library.py validate --output-report
```

### `status`
Displays a concise health and count dashboard.
```bash
python3 tools/skill-library.py status
```

### `test`
Executes the automated end-to-end test suite verifying Scenarios A through F.
```bash
python3 tools/skill-library.py test
```

---

## 5. End-to-End Walkthrough: Adding a New Skill

1. **Place package in staging**:
   ```bash
   mkdir -p intake/my-telemetry-agent
   cat << 'EOF' > intake/my-telemetry-agent/SKILL.md
   ---
   name: my-telemetry-agent
   description: Real-time telemetry monitoring agent. Use when configuring telemetry stream processing.
   ---
   # Telemetry Agent
   Instructions...
   EOF
   ```

2. **Evaluate candidate**:
   ```bash
   python3 tools/skill-library.py intake --candidate my-telemetry-agent
   ```

3. **Install approved candidate**:
   ```bash
   python3 tools/skill-library.py apply \
     --candidate my-telemetry-agent \
     --category infrastructure-and-ops \
     --subcategory observability
   ```

4. **Synchronize runtime discovery**:
   ```bash
   python3 tools/skill-library.py sync
   ```

5. **Verify library health**:
   ```bash
   python3 tools/skill-library.py validate
   ```

---

## 6. Recovery & Troubleshooting Procedures

### Broken Symlinks in `~/.agents/skills/`
- **Symptom**: `python3 tools/skill-library.py status` reports `Broken links > 0`.
- **Cause**: A canonical folder was moved or renamed without running `apply`/`sync`.
- **Resolution**:
  ```bash
  python3 tools/skill-library.py sync
  ```
  `sync` automatically redirects managed symlinks back to their canonical targets as defined in `audit/runtime-manifest.json`.

### Physical Directory Installed into `~/.agents/skills/` by External Tool
- **Symptom**: `python3 tools/skill-library.py status` reports `New external installs > 0`.
- **Cause**: An installer like `skills.sh` created a physical directory directly in `~/.agents/skills/`.
- **Resolution**:
  1. Run `python3 tools/skill-library.py sync`. This safely copies the package into `intake/<name>` with its `.installer-metadata.json`.
  2. Run `python3 tools/skill-library.py intake` to review and normalize the candidate.
  3. Run `python3 tools/skill-library.py apply` to install it into `library/`.
  4. The apply process replaces the external directory with the canonical relative symlink.

### Runtime Name Collision
- **Symptom**: `python3 tools/skill-library.py intake` outputs `[HUMAN APPROVAL GATE]` with `Name collision with existing runtime skill`.
- **Resolution**:
  - If distinct functionality: supply `--canonical-name` or use a category namespace prefix (e.g. `--canonical-name cloud-observability`).
  - If duplicate: remove candidate from `intake/` and update the existing canonical skill.
