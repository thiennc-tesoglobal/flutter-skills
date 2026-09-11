import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "run_eval_matrix.py"
SPEC = importlib.util.spec_from_file_location("run_eval_matrix", SCRIPT)
assert SPEC and SPEC.loader
MATRIX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATRIX)


class EvalMatrixTests(unittest.TestCase):
    def test_repository_default_matrix_is_codex_only(self):
        matrix = MATRIX.load_json(MATRIX.DEFAULT_MATRIX)
        self.assertEqual(MATRIX.validate_matrix(matrix), [])
        self.assertEqual(len(matrix["runs"]), 1)
        run = matrix["runs"][0]
        self.assertEqual(run["agent"], "codex")
        self.assertEqual(run["judges"], ["codex"])
        self.assertTrue(run["skip_baseline"])
        self.assertFalse(run.get("require_independent_judge", False))

    def test_optional_cross_agent_matrix_is_independently_judged(self):
        matrix = MATRIX.load_json(MATRIX.CROSS_AGENT_MATRIX)
        self.assertEqual(MATRIX.validate_matrix(matrix), [])
        self.assertEqual({run["agent"] for run in matrix["runs"]}, {"codex", "claude"})
        for run in matrix["runs"]:
            self.assertEqual(len(run["judges"]), 2)
            self.assertNotEqual(run["judges"][0], run["agent"])
            self.assertTrue(run["skip_baseline"])
            self.assertTrue(run["require_independent_judge"])

    def test_matrix_rejects_duplicate_judges_and_external_profile(self):
        matrix = {
            "name": "invalid",
            "runs": [
                {
                    "id": "bad-run",
                    "agent": "codex",
                    "judges": ["codex", "codex"],
                    "profile": "../../outside.json",
                }
            ],
        }
        errors = MATRIX.validate_matrix(matrix)
        self.assertTrue(any("distinct" in error for error in errors))
        self.assertTrue(any("resolve inside" in error for error in errors))

    def test_command_uses_argv_and_repeated_judges(self):
        run = {
            "id": "codex-solver",
            "agent": "codex",
            "judges": ["claude", "codex"],
            "profile": "profiles/pr-smoke.json",
            "require_independent_judge": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            command = MATRIX.command_for_run(
                run, Path(directory), 90, "profiles/release-full.json"
            )
        self.assertEqual(command.count("--judge-agent"), 2)
        self.assertIn("--require-independent-judge", command)
        self.assertIn("claude", command)
        self.assertIn("codex", command)
        self.assertIn(str(MATRIX.EVALS_DIR / "profiles" / "release-full.json"), command)
        self.assertNotIn("sh", command)

    def test_default_command_does_not_claim_independent_judging(self):
        run = {
            "id": "codex-solver",
            "agent": "codex",
            "judges": ["codex"],
            "profile": "profiles/pr-smoke.json",
            "skip_baseline": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            command = MATRIX.command_for_run(run, Path(directory), 90)
        self.assertEqual(command.count("--judge-agent"), 1)
        self.assertNotIn("--require-independent-judge", command)
        self.assertIn("--skip-baseline", command)


if __name__ == "__main__":
    unittest.main()
