# Platform toolchain migrations

Package or Flutter SDK upgrades can change native minimums and build-tool compatibility even when Dart resolution succeeds. Inspect the exact target Flutter release and plugin requirements instead of copying the newest Gradle, Kotlin, JDK, Xcode, CocoaPods, Swift, or deployment-target values from another project.

## Android

Record the Gradle wrapper, Android Gradle Plugin, Kotlin mode/version, JDK, compile/target/min SDK, NDK, namespace, repositories, and custom build logic. Check the Flutter migration guide for the target release and each affected plugin's supported ranges. Upgrade a compatible toolchain set, then run the repository's Android build and a representative launch before changing another layer.

Do not overwrite custom Gradle configuration with a newly generated template. Compare templates or official migrations selectively. Preserve product flavors, signing references, application ID, native libraries, and CI JDK selection. A build-tool migration does not authorize changing signing keys or publishing an artifact.

## Apple platforms

Record Xcode, Swift, CocoaPods or Swift Package Manager usage, deployment targets, Podfile hooks, build configurations, schemes, entitlements, and plugin minimums. Keep the highest justified minimum platform across Flutter and required plugins; raising it is a product-support decision, not a routine cleanup.

Regenerate dependency integration only with the repository's established commands. Review Podfile, lockfile, Xcode project, xcconfig, entitlements, and generated plugin changes. Build the affected simulator/device configuration without altering signing ownership.

## Other targets

For web and desktop, inspect renderer/runtime changes, browser or OS minimums, CMake/MSBuild/Xcode requirements, native assets, and plugin support. Report unsupported targets rather than allowing a late missing-plugin or build failure.

## Verification matrix

For every supported affected platform, record toolchain versions and run dependency resolution, generation, analysis, tests, and at least a representative debug or release-like build appropriate to the claim. Add device/runtime verification for changed plugin behavior. Keep CI pins aligned, but route pipeline implementation to `flutter-ci-cd`.

## Sources

- [Flutter breaking changes](https://docs.flutter.dev/release/breaking-changes)
- [Build and release Android apps](https://docs.flutter.dev/deployment/android)
- [Build and release iOS apps](https://docs.flutter.dev/deployment/ios)
- [Flutter supported platforms](https://docs.flutter.dev/reference/supported-platforms)
