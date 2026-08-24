# Greenfield and evolution

## Greenfield

Start with UI and data separation, explicit state ownership, repositories for domain data, and services around external systems. Add a domain/use-case layer only when business logic is shared, complex, or hard to test in presentation state. Choose dependency injection consistent with the project constraints; a package is not an architecture.

Document one vertical slice from user intent to data source and back. That example should make dependency direction and error ownership obvious without creating an interface for every class.

## Existing applications

Name the concrete failure before migrating: circular dependencies, untestable state, duplicated policy, cross-feature data access, or unsafe lifecycle ownership. Introduce a seam around the affected feature, migrate one path, preserve public behavior, and keep old and new paths interoperable until callers move.

Avoid a big-bang folder rewrite. File movement without corrected ownership or dependency direction is not an architecture improvement. Add characterization tests before changing behavior and remove obsolete paths only after usage is verified.

## Sources

- [Flutter architecture recommendations](https://docs.flutter.dev/app-architecture/recommendations)
- [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide)
