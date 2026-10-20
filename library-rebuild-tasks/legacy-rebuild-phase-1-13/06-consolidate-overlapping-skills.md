# Task 06: Consolidate Overlapping Skills

## Objective

Resolve retained skills that share substantially the same trigger, workflow, or output by selecting canonical owners and preserving unique material without duplicate active discovery.

## Preconditions

- Inventory, compatibility, provider-conversion, taxonomy, and destination-map artifacts exist and reconcile.
- `.agents/skills` is the verified canonical task-workflow path.
- Retained skills are assigned to proposed functional destinations.
- Overlap clusters are identified but not assumed to be duplicates by name alone.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-library-restructure/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-improver/SKILL.md`

Use `skill-review` for canonical-owner and disposition decisions, `skill-library-restructure` for merge structure and routing consequences, and `skill-improver` for approved canonical repairs. Use `.agents/skills/github-operations/SKILL.md` for reviewable branches, diffs, commits, and publication.

## Work

1. Review one functional overlap cluster at a time.
2. Compare actual contents and bundled resources, including:
   - User triggers and functional outcome
   - Required inputs, tools, permissions, and applications
   - Execution workflow
   - Risk and authorization gates
   - Validation and completion evidence
   - Scripts, references, assets, and templates
   - Unique instructions worth preserving
3. Assign one decision to each cluster:
   - Keep separately
   - Merge into one canonical skill
   - Convert one source into a reference or template
   - Preserve a temporary compatibility alias
   - Retire a true duplicate
   - Defer for manual review
4. Select the canonical owner for each duplicate workflow.
5. Merge unique, valid material into the canonical destination.
6. Move superseded active sources out of discovery without deleting Git history.
7. Preserve source-to-canonical provenance.
8. Verify no active router links to a superseded path.
9. Commit each manageable functional consolidation batch separately.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/consolidation-map.md`
- `agents/skills-rebuild/_audit/merge-decisions.csv`

The decision log must record cluster, source paths, canonical destination, decision, rationale, unique material preserved, resources moved, aliases retained, and retired paths.

## Reconciliation Requirements

- Reconcile every identified overlap cluster to one decision-log entry.
- Reconcile every merged source path to one canonical destination.
- Confirm unique retained material and bundled resources are accounted for.
- Confirm active routers and destination records contain no superseded paths.
- Confirm retained, merged, retired, aliased, and deferred counts reconcile with the cluster population.

## Repository Checkpoint

1. Begin only after Phase 05 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-06-consolidation` from the updated `main` branch.
3. Review the final diff and confirm it contains only approved overlap-cluster consolidations, decision artifacts, provenance updates, and directly required supporting changes.
4. Use focused intermediate commits for individual functional clusters when needed, then finish with the phase commit: `skills-rebuild: complete phase 06 consolidation`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize clusters reviewed, canonical owners selected, retired paths, artifact paths, reconciliation evidence, and deferred decisions.
7. Leave the pull request unmerged for review. Do not begin Phase 07 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- Both artifacts exist with complete cluster decisions.
- Every duplicate workflow has one canonical active owner.
- Unique retained material and provenance are traceable.
- Filesystem, routers, destination map, and consolidation records reconcile.
- The phase branch is pushed and its draft pull request is open for review.