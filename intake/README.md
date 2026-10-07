# Skill Intake Staging Area

This directory serves as the non-destructive staging area for new, updated, or externally discovered skill packages.

## Intake Sources

A skill enters `intake/` through:
1. **Manual Placement**: A contributor or developer drops a skill folder here for evaluation.
2. **External Installer Discovery**: The runtime synchronization tool (`tools/skill-library.py sync` or `scan`) discovers an unmanaged physical folder created in `.agents/skills` (e.g. by `skills.sh`) and stages it here for safe processing.
3. **Repository Import**: Skills imported from external repositories or packages.
4. **Substantial Reprocessing**: Existing canonical skills requiring major refactoring or re-evaluation.

## Intake Lifecycle

```text
Staged Candidate (intake/<skill-name>)
       ↓
Evaluation & Validation (`python3 tools/skill-library.py intake`)
       ↓
Review / Approval / Normalization
       ↓
Canonical Installation (`python3 tools/skill-library.py apply`)
       ↓
Runtime Symlink Sync (`python3 tools/skill-library.py sync`)
```

*Note: Intake is temporary staging. Approved skills move into `library/`. Rejected or quarantined packages are preserved with actionable reports.*
