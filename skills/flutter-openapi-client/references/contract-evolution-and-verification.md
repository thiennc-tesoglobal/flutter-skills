# Contract evolution and verification

## Compare stable inputs

Retain or retrieve the exact old and new raw documents, including external references, generator version, configuration, and normalization rules. Compare semantic operations and schemas rather than formatted YAML or generated file noise. Record hashes and acquisition boundaries so an unexplained live-document change is not mistaken for a reviewed version.

Classify impact for the generated client and its actual consumers. Examples that are often breaking include removing an operation or response, changing method or path, adding a required request field or parameter, narrowing accepted input, changing a field type, removing an enum value, changing security requirements, or changing parameter serialization. A new response field may be compatible only if decoders tolerate it; a new enum value can still break exhaustive clients. A new required response field may expose a server/client rollout mismatch even when client decoding would accept it.

Do not infer compatibility solely from a generic diff tool. Account for direction: request versus response, client producer versus consumer, optionality, server rollout order, handwritten adapters, and generated public API changes.

## Update without erasing ownership

Regenerate only the intended tag, operation, or module when the tool supports stable partial generation. Review renames and deletions instead of accepting them as churn. Preserve handwritten adapters and migrate affected call sites deliberately. If generator output changes widely after only a tool upgrade, separate that migration from a contract change where practical.

Never “fix” a confirmed backend deviation by silently falsifying the canonical spec unless the contract owner approves the correction. A local compatibility adapter can be appropriate, but document the deviation, environment, evidence, and removal condition.

## Verification layers

1. Validate the complete document set and resolve all selected references.
2. Regenerate twice from clean inputs and require a stable second diff.
3. Run the repository's formatter, analyzer, generator checks, and unit tests.
4. Test request method, path, parameter encoding, headers, body and media type against a fake transport or mock server.
5. Test every selected documented response class, malformed payloads, unknown enum or variant behavior, empty bodies, and binary or multipart paths where applicable.
6. Compile representative consumers and verify handwritten mapping or repository behavior.
7. Use an authorized non-production service only when live conformance is in scope; start with safe read-only operations and obtain explicit authorization before mutations.

Report separately what the spec declares, what generated code compiles, what mocks prove, and what a deployed backend actually returned. None of those layers alone proves the others.

## Sources

- [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html)
- [Flutter JSON serialization](https://docs.flutter.dev/data-and-backend/serialization/json)
