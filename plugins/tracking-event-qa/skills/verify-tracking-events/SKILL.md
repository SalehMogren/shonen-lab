---
name: verify-tracking-events
description: Verify tracking-plan event/platform cells marked QA against real PostHog traffic, classify them with evidence, and update the configured Notion tracking plan. Use for analytics QA, instrumentation audits, checking whether events are live, or moving tracking statuses from QA to Live.
---

# Verify Tracking Events

Verify each configured **event × platform** cell marked QA against observed PostHog traffic. Produce an evidence-backed report and, when authorized and supported, write the result back to the configured Notion tracking plan.

## Load the profile

1. Run `python3 ../../scripts/manage_profiles.py show` from this skill directory, or pass `--name <profile>` when the user specifies a profile.
2. If there is no profile, perform the essential first-run flow from `$setup-tracking-event-qa` before querying data. Do not fall back to a hardcoded product, squad, Notion database, or PostHog project.
3. State the selected profile and thresholds at the start of the report.

## Verification workflow

1. Query the configured Notion source for rows whose configured App or Web status equals the configured QA value. Collect the page ID needed for write-back. Do not touch earlier workflow states.
2. Exclude non-PostHog-only rows from failure classification. Report them as out of scope.
3. Read the PostHog event taxonomy once, normalize escaped event names, and diff it against the QA list. Absent names are `Failed — never fired`; preserve any suggested-name hints.
4. Confirm the configured platform discriminator and actual values from a real event before classification.
5. Batch events in aggregate HogQL queries of roughly 30 names. Group by event and the configured platform property, returning count, first seen, and last seen within the configured lookback window.
6. Classify every QA cell using [verification-rules.md](../../references/verification-rules.md). Every verdict needs count and dates or a precise non-volume reason.
7. Present the report in this order:
   - timestamp, profile, PostHog project, lookback, exact query shape, and platform mapping;
   - recommended QA → Live table;
   - flagged results grouped by reason;
   - summary counts;
   - write-back status.

## Write-back and follow-up

- Before mutating Notion, summarize the rows and fields that will change. Treat the user's request to verify and update as authorization only for the configured verification fields.
- Change only the QA'd platform status. Set Last Verified, a concise evidence note, and a PostHog reproduce URL when the tools return one. Never assign a person automatically.
- If a write tool is unavailable, return an apply-ready update list and say that write-back was not performed.
- Offer Jira follow-up for Failed results. Create Jira issues only when the user explicitly asks, using the configured project key if present.
- Never store or expose credentials in Notion, reports, Jira, or the local profile.

## Required judgment

- Wrong-platform evidence takes precedence over low volume.
- Treat failure-path events (`*_failed`, `*_error`) with extra scrutiny.
- Low-volume events can include internal or tester traffic; flag them for a sanity check before interpreting them as healthy product usage.
- A database link that does not contain event names and per-platform QA statuses is the wrong source. Stop and request the correct source rather than verifying unrelated content.
