# Platform attack surfaces

Inspect only the target platforms and capabilities in scope.

## Deep links and intents

Treat every incoming URI, route argument, Android intent, iOS URL context, and shared file as untrusted input. Validate scheme, host, path, parameter types, authorization state, and the transition being requested.

Prefer verified Android App Links and Apple Universal Links for trusted web-to-app associations. A valid association does not authorize the user or make route parameters trustworthy. Prevent open redirects, privileged actions from links, path traversal, and unsafe forwarding to WebViews or external applications.

## WebViews and native bridges

Load the narrowest set of trusted origins and content. Disable JavaScript or bridge features that are unnecessary. Validate both scheme and host before navigation and open unrelated external content outside the privileged WebView.

Keep bridge APIs minimal, authenticate sensitive operations independently, validate every message, and never expose privileged native behavior to arbitrary page scripts. Review file access, mixed content, certificate-error handlers, downloads, popups, cache, cookies, and storage lifecycle.

## Platform channels and plugins

Treat channel messages, plugin callbacks, method names, and serialized values as boundary input. Validate shapes and ranges on both sides, restrict exported native entry points, and map errors without exposing secrets or internals.

Review plugin platform code and transitive permissions rather than assuming a Dart API fully describes its attack surface. Preserve explicit unsupported-platform behavior.

## Permissions and exported components

Request the minimum permission at the moment its user-visible feature requires it. Handle denial, restriction, revocation, and partial access without pressuring the user or weakening controls.

Inspect Android exported activities, services, receivers, providers, intent filters, file providers, backup rules, and network security configuration. Inspect Apple entitlements, URL schemes, associated domains, keychain access groups, app groups, background modes, and transport exceptions.

## User-visible exposure

Check notifications, recent-app snapshots, media projection, screenshots, clipboard, autofill, keyboard suggestions, share sheets, accessibility output, and external displays for sensitive flows. Use supported platform protections only where exposure would cause concrete harm; do not blanket-disable useful system behavior without product agreement.

## Embedded and shared data

Scope shared files, app groups, content providers, temporary exports, and home-screen widget data to the least privilege and shortest useful lifetime. Do not place credentials or unrestricted sensitive payloads in broadly readable shared containers.
