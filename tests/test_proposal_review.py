import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.proposal_review import (
    edit_proposal,
    get_proposal,
    load_proposals,
    proposal_id,
    set_status,
    upsert_proposal,
)


def merge_payload():
    return {
        "target": "postgres-18",
        "candidate": "install-postgres-18",
        "verdict": "SUPPLEMENT",
        "confidence": "high",
        "claim_diff": {"added": [], "restatement": [], "conflict": [], "unchanged": 3},
        "include_claims": [],
        "skip_claims": [],
        "escalate_claims": [],
        "reasoning": "Adds installation detail",
    }


def granularity_payload():
    return {
        "parent": "postgres-18",
        "candidate": "install-postgres-18",
        "action": "EXTRACT_FACET",
        "new_skill_name": "postgres-install",
        "new_skill_id": "postgres:install",
        "role": "primitive",
        "scope": "Install PostgreSQL 18 only",
        "extracted_claim_ids": ["C1"],
        "parent_remove_claim_ids": ["E1"],
        "parent_composed_of_add": ["postgres:install"],
        "candidate_extends": None,
        "candidate_depends_on": [],
        "reasoning": "Independently shippable facet",
        "confidence": "high",
        "status": "PROPOSED",
    }


class TestProposalStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Path(self.tmp.name) / "proposals.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_upsert_is_idempotent_and_preserves_decision(self):
        first = upsert_proposal(self.store, "merge", merge_payload())
        set_status(self.store, first["id"], "APPROVED", "looks good")
        second = upsert_proposal(self.store, "merge", merge_payload())
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(second["status"], "APPROVED")
        self.assertEqual(len(load_proposals(self.store)), 1)

    def test_changed_payload_gets_new_id(self):
        first = upsert_proposal(self.store, "merge", merge_payload())
        changed = merge_payload()
        changed["reasoning"] = "Different reasoning"
        second = upsert_proposal(self.store, "merge", changed)
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(len(load_proposals(self.store)), 2)

    def test_reject_sets_status_and_note(self):
        proposal = upsert_proposal(self.store, "merge", merge_payload())
        updated = set_status(self.store, proposal["id"], "REJECTED", "not a real overlap")
        self.assertEqual(updated["status"], "REJECTED")
        self.assertEqual(updated["note"], "not a real overlap")

    def test_edit_reopens_proposal_and_increments_revision(self):
        proposal = upsert_proposal(self.store, "granularity", granularity_payload())
        set_status(self.store, proposal["id"], "APPROVED")
        edited_payload = granularity_payload()
        edited_payload["scope"] = "Install PostgreSQL on Ubuntu only"
        edited = edit_proposal(self.store, proposal["id"], edited_payload, "narrower scope")
        self.assertEqual(edited["status"], "PROPOSED")
        self.assertEqual(edited["revision"], 2)
        self.assertNotEqual(edited["id"], proposal["id"])

    def test_invalid_edit_is_rejected(self):
        proposal = upsert_proposal(self.store, "granularity", granularity_payload())
        invalid = granularity_payload()
        invalid["new_skill_id"] = "not-a-valid-id"
        with self.assertRaises(ValueError):
            edit_proposal(self.store, proposal["id"], invalid)
        self.assertEqual(get_proposal(self.store, proposal["id"])["status"], "PROPOSED")

    def test_conflicting_claim_cannot_be_included(self):
        payload = merge_payload()
        payload["claim_diff"]["conflict"] = [{
            "candidate": {"id": "C1", "text": "Use port 5433"},
            "existing": {"id": "E1", "text": "Use port 5432"},
            "reason": "Port mismatch", "severity": "critical",
        }]
        payload["include_claims"] = [{"id": "C1", "text": "Use port 5433"}]
        with self.assertRaises(ValueError):
            upsert_proposal(self.store, "merge", payload)

    def test_applied_proposal_cannot_be_edited(self):
        proposal = upsert_proposal(self.store, "merge", merge_payload())
        set_status(self.store, proposal["id"], "APPLIED")
        edited = merge_payload()
        edited["reasoning"] = "too late"
        with self.assertRaises(ValueError):
            edit_proposal(self.store, proposal["id"], edited)


class TestReviewCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Path(self.tmp.name) / "proposals.json"
        self.proposal = upsert_proposal(self.store, "merge", merge_payload())

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "librarian_review.py"), "--store", str(self.store), *args],
            capture_output=True,
            text=True,
        )

    def test_list_and_show(self):
        listed = self.run_cli("list")
        self.assertEqual(listed.returncode, 0)
        self.assertIn(self.proposal["id"], listed.stdout)
        shown = self.run_cli("show", self.proposal["id"])
        self.assertEqual(shown.returncode, 0)
        self.assertIn("MERGE install-postgres-18 -> postgres-18", shown.stdout)

    def test_approve_and_reject(self):
        approved = self.run_cli("approve", self.proposal["id"], "--note", "ok")
        self.assertEqual(approved.returncode, 0)
        self.assertEqual(get_proposal(self.store, self.proposal["id"])["status"], "APPROVED")
        rejected = self.run_cli("reject", self.proposal["id"], "--note", "changed my mind")
        self.assertEqual(rejected.returncode, 0)
        self.assertEqual(get_proposal(self.store, self.proposal["id"])["status"], "REJECTED")

    def test_edit_from_file(self):
        edited_payload = merge_payload()
        edited_payload["reasoning"] = "Edited reasoning"
        path = Path(self.tmp.name) / "edited.json"
        path.write_text(json.dumps(edited_payload), encoding="utf-8")
        result = self.run_cli("edit", self.proposal["id"], "--file", str(path))
        self.assertEqual(result.returncode, 0)
        proposals = load_proposals(self.store)
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["proposal"]["reasoning"], "Edited reasoning")


if __name__ == "__main__":
    unittest.main()
