# Flutter Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-21-2ea44f)](skills/)
[![Flutter](https://img.shields.io/badge/Flutter-3.44-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.12-0175C2?logo=dart&logoColor=white)](https://dart.dev)
[![Validation](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml/badge.svg)](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml)
[![License](https://img.shields.io/badge/License-BSD--3--Clause-blue)](LICENSE)

A focused Agent Skills collection for delivering maintainable Flutter applications across mobile, web, and desktop.

The collection coordinates architecture, UI, state, data, testing, performance, accessibility, native integration, and release verification. It adapts to the project instead of forcing a state-management package or folder structure onto every app.

> **Tiếng Việt:** Bộ skill giúp AI coding agent xây dựng ứng dụng Flutter theo quy trình thực tế: đọc dự án, chọn đúng chuyên môn, triển khai, chạy analyze/test và xác minh trên thiết bị.

## How it works

Start a complete app or substantial multi-file feature with [`flutter-app-workflow`](skills/flutter-app-workflow/). Use a specialist directly for narrow work.

```text
Product request → project preflight → relevant skills → vertical slices → verification
```

## Install

Choose skills interactively:

```sh
npx skills add thiennc-tesoglobal/flutter-skills
```

Install the delivery workflow:

```sh
npx skills add thiennc-tesoglobal/flutter-skills --skill flutter-app-workflow
```

The workflow remains usable by itself. It delegates to specialist skills only when they are installed and discoverable.

Install the complete collection only when broad coverage is required:

```sh
npx skills add thiennc-tesoglobal/flutter-skills --all
```

### Claude Code

```sh
/plugin marketplace add thiennc-tesoglobal/flutter-skills
/plugin install all-flutter-skills@flutter-skills
```

Focused bundles are also available:

```sh
/plugin install flutter-core-skills@flutter-skills
/plugin install flutter-ui-skills@flutter-skills
/plugin install flutter-engineering-skills@flutter-skills
```

## Catalog

| Area | Skills |
|---|---|
| Delivery | `flutter-app-workflow`, `flutter-build-release`, `flutter-device-testing` |
| Dart | `dart-language`, `dart-concurrency` |
| Structure | `flutter-architecture`, `flutter-state-management` |
| UI | `flutter-ui-design`, `flutter-ui-patterns`, `flutter-responsive-layout`, `flutter-animation`, `flutter-navigation` |
| Data | `flutter-networking`, `flutter-persistence` |
| Quality | `flutter-code-review`, `flutter-security`, `flutter-testing`, `flutter-performance`, `flutter-accessibility`, `flutter-localization` |
| Platform | `flutter-platform-integration` |

Example:

```text
Use $flutter-app-workflow to build a polished offline-first todo app,
preserve the project's existing conventions, add tests, and verify it on a device.
```

Installing every skill does not mean every skill should be loaded for every request. Prefer one workflow skill plus only the specialists required by the task.

## Quality

Pull requests validate skill metadata, links, evaluations, Claude/Tessl bundles, unit tests, and clean Agent Skills discovery.

```sh
python3 .github/scripts/validate_repository.py
python3 .github/scripts/run_behavior_evals.py
python3 -m unittest discover -s tests -v
npx skills add . --list
```

Run an intentional forward-eval sample with an installed agent CLI:

```sh
python3 .github/scripts/run_behavior_evals.py --execute --suite behavior --skill flutter-app-workflow --max-cases 1
```

Forward evals compare baseline and skill-injected answers, then grade observable expectations. Execution is opt-in because it calls an external model and can incur cost; use `--all-cases` only for a deliberate collection run.

Behavior cases may declare only the linked references needed for that scenario. This keeps forward evaluation aligned with production progressive disclosure instead of injecting every supporting document.

Validate Agent Skills specification conformance with the pinned official linter:

```sh
bash .github/scripts/run_dart_skills_lint.sh
```

Release validation additionally requires a dated changelog entry and rejects a version that remains marked `Unreleased`:

```sh
python3 .github/scripts/validate_repository.py --release
```

The collection contains **21 skills**, **59 behavior-focused evaluation cases**, and **17 cross-catalog routing cases**.

## Sources and contribution

The collection is informed by the official [Flutter Agent Plugins](https://github.com/flutter/agent-plugins), [Flutter documentation](https://docs.flutter.dev), and [Dart documentation](https://dart.dev). It adds end-to-end coordination, package-neutral routing, and repository quality gates rather than copying upstream skills verbatim.

See [`docs/SOURCES.md`](docs/SOURCES.md) for source policy and [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution requirements.

## License

Distributed under the [BSD 3-Clause License](LICENSE). Flutter and Dart are trademarks of Google LLC. This independent project is not affiliated with or endorsed by Google or the Flutter team.
