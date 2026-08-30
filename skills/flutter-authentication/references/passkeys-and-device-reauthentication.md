# Passkeys and device re-authentication

Use this reference when authentication uses public-key credentials or a device-local biometric or credential prompt.

## Passkeys

A passkey ceremony spans the relying-party server and the platform credential API. The server creates a fresh challenge and verifies the returned origin or relying-party identity, challenge, credential, signature, user binding, and replay protections. The Flutter client transports options and results but does not declare success independently.

Configure relying-party identifiers, Android asset associations, Apple associated domains, application identifiers, and provider capabilities consistently. Handle no credential, user cancellation, interrupted ceremony, multiple accounts, credential replacement, synced credentials, process death, and unsupported platforms.

Do not invent a passkey fallback that weakens account recovery. Preserve the product's verified recovery, enrollment, and account-linking policy.

## Device-local re-authentication

Biometric or device-credential success proves that the platform accepted a local authentication policy; it does not identify a remote account, refresh a server session, or authorize a backend action by itself. Use it to release a locally protected key or gate a narrowly defined local action when the threat model supports that design.

Choose biometric-only versus device-credential fallback deliberately. Handle cancellation, lockout, enrollment changes, backgrounding, repeated prompts, unsupported hardware, and platform error mapping. Never treat a biometric boolean stored in application preferences as durable authentication evidence.

Verify passkeys against an authorized non-production relying party and local re-authentication on real supported devices. Simulator success alone may not prove hardware, enrollment, association, or recovery behavior.
