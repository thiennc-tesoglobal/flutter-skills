# JavaScript bridges and permissions

## Minimize the bridge

Keep JavaScript disabled for static content. When required, expose a small versioned message contract rather than a general command executor. Parse bounded JSON into typed variants, reject unknown fields and oversized payloads, validate origin and current top-level navigation state where the platform exposes sufficient evidence, and authorize every native action in Dart or on the trusted backend.

Assume hostile or compromised page content can call every exposed channel. A random channel name, hidden button, secret in shipped Dart code, or successful navigation is not an authorization control. Never expose raw filesystem, arbitrary URL loading, token reads, unrestricted platform channels, dynamic code, or direct entitlement and identity mutation.

Use correlation identifiers and one-shot consumption for completion messages that can be retried or replayed. Drop callbacks from an old controller, page generation, account, or disposed screen. Return bounded errors rather than sensitive stack traces or credentials.

## Permissions and web UI

Map each page permission request to the active trusted origin, a user-visible product action, the platform permission state, and the least capability required. Denial and cancellation must remain recoverable. Do not automatically grant camera, microphone, location, clipboard, media capture, notifications, or persistent storage because the page requested them.

Handle JavaScript dialogs, fullscreen media, and new windows explicitly when needed. Avoid logging page payloads, tokens, form values, or personal data. Disable WebView debugging in release builds unless an authorized diagnostic requirement says otherwise.

## Verification

Test valid messages, malformed JSON, unknown types, oversized input, duplicate and replayed IDs, nested-frame attempts where relevant, navigation to an untrusted origin while a channel exists, delayed callbacks after disposal, and permission allow, deny, cancel, and permanently-denied paths. Device evidence is required for the actual platform bridge and permission prompts.

## Sources

- [Android WebView native bridge risks](https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges)
- [webview_flutter JavaScriptMessage](https://pub.dev/documentation/webview_flutter/latest/webview_flutter/JavaScriptMessage-class.html)
- [webview_flutter PlatformWebViewPermissionRequest](https://pub.dev/documentation/webview_flutter/latest/webview_flutter/PlatformWebViewPermissionRequest-class.html)
