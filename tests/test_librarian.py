"""Tests for the Librarian pipeline.

Verifies the deterministic steps (retrieval, diff) work correctly and the
pipeline orchestration produces the expected structure.
"""

import json
import sys
import tempfile
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
            RetrievedCandidate(name="a", canonical_path="a", similarity=0.9, description="a", body_sample="Body A"),
            RetrievedCandidate(name="b", canonical_path="b", similarity=0.5, description="b", body_sample="Body B"),
        ]
        results = rerank_candidates(query="test", candidates=candidates, rerank_fn=None)
        self.assertEqual(results[0].name, "a")
        self.assertEqual(results[1].name, "b")
        self.assertEqual(results[0].body_sample, "Body A")

    def test_rerank_fn_reorders(self):
        candidates = [
            RetrievedCandidate(name="a", canonical_path="a", similarity=0.9, description="a", body_sample="Body A"),
            RetrievedCandidate(name="b", canonical_path="b", similarity=0.5, description="b", body_sample="Body B"),
        ]
        # Mock rerank: b is more relevant
        def mock_rerank(query, passages):
            return [(0, 0.1), (1, 0.9)]  # a low, b high

        results = rerank_candidates(query="test", candidates=candidates, rerank_fn=mock_rerank)
        self.assertEqual(results[0].name, "b")
        self.assertEqual(results[1].name, "a")
        self.assertEqual(results[0].body_sample, "Body B")


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


class TestOpenCodeFallback(unittest.TestCase):
    """Test the model fallback chain without making real AI calls."""

    def test_falls_back_after_rate_limit(self):
        from unittest.mock import patch, MagicMock
        from skill_library import librarian_ai
        librarian_ai._MODEL_COOLDOWNS.clear()

        failed = MagicMock(returncode=1, stdout="", stderr="429 rate limit")
        succeeded = MagicMock(returncode=0, stdout="> model\nOK\n", stderr="")

        with patch("skill_library.librarian_ai._find_opencode", return_value="/fake/opencode"), \
             patch("skill_library.librarian_ai.subprocess.run", side_effect=[failed, succeeded]) as run:
            result = librarian_ai.opencode_run("test prompt", models=["model-a", "model-b"])

        self.assertEqual(result, "OK")
        self.assertEqual(run.call_count, 2)
        first_args = run.call_args_list[0].args[0]
        second_args = run.call_args_list[1].args[0]
        self.assertIn("model-a", first_args)
        self.assertIn("model-b", second_args)

    def test_raises_when_all_models_fail(self):
        from unittest.mock import patch, MagicMock
        from skill_library import librarian_ai
        librarian_ai._MODEL_COOLDOWNS.clear()

        failed = MagicMock(returncode=1, stdout="", stderr="provider error")
        with patch("skill_library.librarian_ai._find_opencode", return_value="/fake/opencode"), \
             patch("skill_library.librarian_ai.subprocess.run", return_value=failed):
            with self.assertRaises(RuntimeError) as ctx:
                librarian_ai.opencode_run("test prompt", models=["model-a", "model-b"])
        self.assertIn("All OpenCode models failed", str(ctx.exception))


class TestTestLibraryPackageCopy(unittest.TestCase):
    """Installed candidates retain every bundled resource and the source stays intact."""

    def test_writer_copies_complete_package_and_replaces_only_skill_body(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "intake" / "database-design"
            source.mkdir(parents=True)
            original_skill = '---\nname: "database-design"\n---\n# Original\n'
            (source / "SKILL.md").write_text(original_skill, encoding="utf-8")
            resources = {
                "references/schema.md": "# Schema\n",
                "assets/templates/migration.sql": "CREATE TABLE example (id INTEGER);\n",
                "scripts/validate.py": "print('validate')\n",
                "README.md": "Package notes\n",
            }
            for relative, content in resources.items():
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            library = root / "test-library"
            library.mkdir()
            manifest = library / "runtime-manifest.json"
            ledger = library / "change-ledger.jsonl"
            manifest.write_text(json.dumps({"version": "1.0", "skills": {}}), encoding="utf-8")
            ledger.write_text("", encoding="utf-8")
            replacement = '---\nname: "database-design"\n---\n# Curated\n'

            with patch.object(pipe, "TEST_LIBRARY", library), \
                 patch.object(pipe, "TEST_MANIFEST", manifest), \
                 patch.object(pipe, "TEST_LEDGER", ledger):
                destination = pipe.write_skill_to_test_library(
                    "database-design", replacement, "Database design",
                    "data-and-ai", "analytics", "capability", str(source),
                )

            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), replacement)
            for relative, content in resources.items():
                self.assertEqual((destination / relative).read_text(encoding="utf-8"), content)
            self.assertEqual((source / "SKILL.md").read_text(encoding="utf-8"), original_skill)
            self.assertEqual(json.loads(manifest.read_text(encoding="utf-8"))["skills"]["database-design"]["role"], "capability")
            self.assertIn("INSTALL", ledger.read_text(encoding="utf-8"))

    def test_writer_rejects_symlinked_resources(self):
        import librarian_testpipe as pipe

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "intake" / "linked"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("# Linked\n", encoding="utf-8")
            outside = root / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            (source / "references").mkdir()
            (source / "references" / "escape.md").symlink_to(outside)

            with self.assertRaises(ValueError):
                pipe.copy_candidate_package(source, root / "test-library" / "linked", "# Curated\n")
            self.assertFalse((root / "test-library").exists())

    def test_proposal_persistence_failure_does_not_abort_remaining_candidates(self):
        import io
        from unittest.mock import patch
        import librarian_testpipe as pipe

        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(pipe, "PROPOSALS_FILE", Path(tmp) / "proposals.json"), \
             patch("skill_library.proposal_review.upsert_proposal", side_effect=ValueError("malformed proposal")), \
             patch("sys.stderr", new=io.StringIO()):
            pipe.record_review_proposals({"proposals": [{}], "granularity": [{}]})

    def test_dry_run_rejects_reset_without_touching_library(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe

        with tempfile.TemporaryDirectory() as tmp:
            library = Path(tmp) / "test-library"
            library.mkdir()
            sentinel = library / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with patch("sys.argv", ["librarian_testpipe.py", "--dry-run", "--reset"]), \
                 patch.object(pipe, "TEST_LIBRARY", library):
                with self.assertRaises(SystemExit) as error:
                    pipe.main()
            self.assertEqual(error.exception.code, 2)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")


class TestRelationshipGate(unittest.TestCase):
    """The pipeline must classify before attempting a merge."""

    def _candidate(self, name="new-skill"):
        return CandidatePackage(
            name=name,
            source_dir="/tmp/test",
            description="A new capability",
            body_sample="Do the thing",
        )

    def test_no_matches_is_new_without_claim_extraction(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe

        with patch.object(pipe, "retrieve_candidates", return_value=[]), \
             patch.object(pipe, "extract_claims") as extract:
            result = pipe.process_candidate(self._candidate(), catalog=[])
        self.assertEqual(result["verdict"], "NEW")
        extract.assert_not_called()

    def test_self_match_is_alias_without_claim_extraction(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe
        from skill_library.librarian import RerankedCandidate, RetrievedCandidate

        retrieved = RetrievedCandidate(
            name="new-skill", canonical_path="library/x/new-skill",
            similarity=1.0, description="Same skill", body_sample="",
        )
        match = RerankedCandidate(
            name="new-skill", canonical_path="library/x/new-skill",
            rerank_score=0.3, dice_similarity=1.0, description="Same skill",
        )
        with patch.object(pipe, "retrieve_candidates", return_value=[retrieved]), \
             patch.object(pipe, "rerank_candidates", return_value=[match]), \
             patch.object(pipe, "extract_claims") as extract:
            result = pipe.process_candidate(self._candidate(), catalog=[])
        self.assertEqual(result["verdict"], "ALIAS")
        extract.assert_not_called()

    def test_claim_extraction_receives_candidate_and_existing_bodies_after_rerank(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe
        from skill_library.librarian import RetrievedCandidate

        candidate = CandidatePackage(
            name="new-skill", source_dir="/tmp/test",
            description="A new capability", body_sample="Candidate body",
        )
        retrieved = RetrievedCandidate(
            name="existing-skill", canonical_path="library/x/existing-skill",
            similarity=0.7, description="Existing capability", body_sample="Existing body",
        )
        candidate_claim = Claim(id="C1", text="Candidate instruction", claim_type="operational", source="new-skill")
        existing_claim = Claim(id="E1", text="Existing instruction", claim_type="operational", source="existing-skill")

        with patch.object(pipe, "retrieve_candidates", return_value=[retrieved]), \
             patch.object(pipe, "rerank_with_openrouter", return_value=[(0, 0.9)]), \
             patch.object(pipe, "extract_claims", side_effect=[[candidate_claim], [existing_claim]]) as extract, \
             patch("skill_library.librarian_ai.detect_semantic_conflicts_opencode", return_value=[]), \
             patch.object(pipe, "decide_merge_opencode", return_value={
                 "verdict": "SUPPLEMENT", "confidence": "high",
                 "include_claims": [], "skip_claims": [], "escalate_claims": [],
                 "reasoning": "test decision",
             }):
            result = pipe.process_candidate(candidate, catalog=[])

        self.assertEqual(result["verdict"], "SUPPLEMENT")
        self.assertEqual(
            [call.kwargs["skill_body"] for call in extract.call_args_list],
            ["Candidate body", "Existing body"],
        )

    def test_claim_extraction_receives_existing_body_after_rerank_fallback(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe
        from skill_library.librarian import RetrievedCandidate

        candidate = CandidatePackage(
            name="new-skill", source_dir="/tmp/test",
            description="A new capability", body_sample="Candidate body",
        )
        retrieved = RetrievedCandidate(
            name="existing-skill", canonical_path="library/x/existing-skill",
            similarity=0.7, description="Existing capability", body_sample="Existing body",
        )
        candidate_claim = Claim(id="C1", text="Candidate instruction", claim_type="operational", source="new-skill")
        existing_claim = Claim(id="E1", text="Existing instruction", claim_type="operational", source="existing-skill")

        with patch.object(pipe, "retrieve_candidates", return_value=[retrieved]), \
             patch.object(pipe, "rerank_with_openrouter", side_effect=RuntimeError("quota exhausted")), \
             patch.object(pipe, "extract_claims", side_effect=[[candidate_claim], [existing_claim]]) as extract, \
             patch("skill_library.librarian_ai.detect_semantic_conflicts_opencode", return_value=[]), \
             patch.object(pipe, "decide_merge_opencode", return_value={
                 "verdict": "SUPPLEMENT", "confidence": "high",
                 "include_claims": [], "skip_claims": [], "escalate_claims": [],
                 "reasoning": "test decision",
             }):
            result = pipe.process_candidate(candidate, catalog=[])

        self.assertEqual(result["verdict"], "SUPPLEMENT")
        self.assertEqual(
            [call.kwargs["skill_body"] for call in extract.call_args_list],
            ["Candidate body", "Existing body"],
        )

    def test_semantic_conflict_failure_returns_review_without_merging(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe
        from skill_library.librarian import RetrievedCandidate

        candidate = CandidatePackage(
            name="new-skill", source_dir="/tmp/test",
            description="A new capability", body_sample="Candidate body",
        )
        retrieved = RetrievedCandidate(
            name="existing-skill", canonical_path="library/x/existing-skill",
            similarity=0.7, description="Existing capability", body_sample="Existing body",
        )
        candidate_claim = Claim(id="C1", text="Candidate instruction", claim_type="operational", source="new-skill")
        existing_claim = Claim(id="E1", text="Existing instruction", claim_type="operational", source="existing-skill")

        with patch.object(pipe, "retrieve_candidates", return_value=[retrieved]), \
             patch.object(pipe, "rerank_with_openrouter", return_value=[(0, 0.9)]), \
             patch.object(pipe, "extract_claims", side_effect=[[candidate_claim], [existing_claim]]), \
             patch("skill_library.librarian_ai.detect_semantic_conflicts_opencode", side_effect=RuntimeError("detector unavailable")), \
             patch.object(pipe, "decide_merge") as merge:
            result = pipe.process_candidate(candidate, catalog=[])

        self.assertEqual(result["verdict"], "REVIEW")
        self.assertEqual(result["proposals"], [])
        merge.assert_not_called()

    def test_unrelated_gate_is_new_without_claim_extraction(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe
        from skill_library.librarian import RerankedCandidate, RetrievedCandidate

        retrieved = RetrievedCandidate(
            name="other-skill", canonical_path="library/x/other-skill",
            similarity=0.3, description="Different skill", body_sample="",
        )
        match = RerankedCandidate(
            name="other-skill", canonical_path="library/x/other-skill",
            rerank_score=0.05, dice_similarity=0.3, description="Different skill",
        )
        with patch.object(pipe, "retrieve_candidates", return_value=[retrieved]), \
             patch.object(pipe, "rerank_candidates", return_value=[match]), \
             patch("skill_library.librarian_ai.classify_relationship_opencode",
                   return_value={"relationship": "unrelated", "match": None, "reasoning": "Different scope"}), \
             patch.object(pipe, "extract_claims") as extract:
            result = pipe.process_candidate(self._candidate(), catalog=[])
        self.assertEqual(result["verdict"], "NEW")
        extract.assert_not_called()


class TestSemanticConflicts(unittest.TestCase):
    """True semantic conflicts are structured and cannot be silently merged."""

    def test_apply_semantic_conflicts_moves_claim_out_of_added(self):
        from skill_library.librarian import apply_semantic_conflicts

        existing = Claim(id="E2", text="Use port 5432", claim_type="operational", source="old")
        candidate = Claim(id="C7", text="Use port 5433", claim_type="operational", source="new")
        diff = ClaimDiff(added=[candidate])
        apply_semantic_conflicts(diff, [existing], [{
            "candidate_id": "C7", "existing_id": "E2",
            "reason": "Different port for the same server", "severity": "critical",
        }])
        self.assertEqual(diff.added, [])
        self.assertEqual(len(diff.conflict), 1)
        self.assertEqual(diff.conflict[0].candidate.id, "C7")
        self.assertEqual(diff.conflict[0].existing.id, "E2")
        self.assertEqual(diff.conflict[0].severity, "critical")

    def test_decide_merge_always_escalates_conflicts(self):
        from skill_library.librarian import ClaimConflict, decide_merge

        existing = Claim(id="E2", text="Use port 5432", claim_type="operational", source="old")
        candidate = Claim(id="C7", text="Use port 5433", claim_type="operational", source="new")
        diff = ClaimDiff(conflict=[ClaimConflict(candidate, existing, "Port mismatch", "critical")])

        def bad_decider(s1, s2, d):
            # Model tries to include the conflicting claim anyway.
            return {
                "verdict": "SUPPLEMENT", "confidence": "high",
                "include_claims": ["C7"], "skip_claims": [], "escalate_claims": [],
                "reasoning": "bad model output",
            }

        proposal = decide_merge("old", "new", diff, decide_fn=bad_decider)
        self.assertEqual([c.id for c in proposal.include_claims], [])
        self.assertEqual([c.id for c in proposal.escalate_claims], ["C7"])
        self.assertIn("Port mismatch", proposal.summary())

    def test_conflict_prompt_truncates_only_on_claim_boundaries(self):
        from skill_library.librarian_ai import _format_claims_for_prompt

        claims = [
            Claim(id=f"C{index}", text="x" * 100, claim_type="operational", source="test")
            for index in range(4)
        ]
        formatted = _format_claims_for_prompt(claims, max_chars=250)
        lines = formatted.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines, [f"[{claim.id}] {claim.text}" for claim in claims[:2]])

        long_claim = Claim(id="LONG", text="x" * 500, claim_type="operational", source="test")
        self.assertEqual(_format_claims_for_prompt([long_claim], max_chars=10), f"[LONG] {long_claim.text}")

    def test_detector_parses_valid_response(self):
        from unittest.mock import patch
        from skill_library.librarian_ai import detect_semantic_conflicts_opencode

        existing = Claim(id="E2", text="Use port 5432", claim_type="operational", source="old")
        candidate = Claim(id="C7", text="Use port 5433", claim_type="operational", source="new")
        response = '{"conflicts":[{"candidate_id":"C7","existing_id":"E2","reason":"Port mismatch","severity":"critical"}]}'
        with patch("skill_library.librarian_ai.opencode_run", return_value=response):
            conflicts = detect_semantic_conflicts_opencode([existing], [candidate])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["severity"], "critical")

    def test_detector_rejects_invalid_json(self):
        from unittest.mock import patch
        from skill_library.librarian_ai import detect_semantic_conflicts_opencode

        existing = Claim(id="E2", text="Use port 5432", claim_type="operational", source="old")
        candidate = Claim(id="C7", text="Use port 5433", claim_type="operational", source="new")
        with patch("skill_library.librarian_ai.opencode_run", return_value="not json"):
            with self.assertRaises(RuntimeError):
                detect_semantic_conflicts_opencode([existing], [candidate])


class TestGranularityProposals(unittest.TestCase):
    """Incremental splits are proposed only for concrete, shippable facets."""

    def test_valid_extraction_proposal(self):
        from skill_library.librarian import build_granularity_proposal

        parent = Claim(id="E1", text="Install PostgreSQL", claim_type="operational", source="parent")
        parent2 = Claim(id="E2", text="Run SQL queries", claim_type="operational", source="parent")
        child = Claim(id="C1", text="Install PostgreSQL 18", claim_type="operational", source="child")
        proposal = build_granularity_proposal({
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
            "reasoning": "Independently shippable install facet",
            "confidence": "high",
        }, "postgres-18", "install-postgres-18", [parent, parent2], [child])
        self.assertEqual(proposal.action, "EXTRACT_FACET")
        self.assertEqual(proposal.new_skill_id, "postgres:install")
        self.assertEqual(proposal.to_dict()["status"], "PROPOSED")
        self.assertIn("human approval required", proposal.summary())

    def test_incomplete_extraction_fails_safe(self):
        from skill_library.librarian import build_granularity_proposal

        child = Claim(id="C1", text="Install PostgreSQL", claim_type="operational", source="child")
        proposal = build_granularity_proposal({
            "action": "EXTRACT_FACET",
            "new_skill_name": "postgres-install",
        }, "postgres-18", "install-postgres-18", [], [child])
        self.assertEqual(proposal.action, "NO_SPLIT")
        self.assertEqual(proposal.confidence, "low")

    def test_ai_proposal_parser(self):
        from unittest.mock import patch
        from skill_library.librarian_ai import propose_granularity_opencode

        parent = Claim(id="E1", text="Install PostgreSQL", claim_type="operational", source="parent")
        child = Claim(id="C1", text="Install PostgreSQL 18", claim_type="operational", source="child")
        response = '{"action":"EXTRACT_FACET","new_skill_name":"postgres-install","new_skill_id":"postgres:install","role":"primitive","scope":"Install only","extracted_claim_ids":["C1"],"confidence":"high"}'
        with patch("skill_library.librarian_ai.opencode_run", return_value=response):
            result = propose_granularity_opencode("parent", "Parent", [parent], "child", "Child", [child])
        self.assertEqual(result["action"], "EXTRACT_FACET")

    def test_overlap_can_propose_split_without_merging(self):
        from unittest.mock import patch
        import librarian_testpipe as pipe
        from skill_library.librarian import RetrievedCandidate, RerankedCandidate

        candidate = CandidatePackage(
            name="install-postgres-18", source_dir="/tmp/test",
            description="Install PostgreSQL 18", body_sample="Install PostgreSQL 18",
        )
        retrieved = RetrievedCandidate(
            name="postgres-18", canonical_path="library/data/postgres-18",
            similarity=0.4, description="Install, query, and optimize PostgreSQL",
            body_sample="Install, query, and optimize PostgreSQL",
        )
        ranked = RerankedCandidate(
            name="postgres-18", canonical_path="library/data/postgres-18",
            rerank_score=0.2, dice_similarity=0.4,
            description="Install, query, and optimize PostgreSQL",
        )
        child_claim = Claim(id="C1", text="Install PostgreSQL 18", claim_type="operational", source="child")
        parent_claim = Claim(id="E1", text="Install PostgreSQL", claim_type="operational", source="parent")

        with patch.object(pipe, "retrieve_candidates", return_value=[retrieved]), \
             patch.object(pipe, "rerank_candidates", return_value=[ranked]), \
             patch("skill_library.librarian_ai.classify_relationship_opencode",
                   return_value={"relationship": "overlap", "match": "postgres-18", "reasoning": "Facet"}), \
             patch.object(pipe, "extract_claims", side_effect=[[child_claim], [parent_claim]]), \
             patch("skill_library.librarian_ai.detect_semantic_conflicts_opencode", return_value=[]), \
             patch("skill_library.librarian_ai.propose_granularity_opencode", return_value={
                 "action": "EXTRACT_FACET", "new_skill_name": "postgres-install",
                 "new_skill_id": "postgres:install", "role": "primitive",
                 "scope": "Install only", "extracted_claim_ids": ["C1"],
                 "parent_remove_claim_ids": ["E1"],
                 "parent_composed_of_add": ["postgres:install"],
                 "reasoning": "Independently shippable", "confidence": "high",
             }), \
             patch.object(pipe, "decide_merge") as merge:
            result = pipe.process_candidate(candidate, catalog=[])

        self.assertEqual(result["verdict"], "SPLIT_PROPOSAL")
        self.assertEqual(result["granularity"][0]["action"], "EXTRACT_FACET")
        merge.assert_not_called()


if __name__ == "__main__":
    unittest.main()