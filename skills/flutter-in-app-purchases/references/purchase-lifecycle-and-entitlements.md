# Purchase lifecycle and entitlements

Use this reference for transaction processing and the boundary between the store, application, backend, and delivered capability.

## Listener and reconciliation ownership

Create one clearly owned purchase-update subscription early enough to receive updates after launch and resume. Dispose it according to the package lifecycle without creating duplicate listeners. Re-query or reconcile current purchases when the store contract requires it because transactions may complete while the application is stopped, on another device, or outside the current flow.

Do not associate a transaction only with the screen or button that initiated it. Persist or recover enough non-sensitive correlation to attribute a returned transaction safely, and handle updates when no purchase screen exists.

## Processing sequence

For each transaction identity:

1. Normalize product, store, transaction identity, account context, state, and verification material.
2. Reject or defer pending, cancelled, failed, malformed, mismatched, or unverified results.
3. Verify with the established trusted store or backend boundary.
4. Grant or update the entitlement idempotently.
5. Record delivery durably enough to recover from interruption.
6. Acknowledge, consume, or finish the transaction according to product type and store contract.

Make retries safe at every step. Duplicate callbacks, backend notifications, restores, and app restarts must not deliver a consumable twice or create contradictory entitlement state. Do not acknowledge or finish before the application can recover proof of delivery.

## Account and trust boundary

A purchase token, receipt, or signed transaction is sensitive evidence, not an application secret and not an entitlement by itself. Avoid logging or exposing it unnecessarily. Bind verified purchases to the correct authenticated account using the existing backend design where cross-device access or fraud resistance requires it.

If the user changes account during a transaction, stop automatic attribution until the owning account can be determined safely. Never carry cached premium state from one account to another.

## Product types

- Consumable: delivery must be exactly-once from the product perspective before consumption permits repurchase.
- Non-consumable: reconciliation should recover the durable entitlement without duplicate side effects.
- Subscription: entitlement follows verified effective state and access period, not a one-time success callback.

Keep product identifiers and entitlement names centrally mapped and environment-aware. Missing, duplicated, or unknown products should fail visibly without inventing price or access state.
