# Data Privacy and Event Contract

The event contract is designed for pseudonymous product analytics.

Do not send:
- full name
- email address
- phone number
- payment card data
- passwords/tokens
- government identifiers
- raw free-form form fields

Use opaque `user_id`, `anonymous_id`, and `session_id` identifiers. Data deletion/export requests should be implemented against the canonical data lake using governed identity-mapping processes outside this demo event contract.
