# Apple background tasks

## Match the task class

Use the platform mode that matches the product behavior rather than enabling every background capability.

- App refresh is for short opportunities to update content.
- Processing tasks are for deferrable maintenance that may require conditions such as power or network.
- Continued or extended foreground-originated processing is for supported long-running user work; it is not a general daemon.
- Audio, location, Bluetooth, push, and similar background modes have use-case-specific policies and should be enabled only when the feature genuinely needs them.

Register permitted identifiers and handlers during the required launch phase, keep identifiers consistent across native configuration and Dart/plugin wiring, and resubmit recurring work according to the chosen API contract. An earliest begin date is not an exact execution promise: the system chooses whether and when to provide runtime based on policy and conditions.

## Expiration and completion

Install expiration handling before starting meaningful work. On expiration, cancel network, database, or computation ownership, checkpoint only valid durable progress, and report completion exactly once through the platform contract. Design the next run to resume safely rather than assuming the process will remain alive.

Keep background capabilities and task identifiers minimal. Do not claim periodic execution, execution after force-quit, or a precise daily time unless the relevant Apple API explicitly guarantees that behavior.

## Verification

Test registration and submission errors, expiration, cancellation, duplicate execution, disabled background refresh, account removal, and partial progress. Use the supported Xcode/device simulation path for the chosen task type and separately verify a real lifecycle path. A direct callback invocation proves job logic, not scheduler delivery.

## Sources

- [BGTaskScheduler](https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler)
- [Using background tasks to update your app](https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app)
- [Configuring background execution modes](https://developer.apple.com/documentation/xcode/configuring-background-execution-modes)
- [Extending background execution time](https://developer.apple.com/documentation/uikit/extending-your-app-s-background-execution-time)
