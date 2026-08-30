# Verification and experiments

Use this reference to prove events and exposure semantics beyond a successful client method call.

## Layered verification

1. Unit-test event producers and provider mapping with a fake adapter.
2. Exercise the semantic user flow in an authorized development or staging build.
3. Observe the event in the provider's debug surface or ingestion endpoint.
4. Verify name, properties, identity, timestamp, consent, environment, and count.
5. Confirm the intended dashboard, funnel, export, experiment, or downstream query when it is part of the change.

Test retries, offline delivery, app restart, backgrounding, rapid taps, navigation reconstruction, account switch, and consent transitions for duplicate or misattributed events. Do not send test data into production unless explicitly authorized and safely identifiable.

## Experiments

Separate assignment, configuration fetch, exposure, and outcome. Emit exposure only when the user or session actually receives the variant according to the experiment definition, not on every rebuild, config refresh, or outcome. Give an exposure a stable experiment, variant, subject, and assignment identity without leaking personal data.

Prevent the same exposure from firing repeatedly during one defined exposure window. Preserve assignment across the required lifecycle and define behavior for anonymous-to-authenticated transitions. Outcomes must not choose or modify assignment retroactively.

## External mutations

Creating projects, data streams, dashboards, audiences, experiments, retention rules, exports, credentials, or production collection changes external state and requires explicit authorization. Resolve the exact vendor, project, environment, property, and expected change first.
