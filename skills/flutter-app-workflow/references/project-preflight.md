# Project preflight

Inspect before changing the project:

1. Read `pubspec.yaml`, `pubspec.lock`, `analysis_options.yaml`, and relevant workspace/package configuration.
2. Map `lib/`, `test/`, `integration_test/`, platform folders, generated code, and feature boundaries.
3. Identify the actual state, navigation, networking, persistence, dependency-injection, serialization, and localization approaches.
4. Check Dart and Flutter SDK constraints instead of assuming the newest local syntax is allowed.
5. Discover runnable targets with `flutter devices` and project tests with `flutter test` or workspace tooling.
6. Check the working tree and preserve unrelated user changes.
7. Discover Dart and Flutter MCP capabilities when the agent environment exposes them. Prefer those tools for semantic analysis, symbol lookup, dependency edits, tests, formatting, or running-app inspection when they improve evidence; otherwise use the project's existing scripts and Flutter/Dart CLI commands. Do not make delivery depend on optional MCP availability.

Separate supplied facts from unknowns. Carry an explicitly provided SDK version, architecture, package stack, platform, or device into the plan as an established constraint. Later repository inspection should confirm and refine those facts, not present them as unknown or replace them with a preferred default.

Summarize only decisions that affect implementation. Do not turn preflight into a large report when the project is straightforward.
