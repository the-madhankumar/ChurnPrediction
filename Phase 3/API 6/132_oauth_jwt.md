### API Key vs OAuth2/JWT

1. **API Key**

   * Simple static secret.
   * Sent in `X-API-Key` header.
   * Easy to implement.
   * Usually identifies the application/client.
   * No built-in user identity or permissions.
   * Harder to rotate securely if widely distributed.

2. **OAuth2/JWT**

   * Uses authentication/authorization flows.
   * JWT contains claims such as user ID, roles, and expiry.
   * Supports user-level authentication.
   * Can implement role/permission-based access.
   * Tokens can have short expiration times.

### What changes in production?

* Use **HTTPS** everywhere.
* Store secrets in a **secret manager**, not `.env` committed to Git.
* Use **short-lived JWT access tokens**.
* Implement **refresh tokens** where appropriate.
* Add **roles/scopes/permissions**.
* Support **key rotation**.
* Add **rate limiting**.
* Log authentication failures.
* Never log API keys or JWTs.
* Use proper OAuth2/OIDC provider if user authentication is required.
* Validate token **signature, issuer, audience, and expiration**.
