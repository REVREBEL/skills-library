# Skills Create, Manage & Update Consolidation

## Purpose

This pass reduced overlapping discoverable workflows, clarified boundaries, removed broken or obsolete task skills, and added two missing workflows required by the larger skills-library rebuild.

## Active Architecture

### Discovery and Decisions

- `skill-inventory`: catalog every source skill before changes
- `skill-audit`: security, application compatibility, permissions, and provider coupling
- `skill-review`: library fit and primary disposition
- `skill-check`: final specification and package validation

### Creation and Authoring

- `skill-make-template`: simple, focused scaffold
- `skill-writer`: complex source-backed authoring
- `skill-creator`: evaluation-backed creation and packaging
- `skills-writing`: supporting architecture and testing pattern library
- `template-skill-enhanced`: worked multi-file structural example

### Improvement and Operations

- `skill-improver`: write repairs through a review-fix-verify loop
- `skill-optimizer`: read-only usage and static-quality diagnostics
- `skill-manage`: installed-skill lifecycle operations, including synchronization
- `skill-library-restructure`: repository-wide merge, split, conversion, categorization, and router work

## Retired From Active Discovery

| Source | Disposition | Reason | Canonical replacement |
|---|---|---|---|
| `skill-development` | Retired | Duplicated creation guidance and was centered on Claude Code plugins | `skill-make-template`, `skill-writer` |
| `skill-developer` | Retired | Depended on Claude hooks, `.claude` paths, and `skill-rules.json`; functionality was provider-specific and duplicated active creation guidance | `skill-make-template`, `skills-writing` |
| `skill-scanner` | Retired | Duplicated the security audit role and referenced bundled scripts and references that were not present | `skill-audit` |
| `skill-router` | Retired | Broad installed-library recommendation router duplicated the new parent router and referenced many unrelated or unsupported skills | Parent `SKILL.md` |
| `skill-update` | Merged | Narrow synchronization workflow belongs inside lifecycle management | `skill-manage` |

Retired content remains recoverable through Git history.

## Rewritten Skills

| Skill | Primary clarification |
|---|---|
| `skill-audit` | Answers whether a source is safe, compatible, and appropriately coupled |
| `skill-check` | Answers whether the finished package validates |
| `skill-review` | Assigns one evidence-based library disposition |
| `skill-make-template` | Owns straightforward creation from clear requirements |
| `skill-writer` | Owns complex source-backed authoring |
| `skill-creator` | Owns evaluation-backed creation, benchmarks, reports, and packaging |
| `skill-improver` | Owns write-based repair loops |
| `skill-manage` | Owns lifecycle, installation, movement, synchronization, and retirement |
| `skills-writing` | Became a reference pattern library instead of another competing creation workflow |
| `template-skill-enhanced` | Became a structural example instead of another primary creation workflow |

## New Skills

- `skill-inventory`: fills the required cataloging phase before audit and moves
- `skill-library-restructure`: owns functional categories, canonical merges, splits, conversions, and routers

## Boundary Tests

Use these questions to select the correct skill:

- **Do we know what exists?** → `skill-inventory`
- **Is the source safe and compatible?** → `skill-audit`
- **Does it belong and what should happen?** → `skill-review`
- **Does the final package validate?** → `skill-check`
- **Is this a simple new skill?** → `skill-make-template`
- **Does authoring require multiple sources or architecture decisions?** → `skill-writer`
- **Does it require benchmarks, graders, or packaging?** → `skill-creator`
- **Are we writing repairs?** → `skill-improver`
- **Are we diagnosing real usage without writing changes?** → `skill-optimizer`
- **Are we moving, syncing, or retiring installed skills?** → `skill-manage`
- **Are we rebuilding a whole library?** → `skill-library-restructure`

## Deferred Cleanup

The bundled `skill-creator/scripts/` directory contains filenames such as `package_skill copy.py` and `quick_validate copy.py`. These are not byte-for-byte duplicates of the similarly named scripts, so they were not deleted during this semantic consolidation. Their behavior should be compared and canonicalized in a dedicated script-quality pass.

## Validation Expectations

Before merge:

- Confirm every active child link in the parent router resolves
- Confirm retired `SKILL.md` files are absent from active discovery
- Search active skills for references to retired paths
- Confirm folder and frontmatter names match for rewritten and new skills
- Review the branch diff for unintended deletions
