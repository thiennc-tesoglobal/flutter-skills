# Streaming, tools, and state

Use this reference for model interaction beyond a single request-response call.

## Streaming state machine

Represent an interaction with explicit states such as idle, submitting, streaming, completed, cancelled, and failed. Keep the user's submitted message separate from partial assistant output. Define whether a partial result remains visible after cancellation or failure.

Assign stable request and conversation identities. Ignore or reconcile late chunks from a cancelled or superseded request, make completion idempotent, and prevent duplicate finalization. Bound buffered text and attachment memory; apply backpressure or batching when rendering every token would create excessive rebuild work.

Retry only when request semantics and provider behavior make it safe. Do not silently resubmit a tool-producing or billable request after an ambiguous failure.

## Conversation and persistence

Separate UI history from the provider context window and from durable product records. Define trimming, summarization, attachment lifetime, model changes, restoration, deletion, and multi-device ownership explicitly. Do not assume sending the complete visible transcript is safe, affordable, or supported.

Use deterministic identifiers and version persisted structures. Route durable database and offline mechanics to `flutter-persistence`.

## Structured output

Decode into a narrow wire representation, validate schema and domain invariants, then map into application models. Handle refusals, missing fields, extra fields, incompatible versions, truncated output, and text returned where structured data was expected. Never use a force cast or regex extraction as the only validation boundary for consequential data.

## Tool calls

Maintain an allowlist mapping tool names to typed argument schemas and application-owned handlers. Validate arguments independently of the model. Enforce authentication, authorization, target scope, idempotency, timeout, and cancellation in the handler.

Return bounded, structured tool results and errors to the model without leaking credentials or unrelated records. Detect repeated calls and cap steps, cost, and elapsed time. Require confirmation immediately before consequential external writes; confirmation cannot be inferred from an earlier broad request.

## Tests

Fake event sequences rather than only final strings: split chunks at unusual boundaries, emit malformed and duplicate events, reorder completion, cancel midstream, fail a tool, deny confirmation, and restore a partially persisted conversation. Assert stable state and visible outcomes without snapshotting provider prose.
