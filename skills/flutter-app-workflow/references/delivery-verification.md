# Delivery verification

Choose checks proportionate to the change:

```sh
dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test
```

For user-visible behavior, also run the intended target and verify the changed flow. Add integration or golden tests only when they provide durable value. Use profile mode and recorded evidence for performance claims.

Describe evidence on two independent axes:

- Execution surface: static inspection, unit test, widget test, host integration test, emulator, simulator, browser, desktop, or physical device.
- Data source: fixture, fake or mock transport, local test server, development service, staging service, or production service.

For live calls, record the environment, operation, status, relevant redacted response shape, and time or build when it affects reproducibility. Running on a simulator does not prove a real backend was used; calling a staging server does not prove physical-device behavior.

## Git handoff

Before committing, inspect the working tree, stage explicit intended paths, then review the staged diff and staged file list. Keep unrelated user changes, disposable test probes, generated caches, credentials, and locally installed skill or plugin directories out of an application repository unless they are the requested deliverable.

Use an atomic conventional commit and include the supplied ticket URL or repository-qualified issue reference in the commit body. Use an automatic closing keyword only when the change fully resolves that ticket and the target branch supports it. Do not push, open a pull request, or otherwise publish the branch until the user explicitly requests that remote action.

Final reporting should state:

- what changed and why;
- which architecture and package choices were preserved;
- exact checks run and their results;
- execution surface and data source actually verified;
- any remaining limitation or external blocker.

## Sources

- [GitHub: Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
