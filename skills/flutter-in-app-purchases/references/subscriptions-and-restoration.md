# Subscriptions and restoration

Use this reference when access changes over time or purchases must be recovered across reinstall, device, or account transitions.

## Subscription state

Model the states the selected stores and backend actually expose, including active access, cancelled-but-still-entitled periods, grace periods, billing hold, pause where supported, expiration, revocation, refund, upgrade, downgrade, and pending replacement. Do not equate cancellation with immediate loss of access or a locally elapsed date with authoritative expiration.

Define which system is authoritative and how the client represents stale or unavailable status. Reconcile on launch, resume, sign-in, account change, successful transaction, backend notification, and manual refresh where appropriate without creating request storms.

Product or offer changes must preserve store-specific replacement, proration, eligibility, and effective-date semantics. Do not emulate subscription replacement as two unrelated purchases unless the store contract requires it.

## Restore is reconciliation

Restore or sync actions recover existing transactions and recompute entitlements; they do not initiate a new purchase and must not double-deliver consumables. Provide visible progress and distinguish no purchases, wrong store account, wrong application account, unavailable store, and verification failure.

Automatic reconciliation may be appropriate, but expose the user-facing restore mechanism required by the product and platform. Keep restoration idempotent and safe across repeated taps, process restart, and multiple devices.

## Account changes

On logout or account switch, clear user-scoped cached entitlements and stop presenting the previous account's access. Reconcile the new account deliberately. If the store account and application account disagree, follow the product's documented ownership and transfer policy rather than silently moving an entitlement.

Test cancellation while access remains valid, renewal, grace or hold, expiration, refund or revocation, restore after reinstall, and store/app account mismatch using supported sandbox mechanisms.
