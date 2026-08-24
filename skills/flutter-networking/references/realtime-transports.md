# Realtime transports

Use this reference for WebSocket, server-sent events (SSE), Socket.IO, GraphQL subscription transport, or another long-lived event channel.

## Identify the protocol first

Do not select a package from the word "socket" alone. Inspect the server endpoint, handshake, subprotocol, message envelope, authentication, heartbeat, delivery guarantees, supported platforms, and existing client.

- WebSocket is a bidirectional message transport. Application acknowledgements, resume, ordering, and replay remain product protocol concerns.
- SSE is a server-to-client UTF-8 event stream over HTTP. Confirm authentication and header support on every target platform, `Last-Event-ID` or equivalent resume behavior, and whether one-way delivery is sufficient.
- Socket.IO is its own event protocol over Engine.IO transports. A plain WebSocket client cannot communicate with a Socket.IO server; preserve or select a compatible client after checking server and protocol versions.
- A GraphQL subscription defines a response stream, not one universal wire protocol. Read the GraphQL reference and match the server's subscription protocol exactly.
- Keep raw TCP or UDP in this skill when implemented through established Dart networking code; add `flutter-platform-integration` only when native APIs, plugins, entitlements, or platform channels are actually involved.

## Own a connection state machine

Give each connection one lifecycle owner outside disposable widgets. Represent states useful to the product, such as idle, connecting, connected, backing off, suspended, and permanently closed. Expose domain events and connection status separately so a reconnect does not masquerade as business data.

Create subscriptions once, cancel them deterministically, and make connect, close, and dispose idempotent. Do not turn a single-subscription stream into a broadcast stream merely to silence an ownership error. Route duplicate listeners, stale callbacks, or ordering races to `dart-concurrency` when concurrency is the underlying defect.

Treat foreground, background, network changes, logout, account switch, and process restart as explicit transitions. Mobile operating systems may suspend or terminate the process; do not promise an indefinitely open connection for background alerts. Use the notification delivery path when the product must notify a terminated app, then reconcile live state after resume.

## Reconnect and resume deliberately

- Reconnect only after unexpected, retryable closure. Stop or surface action for authentication, protocol, policy, or permanent server rejection.
- Use bounded exponential backoff with jitter and reset it only after a meaningful stable connection. Avoid reconnect storms after a shared outage.
- Coordinate token refresh through one owner. Verify whether credentials are supplied in headers, query parameters, cookies, or a protocol initialization message on each platform; never assume all clients can set the same handshake headers.
- Separate reconnect from resume. Define a server cursor, event ID, revision, or snapshot refetch strategy before claiming no events are lost.
- Bound outbound buffers. Persist commands only when the product defines expiry, idempotency, ordering, conflict, and account isolation; otherwise fail visibly instead of replaying stale actions.

## Delivery, liveness, and load

Transport delivery is not business completion. When correctness matters, define message IDs, acknowledgements, sequence or revision numbers, duplicate suppression, gap detection, and authoritative snapshot recovery. Document whether ordering is per connection, topic, entity, or globally undefined.

Use the protocol or server's heartbeat contract rather than layering incompatible ping loops. Distinguish liveness timeout from ordinary request timeout. Decode text and binary frames defensively, enforce payload limits, and reject unsupported message versions.

For high-rate streams, choose an explicit semantic policy: process every event, coalesce by entity, keep latest, sample, pause upstream, or disconnect and resync. Do not allow unbounded stream controllers, widget rebuilds, logs, or in-memory queues. Measure UI and decode cost before claiming the transport causes jank.

## Verification

Use a controllable fake server or transport adapter. Cover handshake failure, malformed and oversized messages, close codes or reasons, half-open detection, heartbeat timeout, auth expiry, retry exhaustion, duplicate and out-of-order events, missed-event recovery, bounded buffering, app lifecycle transitions, logout, account switch, and disposal. Verify platform-specific connection and background behavior on intended devices before making delivery or battery claims.

## Sources

- [Flutter WebSocket recipe](https://docs.flutter.dev/cookbook/networking/web-sockets)
- [Dart web_socket package](https://pub.dev/packages/web_socket)
- [WHATWG WebSockets Standard](https://websockets.spec.whatwg.org/)
- [WHATWG server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Socket.IO protocol overview](https://socket.io/docs/v4/)
