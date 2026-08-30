# Reproduction and attachment

Use this reference when the failure depends on a running target, process lifecycle, startup path, or intermittent trigger.

## Define the failure

Capture a compact reproduction contract:

- target platform and stable device identifier;
- Flutter flavor, entrypoint, defines, and build mode;
- clean start versus warm state;
- exact user or system event sequence;
- expected and actual observable result;
- frequency, timing, network, account, permission, locale, and lifecycle conditions that affect it.

Preserve failing evidence before clearing caches, reinstalling, changing accounts, or restarting services. Do not reset or erase a user-owned device merely to simplify setup.

## Attach or launch

Prefer attaching to the already failing Flutter process when restarting would destroy the state. Use supported runtime discovery or `flutter attach` with an unambiguous target. Launch a fresh process when startup configuration, plugin registration, generated code, assets, native dependencies, or initialization order is under test.

Choose restart depth based on the changed boundary:

- hot reload for compatible Dart source changes where preserved state is desirable;
- hot restart when Dart initialization or state must restart;
- full stop and launch for startup arguments, native registration, assets, permissions, or platform lifecycle;
- rebuild or reinstall for native dependencies, manifests, entitlements, signing, or generated native integration.

Do not repeatedly change restart depth until the symptom disappears; record which transition changes the behavior because that is diagnostic evidence.

## Reduce without distorting

Stabilize fixtures, inputs, and ordering while retaining the suspected boundary. Use breakpoints or bounded instrumentation to identify the first divergence from correct state. For a race, exercise reversed completion, cancellation, disposal, background/foreground, and repeated entry rather than adding arbitrary delays.

For permission and lifecycle failures, trace the result from the platform callback through the plugin or adapter's error mapping, application state owner, and disposed or resumed consumer. Do not pre-commit to a null check or other defensive patch before this path identifies the first invalid transition; the correct fix may belong in result mapping, ownership, cancellation, or lifecycle coordination instead.

When the issue cannot be reproduced, report the exact attempts and missing environmental evidence. Do not present a speculative edit as a verified fix.

## Fix completion gate

After identifying the cause, add or explicitly define a focused regression test at the layer that owns the defect before claiming the fix is verified. For permission or lifecycle failures, cover the failing transition and the nearest denial, cancellation, disposal, or repeated-resume path. Static analysis and one successful manual rerun are insufficient on their own.

Then repeat the original runtime flow under equivalent platform, permission, lifecycle, and startup conditions. Report the regression test and runtime evidence separately; if repository or device access blocks either one, state that the fix remains unverified at that boundary.
