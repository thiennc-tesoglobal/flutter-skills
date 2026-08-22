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


class RepositoryTests(unittest.TestCase):
    def test_repository_validator_passes(self):
        errors, _, counts = VALIDATOR.validate_repository()
        self.assertEqual(errors, [])
        self.assertEqual(counts["skills"], 18)
        self.assertEqual(counts["evals"], 36)

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


if __name__ == "__main__":
    unittest.main()
