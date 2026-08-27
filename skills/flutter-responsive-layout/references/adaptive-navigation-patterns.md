# Adaptive Navigation Patterns

When adaptive navigation is in scope, change navigation UI based on available width, not device types.

## Navigation Progression
- **Narrow Widths (Phones)**: Use `BottomNavigationBar` or `NavigationBar`.
- **Medium Widths (Tablets/Foldables)**: Transition to `NavigationRail`.
- **Wide Widths (Desktops)**: Expand to a persistent `Drawer` or a side menu.

## Best Practices
- **Content-Driven**: Base breakpoints on the layout constraints of the content, not device model names.
- **State Sharing**: Synchronize route and selection state across all layout variants (e.g., sharing a single tab controller or routing state regardless of whether a rail or bottom bar is shown).
- **Readability constraints**: Constrain text width on large screens to improve reading comfort, rather than letting it stretch edge-to-edge. Use extra space for sidebars, supporting content, or generous margins.
- **Display Features**: Consider foldable hinges and multi-window scenarios where the aspect ratio may dynamically shift.

## Testing
- Assert layouts slightly below and above breakpoint boundaries to verify transitions.
- Ensure selection state is preserved during window resize events that cross breakpoints.
