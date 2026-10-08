---
name: "read-all-adrs"
description: "Read every ADR in a project before summarizing architectural context or decisions. Use when working with read all adrs."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
<!-- TODO(David): write the strong wording here -->

## When to Use

- Use when the user explicitly asks to load ADR context.
- Use when architectural decisions must be understood before changing or judging a project.

Read EVERY single ADR `.md` file in this project's `docs/adr/` folder, start to
finish.

Do not skim. Read each ADR completely before summarizing.

Read every single ADR file, for this project, in full.

## Limitations

- Adapted from `davidondrej/skills`; verify local paths, tools, credentials, and agent features before acting.
- For commands, remote access, scheduling, browser automation, or file-changing workflows, get explicit user approval and confirm the target environment first.
