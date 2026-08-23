# Provider and monorepo

Use this reference to adapt the pipeline without forcing a provider migration.

## Provider preservation

First locate current workflow definitions and reusable templates: GitHub Actions, GitLab CI, Codemagic, Bitrise, Xcode Cloud, Jenkins, Buildkite, or another system. Map the actual triggers, jobs, stages, `needs`/dependencies, optional failures, artifact flow, and protected delivery path before editing. Follow the provider's current official schema and validate the final file with its lint, dry-run, or parser when available. Run or syntax-check every referenced repository script separately so valid YAML does not hide a broken command. Translate desired invariants—version pinning, gates, artifacts, least privilege, environments—into that provider instead of pasting a GitHub Actions template everywhere.

Keep provider-specific syntax and credentials in its own file or reusable workflow. Keep substantive build/test logic in repository scripts when that improves local reproducibility, but do not add wrappers that merely hide one command and make logs worse.

## Monorepos and workspaces

Read workspace declarations, package dependency relationships, lockfile ownership, code generation, native app roots, and existing change-detection tooling. Run each command from the expected root. Reuse trusted affected-package logic when it exists; otherwise prefer a correct full gate before inventing brittle path filters.

If adding path filters, include shared packages, root configuration, lockfiles, toolchain files, generators, and pipeline definitions that can affect downstream apps. Provide a manual/full-run escape hatch. Never allow path filtering to skip a release gate whose inputs are uncertain.

## Runner and target constraints

Use macOS only for work that actually requires Apple tooling. Confirm Xcode, Java, Android SDK, browser, desktop dependencies, CocoaPods, and Flutter versions against project constraints. Matrix labels such as `latest` can drift; follow the repository's update policy and make upgrades deliberate when reproducibility matters.

Validate pull-request, default-branch, tag/manual, and scheduled triggers independently. Check that protected delivery jobs cannot be reached from untrusted inputs and that reusable workflow inputs are typed and validated.
