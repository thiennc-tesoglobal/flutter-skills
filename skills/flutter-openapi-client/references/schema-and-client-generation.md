# Schema and client generation

## Select the implementation path

Inspect the existing transport, serializer, generator, build system, naming conventions, and checked-in generated output before choosing tooling. Preserve a compatible established generator. Without one, prefer handwritten code for a small stable surface and evaluate generation for broad or frequently changing contracts. Confirm that any candidate supports the project's Dart and Flutter constraints and the contract features actually used; a generator advertising OpenAPI support may still flatten or reject particular dialect features.

Keep raw spec snapshots and generator configuration separate from generated Dart. Keep handwritten authentication adapters, domain mapping, repositories, retry policy, and business rules outside regeneratable files. Mark ownership clearly and make regeneration deterministic; never patch generated code as the durable fix when a template, mapping, adapter, or contract correction is the real owner.

## Preserve wire semantics

- Distinguish absent, nullable, required, read-only, write-only, defaulted, and deprecated fields.
- Preserve integer and number formats only to the degree Dart can represent them safely; define overflow or precision behavior when the contract exceeds native types.
- Map `format` values such as date, date-time, UUID, URI, byte, and binary deliberately instead of trusting their text shape automatically.
- Model arrays, maps, `additionalProperties`, recursive references, aliases, and free-form JSON without unsafe casts.
- Treat `oneOf`, `anyOf`, `allOf`, and discriminators according to the input dialect. Do not collapse variants into one bag of nullable fields when variant identity affects correctness.
- Define unknown-enum behavior. Closed request enums and forward-compatible response enums may need different treatment.
- Preserve parameter location, encoding, `style`, `explode`, `allowReserved`, and collection rules. Ordinary query-map encoding is not equivalent to every OpenAPI serialization style.
- Select request and response handling by media type and status code. Do not decode every success or error body into the same JSON model.

## Operations and transport hooks

Create deterministic, collision-free Dart names when operation IDs are missing, duplicated, invalid, or changed. Keep the original method and path traceable. Preserve required path parameters, optional query and header parameters, request bodies, documented status variants, empty responses, redirects where relevant, multipart parts, streaming or binary bodies, and cancellation hooks supported by the project's client.

Generate authentication interfaces from security requirements, not credentials. Respect global security, operation overrides, alternatives, combined requirements, and anonymous operations. Route token acquisition, refresh, logout, and account state to the existing authentication owner.

OpenAPI callbacks and webhooks describe inbound requests to another server; they are not ordinary requests that a Flutter client should automatically expose or start listening for. Generate or document them only when the target architecture genuinely owns that receiver.

## Sources

- [OpenAPI authentication](https://swagger.io/docs/specification/v3_0/authentication/)
- [OpenAPI parameter serialization](https://swagger.io/docs/specification/v3_0/serialization/)
- [OpenAPI file uploads](https://swagger.io/docs/specification/v3_0/describing-request-body/file-upload/)
- [OpenAPI callbacks](https://swagger.io/docs/specification/v3_0/callbacks/)
