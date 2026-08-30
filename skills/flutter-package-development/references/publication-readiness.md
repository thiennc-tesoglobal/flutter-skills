# Publication readiness

Use this reference for a package intended for pub.dev or another package registry. Preparation does not authorize publication.

## Readiness review

Confirm the package name, version, description, homepage or repository, issue tracker, license, SDK constraints, supported platforms, topics where used, and included files. Review `README.md`, API documentation, example, and `CHANGELOG.md` from a new consumer's perspective.

Check that:

- the release version matches the intended compatibility impact;
- public APIs are documented and exported intentionally;
- generated files and native binaries have reproducible provenance;
- secrets, local paths, credentials, private endpoints, and unrelated fixtures are excluded;
- analysis and tests pass under the supported SDK policy;
- package score warnings are understood rather than suppressed blindly.

Run `dart pub publish --dry-run` and inspect its complete file list and warnings. When practical, pack or consume the candidate from a clean temporary project so local path dependencies and undeclared files cannot hide defects.

## Authorization boundary

Do not run `dart pub publish`, create a registry release, change publisher ownership, create or push a tag, or upload signing material without explicit user authorization for that external mutation. If authorized, resolve the exact package and version first, stop on registry or identity ambiguity, and report the resulting immutable version.
