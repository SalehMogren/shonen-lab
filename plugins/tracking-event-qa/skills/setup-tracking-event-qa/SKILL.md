---
name: setup-tracking-event-qa
description: Configure, inspect, switch, or repair a tracking-event QA profile that maps one squad/product to a Notion tracking plan, a product-analytics project, and an optional event-stream channel. Use when onboarding the plugin, changing sources or field/platform mappings, adding a second tracking channel, tuning thresholds, or listing profiles.
---

# Set Up Tracking Event QA

A profile is the verifier's source of truth for routing, field mappings, platform values, and thresholds.

Read [operating-guardrails.md](../../references/operating-guardrails.md) before connector calls or profile writes. Read [profile-schema.md](../../references/profile-schema.md) when creating or changing a profile. Read [channel-verification.md](../../references/channel-verification.md) before configuring a second channel.

## Source gate

1. Run `python3 ../../scripts/manage_profiles.py list --json` from this skill directory.
2. Collect only missing inputs: profile name, squad, product, Notion source, product-analytics project name and ID, and optional Jira project key.
3. Fetch the Notion source. Confirm one row represents one tracking event, then resolve the event name, App/Web status, tracking provider, verification note, last verified, and reproduce-link fields that exist.
4. Confirm access to the product-analytics project. Inspect a real event to identify the platform property and the observed values for every Notion platform being configured.

The source gate passes when both sources are accessible, the Notion field roles are unambiguous, and real data proves the platform mapping. Stop at the unresolved source or mapping when it does not pass.

## Channel gate

1. Read the distinct values in the plan's tracking-platform column and ask which destination each one means.
2. When a value routes events away from product analytics, configure the stream channel: dataset, event name and id fields, platform field and observed values, and the key/value fields when properties are stored as rows rather than columns.
3. Prove the mapping against real data: query one known event per platform in the stream and confirm the platform values and property spellings, including any per-platform key prefix.
4. Record which plan values map to which channel through `--analytics-plan-value` and `--stream-plan-value`, and list staging, preview, or local platform values in `--stream-excluded-values`.
5. Name the plan values that map to no configured channel, so the verifier reports them as partially verified instead of implying full proof.

The channel gate passes when every value in the tracking-platform column is either mapped to a configured channel or explicitly recorded as out of scope. Skip this gate only when the plan routes everything to product analytics.

## Save gate

1. Show the candidate profile, including source IDs, mappings, channel routing, and thresholds. Default to a 90-day lookback, 14-day recency window, and Live volume of 10.
2. Resolve ambiguous fields or requested threshold changes. A profile name already present requires explicit confirmation to replace.
3. Save and activate with `python3 ../../scripts/manage_profiles.py save ... --activate`. Pass the observed mappings through `--platform-values-json` and `--stream-platform-values-json`; use `--replace` only after replacement is confirmed.
4. Run `python3 ../../scripts/manage_profiles.py validate`, then `show --name <profile>`.

The save gate passes when validation succeeds and `show` matches the confirmed source IDs, field mapping, platform values, channel routing, and thresholds. Report that evidence, whether a stream channel is configured, and whether Jira is configured.

## Existing profiles

Use `list`, `show`, and `activate` to inspect or switch profiles. `list` marks which profiles carry a stream channel. Keep one profile per squad/product pair so changing one product never changes another profile.
