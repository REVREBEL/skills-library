# Task 12: Pilot, Review, and Publish the Rebuilt Library

## Objective

Test representative end-to-end use cases, correct routing or execution failures, and publish the rebuilt library only after current validation evidence and repository review support the release.

## Preconditions

- The final `agents/skills-rebuild` filesystem and audit records exist.
- `validation-report.md`, `unresolved-items.md`, and `router-validation.md` reconcile with the filesystem.
- `.agents/skills` is the verified canonical task-workflow path.
- No unresolved item is marked as a blocking structural, compatibility, security, routing, provenance, or path-portability failure.
- Applicable rebuilt root and category routers are ready for pilot use.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-check/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-improver/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-manage/SKILL.md`
- `.agents/skills/github-operations/SKILL.md`

Use `skill-check` for retesting, `skill-improver` for approved defects found during pilots, `skill-manage` for final movement or synchronization, and the GitHub router for diff review, commits, pull requests, review feedback, merge, and remote verification. Use `skill-optimizer` only after the pilot produces real usage evidence and only for evidence-based performance or discovery optimization.

## Work

1. Confirm no blocking unresolved item remains.
2. Run representative pilot scenarios against the rebuilt routers and children, including:
   - Create a new skill
   - Find and review an existing skill
   - Publish a GitHub change
   - Debug a workflow failure
   - Analyze a dataset
   - Create or revise documentation
   - Perform a marketing or SEO task when retained
   - Route a hospitality-specific task when retained
3. Record the selected route, child skill, required tools, outcome, handoffs, and duplicated or missing steps using repository-relative paths.
4. Correct discovery descriptions, router boundaries, broken handoffs, and execution defects found during the pilot.
5. Rerun affected validation and pilot scenarios after every correction.
6. Reconcile the final inventory and destination records with the publishable filesystem.
7. Review the complete repository diff and exclude unrelated changes.
8. Scan all changed artifacts and PR text for user-specific absolute paths or other local environment details.
9. Normalize any local paths to repository-relative paths or approved neutral placeholders before commit.
10. Commit and push the final validated batches.
11. Open or update a reviewable pull request with truthful validation and unresolved-item status.
12. Address review feedback and merge only after current checks, approvals, and repository policy are satisfied.
13. Verify the target branch and published library after merge.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/pilot-report.md`
- `agents/skills-rebuild/_audit/publication-record.md`

The pilot report must record each scenario, expected route, actual route, result, defect, correction, retest result, and any accepted limitation. The publication record must include branch, commits, pull request, review state, validation evidence, unresolved-item status, merge result, target branch, and final target SHA.

All artifact paths must be repository-relative. Do not store contributor usernames, home-directory paths, workstation names, mount points, drive letters, or comparable machine-specific details.

## Reconciliation Requirements

- Reconcile every pilot scenario to the router path and active child used.
- Reconcile every pilot defect to a correction, accepted limitation, or unresolved item.
- Reconcile final inventory, destination, router, validation, and filesystem state before publication.
- Reconcile published commits and pull-request head to the reviewed diff.
- Reconcile the merge result and final target SHA through remote readback.
- Confirm final artifacts and PR text contain only repository-relative paths or approved neutral placeholders.

## Repository Checkpoint

1. Begin only after Phase 11 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-12-pilot-publish` from the updated `main` branch.
3. Use focused repair commits for pilot defects, then review the final cumulative diff against the approved rebuilt-library scope.
4. Finish with the phase commit: `skills-rebuild: complete phase 12 pilot and publication`.
5. Push the branch and open or update a draft pull request targeting `main`.
6. The pull request must summarize pilot scenarios, defects and retests, validation evidence, artifact paths, unresolved limitations, reconciliation status, and publication readiness without exposing local environment details.
7. Leave the pull request unmerged until review, checks, approvals, and repository policy are satisfied. Merge only when explicitly authorized.
8. After merge, verify the target branch and final SHA and record them in `publication-record.md`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- Both pilot and publication artifacts exist with complete evidence.
- All pilot scenarios pass or have explicitly accepted non-blocking limitations.
- Blocking validation issues are resolved.
- Audit records reconcile with the final filesystem.
- No committed artifact or PR text contains an unapproved user-specific absolute path.
- Changes are merged according to repository policy and the published target state is verified.