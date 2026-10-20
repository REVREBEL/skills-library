# Task 09: Clean Bundled Resources

## Objective

Ensure every bundled script, reference, asset, and template in the rebuilt library is necessary, correctly classified, safely usable, and linked from an active canonical skill.

## Preconditions

- Canonical functional batches are complete and their batch records exist.
- Inventory, destination, consolidation, split, and provider-conversion records reconcile with the active rebuilt library.
- `.agents/skills` is the verified canonical task-workflow path.
- Quarantined and retired sources are excluded except when tracing provenance or comparing suspected duplicates.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-audit/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-improver/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-check/SKILL.md`

Use `skill-audit` for safety, dependency, secret, and compatibility findings; `skill-improver` for approved repairs; and `skill-check` for resource and path validation. Use `.agents/skills/github-operations/SKILL.md` for repository history, diff review, commits, and publication.

## Work

1. Enumerate all bundled resources under active canonical skill folders.
2. Map every resource to the skill and workflow that uses it.
3. Inspect for:
   - Unused or orphaned resources
   - Duplicate scripts with different names
   - Similar scripts with materially different behavior
   - Broken relative paths and missing files
   - Stale API or platform documentation
   - Oversized examples that belong in references
   - Editable scaffolds stored as assets
   - Static files stored as templates
   - Credentials, tokens, private keys, internal URLs, or personal data
   - Generated files, caches, `__MACOSX`, `.DS_Store`, and `._*`
4. Compare suspected duplicate scripts by content and behavior before deciding.
5. Remove confirmed generated or unused resources while preserving Git history.
6. Move resources into the correct `scripts/`, `references/`, `assets/`, or `templates/` location.
7. Repair every active relative reference.
8. Review scripts for input validation, destructive behavior, hardcoded paths, and undeclared dependencies.
9. Validate the final resource tree against active canonical skills.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/resource-cleanup-report.md`

The report must list every reviewed resource, owning skill, original and final path, disposition, evidence, repair or movement performed, validation result, and deferred issue.

## Reconciliation Requirements

- Reconcile every active bundled resource to an owning skill or documented preservation reason.
- Reconcile moved and removed resources to Git history and final filesystem state.
- Confirm every active resource reference resolves from its owning `SKILL.md`.
- Confirm resource counts in the cleanup report match the active resource tree.
- Confirm no generated metadata, secret, or unsafe undeclared dependency remains.

## Repository Checkpoint

1. Begin only after Phase 08 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-09-resource-cleanup` from the updated `main` branch.
3. Review the final diff and confirm it contains only approved resource cleanup, reference repairs, the cleanup report, and directly required supporting changes.
4. Commit the completed phase with: `skills-rebuild: complete phase 09 resource cleanup`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize resources reviewed, retained, moved, removed, repaired, or deferred, plus artifact paths, safety findings, validation, and reconciliation evidence.
7. Leave the pull request unmerged for review. Do not begin Phase 10 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- The cleanup report exists with complete resource coverage.
- Every active resource has an owner or documented preservation reason.
- All active paths and references resolve.
- Filesystem, batch records, inventory, and cleanup decisions reconcile.
- The phase branch is pushed and its draft pull request is open for review.