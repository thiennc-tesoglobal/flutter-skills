# Logging, tracing, and privacy

Use this reference for operational event design and correlation.

## Signal design

Prefer structured events with stable names and bounded attributes over prose assembled from arbitrary objects. Define severity and ownership so alerts map to action. Add breadcrumbs only around state transitions useful for diagnosis; high-volume UI gestures usually add cost and noise.

Trace user-important asynchronous paths at meaningful boundaries such as repository request, local lookup, parsing, and rendering handoff. Propagate an existing correlation or trace identifier through owned layers without coupling domain models to a vendor. Do not create a span for every function.

Use `dart:developer` logging or timeline APIs for local tooling when they fit; a production backend still needs an explicit adapter. Keep the telemetry interface small enough to fake in tests and to disable safely.

## Privacy and cost

Classify attributes before capture. Default-deny raw request/response bodies, headers, tokens, passwords, payment values, health data, message contents, precise location, and arbitrary `toString()` output. Redact at the earliest shared boundary and test the redactor.

Honor the application's consent and deletion model. Distinguish crash/operational collection from product analytics where policy or platform disclosures do. Configure retention, environment separation, access, and sampling in the actual backend rather than promising them only in client code.

Sample high-volume success traces intentionally, but preserve enough error and latency tail data to diagnose incidents. Bound offline buffers by age and size; telemetry must not crowd out product data or block a user flow.

## Useful invariants

- One logical failure produces one primary error event.
- Release, environment, and platform fields are present and trustworthy.
- Correlation identifiers help join owned spans without identifying a person.
- Telemetry failure is non-fatal and does not recurse through its own logger.
- Debug logs and production collection can be controlled independently.

## Sources

- [Dart developer log](https://api.dart.dev/dart-developer/log.html)
- [Dart Timeline](https://api.dart.dev/dart-developer/Timeline-class.html)

