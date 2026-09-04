# Isolate Communication and Worker Pools

Isolates execute code in independent memory heaps with their own event loops. Use isolates to offload heavy CPU-bound computations without blocking Flutter's UI frame budget.

## When to Use Isolates

- **CPU-Heavy Tasks**: Parsing large JSON payloads (>1 MB), image encoding/decoding, cryptography, compression, or complex data transformations.
- **Do NOT use isolates for**: Ordinary network I/O, file reading, SQLite queries, or simple data mapping. Asynchronous I/O already executes off the main thread at the OS level; spawning an isolate adds unnecessary serialization overhead.

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

## Object Transfer and Memory Boundaries

- **TransferableTypedData**: For very large byte buffers, wrap data in `TransferableTypedData.fromList()` to transfer ownership without copying. The original reference becomes invalid.
- **Sendable Types**: Primitives, null, boolean, numbers, strings, instances of `SendPort`, `Capability`, and lists/maps of sendable objects. Non-sendable types (such as open file handles, native pointers without wrappers, closures with non-transferable context) throw `ArgumentError`.

## Error Propagation and Teardown

- Always attach an error listener (`isolate.addErrorListener`) or catch errors from `Isolate.run`.
- Clean up lingering worker isolates when the host feature or application terminates to prevent resource leaks.
