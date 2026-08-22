---
name: flutter-networking
description: Build or review Flutter networking with the project's HTTP client, serialization, authentication, pagination, retries, cancellation, caching, and error mapping. Use for remote APIs and transport behavior; route local storage ownership to flutter-persistence.
---

# Flutter Networking

Keep transport concerns at the service boundary and expose domain-meaningful results to the rest of the app.

## Inspect

Read current client, generated API code, interceptors, model generation, authentication, environment configuration, and tests. Preserve `http`, Dio, generated clients, or another established choice when it meets the requirement.

## Rules

- Centralize base URLs, headers, timeouts, and environment selection without committing secrets.
- Decode untrusted responses defensively and distinguish transport, protocol, decoding, authentication, and domain failures.
- Map wire models to domain models at an explicit boundary.
- Retry only transient, safe, or idempotent operations with bounded backoff and cancellation.
- Refresh credentials through one coordinated path to avoid request storms.
- Define pagination identity, ordering, duplicate handling, terminal conditions, and refresh behavior.
- Apply cache policy deliberately; do not silently return stale data as fresh.
- Avoid logging tokens, personal data, or full sensitive payloads.

## Verification

Use deterministic fake servers or mock transports to cover success, malformed data, timeouts, cancellation, unauthorized refresh, retry exhaustion, pagination boundaries, and offline behavior. Run integration tests against a real service only when credentials and environment are explicitly in scope.

## Sources

- [Flutter networking](https://docs.flutter.dev/data-and-backend/networking)
- [JSON serialization](https://docs.flutter.dev/data-and-backend/serialization/json)
