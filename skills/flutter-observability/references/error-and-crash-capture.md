# Error and crash capture

Use this reference to make error coverage explicit instead of assuming one global handler sees everything.

## Coverage map

- Flutter framework callbacks: preserve console visibility where useful and forward `FlutterError.onError` details to the established reporter.
- Unhandled root-isolate errors outside Flutter callbacks: use `PlatformDispatcher.instance.onError` and return the truthful handled status.
- Child isolates: install error forwarding for isolates the app creates; the root dispatcher does not receive their errors automatically.
- Explicitly handled failures: record only actionable failures at the correct severity. Expected validation, cancellation, or offline states are not crashes.
- Native crashes, ANRs, and platform exceptions: confirm what the selected vendor and platform SDK actually capture; Dart handlers alone do not cover them.

Do not wrap an existing startup sequence in a zone merely by habit. Zones, dispatchers, framework handlers, and vendor integrations can overlap; preserve existing initialization and verify each controlled failure arrives once.

## Context and grouping

Normalize errors at an adapter boundary. Attach release/build, environment, platform, current operation, and safe correlation context. Preserve the original exception and stack when the vendor supports it. Use stable fingerprints only when default grouping is demonstrably wrong; overly broad fingerprints hide distinct failures.

Provide a safe user fallback for build/render failures where the product requires it, without exposing exception text. An error widget is UX recovery, not a substitute for reporting or fixing the failure.

## Verification

Use controlled non-production fixtures for a framework error, async root-isolate error, and child-isolate error when the app uses isolates. Confirm single ingestion, symbolicated stack quality, correct release/environment, and no secret leakage. Remove or protect deliberate crash triggers before shipping.

## Sources

- [Handling errors in Flutter](https://docs.flutter.dev/testing/errors)
- [PlatformDispatcher.onError](https://api.flutter.dev/flutter/dart-ui/PlatformDispatcher/onError.html)
- [FlutterError.onError](https://api.flutter.dev/flutter/foundation/FlutterError/onError.html)

