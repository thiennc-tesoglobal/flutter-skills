import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / ".github" / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

BEHAVIOR_EVAL_PATH = ROOT / ".github" / "scripts" / "run_behavior_evals.py"
BEHAVIOR_SPEC = importlib.util.spec_from_file_location("run_behavior_evals", BEHAVIOR_EVAL_PATH)
assert BEHAVIOR_SPEC and BEHAVIOR_SPEC.loader
BEHAVIOR_EVAL = importlib.util.module_from_spec(BEHAVIOR_SPEC)
BEHAVIOR_SPEC.loader.exec_module(BEHAVIOR_EVAL)


class RepositoryTests(unittest.TestCase):
    def test_repository_validator_passes(self):
        errors, _, counts = VALIDATOR.validate_repository()
        self.assertEqual(errors, [])
        self.assertEqual(counts["skills"], 25)
        self.assertEqual(counts["evals"], 73)
        self.assertEqual(counts["routing_evals"], 21)

    def test_release_changelog_requires_finalized_date(self):
        self.assertEqual(
            VALIDATOR.release_changelog_errors("## 0.1.0 - Unreleased\n"),
            [
                "release metadata requires '## 0.1.0 - YYYY-MM-DD'; "
                "the version must not remain Unreleased"
            ],
        )
        self.assertEqual(
            VALIDATOR.release_changelog_errors("## 0.1.0 - 2026-08-23\n"), []
        )
        self.assertTrue(
            VALIDATOR.release_changelog_errors("## 0.1.0 - 2026-02-30\n")
        )

    def test_eval_names_are_unique_across_catalog(self):
        names = []
        for path in sorted((ROOT / "skills").glob("*/evals/cases.json")):
            cases = json.loads(path.read_text(encoding="utf-8"))
            names.extend(f"{path.parents[1].name}:{case['name']}" for case in cases)
        self.assertEqual(len(names), len(set(names)))

    def test_all_skills_have_selection_boundaries(self):
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            metadata, _ = VALIDATOR.parse_frontmatter(path)
            description = metadata["description"].lower()
            self.assertTrue("use" in description, path)

    def test_behavior_eval_inputs_validate(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        behavior_cases = BEHAVIOR_EVAL.behavior_cases(catalog)
        routing_cases = BEHAVIOR_EVAL.routing_cases()
        self.assertEqual(
            BEHAVIOR_EVAL.validate_behavior_cases(behavior_cases, catalog), []
        )
        self.assertEqual(
            BEHAVIOR_EVAL.validate_routing_cases(routing_cases, set(catalog)), []
        )
        self.assertNotIn(
            "<supporting_resources>", catalog["flutter-app-workflow"]["instructions"]
        )
        complete_feature = next(
            case
            for case in behavior_cases
            if case["skill"] == "flutter-app-workflow"
            and case["name"] == "complete-feature-routes-specialists"
        )
        instructions = BEHAVIOR_EVAL.instructions_for_case(complete_feature, catalog)
        self.assertIn("<supporting_resources>", instructions)
        self.assertIn("references/project-preflight.md", instructions)
        self.assertIn("references/delivery-verification.md", instructions)

        async_form = next(
            case
            for case in behavior_cases
            if case["skill"] == "flutter-ui-patterns"
            and case["name"] == "async-form-submission-has-stable-ownership"
        )
        form_instructions = BEHAVIOR_EVAL.instructions_for_case(async_form, catalog)
        self.assertIn("references/forms-and-input.md", form_instructions)
        self.assertNotIn("references/widget-previews.md\">", form_instructions)

    def test_behavior_eval_rejects_unknown_reference(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        case = {
            "skill": "flutter-app-workflow",
            "name": "unknown-reference",
            "prompt": "Build a feature.",
            "expectations": ["keeps scope"],
            "resources": ["references/does-not-exist.md"],
        }
        errors = BEHAVIOR_EVAL.validate_behavior_cases([case], catalog)
        self.assertEqual(
            errors,
            [
                "flutter-app-workflow:unknown-reference: unknown resources "
                "['references/does-not-exist.md']"
            ],
        )

    def test_behavior_prompt_does_not_leak_expectations(self):
        case = {
            "prompt": "Fix the stale result.",
            "expectations": ["tests reversed completion order"],
        }
        solver_prompt = BEHAVIOR_EVAL.build_behavior_prompt(case, "Skill instructions")
        judge_prompt = BEHAVIOR_EVAL.build_judge_prompt(case, "Candidate response")
        self.assertNotIn(case["expectations"][0], solver_prompt)
        self.assertIn(case["expectations"][0], judge_prompt)

    def test_routing_score_rejects_overactivation(self):
        case = {
            "required": ["flutter-testing"],
            "optional": ["flutter-animation"],
            "forbidden": ["flutter-device-testing"],
        }
        passing = BEHAVIOR_EVAL.score_routing_selection(case, ["flutter-testing"])
        failing = BEHAVIOR_EVAL.score_routing_selection(
            case, ["flutter-testing", "flutter-device-testing", "flutter-architecture"]
        )
        self.assertTrue(passing["passed"])
        self.assertFalse(failing["passed"])
        self.assertEqual(failing["forbidden_selected"], ["flutter-device-testing"])
        self.assertEqual(failing["unexpected"], ["flutter-architecture", "flutter-device-testing"])

    def test_judgment_validation_rejects_incomplete_rubric(self):
        valid = {
            "score": 100,
            "expectations": [
                {"criterion": "preserves scope", "met": True, "evidence": "Explicit"}
            ],
            "summary": "Meets the criterion",
        }
        BEHAVIOR_EVAL.validate_judgment(valid, 1, "example")
        invalid = {"score": 100, "expectations": []}
        with self.assertRaises(BEHAVIOR_EVAL.EvalError):
            BEHAVIOR_EVAL.validate_judgment(invalid, 1, "example")


if __name__ == "__main__":
    unittest.main()
