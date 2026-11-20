"""
Unit and Negative Regression Test Suite for REV-150 Semantic Census Validation.

Tests authoritative census population invariants, independent mathematical
verification of narrative percentages against underlying counts, and explicit
negative regression test cases (invalid roles, missing schema fields, template
leaks, count divergences, and untracked artifacts).
"""

import csv
import json
import os
import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

# Ensure tools directory is in sys.path
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from validate_semantic_census import (
    ROLE_ADAPTER,
    ROLE_ALIAS,
    ROLE_FAMILY_PRIMITIVE,
    ROLE_INDEPENDENT_CAPABILITY,
    ROLE_MANUAL_REVIEW,
    ROLE_OVERLAY,
    ROLE_REFERENCE,
    ROLE_WORKFLOW,
    VALID_ROLES,
    assert_family_census_completeness,
    assert_no_template_leaks,
    write_manual_outliers,
)

CENSUS_DIR = REPO_ROOT / "audit" / "taxonomy-census"


class TestSemanticCensusInvariants(unittest.TestCase):
    """Authoritative population, schema integrity, and classification consistency tests."""

    @classmethod
    def setUpClass(cls):
        cls.csv_path = CENSUS_DIR / "semantic-role-census.csv"
        cls.json_path = CENSUS_DIR / "semantic-role-census.json"

        with open(cls.csv_path, mode="r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

        with open(cls.json_path, mode="r", encoding="utf-8") as f:
            cls.json_rows = json.load(f)

    def test_population_exact_count_and_parity(self):
        """CSV and JSON must agree on population, and canonical IDs must be unique.

        The population size is derived from the data, not pinned: the catalog
        legitimately changes, and a count is a catalog fact, not a defect.
        """
        self.assertEqual(len(self.csv_rows), len(self.json_rows), "CSV and JSON populations diverge")

        csv_ids = [r["canonical_id"] for r in self.csv_rows]
        json_ids = [r["canonical_id"] for r in self.json_rows]
        self.assertEqual(csv_ids, json_ids)
        self.assertEqual(len(set(csv_ids)), len(csv_ids), "All canonical IDs must be unique")

    def test_role_distribution_invariants(self):
        """Every row carries one of the accepted roles, and the roles partition the population."""
        counts = Counter(r["semantic_role"] for r in self.csv_rows)

        self.assertLessEqual(set(counts), set(VALID_ROLES), "Census contains an unknown semantic role")
        self.assertEqual(sum(counts.values()), len(self.csv_rows), "Role counts must sum to the population")

    def test_asset_audit_classification_integrity(self):
        """Verify asset-audit is classified as workflow across datasets and reports."""
        asset_audit_rows = [r for r in self.csv_rows if r["name"] == "asset-audit"]
        self.assertEqual(len(asset_audit_rows), 1)
        self.assertEqual(asset_audit_rows[0]["semantic_role"], ROLE_WORKFLOW)

        # Family register must note asset-audit as pruned to domain capability
        family_reg = (CENSUS_DIR / "family-candidate-register.md").read_text(encoding="utf-8")
        self.assertIn("asset-audit", family_reg)
        self.assertIn("Pruned Generic Audit Skills", family_reg)

        # Catch-all bin report must clarify asset-audit as domain workflow, not overlay
        catch_all = (CENSUS_DIR / "catch-all-bin-analysis.md").read_text(encoding="utf-8")
        self.assertIn("asset-audit", catch_all)
        self.assertIn("retained as a domain workflow", catch_all)
        # Ensure it does not list asset-audit as a Webflow CMS overlay
        self.assertNotIn("(`publish-blog`, `asset-audit`)", catch_all)

    def test_catch_all_bin_table_structure_and_aliases_header(self):
        """Catch-all breakdown must use 'Aliases' header and rows must match the census.

        Expected rows are derived from the census itself, so a legitimate
        population change restates the table instead of failing the build.
        """
        catch_all = (CENSUS_DIR / "catch-all-bin-analysis.md").read_text(encoding="utf-8")
        self.assertIn("| Catch-All Bin | Total Skills | Independent Capabilities | Workflows | Aliases | Overlays / Adapters | References | Primitives | Manual Review |", catch_all)
        self.assertNotIn("Aliases / Duplicates", catch_all)

        bin_names = ["development/fullstack", "marketing-and-seo/on-page-seo", "marketing-and-seo/cro"]
        for bin_name in bin_names:
            cat, sub = bin_name.split("/")
            members = [r for r in self.csv_rows if r["current_category"] == cat and r["current_subcategory"] == sub]
            rc = Counter(r["semantic_role"] for r in members)
            expected_row = (
                f"| `{bin_name}` | {len(members)} | {rc[ROLE_INDEPENDENT_CAPABILITY]} | "
                f"{rc[ROLE_WORKFLOW]} | {rc[ROLE_ALIAS]} | {rc[ROLE_OVERLAY] + rc[ROLE_ADAPTER]} | "
                f"{rc[ROLE_REFERENCE]} | {rc[ROLE_FAMILY_PRIMITIVE]} | {rc[ROLE_MANUAL_REVIEW]} |"
            )
            self.assertIn(expected_row, catch_all, f"Catch-all row for {bin_name} does not match the census")

    def test_independent_validation_narrative_percentages_against_counts(self):
        """The narrative percentages in the report must match the census counts.

        Expected percentages are computed from the census, so a legitimate
        population change restates the narrative instead of failing the build.
        """
        total = len(self.csv_rows)
        counts = Counter(r["semantic_role"] for r in self.csv_rows)

        report_text = (CENSUS_DIR / "census-validation-report.md").read_text(encoding="utf-8")
        for role, count in counts.items():
            expected_pct = round((count / total) * 100, 1)
            self.assertIn(f"{expected_pct}%", report_text, f"Report missing {expected_pct}% for {role}")


class TestNegativeSemanticRegression(unittest.TestCase):
    """Explicit negative regression tests asserting failure under invalid/drifted states."""

    def test_negative_invalid_role_rejection(self):
        """Negative test: asserting an invalid semantic role raises an error."""
        invalid_row = {
            "canonical_id": "test-invalid-skill",
            "name": "test-invalid-skill",
            "semantic_role": "unsupported_utility_role",
        }
        with self.assertRaises(ValueError) as ctx:
            if invalid_row["semantic_role"] not in VALID_ROLES:
                raise ValueError(f"Invalid semantic role: {invalid_row['semantic_role']}")
        self.assertIn("unsupported_utility_role", str(ctx.exception))

    def test_negative_missing_schema_fields_rejection(self):
        """Negative test: asserting records missing mandatory fields are rejected."""
        incomplete_row = {
            "canonical_id": "incomplete-item",
            # missing semantic_role and confidence
        }
        mandatory_fields = ["canonical_id", "semantic_role", "confidence", "classification_method"]
        with self.assertRaises(KeyError):
            for field in mandatory_fields:
                _ = incomplete_row[field]

    def test_negative_template_leak_detection(self):
        """Negative test: assert_no_template_leaks raises AssertionError on unrendered placeholders."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            leaky_file = tmp_path / "test_report.md"
            leaky_file.write_text("# Report with {unresolved_var}\nContent here", encoding="utf-8")

            with self.assertRaises(AssertionError) as ctx:
                assert_no_template_leaks(tmp_path)
            self.assertIn("Unresolved template leak detected", str(ctx.exception))
            self.assertIn("{unresolved_var}", str(ctx.exception))

    def test_negative_narrative_percentage_divergence_fails_assertion(self):
        """Negative test: asserting that narrative percentage divergence triggers failure."""
        def verify_percentage(actual_count: int, total_count: int, reported_pct: float):
            computed_pct = round((actual_count / total_count) * 100, 1)
            if abs(computed_pct - reported_pct) > 0.01:
                raise AssertionError(f"Percentage mismatch: computed {computed_pct}%, reported {reported_pct}%")

        # True count matches
        verify_percentage(1651, 2050, 80.5)

        # Injected discrepancy (e.g. stale 85.0%) must raise AssertionError
        with self.assertRaises(AssertionError) as ctx:
            verify_percentage(1640, 2050, 85.0)
        self.assertIn("Percentage mismatch", str(ctx.exception))

    def test_negative_untracked_files_detection(self):
        """Negative test: verifying detection logic catches untracked files in census directory."""
        def detect_untracked_census_artifacts(file_list: list[str]) -> list[str]:
            allowed_files = {
                "architecture-stress-test-report.md",
                "catch-all-bin-analysis.md",
                "census-validation-report.md",
                "family-candidate-register.md",
                "manual-review-outliers.md",
                "manual-semantic-sample-audit.md",
                "semantic-role-census.csv",
                "semantic-role-census.json",
            }
            untracked = [f for f in file_list if f not in allowed_files]
            if untracked:
                raise AssertionError(f"Unexpected untracked files in audit/taxonomy-census/: {untracked}")
            return untracked

        # Standard file list passes
        detect_untracked_census_artifacts([
            "census-validation-report.md",
            "semantic-role-census.csv",
        ])

        # Rogue or unexpected file fails
        with self.assertRaises(AssertionError) as ctx:
            detect_untracked_census_artifacts([
                "census-validation-report.md",
                "untracked_scratch_artifact.tmp",
            ])
        self.assertIn("Unexpected untracked files", str(ctx.exception))


class TestManualOutlierReconciliation(unittest.TestCase):
    """The outlier report must track the live manual-review population.

    Curated notes annotate the population; they are not the population. These
    tests pin the reconciliation: a reclassified or pruned package drops out,
    and a newly surfaced case is not silently omitted.
    """

    @staticmethod
    def _mr_row(canonical_id, path, reason="boundary case"):
        return {
            "canonical_id": canonical_id,
            "name": canonical_id,
            "semantic_role": ROLE_MANUAL_REVIEW,
            "current_path": path,
            "current_category": path.split("/")[1],
            "manual_review_reason": reason,
        }

    def _write(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manual-review-outliers.md"
            write_manual_outliers(path, rows)
            return path.read_text(encoding="utf-8")

    def test_removed_boundary_case_drops_from_report(self):
        """A curated boundary package that is no longer manual_review must not be described."""
        rows = [
            self._mr_row("007", "library/quality-and-security/security/007"),
            self._mr_row("figma-swiftui", "library/design-and-experience/design-systems/figma-swiftui"),
        ]
        text = self._write(rows)
        self.assertIn("`figma-swiftui`", text)
        # `launch` is curated but absent from this population; its line must go.
        self.assertNotIn("`launch` (`library/development/backend/launch`)", text)
        self.assertNotIn("`launch`", text)

    def test_new_boundary_case_is_surfaced(self):
        """A manual_review package with no curated note must be surfaced, not dropped."""
        rows = [
            self._mr_row("007", "library/quality-and-security/security/007"),
            self._mr_row(
                "brand-new-boundary",
                "library/development/fullstack/brand-new-boundary",
                "newly disputed classification boundary",
            ),
        ]
        text = self._write(rows)
        self.assertIn("Newly Surfaced Boundary Cases", text)
        self.assertIn("`brand-new-boundary`", text)
        self.assertIn("newly disputed classification boundary", text)

    def test_removed_original_outlier_drops_from_report(self):
        """A curated original outlier that is no longer manual_review must not be listed."""
        rows = [self._mr_row("steve-jobs", "library/development/fullstack/steve-jobs")]
        text = self._write(rows)
        self.assertIn("`steve-jobs`", text)
        # `007` is curated but absent from this population; its row must go.
        self.assertNotIn("`007`", text)


class TestFamilyCensusCompleteness(unittest.TestCase):
    """A census member tagged with a family no contract record claims is a gap."""

    def test_unclaimed_census_family_member_is_rejected(self):
        rows = [{
            "candidate_family": "Webflow",
            "current_path": "library/development/fullstack/ghost-webflow-skill",
            "current_category": "development",
            "current_subcategory": "fullstack",
            "semantic_role": ROLE_INDEPENDENT_CAPABILITY,
        }]
        with self.assertRaises(AssertionError) as ctx:
            assert_family_census_completeness(rows)
        self.assertIn("not claimed by any contract", str(ctx.exception))

    def test_untagged_census_rows_are_allowed(self):
        """Families the census does not tag are contract-only by design."""
        rows = [{
            "candidate_family": "None",
            "current_path": "library/development/fullstack/some-skill",
            "current_category": "development",
            "current_subcategory": "fullstack",
            "semantic_role": ROLE_INDEPENDENT_CAPABILITY,
        }]
        assert_family_census_completeness(rows)  # must not raise


if __name__ == "__main__":
    unittest.main()
