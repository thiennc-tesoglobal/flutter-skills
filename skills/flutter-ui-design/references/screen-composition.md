# Screen composition

Compose screens around decisions and content, not around a gallery of components.

## Establish the reading order

Identify, in order:

1. The primary task or decision.
2. The context needed to make it.
3. The core content.
4. The primary action.
5. Secondary actions and supporting information.

Use position, grouping, typography, and whitespace to preserve this order. Avoid multiple headers, banners, floating controls, and accent cards competing above the fold.

For mobile, inspect the first viewport as a composition of its own. A large hero, repeated zero metrics, oversized empty-state artwork, and a detached floating action can each be reasonable in isolation but leave the product feeling sparse when combined.

## Choose a composition that fits the content

### Lists and feeds

Make scanning easy with consistent alignment, predictable metadata, and restrained separators. Emphasize the information users compare. Avoid placing every row inside a nested card unless each item genuinely behaves as an independent surface.

### Detail screens

Lead with identity and the highest-value information. Group supporting facts by user intent, not database fields. Keep a persistent action only when it remains relevant throughout the scroll and does not cover content.

### Dashboards

Prioritize decisions over metric count. Establish one summary level, then expose trends, exceptions, and drill-downs. Do not give every metric equal visual weight or use decorative charts that convey no comparison.

### Forms and settings

Group related fields, put help near the decision it supports, and show validation where it can be acted upon. Distinguish editable values from navigation rows and destructive actions. Route validation and state ownership mechanics to `flutter-ui-patterns`.

### Onboarding and empty experiences

Explain value or absence quickly, then offer one relevant next step. Illustration is optional; it should reinforce meaning rather than fill space.

Do not let the empty state become the only visually reviewed fixture. A task-oriented product must also demonstrate how typical content scans, how metadata competes, and how the primary action relates to the list.

### Wide layouts

Use available width to improve hierarchy, comparison, or multitasking—not simply to stretch phone content. Route breakpoints, constraints, and adaptive layout implementation to `flutter-responsive-layout`.

## Control density

Match density to the product and input mode. A consumer mobile screen may benefit from generous breathing room; a desktop operations tool may require compact, highly scannable rows. Preserve adequate targets and clarity in either case.

Use progressive disclosure when secondary information interrupts the main task, but keep frequent actions discoverable. Avoid hiding essential actions behind ambiguous icon-only menus.

## Preserve product identity

A professional design is recognizable without ignoring platform expectations. Express the brand through a controlled combination of color, typography, imagery, shape, illustration, voice, or motion. Do not maximize all of them simultaneously.

When a reference image is supplied, extract transferable properties—hierarchy, density, rhythm, content grouping, and brand tone—rather than tracing its pixels or importing platform-specific decoration blindly.

## Composition review

- Can a first-time user identify the screen and primary action in a few seconds?
- Does visual weight match task importance?
- Are related items closer to each other than to unrelated items?
- Can any card, label, icon, divider, or effect be removed without losing meaning?
- Does realistic long content preserve the intended reading order?
