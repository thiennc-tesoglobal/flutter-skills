# DevTools diagnosis

Use this reference after establishing a concrete runtime hypothesis. Select the smallest DevTools surface that can confirm or reject it.

## Evidence by symptom

- Widget identity, constraints, focus, semantics, or rebuild state: Inspector and framework diagnostics.
- Exception or incorrect branch: debugger breakpoints, exception pause settings, call stack, variables, and watches.
- Request sequencing or malformed responses: Network view plus safe application logs; do not expose tokens or sensitive bodies.
- Ownership or repeated-growth suspicion: Memory view, snapshots, allocation traces, and a repeated lifecycle flow. A single large snapshot does not prove a leak.
- CPU saturation or unexpected synchronous work: CPU profiler around a bounded reproduction.
- Missed frames: Performance view in profile mode, then route optimization claims to `flutter-performance`.
- Startup or platform registration: full process logs and platform logs, not hot reload alone.

Correlate timestamps and identifiers across surfaces. Begin with the first incorrect transition, not the loudest downstream symptom.

## Minimal experiments

Use breakpoints, conditional logging, assertions, or a local fake only to distinguish competing hypotheses. Keep experiments reversible and avoid changing multiple causes at once. Remove probes that are noisy, sensitive, or expensive; retain only diagnostics that have a justified operational owner.

## Completion evidence

After the fix, repeat the same trigger and compare the relevant evidence. Confirm the nearest adjacent error and lifecycle path, then add a regression test at the owning layer. A clean console with a different flow is not proof that the original failure is fixed.
