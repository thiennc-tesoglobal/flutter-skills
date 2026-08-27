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
- Verify behavior of both cold and warm deep links.
- Test authentication redirects and loop prevention.
- Assert proper fallback or error handling for invalid paths.
