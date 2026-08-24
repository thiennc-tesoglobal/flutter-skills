# SDK and package upgrades

## Establish the version contract

Identify the repository's Flutter/Dart source of truth: a checked-in version-manager file, CI pin, container image, or documented channel. Preserve it and update all consumers consistently; do not rely on whichever global Flutter happens to be installed.

For a Flutter SDK change, compare the current and target release notes, breaking-change guides, Dart language version, supported platform/toolchain requirements, and plugin compatibility. Treat skipped stable releases as cumulative migrations. Use `dart fix --dry-run` or equivalent current tooling to inspect available source migrations before applying and reviewing them.

For packages, use `dart pub outdated` or the Flutter wrapper to distinguish Current, Upgradable, Resolvable, and Latest. Latest is not automatically compatible. Upgrade one package or a related cohort when their APIs and generators must move together; avoid a blind collection-wide `--major-versions` change in a production repository.

## Reproducible sequence

1. Record baseline SDK output, dependency graph, analysis, tests, generation, and representative builds.
2. Read publisher migration notes and target SDK bounds for the selected cohort.
3. Update declared constraints intentionally and resolve through Pub rather than editing the lockfile by hand.
4. Review direct and transitive lock changes, removed or changed package sources, and content-hash warnings.
5. Run project-owned generators and inspect generated as well as hand-written diffs.
6. Format, analyze, test, and build each affected supported target.

Application repositories normally commit their lockfile for reproducible deployments. Published packages generally validate a supported constraint range and normally do not commit the root lockfile; preserve the repository's established and current Pub policy.

If the upgrade changes runtime behavior, add a focused regression test or device check. Do not mix unrelated architecture, formatting, or design refactors into the migration diff.

## Sources

- [How to use Dart packages](https://dart.dev/tools/pub/packages)
- [dart pub get and lockfiles](https://dart.dev/tools/pub/cmd/pub-get)
- [Package versioning](https://dart.dev/tools/pub/versioning)
- [Upgrade Flutter](https://docs.flutter.dev/install/upgrade)
- [Flutter release notes](https://docs.flutter.dev/release/release-notes)
- [Flutter breaking changes and migration guides](https://docs.flutter.dev/release/breaking-changes)
