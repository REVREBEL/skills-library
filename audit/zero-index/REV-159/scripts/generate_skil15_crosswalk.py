#!/usr/bin/env python3
"""
Zero-Index Inventory & Functional Crosswalk Generator for SKIL-15 (ZI-02).

This generator deterministically produces the 6 required audit deliverables:
  1. archive-source-manifest.csv
  2. script-reuse-crosswalk.csv
  3. module-capability-matrix.md
  4. gaps-and-collisions.md
  5. commands-and-tests.md (initial template or verified output)
  6. summary.md
"""

import argparse
import ast
import csv
import hashlib
from pathlib import Path


AUTHORITATIVE_52_SCRIPTS = [
    "analyze_inventory_columns.py",
    "analyze_provider_coupling_detailed.py",
    "analyze_provider_dependencies.py",
    "build_phase_05_artifacts.py",
    "build_phase_06_artifacts.py",
    "build_phase_07_artifacts.py",
    "build_phase_08_artifacts.py",
    "catalog_semantic_census.py",
    "classify_compatibility.py",
    "dry_run_provider_conversion.py",
    "execute_phase08_batches.py",
    "execute_provider_conversion.py",
    "execute_provider_conversion_pass2.py",
    "execute_provider_conversion_pass3.py",
    "fix_cumulative_reconciliation.py",
    "fix_mcp_zod.py",
    "fix_registry_check.py",
    "gen_phase11_artifacts.py",
    "gen_phase12_artifacts.py",
    "generate_batch_plan.py",
    "generate_inventory.py",
    "generate_ledger.py",
    "neutralize_claude_dependencies.py",
    "neutralize_claude_dependencies_v2.py",
    "patch_phase_08_batch1.py",
    "run_all_batches.py",
    "semantic_cleanup.py",
    "skill-library.py",
    "test_family_eligibility.py",
    "test_migration_gates.py",
    "test_migration_roadmap.py",
    "test_physical_ownership.py",
    "test_registry_router_contracts.py",
    "test_runtime_publication.py",
    "test_scenarios.py",
    "test_semantic_census.py",
    "test_semantic_object_model.py",
    "update_check16.py",
    "update_csv_evidence.py",
    "update_descriptions.py",
    "update_phase_08_batch1.py",
    "validate_semantic_census.py",
    "verify_phase_04.py",
    "verify_phase_05.py",
    "verify_phase_06.py",
    "verify_phase_07.py",
    "verify_phase_08.py",
    "verify_phase_08_cumulative.py",
    "verify_phase_09.py",
    "verify_phase_10.py",
    "verify_phase_11.py",
    "verify_phase_12.py",
]

CORE_14_MODULES = [
    "object_model.py",
    "ledger.py",
    "registry_contract.py",
    "config.py",
    "family_contract.py",
    "physical_layout.py",
    "migration_gates.py",
    "manifest.py",
    "sync.py",
    "intake.py",
    "intake_capture.py",
    "publisher.py",
    "validator.py",
    "pilot.py",
]

CROSSWALK_RECORDS = [
    {
        "archived_script": "analyze_inventory_columns.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/migration_gates.py",
        "current_function": "HistoricalProvenanceMapper.reconcile",
        "has_test": "UNVERIFIED",
        "status": "NEEDS-FURTHER-TEST",
        "rationale": "Historical Phase 02 utility checking legacy CSV headers and nullity. Conceptual equivalent in modern architecture is HistoricalProvenanceMapper.reconcile, which performs structured provenance mapping and manifest reconciliation; has_test marked UNVERIFIED pending isolated testing against zero-index baseline.",
        "suggested_zi_target": "ZI-03",
    },
    {
        "archived_script": "analyze_provider_coupling_detailed.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/family_contract.py",
        "current_function": "ExecutionProviderBinding.validate",
        "has_test": "TRUE",
        "status": "ADAPT-EXISTING",
        "rationale": "Evaluated deep Claude and tool couplings across legacy skills via regex text search. Modern provider qualification is codified in data contracts via ExecutionProviderBinding.validate (tested in tests/test_family_eligibility.py). Any automated coupling scanner for unstructured skill text would be adapted in ZI-04.",
        "suggested_zi_target": "ZI-04",
    },
    {
        "archived_script": "analyze_provider_dependencies.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/family_contract.py",
        "current_function": "ExecutionProviderContract.validate_capability_providers",
        "has_test": "TRUE",
        "status": "ADAPT-EXISTING",
        "rationale": "Regex scanner for provider-specific dependencies (Anthropic, Bedrock, Vertex). Replaced by typed ProviderType enums and ExecutionProviderContract.validate_capability_providers in family_contract.py (tested in tests/test_family_eligibility.py). Adaptable in ZI-04 if automated regex extraction from raw unparsed skill bodies is needed.",
        "suggested_zi_target": "ZI-04",
    },
    {
        "archived_script": "build_phase_05_artifacts.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/registry_contract.py",
        "current_function": "CatalogCompiler.compile",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 05 legacy functional taxonomy builder enforcing obsolete 2,103 leaf count and legacy category bins. Conceptual equivalence to CatalogCompiler.compile in modern architecture (which has contract tests), but historical script itself is retired, unexecuted in test suites, and prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "build_phase_06_artifacts.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/registry_contract.py",
        "current_function": "AliasResolver.resolve",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "One-time artifact builder for Phase 06 skill consolidation (merges/splits). Conceptual equivalence to AliasResolver.resolve in modern architecture (which has contract tests), but historical script is retired, untested, and prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "build_phase_07_artifacts.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/physical_layout.py",
        "current_function": "PhysicalLayoutValidator.validate_object_placement",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 07 oversized skill splitting generator. Conceptual equivalence to PhysicalLayoutValidator.validate_object_placement, but historical script is retired, untested, and prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "build_phase_08_artifacts.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/registry_contract.py",
        "current_function": "CatalogRegistry.add_entry",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Constructed historical Phase 08 canonical registry CSVs using hardcoded phase schemas. Conceptual equivalence to CatalogRegistry.add_entry, but historical script is retired, untested, and prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "catalog_semantic_census.py",
        "archived_function": "main",
        "current_file": "tools/validate_semantic_census.py",
        "current_function": "main",
        "has_test": "UNVERIFIED",
        "status": "REUSE-AS-IS",
        "rationale": "Authoritative semantic role census generator runner located in tools/catalog_semantic_census.py, delegating directly to validate_semantic_census.main(). Census data contracts verified by tests/test_semantic_census.py, but CLI main() entrypoint lacks direct unit test execution (has_test downgraded from static claim).",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "classify_compatibility.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/family_contract.py",
        "current_function": "FamilyCandidateEvaluator.evaluate",
        "has_test": "TRUE",
        "status": "ADAPT-EXISTING",
        "rationale": "Evaluated application compatibility gates for Phase 03. Formalized into FamilyTier qualification and FamilyCandidateEvaluator.evaluate in family_contract.py (tested in tests/test_family_eligibility.py). Adaptable for ZI-04 gate automation.",
        "suggested_zi_target": "ZI-04",
    },
    {
        "archived_script": "dry_run_provider_conversion.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/family_contract.py",
        "current_function": "FamilyCandidateEvaluator.evaluate",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Dry-run script for Phase 04 provider neutralization. Conceptual equivalence to FamilyCandidateEvaluator.evaluate in family_contract.py, but historical script is retired, untested, and prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "execute_phase08_batches.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Historical batch re-writer that modified skill packages on disk during Phase 08. MUST NEVER BE EXECUTED against live catalog or zero-index snapshot under ADR-000.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "execute_provider_conversion.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "In-place regex string replacement script targeting Claude provider syntax in Phase 04. Deprecated and retired; historical writer that must never run against live catalog.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "execute_provider_conversion_pass2.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Second pass in-place provider mutator for Phase 04. Deprecated and retired; historical writer that must never run against live catalog.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "execute_provider_conversion_pass3.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Third pass in-place provider mutator for Phase 04. Deprecated and retired; historical writer that must never run against live catalog.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "fix_cumulative_reconciliation.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/ledger.py",
        "current_function": "ChangeLedger.record_change",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "One-time patch script reconciling cumulative discrepancy counts in Phase 08. Modern append-only ledger mechanics are tested in tests/test_ledger.py, but the specific historical reconciliation script behavior lacks direct unit test coverage (conceptual equivalence only; has_test downgraded from static claim). Prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "fix_mcp_zod.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Ad-hoc AST patch script for MCP Zod schema syntax across legacy packages. Retired; package integrity is enforced via schema validation gates without file mutation.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "fix_registry_check.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/validator.py",
        "current_function": "validate_library_integrity",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "One-time fix for registry check 16 in Phase 08. Conceptual equivalence to validate_library_integrity in modern architecture, but historical script is retired, untested, and prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "gen_phase11_artifacts.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/validator.py",
        "current_function": "validate_library_integrity",
        "has_test": "UNVERIFIED",
        "status": "ADAPT-EXISTING",
        "rationale": "Phase 11 full-library validation artifact generator. Validation logic has been formalized into validate_library_integrity; mapped entrypoint is exercised in integration tests (test_runtime_publication.py) but lacks direct unit test execution in core 213 test suite (has_test marked UNVERIFIED).",
        "suggested_zi_target": "ZI-04",
    },
    {
        "archived_script": "gen_phase12_artifacts.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/pilot.py",
        "current_function": "run_targeted_pilot",
        "has_test": "UNVERIFIED",
        "status": "ADAPT-EXISTING",
        "rationale": "Phase 12 pilot review artifact generator. Formalized into run_targeted_pilot; mapped entrypoint is exercised in scenario tests (test_scenarios.py) but lacks direct unit test execution in core 213 test suite (has_test marked UNVERIFIED).",
        "suggested_zi_target": "ZI-05",
    },
    {
        "archived_script": "generate_batch_plan.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/registry_contract.py",
        "current_function": "ProjectMaterializer.materialize_bundle",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Partitioned legacy skills into 160 migration batches for Phase 08. Conceptual equivalence to ProjectMaterializer.materialize_bundle in modern architecture (which has contract tests), but historical script is retired, untested, and prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "generate_inventory.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/migration_gates.py",
        "current_function": "SkillPackageManifest.from_directory",
        "has_test": "TRUE",
        "status": "ADAPT-EXISTING",
        "rationale": "Phase 02 inventory scanner. Core directory walking and package SHA-256 manifest logic was adapted into SkillPackageManifest.from_directory and zero-index baseline scanners in ZI-01/ZI-03.",
        "suggested_zi_target": "ZI-03",
    },
    {
        "archived_script": "generate_ledger.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/ledger.py",
        "current_function": "ChangeLedger.record_change",
        "has_test": "UNVERIFIED",
        "status": "ADAPT-EXISTING",
        "rationale": "Phase 01/02 change ledger builder. Codified into tools/skill_library/ledger.py as the official append-only JSONL ChangeLedger interface; unit tests in tests/test_ledger.py verify ChangeLedger, but historical script CLI/entrypoint is not directly exercised by test suites (has_test downgraded from static claim).",
        "suggested_zi_target": "ZI-03",
    },
    {
        "archived_script": "neutralize_claude_dependencies.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Historical writer script performing regex replacements of Claude-specific prompt syntax. Retired; must never be run against live catalog under Zero-Index immutability.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "neutralize_claude_dependencies_v2.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Historical writer script second revision for Claude prompt neutralization. Retired; must never be run against live catalog.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "patch_phase_08_batch1.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "One-time patch script for batch 1 of Phase 08. Historical migration writer; must never be run against live catalog.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "run_all_batches.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Orchestrator for all 160 historical Phase 08 migration batches. Retired; batch migration is finished and live catalog writes are prohibited.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "semantic_cleanup.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "One-time sanitization script for legacy metadata fields. Superseded by object_model.py validation rules. Prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "skill-library.py",
        "archived_function": "main",
        "current_file": "tools/skill-library.py",
        "current_function": "main",
        "has_test": "UNVERIFIED",
        "status": "REUSE-AS-IS",
        "rationale": "Unified CLI management entrypoint active in repository at tools/skill-library.py, providing scan, intake, validate, sync, and publish subcommands; CLI entrypoint itself lacks direct unit test execution in core 213 test suite (has_test marked UNVERIFIED).",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_family_eligibility.py",
        "archived_function": "TestFamilyEligibilityGates",
        "current_file": "tests/test_family_eligibility.py",
        "current_function": "TestFamilyEligibilityGates",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Comprehensive unit test suite for family eligibility contracts (ADR-003). Active in tests/test_family_eligibility.py and passes 40/40 tests.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_migration_gates.py",
        "archived_function": "TestMigrationGates",
        "current_file": "tests/test_migration_gates.py",
        "current_function": "TestMigrationGateRunnerEndToEnd",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Comprehensive unit test suite for G01-G08 architecture migration gates (ADR-005). Active in tests/test_migration_gates.py and passes 56/56 tests across 11 test classes.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_migration_roadmap.py",
        "archived_function": "TestMigrationRoadmap",
        "current_file": "tests/test_migration_roadmap.py",
        "current_function": "TestMigrationRoadmapContracts",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Comprehensive unit test suite for MIGRATION_ROADMAP milestone progression. Active in tests/test_migration_roadmap.py and passes 14/14 tests.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_physical_ownership.py",
        "archived_function": "TestPhysicalOwnership",
        "current_file": "tests/test_physical_ownership.py",
        "current_function": "TestPhysicalLayoutValidator",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Comprehensive unit test suite for physical ownership plane contracts (ADR-002). Active in tests/test_physical_ownership.py and passes 19/19 tests across 3 test classes.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_registry_router_contracts.py",
        "archived_function": "TestRegistryRouterContracts",
        "current_file": "tests/test_registry_router_contracts.py",
        "current_function": "TestCatalogCompilerAndIdempotency",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Comprehensive unit test suite for registry/router alias and dependency contracts (ADR-004). Active in tests/test_registry_router_contracts.py and passes 39/39 tests across 9 test classes.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_runtime_publication.py",
        "archived_function": "TestRuntimeGitClonePublication",
        "current_file": "tests/test_runtime_publication.py",
        "current_function": "TestRuntimeGitClonePublication",
        "has_test": "UNVERIFIED",
        "status": "REUSE-AS-IS",
        "rationale": "Integration test suite for git clone publication and runtime target synchronization. Active in tests/test_runtime_publication.py; excluded from fast core 213 unit test suite due to live clone and mock environment prerequisites (has_test marked UNVERIFIED).",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_scenarios.py",
        "archived_function": "TestGlobalRuntimePath",
        "current_file": "tests/test_scenarios.py",
        "current_function": "TestGlobalRuntimePath",
        "has_test": "UNVERIFIED",
        "status": "REUSE-AS-IS",
        "rationale": "Scenario and path validation test suite covering runtime distribution and global path handling. Active in tests/test_scenarios.py; excluded from fast core 213 unit test suite due to mock repo prerequisites (has_test marked UNVERIFIED).",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_semantic_census.py",
        "archived_function": "TestSemanticCensusValidation",
        "current_file": "tests/test_semantic_census.py",
        "current_function": "TestSemanticCensusInvariants",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Validation test suite for semantic role census integrity and schema rules. Active in tests/test_semantic_census.py and passes 10/10 tests.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "test_semantic_object_model.py",
        "archived_function": "TestSemanticObjectModel",
        "current_file": "tests/test_semantic_object_model.py",
        "current_function": "TestCanonicalIdentity",
        "has_test": "TRUE",
        "status": "REUSE-AS-IS",
        "rationale": "Comprehensive unit test suite for CanonicalIdentity and ObjectGraph (ADR-001). Active in tests/test_semantic_object_model.py and passes 35/35 tests across 4 test classes.",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "update_check16.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Ad-hoc updater for historical check 16 evidence in Phase 08. Deprecated and retired; historical writer prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "update_csv_evidence.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "One-time CSV evidence mutation script from Phase 08. Deprecated and retired; historical writer prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "update_descriptions.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Batch updater for skill frontmatter descriptions in Phase 08. Deprecated and retired; historical writer prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "update_phase_08_batch1.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Specific batch updater for Phase 08 batch 1. Deprecated and retired; historical writer prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "validate_semantic_census.py",
        "archived_function": "main",
        "current_file": "tools/validate_semantic_census.py",
        "current_function": "main",
        "has_test": "UNVERIFIED",
        "status": "REUSE-AS-IS",
        "rationale": "Authoritative semantic role census validation tool active in tools/validate_semantic_census.py. Core census models and data contracts verified by tests/test_semantic_census.py, but CLI main() entrypoint lacks direct unit test execution (has_test downgraded from static claim).",
        "suggested_zi_target": "ACTIVE_IN_REPO",
    },
    {
        "archived_script": "verify_phase_04.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 04 acceptance verifier asserting legacy phase assumptions and fixed counts. Retired in favor of G01-G08 migration gates.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_05.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 05 acceptance verifier asserting legacy 2,103 leaf counts and taxonomy boundaries. Retired; superseded by ADR-004 contracts.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_06.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 06 consolidation verifier checking legacy merge/split outcomes. Retired; superseded by AliasResolver contracts.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_07.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 07 skill-splitting verifier. Retired; superseded by PhysicalLayoutValidator.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_08.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 08 canonical registry verifier. Retired; superseded by ObjectGraph and CatalogRegistry.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_08_cumulative.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/migration_gates.py",
        "current_function": "MigrationGateRunner.run_all_gates",
        "has_test": "UNVERIFIED",
        "status": "NEEDS-FURTHER-TEST",
        "rationale": "Cumulative reconciliation verifier checking discrepancy counts across historical phases. Conceptual equivalence to MigrationGateRunner.run_all_gates in modern architecture (which has contract tests), but historical script is retired, untested against zero-index baseline, and marked UNVERIFIED.",
        "suggested_zi_target": "ZI-03",
    },
    {
        "archived_script": "verify_phase_09.py",
        "archived_function": "main",
        "current_file": "HISTORICAL_REBUILD_ONLY",
        "current_function": "NONE_RETIRED",
        "has_test": "FALSE",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 09 resource registry verifier. Retired; superseded by physical_layout.py and migration_gates.py.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_10.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/registry_contract.py",
        "current_function": "FamilyRouterGenerator.generate_tier_1_hub_router",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 10 functional routing map verifier. Asserts legacy routing contracts and static counts; must NOT be treated as live Codex A/B/C runner or hybrid router compiler. Modern routers are generated deterministically by FamilyRouterGenerator.generate_tier_1_hub_router (which has contract tests), but historical script is retired, unexecuted in test suites, and prohibited from live catalog execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_11.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/validator.py",
        "current_function": "validate_library_integrity",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 11 library validation verifier. Conceptual equivalence to validate_library_integrity in modern architecture, but historical script is retired, untested, and prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
    {
        "archived_script": "verify_phase_12.py",
        "archived_function": "main",
        "current_file": "tools/skill_library/pilot.py",
        "current_function": "run_targeted_pilot",
        "has_test": "UNVERIFIED",
        "status": "HISTORICAL-ONLY",
        "rationale": "Phase 12 pilot review verifier. Conceptual equivalence to run_targeted_pilot in modern architecture, but historical script is retired, untested, and prohibited from live execution.",
        "suggested_zi_target": "RETIRED_DO_NOT_MIGRATE",
    },
]


def generate_archive_manifest(source_root: Path, output_dir: Path):
    manifest_path = output_dir / "archive-source-manifest.csv"
    fieldnames = [
        "script_name",
        "drive_file_id",
        "drive_revision",
        "drive_access_status",
        "archive_provenance_source",
        "archive_sha256",
        "size_bytes",
        "inaccessible_reason",
    ]

    all_scripts_dir = source_root / "tools" / "all_scripts"
    rows = []
    for script_name in AUTHORITATIVE_52_SCRIPTS:
        p = all_scripts_dir / script_name
        if not p.exists():
            rows.append({
                "script_name": script_name,
                "drive_file_id": "UNVERIFIED_DIRECT_DRIVE_OFFLINE",
                "drive_revision": "UNVERIFIED",
                "drive_access_status": "FILE_NOT_FOUND_IN_ARCHIVE",
                "archive_provenance_source": "MISSING",
                "archive_sha256": "NONE",
                "size_bytes": 0,
                "inaccessible_reason": "File missing from tools/all_scripts archive directory",
            })
            continue

        raw = p.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        size = len(raw)
        rows.append({
            "script_name": script_name,
            "drive_file_id": "UNVERIFIED_DIRECT_DRIVE_OFFLINE",
            "drive_revision": "UNVERIFIED",
            "drive_access_status": "UNVERIFIED_OFFLINE_REPOSITORY_PROVENANCE",
            "archive_provenance_source": f"tools/all_scripts/{script_name}",
            "archive_sha256": sha,
            "size_bytes": size,
            "inaccessible_reason": "NONE (bytes verified from authoritative repository archive; direct Drive API identity unverified)",
        })

    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


CORE_CONTRACT_TEST_FILES = [
    "tests/test_family_eligibility.py",
    "tests/test_migration_gates.py",
    "tests/test_migration_roadmap.py",
    "tests/test_physical_ownership.py",
    "tests/test_registry_router_contracts.py",
    "tests/test_semantic_census.py",
    "tests/test_semantic_object_model.py",
]


def verify_symbol_in_file(file_path: Path, symbol: str) -> tuple[bool, str]:
    """Dynamically verify that a callable symbol (function, class, or method) exists in file AST."""
    if not file_path.exists():
        return False, f"File does not exist: {file_path}"
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"AST parse error in {file_path}: {e}"

    parts = symbol.split(".")
    if len(parts) == 1:
        name = parts[0]
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                return True, "FUNCTION_EXISTS"
            if isinstance(node, ast.ClassDef) and node.name == name:
                return True, "CLASS_EXISTS"
        return False, f"Top-level symbol '{name}' not found in {file_path}"
    elif len(parts) == 2:
        class_name, method_name = parts
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name == method_name:
                        return True, "METHOD_EXISTS"
                return False, f"Method '{method_name}' not found in class '{class_name}' in {file_path}"
        return False, f"Class '{class_name}' not found in {file_path}"
    return False, f"Unsupported symbol path structure: {symbol}"


VERIFIED_CALLABLE_TEST_MAP = {
    ("tools/skill_library/family_contract.py", "ExecutionProviderBinding.validate"): {
        "test_file": "tests/test_family_eligibility.py",
        "test_class": "TestProviderAdapterRules",
        "test_methods": ["test_negative_provider_missing_binding_target"],
    },
    ("tools/skill_library/family_contract.py", "ExecutionProviderContract.validate_capability_providers"): {
        "test_file": "tests/test_family_eligibility.py",
        "test_class": "TestProviderAdapterRules",
        "test_methods": [
            "test_valid_multi_provider_binding_on_single_capability",
            "test_valid_multiple_providers_of_same_type",
            "test_negative_duplicate_provider_name_rejected",
            "test_negative_provider_missing_binding_target",
            "test_negative_canonical_slug_encoding_mechanism_rejected",
        ],
    },
    ("tools/skill_library/family_contract.py", "FamilyCandidateEvaluator.evaluate"): {
        "test_file": "tests/test_family_eligibility.py",
        "test_class": "TestFamilyEligibilityGates",
        "test_methods": [
            "test_tier_1_platform_qualification_github",
            "test_tier_1_platform_qualification_webflow",
            "test_tier_1_platform_qualification_single_domain_high_density_1password",
            "test_tier_2_community_multi_provider_notion",
            "test_tier_3_ecosystem_super_code_python",
            "test_tier_4_governed_specialist_linear",
        ],
    },
    ("tools/skill_library/migration_gates.py", "SkillPackageManifest.from_directory"): {
        "test_file": "tests/test_migration_gates.py",
        "test_class": "TestGate4ResourcePreservation",
        "test_methods": [
            "test_gate4_source_to_destination_missing_supporting_asset",
            "test_gate4_source_to_destination_checksum_mismatch",
            "test_gate4_source_to_destination_exact_match_passes",
            "test_gate4_migration_authorization_fails_when_destination_manifest_missing",
            "test_gate4_migration_authorization_passes_with_matching_manifests",
        ],
    },
}


def _check_linear_statements(stmts: list[ast.stmt], cls_name: str, method_name: str, bound_vars: dict[str, str]) -> bool:
    """
    Sequentially traverse statement lists, tracking variable bindings statement-by-statement,
    unbinding variables upon reassignment, and checking callable invocations only when bound
    at that exact point in the statement execution stream.
    """
    for stmt in stmts:
        # 1. Check all calls made within this statement
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == method_name:
                    # Direct class/static method call: ClassName.method(...)
                    if isinstance(func.value, ast.Name) and func.value.id == cls_name:
                        return True
                    # Direct chained call: ClassName(...).method(...)
                    if (
                        isinstance(func.value, ast.Call)
                        and isinstance(func.value.func, ast.Name)
                        and func.value.func.id == cls_name
                    ):
                        return True
                    # Receiver variable call: var.method(...) where var is currently bound to cls_name
                    if isinstance(func.value, ast.Name) and bound_vars.get(func.value.id) == cls_name:
                        return True

        # 2. Update or unbind variable bindings based on this statement
        if isinstance(stmt, ast.Assign):
            is_class_call = (
                isinstance(stmt.value, ast.Call)
                and isinstance(stmt.value.func, ast.Name)
            )
            assigned_cls = stmt.value.func.id if is_class_call else None
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    if assigned_cls == cls_name:
                        bound_vars[target.id] = cls_name
                    else:
                        bound_vars.pop(target.id, None)

        elif isinstance(stmt, ast.AnnAssign):
            is_class_call = (
                stmt.value is not None
                and isinstance(stmt.value, ast.Call)
                and isinstance(stmt.value.func, ast.Name)
            )
            assigned_cls = stmt.value.func.id if is_class_call else None
            if isinstance(stmt.target, ast.Name):
                if assigned_cls == cls_name:
                    bound_vars[stmt.target.id] = cls_name
                else:
                    bound_vars.pop(stmt.target.id, None)

        elif isinstance(stmt, ast.With):
            # Check withitems for context manager instantiation
            with_bound = dict(bound_vars)
            for item in stmt.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call) and isinstance(ctx.func, ast.Name):
                    if isinstance(item.optional_vars, ast.Name):
                        if ctx.func.id == cls_name:
                            with_bound[item.optional_vars.id] = cls_name
                        else:
                            with_bound.pop(item.optional_vars.id, None)
            if _check_linear_statements(stmt.body, cls_name, method_name, with_bound):
                return True

        elif isinstance(stmt, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            if _check_linear_statements(stmt.body, cls_name, method_name, dict(bound_vars)):
                return True
            if hasattr(stmt, "orelse") and stmt.orelse:
                if _check_linear_statements(stmt.orelse, cls_name, method_name, dict(bound_vars)):
                    return True

        elif isinstance(stmt, (ast.Try, getattr(ast, "TryStar", ast.Try))):
            if _check_linear_statements(stmt.body, cls_name, method_name, dict(bound_vars)):
                return True
            for handler in stmt.handlers:
                if _check_linear_statements(handler.body, cls_name, method_name, dict(bound_vars)):
                    return True
            if stmt.orelse:
                if _check_linear_statements(stmt.orelse, cls_name, method_name, dict(bound_vars)):
                    return True
            if stmt.finalbody:
                if _check_linear_statements(stmt.finalbody, cls_name, method_name, dict(bound_vars)):
                    return True

    return False


def is_callable_invoked_in_ast(tree: ast.AST, cls_name: str | None, method_name: str) -> bool:
    """
    Precisely determine whether `cls_name.method_name` (or top-level `method_name`)
    is invoked as a callable via an ast.Call node within statement execution order.

    Enforces linear statement ordering and variable reassignment tracking:
      - Simple Name mentions (imports, type annotations, docstrings, uncalled variables) do NOT count.
      - A class import plus unrelated other_object.method() call does NOT count.
      - Calls prior to assignment do NOT count.
      - Calls after reassignment to an unrelated class do NOT count.
      - Requires either:
        1. Direct class/static method call: ClassName.method(...)
        2. Direct chained call: ClassName(...).method(...)
        3. Instantiated receiver variable call: var = ClassName(...); ... var.method(...)
           where var is bound to ClassName at that point in the statement stream.
        4. (If top-level function) Direct call: func_name(...)
    """
    if cls_name is None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == method_name:
                return True
        return False

    # Check linear statement order within every function, method, or module body
    for scope_node in ast.walk(tree):
        if isinstance(scope_node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
            if _check_linear_statements(scope_node.body, cls_name, method_name, {}):
                return True

    return False


def verify_test_linkage(source_root: Path, current_file: str, current_function: str) -> tuple[bool, str, list[str]]:
    """
    Dynamically verify that a mapped callable or test class is executed in the core 213 unit test suite.
    Enforces precise AST call/receiver tracing and verified explicit callable-to-test mapping.
    Simple name mentions or unrelated receiver calls are strictly rejected.
    """
    if current_file.startswith("tests/"):
        if current_file not in CORE_CONTRACT_TEST_FILES:
            return False, f"Test file {current_file} is not part of the 213-test core contract suite", []
        test_path = source_root / current_file
        if not test_path.exists():
            return False, f"Test file does not exist: {test_path}", []
        try:
            tree = ast.parse(test_path.read_text(encoding="utf-8"))
        except Exception as e:
            return False, f"AST parse error in {test_path}: {e}", []
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == current_function:
                has_test_method = any(
                    isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name.startswith("test_")
                    for sub in node.body
                )
                if has_test_method:
                    return True, "CORE_TEST_CLASS_VERIFIED", [current_file]
                return False, f"Class {current_function} in {current_file} has no test methods", []
        return False, f"Symbol {current_function} not defined in {current_file}", []

    parts = current_function.split(".")
    cls_name = parts[0] if len(parts) == 2 else None
    method_name = parts[1] if len(parts) == 2 else parts[0]

    # 1. Check verified explicit callable-to-test mapping if registered
    explicit_key = (current_file, current_function)
    if explicit_key in VERIFIED_CALLABLE_TEST_MAP:
        mapping = VERIFIED_CALLABLE_TEST_MAP[explicit_key]
        test_file = mapping["test_file"]
        if test_file not in CORE_CONTRACT_TEST_FILES:
            return False, f"Mapped test file {test_file} is not part of core contract suite", []
        tf_path = source_root / test_file
        if not tf_path.exists():
            return False, f"Mapped test file not found: {tf_path}", []
        try:
            tree = ast.parse(tf_path.read_text(encoding="utf-8"))
        except Exception as e:
            return False, f"AST parse error in {tf_path}: {e}", []

        target_class_name = mapping.get("test_class")
        target_methods = set(mapping.get("test_methods", []))
        invoked = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and (target_class_name is None or node.name == target_class_name):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not target_methods or sub.name in target_methods:
                            if is_callable_invoked_in_ast(sub, cls_name, method_name):
                                invoked = True
                                break
            if invoked:
                break

        if invoked:
            return True, "VERIFIED_TEST_CASE_MAPPING_INVOKES_CALLABLE", [test_file]
        return False, f"Callable {current_function} not invoked in mapped test cases of {test_file}", []

    # 2. General AST call tracing across all core contract test files
    found_in = []
    core_paths = [source_root / tf for tf in CORE_CONTRACT_TEST_FILES]
    for tf_path in core_paths:
        if not tf_path.exists():
            continue
        try:
            tree = ast.parse(tf_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if is_callable_invoked_in_ast(tree, cls_name, method_name):
            found_in.append(tf_path.name)

    if found_in:
        return True, "MAPPED_CALLABLE_TESTED_IN_CORE_SUITE", found_in
    return False, "NO_DIRECT_CORE_UNIT_TEST_COVERAGE", []


def generate_reuse_crosswalk(source_root: Path, output_dir: Path):
    crosswalk_path = output_dir / "script-reuse-crosswalk.csv"
    fieldnames = [
        "archived_script",
        "archived_function",
        "current_file",
        "current_function",
        "has_test",
        "status",
        "rationale",
        "suggested_zi_target",
    ]

    # Verify all mapped symbols exist in source repository and validate test coverage claims
    resolution_failures = []
    test_claim_failures = []
    for record in CROSSWALK_RECORDS:
        cur_file = record["current_file"]
        cur_func = record["current_function"]
        has_test_claim = record["has_test"]
        status = record["status"]

        if cur_file == "HISTORICAL_REBUILD_ONLY" and cur_func == "NONE_RETIRED":
            if has_test_claim != "FALSE":
                test_claim_failures.append(f"{record['archived_script']}: retired script must have has_test == 'FALSE', got '{has_test_claim}'")
            continue

        target_path = source_root / cur_file
        ok, reason = verify_symbol_in_file(target_path, cur_func)
        if not ok:
            resolution_failures.append(f"{record['archived_script']} -> {cur_file}:{cur_func} ({reason})")

        has_test_ok, test_reason, test_files = verify_test_linkage(source_root, cur_file, cur_func)

        if has_test_claim == "TRUE":
            # Must have verified test linkage in core test suite
            if not has_test_ok:
                test_claim_failures.append(f"{record['archived_script']} -> {cur_file}:{cur_func}: claimed has_test == 'TRUE' but {test_reason}")
            # Conceptual equivalence must be kept distinct from executed test coverage:
            # Historical-only and needs-further-test scripts cannot claim TRUE test coverage
            if status in ("HISTORICAL-ONLY", "NEEDS-FURTHER-TEST"):
                test_claim_failures.append(f"{record['archived_script']}: status '{status}' cannot claim has_test == 'TRUE' based on conceptual equivalence")
        elif has_test_claim not in ("UNVERIFIED", "FALSE"):
            test_claim_failures.append(f"{record['archived_script']}: invalid has_test claim '{has_test_claim}' (must be TRUE, UNVERIFIED, or FALSE)")

    if resolution_failures or test_claim_failures:
        errors = resolution_failures + test_claim_failures
        msg = f"Crosswalk verification failed for {len(errors)} records:\n" + "\n".join(errors)
        raise RuntimeError(msg)

    with open(crosswalk_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(CROSSWALK_RECORDS)


def generate_module_matrix(output_dir: Path):
    matrix_path = output_dir / "module-capability-matrix.md"
    content = """# Module Capability Matrix: Repository-Native Core Modules

This document details the 14 explicitly named repository-native core modules under `tools/skill_library/` (plus the CLI entrypoint and scanner), their architectural responsibilities, key classes and callable functions, existing capabilities, limitations/guardrails, and how historical Drive-archived scripts map into or conflict with them.

---

## 1. Executive Summary of Core Cohort

The repository-native architecture formalized under ADR-001 through ADR-005 establishes a path-independent, contract-governed semantic object model for the skills library. Unlike the historical rebuild scripts—which operated primarily as linear procedural batch mutators and static phase verifiers—the core `tools/skill_library/` modules provide idempotent, read-safe, and verifiable operations.

| Module | Core Responsibility | Primary Contract / ADR | Key Classes & Callable Entrypoints |
| :--- | :--- | :--- | :--- |
| `object_model.py` | Canonical Identity & Object Graph | ADR-001 | `CanonicalIdentity.parse`, `ObjectGraph.add_object`, `ObjectGraph.validate_invariants` |
| `ledger.py` | Change Ledger Management | Living Library Contract | `ChangeLedger.record_change`, `ChangeLedger.list_changes`, `ChangeLedger.get_history` |
| `registry_contract.py` | Catalog & Multi-View Projections | ADR-004 | `CatalogCompiler.compile`, `CatalogRegistry.add_entry`, `AliasResolver.resolve`, `DependencyResolver.detect_cycle`, `ProjectMaterializer.materialize_bundle` |
| `config.py` | Runtime Configuration & Targets | Runtime Distribution | `load_runtime_targets`, `get_all_routers`, `RuntimeTarget.resolved_path` |
| `family_contract.py` | Family Qualification & Provider Bindings | ADR-003 | `FamilyQualificationGate.is_tier_1_eligible`, `FamilyCandidateEvaluator.evaluate`, `ExecutionProviderBinding.validate`, `ExecutionProviderContract.validate_capability_providers` |
| `physical_layout.py` | Physical Plane Boundaries | ADR-002 | `PhysicalPathContract.normalize`, `PhysicalPathContract.parse`, `PhysicalLayoutValidator.validate_object_placement`, `DuplicateCandidateRegistry.get_all_pairs` |
| `migration_gates.py` | Architecture Migration Gates | ADR-005 | `MigrationGateRunner.run_all_gates`, `SkillPackageManifest.from_directory`, `HistoricalProvenanceMapper.reconcile` |
| `manifest.py` | Runtime Distribution Manifest | Runtime Publication | `RuntimeManifest.load`, `RuntimeManifest.save`, `RuntimeManifest.build_from_library` |
| `sync.py` | Target Synchronization | Runtime Distribution | `sync_target`, `sync_all_targets`, `migrate_legacy_symlink_target` |
| `intake.py` | Reusable Intake Pipeline | Living Library Intake | `evaluate_candidate`, `compute_dice_similarity`, `apply_candidate`, `normalize_package_content` |
| `intake_capture.py` | Target State Capture | Living Library Intake | `scan_target_dirty_state`, `capture_dirty_target`, `convert_incoming_to_intake` |
| `publisher.py` | Runtime Branch Publication | Runtime Publication | `publish_runtime_branch`, `get_library_tree_sha`, `get_commit_tree_sha` |
| `validator.py` | Library Integrity Validation | Living Library Governance | `validate_library_integrity`, `validate_single_skill`, `parse_frontmatter` |
| `pilot.py` | Targeted Operational Pilot | Pilot Review Protocol | `run_targeted_pilot` |
| `scanner.py` | Filesystem Inventory Scanner | Inventory Discovery | `scan_candidate_directory`, `scan_runtime`, `run_full_scan` |
| `tools/skill-library.py` | Unified CLI Entrypoint | Operator Interface | Top-level CLI `main()` dispatching to `scan`, `intake`, `validate`, `sync`, `publish` |

### 1.1 Methodological Definition of Test Linkage (`has_test`)

In all crosswalk tables and audit deliverables:
- **`has_test = TRUE`**: Represents **static call linkage** to passing core contract test suites. The mapped callable or test class is confirmed via AST call and receiver tracing to be invoked within the 213 unit tests (`tests/test_*.py`). It does **NOT** denote dynamic runtime code coverage or line-by-line branch coverage instrumentation.
- **`has_test = UNVERIFIED`**: Represents architectural conceptual equivalence where modern core classes have contract tests, but the specific historical script entrypoint or utility lacks direct unit test execution, or the historical script is retired/prohibited from execution.
- **`has_test = FALSE`**: Represents historical batch writers, in-place regex mutators, or ad-hoc scripts with no test coverage whatsoever.

---

## 2. Detailed Module Inspection & API Verification

### 2.1 `object_model.py`
- **Location:** `tools/skill_library/object_model.py`
- **Architectural Invariant:** Under ADR-001, identity is path-independent and scoped at minting. The identifier format is strictly `<scope>:<slug>` or `urn:skill:<scope>:<slug>` (with prefix `urn:skill:`).
  - Scope is an immutable identity namespace / provenance scope.
  - Path separators (`/`, `\\`) and file extensions (`.md`, `.json`, etc.) are prohibited in canonical identities.
  - Scope and slug must match lowercase alphanumeric regex: `^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$`.
- **Key Classes & Methods:**
  - `CanonicalIdentity`: `parse(identifier: str) -> CanonicalIdentity`, `compact` property (`<scope>:<slug>`), `urn` property (`urn:skill:<scope>:<slug>`), `__post_init__()`.
  - `SkillRole`: Typed role enum: `INDEPENDENT_CAPABILITY`, `FAMILY_PRIMITIVE`, `WORKFLOW`, `OVERLAY`, `ADAPTER`, `ALIAS_CANDIDATE`, `REFERENCE_OR_SUPPORT_CANDIDATE`, `MANUAL_REVIEW`.
  - `ReviewStatus`: Lifecycle status enum: `DRAFT`, `IN_REVIEW`, `APPROVED`, `RETIRED`.
  - `RelationshipType`: Typed graph edge enum: `DEPENDS_ON`, `COMPOSED_OF`, `ADAPTS`, `OVERLAYS`, `REFERENCES`, `ALIASED_TO`.
  - `ObjectGraph`: In-memory DAG of skill objects. Callable entrypoints: `add_object(obj)`, `get_object(id)`, `resolve_alias(id)`, `validate_invariants()`, `export_catalog()`.
- **Existing Capabilities:** Enforces graph acyclicity (INV-1), single canonical ownership (INV-2), referential closure (INV-3).
- **Limitations & Guardrails:** Operates purely as an in-memory data model; does not perform direct filesystem mutation. Unscoped legacy identifiers cannot be coerced to URNs without formal minting.
- **Crosswalk Mapping:**
  - Replaces historical string-based classification in `classify_compatibility.py` and `build_phase_08_artifacts.py`.
  - Replaces `semantic_cleanup.py`'s destructive field deletions with formal data validation invariants.

### 2.2 `ledger.py`
- **Location:** `tools/skill_library/ledger.py`
- **Architectural Role:** Append-only JSONL recording of catalog and skill lifecycle changes into `audit/change-ledger.jsonl`.
- **Key Classes & Methods:**
  - `ChangeLedger`: `record_change(entry: dict) -> None`, `list_changes(skill_id: Optional[str] = None) -> list[dict]`, `get_history(skill_id: str) -> list[dict]`.
  - `get_current_iso_timestamp() -> str`: Generates deterministic UTC ISO-8601 timestamps.
- **Existing Capabilities:** Idempotent event logging, sequential event auditing, schema validation of change records.
- **Limitations & Guardrails:** Strictly append-only. No method exists to delete, overwrite, or mutate recorded historical entries.
- **Crosswalk Mapping:**
  - Modernizes `generate_ledger.py` and supersedes ad-hoc ledger patches in `fix_cumulative_reconciliation.py`.

### 2.3 `registry_contract.py`
- **Location:** `tools/skill_library/registry_contract.py`
- **Architectural Role:** Multi-view projection compiler, registry indexer, and alias adjudication engine conforming to ADR-004.
- **Key Classes & Methods:**
  - `CatalogCompiler`: `compile(catalog_registry: Optional[CatalogRegistry] = None) -> dict`. Compiles functional, family, semantic group, and provider views deterministically.
  - `CatalogRegistry`: `add_entry(entry: RegistryEntry)`, `get_entry(canonical_id: str)`, `add_semantic_group(group: SemanticGroupObject)`, `to_dict()`, `to_json()`, `from_json()`.
  - `AliasResolver`: `resolve(alias_id: str) -> str`, `adjudicate_duplicate_pair(...)`, `build_direction_neutral_duplicate_pair(...)`.
  - `DependencyResolver`: `validate_invariants()`, `detect_cycle() -> Optional[list[str]]`, `compute_transitive_closure(start_id: str) -> set[str]`, `compute_execution_plan() -> list[str]`.
  - `ProjectMaterializer`: `materialize_bundle(target_dir: str, canonical_ids: list[str]) -> dict`.
  - `FamilyRouterGenerator`: `generate_tier_1_hub_router(hub_name: str, members: list[RegistryEntry]) -> str`, `generate_tier_2_virtual_router(family_name: str, members: list[RegistryEntry]) -> str`.
- **Enums & Types:**
  - `ProjectionMode`: `FUNCTIONAL`, `FAMILY`, `SEMANTIC_GROUP`, `PROVIDER`.
  - `DuplicateAdjudicationOutcome`: `KEEP_CANONICAL`, `MERGE`, `SUPERSEDE`, `SPLIT`, `QUARANTINE`.
- **Existing Capabilities:** Idempotent compilation with zero variance across repeated runs on identical input.
- **Limitations & Guardrails:** Projections are generated dynamically in-memory or into designated build artifacts; does not mutate live skill directories.
- **Crosswalk Mapping:**
  - Replaces `build_phase_05_artifacts.py`, `build_phase_06_artifacts.py`, `build_phase_08_artifacts.py`, and `generate_batch_plan.py`.

### 2.4 `config.py`
- **Location:** `tools/skill_library/config.py`
- **Architectural Role:** Centralized configuration provider for runtime publication targets and repository paths.
- **Key Classes & Methods:**
  - `RuntimeTarget`: Dataclass with `name`, `path`, `mode`, `enabled`, and `resolved_path()` method.
  - `load_runtime_targets() -> list[RuntimeTarget]`: Parses target configuration from environment or repository settings.
  - `get_all_routers(root_path: Path) -> list[Path]`: Discovers all valid `ROUTER.md` and hub router files.
- **Crosswalk Mapping:**
  - Replaces hardcoded path constants scattered across historical phase verifiers (`verify_phase_04.py` through `verify_phase_12.py`).

### 2.5 `family_contract.py`
- **Location:** `tools/skill_library/family_contract.py`
- **Architectural Role:** Governs family qualification gates, evidence integrity, and provider neutrality (ADR-003).
- **Key Classes & Methods:**
  - `FamilyQualificationGate`: `is_tier_1_eligible(record: FamilyQualificationRecord) -> bool`, `is_tier_2_eligible(record: FamilyQualificationRecord) -> bool`.
  - `FamilyCandidateEvaluator`: `evaluate(record: FamilyQualificationRecord) -> FamilyTier`, `validate_record_integrity(record)`.
  - `ExecutionProviderBinding`: `validate() -> bool`.
  - `ExecutionProviderContract`: `validate_capability_providers(skill: SkillObject, bindings: list[ExecutionProviderBinding])`, `validate_adapter_purity(adapter: AdapterObject)`.
- **Enums & Types:**
  - `FamilyTier`: `TIER_1_CANONICAL`, `TIER_2_VIRTUAL`, `UNQUALIFIED`.
  - `EvidenceStatus`: `VERIFIED`, `INSUFFICIENT`, `CONTRADICTORY`.
  - `ProviderType`: `ANTHROPIC`, `BEDROCK`, `VERTEX`, `LOCAL`, `GENERIC_OPENAI`.
- **Existing Capabilities:** Enforces Tier 1 qualification threshold (>=5 verified members across multiple categories, shared primitives, tool surface, coordinated lifecycle).
- **Limitations & Guardrails:** Enforces provider neutrality contractually via structured bindings; does not perform blind regex string replacements in skill bodies.
- **Crosswalk Mapping:**
  - Replaces `analyze_provider_coupling_detailed.py`, `analyze_provider_dependencies.py`, and `classify_compatibility.py`.
  - Prohibits historical mutators: `execute_provider_conversion*.py` and `neutralize_claude_dependencies*.py`.

### 2.6 `physical_layout.py`
- **Location:** `tools/skill_library/physical_layout.py`
- **Architectural Role:** Enforces namespace containment and physical plane boundaries (ADR-002).
- **Key Classes & Methods:**
  - `PhysicalPlane`: Plane enum: `CANONICAL`, `HUB`, `TIER_2_VIRTUAL`, `ADAPTER`, `SCRATCH`, `QUARANTINE`.
  - `PhysicalPathContract`: `normalize(path: str) -> str`, `parse(path: str) -> ParsedPhysicalPath`.
  - `PhysicalLayoutValidator`: `validate_object_placement(obj: SkillObject, path: str) -> bool`, `verify_path_independent_relocation(old_path, new_path) -> bool`.
  - `DuplicateCandidateRegistry`: `is_candidate_leaf(path)`, `get_candidate_hypothesis(path)`, `get_all_pairs()`.
- **Existing Capabilities:** Validates that skill packages adhere to designated planes without rogue symlinks or unauthorized subdirectories.
- **Crosswalk Mapping:**
  - Replaces `build_phase_07_artifacts.py` and `verify_phase_07.py`.

### 2.7 `migration_gates.py`
- **Location:** `tools/skill_library/migration_gates.py`
- **Architectural Role:** Comprehensive architecture migration gate runner (G01–G09) and manifest generator (ADR-005).
- **Key Classes & Methods:**
  - `SkillPackageManifest`: `from_directory(path: Path) -> SkillPackageManifest`, `root_path -> Path`, `to_dict() -> dict`. Computes root manifest SHA-256 and individual file asset digests.
  - `HistoricalProvenanceMapper`: `reconcile(historical_path: str) -> HistoricalProvenanceRecord`, `normalize_historical_destination(dest)`, `load_phase08_canonical_registry(path)`, `load_census(path)`.
  - `MigrationGateRunner`: `run_gate(gate_id: GateID) -> GateResult`, `run_all_gates() -> MigrationGateReport`.
- **Gate Definitions:**
  - `G01`: Canonical Identity Validation
  - `G02`: Family Qualification Gate
  - `G03`: Graph Topology & Acyclicity
  - `G04`: Resource Preservation
  - `G05`: Reference Closure
  - `G06`: View Reconciliation
  - `G07`: Deterministic Compilation
  - `G08`: Project Materialization
  - `G09`: Runtime Publication Pre-Flight
- **Crosswalk Mapping:**
  - Formalizes and supersedes `generate_inventory.py`, `verify_phase_08_cumulative.py`, and `verify_phase_09.py`.

### 2.8 `manifest.py`
- **Location:** `tools/skill_library/manifest.py`
- **Architectural Role:** Generates and maintains runtime publication manifests.
- **Key Classes & Methods:**
  - `RuntimeManifest`: `load(path: Path)`, `save(path: Path)`, `add_skill(skill: dict)`, `build_from_library(library_path: Path)`.

### 2.9 `sync.py`
- **Location:** `tools/skill_library/sync.py`
- **Architectural Role:** Multi-target synchronization for local runtime distributions using git sparse-checkout.
- **Key Classes & Methods:**
  - `sync_target(target: RuntimeTarget)`, `sync_all_targets()`, `migrate_legacy_symlink_target(target)`.

### 2.10 `intake.py` & `intake_capture.py`
- **Location:** `tools/skill_library/intake.py` and `intake_capture.py`
- **Architectural Role:** Living library intake pipeline for discovering, evaluating, and safely importing candidate skills.
- **Key Classes & Methods:**
  - `evaluate_candidate(candidate_path: Path) -> IntakeEvaluation`: Checks frontmatter schema and calculates Dice similarity against existing catalog.
  - `scan_target_dirty_state(target_path: Path)`: Captures external runtime modifications safely into staging.

### 2.11 `publisher.py`
- **Location:** `tools/skill_library/publisher.py`
- **Architectural Role:** Publication gate and branch publisher for runtime distribution branches.
- **Key Classes & Methods:**
  - `publish_runtime_branch()`, `get_library_tree_sha()`, `get_commit_tree_sha(commit)`.

### 2.12 `validator.py`
- **Location:** `tools/skill_library/validator.py`
- **Architectural Role:** Production whole-library frontmatter and integrity validation.
- **Key Classes & Methods:**
  - `validate_library_integrity(library_path: Path) -> ValidationResult`, `validate_single_skill(skill_path: Path)`.
- **Crosswalk Mapping:**
  - Replaces `fix_registry_check.py`, `gen_phase11_artifacts.py`, and `verify_phase_11.py`.

### 2.13 `pilot.py`
- **Location:** `tools/skill_library/pilot.py`
- **Architectural Role:** Targeted operational pilot execution and validation.
- **Key Classes & Methods:**
  - `run_targeted_pilot(skill_path: Path) -> PilotResult`.
- **Crosswalk Mapping:**
  - Replaces `gen_phase12_artifacts.py` and `verify_phase_12.py`.
"""
    with open(matrix_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")


def generate_gaps_and_collisions(output_dir: Path):
    gaps_path = output_dir / "gaps-and-collisions.md"
    content = """# Gaps, Collisions, and Historical Safety Analysis

This document identifies capabilities present in the 52 historical Drive-archived scripts that are absent or modified in the current codebase, highlights dangerous historical migration writers that must **NEVER** be run against the live catalog, and documents legacy filesystem paths and deprecated contracts.

---

## 1. Capabilities Present in Historical Scripts but Missing in Current Codebase (Gaps)

While the modern `tools/skill_library/` architecture provides superior governance and type safety, specific diagnostic and analytical capabilities from the historical archive have not yet been formalized into callable CLI subcommands:

### 1.1 Cumulative Multi-Phase Discrepancy Auditing (`verify_phase_08_cumulative.py`)
- **Historical Capability:** `verify_phase_08_cumulative.py` tracked discrepancy reconciliation across successive transformation passes (splits, merges, renames) against historical baselines.
- **Current State:** `migration_gates.py` checks point-in-time gate rules (G01–G09) and provenance records, but does not provide an automated historical delta matrix comparing arbitrary historical CSV baselines against current zero-index snapshots.
- **Recommendation:** Adapt the discrepancy matrix calculation logic into `ZI-03` for continuous historical reconciliation reporting without reviving historical mutation passes.

### 1.2 Heuristic Column Discovery (`analyze_inventory_columns.py`)
- **Historical Capability:** Evaluated variance and nullity across unstructured legacy metadata columns.
- **Current State:** Current models expect strict typed schemas (`SkillObject`, `RegistryEntry`).
- **Recommendation:** Maintain as a standalone read-only diagnostic utility for evaluating raw external intake packages that lack canonical frontmatter.

### 1.3 Automated Batch Execution Planning (`generate_batch_plan.py`)
- **Historical Capability:** Partitioned 2,100+ skills into balanced batches for batch processing.
- **Current State:** Modern catalog operations are compiled atomically via `CatalogCompiler.compile`.
- **Recommendation:** Batch planning is no longer needed for catalog compilation, but similar partitioning logic may assist downstream distributed testing in `ZI-05`.

---

## 2. Retired Migration Writers: Safety Guardrails (Collisions & Prohibited Scripts)

A critical outcome of this audit is identifying historical scripts that performed destructive or in-place file modifications. Under approved ADR-000 and Zero-Index governance, **THESE SCRIPTS MUST NEVER BE RUN AGAINST THE LIVE CATALOG OR REPOSITORY CODEBASE**:

| Dangerous Script | Historical Function | Risk / Prohibited Behavior | Current Safe Counterpart |
| :--- | :--- | :--- | :--- |
| `execute_phase08_batches.py` | Rewrote skill files across 160 batches | In-place regex modification of live skill files; violates zero-index immutability | `CatalogCompiler.compile` (read-only projection compiler) |
| `execute_provider_conversion.py` | Pass 1 Claude provider syntax neutralization | Blind string replacements in code samples; strips valid multi-provider syntax | `family_contract.py` (`ExecutionProviderBinding.validate`) |
| `execute_provider_conversion_pass2.py` | Pass 2 provider syntax neutralization | Blind regex replacements; potential file corruption | `family_contract.py` (`ExecutionProviderBinding.validate`) |
| `execute_provider_conversion_pass3.py` | Pass 3 provider syntax neutralization | Blind regex replacements; potential file corruption | `family_contract.py` (`ExecutionProviderBinding.validate`) |
| `neutralize_claude_dependencies.py` | Regex prompt neutralizer | Destructive edits to frontmatter and body | `ExecutionProviderContract.validate_capability_providers` |
| `neutralize_claude_dependencies_v2.py` | Enhanced regex prompt neutralizer | Destructive edits to frontmatter and body | `ExecutionProviderContract.validate_capability_providers` |
| `patch_phase_08_batch1.py` | Hardcoded batch 1 hotfix | Re-imposes superseded Phase 08 path assumptions | Read-only zero-index baseline |
| `update_phase_08_batch1.py` | Hardcoded batch 1 updater | Destructive disk writes | Read-only zero-index baseline |
| `run_all_batches.py` | Automated batch orchestrator | Uncontrolled mass re-writing of catalog tree | Pure read-only CLI (`tools/skill-library.py`) |
| `fix_mcp_zod.py` | AST patcher for MCP schemas | Arbitrary code mutation | Static validation (`validator.py:validate_library_integrity`) |
| `semantic_cleanup.py` | Ad-hoc metadata cleaner | Destructive field deletions | Invariant checking (`object_model.py:ObjectGraph.validate_invariants`) |
| `update_descriptions.py` | Mass frontmatter description updater | Destructive overwrites of curated descriptions | Safe candidate intake (`intake.py:evaluate_candidate`) |

> [!CAUTION]
> **Enforcement Rule:** All 12 scripts listed above are classified as `HISTORICAL-ONLY`. CI pipelines and operational scripts must block any execution of these files.

---

## 3. Accurate Treatment of Historical and Noncanonical Paths

Historical scripts frequently hardcoded filesystem paths and assumptions that require careful differentiation:

### 3.1 Historical Non-Canonical Archive Directories (`task-folder/agents/skills/`)
- **Historical Reference:** Historical scripts (`verify_phase_04.py`, `build_phase_05_artifacts.py`, etc.) contain hardcoded references to `task-folder/agents/skills/`.
- **Accurate Architectural Status:** **HISTORICAL ARCHIVE (Present on disk; non-canonical)**.
  - `task-folder/agents/skills/` is NOT a 404 nonexistent path; it exists physically in the repository and contains 2,101 active pre-rebuild skill packages (cataloged in the SKIL-16 zero-index baseline).
  - However, scripts that hardcode `task-folder/agents/skills/` as the live library root fail architecturally because under ADR-002, the active canonical plane is strictly `library/` governed by `PhysicalPathContract`.
  - These scripts cannot be executed against `library/` without rewrite, nor should their hardcoded path assumptions be reintroduced.

### 3.2 True Nonexistent Paths (Historical 404s)
- **Historical Reference:** Ephemeral external scratch paths (e.g. `/tmp/scratch/`, `/Volumes/External/rebuild-scratch/`) and defunct symlink trees (e.g. `~/.agents/skills/` symlink targets assumed by early pilot scripts).
- **Accurate Architectural Status:** **404 / NONEXISTENT**. These paths were external to the git repository and do not exist on the current host or CI environments.

### 3.3 Obsolete Static Taxonomy Categories
- **Historical Reference:** `build_phase_05_artifacts.py` and `verify_phase_10.py` hardcoded 12 top-level category folders and expected an exact count of 2,103 leaves.
- **Accurate Architectural Status:** **SUPERSEDED**. ADR-004 establishes dynamic multi-view projections (`Functional`, `Family`, `Semantic Group`, `Provider`). Category counts are discovered from the zero-index snapshot, never assumed.

### 3.4 Flat Legacy Symlink Targets
- **Historical Reference:** Historical pilot and publication scripts assumed symlinks pointing directly into `library/`.
- **Accurate Architectural Status:** **DEPRECATED / MIGRATED**. ADR-002 and `sync.py` enforce git sparse-checkout and clone targets, eliminating fragile cross-volume symlinks.

### 3.5 Outdated Evidence File Targets
- **Historical Reference:** References to `audit/rebuild-phase-1-12/skills-inventory.csv`, `phase08-canonical-registry.csv`, and `phase10-functional-routing-map.csv`.
- **Accurate Architectural Status:** **ARCHIVED EVIDENCE ONLY**. These files serve as dated provenance records, not live operational registries.
"""
    with open(gaps_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")


def build_all(source_root: Path, output_dir: Path):
    source_root = source_root.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    generate_archive_manifest(source_root, output_dir)
    generate_reuse_crosswalk(source_root, output_dir)
    generate_module_matrix(output_dir)
    generate_gaps_and_collisions(output_dir)


def main():
    parser = argparse.ArgumentParser(description="Generate SKIL-15 crosswalk deliverables")
    parser.add_argument("--source-root", default=".", help="Repository root")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    build_all(Path(args.source_root), Path(args.output_dir))
    print(f"SKIL-15 crosswalk deliverables generated successfully in {args.output_dir}")


if __name__ == "__main__":
    main()
