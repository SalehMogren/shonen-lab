# Verification rules

Apply these defaults from the active profile to each QA-marked event × platform cell.

| Verdict | Criteria | Status action |
|---|---|---|
| Live | Count meets the Live threshold and last seen is within the recency window | Change QA to Live |
| Live (low volume) | 2 or more events, below the Live threshold, and recent | Change QA to Live; flag for sanity check |
| Failed — never fired | Event is absent from the PostHog taxonomy | Leave/mark Failed and include naming hints |
| Failed — wrong platform | Zero on the QA'd platform and positive volume elsewhere | Leave/mark Failed; name the observed platform |
| Failed — single fire | Exactly one event in the lookback | Leave/mark Failed; include its date |
| Failed — stale | At least two events but last seen before the recency threshold | Leave/mark Failed; include last seen |
| Unverifiable | No concrete event name/property filter, or non-PostHog-only tracking | Do not mark Failed; state what is missing |

The default profile uses a 90-day lookback, a 14-day recency window, and a Live threshold of 10 events. These are configurable. When a deliberately rare event warrants judgment outside the thresholds, explain the deviation explicitly.

The aggregate query should return event, configured platform property, count, minimum timestamp, and maximum timestamp; group by event and platform. Batch roughly 30 event names per query and preserve the PostHog reproduce link when available.
