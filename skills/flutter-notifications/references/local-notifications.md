# Local notifications

Use this reference for device-scheduled notifications. Keep domain reminder state separate from the OS scheduler.

## Source of truth and reconciliation

- If a notification represents durable domain state, keep that state in the repository's existing persistence layer. Treat pending OS requests as a delivery projection, not the only copy.
- Give each projected occurrence a deterministic identifier. Re-running reconciliation must update or preserve the intended schedule without duplicating notifications.
- Reconcile after the user edits or deletes the source record and at safe lifecycle moments such as app startup, upgrade, time-zone change, or permission recovery. Do not assume every platform will wake the app after reboot or settings changes.
- Use a bounded scheduling horizon when platform pending-request limits or recurrence semantics require it. Refill the horizon from domain state.

## Time semantics

Decide whether the user means a wall-clock time in a named time zone or an elapsed duration. Store enough information to recompute future occurrences after daylight-saving or time-zone changes.

Define behavior for nonexistent and repeated local times, overdue reminders, clock rollback, locale change, and a recurrence whose source record changed. Prefer calendar-aware recurrence over adding fixed durations when the intent is “at this local time.”

Use exact Android alarms only when the product requirement is genuinely exact and the target platform permits them. Degrade explicitly to inexact delivery or an in-app reminder when exact scheduling is unavailable; do not silently claim exactness.

## Package boundary

Wrap the established notification plugin behind a narrow adapter when business logic otherwise depends on static/plugin APIs. Test recurrence and reconciliation through the adapter. Add or replace a package only after checking current platform support, maintenance, license, existing transitive/native setup, and actual missing capability.

## Verification matrix

Cover schedule, update, cancel, duplicate reconciliation, denied permission, restart, overdue item, daylight-saving boundary, time-zone change, and notification tap. Verify visible OS delivery and cancellation on at least one supported physical device when the claim depends on OS behavior.

## Sources

- [Apple: scheduling a local notification](https://developer.apple.com/documentation/usernotifications/scheduling-a-notification-locally-from-your-app)
- [Android: schedule alarms](https://developer.android.com/develop/background-work/services/alarms/schedule)

