---
name: verify-tracking-events
description: Verify Notion tracking-plan cells marked QA against observed traffic in product analytics and any configured event-stream channel, classify every event/platform result with evidence, and optionally write scoped results back. Use for analytics QA, instrumentation audits, event launch checks, channel-routing checks, or QA-to-Live review.
---

# Verify Tracking Events

A **cell** is one event × platform status marked QA. Verification is complete only when every in-scope cell has one evidence-backed verdict.

Read [operating-guardrails.md](../../references/operating-guardrails.md) before connector calls or writes. Read [verification-rules.md](../../references/verification-rules.md) before classification. When the profile configures a stream channel, read [channel-verification.md](../../references/channel-verification.md) before querying it.

## Profile gate

1. Run `python3 ../../scripts/manage_profiles.py show` from this skill directory, or pass `--name <profile>` when the user names one.
2. When no valid profile exists, invoke `setup-tracking-event-qa`; the verifier has no implicit fallback source.
3. State the selected squad/product, Notion source, product-analytics project, stream dataset when configured, platform mappings, and thresholds.

The profile gate passes when the selected profile validates and every configured source is accessible.

## Channel gate

1. Read the plan's tracking-platform value for each QA cell and resolve it to required channels using `plan_channel_value` on each configured channel.
2. Treat values that map to no configured channel as outside the proof path; the cell can only ever be partially verified, and the report must say which channel was not proven.
3. Record, per cell, the channels that are required and the channels the plan excludes. An event routed away from product analytics is expected to be absent there.

The channel gate passes when every in-scope cell has a required-channel list and an excluded-channel list before any volume query runs.

## Evidence gate

1. Query the configured Notion source for App/Web cells whose status equals the profile's QA value. Preserve each page ID for possible write-back.
2. Read the event taxonomy once, normalize escaped event names, and diff it against the QA event names.
3. Reconfirm the configured platform property and values against a real event, on each channel in use.
4. Batch aggregate queries by roughly 30 event names per channel. Return event name, platform value, count, first seen, and last seen within the configured lookback. Count distinct event identifiers on key/value streams, apply the configured key prefixes, and exclude the configured non-production platform values.
5. Check every required channel for presence **and** every excluded channel for leaks.
6. For events shipping on more than one platform, compare observed property values across platforms and against the plan before considering any cell Live.
7. Apply the verdict precedence and evidence contract in `verification-rules.md` to every cell.

The evidence gate passes when every in-scope cell has exactly one verdict plus count and dates per required channel, or a precise non-volume reason. Present the profile, timestamp, query shape, platform mapping, per-channel results, Live candidates, flagged cells by reason, and summary counts.

## Write gate

1. Preview the exact pages, properties, old values, and new values.
2. Apply only the authorized fields after explicit confirmation.
3. Write the channel result and the value check into the verification note, not just the volume, so a later reader can tell a routing defect from a low-traffic event.
4. Re-read changed rows and report the confirmed values. When writes are unavailable, return an apply-ready change list.
5. Offer optional Jira follow-up for failed cells; create issues only after a separate explicit request.

The write gate passes when every intended row is re-read successfully, unrelated fields remain untouched, and failures or unavailable writes are reported precisely.
