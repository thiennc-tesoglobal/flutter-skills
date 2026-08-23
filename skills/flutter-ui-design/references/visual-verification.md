# Visual verification

Visual quality requires repeatable evidence, not a single hand-picked screenshot.

## Define fixtures

Use deterministic data and capture the same representative fixtures before and after a redesign. Include only relevant combinations from:

- Loaded with typical and long content
- Loading, empty, partial error, full error, offline, and retrying
- Light and dark themes
- Compact and wide constraints
- Default and enlarged text
- Left-to-right and right-to-left locales
- Touch, pointer, keyboard focus, selected, pressed, and disabled states

Keep the matrix small enough to maintain while covering the highest-risk visual differences.

## Choose the evidence

Use screenshot or golden tests for stable component and screen states. Use emulator or real-device captures when system chrome, fonts, safe areas, platform controls, GPU effects, keyboard behavior, or input mode matters. Behavioral widget tests remain separate evidence.

Do not approve visual output solely from source review. Render it at the intended sizes.

## Inspect systematically

- Primary task and action are immediately identifiable.
- Reading order remains clear without accent color.
- Text wraps, scales, and localizes without clipping or hiding actions.
- Foreground/background pairs maintain contrast in every theme and state.
- Spacing and alignment follow the token rhythm.
- Components have coherent shape, icon, elevation, and state treatment.
- Empty, loading, error, offline, disabled, and focus states feel designed rather than appended.
- Touch targets, keyboard focus, hover, and platform conventions remain usable.
- Images preserve useful crops and have loading/error fallbacks.
- No decorative effect competes with content or introduces avoidable rendering cost.

## Compare and report

Describe changes in observable terms: reduced competing accents, clearer title/action hierarchy, fewer redundant surfaces, consistent typography roles, stable loading geometry, or improved state coverage.

If the result depends on subjective brand direction that the repository and brief do not establish, present a restrained default and record the open choice. Do not invent a redesign mandate or claim universal aesthetic superiority.
