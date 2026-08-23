# Translate iOS visual effects to Flutter

Use this reference to preserve the visual role and optical behavior of a SwiftUI reference without claiming that Flutter reproduces Apple's private material implementation.

## Translate behavior, not API names

| SwiftUI intent | Flutter implementation direction |
|---|---|
| `.ultraThinMaterial` | Clip a bounded `BackdropFilter`, then add a controlled tint, subtle edge highlight, and readable foreground. |
| `.glassEffect()` | Start with frosted core layers; add a custom shader only when refraction or dynamic lighting is visibly required. |
| `GlassEffectContainer` | Share or group backdrop work where supported, and keep related glass shapes inside one rendering boundary. |
| `.glassProminent` | Use the same material family with stronger tint, contrast, and action emphasis—not a separate unrelated style. |
| `.interactive()` | Derive highlight, scale, glow, or deformation from actual hover/press/focus state on a real control. |
| `glassEffectID` or union | Preserve stable IDs and geometry across states; let the animation layer drive the morph while the effect renderer follows. |
| `backgroundExtensionEffect` | Extend or mirror the actual background under the safe area, clip the sampled region, and verify edge artifacts. |
| `scrollEdgeEffectStyle` | Use an intentional fade, mask, material bar, or edge treatment tied to scroll state rather than cloning system chrome. |
| `PhaseAnimator` | Model explicit phases with Flutter animation primitives; keep optical rendering derived from the current phase. |
| `matchedGeometryEffect` | Use stable shared identity and a Hero or coordinated geometry animation when the same element persists. |
| native haptics | Use project-compatible Flutter haptics only for meaningful interaction milestones. |

Morphing, phase timing, spring choice, and interruption semantics belong to `flutter-animation`. This skill owns how the material renders at each sampled state.

## Core frosted-material recipe

Use core Flutter when the acceptance criteria are blur, translucency, tint, and an edge highlight:

```dart
ClipRRect(
  borderRadius: BorderRadius.circular(radius),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
    child: DecoratedBox(
      decoration: BoxDecoration(
        color: tint.withValues(alpha: tintAlpha),
        border: Border.all(color: edgeColor),
      ),
      child: child,
    ),
  ),
)
```

Treat this as a layer recipe, not a universal component. Use the project's theme, shapes, semantics, and SDK-compatible color APIs. If only one child needs blur, use `ImageFiltered`; a backdrop filter samples the already painted scene behind it.

## Fidelity ladder

- **Frosted fallback:** opaque or translucent fill, border, and restrained shadow; no live backdrop sampling.
- **Core material:** clipped backdrop blur plus tint and edge treatment.
- **Enhanced material:** core material plus state-driven highlight, grouped layers, subtle distortion, or procedural noise.
- **Liquid/refraction:** shader or a verified renderer package with explicit backend and hardware constraints.
- **Native-only parity:** platform implementation with a cross-platform fallback, only when the product explicitly accepts divergent rendering.

Choose the lowest rung that preserves the reference's meaningful identity. Do not escalate to a shader because the reference happens to be iOS.

## Accessibility and fallback

Flutter does not expose every Apple accessibility setting uniformly on every target. Use the project-compatible platform signal when available; otherwise provide an app-level opaque-material path that can be exercised deterministically.

- Reduced transparency: replace backdrop sampling and refraction with an opaque semantic surface.
- High contrast: strengthen foreground, border, and tint separation; verify actual color pairs.
- Reduced motion: stop ambient loops and responsive deformation while preserving state feedback.
- Busy backgrounds: introduce enough tint or dimming to keep labels and icons readable.
- Unsupported renderer or platform: select the documented lower fidelity tier without changing layout or interaction semantics.

## Review boundary

Compare equivalent screenshots and describe parity in properties: blur radius and containment, tint, edge lighting, depth, shape continuity, interaction response, and fallback behavior. Do not label an approximation “native Liquid Glass” merely because it is translucent.
