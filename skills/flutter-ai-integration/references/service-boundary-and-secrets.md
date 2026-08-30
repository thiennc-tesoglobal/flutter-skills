# Service boundary and secrets

Use this reference when deciding where provider access, credentials, policy, tools, and model configuration belong.

## No credential is needed to use the skill

Skill installation supplies coding instructions only. It must not ask for, create, read, or configure an OpenAI or other provider key unless the user's application task explicitly requires a provider integration and the credential is needed for authorized end-to-end verification.

First distinguish installing or documenting the coding skill from implementing an AI feature in an application. If the request is only about the skill, explain that it is static provider-neutral guidance and stop there. Do not propose or scaffold a provider SDK, environment variable, credential placeholder, backend, authentication flow, account, or billable resource without a separate application requirement.

A distributed Flutter application cannot keep a provider secret. Do not embed a secret key in Dart source, assets, `--dart-define`, obfuscated builds, mobile manifests, desktop bundles, or web JavaScript. Use an existing trusted backend or an explicitly approved server-side boundary for secrets, authorization, policy, rate limits, spend controls, audit, and provider calls. Public client identifiers or provider-designed ephemeral credentials must follow that provider's documented threat model and restrictions.

Do not create a backend, provider account, billable resource, or rotate credentials without explicit scope and authorization.

## Application-owned contract

Define the capability the product needs rather than leaking one provider's request and response types throughout the app. Model the supported inputs, streamed events, final result, citations or provenance, usage metadata where required, cancellation, and domain failures.

Keep model names, provider endpoints, policy, limits, and experiments in an environment-aware boundary. Preserve the project's existing provider unless migration is requested. A provider abstraction should support a real product or testing need; do not build a universal framework speculatively.

## Trust and safety boundary

Treat model output and tool arguments as untrusted. Validate structured output against a schema and domain rules. Render generated rich text defensively; do not execute generated markup, URLs, code, or commands automatically.

Give tools the least authority and smallest data scope needed. Separate read from write tools, validate targets and arguments, surface meaningful side effects, and require user confirmation at the point of consequential external action. A model request is not authorization to disclose unrelated local data or perform a materially different mutation.

Minimize prompts, attachments, logs, and retained conversations. Apply the product's consent, deletion, residency, retention, and sensitive-data rules at both client and backend boundaries. Do not log prompts, responses, tokens, or tool payloads by default.
