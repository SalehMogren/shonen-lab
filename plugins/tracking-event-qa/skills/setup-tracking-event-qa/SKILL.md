---
name: setup-tracking-event-qa
description: Configure, inspect, switch, or repair a tracking-event QA profile that maps one squad/product to a Notion tracking plan and PostHog project. Use when onboarding the plugin, changing sources or field/platform mappings, tuning thresholds, or listing profiles.
---

# Set Up Tracking Event QA

A profile is the verifier's source of truth for routing, field mappings, platform values, and thresholds.

Read [operating-guardrails.md](../../references/operating-guardrails.md) before connector calls or profile writes. Read [profile-schema.md](../../references/profile-schema.md) when creating or changing a profile.

## Source gate

1. Run `python3 ../../scripts/manage_profiles.py list --json` from this skill directory.
2. Collect only missing inputs: profile name, squad, product, Notion source, PostHog project name and ID, and optional Jira project key.
3. Fetch the Notion source. Confirm one row represents one tracking event, then resolve the event name, App/Web status, tracking provider, verification note, last verified, and reproduce-link fields that exist.
4. Confirm access to the PostHog project. Inspect a real event to identify the platform property and the observed values for every Notion platform being configured.

The source gate passes when both sources are accessible, the Notion field roles are unambiguous, and real PostHog data proves the platform mapping. Stop at the unresolved source or mapping when it does not pass.

## Save gate

1. Show the candidate profile, including source IDs, mappings, and thresholds. Default to a 90-day lookback, 14-day recency window, and Live volume of 10.
2. Resolve ambiguous fields or requested threshold changes. A profile name already present requires explicit confirmation to replace.
3. Save and activate with `python3 ../../scripts/manage_profiles.py save ... --activate`. Pass the observed mapping through `--platform-values-json`; use `--replace` only after replacement is confirmed.
4. Run `python3 ../../scripts/manage_profiles.py validate`, then `show --name <profile>`.

The save gate passes when validation succeeds and `show` matches the confirmed source IDs, field mapping, platform values, and thresholds. Report that evidence and whether Jira is configured.

## Existing profiles

Use `list`, `show`, and `activate` to inspect or switch profiles. Keep one profile per squad/product pair so changing one product never changes another profile.
