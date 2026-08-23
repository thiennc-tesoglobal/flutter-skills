---
name: flutter-build-release
description: Configure and verify Flutter flavors, environments, signing, versioning, release artifacts, obfuscation symbols, and store-ready builds. Use for local artifact configuration; route CI provider workflows to flutter-ci-cd, and do not publish or change live credentials without explicit authorization.
---

# Flutter Build and Release

Produce reproducible artifacts for the requested platforms while preserving secrets and external-release authority.

## Preflight

Read SDK constraints, flavors/schemes, bundle/application IDs, version source, signing configuration, environment injection, CI, native deployment targets, and store requirements. Never print or commit secrets, keystores, provisioning material, or service credentials.

## Rules

- Keep environment selection explicit and fail safely when required values are missing.
- Align Dart defines, Android variants, Apple schemes/configurations, and service files by environment.
- Increment versions according to the repository's release policy.
- Build the exact requested artifact and keep symbols needed for crash deobfuscation.
- Treat obfuscation as code-hardening, not secret protection.
- Validate icons, names, permissions, privacy declarations, and target-specific metadata.
- Make CI use pinned or declared tool versions where practical.
- Require explicit authorization immediately before store upload, signing-credential mutation, tagging, or publishing.

## Verification

Run formatting, analysis, tests, and a clean release build for each intended target/flavor. Install or serve the built artifact and smoke-test startup plus a critical flow. Record artifact path, version, flavor, target, and remaining store-side work.

## Sources

- [Flutter deployment](https://docs.flutter.dev/deployment)
- [Build and release an Android app](https://docs.flutter.dev/deployment/android)
- [Build and release an iOS app](https://docs.flutter.dev/deployment/ios)
