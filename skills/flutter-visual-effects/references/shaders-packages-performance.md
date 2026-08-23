# Shaders, packages, and performance

Read this reference when the requested effect samples or distorts pixels, requires a package decision, or can materially affect raster work.

## Choose core, shader, or package

| Requirement | Preferred starting point |
|---|---|
| Gradient, glow, border lighting, simple noise | Decoration, `CustomPainter`, masks, or existing project primitives |
| Frosted material | Clipped `BackdropFilter` with tint and contrast layers |
| Filter one owned image or subtree | `ImageFiltered` |
| Refraction, chromatic split, ripple, dissolve, procedural distortion | Custom fragment shader |
| Complex shape blending already solved by a maintained dependency | Evaluate the package against the project constraints |
| Exact native material is a product requirement | Platform integration plus an explicit non-native fallback |

## Fragment shader discipline

Inspect the project's Flutter constraint before choosing syntax. Declare `.frag` assets in `pubspec.yaml`, load them with `FragmentProgram`, and reuse programs or shader instances where safe instead of recompiling per frame. Keep uniform ordering documented beside the Dart binding and drive uniforms from normalized geometry and state.

Custom shaders used as `ImageFilter`s have renderer-specific constraints. Verify current Flutter documentation and the actual target backend before relying on them; fail into a simpler material rather than throwing at runtime. Prewarm or precache shader work when the target backend would otherwise compile it during the first interaction.

Keep shader inputs bounded. Avoid capturing and converting a large scene every frame merely to distort a small control. If the effect depends on the backdrop, test it with moving and scrolling content rather than a static color fixture.

## Package gate

Before adding an effect package:

1. Read the repository's `pubspec.yaml` and lockfile.
2. Check the current pub.dev page, changelog, source repository, license, publisher, SDK range, supported platforms, renderer assumptions, and open limitations.
3. Compare the package's lowest-cost fallback with a small core-Flutter implementation.
4. Confirm that the package does not bring a competing component theme or interaction model.
5. Define unsupported-platform behavior before integrating it.
6. Get rendered and profile-mode evidence on representative devices before making it the default path.

[`liquid_glass_renderer`](https://pub.dev/packages/liquid_glass_renderer) is an example of a specialized renderer, not a default dependency. Its stability, Impeller requirements, platform matrix, memory behavior, and fallback APIs are fast-moving facts; verify them at task time and preserve a core or opaque fallback. Packages that only wrap ordinary blur and decoration rarely justify a dependency when the project needs one or two surfaces.

## Paint and compositing cost

- Clip blur and shader bounds tightly.
- Share backdrop sampling for related surfaces when the current SDK supports it.
- Avoid live blur or refraction per scrolling cell; use one containing surface, a cached approximation, or no effect.
- Pause repeating shaders and ambient effects when offscreen or inactive.
- Do not add `RepaintBoundary`, caching, reduced resolution, or a lower refresh rate speculatively; measure the same scene before and after.
- Keep a visually compatible low-cost tier for low-end devices, unsupported platforms, battery-sensitive contexts, and accessibility settings.

## Evidence matrix

For advanced effects, record:

- Flutter version, platform, renderer, build mode, and device class;
- static, scrolling, and interaction scenes that exercise the effect;
- normal, reduced-motion, high-contrast, and opaque fallback states;
- raster/UI timing or trace evidence for the affected flow;
- screenshots over quiet and busy backdrops;
- warm and first-use behavior when shader compilation or texture allocation matters.

A passing widget test proves behavior and ownership, not optical fidelity or GPU cost. A screenshot proves appearance at one state, not animation smoothness.
