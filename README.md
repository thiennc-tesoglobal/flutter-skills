# Flutter Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-28-2ea44f)](skills/)
[![Validation](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml/badge.svg)](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml)
[![License](https://img.shields.io/badge/License-BSD--3--Clause-blue)](LICENSE)

28 package-neutral Agent Skills for building, reviewing, testing, and releasing Flutter apps without forcing a state-management package or folder structure.

> Bộ skill giúp AI coding agent đọc dự án Flutter, chọn đúng chuyên môn, triển khai và xác minh kết quả theo conventions sẵn có.

## Install

Choose skills interactively:

```sh
npx @thiennc/flutter-skills
```

Start with the end-to-end workflow for a complete app or feature:

```sh
npx @thiennc/flutter-skills \
  --agent codex \
  --skill flutter-app-workflow
```

Install one specialist when the task is focused:

```sh
npx @thiennc/flutter-skills \
  --agent codex \
  --skill flutter-ui-design
```

Project installation is the default. Add `--global` to use the selected skills across projects.

The direct GitHub installer remains available: `npx skills add thiennc-tesoglobal/flutter-skills`.

> In a regular terminal, the installer asks which skills and agents to use. Inside Codex, it may detect Codex and install non-interactively; pass `--skill` explicitly when you do not want all 28 skills.

### Claude Code bundles

```sh
/plugin marketplace add thiennc-tesoglobal/flutter-skills
/plugin install flutter-core-skills@flutter-skills
```

Available bundles: `all-flutter-skills`, `flutter-core-skills`, `flutter-ui-skills`, and `flutter-engineering-skills`.

## Catalog

| Area | Skills |
|---|---|
| Workflow | `flutter-app-workflow`, `flutter-dependency-upgrades`, `flutter-build-release`, `flutter-ci-cd`, `flutter-device-testing` |
| Dart | `dart-language`, `dart-concurrency` |
| Architecture | `flutter-architecture`, `flutter-state-management` |
| UI | `flutter-ui-design`, `flutter-figma-workflow`, `flutter-visual-effects`, `flutter-ui-patterns`, `flutter-responsive-layout`, `flutter-animation`, `flutter-navigation` |
| Data | `flutter-networking`, `flutter-persistence` |
| Quality | `flutter-code-review`, `flutter-security`, `flutter-testing`, `flutter-performance`, `flutter-observability`, `flutter-accessibility`, `flutter-localization` |
| Platform | `flutter-background-execution`, `flutter-platform-integration`, `flutter-notifications` |

## Use

Codex and compatible agents first see skill names and descriptions, then load only the relevant `SKILL.md` and references.

```text
Use $flutter-app-workflow to build a polished offline-first todo app,
preserve the existing architecture, add tests, and verify it on Android.
```

For a focused task, name the specialist directly or let the agent route from the request. Installing every skill does not load every skill into the task context.

## Quality

The catalog contains **28 skills**, **97 behavior-focused evaluation cases**, and **33 cross-catalog routing cases**. Validation checks metadata, references, bundles, tests, and clean installation discovery.

Representative baseline-versus-skill benchmark results and the reproducible profile are published in [benchmarks](benchmarks/README.md). They are a transparent sample, not a claim that one model or a small case set proves every workflow.

See [CONTRIBUTING.md](CONTRIBUTING.md) for validation and contribution instructions, and [docs/SOURCES.md](docs/SOURCES.md) for the source policy.

## License

BSD 3-Clause. Flutter and Dart are trademarks of Google LLC. This independent project is not affiliated with or endorsed by Google or the Flutter team.
