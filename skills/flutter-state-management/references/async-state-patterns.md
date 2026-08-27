# Async State Patterns

Modeling async state correctly ensures the UI stays predictable during data fetches, handles errors gracefully, and avoids impossible logic states.

## Sealed Result and AsyncValue vs. Booleans

- Use sealed classes, `AsyncValue` (Riverpod), or algebraic data types instead of loose boolean flags (`isLoading`, `hasError`).
- Loose booleans can lead to impossible combinations (e.g., `isLoading = true` AND `hasError = true` AND `data != null`), confusing the UI layer. Sealed hierarchies enforce mutually exclusive, well-defined states.

## State Modeling

Clearly delineate these standard async states where the UI needs them:
1. **Initial / Empty**: No data yet, no fetch initiated.
2. **Loading**: Fetch in progress. Distinguish between first-time loading and background refreshing if necessary.
3. **Success**: Data fetched and ready to display.
4. **Error**: Fetch failed. Store the error and stack trace for logging or display.

## Error Recovery and Retry

- Ensure error states expose enough information to allow the user to retry the operation.
- Implement explicit transitions back to `Loading` from `Error` when a retry is triggered, preventing the UI from being permanently stuck in an error state.

## Preventing Impossible Combinations

- Do not use overlapping boolean properties.
- Do not let successful data remain populated in a way that conflicts with a new loading or error state unless you explicitly model an "updating with previous data" state.
- Validate that the chosen architecture forces the compiler to check exhaustive state handling (e.g., using exhaustive `switch` on sealed classes).
