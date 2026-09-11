---
name: flutter-app-workflow
description: Coordinate end-to-end delivery of a complete Flutter app or feature across UI, state, data, tests, bounded implementation review, and runtime verification. Use for broad vertical-slice ownership; not for data-only sync/cache, one screen or form, or contained work that merely touches multiple files or two domains.
---

# Flutter App Workflow

Deliver a runnable, maintainable result with evidence. Preserve the user's product choices and existing conventions unless migration is explicitly requested.

## Preflight

Read [project preflight](references/project-preflight.md) before planning. When the task includes a ticket, read it through the available GitHub integration or CLI, reconcile it with the current code, and state the agreed implementation scope before editing. Do not edit behavior whose requirement or ownership remains materially ambiguous. After exhausting available evidence, give a compact understanding checkpoint—current and intended behavior, evidence versus hypotheses, in-scope work, affected shared consumers, data contracts, time or localization semantics, tests and platforms outside scope, and inspection that can continue—then ask one focused question. Pair each affected boundary with why the behavior reaches it and the exact code, contract, or test evidence still needed; a list of module names is not an impact map. Treat supplied project facts as preflight evidence; inspect repository constraints (SDK, platforms, packages, architecture, tests, flavors, devices) instead of re-asking. Reuse adequate existing solutions; do not add packages merely for familiarity.

## Route specialists

Load only the available specialists needed for the vertical slice:
- Architecture & state: `flutter-architecture`, `flutter-state-management`
- UI & visual: `flutter-ui-design`, `flutter-visual-effects`, or matching UI specialist
- Data, AI & product: `flutter-networking`, `flutter-persistence`, `flutter-authentication`, `flutter-in-app-purchases`, `flutter-product-analytics`, `flutter-ai-integration`
- Platform & ops: `flutter-package-development`, `flutter-notifications`, `flutter-background-execution`, `flutter-dependency-upgrades`, `flutter-observability`, `flutter-runtime-debugging`
- Language & security: `dart-language`, `dart-concurrency`, `flutter-security`, `flutter-code-review`
- Quality & delivery: testing, accessibility, performance, CI/CD, release, device specialists

If a specialist is unavailable, continue with this workflow's preflight and vertical-slice rules; do not claim it was loaded or silently install skills. Hand focused work (e.g. form validation, API cache) to dedicated specialists rather than running this workflow.

## Deliver in vertical slices

1. Establish the current behavior, intended behavior, supported root cause, scope, impact map, and acceptance evidence.
2. Choose the smallest architectural change fitting the existing project.
3. Implement one coherent path through model, data, state, and UI.
4. Add focused tests with the behavior, not after an unrelated rewrite.
5. Run narrow checks after each slice.
6. Before claiming completion, follow [post-implementation review](references/post-implementation-review.md), satisfy its clean-implementation gate, resolve material findings within the authorized scope, and rerun affected checks.
7. Follow [delivery verification](references/delivery-verification.md), including evidence labels and scoped Git handoff.

Keep files cohesive and domain-oriented. Do not split files solely for line counts.

## Stop conditions

Do not claim completion while required checks fail. If credentials, devices, or backends block verification, report what was verified and what remains blocked.

## Sources

- [Flutter app architecture](https://docs.flutter.dev/app-architecture)
- [Flutter testing](https://docs.flutter.dev/testing)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
- [Supported platforms](https://docs.flutter.dev/reference/supported-platforms)
