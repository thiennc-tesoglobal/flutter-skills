# Profile and frame analysis

Use one reproducible interaction, representative data, a named device, and a profile build. Record a baseline trace before editing.

## Attribute the bottleneck

1. Locate the slow frames and compare UI-thread and raster-thread time.
2. For UI work, inspect CPU samples and timeline events around build, layout, parsing, sorting, and synchronous I/O.
3. For raster work, inspect image decode/upload, clipping, saveLayer use, shaders, and large repaints.
4. Use rebuild and repaint diagnostics to confirm scope; counts alone are not a bug.
5. Change the smallest owner of the measured work, then repeat the identical flow.

Do not prescribe `const`, list caching, isolates, repaint boundaries, or smaller images until the trace supports that intervention. Warm up both runs when shader compilation or caches would otherwise distort the comparison. Report median or a small distribution when a single run is noisy.

## Web

Profile a release-like web build with browser performance and memory tools. Record browser, renderer, viewport, and network/CPU throttling. Do not claim a Flutter DevTools frame chart proves web rendering performance when browser tooling is the relevant evidence.

## Sources

- [Flutter UI performance](https://docs.flutter.dev/perf/ui-performance)
- [Flutter performance metrics](https://docs.flutter.dev/perf/metrics)
- [DevTools CPU profiler](https://docs.flutter.dev/tools/devtools/cpu-profiler)
