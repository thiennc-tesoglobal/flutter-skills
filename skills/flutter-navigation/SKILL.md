---
name: flutter-navigation
description: Implement or review Flutter routing, deep links, nested navigation, restoration, redirects, and URL synchronization. Use for Navigator, Router, or an existing routing package; do not introduce a package when simple Navigator behavior is sufficient.
---

# Flutter Navigation

Model navigation as application state when URLs, deep links, restoration, or multiple navigators require it; use simpler imperative navigation for genuinely local flows.

## Inspect first

Identify the current router, route ownership, authentication flow, tab/shell structure, supported platforms, URL requirements, and state restoration expectations. Preserve the existing routing package unless migration is requested.

## Rules

- Keep route names, path parameters, and argument decoding typed or centrally validated.
- Make redirect logic deterministic and free of redirect loops.
- Preserve intended back behavior across Android system back, browser history, iOS gestures, nested navigators, and modals.
- Use nested navigation only for independent histories such as tab shells.
- Parse deep links into domain-safe state and define behavior for unknown or unauthorized destinations.
- Keep navigation side effects outside widget `build`.
- Do not place large domain objects directly in URLs or restoration state.

## Verification

Test cold deep links, warm links, back/forward behavior, authentication redirects, invalid parameters, restoration where required, and each supported shell/tab history.

## Sources

- [Flutter navigation and routing](https://docs.flutter.dev/ui/navigation)
- [Deep linking](https://docs.flutter.dev/ui/navigation/deep-linking)
