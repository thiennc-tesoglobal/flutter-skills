# Nested Shell Navigation

When tab shell patterns or independent back histories are in scope, use nested navigators or `ShellRoute`.

## Patterns
- **Tab Shells**: Use a parent routing mechanism (like `ShellRoute` or `StatefulShellRoute` in `go_router`) to coordinate persistent UI around changing nested content.
- **Independent Back Stacks**: Keep each tab's history isolated so navigating deep into one tab doesn't affect the history of others.

## Implementation Approaches
- **StatefulShellRoute**: Preferred in modern `go_router` usage as it manages state restoration and branch switching automatically.
- **Nested Navigators**: Manual implementation involves assigning unique `GlobalKey<NavigatorState>` to each tab's `Navigator`.

## Best Practices
- **Preserve State**: Switching between tabs must preserve scrolling and input state within each tab.
- **Testing**: Verify back behavior both within a nested route (popping a tab's stack) and across tabs (returning to a default tab or exiting the app).
