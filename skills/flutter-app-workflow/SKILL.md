---
name: flutter-app-workflow
description: Coordinate end-to-end delivery of a complete Flutter app or feature across UI, state, data, tests, and runtime verification. Use for broad vertical-slice ownership; not for data-only sync/cache, one screen or form, or contained work that merely touches multiple files or two domains.
---

# Flutter App Workflow

Deliver a runnable, maintainable result with evidence. Preserve the user's product choices and the project's existing conventions unless a migration is explicitly requested.

## Start with preflight

Read [project preflight](references/project-preflight.md) before planning. Establish the SDK constraints, enabled platforms, architecture, state management, navigation, data packages, code generation, flavors, tests, and available devices.

When the request already supplies project facts, treat them as preflight evidence and carry material constraints such as the SDK and established packages into the plan. Do not ask for the same facts again; inspect the repository later only for details that were not supplied.

Do not add a package merely because it is familiar. Reuse an existing solution when it is adequate and compatible.

## Route specialists

First identify which specialist skills are discoverable in the current environment. Load only the available skills required by the task:

- Architecture or state boundaries: `flutter-architecture`, `flutter-state-management`
- Visual direction or polish: `flutter-ui-design`
- Advanced glass, blur, refraction, shaders, or custom optical rendering: `flutter-visual-effects`
- Widget composition, layout mechanics, motion, or routing: the matching Flutter UI specialist
- APIs or storage: `flutter-networking`, `flutter-persistence`
- Sign-in, session, or passkey behavior: `flutter-authentication`
- Store purchases, subscriptions, or entitlement restoration: `flutter-in-app-purchases`
- Product events, funnels, attribution, or experiments: `flutter-product-analytics`
- Model-backed product behavior: `flutter-ai-integration`
- Reusable Dart packages or Flutter plugins: `flutter-package-development`
- Local or remote notification delivery: `flutter-notifications`
- OS-scheduled, foreground-service, or headless background work: `flutter-background-execution`
- Flutter/Dart SDK, dependency graph, lockfile, or native toolchain upgrades: `flutter-dependency-upgrades`
- Production diagnostics, crash context, logs, or traces: `flutter-observability`
- Reproducing and diagnosing a failure in a running app: `flutter-runtime-debugging`
- Language or async behavior: `dart-language`, `dart-concurrency`
- Security or privacy hardening: `flutter-security`
- Explicit review or audit findings: `flutter-code-review`
- Quality and delivery: testing, accessibility, performance, platform, CI/CD, release, or device specialists

If a named specialist is unavailable, continue with this workflow's preflight, preservation, vertical-slice, and verification rules. Do not claim that a missing skill was loaded, silently install it, or block straightforward work merely because the optional specialist is absent. Report the limitation only when its missing domain guidance prevents reliable delivery.

Use this workflow only when the request needs end-to-end coordination across UI, state or business logic, data, tests, and runtime delivery. A task is still focused when it touches multiple files or two specialist domains, such as API plus persistence or an asynchronously validated form. Hand focused ownership to the matching specialists instead of running this workflow.

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
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
- [Supported platforms](https://docs.flutter.dev/reference/supported-platforms)
