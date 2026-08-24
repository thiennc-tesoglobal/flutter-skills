# Source policy

Flutter and Dart evolve quickly. Technical guidance in this collection should prefer current primary sources and preserve the target project's declared SDK constraints.

## Primary sources

- [Flutter Agent Plugins](https://github.com/flutter/agent-plugins)
- [Flutter Agent Skills documentation](https://docs.flutter.dev/ai/agent-skills)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
- [Flutter AI evaluations](https://docs.flutter.dev/ai/evals)
- [Flutter app architecture](https://docs.flutter.dev/app-architecture)
- [Flutter UI documentation](https://docs.flutter.dev/ui)
- [Material Design for Flutter](https://docs.flutter.dev/ui/design/material)
- [Flutter theming](https://docs.flutter.dev/cookbook/design/themes)
- [Flutter typography](https://docs.flutter.dev/ui/design/text/typography)
- [Flutter platform adaptations](https://docs.flutter.dev/ui/adaptive-responsive/platform-adaptations)
- [Flutter testing](https://docs.flutter.dev/testing)
- [Flutter performance](https://docs.flutter.dev/perf)
- [Flutter accessibility](https://docs.flutter.dev/ui/accessibility)
- [Flutter platform integration](https://docs.flutter.dev/platform-integration)
- [Flutter security](https://docs.flutter.dev/security)
- [Flutter obfuscation limitations](https://docs.flutter.dev/deployment/obfuscate)
- [Flutter Widget Previewer](https://docs.flutter.dev/tools/widget-previewer)
- [Flutter FFI and build hooks](https://docs.flutter.dev/platform-integration/bind-native-code)
- [Flutter package and plugin development](https://docs.flutter.dev/packages-and-plugins/developing-packages)
- [Flutter offline-first support](https://docs.flutter.dev/app-architecture/design-patterns/offline-first)
- [Flutter background processes](https://docs.flutter.dev/packages-and-plugins/background-processes)
- [Android background work](https://developer.android.com/develop/background-work)
- [Apple Background Tasks](https://developer.apple.com/documentation/backgroundtasks)
- [OWASP Mobile Application Security Verification Standard](https://mas.owasp.org/MASVS/)
- [Android security checklist](https://developer.android.com/privacy-and-security/security-tips)
- [Flutter deployment](https://docs.flutter.dev/deployment)
- [Dart language](https://dart.dev/language)
- [Dart concurrency](https://dart.dev/language/concurrency)
- [Dart package documentation](https://pub.dev)
- [Dart Pub package dependencies](https://dart.dev/tools/pub/dependencies)
- [Flutter breaking changes and migration guides](https://docs.flutter.dev/release/breaking-changes)
- [Figma developer documentation](https://developers.figma.com/)
- [Figma Code Connect](https://developers.figma.com/docs/code-connect/)

Package-specific claims should use the package publisher's documentation and confirm compatibility with the project's SDK constraints. Community articles may provide examples but must not override current primary documentation.

MCP integration must be capability-aware: use the semantic or runtime tools when the current agent exposes them, and preserve a CLI fallback so each skill remains portable. Agent behavior claims should be supported by forward evaluations when practical; deterministic schema checks alone are not behavior evidence.

## Upstream relationship

The official `flutter/agent-plugins` repository is a trusted reference and inspiration for focused workflows such as architecture, responsive layout, routing, HTTP, serialization, localization, and tests. This repository maintains independent wording, broader delivery coordination, package-neutral decision rules, and its own evaluations and quality gates.
