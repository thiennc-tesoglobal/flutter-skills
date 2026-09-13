# Schema migrations and recovery

A migration changes a durable data contract. Preserve the existing storage package and prove what happens to every supported installed version before changing production data.

## Establish the contract

Inspect `pubspec.yaml`, the lockfile, SDK constraints, the resolved database package and version, generated schema or adapters, migration callbacks, and publisher documentation. Determine whether the package wraps its migration callback in a transaction and whether nested transactions or schema changes have special constraints.

Inventory:

- Current and target schema or format versions.
- Every version that a supported production installation may still contain.
- Durable user-authored records, queued operations, identifiers, relationships, serialized payloads, indexes, triggers, and constraints.
- Disposable caches and reproducible derived data that have an explicitly safe rebuild source.
- Writers, readers, background workers, or isolates that must remain stopped until migration completes.

Do not infer package APIs from a different database library or its latest documentation. Use the resolved package's supported migration and transaction boundary.

## Plan every transition

Define an ordered transition for every supported starting version. An app can skip releases, so opening version 3 directly with version 5 code must execute the required `3 -> 4 -> 5` work or an equally verified direct transition.

For each step:

1. Add compatible intermediate structure.
2. Backfill or transform data with explicit rules for null, malformed, ambiguous, legacy, and account-owned values.
3. Validate the transformed rows and relationships.
4. Add final non-null, uniqueness, foreign-key, or other constraints only after the data satisfies them.
5. Recreate required indexes, triggers, views, and serialized or outbox compatibility.
6. Advance the application schema version only through the package's successful migration contract.

Handle an unsupported newer schema or downgrade explicitly. Do not open it as an older known schema, silently coerce it, or recreate it.

## Make failure recoverable

Use the established package's documented atomic migration or transaction mechanism. For SQLite-backed stores, group related schema and data changes so failure rolls them back together; do not add a nested transaction when the package already owns one.

On failure, keep the prior database and version recoverable, stop code that expects the new schema, and surface an explicit retry, support, restore, or export path appropriate to the product. Never catch a migration error and delete durable storage merely to make startup succeed. A destructive reset requires an explicit product decision and authorization after the affected data has been classified.

Keep synchronization and background writers paused during migration. Preserve outbox operation identity, ordering, retry metadata, and payload compatibility; migration must not send, acknowledge, duplicate, or drop pending operations.

## Verify released states

Create fixtures with the previously released schema definitions or binaries, or retain reviewed database snapshots produced by those versions. Rebuilding an approximation of the old schema using only the new migration code does not prove compatibility.

For every supported starting version, test:

- Direct upgrade to the target plus fresh creation at the target.
- Exact target schema version after success and no repeated work after close and reopen.
- Preserved identifiers, values, row counts where meaningful, relationships, user or tenant ownership, and pending operations.
- Final nullability, uniqueness, foreign keys, indexes, triggers, and application reads and writes.
- Injected failure during each destructive or transformative phase, followed by close and reopen; assert the prior version and data remain recoverable, then verify the documented retry or recovery path.
- Empty, large, malformed, ambiguous, and historically nullable values relevant to the changed columns.
- Concurrent startup, background-worker, insufficient-storage, corruption, and process-interruption behavior when those risks are reachable and the harness can reproduce them.

Report which prior versions, package version, platforms, fixtures, failure points, and invariants were actually exercised. Do not claim device or crash-safety evidence from an in-memory database alone.

## Sources

- [Flutter persistence cookbook](https://docs.flutter.dev/cookbook/persistence)
- [Flutter persistent storage architecture: SQL](https://docs.flutter.dev/app-architecture/design-patterns/sql)
- [SQLite is transactional](https://www.sqlite.org/transactional.html)
- [SQLite application-defined user version](https://www.sqlite.org/pragma.html#pragma_user_version)
