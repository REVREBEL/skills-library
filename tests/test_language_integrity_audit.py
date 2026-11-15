"""
Comprehensive Unit, Scanner Correctness, and Invariant Test Suite for SKIL-11 (ZI-06).
"""

import ast
import csv
import json
import os
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
ZERO_INDEX_DIR = REPO_ROOT / "audit" / "zero-index" / "SKIL-11"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

try:
    from tools.audit_language_and_integrity import (
        classify_leak,
        audit_language_entry,
        audit_resources_and_ast,
        generate_quarantine_reconciliation,
        run_skil11_audit,
        SECRET_PATTERNS,
        WORKSTATION_PATH_PATTERNS,
        BENIGN_PATH_MARKERS,
    )
except ImportError:
    from audit_language_and_integrity import (
        classify_leak,
        audit_language_entry,
        audit_resources_and_ast,
        generate_quarantine_reconciliation,
        run_skil11_audit,
        SECRET_PATTERNS,
        WORKSTATION_PATH_PATTERNS,
        BENIGN_PATH_MARKERS,
    )

class TestScannerCorrectness(unittest.TestCase):
    """Test unit-level scanner behavior, regex classifications, AST checks, and error handling."""

    def test_leak_classification_real_secrets(self):
        """Real-looking credentials outside fixtures must be classified as unclassified findings."""
        # 1. Private Key
        pk_res = classify_leak(
            "private_key",
            "-----BEGIN RSA PRIVATE KEY-----",
            "key = '-----BEGIN RSA PRIVATE KEY-----'",
            "crypto.py",
            "library/security/crypto.py"
        )
        self.assertEqual(pk_res, "unclassified_private_key")
        self.assertTrue(pk_res.startswith("unclassified_"))

        # 2. GitHub Token
        tok_val = "ghp_" + "A" * 36
        tok_res = classify_leak(
            "api_token",
            tok_val,
            f"token = '{tok_val}'",
            "auth.py",
            "library/integrations/auth.py"
        )
        self.assertEqual(tok_res, "unclassified_api_token")
        self.assertTrue(tok_res.startswith("unclassified_"))

        # 3. Internal URL
        url_val = "http://10.240.12.5:8080/api"
        url_res = classify_leak(
            "internal_url",
            url_val,
            f"endpoint = '{url_val}'",
            "client.py",
            "library/net/client.py"
        )
        self.assertEqual(url_res, "unclassified_internal_url")
        self.assertTrue(url_res.startswith("unclassified_"))

    def test_leak_classification_benign_fixtures(self):
        """Test fixtures, examples, mock files, and placeholder strings must be classified as documentation_fixture."""
        # Path containing 'example'
        res1 = classify_leak(
            "api_token",
            "ghp_" + "A" * 36,
            "export GITHUB_TOKEN=ghp_...",
            ".env.example",
            "library/tools/.env.example"
        )
        self.assertEqual(res1, "documentation_fixture")

        # Snippet containing 'placeholder' or 'your-api-key'
        res2 = classify_leak(
            "api_token",
            "ghp_" + "A" * 36,
            "api_key = 'your-api-key-here'",
            "quickstart.md",
            "library/guide/quickstart.md"
        )
        self.assertEqual(res2, "documentation_fixture")

        # Standard localhost / loopback internal IP
        res3 = classify_leak(
            "internal_url",
            "http://127.0.0.1:8000",
            "bind_addr = 'http://127.0.0.1:8000'",
            "server.py",
            "library/web/server.py"
        )
        self.assertEqual(res3, "documentation_fixture")

    def test_language_classification_branching(self):
        """Verify language classification assigns correct scopes and actions across dialects."""
        # 1. Native English
        item_en = {"canonical_id": "test:en", "raw_name": "test-en", "rel_path": "library/test/en", "category": "test", "subcategory": "en"}
        meta_en = {"name": "Test English", "description": "A standard English skill description.", "body": "Follow these steps to complete the task."}
        res_en = audit_language_entry(item_en, meta_en)
        self.assertEqual(res_en["language_classification"], "english_native")
        self.assertEqual(res_en["translation_scope"], "NONE")
        self.assertEqual(res_en["proposed_disposition"], "CANONICAL_ACTIVE")

        # 2. Chinese Dominant (Metadata and Body)
        meta_zh_dom = {
            "name": "Chinese Skill",
            "description": "这是一个完整的中文技能描述，包含很多汉字。",
            "body": "这里是中文的正文内容，包含详细的执行步骤和操作流程，汉字数量较多以触发多语种分类器。为了确保汉字数量超过五十个字符阈值，我们继续在此处添加更多的中文技术说明与执行细节内容。"
        }
        res_zh_dom = audit_language_entry(item_en, meta_zh_dom)
        self.assertEqual(res_zh_dom["language_classification"], "foreign_language_dominant")
        self.assertEqual(res_zh_dom["translation_scope"], "METADATA_AND_BODY")
        self.assertEqual(res_zh_dom["proposed_disposition"], "TRANSLATE_OR_QUARANTINE")

        # 3. Chinese Mixed Metadata Only
        meta_zh_meta = {
            "name": "Chinese Meta",
            "description": "这是一个中文描述前端元数据。",
            "body": "This is standard English prompt instructions and steps for execution."
        }
        res_zh_meta = audit_language_entry(item_en, meta_zh_meta)
        self.assertEqual(res_zh_meta["language_classification"], "mixed_foreign_metadata")
        self.assertEqual(res_zh_meta["translation_scope"], "METADATA_ONLY")
        self.assertEqual(res_zh_meta["proposed_disposition"], "TRANSLATE_RECOMMENDED")

        # 4. Chinese Mixed Body Only
        meta_zh_body = {
            "name": "Chinese Body",
            "description": "A standard English description for this skill tool.",
            "body": "这是正文部分的中文指令，包含了大量的汉字，用于指导大模型如何完成专业的业务逻辑处理与推演分析工作。为了满足大于五十个字符的判定条件，我们在正文中补充了更多的中文说明内容。"
        }
        res_zh_body = audit_language_entry(item_en, meta_zh_body)
        self.assertEqual(res_zh_body["language_classification"], "mixed_foreign_body")
        self.assertEqual(res_zh_body["translation_scope"], "BODY_ONLY")
        self.assertEqual(res_zh_body["proposed_disposition"], "TRANSLATE_RECOMMENDED")

        # 5. Portuguese Dominant
        meta_pt_dom = {
            "name": "Portuguese Skill",
            "description": "Agente para execução e avaliação de múltiplos relatórios de inteligência.",
            "body": "Configuração padrão para o usuário quando você está criando relatórios com especialistas."
        }
        res_pt_dom = audit_language_entry(item_en, meta_pt_dom)
        self.assertEqual(res_pt_dom["primary_language"], "Portuguese")
        self.assertEqual(res_pt_dom["language_classification"], "foreign_language_dominant")
        self.assertEqual(res_pt_dom["translation_scope"], "METADATA_AND_BODY")
        self.assertEqual(res_pt_dom["proposed_disposition"], "TRANSLATE_OR_QUARANTINE")

    def test_quarantine_reconciliation_distinguishes_body_and_metadata(self):
        """Quarantine reconciliation must assign TRANSLATE_BODY vs TRANSLATE_METADATA correctly."""
        pop = [
            {"canonical_id": "test:meta", "raw_name": "test-meta", "rel_path": "library/test/meta", "category": "test"},
            {"canonical_id": "test:body", "raw_name": "test-body", "rel_path": "library/test/body", "category": "test"},
        ]
        lang_rows = [
            {
                "canonical_id": "test:meta",
                "language_classification": "mixed_foreign_metadata",
                "translation_candidate": True,
                "primary_language": "Chinese",
                "rationale": "Chinese description"
            },
            {
                "canonical_id": "test:body",
                "language_classification": "mixed_foreign_body",
                "translation_candidate": True,
                "primary_language": "Chinese",
                "rationale": "Chinese body content"
            }
        ]
        q_rows = generate_quarantine_reconciliation(pop, lang_rows, [])
        self.assertEqual(len(q_rows), 2)
        q_map = {r["canonical_id"]: r for r in q_rows}

        self.assertEqual(q_map["test:meta"]["quarantine_reason_class"], "mixed_language_metadata")
        self.assertEqual(q_map["test:meta"]["proposed_action"], "TRANSLATE_METADATA")

        self.assertEqual(q_map["test:body"]["quarantine_reason_class"], "mixed_language_body")
        self.assertEqual(q_map["test:body"]["proposed_action"], "TRANSLATE_BODY")

    def test_ast_safety_detection_in_mock_env(self):
        """AST scanner must flag dangerous calls (eval, exec, os.system, shell=True) and syntax errors."""
        with tempfile.TemporaryDirectory() as td:
            tmp_root = Path(td)
            skill_dir = tmp_root / "library" / "test-skill"
            skill_dir.mkdir(parents=True)

            (skill_dir / "SKILL.md").write_text("# Test Skill", encoding="utf-8")
            (skill_dir / "safe.py").write_text("import sys\ndef main():\n    print(sys.argv)\n", encoding="utf-8")
            (skill_dir / "unsafe_eval.py").write_text("x = eval('2 + 2')\n", encoding="utf-8")
            (skill_dir / "unsafe_system.py").write_text("import os\nos.system('echo test')\n", encoding="utf-8")
            (skill_dir / "unsafe_popen.py").write_text("import subprocess\nsubprocess.Popen('ls', shell=True)\n", encoding="utf-8")
            (skill_dir / "syntax_err.py").write_text("def broken(\n", encoding="utf-8")

            pop = [{"canonical_id": "test:skill", "raw_name": "test-skill", "rel_path": "library/test-skill", "category": "test"}]
            rows, stats = audit_resources_and_ast(pop, repo_root=tmp_root)

            self.assertEqual(stats["total_python_scripts"], 5)
            self.assertEqual(stats["ast_syntax_valid"], 4)
            self.assertEqual(stats["ast_syntax_errors"], 1)
            self.assertEqual(stats["dangerous_calls_detected"], 3)

            r_map = {r["file_relative_path"]: r for r in rows}
            self.assertEqual(r_map["safe.py"]["safety_status"], "safe_inspected_script")
            self.assertEqual(r_map["unsafe_eval.py"]["safety_status"], "ast_risk_flagged")
            self.assertEqual(r_map["unsafe_system.py"]["safety_status"], "ast_risk_flagged")
            self.assertEqual(r_map["unsafe_popen.py"]["safety_status"], "ast_risk_flagged")
            self.assertEqual(r_map["syntax_err.py"]["ast_syntax_status"], "ast_syntax_error")

class TestRegenerationAndParity(unittest.TestCase):
    """Test full audit engine regeneration into a temporary directory and verify parity."""

    def test_reproducible_regeneration(self):
        """Regenerating audit deliverables in a scratch directory must produce valid artifacts with identical counts."""
        with tempfile.TemporaryDirectory() as td:
            tmp_out = Path(td)
            summary = run_skil11_audit(output_dir=tmp_out)

            # Assert all 6 files are created
            self.assertTrue((tmp_out / "language-audit.csv").exists())
            self.assertTrue((tmp_out / "integrity-and-exposure-findings.csv").exists())
            self.assertTrue((tmp_out / "quarantine-candidates.csv").exists())
            self.assertTrue((tmp_out / "language-integrity-exposure-summary.json").exists())
            self.assertTrue((tmp_out / "commands-and-tests.md").exists())
            self.assertTrue((tmp_out / "summary.md").exists())

            # Verify row counts match authoritative data
            with open(tmp_out / "language-audit.csv", mode="r", encoding="utf-8") as f:
                lang_rows = list(csv.DictReader(f))
            self.assertEqual(len(lang_rows), 2133)

            with open(tmp_out / "integrity-and-exposure-findings.csv", mode="r", encoding="utf-8") as f:
                res_rows = list(csv.DictReader(f))
            self.assertEqual(len(res_rows), 8172)

            with open(tmp_out / "quarantine-candidates.csv", mode="r", encoding="utf-8") as f:
                q_rows = list(csv.DictReader(f))
            self.assertEqual(len(q_rows), 48)

            self.assertEqual(summary["audit_metadata"]["population_audited"], 2133)
            self.assertEqual(summary["audit_metadata"]["total_resources_audited"], 8172)

class TestFailClosedGate(unittest.TestCase):
    """Test fault-injection and fail-closed gate behavior."""

    def test_audit_failure_raises_and_fails_closed(self):
        """When SKIL-11 audit encounters a critical failure, it must raise and prevent a false-green validation."""
        import unittest.mock
        with unittest.mock.patch("tools.audit_language_and_integrity.load_authoritative_population", side_effect=RuntimeError("Injected audit failure")):
            with self.assertRaises(RuntimeError):
                run_skil11_audit()

class TestLanguageIntegrityAuditInvariants(unittest.TestCase):
    """Test invariants of committed SKIL-11 audit deliverables."""

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
        """Resource audit must verify 8,172 resources with 0 AST syntax errors and 0 unclassified leaks."""
        self.assertEqual(len(self.res_rows), 8172)
        ast_errors = [r for r in self.res_rows if r["ast_syntax_status"] == "ast_syntax_error"]
        self.assertEqual(len(ast_errors), 0, "All Python scripts must be syntactically valid")

        secret_leaks = [r for r in self.res_rows if r["leak_status"] == "secret_leak_flagged"]
        self.assertEqual(len(secret_leaks), 0, "Must have zero unclassified secret leaks")

        workstation_leaks = [r for r in self.res_rows if r["leak_status"] == "workstation_path_leak"]
        self.assertEqual(len(workstation_leaks), 0, "Must have zero unclassified workstation path leaks")

        unreadable_files = [r for r in self.res_rows if r["safety_status"] == "scan_error"]
        self.assertEqual(len(unreadable_files), 0, "Must have zero unreadable files")

    def test_quarantine_reconciliation_categories(self):
        """Quarantine candidates must reconcile translation, persona, and tech-coupling criteria."""
        self.assertEqual(len(self.q_rows), 48)
        reasons = Counter(r["quarantine_reason_class"] for r in self.q_rows)
        self.assertEqual(reasons["foreign_language_dominant"], 14)
        self.assertEqual(reasons["mixed_language_metadata"], 23)
        self.assertEqual(reasons["mixed_language_body"], 4)
        self.assertEqual(reasons["persona_or_prompt_outlier"], 6)
        self.assertEqual(reasons["historical_phase03_excluded_tech"], 1)

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
