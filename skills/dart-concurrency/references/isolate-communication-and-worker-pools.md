# Isolate Communication and Worker Pools

Isolates execute code in independent memory heaps with their own event loops. Use isolates to offload heavy CPU-bound computations without blocking Flutter's UI frame budget.

## When to Use Isolates

- **CPU-Heavy Tasks**: Parsing large JSON payloads (>1 MB), image encoding/decoding, cryptography, compression, or complex data transformations.
- **Synchronous FFI and SQLite**: Native libraries and synchronous database operations (e.g., `package:sqlite3` or heavy Drift batch operations) execute synchronously on the caller's thread and will block the Flutter UI thread. Run synchronous FFI databases in a dedicated background isolate (e.g., via `drift/isolate.dart` or `NativeDatabase.createInBackground`).
- **Do NOT use isolates for**: Ordinary asynchronous I/O (network requests, non-blocking `dart:io` reads, or simple data mapping) where Dart's event loop and OS threads already handle I/O without blocking the UI. Spawning isolates for simple async I/O introduces needless message-passing overhead.

## Patterns

### 1. One-Shot Computations (`Isolate.run`)
For isolated, single-result tasks, prefer `Isolate.run()`:

```dart
final processed = await Isolate.run(() => heavyTransform(rawData));
```

- Closure must be top-level or static, or capture only sendable objects.
- Uncaught errors in the closure are propagated back to the calling isolate as asynchronous exceptions.

### 2. Long-Running Worker Pools (`SendPort` / `ReceivePort`)
When repeatedly dispatching tasks to avoid repeated isolate spawn overhead:
- Establish a bidirectional handshake using `ReceivePort` and `SendPort`.
- Pass a response port with each request message to correlate asynchronous replies.
- Implement explicit message typing (e.g., sealed class message protocol) for request/response contracts.
- Close ports and call `isolate.kill(priority: Isolate.immediate)` during lifecycle teardown.

- **TransferableTypedData**: For very large byte buffers, `TransferableTypedData.fromList()` copies bytes once into native unmanaged memory upon creation. Subsequent transfer across a `SendPort` is an $O(1)$ pointer move with zero serialization or message copy overhead. Once materialized by the receiver via `.materialize()`, ownership is transferred and the original transferable instance cannot be read again.
- **Sendable Types**: Primitives, null, boolean, numbers, strings, instances of `SendPort`, `Capability`, and lists/maps of sendable objects. Non-sendable types (such as open file handles, native pointers without wrappers, closures with non-transferable context) throw `ArgumentError`.

## Error Propagation and Teardown

- Always attach an error listener (`isolate.addErrorListener`) or catch errors from `Isolate.run`.
- Clean up lingering worker isolates when the host feature or application terminates to prevent resource leaks.
