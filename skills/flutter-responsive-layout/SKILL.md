---
name: flutter-responsive-layout
description: Build or repair adaptive Flutter layouts across phones, tablets, foldables, desktop, and web. Use for constraints, breakpoints, overflow, orientation, and input-mode adaptation; not for general widget state architecture.
---

# Flutter Responsive Layout

Design from the constraints supplied by the parent, not from a guessed device model.

## Diagnose

Reproduce the layout on the failing viewport with text scaling and the relevant platform chrome. Read the first meaningful constraint or overflow failure and identify which widget imposed the incompatible size.

## Rules

- Use `LayoutBuilder` when a subtree responds to local constraints and `MediaQuery` when behavior depends on window or accessibility properties.
- Choose a small set of content-driven breakpoints; do not branch on specific device names.
- Prefer flexible constraints, wrapping, scrolling, or alternate composition over fixed width/height patches.
- Keep readable content widths on large displays instead of stretching every element.
- Adapt navigation and information density when space changes materially.
- Respect safe areas, display features, keyboard insets, text scaling, and both pointer and touch input.
- Avoid `IntrinsicHeight` or repeated intrinsic measurement on hot, complex trees without evidence.

## Verification

Exercise boundary widths just below and above each breakpoint, long localized strings, large text, landscape, and the intended desktop/web window sizes. Add a focused widget or golden test for regressions that visual assertions can represent reliably.

## Sources

- [Adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Building responsive layouts](https://docs.flutter.dev/ui/adaptive-responsive/best-practices)
