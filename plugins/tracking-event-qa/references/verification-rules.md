# Verification rules

Apply the active profile to each QA-marked **cell** in this precedence order. Stop at the first matching verdict.

A cell is one event × platform status marked QA. When the profile configures a stream channel, read [channel-verification.md](channel-verification.md) first: the required channels come from the plan's tracking-platform column, and absence from product analytics can be correct.

| Order | Verdict | Proof | Status action |
| --- | --- | --- | --- |
| 1 | Unverifiable | No concrete event/property filter, tracking routed only to channels this plugin cannot query, or unresolved source mapping | Keep QA; state the missing proof |
| 2 | Failed: never fired | Event is absent from every required channel's taxonomy or dataset | Keep QA; include naming hints |
| 3 | Failed: wrong channel | Zero on a required channel, or present on a channel the plan excludes | Keep QA; name the channel and the observed volume |
| 4 | Failed: wrong platform | Zero on the QA platform and positive volume on another mapped platform | Keep QA; name the observed platform |
| 5 | Failed: no traffic | Event exists but has zero traffic on all mapped platforms in the lookback | Keep QA; include the lookback |
| 6 | Failed: single fire | Exactly one matching event in the lookback | Keep QA; include its date |
| 7 | Failed: stale | At least two matches, but last seen is older than the recency window | Keep QA; include last seen |
| 8 | Review: value mismatch | Required channels and volume pass, but a property is unusable: platforms disagree on the value or the field carrying it, a value comes from the wrong source, or one distinct value covers the whole window | Keep QA; name the property, both observed values, and which side matches the plan |
| 9 | Review: low volume | At least two recent matches on the required channels, below the Live threshold | Keep QA; request a sanity check |
| 10 | Live | Required channels satisfied with no excluded-channel traffic, count meets the Live threshold, last seen within the recency window, and values match the plan | Eligible for QA → Live |

## Evidence contract

Every volume verdict includes count, first seen, last seen, lookback, platform property, matched platform value, and — when a stream channel is configured — the per-channel result and any excluded host or environment values. Non-volume verdicts name the missing or conflicting proof.

Wrong-channel evidence outranks wrong-platform, which outranks volume: an event reaching a channel the plan excludes is a routing defect no amount of volume redeems. Failure-path events such as `*_failed` or `*_error` require the same proof as any other cell.

The aggregate query groups by event and platform and returns count, minimum timestamp, and maximum timestamp. Batch roughly 30 event names per query, count distinct event identifiers on key/value streams, and preserve a reproduce link when the connector returns one.

A deliberately rare event may justify a threshold exception, but the report must label it as a human override. It is not automatically eligible for write-back.

## Value checks before Live

Before flipping any cell, confirm for that event:

- Every property the plan lists is present, and nothing unexpected beyond SDK and campaign parameters.
- Enum properties carry values from the plan's enum, not a neighbouring field's values.
- Identity properties are stable and semantic, not synthesised from a database primary key, and two identity fields do not carry the same value.
- No property is null, or a single constant, across the whole window unless the plan declares it blocked.
- Cross-platform properties use one vocabulary.
- No credential, discount code, raw user input, or URL query string is present.
