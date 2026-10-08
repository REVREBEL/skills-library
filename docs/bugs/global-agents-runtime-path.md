> **Superseded architecture:** The individual-symlink runtime publication model in this report is superseded by [Runtime Publication Architecture: Physical Git Clones, Configured Targets, and Intake Capture](./runtime-git-clone-publication.md). Preserve this file as the historical record of the original runtime-path correction, but do not use its symlink-specific implementation or acceptance criteria for new work.

# Bug: Runtime Skills Path Targets Repo-Local `.agents/skills` Instead of Global `~/.agents/skills`

## Summary

Task 13 is merged and the canonical skills library is correct, but the runtime path is pointed at the wrong directory.

The current implementation defines:

```python
RUNTIME_DIR = os.path.join(REPO_ROOT, ".agents", "skills")
```

which resolves to:

```text
~/github-revrebel/skills-library/.agents/skills
```

On macOS, the actual Agent Skills runtime/discovery directory is:

```text
~/.agents/skills
```

As a result, `sync`, `status`, `validate`, external-install detection, and runtime reconciliation currently operate on a repo-local directory instead of the real user-level Agent Skills directory.

## Correct Architecture

The canonical files remain in the Git-backed repository:

```text
~/github-revrebel/skills-library/library/
```

The runtime/discovery layer belongs at:

```text
~/.agents/skills/
```

Each managed runtime entry should be an individual symbolic link directly to its canonical package in the repository:

```text
~/.agents/skills/actions-debugger
    -> ../../github-revrebel/skills-library/library/infrastructure-and-ops/ci-cd/actions-debugger
```

Conceptually:

```text
~/github-revrebel/skills-library/library/
        actual canonical skill packages
                    ↑
                    │ individual symlinks
                    │
~/.agents/skills/
        global runtime/discovery directory
```

There should not be a second managed runtime tree at:

```text
~/github-revrebel/skills-library/.agents/skills/
```

## Required Fix

### 1. Point the production runtime at the user-level Agent Skills directory

Change the production runtime default from the repository-local path to the user's home directory.

Preferred implementation:

```python
RUNTIME_DIR = str(Path.home() / ".agents" / "skills")
```

Do not hardcode a username or workstation-specific absolute path.

Existing functions that accept an injected `runtime_dir` for tests must continue to support isolated temporary directories.

### 2. Remove the repo-local generated runtime tree

Remove the tracked/generated:

```text
.agents/skills/
```

runtime tree from this repository.

The repository owns the canonical `library/`, intake tooling, manifests, audit records, docs, and tests. It should not contain a second generated runtime copy.

If appropriate, add the repo-local `.agents/` runtime path to `.gitignore` so it cannot be recreated accidentally.

Do not delete or move canonical skills from `library/`.

### 3. Build global runtime links correctly

Running:

```bash
python3 tools/skill-library.py sync
```

from the repository must reconcile:

```text
~/.agents/skills/
```

against `audit/runtime-manifest.json`.

The sync must:

- create missing managed links in `~/.agents/skills`
- use portable relative symlinks where possible
- point each managed link directly to its canonical package under this repository's `library/`
- create the global runtime directory if it does not exist
- preserve unmanaged/external entries rather than silently overwrite them
- continue detecting physical external installs and `EXTERNAL_UPDATE` candidates in the real global runtime directory
- continue handling broken managed links, collisions, and transactional rollback behavior

### 4. Keep tests isolated from the real home directory

Automated tests must never write to the real:

```text
~/.agents/skills
```

Tests must continue injecting temporary runtime directories under `tempfile.TemporaryDirectory()`.

Add an explicit regression test proving that the production default resolves to the user's home-level `.agents/skills`, while test fixtures remain fully isolated.

### 5. Update validation and status behavior

`status` and `validate` must inspect the real production runtime:

```text
~/.agents/skills
```

unless a runtime directory is explicitly injected for a test.

The existing four-way invariant remains:

```text
Physical Canonical Packages
==
Router-Indexed Packages
==
Manifest Packages
==
Global Runtime Symlink Targets
```

### 6. Update documentation

Update the operator documentation and Task 13 architecture references so they clearly distinguish:

```text
Repository:
~/github-revrebel/skills-library/library/

Global runtime:
~/.agents/skills/
```

Remove documentation that describes `<repo>/.agents/skills` as the production runtime.

## Migration / Rollout Behavior

The current user-level directory may already exist and may contain external entries.

The migration must be non-destructive.

For the current machine, `~/.agents/skills` exists but contains no managed skills yet. After the fix, running:

```bash
python3 tools/skill-library.py sync --dry-run
```

should report the managed links it intends to create in the global runtime.

Then:

```bash
python3 tools/skill-library.py sync
```

should materialize the global runtime links.

Do not rely on a single symlink from `~/.agents/skills` to a repo-local runtime directory. The desired model is individual runtime skill links pointing directly to canonical packages.

## Regression Coverage

Add tests covering at minimum:

1. Default production runtime resolves to `Path.home() / ".agents" / "skills"`.
2. Test runtime injection still uses isolated temporary directories and never touches the real home directory.
3. Empty global runtime is populated from the manifest.
4. Existing valid global managed symlinks remain unchanged.
5. A new physical skill appearing in the global runtime is classified and staged as external intake.
6. An existing managed global symlink replaced by a physical directory is classified as `EXTERNAL_UPDATE`.
7. Failed UPDATE rollback reconstructs the global runtime symlink to the prior canonical package.
8. Four-way validation uses global runtime targets.
9. Repo-local `.agents/skills` is no longer required or generated.

## Acceptance Criteria

This bug is resolved when all of the following are true:

- `RUNTIME_DIR` production default is `~/.agents/skills`.
- `library/` remains the single physical source of truth for approved skill packages.
- The repository no longer carries a generated `.agents/skills` runtime tree.
- `sync --dry-run` against an empty `~/.agents/skills` reports the expected managed links without modifying anything.
- `sync` creates the managed global runtime symlinks.
- Every managed global runtime link resolves into this repository's `library/`.
- External installs written by tools such as `skills.sh` into `~/.agents/skills` enter the existing intake/update pipeline.
- `status`, `validate`, and transactional rollback all operate against the correct global runtime.
- Automated tests remain isolated and do not mutate the user's actual home directory.
- Full test suite passes.
- Four-way living-library reconciliation passes after the global runtime is built.

## Out of Scope

Do not redesign the taxonomy, routers, manifest format, semantic intake logic, approval model, or transactional apply system. This is a runtime-path correction and migration only.
