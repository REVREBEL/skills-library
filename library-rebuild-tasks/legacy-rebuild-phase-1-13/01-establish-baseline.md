# Task 01: Establish the Skills Library Baseline

## Objective

Create a fixed, traceable baseline of the current skills library before any files are moved, rewritten, merged, split, or retired.

## Preconditions

- Repository identity and access are available.
- The logical paths `agents/skills`, `agents/not-needed`, `agents/skills-rebuild`, and `.agents/skills` are known but the physical source, quarantine, and rebuilt paths have not yet been assumed.
- No broad source-library movement or rewriting has started.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/github-operations/SKILL.md`

Use the GitHub router for repository inspection, branch creation, revision capture, commits, and remote verification. Keep baseline ownership in this task until its artifacts and reconciliation checks are complete.

## Work

1. Confirm the exact repository and current default branch.
2. Create or confirm a dedicated working branch.
3. Record the starting commit SHA.
4. Resolve the physical paths corresponding to:
   - Source library: `agents/skills`
   - Quarantine library: `agents/not-needed`
   - Rebuilt library: `agents/skills-rebuild`
   - Task workflow library: `.agents/skills`
5. Confirm `.agents/skills` is present at the project root and discoverable by the supported IDE or agent runtime.
6. Normalize every path written to committed artifacts as repository-relative from the project root.
7. Use absolute local paths only transiently for verification. Do not write usernames, home directories, workstation names, mount points, drive letters, or other machine-specific prefixes to the baseline or pull request.
8. Capture the complete source-library directory tree and count its skill folders.
9. Identify existing root and category routers.
10. Record protected files, excluded paths, and pre-existing work that must not be overwritten.
11. Exclude generated or operating-system metadata such as `__MACOSX`, `.DS_Store`, and `._*`.
12. Do not move or rewrite source skills during this task.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/baseline.md`

The artifact must record repository identity, default and working branches, starting SHA, repository-relative path mappings, the canonical `.agents/skills` task-workflow path, source-tree summary, source skill count, existing router locations, exclusions, protected work, and rollback reference.

Do not include contributor-specific absolute paths. When an absolute-path example is genuinely necessary, use a neutral placeholder such as `<repo-root>/...`.

## Reconciliation Requirements

- Verify every repository-relative path against the local filesystem without persisting the local absolute prefix.
- Verify `.agents/skills/SKILL.md` and its linked child routers resolve.
- Verify the source skill count against the captured directory tree.
- Verify the starting SHA and branch state through repository readback.
- Scan the baseline and pull-request text for user-specific absolute paths before commit.
- Confirm no source skill was moved, rewritten, or deleted during this task.

## Repository Checkpoint

1. Start from the current reviewed `main` branch.
2. Create and complete this phase on `skills-rebuild/phase-01-baseline`.
3. Review the final diff and confirm it contains only the baseline artifact and directly required supporting changes.
4. Confirm the diff and pull-request description contain only repository-relative paths or approved neutral placeholders.
5. Commit the completed phase with: `skills-rebuild: complete phase 01 baseline`.
6. Push the branch and open a draft pull request targeting `main`.
7. The pull request must summarize the artifact created, reconciliation performed, validation evidence, and unresolved items without exposing local environment details.
8. Leave the pull request unmerged for review. Do not begin Phase 02 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions have been resolved.
- `baseline.md` exists with every required field.
- Repository, branch, revision, path, tree, and count evidence reconcile.
- `.agents/skills` is verified as the canonical discoverable task-skill location.
- The baseline can identify the original location and rollback point for every source skill.
- No committed artifact or PR text contains an unapproved user-specific absolute path.
- The phase branch is pushed and its draft pull request is open for review.