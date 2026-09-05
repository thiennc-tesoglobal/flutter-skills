# Device Discovery and Emulators

Testing on physical devices, simulators, and emulators proves real platform runtime behavior, permissions, and native bridge integration that cannot be replicated in unit or widget tests.

## Target Discovery and Selection

- **Query Available Targets**: Run `flutter devices` to list connected devices, emulators, and desktop/browser engines.
- **Select by Stable Identifier**: When multiple devices are attached, always target a specific device using its stable device ID (`-d <device-id>`):
  ```sh
  flutter devices
  flutter run -d emulator-5554 --flavor staging
  ```
- **Do NOT Reset User Devices or Casually Uninstall Applications**:
  - Never issue factory reset, wipe, or erase commands on a developer's connected physical device or primary emulator. Prefer disposable test targets or ephemeral emulators.
  - Uninstalling an application (`adb uninstall`, `xcrun simctl uninstall`) or clearing application data (`pm clear`) destroys local databases, caches, preferences, and user-owned test data. Treat uninstallation as a destructive action requiring an explicit data-preservation and authorization decision rather than routine cleanup.
  - When clean state is authorized and verified to be safe:
    ```sh
    adb -s <id> uninstall com.example.app.staging
    xcrun simctl uninstall <id> com.example.app.staging
    ```

## Capturing Platform Logs and Crashes

When an application fails to start or crashes during execution:
- Android: Capture the crash stack via `flutter logs` or direct logcat:
  ```sh
  adb -s <id> logcat -d -s flutter:V AndroidRuntime:E
  ```
- iOS: Inspect system and simulator logs via:
  ```sh
  xcrun simctl spawn <id> log stream --predicate 'process == "Runner"'
  ```

## Exercising Platform States

Verify app behavior under real OS lifecycle transitions:
- **Background and Resume**: Simulate app backgrounding and foregrounding to verify state preservation and reconnection.
- **Orientation Changes**: Verify layout transitions when rotating between portrait and landscape modes.
- **Permissions**: Test both granted and denied states for camera, location, and notification permissions.
