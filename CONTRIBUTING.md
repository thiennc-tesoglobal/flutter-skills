# Contributing to Flutter Skills

Contributions should solve a concrete agent behavior problem and remain focused enough to review, evaluate, and maintain.

## Skill rules

1. Use a lowercase, hyphenated folder name matching the `name` in `SKILL.md`.
2. Make the description explain both capability and selection boundary.
3. Inspect and preserve the target project's current architecture, packages, SDK constraints, and platforms.
4. Do not promote a third-party package as a universal default.
5. Keep primary instructions concise; move conditional detail into linked references.
6. Require proportionate evidence such as formatting, analysis, tests, profile data, or device behavior.
7. Add or update behavior-focused evaluation cases.

## Evaluation cases

Each public skill contains `evals/cases.json`. Cases require a stable `name`, a realistic `prompt`, and an array of observable `expectations`. Include at least one successful routing case and one boundary or preservation case.

## Local checks

```sh
python3 .github/scripts/validate_repository.py
python3 -m unittest discover -s tests -v
npx skills add . --list
```

If marketplace metadata changes, also run:

```sh
claude plugin validate .
```

## Pull-request checklist

- [ ] The change addresses one clear problem.
- [ ] Frontmatter, links, and source claims are valid.
- [ ] Existing project choices remain respected.
- [ ] Evaluation coverage was added or updated.
- [ ] Validation and tests pass locally.
- [ ] Bundle membership and versions remain aligned.

By contributing, you agree that your contribution is distributed under the repository's BSD 3-Clause License.
