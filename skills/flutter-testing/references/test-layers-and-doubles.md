# Test layers and doubles

Choose the narrowest layer that crosses the risk boundary.

- Unit: transformations, policies, state machines, repositories behind controlled dependencies.
- Widget: rendering and semantics, focus, gestures, navigation wiring, and state-driven UI.
- Golden: intentional visual contracts under controlled fonts, locale, surface, device pixel ratio, and theme.
- Integration/device: plugins, platform channels, persistence integration, startup, deep links, and critical cross-screen flows.

Flutter integration tests cannot operate arbitrary native permission dialogs, notifications, or platform views as if they were Flutter widgets. Keep domain decisions behind a seam for deterministic tests, then verify the native boundary on a supported device workflow.

Prefer small stateful fakes when behavior matters. Use mocks at narrow interaction boundaries where call verification is the contract. Avoid mirroring the production object graph in test setup.

## Sources

- [Flutter testing overview](https://docs.flutter.dev/testing/overview)
- [Flutter integration tests](https://docs.flutter.dev/testing/integration-tests)
