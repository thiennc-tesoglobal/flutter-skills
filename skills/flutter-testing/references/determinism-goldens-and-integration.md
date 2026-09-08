# Determinism, goldens, and integration

## Async determinism

Expose clocks, randomness, schedulers, transports, and storage through existing project seams. Await a named state or event. If progress may never complete, use a bounded loop or framework timeout that reports the missing condition. Cancel timers, streams, subscriptions, and pending work in teardown.

`pumpAndSettle` is suitable only when the UI is expected to settle. For repeating animations, polling, or intentionally live streams, advance a known duration or pump until an explicit observable condition.

## Goldens

Stabilize fonts, locale, theme, surface size, pixel ratio, animation time, and fixtures. Store focused variants rather than one enormous application screenshot. A golden update is a review artifact: render the diff, explain the intended change, and reject unrelated pixel movement.

### Cross-Platform Font Rasterization

Operating systems use different text rasterization engines (macOS CoreText, Linux FreeType/HarfBuzz, Windows DirectWrite), causing subtle subpixel anti-aliasing differences that make golden PNGs fail across OS boundaries:
- **Pin Golden Generation Environment**: Standardize golden file generation and updates to a single OS environment (typically Linux via Docker or a dedicated CI runner) so byte-level pixel comparisons remain identical.
- **Load Consistent Fonts**: Use `FontLoader` or bundle explicit mock fonts (e.g. `Ahem` or Google Fonts loaded in `flutter_test_config.dart`) to eliminate differences in system font availability.
- **Comparator Thresholds**: When cross-platform local verification is needed, configure a bounded difference threshold via `GoldenFileComparator` or use maintained packages (e.g., `alchemist` or `golden_toolkit`) rather than loose visual approximations.
- **Never Auto-Update in CI**: Treat `--update-goldens` as a local, intentional authoring command. CI pipelines must only verify against committed golden baselines and fail on drift.

## Integration

Seed independent data, reset durable state, and avoid ordering dependencies. Assert meaningful user milestones instead of implementation timing. Run the smallest supported device matrix that covers platform-specific behavior and report skipped targets explicitly.

## Disposable source and runtime artifacts

Separate two cleanup lifecycles:

- Source lifecycle: an AI-created one-off `*_test.dart` probe is removed by the host workflow after its exact path, prior existence, and tracked state have been recorded. Arrange cleanup immediately, retain the test command's exit status and relevant output, and run cleanup on both pass and failure. Do not use recursive directory deletion or wildcard cleanup under `test/` or `integration_test/`.
- Test runtime lifecycle: files, databases, servers, view overrides, bindings, and subscriptions created while a test runs are released with the narrowest framework teardown. Register `addTearDown` as soon as a resource exists; use a uniquely created temporary directory when filesystem isolation is appropriate.

After host cleanup, verify every recorded disposable path is absent and inspect scoped Git status or diff against the baseline. This final check catches interrupted cleanup and untracked generated artifacts. Preserve existing test files and keep any test that now serves as a useful regression contract.

## Sources

- [Flutter widget testing](https://docs.flutter.dev/cookbook/testing/widget/introduction)
- [Flutter integration testing](https://docs.flutter.dev/testing/integration-tests)
- [Flutter `addTearDown`](https://api.flutter.dev/flutter/flutter_test/addTearDown.html)
- [Dart `Directory.createTemp`](https://api.dart.dev/dart-io/Directory/createTemp.html)
