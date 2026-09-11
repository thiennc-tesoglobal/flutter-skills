import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
SCRIPT = SCRIPTS_DIR / "run_executable_evals.py"
SPEC = importlib.util.spec_from_file_location("run_executable_evals", SCRIPT)
assert SPEC and SPEC.loader
EXECUTABLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXECUTABLE)


class ExecutableEvalTests(unittest.TestCase):
    def test_rejects_traversal_and_non_allowlisted_commands(self):
        catalog = {"dart-concurrency": {"resources": {}}}
        case = {
            "name": "unsafe",
            "skill": "dart-concurrency",
            "prompt": "Fix it",
            "fixture": "../outside",
            "allowed_changes": ["../tests"],
            "checks": [{"command": ["bash", "-c", "true"]}],
        }
        errors = EXECUTABLE.validate_case(case, catalog)
        self.assertTrue(any("safe relative path" in error for error in errors))
        self.assertTrue(any("executable is not allowed" in error for error in errors))

    def test_rejects_allowlisted_runtime_with_external_path(self):
        catalog = {"dart-concurrency": {"resources": {}}}
        case = {
            "name": "unsafe-path",
            "skill": "dart-concurrency",
            "prompt": "Fix it",
            "fixture": "missing",
            "allowed_changes": ["lib"],
            "checks": [{"command": ["dart", "run", "/tmp/untrusted.dart"]}],
        }
        errors = EXECUTABLE.validate_case(case, catalog)
        self.assertTrue(any("outside the fixture" in error for error in errors))

    def test_changed_paths_must_stay_within_declared_owners(self):
        self.assertTrue(EXECUTABLE.path_is_allowed("lib/latest.dart", ["lib"]))
        self.assertFalse(EXECUTABLE.path_is_allowed("bin/verify.dart", ["lib"]))
        self.assertFalse(EXECUTABLE.path_is_allowed("lib-other/file.dart", ["lib"]))

    def test_execute_case_rejects_agent_changes_to_verifier(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixtures = root / "fixtures"
            fixture = fixtures / "case"
            (fixture / "lib").mkdir(parents=True)
            (fixture / "bin").mkdir()
            (fixture / "lib" / "code.dart").write_text("broken\n", encoding="utf-8")
            (fixture / "bin" / "verify.dart").write_text("verify\n", encoding="utf-8")
            case = {
                "name": "case",
                "skill": "dart-concurrency",
                "prompt": "Fix it",
                "resources": [],
                "fixture": "case",
                "allowed_changes": ["lib"],
                "checks": [{"command": ["dart", "analyze", "lib"]}],
            }
            catalog = {
                "dart-concurrency": {
                    "instructions": "Keep latest results.",
                    "resources": {},
                }
            }

            class Agent:
                def run_in_workspace(self, prompt, workspace):
                    (workspace / "lib" / "code.dart").write_text("fixed\n", encoding="utf-8")
                    (workspace / "bin" / "verify.dart").write_text("weakened\n", encoding="utf-8")
                    return "done"

            baseline = [
                {
                    "name": "analyze",
                    "command": ["dart", "analyze", "lib"],
                    "exit_code": 1,
                    "stdout": "",
                    "stderr": "expected failure",
                    "passed": False,
                }
            ]
            with (
                patch.object(EXECUTABLE, "FIXTURES_DIR", fixtures),
                patch.object(EXECUTABLE, "run_checks", return_value=baseline),
            ):
                result = EXECUTABLE.execute_case(case, catalog, Agent())
            self.assertFalse(result["passed"])
            self.assertEqual(result["forbidden_changes"], ["bin/verify.dart"])
            self.assertEqual(result["checks"], [])


if __name__ == "__main__":
    unittest.main()
