---
name: flutter-code-review
description: Review Flutter and Dart diffs, commits, pull requests, or focused modules for concrete correctness, lifecycle, architecture, security, accessibility, performance, and test risks. Use when the user explicitly asks for review or audit findings; report actionable evidence without changing code unless a fix is also requested.
---

# Flutter Code Review

Find defects that materially affect behavior, users, delivery, or maintainability. A review is an evidence-backed risk assessment, not a style tour or an implicit rewrite.

## Establish the review boundary

1. Determine the requested diff, commit range, pull request, working tree, or module and the intended behavior.
2. Read repository instructions and inspect enough nearby code, tests, generated boundaries, and configuration to understand changed behavior.
3. Review changed lines first, but follow their data flow and lifecycle when evidence requires surrounding context.
4. Do not edit files, post comments, approve, merge, or expand into remediation unless the user authorizes those actions.

## Review by risk

Prioritize data loss, security exposure, crashes, incorrect results, broken lifecycle, concurrency races, inaccessible flows, release failures, and missing regression coverage. Then consider architecture or maintainability issues that have a concrete cost.

Do not report preferences, hypothetical rewrites, unchanged legacy issues, or framework behavior that current code already handles. Validate API and package claims against the project's SDK and resolved dependencies.

## Load references conditionally

- Read [review workflow](references/review-workflow.md) for gathering the change, tracing impact, calibrating severity, and formatting findings.
- Read [Flutter review checklist](references/flutter-review-checklist.md) only for the technical domains touched by the change.

Load available specialists only when their domain is materially changed or a claim needs deeper verification. A review touching storage does not automatically require every quality skill.

## Output

Lead with findings ordered by severity. Each finding must name the affected file and tight line range, explain the failure path and impact, and propose a proportionate correction. Keep separate sections for open questions and a short summary only when useful.

If there are no actionable findings, say so directly and identify meaningful verification gaps. Never invent findings to make the review appear thorough.

## Sources

- [Flutter testing](https://docs.flutter.dev/testing)
- [Flutter performance](https://docs.flutter.dev/perf)
- [Flutter architecture](https://docs.flutter.dev/app-architecture)
- [Effective Dart](https://dart.dev/effective-dart)
