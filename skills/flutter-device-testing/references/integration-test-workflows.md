# Integration Test Workflows

Integration tests verify complete user journeys and native plugin interactions on a live target device using `package:integration_test`.

## Project Setup

Add `integration_test` to `pubspec.yaml` under `dev_dependencies`:
```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
```

Create test entrypoints inside the `integration_test/` directory at the project root (e.g., `integration_test/app_test.dart`):

Inspect the imported entrypoint before choosing the startup call. The example below assumes the app exposes `Future<void> main()`. Await asynchronous initialization before the first pump. For a synchronous `void main()`, call it without `await`. If the app declares `void main() async`, prefer extracting initialization into an awaitable `Future<void>` bootstrap shared by production and tests so the test can observe completion.

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Complete checkout flow on target device', (tester) async {
    await app.main(); // This example assumes Future<void> main().
    await tester.pumpAndSettle();

    // Interact with UI using standard finder and tap APIs
    final startButton = find.byKey(const Key('start_checkout'));
    expect(startButton, findsOneWidget);
    await tester.tap(startButton);
    await tester.pumpAndSettle();

    // Verify destination behavior
    expect(find.text('Order Summary'), findsOneWidget);
  });
}
```

## Running Integration Tests

Execute integration tests against a specific target device and flavor:
```sh
flutter test integration_test/app_test.dart -d <device-id> --flavor staging
```

## Best Practices and Determinism

- **Semantic Finders**: Prefer finding widgets by `ValueKey` or explicit text rather than fragile relative coordinates or deep widget-tree paths.
- **Startup Boundary**: Match the call to the actual entrypoint signature. Do not leave a returned startup `Future` unawaited, and do not mechanically add `await` to a synchronous entrypoint.
- **Startup Regression Coverage**: When extracting or changing bootstrap behavior, test that dependencies finish before the app is mounted and that an initialization failure remains observable without mounting a partially initialized app. Keep one integration smoke assertion proving the awaited startup reaches the expected first screen; inject or fake the initialization boundary for deterministic failure coverage instead of contacting live services.
- **Pump and Settle Boundaries**: Use `pumpAndSettle()` when awaiting route transitions, but use explicit conditions or timeouts if periodic animations (such as continuous loaders or tickers) are active.
- **Deep Link Verification**: Test deep link invocation on target devices using platform commands:
  - Android: `adb shell am start -a android.intent.action.VIEW -d "myapp://product/123"`
  - iOS Simulator: `xcrun simctl openurl <device-id> "myapp://product/123"`
- **Cleanup**: Ensure integration tests tear down created test accounts or temporary local files created during the test run.

For a repeated cold/warm deep-link or notification-entry matrix, use [lifecycle entry matrix](lifecycle-entry-matrix.md) and keep project-specific setup and assertions in test-owned hooks.
