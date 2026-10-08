# Skills Library Baseline Audit

This document establishes a fixed, traceable baseline of the skills library before any movement, conversion, consolidation, or restructuring operations begin in Phase 02 and beyond.

---

## Repository Identity

- **Name**: `REVREBEL/skills-rebuild`
- **Remote Fetch URL**: `https://github.com/REVREBEL/skills-rebuild.git`
- **Remote Push URL**: `https://github.com/REVREBEL/skills-rebuild.git`

---

## Branch State & Rollback Reference

- **Default Branch**: `main`
- **Dedicated Working Branch**: `skills-rebuild/phase-01-baseline`
- **Starting Commit SHA (Rollback Point)**: `d4355ae5c2727293c43c1a2dcfa5fc97e90a1474`

All original source skills in their pre-restructured state can be restored or referenced by checking out commit `d4355ae5c2727293c43c1a2dcfa5fc97e90a1474` from the `task-folder/agents/skills` directory.

---

## Resolved Physical Paths

Below is the mapping between logical task paths and their absolute, verified locations on the local filesystem:

| Logical Path | Physical Path | Verification Status | Purpose |
| :--- | :--- | :--- | :--- |
| `agents/skills` | `~/github-revrebel/skills-rebuild/task-folder/agents/skills` | **Verified** | Original source library containing skills to process. |
| `agents/not-needed` | `~/github-revrebel/skills-rebuild/task-folder/agents/not-needed` | **Verified** | Quarantine library for retired/unsupported skills. |
| `agents/skills-rebuild` | `~/github-revrebel/skills-rebuild/task-folder/agents/skills-rebuild` | **Verified** | Rebuilt library for active, canonical functional skills. |
| `.agents/skills` | `~/github-revrebel/skills-rebuild/.agents/skills` | **Verified** | Canonical task workflow library discoverable by runtime. |

---

## Task-Workflow Verification (`.agents/skills`)

The logical path `.agents/skills` resides at the project root and is successfully discovered by the IDE / agent runtime.
- **Master Router**: `.agents/skills/SKILL.md` (Skills Library Rebuild Task Router)
- **GitHub Operations Router**: `.agents/skills/github-operations/SKILL.md`
- **Skills Create, Manage & Update Router**: `.agents/skills/skills-create-manage-update/SKILL.md`

All child routers and skills linked within these master routers resolve correctly to active directories on the local filesystem.

---

## Source Library Directory Tree & Skill Folders

To provide a robust target for Phase 02 inventory reconciliation, the library population is captured using both a top-level directory check and a recursive search for active skill markers (`SKILL.md`) across all depths:

- **Total Top-Level Directories**: **738** non-hidden first-level directories under `task-folder/agents/skills`.
  - *Verification Command*: `find task-folder/agents/skills -mindepth 1 -maxdepth 1 -type d ! -name ".*" | wc -l`
- **Recursive Skill Folders (Canonical Skill Marker)**: **2,331** directories containing an active, uppercase `SKILL.md` file across all depths.
  - *Verification Command*: `find task-folder/agents/skills -name "SKILL.md" | wc -l`
  - *Note*: A single lowercase template file (`task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/templates/skill.md`) was identified and excluded as it is a template rather than an active skill.

### OS-Specific Metadata Exclusions
- The search and indexing operations detected no `__MACOSX` folders or `._*` AppleDouble files inside `task-folder/agents/skills`.
- `.DS_Store` files are present inside the root of the source folder and various subdirectories. These operating-system metadata files are explicitly **excluded** from all count, classification, and rebuilding workflows and must not be staged or committed.

---

## Existing Router Locations

Within the source skills folder (`task-folder/agents/skills`), there are no master or library-wide category routers. However, several domain/technique-specific router skills exist:

- `task-folder/agents/skills/pdf-conversion-router`
- `task-folder/agents/skills/fastapi-router-py`
- `task-folder/agents/skills/nextjs/nextjs-app-router-patterns`
- `task-folder/agents/skills/routerbase-model-gateway`
- `task-folder/agents/skills/marketing/digital-marketing-pro-main/scripts/language-router.py`

---

## Protected Work and Excluded Paths

The following paths represent pre-existing work, assets, configurations, or instructions:

### 1. Rebuild Workflows and Control Configuration (Narrow Protection)
- **Paths**: `.agents/` (including `.agents/skills/`) and `library-rebuild-tasks/` (including `task-objective.md`)
- **Rule**: These directories/files house control configurations, instructions, and scripts. They are explicitly excluded from all source-library rebuild operations to prevent accidental edits during the rebuild process. If corrections or improvements to these workflow files are required, they must only be changed through separate, explicitly scoped, and reviewed maintenance pull requests.

### 2. Static Documentation and Archives (Strict Protection)
- **Quarantine README**: `task-folder/agents/not-needed/README.md`
- **Rebuilt README**: `task-folder/agents/skills-rebuild/README.md`
- **Archived README**: `task-folder/agents/archived/README.md`
- **Rule**: These static markdown instructions and pre-existing documentation assets are strictly protected and must not be overwritten or deleted.

---

## Reconciliation Summary

- **Physical Directory Check**: All resolved paths have been verified as present and populated.
- **Router Check**: `.agents/skills/SKILL.md` and its child routers resolve.
- **Starting Commit and Branch**: Switched to branch `skills-rebuild/phase-01-baseline` at SHA `d4355ae5c2727293c43c1a2dcfa5fc97e90a1474`.
- **Integrity Guarantee**: No source skill was moved, rewritten, or deleted during this baseline process.
- **Skill Population Reconciliation**: Confirmed 738 top-level directories and exactly 2,331 canonical skill directories containing `SKILL.md`.
