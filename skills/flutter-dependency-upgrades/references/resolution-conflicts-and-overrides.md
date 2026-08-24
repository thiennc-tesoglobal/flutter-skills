# Resolution conflicts and overrides

## Diagnose the graph

Preserve the full solver error. Identify the incompatible package, which direct dependencies constrain it, whether the conflict is direct or transitive, the effective SDK constraint, dependency sources, prerelease use, workspace members, and any existing overrides. Use `dart pub outdated --transitive`, `dart pub deps`, dry-run resolution, and package publisher metadata as evidence where supported.

Do not delete or manually edit `pubspec.lock` to hide the graph. `pub get` tries to preserve locked versions where possible; `pub upgrade` intentionally seeks newer allowed versions. Choose the command that matches the requested scope and inspect its diff.

## Resolve at the owning constraint

Prefer, in order:

1. a compatible release of the direct dependency that owns the restrictive transitive constraint;
2. a coordinated upgrade or downgrade of a related package cohort;
3. a documented constraint change supported by the package's actual API and SDK requirements;
4. replacement of an abandoned or incompatible package when the user accepts the product change;
5. a temporary fork/path/git source only with explicit ownership and an exit plan.

Use `dependency_overrides` as a bounded experiment or temporary compatibility bridge, not evidence that an unsupported combination is safe. Keep the override visible, documented, tested, and removable; prefer `pubspec_overrides.yaml` for local experiments when repository policy excludes it from version control. Never use `any` or a broad override merely to silence the solver.

For Pub workspaces, inspect the shared root resolution and all members that constrain the package. Avoid stray nested lockfiles or package configs that shadow the workspace resolution.

## Verification

Resolve without the diagnostic override when possible. Then analyze, test, regenerate, and build affected targets. For a published package, test the declared compatibility range or the project's supported lower-bound strategy, not only the newest lock resolution. Record any forced source, override, or fork as remaining debt.

## Sources

- [Dart package dependencies and overrides](https://dart.dev/tools/pub/dependencies)
- [dart pub outdated](https://dart.dev/tools/pub/cmd/pub-outdated)
- [Pub workspaces](https://dart.dev/tools/pub/workspaces)
- [The pubspec file](https://dart.dev/tools/pub/pubspec)
