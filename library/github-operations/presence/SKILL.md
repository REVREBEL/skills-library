---
name: presence
description: 'Improve a GitHub repository or profile for human discoverability and adoption through README structure, topics, description, social preview, badges, contribution guidance, releases, and repository metadata. Use when asked to improve GitHub presence, README quality, project discoverability, or repository presentation.'
compatibility: 'Read-only audits require repository access. Applying metadata or file changes requires GitHub or repository write access.'
metadata:
  category: github
  type: repository-presence
  source: consolidated
---

# GitHub Repository Presence

Improve the repository's human-facing entry points without turning the README into a billboard or claiming unsupported project maturity.

## When to Use

Use for:

- README audits or rewrites
- repository description, topics, website, and social-preview guidance
- profile README improvements
- badges and trust signals
- installation and quick-start clarity
- contribution, support, license, and security entry points
- release and discoverability recommendations

Use `llms-maintain` for machine-oriented `llms.txt` navigation.

## Workflow

### 1. Understand the audience and project

Read the repository's README, documentation, package metadata, releases, contribution files, license, security policy, and current repository metadata.

Identify:

- primary user and use case
- product maturity
- installation path
- supported platforms
- strongest proof of usefulness
- current documentation gaps

Do not infer adoption, performance, compatibility, or security claims without evidence.

### 2. Audit the first screen

The top of the README should answer quickly:

- What is this?
- Who is it for?
- Why would they use it?
- What does it look like or produce?
- How do they start?

Check mobile readability and avoid a dense wall of badges before the project explanation.

### 3. Build an appropriate README structure

Use sections that fit the project:

- concise title and one-line value statement
- screenshot, diagram, or working example
- key capabilities
- quick start
- installation and requirements
- usage examples
- configuration
- documentation links
- support and troubleshooting
- contributing
- security
- license

Preserve useful repository-specific content and inbound links.

### 4. Audit trust signals

Verify every badge and status indicator points to a real source. Prefer a small set such as:

- CI status
- release or package version
- license
- supported runtime
- coverage or security status only when meaningful

Remove broken, redundant, vanity, or misleading badges.

### 5. Improve repository metadata

Review:

- repository description
- website URL
- topics
- social preview
- pinned issues or discussions
- release notes and tags
- issue and PR templates
- `CONTRIBUTING.md`, `SECURITY.md`, and support routes

Use GitHub metadata changes only when authorized.

### 6. Validate usability

Test README commands, relative links, screenshots, badges, and documentation routes. Confirm the quick start works in a clean environment when practical.

### 7. Apply or report

For an audit, return prioritized findings. For an edit, make the smallest coherent set of changes and verify the rendered or source result.

## Quality Rules

- Lead with the project, not decorative badges
- Use concrete examples over abstract marketing claims
- Keep installation commands current and copyable
- Do not fabricate testimonials, stars, downloads, or community size
- Do not expose private repository details in public-facing content
- Preserve accessibility through meaningful alt text and heading order

## Completion

Report the files or metadata changed, validated links and commands, unresolved content gaps, and any claims that still require maintainer evidence.
