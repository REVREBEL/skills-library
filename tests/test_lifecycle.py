"""
Unit and regression tests for the lifecycle vocabulary and transition API.

Covers ZI-07:
  * active / deprecated / retired are all first-class states
  * an explicit state machine rejects illegal transitions
  * invalid status values raise instead of being silently stored
  * ChangeLedger records transitions as append-only evidence
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.ledger import ChangeLedger
from skill_library.object_model import (
    ALLOWED_TRANSITIONS,
    InvariantViolationError,
    ReviewStatus,
    SkillRole,
)
from skill_library.object_model import CapabilityObject
from skill_library.registry_contract import RegistryEntry


def make_skill(status="active", canonical_id="development:demo-skill"):
    return CapabilityObject(
        canonical_id=canonical_id,
        name="Demo Skill",
        role=SkillRole.CAPABILITY,
        status=status,
    )


class TestVocabulary(unittest.TestCase):
    def test_retired_exists(self):
        self.assertEqual(ReviewStatus.RETIRED.value, "retired")

    def test_provisional_exists(self):
        self.assertEqual(ReviewStatus.PROVISIONAL.value, "provisional")

    def test_coerce_accepts_string(self):
        self.assertIs(ReviewStatus.coerce("deprecated"), ReviewStatus.DEPRECATED)

    def test_coerce_is_case_insensitive(self):
        self.assertIs(ReviewStatus.coerce("  RETIRED "), ReviewStatus.RETIRED)

    def test_coerce_rejects_unknown_value(self):
        with self.assertRaises(InvariantViolationError):
            ReviewStatus.coerce("probably-fine")

    def test_coerce_rejects_non_string(self):
        with self.assertRaises(InvariantViolationError):
            ReviewStatus.coerce(42)


class TestTransitions(unittest.TestCase):
    def test_draft_to_active(self):
        skill = make_skill(status="draft")
        record = skill.transition_to("active", reason="released")
        self.assertTrue(record["changed"])
        self.assertIs(skill.status, ReviewStatus.ACTIVE)

    def test_active_to_deprecated(self):
        skill = make_skill()
        record = skill.transition_to("deprecated", reason="superseded")
        self.assertTrue(record["changed"])
        self.assertIs(skill.status, ReviewStatus.DEPRECATED)

    def test_deprecated_to_retired(self):
        skill = make_skill(status="deprecated")
        record = skill.transition_to("retired", reason="removed")
        self.assertTrue(record["changed"])
        self.assertIs(skill.status, ReviewStatus.RETIRED)

    def test_active_to_retired_is_allowed(self):
        skill = make_skill()
        self.assertTrue(skill.transition_to("retired")["changed"])

    def test_retired_is_terminal(self):
        skill = make_skill(status="retired")
        with self.assertRaises(InvariantViolationError):
            skill.transition_to("active")

    def test_active_cannot_return_to_draft(self):
        skill = make_skill()
        with self.assertRaises(InvariantViolationError):
            skill.transition_to("draft")

    def test_unknown_target_raises(self):
        skill = make_skill()
        with self.assertRaises(InvariantViolationError):
            skill.transition_to("sideways")

    def test_same_status_is_a_no_op(self):
        skill = make_skill()
        record = skill.transition_to("active")
        self.assertFalse(record["changed"])
        self.assertIs(skill.status, ReviewStatus.ACTIVE)

    def test_record_carries_provenance(self):
        skill = make_skill(canonical_id="quality-and-security:demo")
        record = skill.transition_to("deprecated", reason="dupe", actor="gary")
        self.assertEqual(record["canonical_id"], "quality-and-security:demo")
        self.assertEqual(record["urn"], "urn:skill:quality-and-security:demo")
        self.assertEqual(record["from_status"], "active")
        self.assertEqual(record["to_status"], "deprecated")
        self.assertEqual(record["reason"], "dupe")
        self.assertEqual(record["actor"], "gary")

    def test_transition_table_covers_every_state(self):
        self.assertEqual(set(ALLOWED_TRANSITIONS), set(ReviewStatus))


class TestConstructionValidation(unittest.TestCase):
    def test_skill_object_rejects_unknown_status(self):
        with self.assertRaises(InvariantViolationError):
            make_skill(status="provisionally-fine")

    def test_skill_object_accepts_provisional(self):
        skill = make_skill(status="provisional")
        self.assertIs(skill.status, ReviewStatus.PROVISIONAL)

    def test_registry_entry_rejects_unknown_status(self):
        with self.assertRaises(InvariantViolationError):
            RegistryEntry(
                canonical_id="development:demo",
                urn="urn:skill:development:demo",
                name="Demo",
                role="capability",
                status="sideways",
            )

    def test_registry_entry_normalizes_status(self):
        entry = RegistryEntry(
            canonical_id="development:demo",
            urn="urn:skill:development:demo",
            name="Demo",
            role="capability",
            status="RETIRED",
        )
        self.assertEqual(entry.status, "retired")


class TestLedgerEvidence(unittest.TestCase):
    def test_transition_is_appended(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = ChangeLedger(ledger_path=os.path.join(tmp, "change-ledger.jsonl"))
            record = ledger.record_lifecycle_transition(
                canonical_id="development:demo",
                from_status="active",
                to_status="deprecated",
                reason="superseded",
                actor="gary",
            )
            self.assertEqual(record["record_type"], "lifecycle_transition")

            with open(ledger.ledger_path, encoding="utf-8") as handle:
                lines = [json.loads(line) for line in handle if line.strip()]
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0]["to_status"], "deprecated")

    def test_filter_by_canonical_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = ChangeLedger(ledger_path=os.path.join(tmp, "change-ledger.jsonl"))
            ledger.record_lifecycle_transition("development:a", "active", "deprecated")
            ledger.record_lifecycle_transition("development:b", "active", "retired")

            transitions = ledger.list_lifecycle_transitions("development:a")
            self.assertEqual(len(transitions), 1)
            self.assertEqual(transitions[0]["canonical_id"], "development:a")

    def test_lifecycle_records_do_not_pollute_change_history_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = ChangeLedger(ledger_path=os.path.join(tmp, "change-ledger.jsonl"))
            ledger.record_change(
                operation="ADD",
                source="manual",
                source_path="x",
                original_name="x",
                canonical_name="x",
                runtime_name="x",
                decision="KEEP",
                category="development",
                subcategory="",
                canonical_path="library/development/x",
                functional_parent="library/development/SKILL.md",
            )
            ledger.record_lifecycle_transition("development:x", "active", "deprecated")

            self.assertEqual(len(ledger.list_changes()), 2)
            self.assertEqual(len(ledger.list_lifecycle_transitions()), 1)


if __name__ == "__main__":
    unittest.main()