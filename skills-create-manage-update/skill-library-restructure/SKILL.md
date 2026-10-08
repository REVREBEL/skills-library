---
name: skill-library-restructure
description: 'Reorganize a reviewed Agent Skills library into clear functional categories with parent routers and focused child skills. Use after inventory and disposition decisions to merge overlaps, split multi-function skills, convert model-specific instructions, move retired skills, preserve provenance, and validate the final router-based structure.'
compatibility: 'Requires filesystem write access. Use a branch or reversible workspace and preserve an inventory mapping from every source skill to its final disposition.'
metadata:
  category: agent-skills
  type: library-restructure
  source: custom
---

# Skill Library Restructure

Apply approved dispositions and produce a coherent router-based skills library.

## When to Use

Use this skill when:

- Inventory and review decisions already exist
- Skills must be grouped by function
- Overlapping skills need consolidation
- Oversized skills need functional splitting
- Claude-specific or other provider-specific skills need conversion
- Retired skills need quarantine or removal from the active tree
- Parent category routers and a root router must be built

Do not start with this skill before the source inventory exists.

## Required Inputs

Resolve:

- Source, quarantine, and rebuilt paths
- Inventory with one row per source skill
- Approved application stack
- Primary disposition for each source skill
- Naming and frontmatter conventions
- Reference architecture for parent/child skills
- Validation commands

## Restructure Principles

- Every source skill has one traceable outcome
- Group by functional job, not merely by application name
- Parent skills route; child skills execute
- Keep hierarchy shallow
- Merge only true workflow duplicates
- Split only independent triggers or outcomes
- Preserve uniquely useful instructions and resources
- Remove accidental model coupling
- Do not silently discard files

## Workflow

### 1. Freeze the Decision Map

Before moving files, confirm each source skill is marked:

- Keep
- Refine
- Convert
- Split
- Merge
- Quarantine
- Retire

Resolve ambiguous rows before broad filesystem changes.

### 2. Design Functional Categories

Cluster retained capabilities by user job and expected outcome.

Good category signals:

- Development
- Infrastructure and deployment
- Data and analytics
- Design and UX
- Documentation and knowledge
- Marketing and SEO
- Automation and integrations
- Agent skills

Avoid empty categories and excessive nesting.

### 3. Define Canonical Skills

For each overlap cluster:

1. Compare triggers, inputs, outputs, workflows, and resources
2. Select or create the canonical skill
3. Map unique content into the canonical destination
4. Remove contradictions and duplicate instructions
5. Record superseded source paths

### 4. Split Multi-Function Skills

Split when sections have different:

- Trigger scenarios
- Inputs
- Tools or permissions
- Outputs
- Safety boundaries
- Completion checks

Create a parent router only when the children belong to one functional family.

### 5. Convert Model-Specific Skills

Replace unnecessary provider assumptions with capability-based instructions.

Search for:

- Provider-specific directories and instruction files
- Hooks and slash commands
- Proprietary tool names
- Forced model identity
- Unsupported agent or delegation syntax

Retain provider-specific content only when the skill's job is explicitly provider-specific and approved.

### 6. Build Routers

Each category router should:

- Explain the category purpose
- List every active child path
- Distinguish overlapping triggers
- Define shared constraints
- Provide common workflow routes
- Avoid repeating full child procedures

The root router should route among categories rather than enumerate every detail.

### 7. Move or Retire Sources

- Move unresolved or potentially reusable sources to quarantine
- Remove superseded skills from active discovery
- Preserve provenance in the inventory and consolidation report
- Check dependencies and router links before removal
- Keep Git history or backups for recovery

### 8. Validate the Final Tree

Confirm:

- Every active folder with `SKILL.md` has valid frontmatter
- Folder and skill names match
- All router links resolve
- Every child appears in exactly one intended category
- No active skill references retired paths
- Trigger boundaries are clear
- No source disposition is missing
- Converted skills have no accidental provider coupling

### 9. Reconcile the Inventory

Update every source row with:

- Final disposition
- Final path
- Merged-into path
- Split-into paths
- Conversion status
- Validation result

Counts in reports must match the filesystem.

## Deliverables

Create or update:

- Root router
- Category routers
- Canonical child skills
- Source-to-final inventory
- Merge and split map
- Provider-conversion report
- Compatibility report
- Validation summary

## Completion Checks

- Source inventory existed before moves
- Every source has one traceable final outcome
- Active skills are grouped by functional job
- Parent and child responsibilities are distinct
- Duplicate triggers and workflows were reduced
- Retired skills are absent from active discovery
- All links and references validate
- Reports reconcile with the final filesystem
