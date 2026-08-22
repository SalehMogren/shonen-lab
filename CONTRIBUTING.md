# Contributing

This marketplace is designed for reusable workflows across product management, product engineering, software engineering, QA, analytics, operations, and adjacent roles.

## Plugin requirements

- Keep the plugin independent of any company, product, squad, environment, or repository.
- Collect workspace-specific inputs through a first-run setup skill.
- Store no credentials or credential references in plugin files or local profiles.
- Declare required connectors and make optional connectors genuinely optional.
- Make write actions scoped, previewed, and attributable.
- Include deterministic validation or a documented verification procedure.
- Keep prompts understandable by every role expected to use the plugin.

## Pull request checklist

- [ ] Plugin manifest validates.
- [ ] Every skill validates.
- [ ] Setup and usage are documented.
- [ ] No company names, internal URLs, IDs, credentials, or customer data are present.
- [ ] Example values are clearly synthetic.
- [ ] Write behavior and security boundaries are documented.
- [ ] Marketplace entry includes installation, authentication, and category policies.
