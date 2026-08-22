# Tracking Event QA

A reusable workflow for product managers, product engineers, software engineers, QA engineers, and analytics teams to verify tracking events against PostHog and write evidence back to a Notion tracking plan.

## Requirements

- Connected Notion and PostHog providers.
- Optional connected Jira provider for follow-up work.
- Python 3 for the bundled profile manager.

Authentication remains with the connected providers. The plugin saves no credentials.

## First-time setup

Run `$setup-tracking-event-qa` and provide a profile name, squad, product, Notion source, PostHog project, and optional Jira project key. The setup skill detects field and platform mappings before saving non-secret configuration to `~/.config/tracking-event-qa/profiles.json`.

Create a separate profile for each squad/product pair. No database, project, product, or organization is hardcoded.

## Verification

Run `$verify-tracking-events`. The skill finds tracking-plan cells marked `QA`, queries observed PostHog traffic, presents evidence for every event/platform result, and previews the scoped Notion changes.

Default thresholds are a 90-day lookback, activity within 14 days, and at least 10 matching events for the standard Live verdict. Setup can override them per profile.

## Safety boundaries

- Only configured verification fields are eligible for write-back.
- Jira follow-up is optional and requires explicit user authorization.
- Credentials, event payloads, and customer data are never written to profiles, reports, Notion, or Jira.
