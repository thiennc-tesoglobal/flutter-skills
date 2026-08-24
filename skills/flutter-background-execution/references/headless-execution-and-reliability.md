# Headless execution and reliability

## Separate execution models

A helper isolate spawned by a running Flutter engine is not the same as an OS-launched headless engine or callback after process recreation.

- For a helper isolate, pass transferable values and use `RootIsolateToken` plus `BackgroundIsolateBinaryMessenger.ensureInitialized` only when platform-plugin access from that isolate is supported and required.
- For an OS-launched callback or headless engine, follow the selected plugin's current callback-dispatcher and plugin-registration contract. Do not rely on a token, singleton, dependency container, or in-memory state from a previous process.
- When AOT reachability requires it, keep the registered dispatcher or callback top-level/static and preserve the package-documented entry-point annotation.

Initialize only the dependencies the job needs. Avoid UI bindings, navigation, widget-owned state, and assumptions that `main()` has run normally. Re-open storage and transports safely, use a background-safe authentication path, and close handles before reporting completion.

## Delivery semantics

Assume at-least-once execution unless the platform and backend prove otherwise. Give each logical operation a durable identity, make side effects idempotent, and store a small state machine such as queued, running lease, succeeded, retryable failure, or terminal failure. Recover expired leases after interruption.

Bound retries by attempt, age, and business relevance. Add jitter where many devices could retry together. Preserve causal error detail without logging tokens, payload secrets, or sensitive records. Reconcile foreground state from durable data when the app resumes rather than trying to push directly into disposed UI state.

## Verification

Test the pure job handler with fake time, transport, and storage. Cover duplicate invocation, process interruption after the remote side effect but before local commit, credential expiry, cancellation, malformed old payloads, retry exhaustion, and sign-out invalidation. Native tests should prove callback registration and plugin availability in the actual headless path.

## Sources

- [Flutter background processes](https://docs.flutter.dev/packages-and-plugins/background-processes)
- [Using platform plugins in isolates](https://docs.flutter.dev/perf/isolates#using-platform-plugins-in-isolates)
- [Dart isolates](https://dart.dev/language/isolates)
