---
name: skill-check
description: 'Validate a SKILL.md and its folder against the Agent Skills specification and repository conventions. Use when checking frontmatter, naming, discovery descriptions, structure, relative paths, bundled resources, trigger boundaries, or readiness before publishing or retaining a rebuilt skill.'
compatibility: 'Read-only unless the user explicitly asks for repairs. Use the repository validator when available.'
metadata:
  category: agent-skills
  type: validation
  source: consolidated
---

# Skill Check

Validate one skill package after creation, conversion, refinement, merge, or split.

## When to Use

Use this skill when:

- A new or rebuilt skill needs a final compliance check
- A skill is not being discovered or triggered correctly
- Folder and frontmatter names may not match
- Relative links or bundled resources may be broken
- A library needs a consistent validation pass

Do not use this skill for malware or supply-chain analysis; use `../skill-audit/SKILL.md`.
Do not use it to decide whether a skill belongs in the library; use `../skill-review/SKILL.md`.

## Workflow

### 1. Resolve the Target

Identify the skill directory, `SKILL.md`, repository conventions, and any documented validator.

Read the complete `SKILL.md` and inventory bundled files.

### 2. Validate Frontmatter

Check:

- YAML parses correctly
- Opening and closing delimiters are valid
- `name` exists and matches the folder exactly
- Name uses lowercase letters, numbers, and hyphens
- `description` exists and fits specification limits
- Description explains both what the skill does and when to use it
- Optional fields are supported and purposeful
- Declared tools and compatibility requirements match the body

### 3. Validate Discovery and Boundaries

Check whether:

- Important trigger terms appear early in the description
- The description uses realistic user language
- Neighboring skills have distinguishable triggers
- The skill states when not to use it where ambiguity is likely
- The description does not promise unsupported capabilities

### 4. Validate Structure

Check:

- The skill has one coherent primary job
- Workflow steps are ordered and actionable
- Prerequisites are explicit
- Destructive actions have safeguards
- Expected outputs are defined
- Completion and verification checks exist
- Long supporting detail uses progressive disclosure
- Empty sections, placeholders, and duplicate instructions are removed

### 5. Validate Bundled Resources

For every referenced file:

- Confirm the path exists with exact case
- Confirm the file is used by the workflow
- Confirm scripts have a clear entry point and input validation
- Confirm templates contain no production secrets
- Confirm assets are appropriate for repository limits
- Confirm references do not contradict `SKILL.md`

Flag orphaned files and unreferenced resources.

### 6. Validate Environment Claims

Check:

- Referenced commands and tools are discoverable or declared prerequisites
- Hardcoded paths are justified
- Model-specific assumptions are intentional
- Unsupported applications are not required accidentally
- The skill does not claim network, repository, or filesystem access it may not have

### 7. Run Available Validators

Discover and run the repository-provided validation command when possible.

Do not invent a validator command. Do not report a successful run unless it actually executed.

### 8. Report Results

Classify findings as:

- **Critical**: Skill cannot load, referenced files are missing, or instructions are unsafe
- **Warning**: Discovery, structure, dependency, or workflow problem likely to reduce reliability
- **Suggestion**: Non-blocking clarity or maintainability improvement

## Output Format

```markdown
## Skill Check: <name>

### Result
Pass | Pass with warnings | Fail

### Critical
- <location>: <issue> — <fix>

### Warnings
- <location>: <issue> — <fix>

### Suggestions
- <location>: <issue> — <fix>

### Validator
- Command:
- Result:

### Verified
- Frontmatter
- Name/folder match
- Description triggers
- Relative paths
- Bundled resources
- Workflow and completion checks
```

## Completion Checks

- Full skill and bundled resources were inspected
- Specification and repository rules were applied
- Every finding includes a location and corrective action
- Validator execution is reported truthfully
- Final result is explicit
