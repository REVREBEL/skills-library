"""
Unit and regression tests for the canonical frontmatter parser and schema.

Covers the ZI-07 decisions:
  * one parser replaces the three divergent implementations
  * canonical five fields are name, description, risk, source, license
  * risk and license have closed vocabularies
  * missing risk/source/license warn unless strict
"""

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.frontmatter import (
    CORE_FIELDS,
    REQUIRED_FIELDS,
    SCHEMA_FIELDS,
    parse_frontmatter,
    validate_frontmatter,
)


def wrap(body: str) -> str:
    return f"---\n{body}\n---\n\n# Heading\n"


class TestParseFrontmatter(unittest.TestCase):
    def test_parses_simple_mapping(self):
        fm = parse_frontmatter(wrap("name: demo\ndescription: Does a thing."))
        self.assertEqual(fm["name"], "demo")
        self.assertEqual(fm["description"], "Does a thing.")

    def test_returns_none_without_frontmatter(self):
        self.assertIsNone(parse_frontmatter("# Just markdown\n"))

    def test_returns_none_when_unclosed(self):
        self.assertIsNone(parse_frontmatter("---\nname: demo\n"))

    def test_ignores_comments_and_blank_lines(self):
        fm = parse_frontmatter(wrap("# a comment\n\nname: demo"))
        self.assertEqual(fm, {"name": "demo"})

    def test_strips_surrounding_quotes(self):
        fm = parse_frontmatter(wrap('name: "demo"\ndescription: \'quoted\''))
        self.assertEqual(fm["name"], "demo")
        self.assertEqual(fm["description"], "quoted")

    def test_horizontal_rule_in_body_does_not_truncate(self):
        # The old scanner implementation split on the first '---' anywhere.
        fm = parse_frontmatter(wrap("name: demo\ndescription: ok") + "\n---\n\nbody\n")
        self.assertEqual(fm["name"], "demo")

    def test_value_may_contain_colons(self):
        fm = parse_frontmatter(wrap("description: Use when: migrating."))
        self.assertEqual(fm["description"], "Use when: migrating.")

    def test_empty_string_input(self):
        self.assertIsNone(parse_frontmatter(""))


class TestValidateFrontmatter(unittest.TestCase):
    def complete(self):
        return {
            "name": "demo",
            "description": "Use when demoing.",
            "risk": "safe",
            "source": "community_canonical",
            "license": "MIT",
        }

    def test_complete_frontmatter_is_clean(self):
        errors, warnings = validate_frontmatter(self.complete())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_core_field_is_an_error(self):
        fm = self.complete()
        del fm["name"]
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(errors, ["Frontmatter missing required 'name'"])

    def test_missing_description_is_an_error(self):
        fm = self.complete()
        del fm["description"]
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(errors, ["Frontmatter missing required 'description'"])

    def test_missing_schema_field_warns_by_default(self):
        fm = self.complete()
        del fm["risk"]
        errors, warnings = validate_frontmatter(fm)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["Frontmatter missing required 'risk'"])

    def test_missing_schema_field_errors_when_strict(self):
        fm = self.complete()
        del fm["license"]
        errors, warnings = validate_frontmatter(fm, strict=True)
        self.assertEqual(errors, ["Frontmatter missing required 'license'"])
        self.assertEqual(warnings, [])

    def test_missing_frontmatter_reports_one_error(self):
        errors, warnings = validate_frontmatter(None)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid or missing YAML frontmatter", errors[0])

    def test_risk_vocabulary_is_case_insensitive(self):
        fm = self.complete()
        fm["risk"] = "SAFE"
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(errors, [])

    def test_unknown_risk_value_is_rejected(self):
        fm = self.complete()
        fm["risk"] = "probably-fine"
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(len(errors), 1)
        self.assertIn("risk", errors[0])

    def test_license_file_reference_is_accepted(self):
        fm = self.complete()
        fm["license"] = "Complete terms in LICENSE.txt"
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(errors, [])

    def test_proprietary_license_is_accepted(self):
        fm = self.complete()
        fm["license"] = "proprietary"
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(errors, [])

    def test_source_is_free_form(self):
        fm = self.complete()
        fm["source"] = "hqhq1025/skill-optimizer (MIT)"
        errors, _ = validate_frontmatter(fm)
        self.assertEqual(errors, [])

    def test_every_schema_field_is_checked(self):
        self.assertEqual(CORE_FIELDS, ("name", "description"))
        self.assertEqual(SCHEMA_FIELDS, ("risk", "source", "license"))
        self.assertEqual(
            set(REQUIRED_FIELDS), set(CORE_FIELDS) | set(SCHEMA_FIELDS)
        )


if __name__ == "__main__":
    unittest.main()