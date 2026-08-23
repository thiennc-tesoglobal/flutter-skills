# Art direction and visible transformation

Use this reference when a screen feels generic, the user asks for a noticeable redesign, or a polished visual reference is available.

## Calibrate ambition

Classify the assignment before choosing treatments:

- **Preservation:** repair hierarchy or consistency without changing the recognizable visual language.
- **Refinement:** improve craft and state quality while retaining the existing direction.
- **Visible transformation:** establish a stronger identity that is immediately apparent in a before-and-after comparison.
- **Reference parity:** recover the reference's visual ambition, hierarchy, density, and product relationships while adapting platform mechanics.

Do not choose a restrained default merely because the brand brief is incomplete when the user has explicitly requested a visible transformation. State a coherent direction, implement a representative slice, and let rendered evidence expose the remaining choices.

## Define a design signature

Write one sentence describing the product feeling, then make a small set of mutually reinforcing decisions:

- **Background:** flat, tonal, atmospheric, illustrated, spatial, or content-led.
- **Surfaces:** mostly flat grouping, bordered panels, material/translucent layers, or deliberate elevation.
- **Typography:** quiet editorial, compact utility, rounded friendly, technical, or another supported character.
- **Accent:** where saturation appears, what it communicates, and where it is intentionally absent.
- **Shape:** one coherent family with role-specific variation instead of the same radius everywhere.
- **Motion:** what changes should feel continuous, responsive, celebratory, or still.
- **Content voice:** concise utility, warm coaching, professional confidence, or another product-appropriate tone.

A direction is not a list of effects. Remove any treatment that does not reinforce the sentence.

## Escape the framework-default look

Flutter's standard widgets provide strong semantics and behavior, but a collection of untouched defaults rarely creates product identity. Review the composed screen for:

- Default `Scaffold` plus app bar plus floating action button with no product-specific relationship
- `ColorScheme.fromSeed` carrying nearly the entire visual direction
- Generic cards, chips, and inputs repeated without role differentiation
- Material icons used as decoration rather than communication
- Equal spacing and weight across unrelated sections
- A hero area that consumes space without adding useful context
- An empty state that looks like a component sample instead of a first-use experience

Prefer theming, composition, custom painting, gradients, `BackdropFilter`, clipping, and core animation primitives before adding a dependency. Preserve accessible semantics and interaction behavior when changing appearance.

## Work from references

When a sibling native implementation or image is supplied:

1. Inspect the rendered reference and its representative data state.
2. Extract the design signature and the relationships that create its character.
3. Separate transferable product design from operating-system chrome and APIs.
4. Map each transferable quality to a maintainable Flutter primitive or token.
5. Compare screenshots at equivalent viewport, theme, content, and state.

Do not copy names, assets, or platform-only APIs unless they belong to the shared product. Do not discard translucency, expressive backgrounds, motion, or composition solely because their original implementation is platform-specific.

## Design the first frame

The first useful frame should communicate the product even before interaction. Verify both:

- A populated fixture with realistic short, typical, and long content
- The actual first-use or empty state with one meaningful next action

Use deterministic fixture data for previews, golden tests, and screenshots. Keep demo fixtures out of production persistence unless the product explicitly wants starter content.

## Stop condition

After the first render, identify the three largest gaps in hierarchy, identity, density, state quality, or reference parity. Iterate on material gaps and render again. Stop when another pass would only change personal preference, or when a product decision or unavailable asset blocks progress; report that boundary explicitly.
