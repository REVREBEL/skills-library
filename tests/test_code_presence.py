"""
Unit tests for the code-presence survey.

The survey exists to size the risk model before ZI-08 design: if most packages
are prose, risk can default cheaply and review effort concentrates on the rest.
"""

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

from skill_library.code_presence import (
    classify_package,
    scan_code_blocks,
    scan_scripts,
    summarise,
    survey_library,
)

LIBRARY = str(REPO_ROOT / "library")


def write_package(root: str, relative: str, body: str = "---\nname: demo\ndescription: d\n---\n") -> str:
    path = os.path.join(root, *relative.split("/"))
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "SKILL.md"), "w", encoding="utf-8") as handle:
        handle.write(body)
    return path


class TestScanScripts(unittest.TestCase):
    def test_finds_executable_suffixes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/demo")
            os.makedirs(os.path.join(pkg, "scripts"), exist_ok=True)
            for name in ("run.py", "setup.sh", "helper.js"):
                open(os.path.join(pkg, "scripts", name), "w").close()
            open(os.path.join(pkg, "notes.md"), "w").close()

            scripts = scan_scripts(pkg)
            self.assertEqual(len(scripts), 3)
            self.assertTrue(all(not s.endswith(".md") for s in scripts))

    def test_ignores_skip_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/demo")
            os.makedirs(os.path.join(pkg, "node_modules", "pkg"), exist_ok=True)
            open(os.path.join(pkg, "node_modules", "pkg", "index.js"), "w").close()

            self.assertEqual(scan_scripts(pkg), [])


class TestScanCodeBlocks(unittest.TestCase):
    def test_counts_fenced_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "SKILL.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# T\n\n```bash\nls\n```\n\n```python\nprint(1)\n```\n")
            self.assertEqual(scan_code_blocks(path), ["shell", "python"])

    def test_handles_tilde_fences(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "SKILL.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("~~~sh\nls\n~~~\n")
            self.assertEqual(scan_code_blocks(path), ["shell"])

    def test_untagged_block_is_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "SKILL.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("```\nplain\n```\n")
            self.assertEqual(scan_code_blocks(path), ["text"])

    def test_missing_file_returns_empty(self):
        self.assertEqual(scan_code_blocks("/nonexistent/SKILL.md"), [])


class TestClassify(unittest.TestCase):
    def test_prose_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/prose-skill", "---\nname: p\n---\nNo code here.\n")
            survey = classify_package(pkg, library_dir=root)
            self.assertEqual(survey.classification, "prose")
            self.assertFalse(survey.has_scripts)
            self.assertFalse(survey.has_code_blocks)

    def test_scripts_make_it_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/scripted")
            open(os.path.join(pkg, "run.py"), "w").close()
            survey = classify_package(pkg, library_dir=root)
            self.assertEqual(survey.classification, "code")
            self.assertTrue(survey.has_scripts)

    def test_code_block_makes_it_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(
                root, "development/backend/blocky", "---\nname: b\n---\n```bash\nls\n```\n"
            )
            survey = classify_package(pkg, library_dir=root)
            self.assertEqual(survey.classification, "code")
            self.assertEqual(survey.block_count, 1)

    def test_command_metadata_makes_it_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(
                root, "development/backend/cmd", "---\nname: c\nallowed-tools: Bash\n---\ntext\n"
            )
            survey = classify_package(pkg, library_dir=root)
            self.assertEqual(survey.classification, "code")
            self.assertTrue(survey.has_command_metadata)

    def test_non_canonical_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/router")
            self.assertIsNone(classify_package(pkg, library_dir=root))

    def test_row_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            pkg = write_package(root, "development/backend/row")
            row = classify_package(pkg, library_dir=root).to_row()
            self.assertEqual(
                set(row),
                {
                    "canonical_id",
                    "path",
                    "risk",
                    "license",
                    "classification",
                    "has_scripts",
                    "script_count",
                    "script_languages",
                    "has_code_blocks",
                    "block_count",
                    "block_languages",
                    "has_command_metadata",
                },
            )


class TestSummarise(unittest.TestCase):
    def test_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "library")
            write_package(root, "development/backend/a")
            write_package(root, "development/backend/b", "---\nname: b\n---\n```sh\nls\n```\n")
            summaries = survey_library(root)
            result = summarise(summaries)
            self.assertEqual(result["total"], 2)
            self.assertEqual(result["code"]["total"], 1)
            self.assertEqual(result["prose"]["total"], 1)
            self.assertEqual(result["code_share_pct"], 50.0)


class TestRealLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.surveys = survey_library(LIBRARY)
        cls.summary = summarise(cls.surveys)

    def test_population(self):
        self.assertEqual(self.summary["total"], 2133)

    def test_both_classes_present(self):
        self.assertGreater(self.summary["code"]["total"], 0)
        self.assertGreater(self.summary["prose"]["total"], 0)

    def test_prose_packages_are_mostly_unknown_risk(self):
        prose = [s for s in self.surveys if s.classification == "prose"]
        unknown = sum(1 for s in prose if s.risk == "unknown")
        self.assertGreater(unknown / len(prose), 0.9)


if __name__ == "__main__":
    unittest.main()