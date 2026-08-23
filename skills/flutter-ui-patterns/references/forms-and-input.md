# Forms and input

Design form behavior as a stateful user flow, not a collection of text fields.

## Ownership

Choose `Form`, individual `FormField`s, controllers, or the project's established form abstraction according to coordination needs. Keep `GlobalKey`, `TextEditingController`, `FocusNode`, and subscriptions in stable lifecycle ownership; never create them during `build`.

Do not duplicate the same value across controllers, widget state, and feature state without defining the source of truth and synchronization direction. Preserve user input across harmless rebuilds and expected navigation or restoration flows.

## Input semantics

Configure labels, hints, keyboard type, input action, capitalization, autofill hints, obscuring, formatting, and semantic context from the meaning of the field. Hints do not replace persistent labels.

Use input formatters only for constraints that are valid while typing. Do not block intermediate text states required by an input method editor, locale, decimal entry, composition, or paste operation.

## Validation

Separate local format checks from remote or business validation. Choose when errors appear—on submit, after interaction, on blur, or asynchronously—so users are not punished while entering valid intermediate input.

Place an error near the affected field, keep its text actionable, preserve layout where practical, and move focus or announce the first invalid field when that improves recovery. Do not encode invalid state by color alone.

Handle server field errors, whole-form errors, stale asynchronous validation, and changed input after a response. A successful client validator does not replace server validation.

Represent asynchronous validation as distinct valid, invalid, failed, and stale or cancelled outcomes. Never encode a stale result as `null` or another value that the submit path interprets as valid. Snapshot the submitted values and abort that attempt if relevant input changes before validation completes.

Every stale, cancelled, invalid, failed, and successful path must leave the visible form state retryable or hand ownership to a newer operation. When input invalidates an in-flight check, return validating/submitting state to idle and re-enable submission; use an operation identity so an older completion cannot clear the busy state owned by a newer attempt.

## Submission

Define idle, validating, submitting, success, recoverable failure, and terminal failure states. Prevent accidental duplicate submissions while preserving deliberate retry. Keep entered data after recoverable failure and avoid clearing a form before durable success.

Acquire the submission guard before the first asynchronous validation or save operation, and release it on every terminal path. Disabling a button only after an `await` leaves a window where repeated taps can start duplicate operations. Map server field errors back to the relevant field and reserve whole-form errors for failures that are not attributable to one input.

For non-idempotent operations, coordinate duplicate protection with the data and networking layers rather than relying only on a disabled button.

## Focus and keyboard

Use logical traversal order, visible focus, appropriate next/done actions, and keyboard dismissal that does not make errors unreachable. Verify hardware keyboard, screen reader, autofill, paste, and platform input-method behavior where supported.

## Verification

Test valid and invalid input, empty and long values, locale-specific input, paste, autofill, focus traversal, keyboard submission, asynchronous race ordering, input changes during validation, duplicate taps before the first await completes, server field errors, retry, restoration, text scaling, and disposal relevant to the form. When the user asks to build the form, deliver the focused regression tests with the implementation instead of only listing them as future work.

For an asynchronously validated profile-style form, the minimum regression set should prove that the first invalid or server-rejected field receives focus, a recoverable failure retains input and can retry successfully, changing input makes an older response harmless, repeated taps start one operation, and disposal with validation or submission pending causes no callback or exception after teardown.
