# Application security

Use these checks only where the protected assets and trust model make them relevant.

## Secrets and configuration

Assume values shipped in Dart code, assets, native resources, build arguments, environment files, or the compiled binary can be recovered. Obfuscation changes symbol readability; it does not encrypt resources or turn a client into a trusted secret holder.

Classify each value before remediation:

- Public identifier with provider-side origin, app-signature, bundle-ID, quota, or API restrictions.
- User credential or refresh token with an explicit lifecycle.
- Service credential that belongs on a trusted backend and must not ship in the app.
- Signing or encryption key that belongs in controlled build or platform key infrastructure.

If an actual credential is exposed, report likely exposure and the required architectural move. Rotation or revocation changes external state and requires explicit authorization.

## Authentication and authorization

Model login, refresh, logout, expiry, revocation, account switching, device loss, and reauthentication for sensitive actions. Avoid concurrent refresh storms and make token failure terminate or recover the session predictably.

Biometrics and local device authentication can unlock local material or improve user presence checks; they do not replace backend authorization. Never treat a hidden widget, disabled button, route guard, or locally editable role as enforcement for a privileged operation.

## Storage and lifecycle

Minimize local sensitive data first. For material that must remain on-device, choose platform-backed protection and accessibility settings from the threat model, supported platforms, backup behavior, and device-lock requirements. Keep cryptographic keys separate from encrypted payloads.

Review every copy: preferences, databases, files, caches, temporary directories, WebView storage, notifications, screenshots, clipboard, logs, crash reports, analytics, backups, and generated exports. Clear user-scoped material on logout or account removal without deleting unrelated users' recoverable data.

## Network transport

Retain Android network security and Apple App Transport Security defaults. Scope development exceptions to the intended host and build variant; never disable certificate validation globally.

Certificate pinning is not a universal upgrade. Require a threat model, supported host ownership, multiple active pins or another safe rotation plan, observability, expiry handling, and an emergency recovery path before adopting it.

## Cryptography

Use reviewed platform or package-publisher primitives that implement a documented protocol. Define algorithm, mode, nonce generation, key generation, storage, rotation, versioning, and failure behavior as one system. Use cryptographically secure randomness for security material.

Do not design custom cryptography, embed a decryption key beside encrypted data, reuse nonces where the primitive forbids it, or confuse hashing, encryption, signing, encoding, and obfuscation.

## Logging and privacy

Prefer allowlisted structured fields over trying to redact arbitrary payloads after logging. Exclude tokens, passwords, authorization headers, payment data, sensitive identifiers, raw request bodies, clipboard contents, and cryptographic material from logs and analytics.

Align consent, retention, deletion, export, and telemetry behavior with the product's stated privacy requirements. Security review does not invent legal requirements; flag where legal or policy confirmation is needed.
