"""Tests for the Librarian pipeline.

Verifies the deterministic steps (retrieval, diff) work correctly and the
pipeline orchestration produces the expected structure.
"""

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from skill_library.librarian import (
    Claim,
    ClaimDiff,
    RetrievedCandidate,
    diff_claims,
    retrieve_candidates,
    rerank_candidates,
    decide_merge,
    run_librarian_pipeline,
    _normalize_claim,
)
from skill_library.scanner import CandidatePackage


class TestClaimDiff(unittest.TestCase):
    """Test the deterministic claim diff (set arithmetic)."""

    def test_exact_match_is_unchanged(self):
        c1 = [Claim(id="C1", text="Install via apt", claim_type="operational", source="a")]
        c2 = [Claim(id="C1", text="Install via apt", claim_type="operational", source="b")]
        diff = diff_claims(c1, c2)
        self.assertEqual(diff.unchanged, 1)
        self.assertEqual(len(diff.added), 0)

    def test_new_claim_is_added(self):
        c1 = [Claim(id="C1", text="Install via apt", claim_type="operational", source="a")]
        c2 = [
            Claim(id="C1", text="Install via apt", claim_type="operational", source="b"),
            Claim(id="C5", text="Enable SSL", claim_type="operational", source="b"),
        ]
        diff = diff_claims(c1, c2)
        self.assertEqual(diff.unchanged, 1)
        self.assertEqual(len(diff.added), 1)
        self.assertEqual(diff.added[0].text, "Enable SSL")

    def test_restatement_is_detected(self):
        c1 = [Claim(id="C1", text="Install the database server via apt package manager", claim_type="operational", source="a")]
        c2 = [Claim(id="C1'", text="Install database server using apt package manager", claim_type="operational", source="b")]
        diff = diff_claims(c1, c2)
        # High token overlap should classify as restatement
        self.assertEqual(len(diff.restatement), 1)
        self.assertEqual(len(diff.added), 0)

    def test_empty_skill2(self):
        c1 = [Claim(id="C1", text="Install via apt", claim_type="operational", source="a")]
        diff = diff_claims(c1, [])
        self.assertEqual(len(diff.added), 0)
        self.assertEqual(diff.unchanged, 0)

    def test_empty_skill1(self):
        c2 = [Claim(id="C1", text="Install via apt", claim_type="operational", source="b")]
        diff = diff_claims([], c2)
        self.assertEqual(len(diff.added), 1)

    def test_normalize_claim(self):
        self.assertEqual(_normalize_claim("Install  via APT!"), "install via apt")
        self.assertEqual(_normalize_claim("  Enable SSL  "), "enable ssl")


class TestRetrieval(unittest.TestCase):
    """Test the Dice retrieval stage."""

    def setUp(self):
        self.catalog = [
            {
                "name": "postgres-install",
                "canonical_path": "library/data-and-ai/analytics/postgres-install",
                "tokens": {"postgres", "install", "apt", "database", "server"},
                "description": "Install PostgreSQL database server",
                "body_sample": "Install postgres via apt",
            },
            {
                "name": "postgres-query",
                "canonical_path": "library/data-and-ai/analytics/postgres-query",
                "tokens": {"postgres", "query", "select", "join", "sql"},
                "description": "Run SQL queries on PostgreSQL",
                "body_sample": "Query postgres with select and join",
            },
            {
                "name": "unrelated-skill",
                "canonical_path": "library/development/frontend/unrelated",
                "tokens": {"react", "component", "frontend", "ui"},
                "description": "Build React components",
                "body_sample": "React component development",
            },
        ]

    def test_retrieves_relevant_candidates(self):
        results = retrieve_candidates(
            candidate_name="install-postgres",
            candidate_description="Install PostgreSQL on Ubuntu",
            candidate_body="Install postgres via apt on Ubuntu",
            catalog=self.catalog,
        )
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].name, "postgres-install")

    def test_ignores_low_similarity(self):
        results = retrieve_candidates(
            candidate_name="install-postgres",
            candidate_description="Install PostgreSQL on Ubuntu",
            candidate_body="Install postgres via apt on Ubuntu",
            catalog=self.catalog,
            threshold=0.9,  # Very high threshold
        )
        # Only exact match should pass
        for r in results:
            self.assertGreaterEqual(r.similarity, 0.9)

    def test_respects_limit(self):
        results = retrieve_candidates(
            candidate_name="install-postgres",
            candidate_description="Install PostgreSQL on Ubuntu",
            candidate_body="Install postgres via apt on Ubuntu",
            catalog=self.catalog,
            limit=1,
        )
        self.assertLessEqual(len(results), 1)


class TestRerank(unittest.TestCase):
    """Test the rerank stage (with no rerank function, should pass through)."""

    def test_no_rerank_fn_preserves_order(self):
        candidates = [
            RetrievedCandidate(name="a", canonical_path="a", similarity=0.9, description="a", body_sample=""),
            RetrievedCandidate(name="b", canonical_path="b", similarity=0.5, description="b", body_sample=""),
        ]
        results = rerank_candidates(query="test", candidates=candidates, rerank_fn=None)
        self.assertEqual(results[0].name, "a")
        self.assertEqual(results[1].name, "b")

    def test_rerank_fn_reorders(self):
        candidates = [
            RetrievedCandidate(name="a", canonical_path="a", similarity=0.9, description="a", body_sample=""),
            RetrievedCandidate(name="b", canonical_path="b", similarity=0.5, description="b", body_sample=""),
        ]
        # Mock rerank: b is more relevant
        def mock_rerank(query, passages):
            return [(0, 0.1), (1, 0.9)]  # a low, b high

        results = rerank_candidates(query="test", candidates=candidates, rerank_fn=mock_rerank)
        self.assertEqual(results[0].name, "b")
        self.assertEqual(results[1].name, "a")


class TestMergeDecision(unittest.TestCase):
    """Test the merge decision stage (with default, no AI)."""

    def test_default_includes_added_claims(self):
        diff = ClaimDiff(
            added=[Claim(id="C5", text="Enable SSL", claim_type="operational", source="b")],
            restatement=[],
            conflict=[],
            unchanged=3,
        )
        proposal = decide_merge("skill-1", "skill-2", diff, decide_fn=None)
        self.assertEqual(proposal.verdict, "SUPPLEMENT")
        self.assertEqual(proposal.confidence, "high")
        self.assertEqual(len(proposal.include_claims), 1)
        self.assertEqual(proposal.include_claims[0].text, "Enable SSL")

    def test_default_skips_restatement(self):
        diff = ClaimDiff(
            added=[],
            restatement=[Claim(id="C1'", text="Install via apt", claim_type="operational", source="b")],
            conflict=[],
            unchanged=3,
        )
        proposal = decide_merge("skill-1", "skill-2", diff, decide_fn=None)
        self.assertEqual(len(proposal.include_claims), 0)
        self.assertEqual(len(proposal.skip_claims), 1)

    def test_custom_decide_fn(self):
        diff = ClaimDiff(
            added=[
                Claim(id="C5", text="Enable SSL", claim_type="operational", source="b"),
                Claim(id="C6", text="Set max_connections", claim_type="operational", source="b"),
            ],
            restatement=[],
            conflict=[],
            unchanged=3,
        )

        def mock_decide(s1, s2, d):
            return {
                "verdict": "SUPPLEMENT",
                "confidence": "medium",
                "include_claims": ["C5"],  # Only include C5
                "skip_claims": ["C6"],  # Skip C6
                "escalate_claims": [],
                "reasoning": "C5 adds value, C6 is too specific.",
            }

        proposal = decide_merge("skill-1", "skill-2", diff, decide_fn=mock_decide)
        self.assertEqual(proposal.confidence, "medium")
        self.assertEqual(len(proposal.include_claims), 1)
        self.assertEqual(proposal.include_claims[0].id, "C5")
        self.assertEqual(len(proposal.skip_claims), 1)
        self.assertEqual(proposal.skip_claims[0].id, "C6")


class TestPipeline(unittest.TestCase):
    """Test the full pipeline orchestration."""

    def setUp(self):
        self.catalog = [
            {
                "name": "postgres-install",
                "canonical_path": "library/data-and-ai/analytics/postgres-install",
                "tokens": {"postgres", "install", "apt", "database"},
                "description": "Install PostgreSQL",
                "body_sample": "Install postgres via apt",
            },
        ]

    def test_new_skill_no_matches(self):
        candidate = CandidatePackage(
            name="brand-new-skill",
            source_dir="/tmp/test",
            description="A completely new skill about nothing",
            body_sample="This skill does something entirely different",
        )
        result = run_librarian_pipeline(
            candidate=candidate,
            catalog=self.catalog,
            extract_fn=None,
            rerank_fn=None,
            decide_fn=None,
        )
        self.assertEqual(result["recommended_action"], "NEW")

    def test_duplicate_skill(self):
        candidate = CandidatePackage(
            name="install-postgres-18",
            source_dir="/tmp/test",
            description="Install PostgreSQL database server",
            body_sample="Install postgres via apt",
        )
        result = run_librarian_pipeline(
            candidate=candidate,
            catalog=self.catalog,
            extract_fn=None,
            rerank_fn=None,
            decide_fn=None,
        )
        self.assertGreater(len(result["retrieved"]), 0)
        self.assertIn(result["recommended_action"], ("SUPPLEMENT", "REVIEW"))


if __name__ == "__main__":
    unittest.main()