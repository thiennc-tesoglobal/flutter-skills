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

## Sources

- [Flutter widget testing](https://docs.flutter.dev/cookbook/testing/widget/introduction)
- [Flutter integration testing](https://docs.flutter.dev/testing/integration-tests)
