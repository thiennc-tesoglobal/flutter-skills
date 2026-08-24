# Flutter implementation and parity

## Translate intent

Convert auto-layout to Flutter constraints and flex behavior, not fixed canvas coordinates. Use `Row`, `Column`, `Wrap`, slivers, constraints, alignment, and theme tokens according to the actual resizing rules. Preserve semantics and hit targets even when Figma layers are purely visual.

Do not create one widget per layer. Extract a widget when it has behavior, a reusable visual contract, isolated state, or a meaningful rebuild boundary. Keep decorative layers close to their owner.

Use provided assets when licensing and quality are clear. Prefer vectors for suitable icons and shapes, but validate unsupported SVG features and rasterize intentionally when needed. Do not silently replace a brand font or icon family.

## Parity loop

1. Seed stable populated, loading, empty, error, disabled, and selected fixtures that exist in the design.
2. Render at the reference surface, pixel ratio, text scale, theme, and locale.
3. Compare reference and implementation side by side or with an image diff.
4. Fix structure and hierarchy first, then typography, spacing, color, assets, and finishing details.
5. Repeat at narrow/wide constraints and with large text when the product supports them.

Document intentional deviations such as platform controls, accessibility changes, unavailable assets, or a design-system token correction. Visual similarity alone does not override interaction, semantics, or runtime constraints.

## Sources

- [Flutter layout constraints](https://docs.flutter.dev/ui/layout/constraints)
- [Flutter asset and image documentation](https://docs.flutter.dev/ui/assets/assets-and-images)
