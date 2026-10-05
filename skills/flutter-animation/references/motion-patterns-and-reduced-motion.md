# Motion Patterns and Reduced Motion

When implementing complex motion or addressing accessibility in Flutter, apply these practices:

## Staggered Animations
- Use a **single `AnimationController`** for sequential or overlapping animations.
- Define staggered timings by passing an `Interval` to a `CurvedAnimation`.
- Do not create multiple controllers unless the animations can independently change state.

## Physics-Based Animation
- Use `SpringSimulation` or `FrictionSimulation` for natural, interruptible gestures.
- Drive the animation using `AnimationController.animateWith(Simulation)`.
- Avoid hardcoded durations when physics simulations dictate the timing.

## Hero Transitions
- Keep each tag unique within a participating route subtree. The corresponding source and destination Heroes must share the same tag; making tags unique across the whole navigation stack prevents the intended flight.
- When a product appears more than once in one participating subtree, scope its tag to that visual context (e.g., `'$tabName-$productId'`) and pass the selected tag to the destination.
- **Tab shells and nested navigators**: Inspect which route subtrees participate in the owning Hero controller. Mounted tabs alone do not prove a collision. Scope duplicate tags within that collection or disable nonparticipating Heroes with `HeroMode`; verify forward and reverse flights as well as the absence of duplicate-tag assertions.

See the [Hero contract](https://api.flutter.dev/flutter/widgets/Hero-class.html) for matching tags and nested-navigator participation.

## Reduced Motion
- Read platform preferences via `MediaQuery.disableAnimationsOf(context)` or `MediaQuery.accessibleNavigationOf(context)`.
- Replace nonessential motion with immediate state changes or minimal fade transitions.
- Ensure the user can still complete tasks regardless of the motion setting.

## AnimatedSwitcher Identity
- `AnimatedSwitcher` only runs its transition when the incoming child's `Key` differs from the outgoing child's. Swapping between two widgets of the same type with no explicit `key` (for example two `Text` widgets, or two instances of the same custom widget) is treated as the same child updated in place, and the transition is silently skipped.
- Give each distinct state a stable, distinguishing `Key` (such as `ValueKey(data.id)` or `ValueKey(stateName)`) even when the widget type does not change.

## Reusing Designed Animation Packages
- For a complex, designer-produced animation (an illustrated loading state, an onboarding sequence, a mascot), check whether the project already depends on `rive` or `lottie` (or an equivalent asset-driven animation package) before hand-rolling the same result with `CustomPainter` or a long `AnimationController` sequence. Reusing the existing package keeps the asset editable by design tooling and avoids re-deriving timing curves by hand.
- A Rive or Lottie animation still needs the same lifecycle discipline as any other controller-driven motion: dispose the backing controller in the owning `State`'s `dispose()`, and respect reduced-motion preferences by pausing or substituting the asset rather than always playing a motion-heavy animation.

## Ticker Leak Prevention
- Always call `dispose()` on `AnimationController` instances within the owning `State`'s `dispose()` method.
- Use `SingleTickerProviderStateMixin` for one controller, or `TickerProviderStateMixin` for multiple. Never leak tickers across route changes.
