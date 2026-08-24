# GraphQL clients

Use this reference when the request involves GraphQL queries, mutations, subscriptions, schema-derived code, normalized caching, or optimistic updates.

## Preserve the contract

Inspect the current client, schema source, generated types, fragments, scalar mappings, cache, fetch policies, links or exchanges, subscription protocol, and generation commands before editing. Preserve `graphql_flutter`, Ferry, another established client, or a thin in-house transport when it already satisfies the product contract. Do not introduce a second cache or generation pipeline for one feature.

Treat the GraphQL document and variables as wire input. Keep named operations and reusable fragments close to the feature or the repository's established operation boundary, then map generated or wire models to domain models explicitly. Regenerate only affected outputs and keep generation deterministic in CI.

The GraphQL specification defines execution semantics but not one universal network transport. Queries and mutations commonly use HTTP; subscriptions produce response streams whose wire protocol must be agreed with the server. Verify endpoint, media type, authentication, persisted-operation, upload, batching, and subscription protocol support against the actual backend and client version.

## Model results and failures

A successful transport does not imply a fully successful GraphQL operation. Model at least these outcomes where the product distinguishes them:

- Transport or intermediary failure with no GraphQL response.
- Request failure such as parse, validation, operation-selection, or variable-coercion failure with errors and no data.
- Execution failure with partial data plus field errors.
- Complete data with no execution errors.
- Authentication or authorization failure represented by HTTP, GraphQL errors, or both according to the server contract.

Do not discard usable partial data automatically or silently present it as complete. Map error paths and stable extension codes only after validating their shape; treat messages and arbitrary extensions as untrusted diagnostics, not durable domain identifiers.

The GraphQL-over-HTTP specification remains a working draft. Inspect the deployed server and client before enforcing draft media types or status-code behavior, and keep GraphQL response parsing separate from generic HTTP status mapping.

## Cache, pagination, and mutations

- Define normalized entity identity per schema type. Test missing IDs, composite keys, interface or union results, and account or tenant changes.
- Make fetch and cache policies explicit for first load, refresh, background refresh, and offline reads. Do not label cached data fresh without policy evidence.
- For cursor or connection pagination, define query identity, variables included in the cache key, edge ordering, duplicate-node handling, page-info merge, refresh replacement, and terminal conditions.
- Use optimistic writes only when the UI can identify the affected entities and roll back or reconcile with the authoritative result. Prevent an older mutation response from overwriting a newer state.
- Retry mutations only with operation-level idempotency or a product-safe recovery contract. A GraphQL mutation sent through HTTP is not safe merely because the transport is retryable.
- Route durable normalized caches, queued offline mutations, conflict resolution, and account-scoped persistence to `flutter-persistence`.

## Subscriptions

Use the realtime transport reference for connection ownership, reconnect, liveness, and event delivery. Additionally define:

- The exact client-server subscription protocol and initialization payload.
- Token refresh and whether reconnect requires reinitialization and resubscription.
- Stable subscription identity and teardown ownership.
- Event IDs, sequence or revision semantics, duplicate handling, gap detection, and snapshot reconciliation.
- Whether authorization or variables can change while a subscription is active.

Do not assume reconnect resumes missed events. If the protocol provides no resume cursor, refetch an authoritative snapshot or accept and communicate the product's consistency boundary.

## Verification

Use a fake GraphQL transport or test server to cover complete data, partial data with errors, request errors without data, malformed payloads, auth refresh coordination, cursor merges, normalized identity collisions, optimistic rollback, and stale mutation completion. For subscriptions, also test initialization rejection, token expiry, duplicate events, gaps, reconnect, resubscribe, and disposal.

## Sources

- [GraphQL September 2025 specification](https://spec.graphql.org/September2025/)
- [GraphQL over HTTP working draft](https://graphql.github.io/graphql-over-http/draft/)
