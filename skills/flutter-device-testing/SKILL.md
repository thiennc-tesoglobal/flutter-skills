---
name: flutter-device-testing
description: Operate and verify Flutter apps on a concrete emulator, simulator, browser, desktop, or physical device. Use when runtime target control, launch, logs, screenshots, permissions, deep links, or on-device integration tests are explicitly needed; not for generic verification covered by focused tests.
---

# Flutter Device Testing

Use the smallest target matrix that proves the changed behavior, then state what was and was not exercised.

## Discover before acting

Run `flutter devices` and inspect the project's supported platforms. Select targets by stable device identifier when multiple devices are available. Do not erase, reset, or recreate a user's device without explicit need and authorization.

## Workflow

1. Confirm dependencies and generated code are ready.
2. Launch with the correct flavor, entrypoint, and defines.
3. Capture build or runtime errors from Flutter and platform logs.
4. Exercise the exact user flow, including backgrounding, rotation, keyboard, deep link, or permission state when relevant.
5. Save focused screenshots or test output when visual/runtime evidence matters.
6. Run integration tests on the chosen target when durable automation is required.

Use running-app inspection from the Dart and Flutter MCP server when it is available and useful. Otherwise use `flutter run`, `flutter logs`, `flutter drive` or `flutter test integration_test`, and native tools such as `adb` or `simctl` only where they add necessary platform control.

## Reliability

Do not assume a successful compilation proves correct runtime behavior. Avoid hardcoded coordinates when semantic finders or integration-test APIs are available. Make test setup explicit and clean up only artifacts created by the test.

## Sources

- [Flutter CLI](https://docs.flutter.dev/reference/flutter-cli)
- [Integration testing](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
