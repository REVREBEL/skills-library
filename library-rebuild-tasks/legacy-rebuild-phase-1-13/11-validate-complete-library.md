# Task 11: Validate the Complete Library

## Objective

Validate the rebuilt skills library structurally, semantically, and operationally before pilot use or publication.

## Preconditions

- The rebuilt filesystem and all expected audit artifacts under `agents/skills-rebuild/_audit/` exist.
- `.agents/skills` is the verified canonical task-workflow path.
- Canonical skills, resources, and router hierarchy are complete enough for whole-library validation.
- The repository-provided skill validator and other safe validation tools have been identified or recorded as unavailable.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-check/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-audit/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`

Use `skill-check` for structural, semantic, link, and package validation; `skill-audit` for safety, compatibility, permissions, dependencies, and secrets; and `skill-review` for final disposition inconsistencies or unresolved ownership decisions. Use `.agents/skills/github-operations/SKILL.md` for repository diff, commit, CI, and publication-state validation.

## Work

1. Run the repository-provided skill validator when available.
2. Independently validate:
   - Every source skill has one documented final disposition
   - Active folder names match frontmatter `name`
   - YAML frontmatter parses and required fields are valid
   - Active skill names are unique
   - Descriptions explain capability and trigger conditions
   - Relative links and bundled-resource references resolve
   - Parent routers cover all active direct children
   - Overlapping triggers are distinguishable
   - Provider and application requirements are declared and supported
   - Unsupported skills remain traceably quarantined or retired
   - Write and destructive workflows contain authorization and verification gates
   - Scripts validate inputs and contain no secrets or unsafe hardcoded assumptions
   - Examples are syntactically valid for their stated environment
   - Committed artifacts, reports, inventories, examples, and documentation contain no unapproved user-specific absolute paths
3. Scan for path forms such as `/Users/`, `/home/`, Windows drive prefixes, UNC paths, local mount points, workstation names, and contributor-specific usernames.
4. Distinguish valid repository-relative paths and neutral placeholders such as `<repo-root>/...` from leaked local environment paths.
5. Test parent-to-child routing with representative prompts.
6. Validate bundled scripts and examples using available safe tooling.
7. Compare every source inventory row with its final disposition and filesystem destination.
8. Separate passed, failed, skipped, unavailable, and manually reviewed checks.
9. Create a repair item for every failure or unresolved validation gap.
10. Do not report a check as passed when it could not be executed.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/validation-report.md`
- `agents/skills-rebuild/_audit/unresolved-items.md`

The validation report must record each check, scope, method, status, evidence, affected repository-relative paths, and repair outcome. The unresolved-items file must record exact scope, impact, owner or next workflow, and blocking status.

## Reconciliation Requirements

- Reconcile the final filesystem against baseline, inventory, compatibility, destination, consolidation, split, batch, resource-cleanup, and router-validation records.
- Reconcile every active, quarantined, retired, merged, and split source to one final disposition.
- Confirm validation totals cover the full active skill and resource population.
- Confirm every failure appears in the repair history or unresolved-items file.
- Confirm every committed path is repository-relative or an approved neutral placeholder.
- Confirm no skipped or unavailable check is represented as passed.

## Repository Checkpoint

1. Begin only after Phase 10 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-11-validation` from the updated `main` branch.
3. Review the final diff and confirm it contains only validation artifacts, approved repairs required to pass validation, and directly required reconciliation updates.
4. Use focused repair commits when needed, then finish with the phase commit: `skills-rebuild: complete phase 11 validation`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize checks run, pass/fail/skip counts, repairs made, artifact paths, reconciliation status, unavailable checks, and unresolved items with blocking status.
7. Confirm the PR body and changed files contain no unapproved user-specific absolute paths before requesting review.
8. Leave the pull request unmerged for review. Do not begin Phase 12 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied or explicitly recorded as unavailable.
- Both validation artifacts exist with complete check coverage.
- Every validation failure is repaired or recorded with exact scope and impact.
- All audit records reconcile with the final filesystem.
- No unapproved contributor-specific absolute path remains in committed content.
- No silent source, skill, resource, router, or validation coverage gap remains.
- The phase branch is pushed and its draft pull request is open for review.