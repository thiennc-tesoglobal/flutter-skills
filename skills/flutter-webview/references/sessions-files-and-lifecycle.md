# Sessions, files, and lifecycle

## Website data and accounts

Identify whether the selected platform implementation uses a persistent, non-persistent, shared, or isolated website data store. Define cookie seeding and update order, third-party cookie policy, storage partitioning, cache behavior, and ownership between the page, application session, and backend.

Logout is a coordinated transition. Revoke or end the application session as required, stop old page work, clear the intended cookies and website data, remove account-bound cached content, and prevent a delayed callback from restoring the old identity. For account switching, bind page and bridge results to an account generation rather than whichever account is current when a callback arrives. Avoid clearing unrelated site data when the platform offers scoped removal, but state package limitations honestly.

## Files, downloads, and external content

Treat file chooser results and downloads as untrusted inputs. Preserve cancellation, accept and capture intent, multiplicity, size and type limits, URI access lifetime, and platform permission behavior. Validate content based on the consuming feature rather than trusting only a filename, extension, MIME declaration, or page request.

Define whether a download belongs to the WebView, app networking layer, system browser, or download manager. Do not forward cookies, authorization headers, or referrers to an arbitrary destination. Use app-private or user-selected storage appropriate to the platform, expose progress and cancellation when required, and clean partial sensitive files.

## Lifecycle ownership

Create controller ownership outside repeated widget builds and dispose subscriptions, delegates, timers, and message ownership with the screen. Define restoration after rotation, memory pressure, backgrounding, renderer termination, and process recreation. Do not promise preservation the selected plugin or platform cannot provide; restore from safe application state instead of replaying privileged page actions blindly.

## Verification

Exercise first launch, warm return, background and resume, rotation where relevant, renderer or process recreation, logout, account switch, cookie expiry, offline startup, file accept and cancellation, malformed content, download redirect, permission denial, and disposal during asynchronous callbacks. Use real supported runtimes for cookie stores, platform pickers, downloads, and lifecycle callbacks.

## Sources

- [webview_flutter WebViewCookieManager](https://pub.dev/documentation/webview_flutter/latest/webview_flutter/WebViewCookieManager-class.html)
- [Android CookieManager](https://developer.android.com/reference/android/webkit/CookieManager)
- [Android WebChromeClient file chooser](https://developer.android.com/reference/android/webkit/WebChromeClient#onShowFileChooser(android.webkit.WebView,android.webkit.ValueCallback%3Candroid.net.Uri%5B%5D%3E,android.webkit.WebChromeClient.FileChooserParams))
- [Apple WKWebsiteDataStore](https://developer.apple.com/documentation/webkit/wkwebsitedatastore)
