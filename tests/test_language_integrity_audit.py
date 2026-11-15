"""
Unit and Invariant Test Suite for SKIL-11 (ZI-06) Language, Integrity & Exposure Audit.
"""

import csv
import json
import unittest
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
ZERO_INDEX_DIR = REPO_ROOT / "audit" / "zero-index" / "SKIL-11"

class TestLanguageIntegrityAuditInvariants(unittest.TestCase):
    """Test invariants of SKIL-11 audit outputs."""

    @classmethod
    def setUpClass(cls):
        cls.lang_csv_path = ZERO_INDEX_DIR / "language-audit.csv"
        cls.res_csv_path = ZERO_INDEX_DIR / "integrity-and-exposure-findings.csv"
        cls.q_csv_path = ZERO_INDEX_DIR / "quarantine-candidates.csv"
        cls.summary_json_path = ZERO_INDEX_DIR / "language-integrity-exposure-summary.json"

        with open(cls.lang_csv_path, mode="r", encoding="utf-8") as f:
            cls.lang_rows = list(csv.DictReader(f))

        with open(cls.res_csv_path, mode="r", encoding="utf-8") as f:
            cls.res_rows = list(csv.DictReader(f))

        with open(cls.q_csv_path, mode="r", encoding="utf-8") as f:
            cls.q_rows = list(csv.DictReader(f))

        with open(cls.summary_json_path, mode="r", encoding="utf-8") as f:
            cls.summary_json = json.load(f)

    def test_language_audit_population_coverage(self):
        """Language audit must cover exactly 2,133 skills with unique canonical IDs."""
        self.assertEqual(len(self.lang_rows), 2133)
        cids = [r["canonical_id"] for r in self.lang_rows]
        self.assertEqual(len(set(cids)), 2133)

        valid_classifications = {
            "english_native", "mixed_english_dominant", "foreign_language_dominant",
            "mixed_foreign_metadata", "mixed_foreign_body"
        }
        for r in self.lang_rows:
            self.assertIn(r["language_classification"], valid_classifications)
            self.assertIn(r["proposed_disposition"], {"CANONICAL_ACTIVE", "TRANSLATE_RECOMMENDED", "TRANSLATE_OR_QUARANTINE"})

    def test_resource_integrity_and_ast_safety(self):
        """Resource audit must verify 8,172 resources with 0 AST syntax errors and 0 leaks."""
        self.assertEqual(len(self.res_rows), 8172)
        ast_errors = [r for r in self.res_rows if r["ast_syntax_status"] == "ast_syntax_error"]
        self.assertEqual(len(ast_errors), 0, "All Python scripts must be syntactically valid")

        secret_leaks = [r for r in self.res_rows if r["leak_status"] == "secret_leak_flagged"]
        self.assertEqual(len(secret_leaks), 0, "Must have zero unclassified secret leaks")

        workstation_leaks = [r for r in self.res_rows if r["leak_status"] == "workstation_path_leak"]
        self.assertEqual(len(workstation_leaks), 0, "Must have zero unclassified workstation path leaks")

    def test_quarantine_reconciliation(self):
        """Quarantine candidates must reconcile translation, persona, and tech-coupling criteria."""
        self.assertGreater(len(self.q_rows), 0)
        reasons = Counter(r["quarantine_reason_class"] for r in self.q_rows)
        self.assertIn("foreign_language_dominant", reasons)
        self.assertIn("persona_or_prompt_outlier", reasons)

    def test_summary_json_parity(self):
        """Summary JSON metrics must exactly match underlying CSV row counts."""
        self.assertEqual(self.summary_json["audit_metadata"]["population_audited"], len(self.lang_rows))
        self.assertEqual(self.summary_json["audit_metadata"]["total_resources_audited"], len(self.res_rows))
        self.assertEqual(self.summary_json["total_quarantine_candidates"], len(self.q_rows))

    def test_zero_template_leaks(self):
        """All markdown and text deliverables must have zero template leaks."""
        for md_file in [ZERO_INDEX_DIR / "commands-and-tests.md", ZERO_INDEX_DIR / "summary.md"]:
            content = md_file.read_text(encoding="utf-8")
            self.assertNotIn("TODO", content)
            self.assertNotIn("TBD", content)
            self.assertNotIn("FIXME", content)
            self.assertNotIn("{{", content)
            self.assertNotIn("}}", content)

if __name__ == "__main__":
    unittest.main()
