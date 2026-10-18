# Task 04: Remove Provider-Specific Assumptions

## Objective

Convert retained skills to provider-neutral, capability-based workflows unless a specific provider or application is intrinsic to the skill's purpose.

## Preconditions

- `agents/skills-rebuild/_audit/skills-inventory.csv` contains final compatibility classifications.
- `agents/skills-rebuild/_audit/application-compatibility-report.md` and `moved-to-not-needed.csv` reconcile with the filesystem.
- `.agents/skills` is the verified canonical task-workflow path.
- Skills selected for conversion are retained, approved for conversion, or manually approved after ambiguity review.

## Canonical Task Skills

Read and follow:

- `.agents/skills/SKILL.md`
- `.agents/skills/skills-create-manage-update/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-review/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-improver/SKILL.md`
- `.agents/skills/skills-create-manage-update/skill-writer/SKILL.md`

Use `skill-review` to decide whether conversion preserves the skill's job, `skill-improver` for targeted repairs, and `skill-writer` for substantial source-backed rewrites. Use `.agents/skills/github-operations/SKILL.md` for repository operations without duplicating authoring or review work.

## Work

1. Review each retained provider-specific skill.
2. Search for:
   - `.claude/`, `CLAUDE.md`, Claude hooks, and provider-specific environment variables
   - Proprietary slash commands or prompt wrappers
   - Hardcoded model identities or vendor-specific role instructions
   - Cursor, Gemini, Codex, or other client-specific paths and commands
   - Tool names unavailable in the approved environment
   - Undeclared connector, CLI, hook-system, or subagent assumptions
3. Decide whether each provider dependency is intrinsic, replaceable, or disqualifying.
4. Replace nonessential provider and client assumptions with capability-based language.
5. Replace unavailable tool references with supported tools or explicit compatibility requirements.
6. Remove obsolete paths, hooks, commands, and environment assumptions.
7. Preserve provider-specific instructions only when intrinsic to the skill and declared in `compatibility`.
8. Preserve the functional job, unique instructions, and source provenance.
9. Validate every converted file and relative reference.

## Artifacts

Create:

- `agents/skills-rebuild/_audit/provider-conversion-report.md`

Update:

- `agents/skills-rebuild/_audit/skills-inventory.csv` with conversion decision, status, and destination.

The conversion report must record source skill, original dependency, decision, changes made, retained compatibility requirements, validation performed, and unresolved blockers.

## Reconciliation Requirements

- Reconcile every reviewed skill to its inventory row and compatibility classification.
- Reconcile every converted skill to its resulting filesystem path.
- Confirm every retained provider dependency is intrinsic and explicitly declared.
- Confirm unconvertible cases are documented and not silently retained as compatible.

## Repository Checkpoint

1. Begin only after Phase 03 is approved and merged into `main`.
2. Create and complete this phase on `skills-rebuild/phase-04-provider-conversion` from the updated `main` branch.
3. Review the final diff and confirm it contains only approved provider conversions, inventory updates, the conversion report, and directly required supporting changes.
4. Commit the completed phase with: `skills-rebuild: complete phase 04 provider conversion`.
5. Push the branch and open a draft pull request targeting `main`.
6. The pull request must summarize converted skills, retained intrinsic dependencies, artifact paths, validation evidence, and unresolved blockers.
7. Leave the pull request unmerged for review. Do not begin Phase 05 until this phase is approved and merged into `main`.

## Completion Gate

Complete only when:

- All preconditions are satisfied.
- The conversion report and inventory updates exist.
- Every retained provider-specific skill has one documented decision.
- Converted skills contain no undeclared provider behavior or unavailable-tool assumptions.
- Filesystem, inventory, compatibility, and conversion records reconcile.
- The phase branch is pushed and its draft pull request is open for review.