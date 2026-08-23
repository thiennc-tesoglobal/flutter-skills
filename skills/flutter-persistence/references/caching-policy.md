# Caching policy

A cache is a correctness contract with bounded staleness and storage, not just a faster copy.

## Define the contract

For each cached value, record:

- Canonical source of truth and ownership.
- Stable cache key, namespace, schema version, and user or tenant scope.
- Freshness rule, expiry behavior, and whether stale data may be shown.
- Refresh trigger, invalidation events, and failure fallback.
- Size or entry budget, eviction policy, and cleanup lifecycle.
- Sensitivity, backup behavior, encryption requirement, and logout/account-removal behavior.

Do not infer freshness solely from connectivity. A connected device may not reach the service, and a disconnected device may still have valid cached data.

## Choose a read strategy

- Cache-first: return a valid cache immediately and refresh according to policy.
- Network-first: prefer authoritative remote data and fall back to an acceptable cache on failure.
- Stale-while-revalidate: disclose or model stale state, return cached data, refresh, then update observers.
- Local-only source of truth: read from local storage while a separate synchronization process updates it.

Choose per use case. Pricing, permissions, medical data, and payment state may require different staleness rules from avatars or reference lists.

## Keys, invalidation, and versioning

Include every input that changes the result in the key: identity, locale, query, filters, pagination cursor, feature variant, or authorization scope as applicable. Prevent cross-account and cross-environment collisions.

Prefer explicit invalidation on successful mutation, logout, account switch, schema change, and product-defined events. Time-based expiry is a fallback, not a substitute for known invalidation events.

Version serialized entries and handle incompatible or corrupt values deterministically. Do not erase durable user-owned data merely because a disposable cache is corrupt; keep those lifecycles separate.

## Eviction and memory

Bound caches by entries, bytes, age, or a product-specific budget. Ensure in-memory and on-disk layers do not multiply an already large payload without need. Close files and databases, cancel warmups, and avoid retaining widget or context ownership in data caches.

Route image decoding, Flutter `ImageCache`, scroll prefetch, and render-object concerns to `flutter-performance`.

## Verification

Test hit, miss, expiry, stale fallback, invalidation after mutation, refresh failure, corrupt entry, schema change, capacity eviction, logout, account switch, and concurrent readers/writers relevant to the feature. Use deterministic clocks and temporary storage.
