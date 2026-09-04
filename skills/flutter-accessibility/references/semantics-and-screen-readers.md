# Semantics and Screen Readers

Screen readers (TalkBack on Android, VoiceOver on iOS/macOS) translate Flutter's semantics tree into spoken feedback and braille output. Proper semantics configuration ensures all users can navigate and operate the app.

## The Semantics Tree

Flutter automatically builds a semantics tree from built-in widgets (e.g., `Text`, `ElevatedButton`, `Checkbox`). Only add manual `Semantics` widgets when custom interactive or composite components are used.

### 1. `Semantics`
Use to annotate custom interactive elements with label, hint, value, button flag, or custom actions:
```dart
Semantics(
  button: true,
  enabled: isActionable,
  label: 'Add item to shopping cart',
  hint: 'Double tap to activate',
  onTap: onAddToCart,
  child: CustomCartButton(),
)
```

### 2. `MergeSemantics`
Merge a subtree of related nodes into a single semantic focus node. Essential for list tiles or cards containing an icon, title, and subtitle so the screen reader speaks the entire group together instead of forcing three separate swipes:
```dart
MergeSemantics(
  child: Row(
    children: [
      Icon(Icons.check_circle),
      SizedBox(width: 8),
      Text('Order Placed'),
    ],
  ),
)
```

### 3. `ExcludeSemantics` / `BlockSemantics`
- **`ExcludeSemantics`**: Hide purely decorative elements (icons with adjacent text, background illustrations, spacer art) from the screen reader to reduce audio clutter.
- **`BlockSemantics`**: Drop semantics behind a modal surface (dialog, bottom sheet, drawer) to prevent screen readers from focusing on backdrop widgets.

## Dynamic Announcements

To notify screen reader users of asynchronous events (e.g., "Item added to cart", "Network disconnected"):
```dart
SemanticsService.announce(
  'Changes saved successfully',
  TextDirection.ltr,
);
```
- Avoid rapid, continuous announcements that interrupt user navigation.

## Automated Verification

- In widget tests, enable semantics using `tester.binding.pipelineOwner.semanticsOwner`:
  ```dart
  final handle = tester.ensureSemantics();
  expect(tester.getSemantics(find.byType(CustomCartButton)), matchesSemantics(...));
  handle.dispose();
  ```
- Use `meetsGuideline(androidTapTargetGuideline)` and `meetsGuideline(iOSTapTargetGuideline)` in widget tests.
