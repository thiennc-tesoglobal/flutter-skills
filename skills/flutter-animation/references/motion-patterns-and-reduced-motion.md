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

## Ticker Leak Prevention
- Always call `dispose()` on `AnimationController` instances within the owning `State`'s `dispose()` method.
- Use `SingleTickerProviderStateMixin` for one controller, or `TickerProviderStateMixin` for multiple. Never leak tickers across route changes.
