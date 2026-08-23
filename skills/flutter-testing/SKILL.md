---
name: flutter-testing
description: Design, write, or review Flutter unit, widget, golden, and integration tests. Use for test strategy, regressions, fakes, async UI behavior, and end-to-end flows; use device testing for operational emulator or hardware control.
---

# Flutter Testing

Test observable behavior at the cheapest layer that provides confidence.

## Choose the layer

- Unit tests: pure logic, state transitions, repositories, parsing, and failure policy.
- Widget tests: rendering, semantics, interaction, focus, navigation wiring, and state-to-UI behavior.
- Golden tests: stable visual contracts where platform/font control makes comparison meaningful.
- Integration tests: critical flows, plugin integration, performance, and behavior requiring a real target.

Do not replace behavior assertions with implementation details such as private method calls or exact widget-tree shape.

## Reliability

- Inject clocks, randomness, storage, and transports when determinism matters.
- Prefer small fakes over large mock graphs; verify outputs and side effects rather than incidental calls.
- Control async progress with the test framework; avoid arbitrary sleeps.
- Pump until a known state or bounded completion, not an unbounded `pumpAndSettle` when animations or timers persist.
- Give tests independent data and clean up global bindings, files, databases, and subscriptions.
- Update a golden only after reviewing the rendered difference.

## Verification

Use the Dart and Flutter MCP test capability when available or the repository's established test command otherwise. Run the narrow test during iteration, then the relevant suite. Report skipped platforms, flaky behavior, or environment dependencies instead of treating them as success.

## Sources

- [Flutter testing](https://docs.flutter.dev/testing)
- [Integration testing](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
