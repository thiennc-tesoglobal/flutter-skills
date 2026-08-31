import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


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
        self.assertEqual(counts["skills"], 35)
        self.assertEqual(counts["evals"], 152)
        self.assertEqual(counts["routing_evals"], 51)

    def test_codex_plugin_and_marketplace_resolve_the_full_catalog(self):
        plugin = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(plugin["name"], "flutter-skills")
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertEqual(plugin["interface"]["capabilities"], ["Skills"])
        self.assertEqual(marketplace["plugins"][0]["name"], plugin["name"])
        self.assertEqual(
            marketplace["plugins"][0]["source"],
            {"source": "local", "path": "./"},
        )

    def test_release_workflow_publishes_and_verifies_npm_before_other_channels(self):
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("publish-npm:", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("npm publish", workflow)
        self.assertIn('npm view "${package_name}@${package_version}" version', workflow)
        self.assertIn("release_tag:", workflow)
        self.assertIn("inputs.release_tag || github.ref", workflow)
        self.assertIn("for attempt in {1..12}", workflow)
        self.assertIn(
            'npm exec --yes --prefix "$smoke_directory" --package="${package_name}@${package_version}" -- flutter-skills --version',
            workflow,
        )
        self.assertIn('smoke_directory="$(mktemp -d)"', workflow)
        self.assertIn("needs: [validate, publish-npm]", workflow)
        self.assertIn('grep -Fq "already exists"', workflow)
        self.assertIn(
            "Tessl version already exists; treating the immutable release as verified.",
            workflow,
        )
        self.assertNotIn("NODE_AUTH_TOKEN", workflow)
        self.assertLess(workflow.index("publish-npm:"), workflow.index("publish-tessl:"))
        self.assertGreaterEqual(workflow.count("if: github.ref_type == 'tag'"), 3)

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

    def test_tool_free_performance_eval_scores_required_evidence_not_fake_artifacts(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-performance"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "attributes-ui-versus-raster-jank"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("requires a reproducible profile-mode trace", expectations)
        self.assertIn("defines a repeat of the same flow", expectations)
        self.assertNotIn("captures a reproducible", expectations)

    def test_tool_free_runtime_eval_scores_required_evidence_not_fake_artifacts(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-runtime-debugging"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "runtime-fix-repeats-original-flow"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("requires tracing", expectations)
        self.assertIn("requires repeating", expectations)
        self.assertNotIn("traces the lifecycle", expectations)
        self.assertNotIn("repeats the original", expectations)

    def test_tool_free_iap_eval_requires_inspection_without_fabricating_access(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-in-app-purchases"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "sandbox-readiness-is-not-store-publication"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("requires a pre-change inspection", expectations)
        self.assertIn("interrupted-purchase and one restoration", expectations)
        self.assertNotIn("inspects identifiers", expectations)

    def test_tool_free_package_eval_accepts_an_executable_review_plan(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-package-development"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "dry-run-does-not-authorize-publish"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("executable review with pass-fail criteria", expectations)
        self.assertIn("without fabricating repository access", expectations)

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
        self.assertEqual(len(selected_behavior), 6)
        self.assertEqual(len(selected_routing), 7)
        self.assertEqual(selected_behavior[0]["skill"], "flutter-package-development")
        self.assertEqual(
            selected_routing[-1]["name"],
            "production-crash-context-is-not-product-analytics",
        )

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

    def test_agent_runner_reports_the_exact_cli_version(self):
        completed = type(
            "Completed",
            (),
            {"returncode": 0, "stdout": "codex-cli 1.2.3\n", "stderr": ""},
        )()
        with patch.object(BEHAVIOR_EVAL.shutil, "which", return_value="/bin/codex"):
            runner = BEHAVIOR_EVAL.AgentRunner("codex", None)
        with patch.object(BEHAVIOR_EVAL.subprocess, "run", return_value=completed) as run:
            self.assertEqual(runner.version(), "codex-cli 1.2.3")
        run.assert_called_once_with(
            ["/bin/codex", "--version"],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_agent_runner_bounds_stalled_invocations(self):
        with patch.object(BEHAVIOR_EVAL.shutil, "which", return_value="/bin/claude"):
            runner = BEHAVIOR_EVAL.AgentRunner("claude", None, timeout_seconds=12)
        with patch.object(
            BEHAVIOR_EVAL.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(["/bin/claude"], 12),
        ):
            with self.assertRaisesRegex(
                BEHAVIOR_EVAL.EvalError,
                "claude eval timed out after 12 seconds",
            ):
                runner.run("prompt")

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
