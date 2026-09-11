import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "review_eval_results.py"
SPEC = importlib.util.spec_from_file_location("review_eval_results", SCRIPT)
assert SPEC and SPEC.loader
REVIEW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REVIEW)


class EvalReliabilityTests(unittest.TestCase):
    def result(self):
        judgment = {
            "score": 100,
            "expectations": [
                {"criterion": "keeps scope", "met": True, "evidence": "explicit"}
            ],
            "summary": "pass",
        }
        return {
            "behavior": [
                {
                    "skill": "flutter-testing",
                    "case": "case-one",
                    "with_skill": {
                        "response": "Scoped response",
                        "judgment": judgment,
                        "judgments": [
                            judgment,
                            {
                                **judgment,
                                "expectations": [
                                    {
                                        "criterion": "keeps scope",
                                        "met": False,
                                        "evidence": "expanded",
                                    }
                                ],
                            },
                        ],
                    },
                }
            ]
        }

    def test_sample_is_reproducible_and_human_agreement_is_per_judge(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_path = root / "result.json"
            result_path.write_text(json.dumps(self.result()), encoding="utf-8")
            first = REVIEW.create_review_template(result_path, 0.15, 42)
            second = REVIEW.create_review_template(result_path, 0.15, 42)
            self.assertEqual(first, second)
            first["reviewer"] = "maintainer"
            first["reviewed_at"] = "2026-09-11T00:00:00Z"
            first["cases"][0]["expectations"][0]["human_met"] = True
            review_path = root / "review.json"
            review_path.write_text(json.dumps(first), encoding="utf-8")

            summary = REVIEW.summarize_review(result_path, review_path)
            self.assertEqual(summary["reviewed_cases"], 1)
            self.assertEqual(
                [item["agreement_rate"] for item in summary["judge_human_agreement"]],
                [100.0, 0.0],
            )

    def test_modified_result_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_path = root / "result.json"
            result_path.write_text(json.dumps(self.result()), encoding="utf-8")
            review = REVIEW.create_review_template(result_path, 1, 0)
            review["reviewer"] = "maintainer"
            review["reviewed_at"] = "2026-09-11T00:00:00Z"
            review["cases"][0]["expectations"][0]["human_met"] = True
            review_path = root / "review.json"
            review_path.write_text(json.dumps(review), encoding="utf-8")
            result_path.write_text(json.dumps({"behavior": []}), encoding="utf-8")
            with self.assertRaisesRegex(REVIEW.ReviewError, "source hash"):
                REVIEW.summarize_review(result_path, review_path)


if __name__ == "__main__":
    unittest.main()
