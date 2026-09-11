# Lifecycle entry matrix

Use a replayable matrix when a deep link or notification tap crosses application lifecycle, authentication, navigation, or remote-data boundaries. Select only rows that can expose failures in the changed behavior.

## Scenario design

Give every row a stable name and state its entry kind, cold or warm lifecycle, account/auth fixture, current UI state, trigger identity, data behavior, expected destination, Back outcome, and allowed side effects. Include duplicate delivery when multiple listeners or initial-message handoff can receive the same intent.

Useful rows include cold signed-in entry, cold signed-out continuation after login, warm entry over a dialog or sheet, duplicate link or notification, slow/error destination API, and account switch between receipt and interaction. A launch command only proves that the OS accepted the trigger; use semantic integration assertions, running-app inspection, or focused screenshots/logs to prove the destination and side effects.

## Runner

`scripts/run_lifecycle_matrix.py` orchestrates one Android emulator/device or iOS Simulator. For iOS, `app_id` is the bundle identifier. It defaults to a dry run, invokes commands as argv without a shell, bounds each step, runs cleanup after failures, redacts common token output, removes URI queries from report labels, and writes machine-readable evidence.

Each project supplies shell-free `before`, `trigger`, `assert`, and `after` commands for its own auth fixture, provider send, API delay, semantic assertion, and cleanup. Put credentials in the command's existing environment or secret store; never place them in the matrix or command arguments.

The `tool/...` commands below illustrate project-owned hooks; replace them with commands already provided by the target repository.

The report can retain a bounded output tail from each hook. Make hooks emit already sanitized evidence and avoid full payloads, personal data, device identifiers, or secrets; automatic token redaction is only a fallback for common patterns.

```json
{
  "platform": "android",
  "device_id": "emulator-5554",
  "app_id": "com.example.app",
  "timeout_seconds": 60,
  "scenarios": [
    {
      "name": "cold-signed-out-order-link",
      "lifecycle": "cold",
      "before": [
        {"name": "seed signed-out fixture", "argv": ["tool/test-state", "signed-out"]},
        {"name": "delay order API", "argv": ["tool/test-server", "delay", "orders", "1500"]}
      ],
      "uri": "myapp://orders/42",
      "assert": [
        {"name": "login then order and Back", "argv": ["tool/assert-flow", "login-order-back", "42"]}
      ],
      "after": [
        {"name": "clear test state", "argv": ["tool/test-state", "clear"]}
      ]
    },
    {
      "name": "warm-duplicate-notification-over-dialog",
      "lifecycle": "warm",
      "before": [
        {"name": "show dialog fixture", "argv": ["tool/test-state", "dialog-open"]}
      ],
      "trigger": {
        "name": "send notification fixture",
        "argv": ["tool/send-test-notification", "order-42"]
      },
      "trigger_count": 2,
      "assert": [
        {"name": "one navigation effect", "argv": ["tool/assert-effect-count", "order-42", "1"]}
      ],
      "after": [
        {"name": "clear test state", "argv": ["tool/test-state", "clear"]}
      ]
    }
  ]
}
```

Review the plan, confirm every hook stays within the task's existing authorization, then execute it:

```sh
python3 path/to/run_lifecycle_matrix.py matrix.json
python3 path/to/run_lifecycle_matrix.py matrix.json --execute --report artifacts/lifecycle-report.json
```

Keep reports only when they contain redacted, useful evidence and the repository's artifact policy permits them. State the device, OS, flavor/build, lifecycle rows, data source, provider layer, and failed or skipped assertions in the final report.

## Sources

- [Flutter deep linking](https://docs.flutter.dev/ui/navigation/deep-linking)
- [Flutter: set up universal links for iOS](https://docs.flutter.dev/cookbook/navigation/set-up-universal-links)
- [Android: create deep links](https://developer.android.com/training/app-links/create-deeplinks)
