# Tracking Event QA

A reusable workflow for product managers, product engineers, software engineers, QA engineers, and analytics teams to verify tracking events against the channels a plan routes them to, and write evidence back to a Notion tracking plan.

## Requirements

- Connected Notion and PostHog providers.
- Optional connected event-stream provider (a log-analytics dataset, warehouse table, or pipeline) when the plan routes events away from product analytics.
- Optional connected Jira provider for follow-up work.
- Python 3 for the bundled profile manager.

Authentication remains with the connected providers. The plugin saves no credentials.

## First-time setup

Run `$setup-tracking-event-qa` and provide a profile name, squad, product, Notion source, product-analytics project, optional stream channel, and optional Jira project key. The setup skill detects field, platform, and channel mappings before saving non-secret configuration to `~/.config/tracking-event-qa/profiles.json`.

Create a separate profile for each squad/product pair. No database, project, product, or organization is hardcoded.

## Verification

Run `$verify-tracking-events`. The skill finds tracking-plan cells marked `QA`, resolves which channels each event is required to reach, queries observed traffic on each of them, presents evidence for every event/platform result, and previews the scoped Notion changes.

The workflow uses explicit gates:

- **Source gate:** the Notion schema and observed platform values agree with the profile.
- **Channel gate:** every QA cell gets a required-channel and excluded-channel list from the plan's routing column.
- **Evidence gate:** every QA-marked event × platform cell receives one verdict with supporting evidence per channel.
- **Write gate:** exact field changes are previewed, authorized, applied, and re-read.

Default thresholds are a 90-day lookback, activity within 14 days, and at least 10 matching events for the standard Live verdict. Setup can override them per profile.

## Two channels, not one

Plans often send high-volume events to a second destination and keep product analytics for funnels and experiments. That changes what "verified" means:

- An event routed away from product analytics is **absent there by design** — absence is not a failure.
- An event that still reaches a channel the plan excludes is a **routing defect**, however healthy its volume looks.
- Key/value streams store one row per property, so events are counted with a distinct count of the event identifier, and property names may carry a per-platform prefix.
- Staging, preview, and local traffic share the dataset and must be excluded explicitly.

See [references/channel-verification.md](references/channel-verification.md).

## Values, not just keys

A cell stays at QA when the property names are right but the values are not: platforms using different vocabularies for the same property, a value read from a neighbouring field, or a property that holds one constant across the entire window. Those checks are in [references/verification-rules.md](references/verification-rules.md).

## Safety boundaries

- Only configured verification fields are eligible for write-back.
- The plan's routing column is never rewritten to match observed traffic; conflicts are reported for a human to decide.
- Jira follow-up is optional and requires explicit user authorization.
- Credentials, raw event payloads, and customer data are never written to profiles, reports, Notion, or Jira.

## Development

Run the profile-manager feedback loop with:

```bash
python3 -m unittest discover -s tests -v
```
