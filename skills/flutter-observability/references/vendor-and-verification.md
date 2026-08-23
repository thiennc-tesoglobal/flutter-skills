# Vendor and verification

Use this reference when selecting, preserving, or proving a telemetry backend.

## Preserve before selecting

Inspect existing packages, native SDK setup, service files, initialization, dashboards, release scripts, privacy disclosures, and backend configuration before diagnosing or prescribing. Dashboard symptoms alone do not prove whether release metadata, build identity, symbol generation, upload, or backend association failed. If those artifacts cannot be inspected, list them as required evidence and keep causes and fixes conditional. Repair the current stack when it can satisfy the requirement. If no stack exists, compare only current candidates compatible with the SDK, target platforms, data residency/privacy needs, native crash coverage, symbolication, offline behavior, sampling controls, licensing, and operating cost. Present tradeoffs before adding one.

Keep vendor APIs behind a narrow application adapter. Do not recreate every vendor feature in a universal abstraction; expose only the signals the product owns.

## Release identity and symbols

Use the same release/build and environment identity in the app, artifact, telemetry event, and symbol upload. When obfuscation or native symbols are enabled, coordinate with `flutter-build-release` so mapping/debug symbols are retained securely and uploaded to the matching release. A received event with an unusable stack is not complete crash observability.

## End-to-end proof

In a non-production project/environment:

1. initialize the adapter with the intended consent state;
2. emit one uniquely identifiable handled test event;
3. trigger one controlled error for each required coverage class;
4. confirm ingestion once, release/environment, attributes, breadcrumbs, grouping, and stack quality in the backend;
5. inspect the captured payload for disallowed data;
6. test offline/rate-limited behavior and app non-interference.

Do not use a production crash, upload symbols, create backend projects, or change retention/access controls without the authority required for those external mutations. If access is unavailable, distinguish local instrumentation verification from backend ingestion verification.
