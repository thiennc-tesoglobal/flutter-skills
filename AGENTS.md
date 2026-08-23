# Repository instructions

## Purpose

This repository contains Agent Skills for Flutter and Dart app delivery. It is not a Flutter application or reusable Dart package. Treat changes as instruction, routing, evaluation, and distribution work.

## Required authoring workflow

Before creating or substantially revising a skill:

1. Follow the active Agent Skills authoring guidance available in the agent environment.
2. Inspect the affected skill, neighboring descriptions, evaluation cases, package bundles, and working tree.
3. Verify fast-moving Flutter, Dart, package, and platform claims against current primary sources.
4. Preserve existing project architecture and package choices unless the user's task explicitly requests migration.
5. Add or update behavior-focused evaluation cases.

## Skill rules

- Keep `SKILL.md` concise and place conditional detail in directly linked references.
- Make frontmatter descriptions cheap, precise, and discriminating.
- Define boundaries between nearby specialists to prevent broad activation.
- Do not promote Provider, Riverpod, Bloc, Dio, Drift, go_router, or another third-party package as a universal default.
- Read `pubspec.yaml` and SDK constraints before recommending syntax or packages.
- Prefer current official Flutter and Dart documentation; use package-publisher documentation for package-specific behavior.
- Require evidence proportionate to the claim: formatting, analysis, tests, profile-mode measurements, or device behavior.
- Keep maintainer-only workflows outside `skills/` so they do not enter the public catalog.

## Surfaces that must stay synchronized

When adding, removing, or renaming a skill, update:

- `skills/<name>/SKILL.md`
- `skills/<name>/evals/cases.json`
- `.claude-plugin/marketplace.json`
- `.tessl-plugin/plugin.json`
- `README.md` counts and catalog
- `CHANGELOG.md`

## Validation

Run before committing:

```sh
python3 .github/scripts/validate_repository.py
python3 .github/scripts/run_behavior_evals.py
python3 -m unittest discover -s tests -v
bash .github/scripts/run_dart_skills_lint.sh
claude plugin validate .
npx skills add . --list
```

For a full audit or release review, follow [the maintainer audit workflow](.github/maintainer/flutter-skill-audit.md).

Before publishing, replace the version's `Unreleased` marker with an ISO date and run `python3 .github/scripts/validate_repository.py --release`.

## Safety and scope

- Preserve unrelated user changes.
- Do not publish packages, create releases, change signing material, upload apps, or mutate live services without explicit authorization.
- Do not claim device, build, test, or performance verification that was not actually performed.
- If credentials or platform tooling block verification, state the exact boundary instead of weakening the check.
