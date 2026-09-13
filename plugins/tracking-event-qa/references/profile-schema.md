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
        "plan_channel_value": "Posthog",
        "thresholds": {
          "lookback_days": 90,
          "recency_days": 14,
          "live_volume": 10
        }
      },
      "stream": {
        "provider": "event-stream",
        "dataset": "product-events",
        "event_name_field": "event_name",
        "event_id_field": "event_id",
        "property_key_field": "data_key",
        "property_value_field": "string_value",
        "platform_field": "source",
        "platform_values": {
          "web": ["example.test"],
          "app": ["app.example.test"]
        },
        "property_key_prefixes": {
          "web": "attributes.",
          "app": ""
        },
        "excluded_platform_values": ["staging.example.test", "localhost"],
        "plan_channel_value": "Stream"
      },
      "jira": {
        "project_key": null,
        "issue_type": "Task"
      }
    }
  }
}
```

## The stream channel

`stream` is optional. Omit it when every event the plan tracks is verifiable in product analytics; configure it when the plan routes some events to a second destination such as a log-analytics dataset, warehouse table, or recommendation pipeline. See [channel-verification.md](channel-verification.md) for how the verifier uses it.

| Field | Meaning |
| --- | --- |
| `dataset` | Dataset, index, or table holding the stream |
| `event_name_field` / `event_id_field` | Event name, and the identifier counted with a distinct count |
| `property_key_field` / `property_value_field` | Set both for key/value streams; omit both when each property is its own column |
| `platform_field` + `platform_values` | How the stream separates platforms, e.g. a site or host field |
| `property_key_prefixes` | Per-platform property-name prefixes, when clients spell the same property differently |
| `excluded_platform_values` | Staging, preview, or local values to keep out of every query |
| `plan_channel_value` | The tracking-plan value that routes an event to this channel |

`plan_channel_value` on both channels is what turns the plan's routing column into a required-channel list. Validation rejects an excluded value that is also mapped to a platform, a key field without a value field, and any platform name outside `web`, `app`, and `backend`.

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
  --analytics-plan-value "Posthog" \
  --stream-dataset "product-events" \
  --stream-platform-field "source" \
  --stream-platform-values-json '{"web":["example.test"],"app":["app.example.test"]}' \
  --stream-property-key-field "data_key" \
  --stream-property-value-field "string_value" \
  --stream-key-prefixes-json '{"web":"attributes.","app":""}' \
  --stream-excluded-values "staging.example.test,localhost" \
  --stream-plan-value "Stream" \
  --activate
```

Drop every `--stream-*` flag to configure product analytics only. `save` refuses to overwrite an existing name; add `--replace` only after the replacement has been confirmed.

Use `list`, `show`, `activate`, and `validate` for profile inspection and switching. `list` marks which profiles carry a stream channel, and `validate` reports how many do.
