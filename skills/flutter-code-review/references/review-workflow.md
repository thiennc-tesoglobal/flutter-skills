# Review workflow

## Gather the change

Resolve the exact base and head when available. Inspect status, diff metadata, renamed and generated files, dependency or lockfile changes, migrations, platform configuration, and tests. Do not assume an untracked file is part of a commit or that generated output is hand-authored.

Read repository instructions before applying generic conventions. Understand the requested behavior and preservation constraints from the task, issue, tests, or nearby implementation.

## Build a risk map

Identify changed entry points, state owners, data boundaries, asynchronous operations, native surfaces, user-visible states, and release configuration. Trace values through the smallest path needed to decide whether a defect is real.

High-risk changes commonly include:

- Authentication, payment, deletion, migration, synchronization, or destructive operations.
- Lifecycle ownership, subscriptions, controllers, background work, and cancellation.
- Parsing untrusted data, native boundaries, permissions, WebViews, and deep links.
- Navigation/back-stack changes and state restoration.
- Build variants, signing, entitlements, manifests, generated code, and dependency upgrades.

## Validate a candidate finding

Before reporting it:

1. Confirm the code path is reachable in the changed behavior.
2. Check callers, guards, ownership, and framework or package guarantees.
3. Identify a concrete input, state, timing, platform, or configuration that triggers failure.
4. Determine whether an existing test actually covers the case.
5. Prefer a focused command or test when it can confirm the claim without mutating external state.

Avoid comments based only on file length, unfamiliar patterns, possible future requirements, or personal style. Do not request abstractions without showing the duplication, dependency, testing, or change-cost problem they solve.

## Severity

- P0: Immediate widespread harm, irreversible data loss, or critical security compromise with a clear reachable path.
- P1: High-impact correctness, security, crash, or release failure likely to affect real users.
- P2: Material defect with narrower conditions or a maintainability issue likely to cause incorrect changes.
- P3: Low-impact but actionable issue worth fixing; omit pure preference.

Calibrate severity from impact and likelihood, not category names. Missing test coverage is not automatically P1, and the word “security” does not automatically make a finding critical.

## Finding format

Use a concise title, file and tight line range, failure path, impact, and fix direction. Keep evidence self-contained so the author does not need to infer why the code fails.

After findings, optionally list assumptions or verification gaps. Summaries must not bury findings or repeat the diff.
