# Security verification

Match evidence to the agreed review type and authorization.

## Static evidence

Inspect source, generated configuration, platform manifests, entitlements, dependency locks, build variants, and relevant native code. Search for credentials and dangerous patterns without printing discovered secret values into chat, logs, patches, or reports.

Confirm reachability and platform applicability before reporting a scanner result. Flutter binaries can trigger native-tool false positives that do not apply to compiled Dart code; document why a finding is applicable or dismissed.

## Dependency review

Record the resolved version and source from the lockfile. Check current advisories using an authorized, reputable database or package publisher. Determine whether the vulnerable component, platform, and code path are actually used.

Do not upgrade packages, regenerate locks, suppress advisories, or accept breaking migrations unless the user asked for remediation. A clean advisory scan does not prove that custom code is secure.

## Dynamic and release evidence

When authorized and tooling is available, verify the relevant release-like variant on representative targets. Focus on observable controls such as transport policy, link routing, session expiry, storage cleanup, WebView navigation, permission denial, account switching, and redacted telemetry.

Do not test production endpoints, accounts, or third parties outside the stated scope. Stop before destructive payloads, credential rotation, denial-of-service behavior, bypass attempts against real users, or data extraction not required by the test.

## Finding format

Each actionable finding should contain:

- Severity based on realistic impact and preconditions.
- Asset and affected platform or build variant.
- File and tight line location where possible.
- Evidence and reachable abuse path.
- User or business impact.
- Smallest viable remediation and compatibility cost.
- Verification needed after the fix.

Keep confirmed findings separate from hardening suggestions, false positives, accepted risks, and questions that require product or backend context. Do not inflate severity because a security header or scanner keyword is absent.

## Completion criteria

Report exactly what was inspected and executed, what could not be verified, and any credentials or external systems deliberately left untouched. Security work is complete only relative to the stated scope; avoid an unconditional “secure” verdict.
