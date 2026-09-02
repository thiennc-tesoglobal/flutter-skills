# Flutter Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-36-2ea44f)](skills/)
[![Validation](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml/badge.svg)](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml)
[![License](https://img.shields.io/badge/License-BSD--3--Clause-blue)](LICENSE)

36 package-neutral Agent Skills for building, reviewing, testing, and shipping Flutter and Dart projects.

The skills help coding agents choose the right workflow, preserve the project's existing architecture and packages, and verify changes with evidence.

## Install

Choose skills interactively:

```sh
npx @thiennc/flutter-skills
```

Install a focused skill for Codex:

```sh
npx @thiennc/flutter-skills --agent codex --skill flutter-app-workflow
```

Project installation is the default. Add `--global` to install for all projects.

You can also install directly from GitHub:

```sh
npx skills add thiennc-tesoglobal/flutter-skills
```

## Plugins

Codex:

```sh
codex plugin marketplace add thiennc-tesoglobal/flutter-skills
codex plugin add flutter-skills@flutter-skills
```

Claude Code:

```sh
/plugin marketplace add thiennc-tesoglobal/flutter-skills
/plugin install flutter-core-skills@flutter-skills
```

Claude bundles: `all-flutter-skills`, `flutter-core-skills`, `flutter-ui-skills`, and `flutter-engineering-skills`.

## Use

Name a skill when the task is specific:

```text
Use $flutter-openapi-client to read this Swagger contract and generate
only the Customer APIs using the project's existing networking stack.
```

For broader work, start with `$flutter-app-workflow`. Agents load only the selected skill and relevant references, not the full catalog.

## Catalog

| Area | Skills |
|---|---|
| Workflow | `flutter-app-workflow`, `flutter-dependency-upgrades`, `flutter-build-release`, `flutter-ci-cd`, `flutter-device-testing` |
| Dart | `dart-language`, `dart-concurrency` |
| Architecture | `flutter-architecture`, `flutter-state-management` |
| UI | `flutter-ui-design`, `flutter-figma-workflow`, `flutter-visual-effects`, `flutter-ui-patterns`, `flutter-responsive-layout`, `flutter-animation`, `flutter-navigation` |
| Data & AI | `flutter-networking`, `flutter-openapi-client`, `flutter-persistence`, `flutter-ai-integration` |
| Identity & product | `flutter-authentication`, `flutter-in-app-purchases`, `flutter-product-analytics` |
| Quality | `flutter-code-review`, `flutter-security`, `flutter-testing`, `flutter-runtime-debugging`, `flutter-performance`, `flutter-observability`, `flutter-accessibility`, `flutter-localization` |
| Platform & packages | `flutter-background-execution`, `flutter-platform-integration`, `flutter-package-development`, `flutter-notifications`, `flutter-webview` |

## Quality

The catalog contains **36 skills**, **158 behavior-focused evaluation cases**, and **54 cross-catalog routing cases**. See [benchmarks](benchmarks/README.md) for measured examples and [CONTRIBUTING.md](CONTRIBUTING.md) for validation and contribution rules.

## License

BSD 3-Clause. Flutter and Dart are trademarks of Google LLC. This project is independent and is not endorsed by Google or the Flutter team.
