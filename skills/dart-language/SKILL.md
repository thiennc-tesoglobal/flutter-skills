---
name: dart-language
description: Apply modern Dart language and API patterns in non-concurrency code. Use for types, records, patterns, sealed classes, extensions, constructors, null safety, collections, and package APIs; route async and isolate work to dart-concurrency.
---

# Dart Language

Write clear Dart that fits the project's SDK constraint and established style.

## Decisions

- Read the SDK constraint in `pubspec.yaml` before using newer syntax.
- Prefer simple types and direct control flow over abstractions with no demonstrated reuse.
- Model closed variants with sealed types when exhaustive switching improves correctness.
- Use records for small structural values; use named domain types when identity, validation, documentation, or evolution matters.
- Use pattern matching when it makes branching or destructuring clearer, not as a novelty.
- Preserve public API compatibility unless a breaking change is requested.
- Keep mutable state private and expose the smallest useful surface.

Follow Effective Dart naming, documentation, usage, and design guidance. Match repository lint rules rather than adding conflicting style policy.

## Verification

Use Dart MCP semantic lookup and analysis when the current environment exposes them; otherwise inspect source and use the project CLI. Run formatting, static analysis, and the narrowest relevant tests. When changing a public package API, check examples and downstream call sites.

## Boundaries

- Async, streams, cancellation, and isolates: use `dart-concurrency`.
- Flutter widget composition or state ownership: use the relevant Flutter skill.
- JSON and persistence schema behavior belongs to the corresponding data skill.

## References

- Read [patterns and records migration](references/patterns-and-records-migration.md) when adopting pattern matching, destructuring, switch expressions, or multiple returns.
- Read [sealed class hierarchies](references/sealed-class-hierarchies.md) when designing algebraic data types, closed result models, or exhaustively verified state families.

## Sources

- [Dart language](https://dart.dev/language)
- [Effective Dart](https://dart.dev/effective-dart)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
