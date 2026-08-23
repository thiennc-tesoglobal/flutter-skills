# Platform delivery

Read this reference when notification behavior depends on Android, Apple, or web configuration.

## Android

- Check the target and minimum SDK before changing manifest entries or runtime flows.
- Android 13 and later use the `POST_NOTIFICATIONS` runtime permission for non-exempt notifications. Request it in product context and test allow, deny, and dismissed states.
- Notification channel identifiers are durable user-facing contracts after creation. Choose purpose and importance deliberately; do not generate a new ID just to override a user's settings.
- Verify icons, channel/category behavior, tap intents, foreground-service implications, battery restrictions, and exact-alarm eligibility for the actual target versions.

## Apple platforms

- Check signing capabilities, APNs environment, entitlements, background modes, notification categories/actions, and service extensions only when the chosen behavior needs them.
- Query current notification settings; users may change authorization and individual presentation settings later.
- Register categories before interactions can arrive. Keep action identifiers stable and validate the response payload.
- Respect pending-request limits and platform scheduling semantics; reconcile a bounded horizon from domain state when needed.

## Web

Check secure-context requirements, service-worker registration and scope, permission state, VAPID/provider configuration, foreground-page behavior, and supported browser matrix. Do not present mobile lifecycle assumptions as web guarantees.

## Evidence

Unit and widget tests can prove contracts and app behavior but not system UI, permission dialogs, background execution, or provider delivery. Use emulator/simulator for fast checks where supported and a physical device for platform behavior the simulator cannot reproduce. Capture OS version, app lifecycle, permission state, flavor, and payload used.

## Sources

- [Android notification runtime permission](https://developer.android.com/develop/ui/views/notifications/notification-permission)
- [Apple: asking permission to use notifications](https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications)
- [Firebase Flutter messaging setup](https://firebase.google.com/docs/cloud-messaging/flutter/get-started)

