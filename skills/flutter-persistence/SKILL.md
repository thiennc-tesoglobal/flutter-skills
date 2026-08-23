---
name: flutter-persistence
description: Design or review Flutter local persistence, caching, offline behavior, schema evolution, and secure-data boundaries. Use for preferences, files, SQLite, or an existing database package; route remote transport to flutter-networking.
---

# Flutter Persistence

Choose storage from data shape, query needs, durability, sensitivity, synchronization, and migration requirements.

## Select proportionately

- Use preferences only for small settings, not relational or critical domain data.
- Use files for document/blob ownership with explicit atomicity and cleanup.
- Use a database when queries, relationships, transactions, indexing, or migration justify it.
- Use platform secure storage for small secrets; do not treat ordinary app databases as secret vaults.
- Preserve an established package unless it cannot satisfy a concrete requirement.

## Model ownership

Define the source of truth, cache freshness, write ordering, conflict behavior, offline mutations, deletion semantics, and recovery from corrupt or incompatible data. Keep storage models behind repositories so schema details do not leak into widgets.

## Load references conditionally

- Read [caching policy](references/caching-policy.md) when choosing cache keys, freshness, invalidation, eviction, stale disclosure, or user isolation.
- Read [offline synchronization](references/offline-sync.md) when local and remote data can diverge, mutations queue offline, background work runs, or conflicts and deletions must reconcile.

Route HTTP validators and transport caching to `flutter-networking`, and image, widget, scroll, or memory-cache performance to `flutter-performance`.

## Migration and safety

Version schemas and test upgrades from realistic prior versions. Never destroy user data as an automatic response to a migration failure unless the product explicitly permits it. Avoid storing access tokens, passwords, or sensitive personal data in logs or plain preferences.

## Verification

Test first run, reopen, upgrade, failed write, concurrent access, corrupted data, deletion, and offline/online transitions relevant to the feature. Use temporary databases or directories for deterministic tests.

## Sources

- [Flutter persistence cookbook](https://docs.flutter.dev/cookbook/persistence)
- [Flutter offline-first support](https://docs.flutter.dev/app-architecture/design-patterns/offline-first)
