---
name: flutter-app-workflow
description: Plan, build, refactor, and verify a complete Flutter app or substantial multi-file feature. Use when work spans project structure, UI, state, data, testing, and device delivery; use a specialist directly for narrow fixes.
---

# Flutter App Workflow

Deliver a runnable, maintainable result with evidence. Preserve the user's product choices and the project's existing conventions unless a migration is explicitly requested.

## Start with preflight

Read [project preflight](references/project-preflight.md) before planning. Establish the SDK constraints, enabled platforms, architecture, state management, navigation, data packages, code generation, flavors, tests, and available devices.

Do not add a package merely because it is familiar. Reuse an existing solution when it is adequate and compatible.

## Route specialists

Load only the skills required by the task:

- Architecture or state boundaries: `flutter-architecture`, `flutter-state-management`
- Widgets, layout, motion, or routing: the matching Flutter UI specialist
- APIs or storage: `flutter-networking`, `flutter-persistence`
- Language or async behavior: `dart-language`, `dart-concurrency`
- Quality and delivery: testing, accessibility, performance, platform, release, or device specialists

For a narrow request, hand ownership to the specialist instead of running the full workflow.

## Deliver in vertical slices

1. Define user-visible behavior and acceptance evidence.
2. Choose the smallest architectural change that fits the existing project.
3. Implement one coherent path through model, data, state, and UI.
4. Add focused tests with the behavior, not after an unrelated rewrite.
5. Run the narrowest useful checks after each slice.
6. Complete the final delivery checklist in [delivery verification](references/delivery-verification.md).

Keep files cohesive and names domain-oriented. Split a file when it owns multiple responsibilities or its independent testing/reuse becomes valuable; do not split merely to satisfy a line-count rule.

## Stop conditions

Do not claim completion while required build, analysis, test, or runtime evidence is failing. If an unavailable SDK, credential, signing identity, backend, or device blocks verification, report exactly what was verified and what remains blocked.

## Sources

- [Flutter app architecture](https://docs.flutter.dev/app-architecture)
- [Flutter testing](https://docs.flutter.dev/testing)
- [Supported platforms](https://docs.flutter.dev/reference/supported-platforms)
