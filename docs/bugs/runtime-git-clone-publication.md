# Runtime Publication Architecture: Physical Git Clones, Configured Targets, and Intake Capture

## Status

This report supersedes the symlink publication model described in `docs/bugs/global-agents-runtime-path.md`.

The canonical library remains authoritative under:

```text
~/github-revrebel/skills-library/library/
```

Runtime skill directories must be physical Git working trees, not collections of per-skill symlinks.

## Objective

Replace the current individual-symlink runtime publication model with one Git-backed publication model that can serve:

- the global universal-agent runtime at `~/.agents/skills/`
- Antigravity global discovery at `~/.gemini/config/skills/`
- project/workspace `.agents/skills/` directories
- any future agent or project skill directory defined in configuration

The same publication system must support either the complete runtime library or selected category, subcategory, package, or individual-skill scopes per target.

## Required Architecture

### Canonical source

```text
skills-library/main
└── library/
    ├── business-and-operations/
    ├── content-and-documentation/
    ├── data-and-ai/
    ├── design-and-experience/
    ├── development/
    ├── infrastructure-and-ops/
    ├── marketing-and-seo/
    ├── meta-and-agent-skills/
    ├── quality-and-security/
    ├── workflow-and-automation/
    ├── github-operations/
    ├── skills-create-manage-update/
    └── SKILL.md
```

Only `library/` is canonical. Runtime directories are deployable working copies.

### Published runtime branch

Create and maintain a generated branch named `runtime` whose repository root mirrors the contents of `main:library/`.

Conceptually:

```text
main
└── library/
    ├── development/
    ├── design-and-experience/
    └── ...

runtime
├── development/
├── design-and-experience/
└── ...
```

The `runtime` branch is generated deployment state. Canonical edits must not be authored there.

### Runtime targets

Runtime targets are normal Git clones/checkouts of the `runtime` branch so scanners see real physical directories and files.

Examples:

```text
~/.agents/skills/
~/.gemini/config/skills/
<project>/.agents/skills/
```

Do not use individual skill symlinks, directory symlinks, bind mounts, or Git submodules as the normal publication mechanism.

## Runtime Target Configuration

Add one repository-managed configuration file, preferably:

```text
config/runtime-targets.json
```

Use a dependency-free format readable by the existing Python tooling.

The configuration must define:

- target name
- destination path
- runtime branch
- whether the target receives the complete runtime tree or a selected subset
- included category/subcategory/package/skill paths for subset targets
- whether incoming external changes are accepted from that target
- whether the target is enabled

Example shape:

```json
{
  "repository": "REVREBEL/skills-library",
  "runtime_branch": "runtime",
  "targets": [
    {
      "name": "universal-global",
      "path": "~/.agents/skills",
      "mode": "full",
      "accept_external_intake": true,
      "enabled": true
    },
    {
      "name": "antigravity-global",
      "path": "~/.gemini/config/skills",
      "mode": "subset",
      "include": [
        "design-and-experience/design-systems",
        "github-operations"
      ],
      "accept_external_intake": false,
      "enabled": true
    }
  ]
}
```

The exact schema may be refined during implementation, but target behavior must remain declarative and repository-managed.

## Full and Partial Clones

### Full target

A full target checks out the complete `runtime` branch.

Example:

```text
~/.agents/skills/
├── development/
├── design-and-experience/
├── marketing-and-seo/
└── ...
```

### Subset target

Use Git sparse-checkout for targets that should receive only selected capability branches.

For example, a target configured with:

```text
design-and-experience/design-systems
github-operations
development/frontend
```

must materialize only those selected paths from the `runtime` branch.

Use Git's native sparse-checkout mechanism rather than copying or symlinking selected directories.

The publisher must be able to:

1. clone the `runtime` branch when a target does not exist
2. initialize or update sparse-checkout rules for subset targets
3. disable sparse-checkout for full targets
4. pull/update with fast-forward-only semantics
5. verify that the resulting physical tree matches the configured scope

## Sync Command

Refactor `python3 tools/skill-library.py sync` from symlink reconciliation into runtime checkout reconciliation.

For each enabled target:

1. resolve `~` and environment-safe paths
2. detect whether the destination is absent, a valid managed checkout, a dirty checkout, or an unmanaged/conflicting directory
3. never overwrite a dirty or unmanaged target before intake capture
4. create the Git clone if absent
5. verify the expected repository remote and `runtime` branch
6. apply configured sparse-checkout scope
7. fetch and fast-forward to the current published runtime commit
8. validate physical skill coverage for that target

The command must remain idempotent.

## Dirty Runtime Intake

A runtime checkout can become dirty when an external installer such as `skills.sh` creates or modifies physical skill packages.

Examples:

```text
?? new-skill/
 M existing-skill/SKILL.md
```

A dirty runtime is incoming source material. It must never be silently reset, deleted, or overwritten.

### Local responsibility

GitHub Actions cannot inspect uncommitted files on a user's workstation. Therefore a local intake collector must perform the first step.

The local collector must:

1. inspect configured targets with `git status --porcelain`
2. group changes by top-level incoming skill/package
3. capture new, modified, deleted, and renamed files
4. optionally cross-check `~/.agents/.skill-lock.json` for `skills.sh` source/provenance metadata
5. create a uniquely named `incoming/<timestamp-or-id>` snapshot branch or equivalent transport commit
6. commit only the captured incoming changes
7. push that snapshot to GitHub
8. confirm the push succeeded before any local cleanup/reset occurs

The runtime target must retain the dirty content if capture or push fails.

### GitHub responsibility

A GitHub workflow triggered by an `incoming/**` snapshot must:

1. inspect the incoming diff against the published `runtime` baseline
2. create a new intake branch based on current `main`, not on the runtime branch
3. copy the incoming package(s) and provenance into the repository's `intake/` area
4. preserve enough metadata to identify the source runtime target and original runtime path
5. run existing intake compatibility, validation, duplicate, and safety checks
6. open an intake PR against `main`
7. never auto-promote an incoming package directly into `library/`
8. leave semantic reconciliation, consolidation, routing, normalization, and canonical placement to the existing reviewed intake process

After successful capture, the local runtime checkout may be restored to `origin/runtime`.

## Canonical Reconciliation Flow

The complete lifecycle is:

```text
skills.sh / external installer
        ↓
physical change in a configured runtime clone
        ↓
local dirty detector
        ↓
incoming/* snapshot pushed to GitHub
        ↓
GitHub workflow
        ↓
main-based intake/* branch
        ↓
intake/ package + provenance
        ↓
review / duplicate detection / consolidation / classification
        ↓
PR to main
        ↓
merge
        ↓
regenerate runtime branch from main:library/
        ↓
configured runtime targets pull/update
```

This flow must specifically prevent normalization from masking duplicates such as `design-md` / `design-md_v1`. Semantic duplicate/reconciliation checks must occur before a new canonical name is invented solely to avoid a folder-name collision.

## Runtime Publication Workflow

Add a GitHub workflow that regenerates the `runtime` branch after approved changes to `main:library/**`.

Requirements:

- runtime root equals the contents of `library/`
- no `audit/`, `docs/`, `tools/`, tests, intake staging, or repository-only files are published into runtime
- publication is deterministic
- unchanged canonical state produces unchanged runtime content
- publication failure must not corrupt the previous usable runtime branch
- runtime branch is generated output and must not be used as the canonical editing surface

## Validation Changes

Retire symlink-specific assertions.

Remove or replace validation for:

- symlink target resolution
- broken managed symlinks
- relative-link portability
- runtime alias names created solely for flat symlink collisions

Validate instead:

- canonical package set
- router-indexed package set
- runtime publication package set
- configured target scope
- checkout repository and branch identity
- sparse-checkout rules where applicable
- clean/dirty runtime state
- incoming changes captured before destructive reconciliation
- physical `SKILL.md` presence in published targets
- full target equality with canonical runtime publication
- subset target equality with its configured include scope

## Migration

The implementation must migrate the current `~/.agents/skills` symlink runtime non-destructively.

Before deleting any current link or directory:

1. scan for physical/unmanaged content
2. stage or capture anything not represented by canonical `library/`
3. verify capture
4. remove the old managed symlink publication layer
5. clone the generated `runtime` branch into the configured target
6. validate the physical checkout

Apply the same process to any other configured target.

## Tests

Add regression coverage for at least:

1. runtime branch generation mirrors `library/`
2. a full target is cloned as physical files
3. a subset target uses sparse-checkout and receives only configured scopes
4. sync is idempotent
5. sync refuses destructive update of a dirty target
6. untracked external skill is detected
7. modified tracked skill is detected
8. incoming capture preserves data if push fails
9. successful incoming capture can be converted into a main-based intake branch
10. runtime reset occurs only after successful capture
11. duplicate candidates are not made unique merely by adding suffixes such as `_1`, `_v1`, or `_2`
12. no runtime symlink publication is generated
13. configured target validation catches wrong remote, wrong branch, or wrong sparse scope
14. tests use isolated temporary Git repositories and never mutate the user's actual home directories

## Acceptance Criteria

This architecture is complete when:

- `library/` remains the single canonical source of approved skills
- a generated `runtime` branch exposes only the canonical library tree at branch root
- `~/.agents/skills` is a physical Git checkout, not a symlink farm
- `~/.gemini/config/skills` can be a physical Git checkout for Antigravity
- additional project/agent targets can be declared in configuration
- full and sparse/subset targets are supported
- target setup and updates are performed by one sync/publish command
- external physical installs are detected as dirty Git state
- dirty state is captured before any reset/update
- GitHub automation converts incoming snapshots into reviewed `intake/` branches based on `main`
- runtime publication is regenerated only from approved canonical `library/`
- symlink creation/reconciliation code and tests are removed
- all runtime and intake tests pass

## Explicit Non-Goals

Do not:

- copy the canonical library independently by hand into each target
- maintain separate publication implementations for Codex, Gemini, Claude, and Antigravity
- use symlinks as the primary runtime publication mechanism
- use Git submodules when normal clones/checkouts are sufficient
- allow GitHub automation to assume it can see uncommitted workstation state
- auto-merge incoming external skills directly into the canonical library
