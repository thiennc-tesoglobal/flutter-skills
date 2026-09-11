# Evaluation strategy

Use the least expensive tier that can answer the current question. Forward evaluation invokes external agents and must remain an explicit maintainer action; repository CI only validates cases, profiles, fixtures, and matrix configuration.

## Trust model

- The default workflow needs only the authenticated Codex CLI: Codex solves and scores the fixed cases, compiler-backed fixtures verify executable behavior, and a named human reviews 10–15% of any published run.
- Treat same-model scoring as regression screening, not independent judgment. It must not be reported as cross-provider evidence.
- When another authenticated provider is available, prefer an independent primary judge and add the solver family as a second judge to measure agreement. A behavior case passes only when every judge reaches the threshold and every mandatory criterion passes.
- Treat model agreement as calibration evidence, not proof that either judge is correct.
- Keep raw failed and successful results. Do not discard disagreement or failed cases to improve reported averages.
- Do not claim cross-provider evidence when either CLI is unauthenticated, unavailable, or timed out.

## Cost tiers

### Pull request

Run only changed-skill cases during ordinary authoring. Use the fixed [PR smoke profile](../evals/profiles/pr-smoke.json) when shared routing, runner, or catalog behavior changes.

```sh
python3 .github/scripts/run_eval_matrix.py \
  --execute \
  --output-dir benchmarks/matrix
```

The default [Codex matrix](../evals/codex-matrix.json) skips baselines and needs 19 model invocations for the six behavior and seven routing cases. It uses the existing Codex CLI login; no Claude account or OpenAI API key is added or required.

### Nightly or periodic audit

The [nightly representative profile](../evals/profiles/nightly-representative.json) contains one behavior case for every skill and all routing cases. The Codex-only matrix with skipped baselines needs 139 model invocations. Refresh baselines only when measuring skill lift.

### Release

The [release profile](../evals/profiles/release-full.json) resolves all behavior and routing cases. The default Codex-only run with skipped baselines needs 443 model invocations before retries. Run it only with an explicit budget and retained output.

## Optional cross-agent matrix

Normal validation checks the Codex-only default without invoking a model:

```sh
python3 .github/scripts/run_eval_matrix.py
```

The optional [cross-agent matrix](../evals/cross-agent-matrix.json) is also validated in CI but never executed there. Use it only after both CLIs are authenticated:

```sh
python3 .github/scripts/run_eval_matrix.py \
  --execute \
  --matrix .github/evals/cross-agent-matrix.json \
  --output-dir benchmarks/matrix
```

The PR profile needs 50 model invocations for the two skipped-baseline role-swap runs. Use `--profile profiles/nightly-representative.json` or `--profile profiles/release-full.json` for a broader tier. If Claude is unavailable, skip this matrix and report Codex, executable, and human-review evidence separately.

Do not add another provider until its CLI has a verified non-interactive input/output contract, bounded timeout behavior, model selection, authentication failure handling, and equivalent tool isolation.

## Human calibration

Create a deterministic 15% sample tied to the raw result and response hashes:

```sh
python3 .github/scripts/review_eval_results.py sample \
  benchmarks/matrix/codex-solver.json \
  --rate 0.15 \
  --seed 20260911 \
  --output benchmarks/matrix/codex-solver-human-review.json
```

Fill `reviewer`, `reviewed_at`, each `human_met`, and optional notes. Then report agreement per judge:

```sh
python3 .github/scripts/review_eval_results.py summarize \
  benchmarks/matrix/codex-solver.json \
  benchmarks/matrix/codex-solver-human-review.json
```

Changing the source result or sampled response invalidates the hashes and blocks summarization.

## Compiler-backed fixtures

Executable cases live under `.github/evals/executable`. Validate their manifests in normal CI:

```sh
python3 .github/scripts/run_executable_evals.py
```

Run a case only with explicit authorization:

```sh
python3 .github/scripts/run_executable_evals.py \
  --execute \
  --case dart-concurrency-latest-wins \
  --output benchmarks/unreleased/dart-concurrency-latest-wins-executable.json
```

The runner copies a fixture to a temporary workspace, disables shell commands, allows only declared source owners to change, rejects verifier or package-metadata edits, and then executes allowlisted `dart` or `flutter` checks with timeouts. Keep fixtures deterministic, dependency-light, free of credentials, and independent of live services. Add `flutter build` only when compilation at that platform boundary is material; prefer format, analysis, focused tests, and runtime assertions for ordinary cases.
