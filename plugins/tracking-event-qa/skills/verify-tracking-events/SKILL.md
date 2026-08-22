---
name: verify-tracking-events
description: Verify Notion tracking-plan cells marked QA against observed PostHog traffic, classify every event/platform result with evidence, and optionally write scoped results back. Use for analytics QA, instrumentation audits, event launch checks, or QA-to-Live review.
---

# Verify Tracking Events

A **cell** is one event × platform status marked QA. Verification is complete only when every in-scope cell has one evidence-backed verdict.

Read [operating-guardrails.md](../../references/operating-guardrails.md) before connector calls or writes. Read [verification-rules.md](../../references/verification-rules.md) before classification.

## Profile gate

1. Run `python3 ../../scripts/manage_profiles.py show` from this skill directory, or pass `--name <profile>` when the user names one.
2. When no valid profile exists, invoke `setup-tracking-event-qa`; the verifier has no implicit fallback source.
3. State the selected squad/product, Notion source, PostHog project, platform mapping, and thresholds.

The profile gate passes when the selected profile validates and both configured sources are accessible.

## Evidence gate

1. Query the configured Notion source for App/Web cells whose status equals the profile's QA value. Preserve each page ID for possible write-back.
2. Separate non-PostHog-only cells as `Unverifiable`; they are outside the PostHog proof path.
3. Read the event taxonomy once, normalize escaped event names, and diff it against the QA event names.
4. Reconfirm the configured platform property and values against a real event.
5. Batch aggregate queries by roughly 30 event names. Return event name, platform value, count, first seen, and last seen within the configured lookback.
6. Apply the verdict precedence and evidence contract in `verification-rules.md` to every cell.

The evidence gate passes when every in-scope cell has exactly one verdict plus count and dates, or a precise non-volume reason. Present the profile, timestamp, query shape, platform mapping, Live candidates, flagged cells by reason, and summary counts.

## Write gate

1. Preview the exact pages, properties, old values, and new values.
2. Apply only the authorized fields after explicit confirmation.
3. Re-read changed rows and report the confirmed values. When writes are unavailable, return an apply-ready change list.
4. Offer optional Jira follow-up for failed cells; create issues only after a separate explicit request.

The write gate passes when every intended row is re-read successfully, unrelated fields remain untouched, and failures or unavailable writes are reported precisely.
