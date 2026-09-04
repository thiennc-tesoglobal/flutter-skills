# Target Sizes and Contrast

Accessible interfaces ensure that interactive elements are easy to tap and readable under diverse lighting conditions, visual impairments, and text scaling settings.

## Touch Target Sizes

- **Minimum Dimensions**:
  - Android Material Design: Minimum **48 × 48 dp**.
  - Apple Human Interface Guidelines: Minimum **44 × 44 pt**.
- **Visual vs Semantic Target**: If an icon or button is visually smaller than 48 dp, expand its hit target using padding, `MaterialTapTargetSize.padded`, or wrapping in `ConstrainedBox`:
  ```dart
  IconButton(
    iconSize: 24,
    padding: const EdgeInsets.all(12), // Total footprint = 48x48
    onPressed: handlePress,
    icon: const Icon(Icons.close),
  )
```
- Never shrink interactive controls below the minimum threshold on touch devices.

## Color Contrast Ratios (WCAG 2.1 AA)

- **Normal Text (< 18 pt or < 14 pt bold)**: Contrast ratio must be at least **4.5:1** against the background.
- **Large Text (≥ 18 pt or ≥ 14 pt bold)**: Contrast ratio must be at least **3.0:1** against the background.
- **UI Components and Icons**: Functional icons and borders must have at least **3.0:1** contrast against adjacent colors.
- **Color Blindness / Dual Encoding**: Never convey critical state or instructions with color alone. Pair color cues with text labels, distinct icons, or patterned styling.

## Text Scaling and Dynamic Type

- Support `TextScaler` scaling up to 200% without clipping, truncation, or layout overflow.
- Avoid fixed heights on containers containing text (`SizedBox(height: 50)`).
- Allow text to wrap or use `SingleChildScrollView` / `Expanded` when large text scale is active.
- Ensure buttons and list tiles expand vertically when text scales.

## Testing Guidelines

Run Flutter's built-in accessibility matchers in widget tests:
```dart
testWidgets('A11y guidelines check', (tester) async {
  final handle = tester.ensureSemantics();
  await tester.pumpWidget(const MyApp());
  await expectLater(tester, meetsGuideline(textContrastGuideline));
  await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
  handle.dispose();
});
```
