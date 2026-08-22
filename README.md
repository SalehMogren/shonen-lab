# Shonen Lab

A growing lab of reusable Codex plugins and skills that help product managers, product engineers, software engineers, QA engineers, and other cross-functional roles level up their everyday work.

The repository is intentionally organization-independent. Plugins must not hardcode company names, internal URLs, database IDs, project IDs, credentials, customer data, or product-specific assumptions. Any required workspace configuration belongs in an explicit first-run setup flow.

## Plugin catalog

| Plugin | Who can use it | Purpose |
| --- | --- | --- |
| [Tracking Event QA](plugins/tracking-event-qa/README.md) | PM, PE, SWE, QA, Analytics | Verify tracking-plan events against PostHog and record evidence in Notion. |

## Install the marketplace

Replace `<owner>` and `<repository>` with the GitHub location used by your team:

```bash
codex plugin marketplace add <owner>/<repository> --ref main
codex plugin add tracking-event-qa@shonen-lab
```

Start a new Codex task after installing or updating a plugin so its skills and tools are loaded.

## Repository structure

```text
.agents/plugins/marketplace.json    Marketplace catalog
plugins/<plugin-name>/              One self-contained plugin per directory
  .codex-plugin/plugin.json         Plugin manifest
  skills/                           Optional reusable skills
  scripts/                          Optional helper scripts
  references/                       Optional operating rules
```

## Adding another plugin

1. Create a normalized lower-case, hyphenated plugin directory under `plugins/`.
2. Add and validate its `.codex-plugin/plugin.json` manifest.
3. Add reusable skills, scripts, references, MCP configuration, or apps only when required.
4. Add the plugin to `.agents/plugins/marketplace.json` with installation and authentication policies.
5. Document requirements, first-run setup, data handling, and verification steps.
6. Run secret and organization-specific-content scans before opening a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the review checklist and [SECURITY.md](SECURITY.md) for data-handling rules.
