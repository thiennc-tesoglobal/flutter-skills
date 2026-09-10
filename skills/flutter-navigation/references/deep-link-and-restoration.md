# Deep Link and Restoration

When handling deep links or state restoration, ensure predictable redirects and stable app states.

## Links and Redirects
- **Cold vs Warm Links**: A cold link opens the app from closed; a warm link routes within an already running app. Both must reach the correct state.
- **Auth Flow**: Route unauthenticated requests for protected content to a login screen, passing a redirect target. On success, seamlessly navigate to that target.
- **Redirect Loops**: Prevent infinite cycles by maintaining clear auth-state boundaries and avoiding circular redirect dependencies.

## State Restoration
- **RestorationMixin**: Use to persist UI state across app restarts. Combine with the router to maintain navigation history.
- **Router Integration**: Ensure deep links re-hydrate not just the destination, but also essential parent routes or dependencies required by that destination.

## Testing

Build a risk-based matrix that can be replayed with the same fixture identity and expected destination:

- Verify both cold and warm entry, including a link received while another route, dialog, sheet, or loading overlay is visible.
- Exercise signed-out redirect and post-login continuation, then repeat after logout or account switch so a destination cannot reuse stale authorization or user data.
- Assert Back or Up behavior after direct entry and after the authentication detour.
- Deliver the same link more than once and verify one intended navigation or idempotent refresh rather than stacked destinations or duplicate side effects.
- Hold the destination API in a controlled slow, empty, error, or malformed state and verify loading, cancellation, retry, and fallback behavior without losing the pending destination.
- Detect multiple listener registration by counting receipt, parsing, navigation, and domain effects for one link.
- Assert proper fallback or error handling for invalid, expired, or unauthorized paths.

Use `flutter-device-testing` when OS delivery or lifecycle behavior must be proven on a target. Keep route assertions in the project's existing integration-test or semantic inspection layer instead of relying on launch-command success alone.
