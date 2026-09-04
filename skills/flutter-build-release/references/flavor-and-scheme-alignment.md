# Flavor and Scheme Alignment

Flavors allow building distinct variants of an application (e.g., development, staging, production) with separate bundle IDs, service configurations, app names, and backend endpoints from the same codebase.

## Three-Tier Alignment Matrix

Every flavor requires synchronized configuration across three layers:
1. **Dart Code Layer**: Environment variables injected via `--dart-define` or `--dart-define-from-file`.
2. **Android Native Layer**: Gradle `productFlavors` grouped under `flavorDimensions`.
3. **Apple Native Layer**: Xcode Schemes mapped to dedicated Build Configurations (e.g., `Debug-staging`, `Release-staging`).

| Flavor | Android Application ID | iOS Bundle ID | Android Flavor | Xcode Scheme |
|---|---|---|---|---|
| Development | `com.example.app.dev` | `com.example.app.dev` | `dev` | `dev` |
| Staging | `com.example.app.staging` | `com.example.app.staging` | `staging` | `staging` |
| Production | `com.example.app` | `com.example.app` | `prod` | `prod` |

## Service Configuration Files

- **Firebase / Google Services**:
  - Android: Place `google-services.json` in `android/app/src/<flavor>/` (e.g., `src/staging/google-services.json`).
  - iOS: Use a build phase run-script to copy the correct `GoogleService-Info.plist` based on `${CONFIGURATION}` or `${SCHEME_NAME}`.
- **Application Icons and Names**:
  - Assign flavor-specific `res/values/strings.xml` on Android.
  - Set flavor-specific `CFBundleDisplayName` and `ASSETCATALOG_COMPILER_APPICON_NAME` in Xcode configurations.

## Command Line Invocation

Always build with explicit flavor and target specification:
```sh
flutter build appbundle --flavor staging --target lib/main_staging.dart --dart-define=ENVIRONMENT=staging
flutter build ipa --flavor staging --target lib/main_staging.dart --dart-define=ENVIRONMENT=staging
```

## Secrets and Credential Isolation

- **Never Commit Secrets**: Never commit keystores, `.p8` private keys, provisioning profiles, or production API keys to source control.
- Reference keystores and passwords in `key.properties` (added to `.gitignore`) or retrieve them from secure environment variables in CI/CD.
