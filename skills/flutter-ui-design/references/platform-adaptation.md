# Platform adaptation

Preserve the product's identity while respecting each platform's interaction model.

## Separate product design from operating-system behavior

Brand color, information hierarchy, content grouping, and product voice can remain consistent. Navigation conventions, gestures, control behavior, feedback, keyboard shortcuts, pointer states, and density may need to adapt.

Use Material 3 as the coherent baseline for Material apps. Use Cupertino widgets when the app's chosen design system or a platform convention warrants them—not as a blanket instruction to make every Apple target resemble a screenshot from another app.

Flutter already adapts some controls and behaviors. Inspect current framework support, including adaptive constructors and adaptive icons, before creating custom platform branches.

## Translating an iOS reference

Extract:

- Information hierarchy and task priority
- Spacing rhythm and density
- Brand tone and imagery
- State coverage and feedback intent
- Navigation and content relationships

Then remap platform-specific choices. Do not copy San Francisco typography, iOS-only navigation chrome, translucent materials, gesture assumptions, or Apple iconography literally onto Android, web, or desktop unless the product explicitly requires a cross-platform imitation and accepts the tradeoffs.

Match the reference's level of visual ambition, not just its information architecture. If translucency, atmospheric color, depth, motion, or an integrated action surface materially creates the product identity, reproduce that intent with maintainable Flutter primitives before deciding it is platform-only. A generic Material reconstruction is not successful adaptation when the supplied reference is recognizably expressive.

Compare equivalent states. A populated native reference and an empty Flutter screen do not establish visual parity; use deterministic fixture data or capture both empty states separately.

## Touch, pointer, and keyboard

Touch interfaces need forgiving targets and gesture alternatives. Pointer interfaces need hover, precise selection, scroll behavior, and appropriate cursors. Keyboard-capable platforms need visible focus order, shortcuts where valuable, and no mouse-only path.

Do not infer input mode only from screen width. A tablet may use a keyboard and pointer; a desktop window may be compact.

## Mobile, web, and desktop density

Adapt the amount of simultaneously visible information to task frequency and available space. Desktop does not mean stretching mobile controls across the window, and mobile does not mean hiding every secondary action.

Keep platform-native text selection, context menus, system back behavior, safe areas, and window conventions unless there is a tested product reason to override them.

## Adaptation review

- Does the product still feel like the same product on every platform?
- Do controls behave as users of that platform expect?
- Are navigation and back semantics native to the target?
- Do pointer, keyboard, touch, safe-area, and window states work independently of visual width?
- Is any custom platform imitation expensive to maintain without improving the primary task?
