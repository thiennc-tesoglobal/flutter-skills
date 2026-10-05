# Nested Shell Navigation

When tab shell patterns or independent back histories are in scope, use nested navigators or `ShellRoute`.

## Patterns
- **Tab Shells**: Use a parent routing mechanism (like `ShellRoute` or `StatefulShellRoute` in `go_router`) to coordinate persistent UI around changing nested content.
- **Independent Back Stacks**: Keep each tab's history isolated so navigating deep into one tab doesn't affect the history of others.

## Implementation Approaches
- **StatefulShellRoute**: Preferred in modern `go_router` usage as it manages state restoration and branch switching automatically.
- **Nested Navigators**: Manual implementation involves assigning unique `GlobalKey<NavigatorState>` to each tab's `Navigator`.

## Best Practices
- **In-Memory Tab Preservation vs Process Restoration**: In-memory caching (via `StatefulShellRoute.indexedStack`, `IndexedStack`, or `AutomaticKeepAliveClientMixin`) preserves scroll position and input state during live tab switches, but does NOT survive OS process termination. Surviving process death requires explicit restoration IDs (`RootRestorationScope`, `restorationId`), `RestorableProperty` registration, and framework state restoration configuration.
- **Hero Tag Scoping**: When tabs stay mounted in memory, ensure Hero tags in offstage tabs do not collide with active or newly pushed routes. Scope tags by tab branch or conditionally disable offstage Heroes.
- **Escaping the shell navigator**: A route declared under a `StatefulShellBranch` (or pushed through the branch's navigator) renders inside the shell, so the tab bar and other shell chrome stay visible around it. Set `parentNavigatorKey` to the root navigator key on routes that must cover the shell chrome — a full-screen viewer, a modal flow spanning tabs — so they push onto the root navigator. While such a route is open the tab bar is covered and tab switching is unavailable; popping it returns to the same branch location.
- **Branch stacks persist across tab switches**: `StatefulShellRoute` keeps each branch's stack when switching tabs. If a pushed route disappears after switching away and back, diagnose the actual cause before moving routes — common ones are a plain `ShellRoute` (no per-branch navigators), navigating with `go` to a location that replaces the stack, or a `GoRouter` instance recreated during rebuild.
- **Testing**: Verify back behavior both within a nested route (popping a tab's stack) and across tabs (returning to a default tab or exiting the app).
