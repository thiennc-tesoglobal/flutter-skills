# Store testing and release

Use this reference to prove store behavior without mutating production configuration unexpectedly.

## Test matrix

Inspect the repository's flavors, bundle or application identifiers, signing setup, product identifiers, and backend environments. Ensure the test build points to the matching sandbox or test product catalog; do not silently reuse production accounts, endpoints, or products.

When repository or console access is unavailable, make that inspection an explicit prerequisite and keep readiness unverified. Do not replace inspection with a request to create fresh products, credentials, signing, or uploads.

Define each important test as a reproducible case with preconditions, store and application account, starting transaction and entitlement state, actions including the interruption point, expected store state, expected entitlement state, required acknowledgement or finish result, and observable pass/fail evidence. A feature checklist without these outcomes is not a deterministic sandbox plan.

Exercise on each affected platform:

- product lookup, localized display, unavailable and mismatched identifiers;
- purchase success, user cancellation, store failure, network interruption, and duplicate tap prevention;
- pending completion while the app is backgrounded or stopped;
- verification failure and backend unavailability;
- delivery followed by interrupted acknowledgement or finish, then recovery;
- restore, reinstall, account switch, multiple devices, and subscription state changes.

Use deterministic fakes for exhaustive ordering and failure cases, then a real store sandbox or test track for the native purchase surface and server notifications. Mock success does not prove store configuration, signing, or backend receipt handling.

## External mutations

Creating or editing store products, subscription groups, offers, prices, tax or banking configuration, tester accounts, credentials, signing, uploads, review submissions, or production releases requires explicit authorization. Resolve the exact application, environment, product identifier, and intended change before acting.

Report which configuration was inspected, which sandbox transactions were observed, which server notifications or verification results were confirmed, and what remains console-, credential-, review-, or time-dependent.
