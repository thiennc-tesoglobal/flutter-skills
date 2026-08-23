# Quality gates

Use this reference for pull-request and branch confidence checks.

## Derive commands from the repository

Use the project's declared Flutter version or version manager. Respect workspaces, package filters, code-generation scripts, build flavors, and existing test grouping. Do not replace repository scripts with generic commands unless the scripts are broken and the task includes fixing them.

A typical gate order is dependency resolution, generated-code freshness when generated files are committed, formatting check, static analysis, fast unit/widget tests, then selected integration or platform jobs. This is a starting shape, not a requirement to run irrelevant work.

- Formatting in CI must check without rewriting the checkout.
- Analysis must preserve the repository's warning/fatal policy.
- Generation freshness may run the established generator in the disposable CI checkout, then must fail on an unexpected diff rather than commit, upload as replacement source, or conceal generated output.
- Golden tests verify committed expectations with the repository's non-update command; never pass an update flag or rewrite expectations in a normal CI gate.
- Coverage should be uploaded as evidence. Enforce a numeric threshold only when the repository already defines one or the user selects it.
- Matrix jobs should cover supported combinations with distinct risk, not every theoretical SDK/platform permutation.

Cache only reproducible dependencies or tool downloads. Every concrete cache key must include the relevant lockfiles, OS/architecture, and effective Flutter/Dart/tool version rather than mentioning them only in prose. A cold miss and a hit must run the same correctness gates and produce equivalent results. Avoid caching signed artifacts or broad mutable build directories such as `.dart_tool` or `build/` when stale mutable output can mask errors.

Use concurrency/cancellation for superseded branch runs where safe. Preserve logs and machine-readable reports needed to diagnose failures, with bounded retention.

## Failure behavior

Make required gates fail loudly and stop dependent delivery. Do not use `continue-on-error`, ignored exit codes, retries, or job-level optionality to conceal deterministic failures. Retry only demonstrated transient operations with a bound; surface the final failure and evidence.

## Sources

- [Testing Flutter apps](https://docs.flutter.dev/testing/overview)
- [Flutter integration tests](https://docs.flutter.dev/testing/integration-tests)
