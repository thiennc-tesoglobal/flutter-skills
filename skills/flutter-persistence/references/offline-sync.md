# Offline synchronization

Offline-first behavior is a product consistency decision. Define what users may read and write offline, how divergence is surfaced, and which system ultimately decides conflicts.

## Read paths

Choose deliberately among remote-first fallback, local-then-remote streams, and local-only reads with a separate sync process. Model freshness and synchronization state so cached data is not silently presented as current.

Keep the repository as the access point that coordinates local and remote services. Avoid making widgets merge two sources or interpret transport errors as data state.

## Write paths

- Online-only: require server acknowledgement before committing local state when duplication or divergence is unacceptable.
- Optimistic online: update presentation state immediately, retain a rollback or reconciliation path, and persist only according to product policy.
- Offline queue/outbox: atomically persist the domain mutation and a durable operation record before showing it as safely queued.

Do not represent a queue with only a `synchronized` boolean when retries, ordering, multiple edits, partial failure, or deletion matter. Give operations stable identities, type, payload or reference, creation order, attempt metadata, and terminal state.

## Idempotency and ordering

Design remote mutation identifiers and server behavior so retrying after an unknown outcome cannot duplicate payment, creation, or side effects. Define per-entity ordering and whether independent entities may sync concurrently.

Use bounded backoff and distinguish retryable transport failures from authentication, validation, conflict, and permanent server failures. Connectivity signals may trigger an attempt but do not prove internet or service reachability.

## Conflicts and deletion

Choose a conflict policy from domain semantics: server authority, client authority, last-write-wins with a trustworthy version, field merge, user resolution, or rejection and reload. Record server versions or other comparison data explicitly.

Represent offline deletion with a tombstone or durable delete operation until the server acknowledges it. Removing the local row immediately without a durable operation can resurrect data on the next pull.

## Background execution

Mobile operating systems schedule, delay, constrain, or cancel background work. Treat background sync as opportunistic unless a platform contract guarantees otherwise. Make foreground resume, manual retry, process death, battery constraints, and duplicate worker execution safe.

Preserve the project's established background-work package when adequate and verify every supported platform separately.

## Verification

Test process death after local commit, duplicate worker execution, response loss after server success, reordering, authentication expiry, conflict, deletion, account switch, partial batch failure, retry exhaustion, and eventual recovery. Assert both durable state and user-visible synchronization status.
