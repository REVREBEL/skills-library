# Task 07: Split Oversized Skills

## Objective

Split retained skills only when they contain independently triggered jobs with different workflows, tools, outputs, risks, or validation paths.

## Preconditions

- Inventory, taxonomy, destination, consolidation, and merge-decision artifacts exist and reconcile.
- `.agents/skills` is the verified canonical task-workflow path.
- Canonical owners for overlap clusters are established.
- Candidate skills have been reviewed for true multi-job behavior rather than length alone.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-library-restructure/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-writer/SKILL.md`

Use `skill-review` for split approval, `skill-library-restructure` for parent-child architecture and destination updates, and `skill-writer` for substantial source-backed child or router authoring. Use `.agents/skills/github-operations/SKILL.md` for repository operations and reviewable publication batches.

## Work

1. Identify retained skills with multiple independent jobs.
2. Distinguish true multi-job skills from singular jobs with extensive supporting material.
3. Approve a split only when sections have independent:
   - Trigger phrases or user goals
   - Required inputs
   - Tools, applications, or permissions
   - Execution sequences
   - Risk or authorization requirements
   - Outputs and completion evidence
4. Define each child skill's trigger, scope, output, tools, and completion evidence.
5. Create a parent router only when several focused children share a coherent category and require routing.
6. Move shared category policy to the parent without duplicating child execution workflows.
7. Move long supporting detail into `references/` when the functional job remains singular.
8. Update destination and provenance mappings for every resulting child.
9. Verify parent links, child links, and retired source paths.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/split-map.md`

The map must record original path, split decision, rationale, parent destination, child destinations, content allocation, shared resources, routing boundaries, retired source path, and validation status.

## Reconciliation Requirements

- Reconcile every approved or rejected split candidate to the split map.
- Account for every source section and bundled resource in a child, parent, reference, canonical destination, or documented retirement.
- Reconcile all new child paths with the destination map and inventory provenance.
- Confirm parent routers link only to existing children and contain no duplicated end-to-end child workflow.

## Repository Checkpoint

1. Begin only after Phase 06 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-07-splits` from the updated `main` branch.
3. Review the final diff and confirm it contains only approved splits, router or child files created by those splits, mapping updates, and directly required supporting changes.
4. Use focused intermediate commits for large split candidates when needed, then finish with the phase commit: `skills-rebuild: complete phase 07 skill splits`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize candidates reviewed, approved and rejected splits, resulting paths, artifact locations, reconciliation evidence, and unresolved cases.
7. Leave the pull request unmerged for review. Do not begin Phase 08 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- The split map exists and accounts for every reviewed candidate.
- Every approved child has a distinct trigger, job, and outcome.
- Parent, child, reference, destination, and provenance records reconcile.
- No content or resource disappears without a documented disposition.
- The phase branch is pushed and its draft pull request is open for review.