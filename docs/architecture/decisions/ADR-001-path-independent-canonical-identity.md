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
   Follows the lexical syntax rules of RFC 8141 for Uniform Resource Names (`urn:<NID>:<NSS>`):
   - `urn:`: Standard scheme prefix (case-insensitive, normalized lowercase).
   - `skill`: The repository's internal/organization Namespace Identifier (NID). *(Note: As an internal/private organization namespace within the skills library ecosystem, it implements RFC 8141 lexical structure without claiming formal IANA registry reservation).*
   - `<scope>:<slug>`: The Namespace Specific String (NSS), containing colon-separated sub-namespaces.
   - Examples:
     * `urn:skill:github:create-pull-request`
     * `urn:skill:software-architecture:code-refactoring-tech-debt`
     * `urn:skill:on-page-seo:audit`

2. **Compact Scoped Representation**:
   ```text
   <scope>:<slug>
   ```
   Used in manifests, dependency references, CLI parameters, and workflow step declarations.
   - `<scope>`: Lowercase alphanumeric string matching `^[a-z0-9-]+$`. Represents the **immutable provenance identity namespace** assigned at minting (e.g. `github`, `figma`, `webflow`, `development`, `quality`, `software-architecture`, `on-page-seo`, `cro`). It is strictly decoupled from mutable functional domain ownership (`domain`), physical location (`physical_path`), and family memberships (`families`).
   - `<slug>`: Lowercase alphanumeric kebab-case string matching `^[a-z0-9-]+$`. Represents the distinct capability name within that provenance namespace.

### 2.2 Collision Prevention and Identity Stability Analysis

How does path-independent canonical identity survive category moves, family restructuring, duplicate resolution, semantic reownership, and alias pointers without collisions?

1. **Category Moves & Storage Restructuring (REV-128)**:
   - A physical filesystem relocation (e.g., moving `library/development/backend/launch` to `library/workflows/launch` or `library/tools-and-platforms/github/create-pr`) updates solely the registry mapping metadata (`physical_path`).
   - The canonical ID (`<scope>:<slug>`) is an immutable semantic coordinate. Moving a folder across disk directories does not change its scope or slug.
2. **Platform Family Extraction & Multi-Provider Disambiguation (REV-129)**:
   - Platform ecosystems utilize their family namespace as their provenance scope (`github:*`, `figma:*`, `webflow:*`, `n8n:*`).
   - Generic domain capabilities use functional domain scopes (`software-architecture:*`, `on-page-seo:*`, `frontend:*`).
   - When resolving identical leaf names (such as the 15 GitHub duplicate pairs discovered in REV-126/150 like `create-pr`), the two assets occupy distinct scopes (`github:create-pr` vs `development:create-pr`), completely preventing namespace collisions.
3. **Duplicate Resolution & Alias Pointers (REV-130)**:
   - When a duplicate pair is consolidated, one canonical asset is chosen as the authoritative owner (`github:create-pull-request`).
   - The retired or legacy identifier is registered as a first-class `alias` object (`alias:create-pr` or `development:create-pr`) with `aliased_to: "github:create-pull-request"`.
   - The single-hop alias invariant guarantees that consumers querying either identity resolve to the exact same canonical target without namespace collisions or circular redirections.
4. **Semantic Reownership & Family Realignment**:
   - The critical test of identity stability is semantic reownership, not merely moving a folder on disk. Consider a capability originally minted in the general development domain (e.g., `development:create-pr`) that is reassigned to a universal platform family.
   - The four architectural axes remain strictly decoupled:
     * **Permanent Identity Namespace**: `canonical_id = "development:create-pr"` (strictly immutable).
     * **Current Semantic Ownership**: `domain = "platform"`, `owner = "core-tooling"` (mutable metadata).
     * **Current Physical Location**: `physical_path = "library/tools-and-platforms/github/create-pr"` (mutable metadata, REV-128).
     * **Family Memberships**: `families = ["github", "developer-tools"]` (mutable metadata, REV-129).
   - Scope is an immutable identity namespace, NOT a live representation of current ownership. Canonical identity survives semantic reownership intact, ensuring existing workflow step invocations and dependency declarations never break.
5. **Collision Rule**:
   Every registered canonical ID must be globally unique across all scopes and slugs:
   $$\text{Count}(\text{Owner}(\text{canonical\_id})) = 1$$
   No two active objects may share the same `<scope>:<slug>`.

### 2.3 Foundational Invariants vs Provisional Guardrails

To prevent REV-127 from prematurely closing decisions assigned to subsequent work orders, contracts are partitioned as follows:

1. **Foundational Invariants (Decided in REV-127)**:
   - **Zero Path Syntax in Identifiers**: Canonical IDs MUST NOT contain forward slashes (`/`), backward slashes (`\`), directory traversals (`..`), file extensions (`.md`, `.json`, `.yaml`), or drive letters (`C:`).
   - **Path Independence**: Moving a skill directory updates `storage.physical_path` in the registry and MUST NOT mutate the skill's `canonical_id`.
   - **Decoupled Scope Immutability**: Canonical `<scope>` is an immutable provenance coordinate; semantic reownership updates `domain`, `owner`, or `families` metadata without mutating `canonical_id`.
   - **Reference Exclusivity**: Inter-skill relationships (`depends_on`, `composed_of`, `extends`, `aliased_to`) MUST use canonical identifiers, never physical paths.
   - **DAG Acyclicity**: Composition and dependency graphs must be strictly acyclic.
   - **Single-Hop Alias Resolution**: Aliases point directly to a canonical target; chained aliases are rejected.

2. **Provisional Design Guardrails (Assigned to REV-128 – REV-130)**:
   - *Physical Directory Layout & Ownership Models*: Evaluated and decided under **REV-128**.
   - *Family Eligibility Criteria & Multi-Provider Rules*: Evaluated and finalized under **REV-129**.
   - *Registry Router Schemas, Alias Lifecycles, and Runtime Projection*: Evaluated and finalized under **REV-130**.
   - *Shallow Overlay Specialization & Primitive Leaf Boundaries*: Established as baseline provisional constraints in REV-127 to ensure safe graph validation; subject to domain refinement in REV-129.

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
|  (managed, movable in 128)  |   |  (flat, namespaced on clash)|
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
