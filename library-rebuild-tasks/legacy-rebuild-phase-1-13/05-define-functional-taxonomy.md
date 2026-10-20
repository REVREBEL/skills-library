# Task 05: Define the Functional Taxonomy

## Objective

Design the destination category structure for retained skills based on the jobs they perform, without moving or rewriting the full library during this task.

## Preconditions

- Baseline, inventory, compatibility, and provider-conversion artifacts exist and reconcile.
- `.agents/skills` is the verified canonical task-workflow path.
- Quarantined and retired skills are distinguishable from retained skills.
- Every retained skill has a current source path and compatibility status.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-library-restructure/SKILL.md`

Use `skill-review` for placement decisions and `skill-library-restructure` for category design and destination mapping. Use `.agents/skills/github-operations/SKILL.md` only for repository operations required to record and publish the taxonomy work.

## Work

1. Review retained capabilities and recorded overlap clusters.
2. Propose a small set of functional top-level categories.
3. Define each category's purpose, inclusion criteria, and exclusion boundaries.
4. Group skills by functional outcome and trigger, not source repository, model vendor, programming language, or application name alone.
5. Assign every retained source skill one proposed functional destination.
6. Identify root-level meta-skills and routers.
7. Flag ambiguous destinations for review rather than forcing placement.
8. Revise category names that create overlapping routing.
9. Keep the hierarchy shallow and create a category only when its purpose and children justify routing.
10. Do not perform broad moves, merges, splits, or rewrites during this task.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/functional-taxonomy.md`
- `agents/skills-rebuild/_audit/destination-map.csv`

The destination map must record source path, compatibility status, proposed category, proposed final path, routing role, and unresolved placement concerns.

## Reconciliation Requirements

- Reconcile every retained inventory row to exactly one destination-map row.
- Confirm quarantined and retired sources do not appear as active destinations.
- Confirm category totals equal the retained skill population.
- Confirm each category definition matches its assigned children and does not overlap another category without an explicit boundary.

## Repository Checkpoint

1. Begin only after Phase 04 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-05-taxonomy` from the updated `main` branch.
3. Review the final diff and confirm it contains only taxonomy artifacts, destination mapping, and directly required supporting changes.
4. Commit the completed phase with: `skills-rebuild: complete phase 05 functional taxonomy`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize category decisions, destination coverage, artifact paths, reconciliation totals, and unresolved placements.
7. Leave the pull request unmerged for review. Do not begin Phase 06 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- Both artifacts exist with the required contents.
- Every retained skill has exactly one proposed functional home.
- Every category has explicit inclusion and exclusion boundaries.
- Counts reconcile and every unresolved placement is documented.
- The phase branch is pushed and its draft pull request is open for review.