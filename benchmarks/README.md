# Public benchmark

The fixed profile in [public-benchmark.json](../.github/evals/public-benchmark.json) compares normal agent behavior with the same agent receiving the selected skill and separately checks catalog routing.

Run it with:

```sh
python3 .github/scripts/run_behavior_evals.py \
  --execute \
  --agent codex \
  --judge-agent codex \
  --agent-timeout 180 \
  --profile .github/evals/public-benchmark.json \
  --output benchmarks/v0.3.0/codex-default.json
```

Raw results are intentionally committed without removing responses, judgments, selections, or failed cases. Case identifiers resolve to the versioned prompts and rubrics under `skills/*/evals` and `.github/evals`. The current profile is a six-case behavior and seven-case routing sample on one agent configuration; it is useful regression evidence, not proof of quality across every model, app, or skill.

## Unreleased focused result

Four hardening cases now score 100 with `codex-cli 0.153.4`: [accessibility semantics cleanup](unreleased/flutter-accessibility-semantics-cleanup.json), [rapid stream re-trigger ownership](unreleased/dart-concurrency-rapid-retrigger.json), [signature-aware integration startup](unreleased/flutter-device-testing-integration-startup.json), and [locale-bounded orphan handling](unreleased/flutter-text-rendering-locale-orphan.json). Retained initial results document the measured gaps and rubric calibration: [semantics cleanup 67](unreleased/flutter-accessibility-semantics-cleanup-initial.json), [stream ownership 75](unreleased/dart-concurrency-rapid-retrigger-initial.json), and integration startup at [67](unreleased/flutter-device-testing-integration-startup-initial.json) then [65](unreleased/flutter-device-testing-integration-startup-signature-initial.json). These focused runs skip baselines and prove response behavior only.

The `flutter-app-workflow` understanding-gate case now scores 100 with `codex-cli 0.153.4`; see the [final result](unreleased/flutter-app-workflow-understanding-gate.json). The retained [65-point first run](unreleased/flutter-app-workflow-understanding-gate-initial.json), [75-point tool-free calibration run](unreleased/flutter-app-workflow-understanding-gate-tool-free-initial.json), and [80-point impact-map run](unreleased/flutter-app-workflow-understanding-gate-impact-map-initial.json) showed that asking the right question is insufficient by itself: the agent must first state current versus intended behavior and connect every affected boundary to concrete code, contract, or test evidence without fabricating unavailable inspection.

The new `flutter-app-workflow` post-implementation review case scored 100 with `codex-cli 0.153.4`; see the [final result](unreleased/flutter-app-workflow-post-implementation-review.json). The retained [25-point initial result](unreleased/flutter-app-workflow-post-implementation-review-initial.json) showed that a tool-free forward evaluation must assess the required completion plan rather than demand file edits and executed checks that its harness forbids.

The new `flutter-responsive-layout` overlap and bounded viewport-matrix cases each scored 100 with `codex-cli 0.153.1`. The focused runs skipped baselines and prove response behavior only; see the [overlap result](unreleased/flutter-responsive-layout-overlap.json) and [matrix result](unreleased/flutter-responsive-layout-matrix.json). The matrix's two 67-point runs are retained as [the initial result](unreleased/flutter-responsive-layout-matrix-initial.json) and [the compatibility-gate result](unreleased/flutter-responsive-layout-matrix-compatibility-gate-initial.json); they showed that a tool-free prompt must supply inspected SDK capabilities before requiring concrete compatible APIs.

## v0.3.0 result

Run on 2026-08-30 with `codex-cli 0.151.0-alpha.7.2`, its default model, the same agent as solver and judge, and an 80-point behavior threshold.

| Behavior case | Baseline | With skill | Delta |
|---|---:|---:|---:|
| `flutter-package-development` | 30 | 96 | +66 |
| `flutter-runtime-debugging` | 15 | 100 | +85 |
| `flutter-ai-integration` | 0 | 100 | +100 |
| `flutter-authentication` | 100 | 100 | 0 |
| `flutter-in-app-purchases` | 42 | 100 | +58 |
| `flutter-product-analytics` | 67 | 100 | +33 |
| **Average** | **42.33** | **99.33** | **+57.0** |

All six behavior cases and all seven routing cases passed. See [codex-default.json](v0.3.0/codex-default.json) for the final raw run. The first run is retained as [codex-default-initial.json](v0.3.0/codex-default-initial.json); its analytics failure showed that “end-to-end pending” did not identify the unavailable provider-ingestion and downstream-dashboard boundaries precisely enough, so the skill now records those boundaries explicitly as unverified.

## v0.2.0 result

Run on 2026-08-24 with `codex-cli 0.149.0-alpha.4.1`, its default model, the same agent as solver and judge, and an 80-point behavior threshold.

| Behavior case | Baseline | With skill | Delta |
|---|---:|---:|---:|
| `flutter-ui-design` | 78 | 100 | +22 |
| `flutter-figma-workflow` | 91 | 96 | +5 |
| `flutter-architecture` | 75 | 100 | +25 |
| `flutter-performance` | 0 | 100 | +100 |
| `flutter-testing` | 75 | 100 | +25 |
| **Average** | **63.8** | **99.2** | **+35.4** |

All five routing cases passed. See [codex-default.json](v0.2.0/codex-default.json) for every prompt, response, judgment, and selected skill.

The first run is retained as [codex-default-initial.json](v0.2.0/codex-default-initial.json). It exposed an impossible Figma eval that demanded implementation and screenshots while the eval harness intentionally disallowed files and tools. The case was changed to evaluate an implementation plan from already-inspected design evidence, then the full fixed profile was rerun; the failed raw run remains available for audit.
