# Repository Rename Cleanup

## Objective

Complete the repository rename from:

```text
REVREBEL/skills-rebuild
```

to:

```text
REVREBEL/skills-library
```

and the local repository path from:

```text
~/github-revrebel/skills-rebuild
```

to:

```text
~/github-revrebel/skills-library
```

This is a **rename cleanup only**. Do not reorganize the skill library, change taxonomy, migrate the production skill tree, or begin the future intake/symlink system as part of this task.

## Important Path Rule

Do **not** automatically rename historical internal paths such as:

```text
task-folder/agents/skills-rebuild/
```

Those paths are part of the completed rebuild artifacts and audit history.

Only change them if a specific reference is actually intended to refer to the GitHub repository name or former local repository root rather than the historical rebuild workspace.

## 1. Verify Current Repository State

From:

```bash
cd ~/github-revrebel/skills-library
```

verify:

```bash
git status
git remote -v
git branch --show-current
git fetch origin
```

Expected GitHub remote:

```text
https://github.com/REVREBEL/skills-library.git
```

Confirm `main` is current before making cleanup changes.

## 2. Search for Stale Repository References

Search the repository for references to:

```text
REVREBEL/skills-rebuild
github.com/REVREBEL/skills-rebuild
~/github-revrebel/skills-rebuild
/github-revrebel/skills-rebuild
```

Also search for any absolute local paths containing the former repository root.

Classify every match as either:

### UPDATE
References that mean the GitHub repository or local repository itself.

Examples:

```text
https://github.com/REVREBEL/skills-rebuild
git clone ...
repository metadata
documentation telling users where the repo lives
local setup instructions
scripts that calculate paths using the old repository root
```

Change these to:

```text
REVREBEL/skills-library
https://github.com/REVREBEL/skills-library
~/github-revrebel/skills-library
```

### PRESERVE
Historical internal rebuild paths such as:

```text
task-folder/agents/skills-rebuild/
```

Do not change these merely because they contain the string `skills-rebuild`.

## 3. Check GitHub References

Specifically inspect:

- README files
- repository documentation
- scripts
- shell commands
- Python constants
- generated reports
- PR templates
- GitHub workflow files
- package/config files
- audit generators

Replace stale GitHub repository URLs where appropriate.

Do not rewrite historical PR evidence simply to cosmetically change old repository URLs if those URLs accurately identify the repository name at the time the evidence was created.

## 4. Check Local Path Assumptions

Search executable code for assumptions that the repository directory itself is named:

```text
skills-rebuild
```

Any executable tooling should preferably determine the repository root relative to its own file or via Git rather than depending on:

```text
~/github-revrebel/skills-rebuild
```

Remove stale absolute-path dependencies if any exist.

Do not alter legitimate internal paths under:

```text
task-folder/agents/skills-rebuild/
```

## 5. Validate

After corrections:

```bash
git diff
git status
```

Then verify:

```bash
git remote -v
```

and search again for the old external repository reference:

```text
REVREBEL/skills-rebuild
```

Any remaining matches must be explicitly classified as historical/intentional.

Also search for the old local repository root:

```text
github-revrebel/skills-rebuild
```

There should be zero active/runtime dependencies on it.

## 6. Regression Check

Run the relevant existing validation that can execute from the renamed repository directory.

The purpose is to prove that changing the outer repository folder name did not break scripts that relied on repository-relative path calculation.

Do not modify historical validator expectations solely because the outer Git repository was renamed.

## 7. Commit and PR

Create a focused branch such as:

```text
maintenance/repository-rename-cleanup
```

The diff should contain only files genuinely affected by the repository rename.

Commit:

```text
chore: update repository references for skills-library rename
```

Push and open a PR against `main`.

## Completion Criteria

The task is complete when:

- GitHub repository is `REVREBEL/skills-library`
- local repository is `~/github-revrebel/skills-library`
- `origin` points to the renamed GitHub repository
- no active code depends on the old local repository path
- stale external `REVREBEL/skills-rebuild` references are corrected
- historical `task-folder/agents/skills-rebuild/` paths remain intact unless independently justified
- validation still passes from the renamed local repository
- the cleanup is captured in one focused PR

Return a short report listing:

- files changed
- stale references corrected
- intentional historical references preserved
- validation result
- PR URL
- any remaining issue