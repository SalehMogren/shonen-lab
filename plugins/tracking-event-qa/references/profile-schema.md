# Profile schema

Profiles live at `~/.config/tracking-event-qa/profiles.json` with file mode `0600`. The store contains non-secret configuration only.

## Shape

```json
{
  "version": 1,
  "active_profile": "product-squad",
  "profiles": {
    "product-squad": {
      "squad": "Squad Name",
      "product": "Product Name",
      "notion": {
        "source": "collection://data-source-id",
        "event_name_property": "Event Name",
        "app_status_property": "App Status",
        "web_status_property": "Web Status",
        "tracking_platform_property": "Tracking Platform",
        "assignee_property": "Assignee",
        "last_verified_property": "Last Verified",
        "verification_note_property": "Verification Note",
        "reproduce_link_property": "PostHog Reproduce Link",
        "qa_value": "QA",
        "live_value": "Live"
      },
      "posthog": {
        "project_name": "Product Analytics",
        "project_id": "12345",
        "platform_property": "$lib",
        "platform_values": {
          "web": ["web"],
          "app": ["mobile-sdk"]
        },
        "thresholds": {
          "lookback_days": 90,
          "recency_days": 14,
          "live_volume": 10
        }
      },
      "jira": {
        "project_key": null,
        "issue_type": "Task"
      }
    }
  }
}
```

## Save command

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
  --platform-property '$lib' \
  --platform-values-json '{"web":["web"],"app":["mobile-sdk"]}' \
  --activate
```

`save` refuses to overwrite an existing name. Add `--replace` only after the replacement has been confirmed.

Use `list`, `show`, `activate`, and `validate` for profile inspection and switching.
