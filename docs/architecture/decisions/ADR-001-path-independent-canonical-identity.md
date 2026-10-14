# ADR-001: Path-Independent Canonical Semantic Identity

- **Status**: Accepted
- **Deciders**: Architecture Working Group, REVREBEL Agent Platform Team
- **Date**: 2026-10-14
- **Related Issues**: [REV-126](https://linear.app/revrebel/issue/REV-126), [REV-150](https://linear.app/revrebel/issue/REV-150), [REV-127](https://linear.app/revrebel/issue/REV-127), [REV-128](https://linear.app/revrebel/issue/REV-128), [REV-130](https://linear.app/revrebel/issue/REV-130)

---

## 1. Context and Problem Statement

In the Agent Skills Library (encompassing 2,133 catalog skills across 10 functional categories), skills were historically identified by either their leaf directory name (e.g., `create-pr`) or their relative repository path (e.g., `library/development/fullstack/create-pr`).

During the REV-126 catalog census and REV-150 validation, this implicit identity model caused significant architectural friction:
1. **Physical Path Volatility**: As the library evolves across reorganization phases (such as the upcoming REV-128 physical ownership decisions and REV-129 family eligibility rules), skills may be physically relocated—e.g. moving platform tools into `tools-and-platforms/`, re-routing deep categories, or adopting a registry-first storage model. If identity is path-bound, every physical directory move mutates the skill's identity, breaking external links, workflow step invocations, runtime symlinks, and dependency references.
2. **Namespace Collisions**: Physical directory paths permit identical leaf folder names in different subdirectories. The catalog census exposed **15 duplicate leaf names** between `library/github-operations/*` and `library/development/*` (e.g. `create-pr`, `review-pr`, `git-branch-strategy`). Under a flat leaf-name scheme, these collided; under a relative path scheme, they had unstable identities.
3. **Multi-View Projections**: Skills are published and materialized into multiple distinct runtime environments:
   - Global workstation discovery: individual symlinks in `~/.agents/skills/`
   - Hierarchical category navigation: `SKILL.md` routers in `development/`, `marketing-and-seo/`, etc.
   - Published standalone `runtime` Git branch
   - Project-specific sparse checkouts (e.g., frontend-only or marketing-only skill subsets)

Can canonical identity remain tied to physical filesystem paths, or must it be strictly path-independent?

---

## 2. Decision

**Canonical identity MUST be strictly path-independent.**

Physical filesystem paths are treated strictly as mutable storage locations (`physical_path`), managed by the library registry and compilers. A skill's identity is defined exclusively by a stable, scoped logical identifier.

### 2.1 Identifier Format

Canonical identities adhere to the following specification:

1. **Formal URN Representation**:
   ```text
   urn:skill:<scope>:<slug>
   ```
   Conforms to RFC 8141 syntax.
   - Example: `urn:skill:github:create-pull-request`
   - Example: `urn:skill:architecture:code-refactoring-tech-debt`
   - Example: `urn:skill:seo:audit`

2. **Compact Scoped Representation**:
   ```text
   <scope>:<slug>
   ```
   Used in manifests, dependency references, CLI parameters, and workflow step declarations.
   - `<scope>`: Lowercase alphanumeric string matching `^[a-z0-9-]+$`. Represents the owning domain, platform family, or namespace (e.g. `github`, `figma`, `webflow`, `development`, `quality`, `architecture`, `cro`, `seo`). Singletons not belonging to a specific family or sub-domain use their top-level functional domain or `global`.
   - `<slug>`: Lowercase alphanumeric kebab-case string matching `^[a-z0-9-]+$`. Represents the distinct capability name.

### 2.2 Invariants

1. **Zero Path Syntax in Identifiers**:
   A canonical identifier MUST NOT contain forward slashes (`/`), backward slashes (`\`), directory traversals (`..`), file extensions (`.md`, `.json`, `.yaml`), or drive letters (`C:`).
2. **Immutability Under Relocation**:
   Moving a skill directory from `library/development/backend/foo` to `library/tools-and-platforms/foo` or any future physical layout:
   - **MUST** update `storage.physical_path` in the registry.
   - **MUST NOT** mutate the skill's `canonical_id`.
   - **MUST NOT** break any inbound `depends_on`, `composed_of`, `extends`, or `aliased_to` references.
3. **Reference Exclusivity**:
   All internal relationships and inter-skill references in the object model (`depends_on`, `composed_of`, `extends`, `aliased_to`) **MUST** use canonical identifiers, never physical paths.
4. **Collision-Free Uniqueness**:
   Every canonical ID within the library must be globally unique across all categories and families. Exactly one active object owns a given canonical ID.

---

## 3. Storage and Projection Mapping

The decoupling operates through an explicit two-layer architecture:

```text
+-------------------------------------------------------------+
|                     Logical Identity Layer                  |
|          canonical_id: "github:create-pull-request"         |
|          role: workflow                                     |
+-------------------------------------------------------------+
                              |
                     Registry / Object Model
                              |
        +---------------------+---------------------+
        |                                           |
        v                                           v
+-----------------------------+   +-----------------------------+
|    Physical Storage Layer   |   |    Runtime Projection Layer |
|  path: library/...          |   |  symlink: ~/.agents/skills/ |
|  (managed, movable)         |   |  (flat, namespaced on clash)|
+-----------------------------+   +-----------------------------+
```

1. **Registry Manifest (`audit/runtime-manifest.json` / compiled registry)**:
   Maintains the authoritative bidirectional mapping:
   `canonical_id <--> physical_path <--> runtime_name`.
2. **Runtime Projection Resolution**:
   When projecting to a flat namespace (like `~/.agents/skills/`), if two canonical IDs share a slug (e.g. `github:create-pr` and `dev:create-pr`), the compiler deterministically disambiguates the runtime name using the scope prefix (e.g., `github-create-pr`), while preserving the underlying `canonical_id`.

---

## 4. Consequences

### Positive
- **Physical Refactoring Freedom**: Enables upcoming milestones (REV-128 physical ownership resolution and REV-129 family organization) to safely restructure disk directories without breaking references or external tooling.
- **Unambiguous Multi-Provider Support**: Enables multiple platform implementations of common capabilities (e.g., `github:create-pr` vs `gitlab:create-pr`) without filesystem naming collisions.
- **Reliable Graph Invariants**: Enables dependency analysis, composition DAG cycle checks, and topological sorting based on stable identifiers.
- **Traceable History**: Audit ledgers and telemetry track stable identities over time, even if files are renamed or moved across categories.

### Negative / Trade-offs
- **Registry Indirection**: Resolving a skill from disk requires either inspecting the skill's YAML frontmatter/manifest or performing a registry lookup. This is mitigated by requiring `canonical_id` (or deterministic scope derivation) in the skill package metadata.
- **Enforcement Overhead**: Tooling and validators must strictly enforce that authors do not hardcode relative filesystem paths in skill dependency declarations.
