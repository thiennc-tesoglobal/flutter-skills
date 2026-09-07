# Text Overflow, Wrapping, and Typography Formatting

Use this reference when resolving text layout defects, preventing dangling orphaned words, configuring multiline truncation, combining inline text spans, measuring text dimensions, or adapting copy to system text scaling.

## Prevent orphaned words (widows)

An orphan occurs when the final word of a headline, title, or label wraps onto its own line while the rest of the sentence remains on the preceding line. This harms readability and visual balance.

### The non-breaking space technique

Flutter's underlying line-breaking engine (ICU) breaks text across lines at whitespace boundaries. Replacing the final space in a string with a Unicode non-breaking space (`\u00A0`) binds the last two words together into a single unbreakable unit. When space runs out, both words wrap to the next line together instead of leaving one lonely word:

```dart
/// Glues the last two words of a string together using a non-breaking space.
String preventOrphans(String text) {
  final trimmed = text.trim();
  final lastSpaceIndex = trimmed.lastIndexOf(' ');
  if (lastSpaceIndex == -1) return trimmed;
  return trimmed.replaceRange(lastSpaceIndex, lastSpaceIndex + 1, '\u00A0');
}
```

### Preserving semantic units

Apply non-breaking spaces between values and their units or currency symbols so they are never split across lines:

```dart
// Bad: "$99" and "/ mo" may wrap to separate lines
Text('$price / mo')

// Good: Keeps amount and unit glued together
Text('$price\u00A0/\u00A0mo')
Text('15\u00A0MB')
Text('24\u00A0°C')
```

---

## Flex layout text containment

The most common Flutter layout exception is `RenderFlex overflowed by X pixels` caused by unconstrained text inside a `Row` or `Flex`.

### Why it happens

A `Row` grants unbounded maximum width to its children. A `Text` widget measures its own natural width and attempts to consume infinite width, colliding with the viewport boundary.

### Solutions

1. **`Expanded` (tight fit):** Forces the `Text` widget to consume all remaining available space and forces width constraints onto the text layout engine:

```dart
Row(
  children: [
    const Icon(Icons.account_circle),
    const SizedBox(width: 8),
    Expanded(
      child: Text(
        user.displayName,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
    ),
    Text(user.formattedTimestamp),
  ],
)
```

2. **`Flexible` with `FlexFit.loose` (loose fit):** Allows the `Text` to take only as much space as it needs up to the available remaining width, without expanding to fill the row:

```dart
Row(
  mainAxisSize: MainAxisSize.min,
  children: [
    Flexible(
      fit: FlexFit.loose,
      child: Text(
        tag.name,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
    ),
    const SizedBox(width: 4),
    const Icon(Icons.close, size: 16),
  ],
)
```

---

## Truncation and multiline wrapping

### Truncation behaviors (`TextOverflow`)

| Overflow mode | Visual behavior | Best used for |
|---|---|---|
| `TextOverflow.ellipsis` | Appends `...` at the truncation boundary | List titles, names, article summaries |
| `TextOverflow.fade` | Softly fades the text into transparent | Horizontal tag chips, single-line breadcrumbs |
| `TextOverflow.clip` | Hard-cuts characters at the boundary box | Compact fixed-height decorative cards |
| `TextOverflow.visible` | Spills text outside its box without clipping | Special typographic designs with outer clipping |

### Multiline truncation

Pair `maxLines` with `overflow: TextOverflow.ellipsis`:

```dart
Text(
  article.summary,
  maxLines: 3,
  overflow: TextOverflow.ellipsis,
  style: Theme.of(context).textTheme.bodyMedium,
)
```

> [!NOTE]
> `softWrap: false` forces text onto a single line regardless of container width. If you set `softWrap: false`, `maxLines` is overridden or redundant. Always pair `softWrap: false` with explicit `overflow` to avoid accidental clipping.

---

## Inline rich text composition

When copy requires mixed colors, weights, links, or badges, avoid placing adjacent `Text` widgets inside a `Row`, because they will not wrap naturally across line boundaries.

### `Text.rich` vs `RichText`

- **Prefer `Text.rich`:** Inherits the ambient `DefaultTextStyle`, `Directionality`, and `TextScaler` from the Flutter widget tree.
- **Avoid raw `RichText`:** Requires explicit `TextStyle`, explicit `TextDirection`, and does not automatically listen to theme or text scale changes.

```dart
Text.rich(
  TextSpan(
    text: 'Welcome back, ',
    style: Theme.of(context).textTheme.bodyLarge,
    children: [
      TextSpan(
        text: user.name,
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
      const WidgetSpan(
        alignment: PlaceholderAlignment.middle,
        child: Padding(
          padding: EdgeInsets.only(left: 4),
          child: VerifiedBadge(),
        ),
      ),
      const TextSpan(text: '! Click '),
      TextSpan(
        text: 'here',
        style: TextStyle(
          color: Theme.of(context).colorScheme.primary,
          decoration: TextDecoration.underline,
        ),
        recognizer: tapGestureRecognizer,
      ),
      const TextSpan(text: ' to view your account details.'),
    ],
  ),
)
```

---

## Pre-layout text measurement with `TextPainter`

Use `TextPainter` when dynamic layout decisions depend on whether text will overflow or require multiple lines (such as a "Read more / Show less" toggle, or dynamic bubble sizing).

```dart
bool checkWillOverflow({
  required BuildContext context,
  required String text,
  required TextStyle style,
  required double maxWidth,
  required int maxLines,
}) {
  final textPainter = TextPainter(
    text: TextSpan(text: text, style: style),
    maxLines: maxLines,
    textDirection: Directionality.of(context),
    textScaler: MediaQuery.textScalerOf(context),
  )..layout(maxWidth: maxWidth);

  final didOverflow = textPainter.didExceedMaxLines;
  textPainter.dispose(); // Always dispose to prevent memory leaks
  return didOverflow;
}
```

---

## Text scaling and accessibility (`TextScaler`)

Users with low vision frequently configure system text size to 150%–200%.

### Verification and defensive patterns

1. **Avoid fixed container heights:** `SizedBox(height: 48, child: Text(...))` will clip or overflow when text scales up. Use `minHeight` or padding instead.
2. **Use `FittedBox` sparingly:** `FittedBox` shrinks text to fit a container, which directly counteracts the user's explicit request for larger text. Only use `FittedBox` on decorative numbers, dials, or single-character badges where truncation is unacceptable.
3. **Widget testing text scale:**

```dart
testWidgets('renders long copy without overflow under 200% text scale', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      builder: (context, child) {
        return MediaQuery(
          data: MediaQuery.of(context).copyWith(
            textScaler: const TextScaler.linear(2.0),
          ),
          child: child!,
        );
      },
      home: const Scaffold(
        body: Center(
          child: ProfileCard(username: 'Supercalifragilistic User'),
        ),
      ),
    ),
  );

  expect(tester.takeException(), isNull);
  expect(find.byType(ProfileCard), findsOneWidget);
});
```
