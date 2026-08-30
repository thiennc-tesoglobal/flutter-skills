---
name: flutter-package-development
description: Create, evolve, test, or prepare reusable Dart packages and Flutter plugins for distribution. Use when the package itself, its public API, platform support, federation, example app, compatibility, or publication readiness is the deliverable; route app-owned native bridges to flutter-platform-integration.
---

# Flutter Package Development

Treat a reusable package as a versioned contract consumed by projects you do not control. Preserve the repository's SDK range, package shape, supported platforms, API conventions, and release process unless the user requests a deliberate migration.

## Inspect before changing

Read `pubspec.yaml`, SDK constraints, public entrypoints and exports, analysis options, generated-code configuration, examples, tests, platform folders, CI, changelog, and publication metadata. Inspect current consumers when available before changing a public symbol or behavior.

Choose the smallest viable shape:

- A Dart package for reusable Dart-only behavior.
- A Flutter package for reusable Flutter APIs without native implementation.
- A plugin when a public Dart API requires platform implementations.
- An FFI package when the underlying native API and supported toolchain make FFI the appropriate boundary.
- A federated plugin only when independent ownership, release cadence, extension, or endorsement justifies multiple packages.

Do not turn an app-specific bridge into a public package merely because reuse is possible.

## Load references conditionally

- Read [public API and package quality](references/public-api-and-quality.md) when designing exports, evolving compatibility, documenting behavior, or preparing a reusable package for consumers.
- Read [plugins and federation](references/plugins-and-federation.md) when native implementations, platform interfaces, federation, registration, FFI, or generated platform contracts are involved.
- Read [publication readiness](references/publication-readiness.md) when checking package metadata, dry runs, release notes, or an intended publication.

## Boundaries

- `flutter-platform-integration` owns an app's native boundary and the native mechanics inside a plugin; use both when reusable package design and platform implementation are material.
- `flutter-dependency-upgrades` owns consuming or upgrading dependencies in an application.
- `flutter-build-release` owns application artifacts and store delivery, not pub package publication.
- Preserve the package's existing state-management, networking, persistence, and code-generation choices unless the task explicitly changes them.

## Verification

Format and analyze the supported SDK surface, run unit and widget tests, and exercise the example or integration fixture on every affected platform. Test public behavior rather than private structure. For a compatibility change, verify representative consumers or the oldest and newest supported dependency combinations where practical.

Run `dart pub publish --dry-run` only when publication readiness is in scope. Publishing, changing package ownership, applying tags, or creating releases requires explicit authorization; a successful dry run is not a publication.

State the platforms and SDK combinations actually exercised and any remaining consumer, platform, or registry boundary.

## Sources

- [Developing packages and plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages)
- [Creating packages](https://dart.dev/tools/pub/create-packages)
- [Publishing packages](https://dart.dev/tools/pub/publishing)
- [Package layout conventions](https://dart.dev/tools/pub/package-layout)
