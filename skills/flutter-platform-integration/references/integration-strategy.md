# Integration strategy

Choose the smallest boundary that fits the native capability, distribution model, performance requirements, and supported platforms.

## Existing package

Prefer an adequate maintained package when its platform coverage, license, API, release history, native dependencies, and lifecycle behavior meet the project. Inspect resolved versions and native implementations; do not add a second package for a capability already present.

## Platform channels and Pigeon

Use a small method or event channel for a narrow stable surface. Use Pigeon or another existing typed contract when multiple methods, structured messages, or evolution benefit from generated compile-time structure.

Define thread/task-queue requirements, serialization limits, cancellation, event subscription, error mapping, engine attachment, activity or view-controller attachment, and background-isolate access. Validate messages on both sides and avoid exposing domain objects as channel transport.

## FFI and native assets

Use `dart:ffi` for C-compatible APIs, generated bindings, or native libraries where direct calls fit. Inspect the project's Flutter and Dart SDK before selecting templates and build APIs.

For SDKs that support the modern workflow, prefer the documented `package_ffi` template and build hooks. Use a standard plugin when the implementation needs Flutter Plugin APIs or OS-language integration; use legacy FFI plugin mechanics only when the requirement or supported SDK demands them.

Define ABI, symbol visibility, memory ownership, allocation and release, strings and buffers, struct layout, callbacks, threading, blocking behavior, exceptions or error codes, architectures, linking, and binary integrity. Never pass Dart-managed pointers beyond their valid lifetime.

## Web interop

Use current `package:web` and `dart:js_interop` patterns supported by the project's SDK. Keep browser-only imports behind platform boundaries and verify Wasm compatibility when it is a target. Validate messages, origins, DOM ownership, cleanup, and unsupported behavior.

## Platform views

Use a platform view only when a native-rendered control is required. Evaluate composition mode, gestures, focus, accessibility, overlays, clipping, transforms, scrolling, keyboard, lifecycle, and performance on every target. A platform view is not a general escape hatch for difficult Flutter layout.

## Verification

Test the Dart adapter with fakes, then exercise each native implementation on its supported target. Verify lifecycle reattachment, multiple engines when applicable, permissions, threading, cancellation, unsupported platforms, release builds, and native resource cleanup.
