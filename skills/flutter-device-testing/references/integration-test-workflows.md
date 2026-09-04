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
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Complete checkout flow on target device', (tester) async {
    app.main();
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
- **Pump and Settle Boundaries**: Use `pumpAndSettle()` when awaiting route transitions, but use explicit conditions or timeouts if periodic animations (such as continuous loaders or tickers) are active.
- **Deep Link Verification**: Test deep link invocation on target devices using platform commands:
  - Android: `adb shell am start -a android.intent.action.VIEW -d "myapp://product/123"`
  - iOS Simulator: `xcrun simctl openurl <device-id> "myapp://product/123"`
- **Cleanup**: Ensure integration tests tear down created test accounts or temporary local files created during the test run.
