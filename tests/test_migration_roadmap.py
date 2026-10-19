"""
Unit & Contract Tests for the Skills Library Implementation Roadmap (REV-132).

Validates that:
1. The authoritative master roadmap (docs/architecture/MIGRATION_ROADMAP.md) is well-formed,
   references ADR-001 through ADR-005, and maps all 6 migration phases to the 9 formal gates.
2. The legacy rebuild tasks (Phases 01–13) are preserved in library-rebuild-tasks/legacy-rebuild-phase-1-13/.
3. The historical Phase 01–12 rebuild audit evidence in audit/rebuild-phase-1-12/ is untouched.
4. The 6 new active phase specifications in library-rebuild-tasks/ follow the required schema
   and explicitly enforce non-destructive preflight, manifest authenticity, and direction-neutral holds.
"""

import os
import re
import unittest
from pathlib import Path

from skill_library.migration_gates import GateID


class TestMigrationRoadmapContracts(unittest.TestCase):
    """Verifies that the migration roadmap conforms to approved architecture contracts."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.roadmap_path = cls.repo_root / "docs" / "architecture" / "MIGRATION_ROADMAP.md"
        cls.tasks_dir = cls.repo_root / "library-rebuild-tasks"
        cls.legacy_dir = cls.tasks_dir / "legacy-rebuild-phase-1-13"
        cls.audit_dir = cls.repo_root / "audit" / "rebuild-phase-1-12"

    def test_master_roadmap_exists_and_references_architecture_contracts(self):
        """Verifies master roadmap exists and references all 5 approved ADRs."""
        self.assertTrue(self.roadmap_path.exists(), f"Roadmap not found at {self.roadmap_path}")
        content = self.roadmap_path.read_text(encoding="utf-8")

        # Must reference REV-132
        self.assertIn("REV-132", content)

        # Must reference ADR-001 through ADR-005
        self.assertIn("ADR-001", content)
        self.assertIn("ADR-002", content)
        self.assertIn("ADR-003", content)
        self.assertIn("ADR-004", content)
        self.assertIn("ADR-005", content)

        # Must reference REV-125 duplicate freeze replacement
        self.assertIn("REV-125", content)
        self.assertIn("470-group", content)

        # Must reference census and RFC 8141 URNs
        self.assertIn("semantic-role-census.json", content)
        self.assertIn("urn:skill:", content)

    def test_master_roadmap_covers_all_nine_gates(self):
        """Verifies master roadmap covers all 9 GateID enum values."""
        content = self.roadmap_path.read_text(encoding="utf-8")
        for gid in GateID:
            self.assertIn(gid.value, content, f"Roadmap missing coverage for gate ID: {gid.value}")

    def test_master_roadmap_covers_all_ten_invariants(self):
        """Verifies master roadmap documents invariants INV-1 through INV-10."""
        content = self.roadmap_path.read_text(encoding="utf-8")
        for i in range(1, 11):
            inv = f"INV-{i}"
            self.assertIn(inv, content, f"Roadmap missing invariant: {inv}")

    def test_legacy_tasks_are_preserved_in_archive(self):
        """Verifies that all 16 legacy task specs are safely preserved in legacy-rebuild-phase-1-13/."""
        self.assertTrue(self.legacy_dir.exists(), f"Legacy directory not found at {self.legacy_dir}")
        self.assertTrue((self.legacy_dir / "README.md").exists(), "Legacy archive README.md missing")

        expected_legacy_files = [
            "01-establish-baseline.md",
            "02-build-complete-inventory.md",
            "03-apply-application-compatibility-gate.md",
            "04-remove-provider-specific-assumptions.md",
            "05-define-functional-taxonomy.md",
            "06- Consolidate Overlapping Skills (Hardened).md",
            "06-consolidate-overlapping-skills.md",
            "07-split-oversized-skills-hardened.md",
            "07-split-oversized-skills.md",
            "08-rewrite-normalize-canonical-skills.md",
            "09-clean-bundled-resources.md",
            "10-build-router-hierarchy.md",
            "11-validate-complete-library.md",
            "12-pilot-review-publish.md",
            "13-build-reusable-skill-intake-router-hierarchy.md",
            "repository-rename-cleanup.md",
        ]

        for fname in expected_legacy_files:
            file_path = self.legacy_dir / fname
            self.assertTrue(file_path.exists(), f"Legacy file missing from archive: {fname}")
            self.assertGreater(file_path.stat().st_size, 0, f"Legacy file empty: {fname}")

    def test_historical_audit_evidence_remains_intact(self):
        """Verifies that historical CSV records in audit/rebuild-phase-1-12/ are preserved."""
        self.assertTrue(self.audit_dir.exists(), f"Audit directory not found at {self.audit_dir}")

        expected_audit_files = [
            "phase08-canonical-registry.csv",
            "phase08-batch-plan.csv",
            "split-allocations.csv",
            "split-decisions.csv",
            "merge-decisions.csv",
            "merge-members.csv",
            "destination-map.csv",
            "skills-inventory.csv",
            "phase09-resource-registry.csv",
            "phase10-functional-routing-map.csv",
        ]

        for fname in expected_audit_files:
            audit_file = self.audit_dir / fname
            self.assertTrue(audit_file.exists(), f"Historical audit evidence missing: {fname}")
            self.assertGreater(audit_file.stat().st_size, 1000, f"Historical audit file unexpectedly small: {fname}")

    def test_new_phase_specifications_exist_and_conform_to_schema(self):
        """Verifies that the 6 new phase specifications exist and have required sections."""
        expected_phases = [
            ("phase-01-canonical-identity-provenance-baseline.md", "Phase 01", ["Gate 1", "Gate 7"]),
            ("phase-02-family-qualification-physical-layout.md", "Phase 02", ["Gate 2"]),
            ("phase-03-duplicate-adjudication-alias-contracts.md", "Phase 03", ["Gate 3"]),
            ("phase-04-manifest-authenticity-staged-migration.md", "Phase 04", ["Gate 4"]),
            ("phase-05-multi-view-routers-reference-closure.md", "Phase 05", ["Gate 5", "Gate 6"]),
            ("phase-06-compilation-materialization-publication-preflight.md", "Phase 06", ["Gate 7", "Gate 8", "Gate 9"]),
        ]

        # Verify README in tasks directory
        tasks_readme = self.tasks_dir / "README.md"
        self.assertTrue(tasks_readme.exists(), "library-rebuild-tasks/README.md missing")
        readme_content = tasks_readme.read_text(encoding="utf-8")
        self.assertIn("MIGRATION_ROADMAP.md", readme_content)

        required_sections = [
            "## 1. Objective",
            "## 2. Preconditions",
            "## 3. Canonical Task Skills",
            "## 4. Step-by-Step Work",
            "## 5. Artifacts",
            "## 6. Reconciliation Requirements",
            "## 7. Repository Checkpoint",
            "## 8. Completion Gate",
        ]

        for fname, phase_label, expected_gates in expected_phases:
            spec_path = self.tasks_dir / fname
            self.assertTrue(spec_path.exists(), f"Phase spec missing: {fname}")
            content = spec_path.read_text(encoding="utf-8")

            # Check phase title/label
            self.assertIn(phase_label, content, f"Missing {phase_label} label in {fname}")

            # Check required sections
            for sec in required_sections:
                self.assertIn(sec, content, f"Missing section '{sec}' in {fname}")

            # Check gate mentions
            for gate in expected_gates:
                self.assertIn(gate, content, f"Missing expected gate '{gate}' in {fname}")

    def test_phase_03_preserves_direction_neutral_github_pairs(self):
        """Verifies Phase 03 explicitly preserves direction-neutral hold on 15 GitHub duplicate pairs."""
        p3_path = self.tasks_dir / "phase-03-duplicate-adjudication-alias-contracts.md"
        content = p3_path.read_text(encoding="utf-8")
        self.assertIn("direction-neutral", content.lower())
        self.assertIn("15", content)
        self.assertIn("github", content.lower())
        self.assertIn("CANDIDATE_HYPOTHESES", content)
        self.assertIn("single-hop", content.lower())

    def test_phase_04_enforces_manifest_authenticity_and_staging_boundaries(self):
        """Verifies Phase 04 mandates SHA-256 manifest authenticity and path containment."""
        p4_path = self.tasks_dir / "phase-04-manifest-authenticity-staged-migration.md"
        content = p4_path.read_text(encoding="utf-8")
        self.assertIn("SHA-256", content)
        self.assertIn("staging", content.lower())
        self.assertIn("PATH_TRAVERSAL_DETECTED", content)
        self.assertIn("SkillPackageManifest", content)
        self.assertIn("non-destructive", content.lower())

    def test_master_roadmap_status_is_proposed_pending_rev132_approval(self):
        """Verifies master roadmap status is 'Proposed, Pending REV-132 Approval'."""
        content = self.roadmap_path.read_text(encoding="utf-8")
        self.assertIn("- **Status**: Proposed, Pending REV-132 Approval", content)

    def test_census_relative_link_resolves_from_docs_architecture(self):
        """Verifies that the relative census link in MIGRATION_ROADMAP.md resolves correctly from docs/architecture/."""
        content = self.roadmap_path.read_text(encoding="utf-8")
        # Extract markdown link matching semantic-role-census.json
        match = re.search(r"\[.*?\]\((.*?semantic-role-census\.json)\)", content)
        self.assertIsNotNone(match, "Semantic role census relative link not found in roadmap")
        rel_target = match.group(1)
        resolved_path = (self.roadmap_path.parent / rel_target).resolve()
        self.assertTrue(resolved_path.exists(), f"Census relative link '{rel_target}' does not resolve: {resolved_path}")
        self.assertTrue(resolved_path.is_file(), f"Resolved census path is not a file: {resolved_path}")

    def test_phase_05_restores_all_four_adr004_views_and_semantic_projections(self):
        """Verifies Phase 05 restores all 4 ADR-004 projection views and treats overlays/packs as additional structures."""
        roadmap_content = self.roadmap_path.read_text(encoding="utf-8")
        p5_path = self.tasks_dir / "phase-05-multi-view-routers-reference-closure.md"
        p5_content = p5_path.read_text(encoding="utf-8")

        for content, doc_name in [(roadmap_content, "MIGRATION_ROADMAP.md"), (p5_content, "phase-05 task spec")]:
            # View 1: Functional / Domain View
            self.assertIn("views/functional-view.json", content, f"{doc_name} missing functional-view.json")
            # View 2: Platform / Family View
            self.assertIn("views/family-view.json", content, f"{doc_name} missing family-view.json")
            # View 3: Semantic Group View
            self.assertIn("views/semantic-group-view.json", content, f"{doc_name} missing semantic-group-view.json")
            # View 4: Execution / Provider View
            self.assertIn("views/provider-view.json", content, f"{doc_name} missing provider-view.json")

            # Additional semantic projections / content structures
            self.assertIn("extends", content, f"{doc_name} missing extends capability overlays")
            self.assertIn("composed_of", content, f"{doc_name} missing composed_of workflow packs")

        # Check virtual family routers and MultiViewProjector references in Phase 05
        self.assertIn("MultiViewProjector", p5_content)
        self.assertIn("views/routers/family-", p5_content)
        self.assertIn("Tier 2", p5_content)

    def test_phase_06_references_project_materializer_runtime_naming_ladder(self):
        """Verifies Phase 06 references ProjectMaterializer._generate_flat_runtime_names() and the 6-stage candidate ladder."""
        roadmap_content = self.roadmap_path.read_text(encoding="utf-8")
        p6_path = self.tasks_dir / "phase-06-compilation-materialization-publication-preflight.md"
        p6_content = p6_path.read_text(encoding="utf-8")

        for content, doc_name in [(roadmap_content, "MIGRATION_ROADMAP.md"), (p6_content, "phase-06 task spec")]:
            self.assertIn("ProjectMaterializer._generate_flat_runtime_names()", content,
                          f"{doc_name} missing ProjectMaterializer._generate_flat_runtime_names() reference")
            self.assertIn("ADR-004 Section 9.2", content,
                          f"{doc_name} missing ADR-004 Section 9.2 reference")

        # Verify candidate ladder stages in Phase 06 task spec
        self.assertIn("Stage 1: Natural leaf name", p6_content)
        self.assertIn("Stage 2: Category prefix", p6_content)
        self.assertIn("Stage 3: Canonical scope prefix", p6_content)
        self.assertIn("Stage 4: Scope + category prefix", p6_content)
        self.assertIn("Stage 5: Full canonical ID slug", p6_content)
        self.assertIn("Stage 6: Disambiguated canonical ID slug", p6_content)


if __name__ == "__main__":
    unittest.main()
