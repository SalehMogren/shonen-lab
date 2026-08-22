# Verification rules

Apply the active profile to each QA-marked **cell** in this precedence order. Stop at the first matching verdict.

| Order | Verdict | Proof | Status action |
| --- | --- | --- | --- |
| 1 | Unverifiable | No concrete event/property filter, non-PostHog-only tracking, or unresolved source mapping | Keep QA; state the missing proof |
| 2 | Failed: never fired | Event is absent from the PostHog taxonomy | Keep QA; include naming hints |
| 3 | Failed: wrong platform | Zero on the QA platform and positive volume on another mapped platform | Keep QA; name the observed platform |
| 4 | Failed: no traffic | Event exists but has zero traffic on all mapped platforms in the lookback | Keep QA; include the lookback |
| 5 | Failed: single fire | Exactly one matching event in the lookback | Keep QA; include its date |
| 6 | Failed: stale | At least two matches, but last seen is older than the recency window | Keep QA; include last seen |
| 7 | Review: low volume | At least two recent matches, below the Live threshold | Keep QA; request a sanity check |
| 8 | Live | Count meets the Live threshold and last seen is within the recency window | Eligible for QA → Live |

## Evidence contract

Every volume verdict includes count, first seen, last seen, lookback, platform property, and matched platform value. Non-volume verdicts name the missing or conflicting proof. Wrong-platform evidence outranks volume, and failure-path events such as `*_failed` or `*_error` require the same proof as any other cell.

The aggregate query groups by event and platform and returns count, minimum timestamp, and maximum timestamp. Batch roughly 30 event names per query and preserve a PostHog reproduce link when available.

A deliberately rare event may justify a threshold exception, but the report must label it as a human override. It is not automatically eligible for write-back.
