# Visual foundations

Use these rules to turn visual direction into a small, maintainable Flutter theme rather than scattered styling.

## Start from the product

Inspect the current `ThemeData` and component library first. Preserve recognizable brand colors, type choices, shapes, and density unless the brief explicitly changes them. If no system exists, derive the minimum one needed for the current product; do not invent a broad design system spec without evidence.

## Hierarchy

Build hierarchy with position, scale, weight, color, whitespace, and grouping. A screen should have one dominant reading path and one obvious primary action. If every heading, card, icon, and button is visually loud, none of them is dominant.

Check the screen in grayscale or at a glance. The primary content and action should remain identifiable without relying on accent color alone.

## Semantic tokens

Prefer the project's existing token vocabulary. Otherwise define a compact semantic layer:

- `ColorScheme` for roles such as primary, surface, error, and their contrasting foreground colors.
- `TextTheme` for content roles rather than widget-specific font sizes.
- Component themes for repeated control treatment.
- `ThemeExtension` only for stable product-specific concepts that Flutter's theme does not already express.

Avoid raw color, spacing, radius, and duration literals repeated across screens. Avoid wrapping every primitive in a custom token when it is used once and has no semantic meaning.

Concrete seed colors and scale values still need one canonical declaration. Defining them once inside `ThemeData`, `ColorScheme`, `TextTheme`, a component theme, or the project's token layer is centralized configuration—not the scattered-literal problem this guidance is intended to prevent.

## Spacing and alignment

Reuse the project's spacing scale. If none exists, introduce a small rhythm that fits its density and platforms, then use it consistently. Flutter does not require one universal spacing grid.

- Align related content to shared edges.
- Use smaller gaps within a group and larger gaps between groups.
- Let whitespace establish sections before adding containers.
- Treat optical alignment as a deliberate exception, not a stream of unexplained magic numbers.

## Typography

Assign styles by role: display or hero, title, body, label, and supporting text. Limit the number of simultaneous levels and rely on weight and whitespace before adding more sizes or colors.

Preserve dynamic text scaling. Check wrapping, line height, truncation, and readable line length with realistic copy. Do not use fixed-height text containers to force a composition to look tidy.

## Color

Use semantic foreground/background pairs from `ColorScheme`, including their dark-theme equivalents. Reserve saturated accents for high-value emphasis rather than painting every interactive element with the brand color.

Never encode status only with hue. Pair destructive, warning, success, selection, and disabled states with text, shape, iconography, or structure. Verify actual contrast rather than assuming a framework default makes custom combinations accessible.

## Surfaces, shape, and elevation

Use a surface change when it communicates containment, selection, hierarchy, or interaction. Prefer flat grouping when whitespace or a divider communicates the same relationship.

Keep shape families coherent. A radius may express product character, but uniformly oversized rounding makes controls, cards, sheets, and banners lose their roles. Use elevation and shadow sparingly, with a clear layering purpose.

## Icons and imagery

Reuse the project's icon family and established stroke or fill style. Prefer familiar platform-adaptive symbols where available. Add labels when the meaning is not universal.

Give imagery a content role, stable aspect ratio, crop policy, loading treatment, error fallback, and meaningful semantics. Decorative artwork must not compete with essential content or actions.

## Flutter mapping checklist

- Configure shared color and type roles in `ThemeData`.
- Set component themes for repeated buttons, inputs, cards, navigation, dialogs, and selection controls.
- Read styles with `Theme.of(context)` instead of duplicating them locally.
- Keep product tokens semantic so light/dark themes and brand variants can map them differently.
- Prefer stable, documented Flutter APIs over visual-effect packages with no product requirement.
