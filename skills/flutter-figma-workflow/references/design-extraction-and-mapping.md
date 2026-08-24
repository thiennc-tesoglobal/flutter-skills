# Design extraction and mapping

## Resolve evidence

Identify the exact file, page, frame or component node, variant, mode, viewport, and last-known design state. Inspect reusable Figma components and variables before sampling values from individual layers. Record ambiguity rather than inventing hidden states.

Capture:

- color, typography, spacing, radius, elevation, and opacity tokens;
- component variants and interaction states;
- auto-layout direction, gaps, padding, resizing, min/max constraints, and overlays;
- vector/raster assets, crop behavior, and export scale;
- prototype transitions only when they are part of the request.

Map Figma tokens and components to the app's `ThemeData`, extensions, shared widgets, and asset pipeline. Reuse an existing semantic token even when its raw value is slightly different unless parity or a deliberate design-system update requires a change.

Code Connect can provide component mappings, but generated snippets remain context, not an authority over repository conventions. Variable and file APIs may depend on scopes, plan, and access; detect capability and fall back to visible specs or exports.

## Sources

- [Figma variables API](https://developers.figma.com/docs/rest-api/variables-endpoints/)
- [Figma file endpoints](https://developers.figma.com/docs/rest-api/file-endpoints/)
- [Figma Code Connect quickstart](https://developers.figma.com/docs/code-connect/quickstart-guide/)
