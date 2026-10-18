"""
Unit and Regression Test Suite for REV-131 / ADR-005:
Architecture Validation and Migration Gates.

Verifies:
  - Gate 1: Canonical Identity Uniqueness & Structure (INV-2, INV-6)
  - Gate 2: Family Qualification & Boundary Adherence (INV-8, Tier 1 vs Tier 2, Duplicate Neutrality)
  - Gate 3: Graph Topology, Acyclicity & Alias Purity (INV-1, INV-3, INV-4, INV-5)
  - Gate 4: Resource & Asset Preservation (Zero Data Loss, SKILL.md, Support Assets)
  - Gate 5: Reference Closure & Dependency Completeness (INV-7)
  - Gate 6: Generated-View Reconciliation & Router Integrity (Multi-View, Relative Links, Badging)
  - Gate 7: Deterministic Compilation & Idempotency (INV-10)
  - Gate 8: Project Materialization Completeness & Collision-Free Naming (INV-9)
  - Gate 9: Runtime Publication Pre-Flight & Target Compatibility (Clean Protected Assets)
  - Historical Phase 01–12 Provenance Reconciliation Architecture
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure tools directory is in sys.path
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.object_model import (
    CanonicalIdentity,
    CanonicalIdentityError,
    CapabilityObject,
    FamilyObject,
    InvariantViolationError,
    ObjectGraph,
    OverlayObject,
    PrimitiveObject,
    RelationshipType,
    ReviewStatus,
    SkillRole,
    WorkflowObject,
)
from skill_library.family_contract import (
    EvidenceStatus,
    FamilyEligibilityError,
    FamilyQualificationGate,
    FamilyQualificationRecord,
    FamilyTier,
)
from skill_library.registry_contract import (
    CatalogCompiler,
    CatalogRegistry,
    DuplicateAdjudicationOutcome,
    FamilyRouterGenerator,
    ProjectMaterializer,
    ProjectionMode,
    RegistryEntry,
)
from skill_library.migration_gates import (
    GateID,
    GateResult,
    GateStatus,
    GateViolation,
    SkillFileAsset,
    SkillPackageManifest,
    compare_package_manifests,
    HistoricalProvenanceMapper,
    HistoricalProvenanceRecord,
    MigrationGateEvaluator,
    MigrationGateReport,
    MigrationGateRunner,
    ProvenanceReconciliationReport,
    ProvenanceType,
)


def _build_test_registry(entries: list[RegistryEntry]) -> CatalogRegistry:
    """Helper to build a CatalogRegistry with a list of entries without invoking validation in add_entry."""
    reg = CatalogRegistry(commit_sha="test-sha", generated_at="2026-10-17T00:00:00Z")
    for e in entries:
        reg.skills[e.canonical_id] = e
    return reg


class TestHistoricalProvenanceMapping(unittest.TestCase):
    """Verifies REV-131 External Review Amendment:

    Maps historical Phase 01–12 provenance records to canonical identities,
    preserving immutable origin paths and ensuring 100% reconciliation.
    """

    def setUp(self):
        self.phase08_csv = str(REPO_ROOT / "audit" / "rebuild-phase-1-12" / "phase08-canonical-registry.csv")
        self.census_json = str(REPO_ROOT / "audit" / "taxonomy-census" / "semantic-role-census.json")

    def test_reconcile_authoritative_historical_phase08_and_census(self):
        """Reconciles live phase08-canonical-registry.csv against semantic-role-census.json."""
        if not os.path.exists(self.phase08_csv) or not os.path.exists(self.census_json):
            self.skipTest("Historical CSV or census JSON not found in expected repository paths.")

        report = HistoricalProvenanceMapper.reconcile(
            phase08_csv_path=self.phase08_csv,
            census_json_path=self.census_json,
        )

        self.assertIsInstance(report, ProvenanceReconciliationReport)
        self.assertTrue(report.is_fully_reconciled, "Historical provenance must be 100% reconciled.")
        self.assertEqual(len(report.unmatched_historical), 0, "No historical Phase 08 records can be left unmapped.")
        self.assertGreaterEqual(report.total_historical_records, 2100)
        self.assertGreaterEqual(report.matched_records, 2100)

        # Check sample record integrity
        commit_rec = report.provenance_records.get("development:commit")
        self.assertIsNotNone(commit_rec)
        self.assertTrue(commit_rec.origin_path.startswith("task-folder/agents/skills/"))
        self.assertTrue(commit_rec.historical_destination.startswith("task-folder/agents/skills-rebuild/"))
        self.assertEqual(commit_rec.provenance_type, ProvenanceType.PHASE_08_REBUILD)

        # Check that design-md_v1 historical alias was resolved to design:design-md
        design_rec = report.provenance_records.get("design-and-experience:design-md")
        self.assertIsNotNone(design_rec)
        self.assertIn("design-md_v1", design_rec.origin_path)

        # Check that platform candidates exist and are classified
        platform_recs = [
            r for r in report.provenance_records.values()
            if r.provenance_type == ProvenanceType.CENSUS_PLATFORM_CANDIDATE
        ]
        self.assertGreater(len(platform_recs), 0, "Platform family candidates must be tracked in provenance records.")

        summary_text = report.summary()
        self.assertIn("PASSED (100% Traceability)", summary_text)

    def test_reconcile_handles_unmatched_records_gracefully(self):
        """Simulates historical CSV containing orphan records not in census."""
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tf:
            tf.write("origin_path,proposed_category,proposed_subcategory,canonical_skill_name,origin_type,phase08_batch,phase08_final_destination,phase08_rewrite_status,phase08_validation_status\n")
            tf.write("task-folder/agents/skills-rebuild/nonexistent/foo/bar,nonexistent,foo,bar,rebuilt,batch-99,library/nonexistent/foo/bar,COMPLETE,PASSED\n")
            temp_csv = tf.name

        try:
            report = HistoricalProvenanceMapper.reconcile(
                phase08_csv_path=temp_csv,
                census_json_path=self.census_json,
            )
            self.assertFalse(report.is_fully_reconciled)
            self.assertEqual(len(report.unmatched_historical), 1)
            self.assertEqual(report.unmatched_historical[0], "library/nonexistent/foo/bar")
        finally:
            if os.path.exists(temp_csv):
                os.unlink(temp_csv)


class TestGate1CanonicalIdentity(unittest.TestCase):
    """Verifies Gate 1: Canonical Identity Uniqueness & Structure (INV-2, INV-6)."""

    def _make_entry(self, cid: str, path: str = "library/domain/sub/slug") -> RegistryEntry:
        parts = cid.split(":")
        slug = parts[-1]
        entry = object.__new__(RegistryEntry)
        entry.canonical_id = cid
        entry.urn = f"urn:skill:{cid}"
        entry.name = slug
        entry.role = "capability"
        entry.description = "Test skill"
        entry.domain = "domain"
        entry.category = "domain"
        entry.subcategory = "sub"
        entry.owner = "core"
        entry.families = []
        entry.semantic_groups = []
        entry.physical_path = path
        entry.version = "1.0.0"
        entry.status = "active"
        entry.confidence = "high"
        entry.tags = []
        entry.keywords = []
        entry.relationships = {
            "composed_of": [],
            "extends": None,
            "depends_on": [],
            "adapts": None,
            "aliased_to": None,
            "belongs_to_family": None,
        }
        entry.execution_providers = []
        entry.provenance = {}
        return entry

    def test_gate1_valid_catalog_passes(self):
        reg = _build_test_registry([
            self._make_entry("dev:git-commit"),
            self._make_entry("dev:git-push"),
        ])
        res = MigrationGateEvaluator.evaluate_gate_1_canonical_identity(reg)
        self.assertTrue(res.is_passed)
        self.assertEqual(res.items_checked, 2)
        self.assertEqual(len(res.violations), 0)

    def test_gate1_catches_invalid_syntax_and_characters(self):
        reg = _build_test_registry([
            self._make_entry("INVALID:UPPER"),
            self._make_entry("dev:has.dot"),
        ])
        res = MigrationGateEvaluator.evaluate_gate_1_canonical_identity(reg)
        self.assertFalse(res.is_passed)
        self.assertGreaterEqual(len(res.violations), 2)
        inv_ids = [v.entity_id for v in res.violations]
        self.assertIn("INVALID:UPPER", inv_ids)
        self.assertIn("dev:has.dot", inv_ids)

    def test_gate1_catches_path_characters_in_canonical_id(self):
        reg = _build_test_registry([
            self._make_entry("dev:path/to/slug"),
        ])
        res = MigrationGateEvaluator.evaluate_gate_1_canonical_identity(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-6_SYNTAX" or v.rule == "INV-6_PATH_INDEPENDENCE" for v in res.violations))


class TestGate2FamilyQualification(unittest.TestCase):
    """Verifies Gate 2: Family Qualification & Boundary Adherence (INV-8)."""

    def _make_hub_entry(self, cid: str, path: str, family: str) -> RegistryEntry:
        scope, slug = cid.split(":")
        return RegistryEntry(
            canonical_id=cid,
            urn=f"urn:skill:{cid}",
            name=slug,
            role="capability",
            description="Hub member",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory=family,
            owner="core",
            families=[family],
            physical_path=path,
            status="active",
            relationships={"belongs_to_family": family},
        )

    def test_gate2_valid_tier_1_hub_passes(self):
        reg = _build_test_registry([
            self._make_hub_entry(
                "github:create-pr",
                "library/tools-and-platforms/github/create-pr",
                "github",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_2_family_qualification(reg)
        self.assertTrue(res.is_passed)

    def test_gate2_fails_when_tier_1_hub_member_has_mismatched_family(self):
        # Entry at tools-and-platforms/github/create-pr claims family supabase
        entry = RegistryEntry(
            canonical_id="github:create-pr",
            urn="urn:skill:github:create-pr",
            name="create-pr",
            role="capability",
            description="Hub member",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="github",
            owner="core",
            families=["supabase"],  # Mismatched!
            physical_path="library/tools-and-platforms/github/create-pr",
            status="active",
            relationships={"belongs_to_family": "supabase"},
        )
        reg = _build_test_registry([entry])
        res = MigrationGateEvaluator.evaluate_gate_2_family_qualification(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any("does not declare membership in family" in v.message for v in res.violations))

    def test_gate2_direction_neutral_duplicate_protection(self):
        """Verifies duplicate pairs cannot be prematurely deprecated to active aliases without adjudication."""
        entry = RegistryEntry(
            canonical_id="github:pr",
            urn="urn:skill:github:pr",
            name="pr",
            role="alias",
            description="Deprecated alias",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="github",
            owner="core",
            status="active",  # Active alias without adjudication!
            relationships={"aliased_to": "developer-tools:pr"},
        )
        reg = _build_test_registry([entry])
        res = MigrationGateEvaluator.evaluate_gate_2_family_qualification(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any("converted to an active alias without semantic adjudication" in v.message for v in res.violations))

    def test_gate2_rejects_unqualified_family_in_tools_and_platforms(self):
        """Verifies physical hub placement requires an approved Tier 1 platform family (e.g. Supabase is Tier 2)."""
        entry = RegistryEntry(
            canonical_id="supabase:auth",
            urn="urn:skill:supabase:auth",
            name="auth",
            role="capability",
            description="Supabase Auth",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="supabase",
            owner="core",
            families=["supabase"],
            physical_path="library/tools-and-platforms/supabase/auth",
            status="active",
            relationships={"belongs_to_family": "supabase"},
        )
        reg = _build_test_registry([entry])
        res = MigrationGateEvaluator.evaluate_gate_2_family_qualification(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "UNQUALIFIED_FAMILY_PHYSICAL_HUB" for v in res.violations))
        self.assertTrue(any("not an approved Tier 1 platform hub" in v.message for v in res.violations))

    def test_gate2_rejects_deprecated_unadjudicated_duplicate_alias(self):
        """Verifies that an unadjudicated alias marked 'deprecated' is strictly rejected."""
        entry = RegistryEntry(
            canonical_id="github:pr-action",
            urn="urn:skill:github:pr-action",
            name="pr-action",
            role="alias",
            description="Unadjudicated deprecated alias",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="github",
            owner="core",
            status="deprecated",  # Deprecated alias without adjudication!
            relationships={"aliased_to": "developer-tools:pr-action"},
        )
        reg = _build_test_registry([entry])
        res = MigrationGateEvaluator.evaluate_gate_2_family_qualification(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "UNADJUDICATED_DUPLICATE_ALIAS" for v in res.violations))
        self.assertTrue(any("converted to a deprecated alias without semantic adjudication" in v.message for v in res.violations))

    def test_gate2_accepts_adjudicated_duplicate_alias(self):
        """Verifies that an adjudicated alias (with explicit outcome) passes Gate 2."""
        entry = RegistryEntry(
            canonical_id="github:actions",
            urn="urn:skill:github:actions",
            name="actions",
            role="alias",
            description="Adjudicated alias",
            domain="tools-and-platforms",
            category="tools-and-platforms",
            subcategory="github",
            owner="core",
            status="deprecated",
            relationships={
                "aliased_to": "developer-tools:actions",
                "adjudication_outcome": DuplicateAdjudicationOutcome.DOMAIN_CANONICAL.value,
            },
        )
        reg = _build_test_registry([entry])
        res = MigrationGateEvaluator.evaluate_gate_2_family_qualification(reg)
        self.assertTrue(res.is_passed)



class TestGate3GraphTopologyAndAcyclicity(unittest.TestCase):
    """Verifies Gate 3: Graph Topology, Acyclicity & Alias Purity (INV-1, INV-3, INV-4, INV-5)."""

    def test_gate3_valid_dag_passes(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="domain:step-a",
                urn="urn:skill:domain:step-a",
                name="step-a",
                role="capability",
                description="Step A",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
            ),
            RegistryEntry(
                canonical_id="domain:step-b",
                urn="urn:skill:domain:step-b",
                name="step-b",
                role="workflow",
                description="Step B",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"depends_on": ["domain:step-a"]},
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_3_graph_topology(reg)
        self.assertTrue(res.is_passed)

    def test_gate3_catches_cyclic_dependency(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="domain:a",
                urn="urn:skill:domain:a",
                name="a",
                role="capability",
                description="A",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"depends_on": ["domain:b"]},
            ),
            RegistryEntry(
                canonical_id="domain:b",
                urn="urn:skill:domain:b",
                name="b",
                role="capability",
                description="B",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"depends_on": ["domain:a"]},
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_3_graph_topology(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-1_CYCLE_DETECTED" for v in res.violations))

    def test_gate3_catches_alias_chaining(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="domain:canonical-target",
                urn="urn:skill:domain:canonical-target",
                name="canonical-target",
                role="capability",
                description="Target",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
            ),
            RegistryEntry(
                canonical_id="domain:intermediate-alias",
                urn="urn:skill:domain:intermediate-alias",
                name="intermediate-alias",
                role="alias",
                description="Intermediate",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"aliased_to": "domain:canonical-target"},
            ),
            RegistryEntry(
                canonical_id="domain:source-alias",
                urn="urn:skill:domain:source-alias",
                name="source-alias",
                role="alias",
                description="Source",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"aliased_to": "domain:intermediate-alias"},  # Chained alias!
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_3_graph_topology(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-3_CHAINED_ALIAS" for v in res.violations))

    def test_gate3_catches_overlay_extending_overlay(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="domain:base-overlay",
                urn="urn:skill:domain:base-overlay",
                name="base-overlay",
                role="overlay",
                description="Base Overlay",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
            ),
            RegistryEntry(
                canonical_id="domain:child-overlay",
                urn="urn:skill:domain:child-overlay",
                name="child-overlay",
                role="overlay",
                description="Child Overlay",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"extends": "domain:base-overlay"},  # Overlay extending overlay!
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_3_graph_topology(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-4_OVERLAY_EXTENDING_OVERLAY" for v in res.violations))

    def test_gate3_catches_composite_primitive(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="domain:atomic-primitive",
                urn="urn:skill:domain:atomic-primitive",
                name="atomic-primitive",
                role="primitive",
                description="Primitive",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"composed_of": ["domain:sub-skill"]},  # Primitive composing others!
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_3_graph_topology(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-5_PRIMITIVE_COMPOSITION_PROHIBITED" for v in res.violations))

    def test_gate3_catches_cycle_involving_adapts(self):
        """Verifies that a circular cycle involving an 'adapts' relationship is detected (INV-1)."""
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="domain:target-service",
                urn="urn:skill:domain:target-service",
                name="target-service",
                role="capability",
                description="Target Service",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"depends_on": ["domain:adapter-skill"]},
            ),
            RegistryEntry(
                canonical_id="domain:adapter-skill",
                urn="urn:skill:domain:adapter-skill",
                name="adapter-skill",
                role="adapter",
                description="Adapter Skill",
                domain="domain",
                category="domain",
                subcategory="sub",
                owner="core",
                relationships={"adapts": "domain:target-service"},  # Cycle: target-service -> adapter-skill -> target-service
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_3_graph_topology(reg)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-1_CYCLE_DETECTED" for v in res.violations))
        self.assertTrue(any("domain:target-service" in v.message and "domain:adapter-skill" in v.message for v in res.violations))



class TestGate4ResourcePreservation(unittest.TestCase):
    """Verifies Gate 4: Resource & Asset Preservation (Zero Data Loss)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_gate4_passes_with_valid_skill_md_and_assets(self):
        skill_dir = Path(self.temp_dir) / "library" / "dev" / "git" / "commit"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Commit Skill\nDescription here.\n")

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:commit",
                urn="urn:skill:dev:commit",
                name="commit",
                role="capability",
                description="Git commit",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path="library/dev/git/commit",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(reg, repository_root=self.temp_dir)
        self.assertTrue(res.is_passed)
        self.assertEqual(res.items_checked, 1)

    def test_gate4_fails_when_skill_md_is_missing(self):
        skill_dir = Path(self.temp_dir) / "library" / "dev" / "git" / "push"
        skill_dir.mkdir(parents=True)
        # No SKILL.md!

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:push",
                urn="urn:skill:dev:push",
                name="push",
                role="capability",
                description="Git push",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path="library/dev/git/push",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(reg, repository_root=self.temp_dir)
        self.assertFalse(res.is_passed)
        self.assertTrue(any("contains no SKILL.md" in v.message for v in res.violations))

    def test_gate4_fails_when_skill_md_is_truncated(self):
        """Verifies that a 0-byte SKILL.md fails Gate 4 with TRUNCATED_SKILL_MD."""
        skill_dir = Path(self.temp_dir) / "library" / "dev" / "git" / "empty-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("")  # 0 bytes

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:empty-skill",
                urn="urn:skill:dev:empty-skill",
                name="empty-skill",
                role="capability",
                description="Empty skill",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path="library/dev/git/empty-skill",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(reg, repository_root=self.temp_dir)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "TRUNCATED_SKILL_MD" for v in res.violations))

    def test_gate4_fails_when_supporting_asset_is_truncated(self):
        """Verifies that a 0-byte auxiliary asset fails Gate 4 with TRUNCATED_ASSET_FILE."""
        skill_dir = Path(self.temp_dir) / "library" / "dev" / "git" / "trunc-asset"
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Valid Skill\nBody here.\n")
        (scripts_dir / "helper.sh").write_text("")  # 0 bytes!

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:trunc-asset",
                urn="urn:skill:dev:trunc-asset",
                name="trunc-asset",
                role="capability",
                description="Truncated asset skill",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path="library/dev/git/trunc-asset",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(reg, repository_root=self.temp_dir)
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "TRUNCATED_ASSET_FILE" for v in res.violations))

    def test_gate4_source_to_destination_missing_supporting_asset(self):
        """Verifies source-to-destination manifest comparison catches missing auxiliary assets."""
        src_dir = Path(self.temp_dir) / "src" / "commit"
        dst_dir = Path(self.temp_dir) / "dst" / "commit"
        src_scripts = src_dir / "scripts"
        src_scripts.mkdir(parents=True)
        dst_dir.mkdir(parents=True)

        (src_dir / "SKILL.md").write_text("# Commit Skill\n")
        (src_scripts / "run.py").write_text("print('run')\n")
        (dst_dir / "SKILL.md").write_text("# Commit Skill\n")
        # Notice: dst_dir is missing scripts/run.py!

        src_manifest = SkillPackageManifest.from_directory("dev:commit", str(src_dir))
        dst_manifest = SkillPackageManifest.from_directory("dev:commit", str(dst_dir))

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:commit",
                urn="urn:skill:dev:commit",
                name="commit",
                role="capability",
                description="Commit",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path=str(dst_dir),
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(
            reg,
            repository_root=self.temp_dir,
            source_manifests={"dev:commit": src_manifest},
            destination_manifests={"dev:commit": dst_manifest},
        )
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "MISSING_SUPPORTING_ASSET" for v in res.violations))
        self.assertTrue(any("scripts/run.py" in v.message for v in res.violations))

    def test_gate4_source_to_destination_checksum_mismatch(self):
        """Verifies source-to-destination manifest comparison catches file modifications/tampering."""
        src_dir = Path(self.temp_dir) / "src" / "review"
        dst_dir = Path(self.temp_dir) / "dst" / "review"
        src_dir.mkdir(parents=True)
        dst_dir.mkdir(parents=True)

        (src_dir / "SKILL.md").write_text("# Review Skill v1\n")
        (dst_dir / "SKILL.md").write_text("# Review Skill MODIFIED v2\n")

        src_manifest = SkillPackageManifest.from_directory("dev:review", str(src_dir))
        dst_manifest = SkillPackageManifest.from_directory("dev:review", str(dst_dir))

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:review",
                urn="urn:skill:dev:review",
                name="review",
                role="capability",
                description="Review",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path=str(dst_dir),
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(
            reg,
            repository_root=self.temp_dir,
            source_manifests={"dev:review": src_manifest},
            destination_manifests={"dev:review": dst_manifest},
        )
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "RESOURCE_CHECKSUM_MISMATCH" for v in res.violations))

    def test_gate4_source_to_destination_exact_match_passes(self):
        """Verifies that 100% byte-for-byte asset preservation passes Gate 4."""
        src_dir = Path(self.temp_dir) / "src" / "clean-skill"
        dst_dir = Path(self.temp_dir) / "dst" / "clean-skill"
        (src_dir / "scripts").mkdir(parents=True)
        (dst_dir / "scripts").mkdir(parents=True)

        content_skill = "# Clean Skill\nAll documentation.\n"
        content_script = "#!/usr/bin/env python3\nprint('safe')\n"

        (src_dir / "SKILL.md").write_text(content_skill)
        (src_dir / "scripts" / "tool.py").write_text(content_script)
        (dst_dir / "SKILL.md").write_text(content_skill)
        (dst_dir / "scripts" / "tool.py").write_text(content_script)

        src_manifest = SkillPackageManifest.from_directory("dev:clean-skill", str(src_dir))
        dst_manifest = SkillPackageManifest.from_directory("dev:clean-skill", str(dst_dir))

        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:clean-skill",
                urn="urn:skill:dev:clean-skill",
                name="clean-skill",
                role="capability",
                description="Clean Skill",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                physical_path=str(dst_dir),
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_4_resource_preservation(
            reg,
            repository_root=self.temp_dir,
            source_manifests={"dev:clean-skill": src_manifest},
            destination_manifests={"dev:clean-skill": dst_manifest},
        )
        self.assertTrue(res.is_passed)
        self.assertEqual(len(res.violations), 0)



class TestGate5ReferenceClosure(unittest.TestCase):
    """Verifies Gate 5: Reference Closure & Dependency Completeness (INV-7)."""

    def test_gate5_passes_when_all_references_exist(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:auth",
                urn="urn:skill:dev:auth",
                name="auth",
                role="primitive",
                description="Auth",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
            ),
            RegistryEntry(
                canonical_id="dev:commit",
                urn="urn:skill:dev:commit",
                name="commit",
                role="capability",
                description="Commit",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                relationships={"depends_on": ["dev:auth"]},
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_5_reference_closure(reg)
        self.assertTrue(res.is_passed)

    def test_gate5_fails_on_dangling_references(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:workflow",
                urn="urn:skill:dev:workflow",
                name="workflow",
                role="workflow",
                description="Workflow",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                relationships={
                    "depends_on": ["nonexistent:target"],
                    "composed_of": ["ghost:step"],
                },
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_5_reference_closure(reg)
        self.assertFalse(res.is_passed)
        self.assertEqual(len(res.violations), 2)
        self.assertTrue(all(v.rule.startswith("INV-7_") for v in res.violations))


class TestGate6GeneratedViewsAndRouters(unittest.TestCase):
    """Verifies Gate 6: Generated-View Reconciliation & Router Integrity."""

    def test_gate6_passes_with_projection_views(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="development:commit",
                urn="urn:skill:development:commit",
                name="commit",
                role="capability",
                description="Commit",
                domain="development",
                category="development",
                subcategory="git",
                owner="core",
                families=["git-family"],
                semantic_groups=["version-control"],
                physical_path="library/development/git/commit",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_6_view_reconciliation(reg)
        self.assertTrue(res.is_passed)
        self.assertGreaterEqual(res.items_checked, 4)


class TestGate7DeterministicCompilation(unittest.TestCase):
    """Verifies Gate 7: Deterministic Compilation & Idempotency (INV-10)."""

    def test_gate7_passes_on_identical_compilations(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="development:commit",
                urn="urn:skill:development:commit",
                name="commit",
                role="capability",
                description="Commit",
                domain="development",
                category="development",
                subcategory="git",
                owner="core",
            )
        ])
        res = MigrationGateEvaluator.evaluate_gate_7_deterministic_compilation(reg)
        self.assertTrue(res.is_passed)
        self.assertEqual(len(res.violations), 0)

    def test_gate7_fails_when_compilation_bytes_differ(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="development:commit",
                urn="urn:skill:development:commit",
                name="commit",
                role="capability",
                description="Commit",
                domain="development",
                category="development",
                subcategory="git",
                owner="core",
            )
        ])
        counter = [0]
        def non_deterministic_compiler(registry, pinned_ts):
            counter[0] += 1
            return f"output-run-{counter[0]}".encode("utf-8")

        res = MigrationGateEvaluator.evaluate_gate_7_deterministic_compilation(
            reg,
            compiler_fn=non_deterministic_compiler,
        )
        self.assertFalse(res.is_passed)
        self.assertTrue(any(v.rule == "INV-10_HASH_DIVERGENCE" for v in res.violations))


class TestGate8ProjectMaterialization(unittest.TestCase):
    """Verifies Gate 8: Project Materialization Completeness & Collision-Free Naming (INV-9)."""

    def test_gate8_passes_on_valid_materialization(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:auth",
                urn="urn:skill:dev:auth",
                name="auth",
                role="primitive",
                description="Auth",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
            ),
            RegistryEntry(
                canonical_id="dev:commit",
                urn="urn:skill:dev:commit",
                name="commit",
                role="capability",
                description="Commit",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
                relationships={"depends_on": ["dev:auth"]},
            ),
        ])
        res = MigrationGateEvaluator.evaluate_gate_8_project_materialization(reg)
        self.assertTrue(res.is_passed)

    def test_gate8_naming_collision_resolution(self):
        """Verifies collision-free naming ladder generates unique flat runtime names."""
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="dev:commit",
                urn="urn:skill:dev:commit",
                name="commit",
                role="capability",
                description="Commit in dev",
                domain="dev",
                category="dev",
                subcategory="git",
                owner="core",
            ),
            RegistryEntry(
                canonical_id="github:commit",
                urn="urn:skill:github:commit",
                name="commit",
                role="capability",
                description="Commit in github",
                domain="tools-and-platforms",
                category="tools-and-platforms",
                subcategory="github",
                owner="core",
            ),
        ])
        materializer = ProjectMaterializer(reg)
        bundle = materializer.materialize_bundle(
            mode=ProjectionMode.STANDALONE_CLOSURE,
            target_ids=["dev:commit", "github:commit"],
        )
        names = list(bundle["runtime_names"].values())
        self.assertEqual(len(names), 2)
        self.assertNotEqual(names[0], names[1])


class TestGate9RuntimePublicationPreFlight(unittest.TestCase):
    """Verifies Gate 9: Runtime Publication Pre-Flight & Target Compatibility."""

    def test_gate9_passes_when_working_tree_is_clean(self):
        reg = _build_test_registry([])
        res = MigrationGateEvaluator.evaluate_gate_9_publication_preflight(reg, repository_root=str(REPO_ROOT))
        self.assertTrue(res.is_passed, f"Gate 9 should pass on clean protected assets: {res.violations}")


class TestMigrationGateRunnerEndToEnd(unittest.TestCase):
    """End-to-end execution of MigrationGateRunner across all 9 gates and provenance."""

    def test_runner_executes_all_gates(self):
        reg = _build_test_registry([
            RegistryEntry(
                canonical_id="development:commit",
                urn="urn:skill:development:commit",
                name="commit",
                role="capability",
                description="Git commit",
                domain="development",
                category="development",
                subcategory="git",
                owner="core",
            )
        ])
        runner = MigrationGateRunner(registry=reg, repository_root=str(REPO_ROOT))
        report = runner.run_all_gates()

        self.assertIsInstance(report, MigrationGateReport)
        self.assertEqual(report.total_gates, 9)
        self.assertIn(GateID.GATE_1_CANONICAL_IDENTITY, report.gate_results)
        self.assertIn(GateID.GATE_7_DETERMINISTIC_COMPILATION, report.gate_results)
        self.assertIn(GateID.GATE_9_PUBLICATION_PREFLIGHT, report.gate_results)

        # Check report summary string
        summary = report.summary()
        self.assertIn("Migration Architecture Validation Report", summary)
        self.assertIn("Gate Breakdown", summary)


if __name__ == "__main__":
    unittest.main()
