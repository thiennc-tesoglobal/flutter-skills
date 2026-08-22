# Project preflight

Inspect before changing the project:

1. Read `pubspec.yaml`, `pubspec.lock`, `analysis_options.yaml`, and relevant workspace/package configuration.
2. Map `lib/`, `test/`, `integration_test/`, platform folders, generated code, and feature boundaries.
3. Identify the actual state, navigation, networking, persistence, dependency-injection, serialization, and localization approaches.
4. Check Dart and Flutter SDK constraints instead of assuming the newest local syntax is allowed.
5. Discover runnable targets with `flutter devices` and project tests with `flutter test` or workspace tooling.
6. Check the working tree and preserve unrelated user changes.

Summarize only decisions that affect implementation. Do not turn preflight into a large report when the project is straightforward.
