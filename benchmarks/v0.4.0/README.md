# v0.4.0 focused evaluations

These raw results cover focused behavior and routing boundaries for skills added in v0.4.0. They are change evidence, not a catalog benchmark.

## Flutter WebView

- [`flutter-webview-behavior.json`](flutter-webview-behavior.json): the JavaScript bridge and authorization case passed at 100 with the skill instructions.
- [`flutter-webview-routing-initial.json`](flutter-webview-routing-initial.json): OAuth routing passed, but the embedded-content prompt selected `flutter-package-development` unexpectedly because “existing Flutter WebView package” was ambiguous.
- [`flutter-webview-routing.json`](flutter-webview-routing.json): after clarifying that the app consumes an existing dependency and does not change or distribute the plugin, both WebView and OAuth routing cases passed.

The initial failed result is retained so the routing-case correction remains auditable.

## Flutter OpenAPI client

- [`flutter-openapi-client-behavior-initial.json`](flutter-openapi-client-behavior-initial.json): safe Swagger UI discovery scored 55 because the response did not explicitly report unsupported executable initialization syntax or define the acquisition boundary.
- [`flutter-openapi-client-behavior.json`](flutter-openapi-client-behavior.json): after requiring a discovery ledger for fetched, inaccessible, excluded, and unsupported resources, the same case passed at 96.
- [`flutter-openapi-client-routing.json`](flutter-openapi-client-routing.json): OpenAPI generation, ordinary Dio retry, and reusable SDK routing all passed (3/3).
- [`flutter-openapi-client-ref-security-initial.json`](flutter-openapi-client-ref-security-initial.json): malicious external-reference acquisition scored 45 because the response did not cover every redirect/reference hop, all inherited sensitive material, or bounded traversal.
- [`flutter-openapi-client-ref-security.json`](flutter-openapi-client-ref-security.json): after adding explicit network, filesystem, credential-origin, redirect, and traversal boundaries, the same security behavior passed at 100.

The initial behavior failures are retained so each instruction change remains tied to measured evidence.
