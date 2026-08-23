# States and feedback

An interface is not finished when only its ideal loaded state is designed.

## Loading

Preserve the expected layout so content does not jump unnecessarily. Use a progress indicator for indeterminate waits; use skeletons only when they help users anticipate stable content structure. Avoid a spinner in every independent component.

Keep navigation and safe actions available when possible. If a submission blocks interaction, communicate what is in progress and prevent duplicate work.

## Empty

Distinguish first-use emptiness, no search results, and filtered-to-zero results. Explain the cause in plain language and provide one relevant next action. Do not use celebratory artwork to obscure a problem the user must solve.

## Error, offline, and stale content

Place an error near the affected content and make recovery actionable. Preserve useful cached content when the product allows it, clearly mark stale or offline state, and avoid replacing an entire screen for a local failure.

Use concise messages that tell users what happened, what remains safe, and what they can do. Do not expose raw exceptions or blame the user.

## Disabled and unavailable

Use disabled styling only when the action must remain visible but is temporarily unavailable. Make the reason discoverable. If an action is never applicable in the current context, removing it may be clearer than presenting unexplained disabled chrome.

## Interaction states

Design pressed, hovered, focused, selected, dragged, and keyboard states for the platforms that support them. Feedback should confirm interaction without overpowering content.

Keep focus visible. Treat hover as enhancement, not the only way to reveal essential information. Use haptics sparingly for meaningful confirmation or boundary feedback; do not duplicate feedback the operating system already supplies.

Route animation timing, interruption, reduced-motion behavior, and controller implementation to `flutter-animation`.

## Microcopy

Buttons should describe the action, errors should describe recovery, and empty states should describe the next step. Keep terminology consistent with the domain and avoid generic labels such as “OK” where a precise verb is available.

## State matrix

For each asynchronous or interactive region, decide which of these states applies:

- Initial and loading
- Loaded with short, typical, and long content
- Empty or filtered empty
- Partial and full failure
- Offline, stale, or retrying
- Disabled or read-only
- Focused, hovered, pressed, and selected
- Success or confirmation

Implement and verify only relevant states, but document deliberate omissions instead of discovering them in production.
