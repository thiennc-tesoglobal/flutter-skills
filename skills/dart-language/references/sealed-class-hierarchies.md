# Sealed Class Hierarchies

Sealed classes enable algebraic data types (ADTs) and exhaustive pattern matching in Dart. Use sealed hierarchies to model closed sets of subtypes, such as UI states, API results, or command messages.

## Defining Sealed Hierarchies

Mark the root of the class hierarchy with the `sealed` modifier. All direct subtypes must be defined within the same library (file):

```dart
sealed class Result<T> {
  const Result();
}

final class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}

final class Failure<T> extends Result<T> {
  final Exception error;
  final StackTrace? stackTrace;
  const Failure(this.error, [this.stackTrace]);
}
```

## Class Modifiers and Subtyping

- **`sealed`**: Cannot be instantiated directly, cannot be extended/implemented outside its defining library. Guarantees exhaustiveness in switch statements and expressions without needing a fallback `default` case.
- **`final`**: Subtype cannot be extended, implemented, or mixed in outside the library, preventing external hierarchy pollution.
- **`base`**: Subtype enforces inheritance; outside callers can extend it but cannot implement its interface.
- **`interface`**: Subtype enforces interface implementation; outside callers can implement it but cannot extend its implementation.

## Exhaustive Switch Verification

Always leverage compiler exhaustiveness rather than adding a generic `default` branch:
```dart
String describeResult(Result<User> result) => switch (result) {
  Success(:final data) => 'Loaded user: ${data.name}',
  Failure(:final error) => 'Failed with: $error',
};
```
- Omitting `default` ensures that when a new subtype is added to the sealed family in the future, the Dart compiler will flag every unhandled switch expression across the codebase as a compile error.

## Anti-Patterns

- **Do Not Wrap Everything in Sealed Classes**: Avoid sealed classes when open polymorphism (allowing package consumers or third parties to extend types) is desired.
- **Do Not Discard Failure Context**: When modeling failure variants, always retain the original exception and stack trace rather than degrading to a plain error string.
