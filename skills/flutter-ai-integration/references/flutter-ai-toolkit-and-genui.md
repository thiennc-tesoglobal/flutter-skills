# Flutter AI Toolkit and GenUI

Use this reference only when the project already uses these packages or their capabilities justify evaluating them against the existing architecture.

## AI Toolkit

Flutter AI Toolkit provides chat-oriented UI capabilities such as streaming responses, rich text, voice input, attachments, function calls, response widgets, and conversation persistence. Treat it as a presentation and interaction option, not as authority to replace the project's service, state, networking, or persistence boundaries.

Before adopting it, inspect current Flutter SDK constraints, provider adapters, supported platforms, accessibility, theming, customization needs, and testability. Keep provider credentials behind the service boundary; the widget layer should not own a reusable secret.

Test loading, streaming, cancellation, errors, keyboard and focus behavior, large text, screen readers, long conversations, attachment failures, and restoration on each supported target.

## GenUI

Flutter's GenUI capability is experimental. Do not make it a production default or rewrite a stable UI around it merely because the feature involves AI. Use it only when generative UI is an explicit product requirement and the user accepts its maturity and compatibility constraints.

Constrain generative output to a reviewed component catalog and validated data contracts. Keep actions behind the same authorization and confirmation boundaries as ordinary tool calls. Provide deterministic loading, unsupported, invalid-output, and fallback experiences, and verify accessibility and layout across target form factors.
