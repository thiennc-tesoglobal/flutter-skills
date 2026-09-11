# Post-implementation review

Run a distinct review pass after the implementation and its focused tests, while the intended behavior and changed diff are both available.

## Bound the review

Review the current task's diff, acceptance criteria, tests, and directly affected consumers. Trace changed data across parsing, state, UI, lifecycle, persistence, navigation, and platform boundaries only where the implementation reaches them. Do not turn unrelated legacy issues or preferred rewrites into blockers.

Use `flutter-code-review` when it is available. Otherwise apply the same bounded risk review directly. Load a deeper specialist only when the changed behavior enters that domain or a finding needs verification.

## Check reachable failures

Prioritize concrete paths that can cause incorrect data, crashes, leaks, duplicate effects, stale async results, authorization gaps, broken loading or error recovery, inaccessible flows, route or back-stack failures, platform divergence, and release breakage. Check whether tests cover the failure path at the cheapest meaningful layer.

For each suspected problem, identify its trigger, affected code, user or delivery impact, and proportionate correction. Discard findings that cannot be tied to the changed behavior or a directly affected consumer.

## Clean-implementation gate

Require the final code to follow the repository's formatter, analyzer, lints, architecture, naming, ownership, and generated-code conventions. Review the complete task diff and remove implementation residue: temporary logging or probes, commented-out alternatives, stale TODOs created by the change, unused imports or dependencies, dead helpers, duplicate sources of truth, unjustified abstractions, unrelated generated churn, and accidental files.

Do not make checks pass by weakening assertions, skipping tests, suppressing diagnostics, broadening types, swallowing errors, or deleting durable regression coverage. Prefer the smallest cohesive implementation that reuses adequate existing code, keeps error and lifecycle behavior explicit, and avoids a new dependency or layer without demonstrated value.

Run the repository's format, static analysis, focused tests, and relevant broader checks. Inspect final Git status, changed-file list, and diff so successful commands do not hide unintended scope.

## Close the loop

Resolve material findings that remain inside the original implementation scope. Re-review the resulting diff and rerun the smallest checks that exercise each correction, followed by the task's completion checks. If a valid finding needs a product decision, credential, backend change, destructive action, or scope expansion, report it as an explicit remaining item instead of silently broadening the task.

Completion evidence should distinguish inspected risks from executed checks. A clean review does not upgrade a mock, simulator, or static check into stronger runtime evidence.
