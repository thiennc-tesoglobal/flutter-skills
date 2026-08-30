# Public API and package quality

Use this reference when the package's reusable Dart or Flutter contract is the main concern.

## Contract first

Identify intended consumers and supported SDKs before choosing syntax or dependencies. Keep the public surface deliberate: export only supported APIs, avoid leaking implementation types through signatures, and document lifecycle, concurrency, error, and ownership behavior that callers must understand.

Prefer additive compatible evolution. Before removing, renaming, narrowing, or changing behavior, inspect current package versioning, changelog policy, repository consumers, and deprecation history. A deprecation needs a usable replacement and enough time for consumers to migrate; semantic versioning labels impact but does not make a breaking change safe.

Do not expose a package-specific dependency type merely for implementation convenience when a stable platform-neutral contract would suffice. Conversely, do not add abstraction that has no consumer or compatibility value.

## Package structure

- Keep the primary public entrypoint under `lib/`; keep implementation details under `lib/src/` and unexported unless intentionally public.
- Put executable examples in `example/` when users need to see integration, configuration, lifecycle, or platform behavior.
- Keep generated output reproducible. Record generator inputs and versions, and do not hand-edit generated files.
- Include only files needed by consumers. Check licenses and provenance for bundled code, native libraries, fonts, models, or other assets.
- Document supported platforms and actual limitations rather than relying on directory presence as proof of support.

## Dependency discipline

Read SDK and dependency constraints before recommending current language features or package versions. Prefer the smallest compatible dependency surface, avoid unnecessary direct dependencies, and do not use overrides to conceal an unresolved public constraint.

For Flutter packages, do not impose Provider, Riverpod, Bloc, Dio, or another product-level choice on consumers unless that dependency is intrinsic to the package's contract.

## Tests as consumer evidence

Test through public entrypoints wherever possible. Cover documented success, failures, cancellation, disposal, concurrency, and unsupported behavior. Use an example app or integration fixture for behavior that unit or widget tests cannot prove.

When changing public behavior, add a regression test that would fail for the old defect and consider a small representative consumer compile test. Avoid assertions that merely mirror private implementation details.
