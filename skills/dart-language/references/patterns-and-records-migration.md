# Patterns and Records Migration

Dart 3 introduces first-class records and pattern matching. Use these features to simplify destructuring, multiple returns, and conditional branching while preserving type safety.

## Records for Anonymous Composites

- **Multiple Return Values**: Use records to return multiple values from private or local methods instead of creating artificial single-use tuple classes or using loosely typed `List<dynamic>` / `Map<String, dynamic>`:
  ```dart
  (double lat, double lng) parseCoordinates(String input) { ... }
  ```
- **When NOT to Use Records**: Do NOT use records for public domain entities, persistent data transfer objects (DTOs), or models requiring JSON serialization, named methods, inheritance, or validation invariants. Use concrete classes for domain entities.

## Pattern Matching and Destructuring

### 1. Object and Record Destructuring
Extract fields directly in variable declarations or case clauses:
```dart
final (lat, lng) = parseCoordinates(raw);
final {'id': int id, 'name': String name} = jsonMap;
```

### 2. Switch Expressions
Replace verbose imperative switch statements with concise switch expressions:
```dart
final statusColor = switch (order.status) {
  OrderStatus.pending => Colors.amber,
  OrderStatus.completed => Colors.green,
  OrderStatus.cancelled => Colors.red,
};
```
- Switch expressions require exhaustiveness. The compiler guarantees all possible values are handled.

### 3. Guard Clauses
Refine pattern matching with logical guards (`when`) in switch expressions and statements:

```dart
// Switch expression (evaluates to a value; no 'case' keyword)
final label = switch (items) {
  [final first, ...] when first.isValid => 'Valid: ${first.name}',
  [_, ...] => 'Invalid leading item',
  [] => 'Empty',
};

// Switch statement (imperative control flow; uses 'case ... when ...:')
switch (items) {
  case [final first, ...] when first.isValid:
    process(first);
    break;
  default:
    fallback();
}
```

## Migration Rules

- **Preserve SDK Constraints**: Check `pubspec.yaml` environment SDK bounds (`sdk: '>=3.0.0 <4.0.0'`) before migrating older syntax.
- **Do Not Break Public APIs**: Do not change public method signatures or return types of distributed packages without following deprecation and semantic versioning rules.
- **Avoid Novelty**: Do not replace clean, readable `if` statements with complex, unreadable pattern gymnastics merely because the syntax exists.
