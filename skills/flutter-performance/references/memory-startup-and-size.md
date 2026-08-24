# Memory, startup, and size

## Memory retention

Measure a repeated flow: establish a steady baseline, enter and leave the feature several times, force collection through the profiler when appropriate, then compare retained objects and ownership paths. Distinguish a bounded cache from unbounded growth.

Inspect lifecycle ownership of controllers, subscriptions, listeners, image caches, platform handles, and closures capturing widget state. Fix disposal or ownership at the source; do not hide retention by clearing every cache.

## Startup

Define the user-visible milestone, such as first useful frame or first interactive content. Trace initialization on a representative device in profile or release mode. Defer only work that is not required for correctness, and preserve ordering for authentication, migrations, and dependency setup.

## App size

Compare like-for-like release artifacts for the same target, architecture splits, symbols, and build configuration. Use Flutter's size analysis to identify ownership before removing assets or dependencies. Verify runtime loading and licensing after changing fonts, icons, or deferred components.

## Sources

- [DevTools memory view](https://docs.flutter.dev/tools/devtools/memory)
- [Measure app size](https://docs.flutter.dev/perf/app-size)
- [Flutter performance profiling](https://docs.flutter.dev/perf)
