---
name: "llms-txt"
description: "Create and maintain an llms.txt file in a repository root following the llms.txt specification at https://llmstxt.org/. The file gives LLMs a high-level map of a repository — its purpose, key documentation, specifications, examples, and configuration — in a concise, machine-readable, human-readable format. Covers creating from scratch (repository analysis, content discovery, file planning) and updating an existing file to reflect documentation or structure changes."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# LLMs.txt — Repository Guide for LLMs

Create and maintain an `llms.txt` file in the repository root following the official llms.txt specification at https://llmstxt.org/. The file provides high-level guidance to large language models (LLMs) on where to find relevant content for understanding the repository's purpose and specifications.

## When to Use

- Creating a new `llms.txt` from scratch for a repository.
- Updating an existing `llms.txt` to reflect documentation, specification, or structure changes.
- Making a repository easier for LLMs (and humans) to navigate.

## Primary Directive

Produce a comprehensive `llms.txt` that serves as an entry point for LLMs to understand and navigate the repository effectively. The file must comply with the llms.txt specification and be optimized for LLM consumption while remaining human-readable.

## Format Specification

The `llms.txt` file must follow this exact structure per the specification:

1. **H1 Header** — a single line with the repository/project name (required).
2. **Blockquote Summary** — a brief description in blockquote format (optional but recommended).
3. **Additional Details** — zero or more markdown sections without headings for context.
4. **File List Sections** — zero or more H2 sections containing markdown lists of links.

### File link format

Each file link must follow: `[descriptive-name](https://example.com): optional description`

### Section organization

Organize files into logical H2 sections such as:

- **Documentation** — core documentation files
- **Specifications** — technical specifications and requirements
- **Examples** — sample code and usage examples
- **Configuration** — setup and configuration files
- **Optional** — secondary files (special meaning: can be skipped for shorter context)

### Content guidelines

**Language and style:**
- Use concise, clear, unambiguous language.
- Avoid jargon without explanation.
- Write for both human and LLM readers.
- Be specific and informative in descriptions.

**Include files that:**
- Explain the repository's purpose and scope.
- Provide essential technical documentation.
- Show usage examples and patterns.
- Define interfaces and specifications.
- Contain configuration and setup instructions.

**Exclude files that:**
- Are purely implementation details.
- Contain redundant information.
- Are build artifacts or generated content.
- Are not relevant to understanding the project.

## Workflow A — Create from Scratch

### Step 1: Review the specification

- Review https://llmstxt.org/ to ensure full compliance.
- Understand the required format structure and guidelines.
- Note the specific markdown structure requirements.

### Step 2: Analyze the repository structure

- Examine the complete repository structure.
- Identify the primary purpose and scope.
- Catalog all important directories and their purposes.
- List key files valuable for LLM understanding.

### Step 3: Discover content

- Identify README files and their locations.
- Find documentation files (`.md` in `/docs/`, `/spec/`, etc.).
- Locate specification files and their purposes.
- Discover configuration files and their relevance.
- Find example files and code samples.
- Identify any existing documentation structure.

### Step 4: Plan the content

- Repository purpose and scope summary.
- Priority-ordered list of essential files for LLM understanding.
- Secondary files that provide additional context.
- Organizational structure for the `llms.txt` file.

### Step 5: Create the file

1. Create `llms.txt` in the repository root.
2. Follow the exact format specification.
3. Include all required sections.
4. Use proper markdown formatting.
5. Ensure all links are valid relative paths.

### Step 6: Validate

1. Verify compliance with https://llmstxt.org/.
2. Check that all links are valid and accessible.
3. Ensure the file serves as an effective LLM navigation tool.
4. Confirm the file is both human and machine readable.

## Workflow B — Update an Existing File

### Step 1: Review current file and specification

- Read the existing `llms.txt` to understand current structure.
- Review https://llmstxt.org/ for continued compliance.
- Identify areas that may need updates based on repository changes.

### Step 2: Analyze structure and detect changes

- Examine the current repository structure.
- Compare current structure with what's documented in the existing `llms.txt`.
- Identify new directories, files, or documentation to include.
- Note any removed or relocated files that need updating.

### Step 3: Discover new content

- Find new README files and documentation (`.md` in `/docs/`, `/spec/`, etc.).
- Locate new specification files and their purposes.
- Discover new configuration files and their relevance.
- Find new example files and code samples.
- Identify changes to the existing documentation structure.

### Step 4: Plan the update

- Changes needed to maintain accuracy.
- New files to add.
- Outdated references to remove or update.
- Organizational improvements to maintain clarity.

### Step 5: Apply updates

1. Update the existing `llms.txt` in the repository root.
2. Maintain compliance with the exact format.
3. Add new file references with appropriate descriptions.
4. Remove or update outdated references.
5. Ensure all links are valid relative paths.

### Step 6: Validate

1. Verify continued compliance with https://llmstxt.org/.
2. Check that all links are valid and accessible.
3. Ensure the file still serves as an effective LLM navigation tool.
4. Confirm the file remains both human and machine readable.

### Update strategy

**Adding content:**
1. Identify the appropriate section for new files.
2. Create clear, descriptive names for links.
3. Write concise but informative descriptions.
4. Maintain alphabetical or logical ordering within sections.
5. Consider whether new sections are needed for new content types.

**Removing content:**
1. Verify files are actually removed or relocated.
2. Check if relocated files should be updated rather than removed.
3. Remove entire sections if they become empty.
4. Update cross-references if needed.

**Reorganizing content:**
1. Maintain logical flow from general to specific.
2. Keep essential documentation in primary sections.
3. Move secondary content to the "Optional" section if appropriate.
4. Ensure the new organization improves LLM navigation.

## Example Structure Template

```txt
# [Repository Name]

> [Concise description of the repository's purpose and scope]

[Optional additional context paragraphs without headings]

## Documentation

- [Main README](README.md): Primary project documentation and getting started guide
- [Contributing Guide](CONTRIBUTING.md): Guidelines for contributing to the project
- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines and expectations

## Specifications

- [Technical Specification](spec/technical-spec.md): Detailed technical requirements and constraints
- [API Specification](spec/api-spec.md): Interface definitions and data contracts

## Examples

- [Basic Example](examples/basic-usage.md): Simple usage demonstration
- [Advanced Example](examples/advanced-usage.md): Complex implementation patterns

## Configuration

- [Setup Guide](docs/setup.md): Installation and configuration instructions
- [Deployment Guide](docs/deployment.md): Production deployment guidelines

## Optional

- [Architecture Documentation](docs/architecture.md): Detailed system architecture
- [Design Decisions](docs/decisions.md): Historical design decision records
```

## Quality Assurance

### Format validation

- ✅ H1 header with project name
- ✅ Blockquote summary (if included)
- ✅ H2 sections for file lists
- ✅ Proper markdown link format
- ✅ No broken or invalid links
- ✅ Consistent formatting throughout

### Content validation

- ✅ Clear, unambiguous language
- ✅ Comprehensive coverage of essential files
- ✅ Logical organization of content
- ✅ Appropriate file descriptions
- ✅ Serves as an effective LLM navigation tool

### Specification compliance

- ✅ Follows https://llmstxt.org/ format exactly
- ✅ Uses required markdown structure
- ✅ Implements optional sections appropriately
- ✅ File located at repository root (`/llms.txt`)

## Success Criteria

The `llms.txt` file should:

1. Enable LLMs to quickly understand the repository's purpose.
2. Provide clear navigation to essential documentation.
3. Follow the official llms.txt specification exactly.
4. Be comprehensive yet concise.
5. Serve both human and machine readers effectively.
6. Include all critical files for project understanding.
7. Use clear, unambiguous language throughout.
8. Organize content logically for easy consumption.
9. (When updating) accurately reflect the current repository structure and content, with outdated references removed.

## Merged from

- `llms-create` (create-llms) — creating an `llms.txt` from scratch: specification review, repository analysis, content discovery, file planning, creation, validation
- `llms-update` (update-llms) — updating an existing `llms.txt`: current-state analysis, change detection, add/remove/reorganize strategy, validation

## Limitations

- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.