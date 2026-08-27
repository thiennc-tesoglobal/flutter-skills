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
- Ensure `Hero.tag` is unique across the entire navigation stack per visual instance, not just by product ID.
- When an item appears in multiple contexts (e.g., different tabs), combine the ID with a context identifier (e.g., `'$tabName-$productId'`) to avoid tag collisions.

## Reduced Motion
- Read platform preferences via `MediaQuery.disableAnimationsOf(context)` or `MediaQuery.accessibleNavigationOf(context)`.
- Replace nonessential motion with immediate state changes or minimal fade transitions.
- Ensure the user can still complete tasks regardless of the motion setting.

## Ticker Leak Prevention
- Always call `dispose()` on `AnimationController` instances within the owning `State`'s `dispose()` method.
- Use `SingleTickerProviderStateMixin` for one controller, or `TickerProviderStateMixin` for multiple. Never leak tickers across route changes.
