# Delivery verification

Choose checks proportionate to the change:

```sh
dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test
```

For user-visible behavior, also run the intended target and verify the changed flow. Add integration or golden tests only when they provide durable value. Use profile mode and recorded evidence for performance claims.

Final reporting should state:

- what changed and why;
- which architecture and package choices were preserved;
- exact checks run and their results;
- device/platform behavior verified;
- any remaining limitation or external blocker.
