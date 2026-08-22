# Security

## Data handling

Plugins in this repository must store only the minimum non-secret configuration required for their workflow. Authentication must be delegated to connected providers or an approved secret manager.

Never add credentials, cookies, access tokens, API keys, internal URLs, workspace identifiers, exported payloads, or production customer data to this repository or to a saved profile.

## Reporting an issue

Report suspected credential exposure or unsafe write behavior through the maintainers' private security channel. Do not include live secrets, internal identifiers, or customer data in a GitHub issue.
