# Obfuscation and Debug Symbols

Dart obfuscation hides class names, method names, and identifiers in compiled AOT binaries, making reverse-engineering more difficult. Obfuscation also produces stripped stack traces that require symbol maps to deobfuscate.

## Enabling Obfuscation

Obfuscation requires two flags used together:
```sh
flutter build appbundle \
  --obfuscate \
  --split-debug-info=build/app/outputs/symbols
```

- `--obfuscate`: Instructs the Dart AOT compiler to obfuscate symbol names.
- `--split-debug-info=<dir>`: Extracts debug symbols from the compiled binary into separate symbol files (`.symbols` or `app.android-arm64.symbols`).

## Symbol Preservation and Archiving

- **Never Discard Symbols**: Debug symbol files must be archived securely in CI or uploaded immediately to the crash reporting provider (Sentry, Crashlytics). Without the exact symbol map for that specific build number, crash stack traces from production users cannot be decoded.
- **Native Crash Symbols**:
  - Android: Preserve `mapping.txt` (ProGuard/R8) and native `.so` debug symbols.
  - iOS: Preserve `dSYM` bundles (`.app.dSYM`) generated during Xcode archiving.

## Stack Trace Deobfuscation

To manually symbolicate an obfuscated stack trace:
```sh
flutter symbolize \
  -i obfuscated_stack_trace.txt \
  -d build/app/outputs/symbols/app.android-arm64.symbols
```

## Boundaries and Threat Model

- **Obfuscation is NOT Encryption**: Obfuscation only renames identifiers. It does NOT encrypt string literals, embedded URLs, API endpoints, or assets.
- **Never Rely on Obfuscation for Secrets**: Never hardcode service secrets or private keys in Dart code under the assumption that `--obfuscate` keeps them safe. Any string in an APK or IPA can be extracted using `strings` or reverse-engineering tools.
