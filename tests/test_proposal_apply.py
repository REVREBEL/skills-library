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

from skill_library.librarian import Claim
from skill_library.librarian_ai import render_frontmatter
from skill_library.proposal_apply import (
    apply_proposal,
    preflight_proposal,
    rollback,
    validate_test_library,
)
from skill_library.proposal_review import get_proposal, set_status, upsert_proposal


def metadata():
    return {
        "role": "workflow", "applications": ["postgres"], "keywords": ["postgres"],
        "tags": ["database"], "depends_on": [], "composed_of": [], "extends": None,
        "adapts": None, "aliased_to": None,
        "execution_provider": {"default": "prompt_template", "supported": []},
        "risk": "low", "side_effects": "read-only",
    }


def make_library(root: Path):
    parent = root / "development" / "backend" / "postgres-18"
    parent.mkdir(parents=True)
    fm = render_frontmatter("postgres-18", "Install and query PostgreSQL", metadata(), "development:postgres-18")
    (parent / "SKILL.md").write_text(
        fm + "\n# PostgreSQL\n\n- Install PostgreSQL 18\n- Run SQL queries\n",
        encoding="utf-8",
    )
    (root / "runtime-manifest.json").write_text(json.dumps({
        "version": "1.0",
        "skills": {"postgres-18": {"canonical_path": "development/backend/postgres-18"}},
    }, indent=2), encoding="utf-8")
    (root / "change-ledger.jsonl").write_text("", encoding="utf-8")


def merge_payload():
    return {
        "target": "postgres-18",
        "candidate": "postgres-install",
        "verdict": "SUPPLEMENT",
        "confidence": "high",
        "claim_diff": {"added": [], "restatement": [], "conflict": [], "unchanged": 1},
        "include_claims": [{"id": "C1", "text": "Enable SSL", "type": "operational", "source": "postgres-install"}],
        "skip_claims": [],
        "escalate_claims": [],
        "reasoning": "Adds SSL detail",
    }


def granularity_payload(source: Path):
    child_claim = Claim(id="C1", text="Install PostgreSQL 18", claim_type="operational", source="postgres-install")
    parent_claim = Claim(id="E1", text="Install PostgreSQL 18", claim_type="operational", source="postgres-18")
    child_meta = metadata()
    child_meta["role"] = "primitive"
    return {
        "parent": "postgres-18",
        "candidate": "postgres-install",
        "action": "EXTRACT_FACET",
        "new_skill_name": "postgres-install",
        "new_skill_id": "postgres:install",
        "role": "primitive",
        "scope": "Install PostgreSQL 18 only",
        "extracted_claim_ids": ["C1"],
        "parent_remove_claim_ids": ["E1"],
        "extracted_claims": [child_claim.to_dict()],
        "parent_remove_claims": [parent_claim.to_dict()],
        "parent_composed_of_add": ["postgres:install"],
        "candidate_extends": None,
        "candidate_depends_on": [],
        "reasoning": "Independently shippable facet",
        "confidence": "high",
        "status": "PROPOSED",
        "source_path": str(source),
        "placement": {"category": "development", "subcategory": "backend"},
        "metadata": child_meta,
    }


class TestControlledApply(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.library = self.root / "test-library"
        self.store = self.library / "proposals.json"
        self.snapshots = self.root / "test-library-snapshots"
        make_library(self.library)

    def tearDown(self):
        self.tmp.cleanup()

    def approve(self, kind, payload):
        proposal = upsert_proposal(self.store, kind, payload)
        return set_status(self.store, proposal["id"], "APPROVED", "approved for test")

    def test_real_library_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_test_library(REPO_ROOT / "library", REPO_ROOT / "library")

    def test_unapproved_proposal_is_not_applied(self):
        proposal = upsert_proposal(self.store, "merge", merge_payload())
        with self.assertRaises(ValueError):
            apply_proposal(self.library, self.store, self.snapshots, proposal)
        self.assertFalse(self.snapshots.exists())

    def test_merge_apply_and_rollback(self):
        proposal = self.approve("merge", merge_payload())
        target = self.library / "development" / "backend" / "postgres-18" / "SKILL.md"
        before = target.read_text(encoding="utf-8")
        snapshot = apply_proposal(self.library, self.store, self.snapshots, proposal)
        self.assertIn("Enable SSL", target.read_text(encoding="utf-8"))
        self.assertEqual(get_proposal(self.store, proposal["id"])["status"], "APPLIED")
        ledger = (self.library / "change-ledger.jsonl").read_text(encoding="utf-8")
        self.assertIn("LIBRARIAN_APPLY", ledger)

        rollback(self.library, self.store, self.snapshots, snapshot.name)
        self.assertEqual(target.read_text(encoding="utf-8"), before)
        self.assertEqual(get_proposal(self.store, proposal["id"])["status"], "ROLLED_BACK")

    def test_split_apply_updates_parent_and_child(self):
        source = self.root / "intake" / "postgres-install"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(
            '---\nname: "postgres-install"\ndescription: "Install PostgreSQL 18"\nlicense: "MIT"\n---\n'
            "# Install\n\n- Install PostgreSQL 18\n- Start the service\n",
            encoding="utf-8",
        )
        (source / "references").mkdir()
        (source / "references" / "install.md").write_text("# Install reference\n", encoding="utf-8")
        (source / "assets").mkdir()
        (source / "assets" / "service.conf").write_text("enabled=true\n", encoding="utf-8")
        proposal = self.approve("granularity", granularity_payload(source))
        snapshot = apply_proposal(self.library, self.store, self.snapshots, proposal)

        parent = self.library / "development" / "backend" / "postgres-18" / "SKILL.md"
        child = self.library / "development" / "backend" / "postgres-install" / "SKILL.md"
        self.assertTrue(child.exists())
        parent_text = parent.read_text(encoding="utf-8")
        self.assertNotIn("- Install PostgreSQL 18", parent_text)
        self.assertIn("- Run SQL queries", parent_text)
        self.assertIn("composed_of:", parent_text)
        self.assertIn("- postgres:install", parent_text)
        self.assertIn('canonical_id: "postgres:install"', child.read_text(encoding="utf-8"))
        self.assertEqual((child.parent / "references" / "install.md").read_text(encoding="utf-8"), "# Install reference\n")
        self.assertEqual((child.parent / "assets" / "service.conf").read_text(encoding="utf-8"), "enabled=true\n")

        rollback(self.library, self.store, self.snapshots, snapshot.name)
        self.assertFalse(child.exists())
        self.assertIn("- Install PostgreSQL 18", parent.read_text(encoding="utf-8"))

    def test_failed_split_restores_library(self):
        source = self.root / "intake" / "postgres-install"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text("# Install\n", encoding="utf-8")
        payload = granularity_payload(source)
        payload["parent_remove_claims"][0]["text"] = "A claim that is not in the parent body"
        proposal = self.approve("granularity", payload)
        parent = self.library / "development" / "backend" / "postgres-18" / "SKILL.md"
        before = parent.read_text(encoding="utf-8")

        with self.assertRaises(ValueError):
            apply_proposal(self.library, self.store, self.snapshots, proposal)
        self.assertEqual(parent.read_text(encoding="utf-8"), before)
        self.assertEqual(get_proposal(self.store, proposal["id"])["status"], "APPROVED")
        self.assertFalse((self.library / "development" / "backend" / "postgres-install").exists())


class TestApplyCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.library = self.root / "test-library"
        self.store = self.library / "proposals.json"
        self.snapshots = self.root / "test-library-snapshots"
        make_library(self.library)
        self.proposal = upsert_proposal(self.store, "merge", merge_payload())
        set_status(self.store, self.proposal["id"], "APPROVED")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "librarian_apply.py"),
             "--store", str(self.store), "--library", str(self.library),
             "--snapshots", str(self.snapshots), *args],
            capture_output=True, text=True,
        )

    def test_plan_apply_snapshots_rollback(self):
        planned = self.run_cli("plan", "--all")
        self.assertEqual(planned.returncode, 0)
        self.assertIn("READY", planned.stdout)
        applied = self.run_cli("apply", "--all")
        self.assertEqual(applied.returncode, 0)
        self.assertIn("APPLIED", applied.stdout)
        snapshots = self.run_cli("snapshots")
        self.assertEqual(snapshots.returncode, 0)
        snapshot_id = snapshots.stdout.strip().splitlines()[0]
        restored = self.run_cli("rollback", snapshot_id)
        self.assertEqual(restored.returncode, 0)
        self.assertEqual(get_proposal(self.store, self.proposal["id"])["status"], "ROLLED_BACK")


if __name__ == "__main__":
    unittest.main()
