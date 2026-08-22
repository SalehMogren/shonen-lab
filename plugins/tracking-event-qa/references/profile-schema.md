# Profile schema

Profiles are stored in `~/.config/tracking-event-qa/profiles.json`. They contain routing and field mappings only; credentials remain in the connected MCP providers.

## Required setup inputs

- profile name, squad, and product;
- Notion database/data-source URL or ID;
- PostHog project name and ID.

Jira project key is optional.

## Detected or defaulted fields

- Notion: event name, App/Web statuses, tracking platform, assignee, last verified, verification note, reproduce link, QA value, and Live value.
- PostHog: platform property/value mapping, lookback days, recency days, and Live-volume threshold.

## Save example

```bash
python3 ../../scripts/manage_profiles.py save \
  --name product-squad \
  --squad "Squad Name" \
  --product "Product Name" \
  --notion-source "collection://data-source-id" \
  --posthog-project-name "Product Analytics" \
  --posthog-project-id "12345" \
  --event-name-property "Event Name" \
  --app-status-property "App Status" \
  --web-status-property "Web Status" \
  --activate
```

Useful commands:

```bash
python3 ../../scripts/manage_profiles.py list
python3 ../../scripts/manage_profiles.py show
python3 ../../scripts/manage_profiles.py activate product-squad
python3 ../../scripts/manage_profiles.py validate
```
