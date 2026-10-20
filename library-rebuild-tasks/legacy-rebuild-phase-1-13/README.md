# Legacy Skills Library Rebuild Tasks (Phases 01–13)

> **IMMUTABLE AUDIT EVIDENCE — SUPERSEDED BY ARCHITECTURE VALIDATION ROADMAP (REV-132)**

## Historical Context

This directory preserves the original task specifications (Phases 01 through 13) authored during the initial skills library restructuring in August–September 2026.

These legacy tasks guided the early inventorying, compatibility auditing, Claude-dependency neutralization, functional taxonomy drafting, and Phase 08 batch migrations. The historical artifacts and evidence produced by these tasks are permanently preserved and protected in:
- `audit/rebuild-phase-1-12/` (historical CSV inventories, batch plans, split allocations, merge decisions, and validation logs)
- `library-rebuild-tasks/artifacts/` (historical analysis scripts and batch execution logs)

## Why These Tasks Were Superseded

During execution of the original plan, critical architectural limitations were identified:
1. **Unstructured Duplicate Cleanup**: Phase 06 attempted bulk deduplication using heuristic name matching and path-depth winner selection. As documented in [REV-125](https://linear.app/revrebel/issue/REV-125/hold-bulk-duplicate-reconciliation-until-taxonomy-architecture-is-approved), path-depth rules were structurally deterministic but semantically invalid for capability families (e.g. NotebookLM, Figma, GitHub). Bulk deduplication was formally placed on hold.
2. **Path Coupling**: The legacy tasks treated physical directory paths as primary skill identities, resulting in broken links and reference amnesia whenever files moved.
3. **Provider Entanglement**: Execution transports (CLI, MCP, SDK, REST) were coupled directly with skill logic rather than isolated into pure protocol adapters.
4. **Lack of Verifiable Manifest Authenticity**: Migration authorizations lacked fresh cryptographic SHA-256 cross-examination and strict staging path containment, risking asset loss.

## Approved Replacement Architecture

Under **REV-126 through REV-131**, the technical architecture was formally defined and approved:
- **[REV-126 / REV-150]**: Catalog-wide Semantic Role Census (`audit/taxonomy-census/semantic-role-census.json`)
- **[ADR-001]** ([docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md](../../docs/architecture/decisions/ADR-001-path-independent-canonical-identity.md)): Canonical Semantic Object Model & RFC 8141 URNs
- **[ADR-002]** ([docs/architecture/decisions/ADR-002-physical-ownership-model.md](../../docs/architecture/decisions/ADR-002-physical-ownership-model.md)): Physical Ownership Model (Tier 1 Platform Hubs vs. Domain Directories)
- **[ADR-003]** ([docs/architecture/decisions/ADR-003-family-eligibility-and-provider-adapters.md](../../docs/architecture/decisions/ADR-003-family-eligibility-and-provider-adapters.md)): Platform Family Eligibility & Provider-Adapter Implementation Rules
- **[ADR-004]** ([docs/architecture/decisions/ADR-004-registry-router-alias-dependency-contracts.md](../../docs/architecture/decisions/ADR-004-registry-router-alias-dependency-contracts.md)): Registry, Router, Alias, Dependency, and Semantic Group Contracts
- **[ADR-005]** ([docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md](../../docs/architecture/decisions/ADR-005-architecture-validation-and-migration-gates.md)): 9 Formal Architecture Validation and Migration Gates

## Current Active Migration Roadmap

The active, authoritative migration roadmap replacing these legacy tasks is located at:
- Master Roadmap: `docs/architecture/MIGRATION_ROADMAP.md`
- Active Gated Phase Specifications: `library-rebuild-tasks/phase-*.md`
- Validation Engine: `tools/skill_library/migration_gates.py` (`MigrationGateRunner`)

**Do not execute or modify the markdown files in this directory.**
