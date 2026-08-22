---
name: flutter-ui-patterns
description: Build and refactor Flutter widget composition, themes, forms, and UI state boundaries. Use for reusable widgets and screen implementation; route responsive constraints, navigation, animation, and performance diagnosis to dedicated skills.
---

# Flutter UI Patterns

Build declarative interfaces whose widget tree reflects state clearly and remains easy to test.

## Composition

- Extract widgets around cohesive UI concepts, reuse, isolated state, or test value—not arbitrary file length.
- Prefer immutable widget configuration and `const` constructors where valid.
- Keep side effects out of `build`; trigger them from lifecycle-safe controllers, state objects, or explicit callbacks.
- Use the project theme and semantic design tokens instead of scattered literal styles.
- Preserve platform conventions where Material and Cupertino behavior should differ.
- Give forms explicit validation, focus, submission, and error behavior.
- Keep keys stable and purposeful; do not use random or changing keys to force rebuilds.

## State boundaries

Own controllers, focus nodes, and animation controllers in the lifecycle that creates them, and dispose them there. Hoist state only when another component must coordinate it.

## Verification

Test meaningful rendered states and interactions. Check text scaling, keyboard input where supported, light/dark themes, and at least the smallest and largest intended form factors.

## Sources

- [Flutter UI](https://docs.flutter.dev/ui)
- [Widget catalog](https://docs.flutter.dev/ui/widgets)
