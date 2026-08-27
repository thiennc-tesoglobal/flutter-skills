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
        self.assertEqual(counts["skills"], 28)
        self.assertEqual(counts["evals"], 117)
        self.assertEqual(counts["routing_evals"], 36)

    def test_repository_markdown_excludes_generated_dependencies(self):
        paths = {
            path.relative_to(ROOT).as_posix()
            for path in VALIDATOR.repository_markdown_paths()
        }
        self.assertIn("README.md", paths)
        self.assertFalse(any(path.startswith("node_modules/") for path in paths))

    def test_release_changelog_requires_finalized_date(self):
        version = VALIDATOR.EXPECTED_VERSION
        self.assertEqual(
            VALIDATOR.release_changelog_errors(f"## {version} - Unreleased\n"),
            [
                f"release metadata requires '## {version} - YYYY-MM-DD'; "
                "the version must not remain Unreleased"
            ],
        )
        self.assertEqual(
            VALIDATOR.release_changelog_errors(f"## {version} - 2026-08-23\n"), []
        )
        self.assertTrue(
            VALIDATOR.release_changelog_errors(f"## {version} - 2026-02-30\n")
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

    def test_networking_evals_disclose_only_selected_transport_references(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        cases = BEHAVIOR_EVAL.behavior_cases(catalog)

        graphql_case = next(
            case
            for case in cases
            if case["skill"] == "flutter-networking"
            and case["name"] == "graphql-partial-data-and-cache"
        )
        graphql_instructions = BEHAVIOR_EVAL.instructions_for_case(
            graphql_case, catalog
        )
        self.assertIn("references/graphql.md\">", graphql_instructions)
        self.assertNotIn(
            "references/realtime-transports.md\">", graphql_instructions
        )

        subscription_case = next(
            case
            for case in cases
            if case["skill"] == "flutter-networking"
            and case["name"] == "graphql-subscription-recovery"
        )
        subscription_instructions = BEHAVIOR_EVAL.instructions_for_case(
            subscription_case, catalog
        )
        self.assertIn("references/graphql.md\">", subscription_instructions)
        self.assertIn(
            "references/realtime-transports.md\">", subscription_instructions
        )

        websocket_case = next(
            case
            for case in cases
            if case["skill"] == "flutter-networking"
            and case["name"] == "websocket-resume-is-not-reconnect"
        )
        websocket_instructions = BEHAVIOR_EVAL.instructions_for_case(
            websocket_case, catalog
        )
        self.assertIn(
            "references/realtime-transports.md\">", websocket_instructions
        )
        self.assertNotIn("references/graphql.md\">", websocket_instructions)

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

    def test_public_benchmark_profile_resolves_exact_cases(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        behavior = BEHAVIOR_EVAL.behavior_cases(catalog)
        routing = BEHAVIOR_EVAL.routing_cases()
        profile = BEHAVIOR_EVAL.load_json(BEHAVIOR_EVAL.DEFAULT_PROFILE_PATH)
        self.assertEqual(
            BEHAVIOR_EVAL.validate_benchmark_profile(profile, behavior, routing), []
        )
        selected_behavior, selected_routing = BEHAVIOR_EVAL.cases_for_profile(
            profile, behavior, routing
        )
        self.assertEqual(len(selected_behavior), 5)
        self.assertEqual(len(selected_routing), 5)
        self.assertEqual(selected_behavior[0]["skill"], "flutter-ui-design")
        self.assertEqual(selected_routing[-1]["name"], "figma-checkout-node-to-flutter")

    def test_result_summary_reports_raw_score_aggregates(self):
        results = {
            "behavior": [
                {
                    "passed": True,
                    "baseline": {"judgment": {"score": 60}},
                    "with_skill": {"judgment": {"score": 90}},
                }
            ],
            "routing": [{"passed": True}, {"passed": False}],
        }
        self.assertEqual(
            BEHAVIOR_EVAL.result_summary(results),
            {
                "behavior_cases": 1,
                "behavior_passed": 1,
                "baseline_average": 60.0,
                "with_skill_average": 90.0,
                "average_delta": 30.0,
                "routing_cases": 2,
                "routing_passed": 1,
            },
        )

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
