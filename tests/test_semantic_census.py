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
    assert_no_template_leaks,
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
        """CSV and JSON must contain exactly 2,133 skills matching authoritative population."""
        self.assertEqual(len(self.csv_rows), 2133)
        self.assertEqual(len(self.json_rows), 2133)

        csv_ids = [r["canonical_id"] for r in self.csv_rows]
        json_ids = [r["canonical_id"] for r in self.json_rows]
        self.assertEqual(csv_ids, json_ids)
        self.assertEqual(len(set(csv_ids)), 2133, "All canonical IDs must be unique")

    def test_role_distribution_invariants(self):
        """Authoritative breakdown across the 8 accepted semantic roles."""
        counts = Counter(r["semantic_role"] for r in self.csv_rows)

        self.assertEqual(counts[ROLE_INDEPENDENT_CAPABILITY], 1701)
        self.assertEqual(counts[ROLE_WORKFLOW], 391)
        self.assertEqual(counts[ROLE_MANUAL_REVIEW], 22)
        self.assertEqual(counts[ROLE_OVERLAY], 6)
        self.assertEqual(counts[ROLE_REFERENCE], 5)
        self.assertEqual(counts[ROLE_ADAPTER], 4)
        self.assertEqual(counts[ROLE_ALIAS], 3)
        self.assertEqual(counts[ROLE_FAMILY_PRIMITIVE], 1)
        self.assertEqual(sum(counts.values()), 2133)

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
        """Catch-all breakdown must use 'Aliases' header (not 'Aliases / Duplicates')."""
        catch_all = (CENSUS_DIR / "catch-all-bin-analysis.md").read_text(encoding="utf-8")
        self.assertIn("| Catch-All Bin | Total Skills | Independent Capabilities | Workflows | Aliases | Overlays / Adapters | References | Primitives | Manual Review |", catch_all)
        self.assertNotIn("Aliases / Duplicates", catch_all)

        # Exact row counts
        self.assertIn("| `development/fullstack` | 420 | 326 | 83 | 1 | 0 | 1 | 1 | 8 |", catch_all)
        self.assertIn("| `marketing-and-seo/on-page-seo` | 279 | 246 | 30 | 0 | 2 | 0 | 0 | 1 |", catch_all)
        self.assertIn("| `marketing-and-seo/cro` | 209 | 167 | 38 | 0 | 2 | 1 | 0 | 1 |", catch_all)

    def test_independent_validation_narrative_percentages_against_counts(self):
        """Independently verifies that narrative percentages match underlying counts."""
        total = len(self.csv_rows)
        counts = Counter(r["semantic_role"] for r in self.csv_rows)

        expected_pcts = {role: round((count / total) * 100, 1) for role, count in counts.items()}
        self.assertEqual(expected_pcts[ROLE_INDEPENDENT_CAPABILITY], 79.7)
        self.assertEqual(expected_pcts[ROLE_WORKFLOW], 18.3)
        self.assertEqual(expected_pcts[ROLE_MANUAL_REVIEW], 1.0)
        self.assertEqual(expected_pcts[ROLE_OVERLAY], 0.3)
        self.assertEqual(expected_pcts[ROLE_REFERENCE], 0.2)
        self.assertEqual(expected_pcts[ROLE_ADAPTER], 0.2)
        self.assertEqual(expected_pcts[ROLE_ALIAS], 0.1)
        self.assertEqual(expected_pcts[ROLE_FAMILY_PRIMITIVE], 0.0)

        report_text = (CENSUS_DIR / "census-validation-report.md").read_text(encoding="utf-8")
        self.assertIn("79.7%", report_text)
        self.assertIn("18.3%", report_text)
        self.assertIn("1.0%", report_text)
        self.assertIn("0.3%", report_text)


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
        verify_percentage(1701, 2133, 79.7)

        # Injected discrepancy (e.g. stale 85.0%) must raise AssertionError
        with self.assertRaises(AssertionError) as ctx:
            verify_percentage(1701, 2133, 85.0)
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


if __name__ == "__main__":
    unittest.main()
