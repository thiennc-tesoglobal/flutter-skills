# Event contracts and ownership

Use this reference to design analytics that remains meaningful across UI refactors, retries, and provider changes.

## Start from a decision

Write the product question, population, expected behavior, decision owner, and success criterion. Prefer the smallest event set that can answer it. Do not mirror every tap, widget lifecycle, state object, network call, or internal implementation detail into analytics.

Define each event with:

- a stable semantic name and description;
- the exact domain occurrence that owns emission;
- bounded typed properties with units and allowed values;
- identity, consent, and environment requirements;
- expected cardinality and delivery semantics;
- schema version or compatible evolution policy;
- a verification query, debug view, funnel, or downstream consumer.

Use provider-recommended events when their semantics match, but do not force a business event into an inaccurate vendor name. Keep provider mapping behind an adapter and keep vendor types out of domain code.

## Exact semantic ownership

Emit from the layer that knows the domain outcome. A button tap may express intent; a backend or entitlement result may express success. Do not emit the same event from a widget callback, state listener, route observer, and repository.

Use a stable event or operation identity when retries, process restart, queued delivery, backend forwarding, or multiple producers can duplicate an outcome. Decide whether at-most-once, at-least-once with downstream deduplication, or best-effort delivery matches the question. Analytics exact-once is not automatically guaranteed by an SDK call.

Revenue and purchase events must reflect verified purchase outcomes and consistent currency or value units. They must never cause entitlement changes.

## Evolution

Prefer adding compatible optional properties or a new clearly defined event over silently changing semantics. Track deprecated names and dashboard dependencies. Validate property cardinality and length before enabling high-volume collection; do not send free-form user content as an event dimension.
