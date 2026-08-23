# Widget previews

Use Flutter Widget Previewer for fast, isolated visual iteration when the project's Flutter SDK supports the required APIs. It complements tests and device verification; it does not replace them.

## Preflight

Read the project's Flutter SDK constraint and the documentation matching that SDK. The preview API and stability have evolved; do not add `package:flutter/widget_previews.dart`, `@Preview`, or preview commands to a project whose SDK does not support them.

Inspect existing preview conventions, theme wrappers, localization, inherited dependencies, assets, fixtures, and generated files. Reuse shared deterministic wrappers rather than creating a second app shell.

## Preview targets

Prefer a top-level function, supported static method, or eligible public widget constructor/factory that returns a `Widget` or `WidgetBuilder`. Keep fixtures deterministic and free from production network calls, clocks, random values, credentials, and mutable global state.

Use preview names and groups that describe the component and state. Add only meaningful configurations such as:

- Typical, long, empty, loading, error, disabled, and selected content.
- Light and dark themes.
- Compact and wide constraints.
- Enlarged text and representative locales or text directions.

Use wrappers for theme, localization, and lightweight inherited dependencies. Avoid reproducing the entire production dependency graph merely to make a component previewable; improve the component boundary when practical.

## Limitations

The previewer runs in a web-based environment. Native plugins and invoked `dart:io` or `dart:ffi` APIs are unsupported. Isolate those dependencies behind fakes or preview-safe boundaries, and retain device tests for real platform behavior.

Use package-aware asset paths and explicit constraints where required by the current previewer. Do not commit generated preview caches.

## Verification

Start the previewer with the command supported by the project's SDK and confirm every added preview renders without exceptions. Then keep widget, golden, accessibility, and device tests for behavior and platform fidelity. A rendered preview is not regression evidence by itself.
