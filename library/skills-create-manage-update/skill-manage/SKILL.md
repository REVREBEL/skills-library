---
name: skill-manage
description: 'Manage the lifecycle and filesystem placement of Agent Skills across supported project and global locations. Use when listing, locating, enabling, disabling, copying, moving, installing, synchronizing, backing up, or retiring skills for Agents, Cursor, Claude, GitHub Copilot, or Codex.'
compatibility: 'Requires filesystem access. Network synchronization requires access to the upstream source. Destructive operations require explicit confirmation.'
metadata:
  category: agent-skills
  type: lifecycle-management
  source: consolidated
---

# Skill Manage

Manage existing skills safely without conflating lifecycle operations with skill authoring.

## When to Use

Use this skill when the user wants to:

- Locate or list installed skills
- Determine global versus project scope
- Enable or disable a skill
- Copy or move a skill between supported environments
- Back up local customizations
- Synchronize an installed skill with its source
- Retire or remove a skill
- Verify installation paths and duplicates

Use `../skill-make-template/SKILL.md` to create new skill content.
Use `../skill-improver/SKILL.md` to repair skill instructions.

## Supported Locations

Discover actual paths instead of assuming every environment is installed.

Common directory-based locations:

| Environment | Global | Project |
|---|---|---|
| Agent Skills | `~/.agents/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| Cursor | `~/.cursor/skills/<name>/SKILL.md` | `.cursor/skills/<name>/SKILL.md` |
| Claude | `~/.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| Codex | `~/.codex/skills/<name>/SKILL.md` | `.codex/skills/<name>/SKILL.md` |

GitHub Copilot may use repository instructions, custom agents, or environment-specific skill locations. Inspect the current configuration before writing.

Do not edit tool-managed caches directly.

## Safety Rules

- Inventory before changing files
- Prefer reversible operations
- Back up local modifications before synchronization
- Use dry-run behavior when the available manager supports it
- Confirm before deletion, overwrite, or bulk updates
- Never replace a complete single-file configuration without preserving unrelated content
- Re-read the destination after copy or move
- Do not assume equivalent file formats between tools

## Workflow

### 1. Discover the Environment

Determine:

- Installed agent environments
- Global and project skill paths
- Repository root
- Active skill sources
- Duplicate names across locations
- Disabled or archived skills

### 2. Inventory the Target

Record:

- Name and path
- Scope: global or project
- Source or provenance
- Modification status
- Dependencies and reverse dependencies
- Destination and collision risks

### 3. Choose the Operation

#### List or Search

Use bounded filesystem discovery and content search. Report exact paths and scope.

#### Enable or Disable

Use the environment's supported mechanism. Prefer reversible renaming or configuration toggles over deletion.

#### Copy

Verify source and destination formats. Adapt only when required, and validate the copied result.

#### Move

Copy, verify, then remove the source. Preserve unrelated files and avoid overwriting collisions.

#### Synchronize or Update

1. Identify the upstream source and current version
2. Compare local changes
3. Back up local customizations
4. Preview changes when possible
5. Update one skill at a time
6. Re-run validation

Do not bulk-update a production library without reviewing the proposed changes.

#### Retire or Delete

1. Check dependencies and router links
2. Confirm the requested target
3. Preserve provenance in an inventory or changelog
4. Move to quarantine when future review is possible
5. Delete only with explicit confirmation

### 4. Verify

After any write operation, confirm:

- Destination exists
- Expected files are present
- Folder and frontmatter names match
- Relative links resolve
- Routers reference the correct path
- Source removal occurred only when intended
- No unrelated configuration was changed

## Output Format

```markdown
## Skill Lifecycle Operation

### Operation
List | Enable | Disable | Copy | Move | Sync | Retire | Delete

### Source
- Path:
- Scope:
- Provenance:

### Destination
- Path:
- Scope:

### Changes
1. ...

### Verification
- ...

### Backups or Recovery
- ...
```

## Completion Checks

- Environment and paths were discovered
- Target and scope were explicit
- Collision and dependency risks were checked
- Destructive actions received confirmation
- Local customizations were protected
- Destination was read back and validated
- Router or inventory references were updated when necessary
