# Plugins and federation

Use this reference when a reusable package contains platform implementations or must coordinate multiple packages.

## Shape the plugin deliberately

Keep the app-facing API platform-neutral and map native failures into documented Dart behavior. Provide an explicit unsupported-platform result instead of allowing a late missing-plugin failure.

Choose channels, a typed generated contract, FFI, JS interop, or platform views based on the native API and target platforms. Apply `flutter-platform-integration` for the detailed native boundary, lifecycle, threading, memory, permission, and view-embedding work.

## Federation threshold

A federated plugin separates the app-facing package, platform interface, and platform implementations. Accept that versioning and compatibility cost only when at least one of these is real:

- implementations have independent owners or release cadences;
- third parties need a stable extension point;
- endorsed and non-endorsed implementations must coexist;
- platform implementations need independent dependency or platform constraints.

Do not split a small app-owned bridge or single-team plugin into multiple packages by default.

Keep the platform interface difficult to implement accidentally, version it compatibly, and test registration and fallback behavior. Applications should normally depend on the app-facing package, not an implementation package, unless a non-endorsed override is intentional.

## Platform evidence

For every claimed platform, verify registration, normal results, mapped failures, permissions, attach/detach behavior, repeated engine instances where applicable, and release-mode linking. Test the oldest and newest interface/implementation combinations permitted by constraints when compatibility across independently released packages matters.

An example app should demonstrate required configuration and provide a repeatable integration fixture. Compilation on one host platform does not prove all declared platforms work.
