---
name: flutter-ui-design
description: Design or visually refine Flutter screens with clear hierarchy, coherent design tokens, typography, color, surfaces, complete UI states, and platform-aware polish. Use for UI/UX design, redesign, visual direction, or making an interface feel intentional and production-ready; route widget architecture and responsive mechanics to their dedicated skills.
---

# Flutter UI Design

Create coherent, platform-aware Flutter interfaces where every visual choice supports the product's primary task.

## Scope

Own visual direction, hierarchy, composition, semantic tokens, typography, color, surfaces, shape, state presentation, and final visual review.

Route implementation structure, reusable widget APIs, forms, and UI state ownership to `flutter-ui-patterns`. Route constraint mechanics to `flutter-responsive-layout`, motion implementation to `flutter-animation`, accessibility compliance to `flutter-accessibility`, and navigation behavior to `flutter-navigation`.

## Preflight

Before proposing a redesign:

1. Inspect `pubspec.yaml`, supported platforms, nearby screens, assets, fonts, and any supplied references.
2. Find existing `ThemeData`, `ColorScheme`, `TextTheme`, component themes, `ThemeExtension`s, and design-system widgets.
3. Preserve the established brand and component vocabulary unless the request explicitly authorizes a redesign.
4. Do not add a UI package, font, icon set, or competing theme merely because it is familiar.

## Design workflow

1. State the screen's primary user task and the visual problem in observable terms.
2. Derive three to five constraints such as tone, density, hierarchy, brand expression, and platform expectations. Replace vague goals like “modern” with specific decisions.
3. Establish or extend semantic tokens before styling individual widgets. Reuse the project's token scale instead of introducing one-off values.
4. Compose one representative screen around real copy and realistic data. Make the primary action and reading order immediately apparent.
5. Design every relevant state: loaded, loading, empty, error, offline or stale, disabled, focused, hovered, pressed, and selected.
6. Implement through the existing theme and component system, then compare the same fixtures before and after.

## Design rules

- Use typography, spacing, alignment, and grouping before adding decoration.
- Give each surface one clear primary action. Keep secondary actions visibly subordinate.
- Do not turn every content group into a card; use whitespace and dividers when elevation adds no meaning.
- Do not default to gradients, glass effects, glows, oversized radii, or heavy shadows. Use them only when the product language and content justify them.
- Keep color, type, spacing, shape, iconography, and elevation on a small semantic system.
- Use realistic content; placeholder text often hides hierarchy and overflow problems.
- Pair ambiguous icons with labels or other context.
- Preserve brand identity while adapting controls, gestures, density, and navigation conventions to the target platform.

## Load references conditionally

- Read [visual foundations](references/visual-foundations.md) when selecting or extending tokens, typography, color, shape, iconography, or elevation.
- Read [screen composition](references/screen-composition.md) when establishing hierarchy or redesigning a full screen.
- Read [states and feedback](references/states-and-feedback.md) when the interface loads data, accepts input, fails, or needs interaction polish.
- Read [platform adaptation](references/platform-adaptation.md) when targeting more than one platform or translating an iOS, Android, web, or desktop reference.
- Read [visual verification](references/visual-verification.md) before claiming the redesign is complete.

## Verification

Capture stable screenshots or golden fixtures for representative states and form factors. Inspect light and dark themes, compact and wide layouts, text scaling, localization where relevant, pointer or keyboard focus where supported, and platform-specific controls. Test behavior separately from appearance.

If the runnable project or required assets are not supplied, define the smallest representative fixture matrix and state what must be rendered later; do not claim visual verification from a design proposal or source text alone.

Report observable improvements—such as clearer action priority, fewer competing surfaces, consistent token use, and complete state coverage—instead of claiming that a screen is simply “beautiful.”

## Sources

- [Material Design for Flutter](https://docs.flutter.dev/ui/design/material)
- [Use themes to share colors and font styles](https://docs.flutter.dev/cookbook/design/themes)
- [Platform adaptations](https://docs.flutter.dev/ui/adaptive-responsive/platform-adaptations)
- [Adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Typography](https://docs.flutter.dev/ui/design/text/typography)
