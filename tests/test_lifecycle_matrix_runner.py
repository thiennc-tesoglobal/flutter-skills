import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    ROOT
    / "skills"
    / "flutter-device-testing"
    / "scripts"
    / "run_lifecycle_matrix.py"
)
SPEC = importlib.util.spec_from_file_location("run_lifecycle_matrix", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class LifecycleMatrixRunnerTests(unittest.TestCase):
    def test_cli_defaults_to_a_redacted_dry_run(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix_path = Path(directory) / "matrix.json"
            matrix_path.write_text(
                json.dumps(
                    {
                        "platform": "android",
                        "device_id": "emulator-5554",
                        "app_id": "com.example.app",
                        "scenarios": [
                            {
                                "name": "warm-link",
                                "lifecycle": "warm",
                                "uri": "myapp://orders/42?token=secret",
                                "assert": [
                                    {
                                        "name": "order destination",
                                        "argv": [sys.executable, "-c", "pass"],
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(RUNNER_PATH), str(matrix_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual(report["status"], "planned")
            trigger = report["scenarios"][0]["steps"][0]
            self.assertNotIn("token=secret", json.dumps(trigger))

    def test_builds_platform_commands_without_a_shell(self):
        self.assertEqual(
            RUNNER.deep_link_command(
                "android", "emulator-5554", "com.example.app", "myapp://orders/42"
            ),
            [
                "adb",
                "-s",
                "emulator-5554",
                "shell",
                "am",
                "start",
                "-W",
                "-a",
                "android.intent.action.VIEW",
                "-d",
                "myapp://orders/42",
                "com.example.app",
            ],
        )
        self.assertEqual(
            RUNNER.deep_link_command(
                "ios", "A-SIMULATOR-ID", "com.example.app", "myapp://orders/42"
            ),
            ["xcrun", "simctl", "openurl", "A-SIMULATOR-ID", "myapp://orders/42"],
        )

    def test_cleanup_runs_after_a_failed_assertion(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "cleaned"
            matrix = RUNNER.validate_matrix(
                {
                    "platform": "android",
                    "device_id": "test-device",
                    "app_id": "com.example.app",
                    "scenarios": [
                        {
                            "name": "warm-notification",
                            "lifecycle": "warm",
                            "trigger": {
                                "name": "no-op provider fixture",
                                "argv": [sys.executable, "-c", "pass"],
                            },
                            "assert": [
                                {
                                    "name": "destination",
                                    "argv": [sys.executable, "-c", "raise SystemExit(7)"],
                                }
                            ],
                            "after": [
                                {
                                    "name": "remove fixture",
                                    "argv": [
                                        sys.executable,
                                        "-c",
                                        f"from pathlib import Path; Path({str(marker)!r}).touch()",
                                    ],
                                }
                            ],
                        }
                    ],
                }
            )
            report = RUNNER.run_matrix(matrix, execute=True)
            self.assertEqual(report["status"], "failed")
            self.assertTrue(marker.exists())
            self.assertEqual(
                report["scenarios"][0]["steps"][-1]["status"], "passed"
            )

    def test_ios_cold_prepare_accepts_an_already_stopped_app(self):
        result = RUNNER.normalize_lifecycle_result(
            "ios",
            {
                "name": "prepare: terminate app",
                "status": "failed",
                "exit_code": 3,
                "output_tail": "The application is not running",
            },
        )
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["note"], "app was already stopped")

    def test_rejects_a_scenario_without_semantic_assertions(self):
        with self.assertRaisesRegex(
            RUNNER.MatrixError, "assert must contain at least one verification step"
        ):
            RUNNER.validate_matrix(
                {
                    "platform": "android",
                    "device_id": "emulator-5554",
                    "app_id": "com.example.app",
                    "scenarios": [
                        {
                            "name": "launch-only",
                            "lifecycle": "warm",
                            "uri": "myapp://orders/42",
                        }
                    ],
                }
            )

    def test_report_redacts_tokens_and_uri_queries(self):
        self.assertNotIn(
            "secret-value",
            RUNNER.redact("Authorization: Bearer secret-value"),
        )
        self.assertEqual(
            RUNNER.safe_uri("myapp://orders/42?token=secret-value"),
            "myapp://orders/42",
        )
        self.assertEqual(
            RUNNER.safe_command(
                [
                    "tool",
                    "Authorization: Bearer secret-value",
                    "myapp://orders/42?token=x",
                ]
            ),
            ["tool", "Authorization: Bearer [REDACTED]", "myapp://orders/42"],
        )


if __name__ == "__main__":
    unittest.main()
