# Android scheduling and services

## Select the platform mechanism

- Use WorkManager-style persistent work for deferrable, reliable jobs that should survive process exit and reboot. Express network, charging, battery, and storage constraints instead of polling for them.
- Use unique work and an explicit replacement/keep policy when multiple schedules represent the same logical job.
- Use expedited work only for important, short user-relevant work and handle quota fallback deliberately.
- Use AlarmManager only when the product truly requires alarm semantics or exact timing; route a user-visible reminder to `flutter-notifications`.
- Use a foreground service for user-noticeable ongoing work that cannot be deferred, not to bypass background limits.

Read the application's target SDK before prescribing manifest declarations or permissions. Foreground services require an ongoing notification, a declared service type, corresponding permissions where applicable, and a lawful start path. Modern Android restricts starting them from the background, applies while-in-use permission rules to location, camera, microphone, and health data, and may impose type-specific time limits.

## Lifecycle contract

Persist only compact job identifiers and durable input. Re-read authorized data when execution begins; do not serialize credentials or stale UI state into scheduler payloads. Make the job idempotent because retries, replacement, reboot recovery, and process interruption can repeat work.

Return retry only for conditions likely to recover and use bounded backoff. Treat invalid input, revoked authorization, and unsupported configuration as terminal outcomes. Cancel or invalidate account-scoped work during sign-out and data deletion.

## Verification

Test constraints, unique-work policy, retry/backoff, cancellation, and input compatibility. On a representative device or emulator, exercise app backgrounding, force-stop/process death where the platform contract supports recovery, reboot when claimed, restricted network/power, foreground-service start restrictions, notification visibility, and timeout handling. Distinguish force-stop semantics from ordinary process death.

## Sources

- [Android task scheduling](https://developer.android.com/develop/background-work/background-tasks/persistent)
- [Foreground service overview](https://developer.android.com/develop/background-work/services/fgs)
- [Restrictions on background foreground-service starts](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start)
- [Declare foreground services and permissions](https://developer.android.com/develop/background-work/services/fgs/declare)
- [Foreground service timeouts](https://developer.android.com/develop/background-work/services/fgs/timeout)
