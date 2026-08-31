# Flutter WebView focused evaluation

These raw results cover the new `flutter-webview` behavior and its highest-risk routing boundary. They are focused change evidence, not a catalog benchmark.

- [`flutter-webview-behavior.json`](flutter-webview-behavior.json): the JavaScript bridge and authorization case passed at 100 with the skill instructions.
- [`flutter-webview-routing-initial.json`](flutter-webview-routing-initial.json): OAuth routing passed, but the embedded-content prompt selected `flutter-package-development` unexpectedly because “existing Flutter WebView package” was ambiguous.
- [`flutter-webview-routing.json`](flutter-webview-routing.json): after clarifying that the app consumes an existing dependency and does not change or distribute the plugin, both WebView and OAuth routing cases passed.

The initial failed result is retained so the routing-case correction remains auditable.
