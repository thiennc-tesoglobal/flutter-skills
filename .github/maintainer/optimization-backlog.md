# Measured optimization backlog

Use this file for failures and weak signals observed in executed forward evaluations. Do not rewrite a public skill from intuition alone: link the raw result, identify the failed behavior, add the smallest regression case, and rerun that case before changing broader guidance.

## Open

| Priority | Evidence | Measured signal | Next evaluation |
|---|---|---|---|
| P1 | [`v0.3.0/codex-default-initial.json`](../../benchmarks/v0.3.0/codex-default-initial.json) | `flutter-product-analytics:sdk-log-is-not-end-to-end-proof` scored 67 because a generic “pending” state did not name unavailable provider-ingestion and dashboard access as unverified. The skill fix passed at 100, but only one provider-neutral case exercises this boundary. | Add a case where provider ingestion is visible but downstream warehouse or experiment attribution is not, and require a per-boundary evidence ledger. |
| P1 | [`v0.3.0/codex-default-initial.json`](../../benchmarks/v0.3.0/codex-default-initial.json) | `flutter-package-development:dry-run-does-not-authorize-publish` initially exposed a weak tool-free readiness plan. The calibrated skill response passed, but release authorization and authenticated publisher identity remain easy to conflate. | Add a case with a successful dry run but an unexpected publisher or package version; require the agent to stop publication without blocking the completed review. |
| P2 | [`v0.2.0/codex-default-initial.json`](../../benchmarks/v0.2.0/codex-default-initial.json) | The original Figma case asked a tool-free harness to implement files and prove screenshots, making the rubric impossible rather than measuring skill behavior. | Add evaluator validation that flags expectations requiring filesystem, device, design-tool, provider-console, or registry evidence when the solver has no matching capability. |

## Closed and retained as regressions

- `flutter-runtime-debugging:runtime-fix-repeats-original-flow`: require a clean launch for every affected target and record unsupported-platform behavior instead of extrapolating from hot reload.
- `flutter-in-app-purchases:sandbox-readiness-is-not-store-publication`: accept an executable sandbox evidence plan when store credentials or consoles are unavailable; never fabricate readiness or publish.
- `flutter-product-analytics:sdk-log-is-not-end-to-end-proof`: record client dispatch, provider ingestion, and downstream dashboard or funnel evidence separately.
- `flutter-webview` routing: the first focused run interpreted “existing Flutter WebView package” as reusable-package development and selected `flutter-package-development`. The app-focused prompt now states that the existing dependency is not being changed or distributed; both WebView and OAuth boundary cases pass in the retained rerun.
- Forward-evaluation execution: bound each solver invocation so a stalled agent cannot hang the full profile.

## Promotion rule

Move an item to closed only after the focused executed case passes and the raw before-and-after result is retained. A current primary-source correction can bypass the measured-failure requirement, but must cite the changed source and receive a behavior or routing regression case where practical.
