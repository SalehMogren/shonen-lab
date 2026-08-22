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

## Skill authoring

- Choose invocation deliberately. Model-invoked skills need descriptions with distinct trigger branches; explicit-only skills need concise human-facing summaries and matching invocation policy.
- Treat the description as a context pointer: say what the skill does and when it should load, without repeating the body.
- Keep the entrypoint focused on the shared path. Put branch-specific schemas, examples, and rules behind clearly worded reference links.
- Give each consequential phase a checkable completion criterion. The agent should be able to distinguish done from almost done.
- Prefer a compact leading word for repeated behavior, such as `source gate` or `write gate`, and keep its definition in one place.
- Remove no-op advice, stale examples, and duplicated rules. Keep one source of truth for each behavior.
- Add a deterministic script when repeated mechanics benefit from one, and test the behavior the script promises.

## Pull request checklist

- [ ] Plugin manifest validates.
- [ ] Every skill validates.
- [ ] Setup and usage are documented.
- [ ] Invocation policy and trigger description agree.
- [ ] Completion criteria cover every consequential phase.
- [ ] Shared rules have one source of truth and branch-only detail is disclosed by pointers.
- [ ] No company names, internal URLs, IDs, credentials, or customer data are present.
- [ ] Example values are clearly synthetic.
- [ ] Write behavior and security boundaries are documented.
- [ ] Marketplace entry includes installation, authentication, and category policies.
