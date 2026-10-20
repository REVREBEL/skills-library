# Task 03: Apply the Application Compatibility Gate

## Objective

Determine which source skills meet the approved application and environment requirements before investing in consolidation or rewriting.

## Preconditions

- `agents/skills-rebuild/_audit/baseline.md` exists and paths are verified.
- `agents/skills-rebuild/_audit/skills-inventory.csv` and `inventory-summary.md` have complete reconciled coverage.
- `.agents/skills` is the verified canonical task-workflow path.
- The approved application list and target-agent capabilities are available.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-audit/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-manage/SKILL.md`

Use `skill-audit` for application, environment, permission, and dependency evidence; `skill-review` for the disposition decision; and `skill-manage` for approved traceable movement. Use `.agents/skills/github-operations/SKILL.md` for branch, diff, commit, and remote verification without duplicating the compatibility workflow.

## Work

1. Review every inventory row against the approved application and environment requirements.
2. Assign one compatibility classification:
   - Approved and supported
   - Supported after conversion
   - Optional dependency with a supported replacement
   - Unsupported application or platform
   - Unsupported tool or permission dependency
   - Provider-specific but potentially reusable
   - Unrelated to the target library
   - Ambiguous and requiring manual review
3. Record evidence for every classification.
4. Separate intrinsic unsupported dependencies from replaceable implementation details.
5. Mark ambiguous skills for individual review instead of guessing.
6. Move only clearly unsupported or unrelated skills to the resolved `agents/not-needed` path.
7. Preserve source-relative paths or another unambiguous provenance key.
8. Do not delete source skills.
9. Commit the compatibility and quarantine pass separately from later rewrites.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/application-compatibility-report.md`
- `agents/skills-rebuild/_audit/moved-to-not-needed.csv`

Update:

- `agents/skills-rebuild/_audit/skills-inventory.csv` with final compatibility classification and current destination.

## Reconciliation Requirements

- Reconcile every classification to one inventory row.
- Reconcile every moved skill to the quarantine manifest and physical destination.
- Confirm retained, moved, and unresolved counts equal the inventoried source count.
- Confirm no source skill was silently deleted or omitted.

## Repository Checkpoint

1. Begin only after Phase 02 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-03-compatibility` from the updated `main` branch.
3. Review the final diff and confirm it contains only compatibility records, approved quarantine moves, inventory updates, and directly required supporting changes.
4. Commit the completed phase with: `skills-rebuild: complete phase 03 compatibility gate`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize classifications, moved-skill counts, artifact paths, reconciliation totals, validation evidence, and unresolved manual reviews.
7. Leave the pull request unmerged for review. Do not begin Phase 04 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- Required artifacts and inventory updates exist.
- Every inventoried skill has one evidence-backed compatibility classification.
- Every moved skill reconciles with the quarantine manifest and filesystem.
- The full source population is accounted for with no silent omissions.
- The phase branch is pushed and its draft pull request is open for review.