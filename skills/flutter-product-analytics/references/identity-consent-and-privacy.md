# Identity, consent, and privacy

Use this reference when events relate to users, accounts, advertising, sensitive data, or offline delivery.

## Identity lifecycle

Keep anonymous device or installation identity, authenticated account identity, analytics user properties, advertising identifiers, and backend business identifiers distinct. Define if and how anonymous history is linked after sign-in according to the provider and product policy.

On logout or account switch, prevent queued events and user properties from the previous account from being attributed to the next. Reset or rotate provider identity according to the established policy and verify the resulting backend records rather than trusting a local call.

Do not put names, emails, access tokens, purchase tokens, full URLs with query data, search text, messages, or other sensitive content into event names or properties by default. Use bounded business classifications or opaque identifiers only when justified and permitted.

## Consent and collection state

Model consent as an explicit state that covers collection, storage, upload, identity linkage, advertising use, and deletion as required by the product and jurisdictions. Do not initialize or buffer disallowed data before consent if policy prohibits it, and do not assume disabling one SDK flag deletes already collected backend data.

Define what happens to events produced while collection is disabled: drop, aggregate locally without identifiers, or hold only when policy permits. Bound any offline queue by count, age, size, account, environment, and consent state. Purge ineligible queued data on logout, account switch, consent withdrawal, or deletion request as required.

Client controls do not prove backend retention, access, deletion, or data export behavior. Report which controls are implemented in code and which require analytics-console or governance verification.
