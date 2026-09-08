# HTTP response evidence

Use this workflow when runtime decoding fails, the deployed API differs from documentation, or the task asks what an endpoint actually returns.

## Keep evidence separate

- Contract fields come from the exact version or hash of the OpenAPI/Swagger document and describe expected shapes.
- Documentation examples are illustrative payloads and do not establish every value, field, or error response.
- Fixtures, fakes, and mock servers prove client behavior for controlled inputs.
- Observed responses prove what one identified environment returned for a specific request at a specific time.

Do not merge these into one claimed truth. A field absent from one observed response may be optional, rollout-dependent, permission-dependent, or simply absent for that record. A field returned by staging but missing from the contract is evidence of drift, not permission to silently redefine the canonical spec.

## Capture and compare

Identify the environment or origin, build or flavor, method and path, non-sensitive query shape, status, content type, response headers relevant to decoding, and timestamp. Record a bounded redacted body or response shape. Remove authorization, cookies, tokens, personal data, device identifiers, and unrelated payload values before retaining evidence.

Compare the declared and observed response by status and media type, then by envelope, field presence, JSON type, requiredness, nullability, enum values, list/object shape, and error representation. Distinguish a protocol failure, invalid payload, generated-model mismatch, handwritten mapping error, and domain rejection.

Turn a sanitized observed shape into a regression fixture only when it contains no secrets or user data and represents behavior the client should support. Keep the original test result label: a fixture derived from staging remains a fixture during later tests.

Report the smallest accurate claim, for example: “widget test passed with a fixture matching the redacted staging response captured on this build.” Do not shorten that to “verified on staging” unless the test itself called staging.

## Sources

- [OpenAPI Specification 3.1.1: Responses Object](https://spec.openapis.org/oas/v3.1.1.html#responses-object)
- [Flutter JSON serialization](https://docs.flutter.dev/data-and-backend/serialization/json)
