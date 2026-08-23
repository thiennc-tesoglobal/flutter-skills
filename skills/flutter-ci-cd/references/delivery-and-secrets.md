# Delivery and secrets

Use this reference for artifact, signing, and external delivery stages.

## Separate stages

Keep validation, unsigned or development builds, signed release artifacts, and external publication as distinct jobs or stages. Promote the same verified artifact where the platform permits instead of rebuilding different source after approval. Record flavor, version/build, commit, toolchain, checksums, and symbol locations.

Call the repository's established release commands and coordinate artifact configuration with `flutter-build-release`. Preserve debug/mapping/native symbols required by the observability stack. Apply retention appropriate to artifact sensitivity.

## Secrets and trust boundaries

- Store signing material, API credentials, and store tokens in the provider's protected secret facility, not source or logs.
- Give each job only the permissions and secrets it uses. Validation from an untrusted fork must not receive signing/deployment secrets or a writable token, and an artifact-only job must not receive unused store-upload credentials.
- Prefer short-lived or federated credentials where the existing platform supports them; do not migrate credentials as incidental pipeline cleanup.
- Protect production environments with repository/provider controls and required review appropriate to the project.
- Pin third-party pipeline components according to the provider's trusted immutable-reference policy and keep an auditable update mechanism.

Masking is not a substitute for avoiding output. Be cautious with shell tracing, build diagnostics, base64 values, generated files, artifacts, and environment dumps.

## Authorization boundary

Pipeline setup, dry-run validation, and generation of a store-ready artifact do not authorize store upload, beta distribution, tagging, release creation, rollout, or production deployment. Require explicit authorization immediately before the external mutation and confirm the exact app, environment, version, channel, and rollout scope.

## Sources

- [Continuous delivery with Flutter](https://docs.flutter.dev/deployment/cd)
- [GitHub: protect against Actions threats](https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats)
