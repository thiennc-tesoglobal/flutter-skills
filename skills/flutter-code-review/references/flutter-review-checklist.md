# Flutter review checklist

Read only the sections touched by the change.

## Dart and asynchronous behavior

- Nullability, exhaustiveness, equality, collection mutation, serialization, and public API compatibility.
- Awaited work, cancellation, stale-result ordering, error propagation, stream completion, isolate transferability, and cleanup.
- Work triggered from `build`, duplicated by rebuilds, or retained beyond its owner.

## Widgets and lifecycle

- Correct creation and disposal of controllers, focus nodes, subscriptions, observers, and animation resources.
- Stable keys and state identity across reorder, navigation, and restoration.
- State ownership, repeated side effects, mounted checks after asynchronous gaps, and callbacks after disposal.
- Loading, empty, error, disabled, retrying, and long-content states.

## Architecture and data

- UI bypassing state or repository boundaries, circular dependencies, duplicated sources of truth, and schema details leaking upward.
- Cache freshness, transaction boundaries, migration compatibility, offline conflicts, deletion semantics, retry safety, and user isolation.
- Wire-data validation, authentication refresh races, pagination identity, and sensitive logging.

## Accessibility, localization, and layout

- Semantic labels and actions, focus order, keyboard operation, target size, contrast, text scaling, and reduced motion.
- RTL behavior, plural and locale formatting, hardcoded user-facing strings, narrow constraints, and overflow.

## Performance

- Work on the UI isolate, unbounded memory or caches, unnecessary rebuild scope, expensive layout/paint, image decoding, startup work, and leaked ownership.
- Require profile-mode or comparable evidence before asserting a performance regression that source alone cannot establish.

## Platform and release

- Unsupported-platform behavior, permissions, platform-channel validation, lifecycle attachment, native threading, and platform-view tradeoffs.
- Build variants, entitlements, manifests, signing references, symbols, versioning, generated files, and CI/release artifact correctness.

## Tests

- Tests should fail before the fix for the right reason and cover the changed behavior, not implementation trivia.
- Check determinism, clocks, async settling, fake boundaries, cleanup, golden stability, platform assumptions, and whether skipped or weakened assertions hide regression.
