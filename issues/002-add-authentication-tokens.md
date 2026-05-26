Title: Add authentication and token-based API access

Description:
Introduce authentication for signups and administrative actions. Support session-based login for web UI and token-based authentication (e.g., DRF Token or JWT) for API clients.

Why:
- Prevent unauthorized signups/edits
- Support programmatic clients and mobile apps

Acceptance criteria:
- Login/logout endpoints for admin users
- Token issuance endpoint for API clients
- Protected endpoints for signup/unregister/admin actions

Labels: security, enhancement
