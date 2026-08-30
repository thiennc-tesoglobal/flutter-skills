# OAuth, OIDC, and redirects

Use this reference for federated browser sign-in and application callback handling.

## Public-client flow

Flutter mobile, desktop, and web artifacts distributed to users cannot protect a reusable client secret. Do not embed one in Dart, assets, environment files, manifests, desktop bundles, JavaScript, or obfuscated releases.

For native apps, prefer the system browser or provider-supported external authorization agent with authorization code and PKCE. Do not use an embedded WebView for general OAuth authorization or fall back to the implicit flow merely to simplify redirects. Generate a fresh high-entropy verifier and state for each attempt, keep them scoped to that attempt, and reject unsolicited, mismatched, expired, or replayed responses.

For OIDC, validate issuer, audience, signature, expiry, nonce, and other provider-required claims at the trusted boundary. Decoding a JWT is not verification. Preserve the established backend-for-frontend or direct public-client architecture when it meets the provider contract.

## Redirect ownership

Prefer claimed HTTPS links where supported and configure Android Digital Asset Links or Apple associated domains correctly. If a private-use scheme is required, namespace it according to the provider guidance and still rely on PKCE and state because another application may attempt interception.

Separate callback parsing from navigation. Accept only the registered scheme, host, path, parameters, and owning pending authorization attempt. Handle user cancellation, provider denial, missing parameters, process death, duplicate delivery, warm links, and callback arrival when the initiating screen no longer exists.

Do not log authorization codes, tokens, verifier values, state, nonce, or provider error payloads containing user data. Preserve enough redacted context to diagnose the stage and outcome.

## External configuration

Creating identity-provider clients, adding redirect URIs, changing consent screens, rotating secrets, or enabling production connections changes external security state and requires explicit authorization. Resolve the exact provider, application, environment, client type, and redirect before acting.
