---
name: skill-inventory
description: 'Catalog every Agent Skill in a folder or repository before audit or reorganization. Use when building a complete inventory of skill paths, names, descriptions, applications, model dependencies, bundled files, size, references, and current status without moving or rewriting skills.'
compatibility: 'Read-only. Requires filesystem or repository read access to the target library.'
metadata:
  category: agent-skills
  type: inventory
  source: custom
---

# Skill Inventory

Create a complete, deduplicated source inventory before compatibility decisions, moves, merges, splits, or rewrites.

## When to Use

Use this skill when:

- Beginning a large skills-library audit
- Cataloging all `SKILL.md` files in a repository
- Establishing traceability before moving skills to quarantine
- Identifying application-specific and model-specific dependencies
- Measuring skill size and bundled-resource complexity
- Preparing inputs for security audit, review, or restructuring

Do not modify source skills during this workflow.

## Required Inputs

Resolve:

- Source folder or repository
- Scope exclusions such as archives, build outputs, or quarantine folders
- Desired output location and format
- Approved application-stack reference, when available
- Whether nested parent and child skills should be represented separately

## Workflow

### 1. Establish Scope

Record:

- Root path
- Included folders
- Excluded folders
- Active branch or revision
- Inventory timestamp or commit

Exclude generated dependencies, caches, packaged archives, and known output folders unless the user asks to include them.

### 2. Discover Skills

Find every `SKILL.md` under the scope. For each result, identify the skill root and bundled files.

Do not infer one skill per top-level folder when nested child skills exist.

### 3. Read Metadata and Structure

Capture:

- Source path
- Folder name
- Frontmatter name
- Description
- Compatibility and tool fields
- Source and license metadata
- Line and word counts
- Supporting directories
- Referenced relative files
- Parent or child relationships

Flag malformed frontmatter without repairing it.

### 4. Identify Dependencies

Record:

- Applications and frameworks
- CLIs and runtimes
- Model/provider references
- MCP servers and external services
- Hardcoded filesystem paths
- External URLs
- Other skills referenced
- Scripts or package dependencies

Separate primary dependencies from examples and incidental mentions.

### 5. Identify Structural Signals

Record signals for later review:

- Missing or broken references
- Folder/name mismatch
- Overlong main file
- Multiple apparent workflows
- Duplicate or near-duplicate descriptions
- Provider-specific paths or hooks
- Unsupported application dependencies
- Orphaned bundled files

Do not assign final dispositions during inventory unless specifically requested.

### 6. Deduplicate Records

Every source skill must appear exactly once using its source path as the stable key.

If names repeat, preserve separate rows and flag the collision.

### 7. Produce the Inventory

Recommended CSV columns:

```text
source_path
folder_name
frontmatter_name
description
primary_function
application_dependencies
model_dependencies
referenced_skills
bundled_resources
line_count
word_count
frontmatter_valid
broken_references
potential_overlap
notes
```

Also produce a short Markdown summary with counts and high-signal anomalies.

## Output Requirements

Report:

- Total skills discovered
- Duplicate names
- Invalid frontmatter
- Broken references
- Application-specific skills
- Model-specific skills
- Large or multi-workflow candidates
- Potential overlap clusters
- Excluded paths

## Completion Checks

- Every in-scope `SKILL.md` appears exactly once
- Nested skills were not collapsed accidentally
- Source revision and exclusions are documented
- Primary and incidental dependencies are distinguished
- No source files were modified
- Inventory rows reconcile with discovered paths
- Output is ready for audit and disposition work
