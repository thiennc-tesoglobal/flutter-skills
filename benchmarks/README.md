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

## v0.3.0 initial result

Run on 2026-08-30 with `codex-cli 0.151.0-alpha.7.2`, its default model, the same agent as solver and judge, and an 80-point behavior threshold.

| Behavior case | Baseline | With skill | Delta |
|---|---:|---:|---:|
| `flutter-package-development` | 55 | 98 | +43 |
| `flutter-runtime-debugging` | 8 | 100 | +92 |
| `flutter-ai-integration` | 0 | 100 | +100 |
| `flutter-authentication` | 75 | 100 | +25 |
| `flutter-in-app-purchases` | 33 | 100 | +67 |
| `flutter-product-analytics` | 67 | 67 | 0 |
| **Average** | **39.67** | **94.17** | **+54.5** |

Five of six behavior cases and all seven routing cases passed. The analytics failure showed that “end-to-end pending” did not identify the unavailable provider-ingestion and downstream-dashboard boundaries precisely enough, so the skill now requires those boundaries to be recorded explicitly as unverified. The failed raw run remains in [codex-default-initial.json](v0.3.0/codex-default-initial.json); no post-fix score is claimed until the fixed profile is rerun.

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
