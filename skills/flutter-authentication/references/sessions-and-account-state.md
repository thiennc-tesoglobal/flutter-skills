# Sessions and account state

Use this reference for token lifecycle, refresh coordination, startup restoration, logout, revocation, and account switching.

## One session owner

Represent authentication with explicit states such as unknown or restoring, unauthenticated, authenticating, authenticated, reauthenticating, refreshing, and terminal failure. Keep one application-owned session coordinator rather than letting screens and interceptors independently refresh or clear credentials.

Store only the credential material the architecture requires. Use platform-backed protection for refresh tokens or similarly sensitive long-lived credentials according to the threat model; ordinary preferences are not a secret vault. Keep access tokens short-lived and in memory where practical. Do not store passwords.

## Coordinated refresh

Coalesce concurrent unauthorized responses into one refresh operation. Queue or fail callers with bounded behavior, update credentials atomically, and prevent a late refresh for account A from authenticating requests after logout or switch to account B. Retry the original request only when its semantics make retry safe.

Distinguish expired access, invalid refresh, revoked session, unavailable network, backend denial, and provider outage. Do not convert every `401` into an infinite refresh loop or treat offline startup as logout automatically when the product permits a limited cached state.

## Logout and account switching

Define local logout, backend session termination, refresh-token revocation, provider logout, and device-wide provider account changes separately. Perform only the actions the product requires and the user authorized.

Clear credentials and user-scoped caches in an order that prevents stale requests, navigation guards, background tasks, purchase entitlements, notifications, and analytics identity from leaking across accounts. Cancel in-flight refresh and ignore late results from the previous session.

Test restart during refresh, simultaneous `401` responses, refresh rotation, revoked refresh, offline launch, logout with requests in flight, account switch, biometric cancellation, and clock skew where relevant.
