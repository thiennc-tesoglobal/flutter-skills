# Plugin development

Use this reference for reusable packages that expose platform functionality. An application-specific native bridge usually does not need a published or federated plugin architecture.

## Choose package shape

- Dart package: reusable Dart API without Flutter platform implementation.
- Plugin package: Dart API backed by one or more platform implementations.
- FFI package: C-compatible native code or binaries exposed through `dart:ffi` and the supported build system.
- Federated plugin: app-facing API, platform interface, and independently maintained platform implementations.

Choose package-separated federation only when independent ownership, release cadence, platform extension, or endorsement justifies the versioning overhead. Do not split a small app-owned plugin into many packages by default.

## Public API and platform interface

Keep the app-facing API platform-neutral and document supported behavior, failures, concurrency, lifecycle, and unsupported targets. Evolve it compatibly under semantic versioning.

For federated plugins, make the platform interface difficult to implement accidentally, preserve compatibility between interface and implementations, and test registration and fallback behavior. Do not let applications depend directly on an implementation package unless a non-endorsed override is intentional.

## Native implementations

Support current embedding and lifecycle APIs for each target. Avoid static process-wide assumptions when multiple Flutter engines are possible. Scope permissions and manifest or entitlement changes to the feature.

Keep generated channel or FFI code reproducible. Record generator versions and commands, avoid hand-editing generated files, and verify checked-in output matches sources when the project commits generation artifacts.

## Package quality

Provide a minimal example app or integration fixture when native behavior cannot be proven by unit tests. Test the Dart-facing contract, each supported platform implementation, registration, error mapping, lifecycle, and release builds.

Document platform support, setup, privacy or permission impact, breaking changes, license obligations, and binary provenance. Publishing, endorsing third-party implementations, or changing public package ownership requires explicit authorization.

## Federated compatibility

Test the oldest and newest supported interface/implementation combinations that the version constraints permit. Verify unsupported methods fail clearly and that adding a platform does not silently change behavior on existing targets.
