# ICU Messages and Formatting

When working with localizations in Flutter, use standardized formats rather than manual string manipulation:

## ICU Syntax in ARB Files
- Use ICU plural syntax for counts (e.g., `=0{No items} =1{1 item} other{{count} items}`).
- Use ICU select syntax for gender or category-specific translations.
- Declare variables in the `@message_key` metadata block to document their types and meanings.

## Locale-Aware Formatting
- Use `DateFormat` for timestamps and `NumberFormat` for values.
- Use `NumberFormat.compactCurrency` or `NumberFormat.simpleCurrency` for pricing.
- Never hardcode date patterns across locales, as conventions (e.g., MM/DD vs DD/MM) vary by region.

## Fallback and Unsupported Locales
- Define a clear fallback policy in `MaterialApp` using `supportedLocales` and `localeResolutionCallback`.
- Ensure unsupported locales safely gracefully degrade (e.g., defaulting to English) without crashing or displaying raw translation keys.

## Translatable Sentences
- Avoid string concatenation. Assemble complete sentences in the ARB file with placeholders.
- Translators must have the context of the whole phrase to properly adjust word order, which varies by language.

## Testing Representative Locales
- Test layouts with long strings (e.g., German) to verify wrapping and overflow behavior.
- Test Right-to-Left (RTL) locales (e.g., Arabic) to ensure directional widgets (`Row`, `padding`) mirror correctly.
- Do not manually reverse strings or lists for RTL; rely on Flutter's `Directionality`.
