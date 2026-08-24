# Feature boundaries and dependency rules

Group code by user-facing capability when it has distinct state, behavior, or data ownership. A feature may expose a small public surface while keeping widgets, state, models, and data adapters private to itself.

## Dependency rules

- UI depends on presentation state, not concrete HTTP, database, or plugin clients.
- Repositories own domain-facing data policy and coordinate services or caches.
- Services translate external protocols and platform APIs; they do not own UI state.
- Cross-feature reuse goes through a stable capability contract or shared domain concept, not another feature's internal files.
- `core` contains genuinely cross-cutting infrastructure, not code that lacks an owner.

Use an interface when multiple implementations, isolation from an external dependency, or meaningful test substitution justifies it. Avoid speculative abstractions and pass-through layers.

Validate with import/dependency rules where the repository already supports them, plus tests at the feature boundary. A diagram is useful only if it matches actual imports and runtime ownership.

## Sources

- [Flutter architecture concepts](https://docs.flutter.dev/app-architecture/concepts)
- [Flutter dependency injection case study](https://docs.flutter.dev/app-architecture/case-study/dependency-injection)
