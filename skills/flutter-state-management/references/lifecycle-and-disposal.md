# Lifecycle and Disposal

Proper disposal of state resources prevents memory leaks and unintended behavior across screens or sessions. Follow these rules for common patterns.

## Disposal Patterns

- **ChangeNotifier**: Implement `dispose()` and call it when the owner is removed from the widget tree. Ensure any `addListener` calls have corresponding `removeListener` cleanup if the notifier outlives the listener.
- **Bloc/Cubit**: Clean up resources in `close()`. If the Bloc creates standard Dart Streams, ensure they are canceled here.
- **Riverpod**: For `autoDispose` providers, rely on Riverpod's internal cleanup, but explicitly register disposal callbacks via `ref.onDispose` for native resources or non-Riverpod listeners.

## Stream and Controller Cleanup

- Close any `StreamController` created locally. Do this in `dispose()` or the equivalent lifecycle teardown method.
- Cancel all active `StreamSubscription` instances when the class that created them is disposed. Do not rely on garbage collection for active subscriptions.

## Testing Lifecycle

- Explicitly test the disposal path. Verify that resources are freed, subscriptions are canceled, and no lingering state remains that could pollute the next run.
- Test that calling `dispose()` twice (if allowed by the framework) is safe or throws appropriately, and verify no updates are emitted post-disposal.

## Leak Patterns

- **Global Singletons**: Do not use global singletons or static variables as a substitute for clear scope boundaries and proper disposal. Global lifespans bypass tree lifecycle hooks.
- **Undisposed Controllers**: Missing `close()` calls on controllers or missing `cancel()` calls on subscriptions are the primary sources of leaks in Flutter apps. Review these carefully.
