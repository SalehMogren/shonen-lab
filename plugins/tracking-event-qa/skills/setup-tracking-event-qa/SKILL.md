---
name: setup-tracking-event-qa
description: Configure or switch a reusable squad/product profile for tracking-event QA by connecting a Notion tracking database to a PostHog project, with optional Jira follow-up settings. Use when setting up, configuring, onboarding, changing, or listing tracking QA profiles.
---

# Set Up Tracking Event QA

Create a reusable, non-secret profile for a squad and product. A profile points the verifier to the correct Notion tracking database and PostHog project and records the database field mappings and acceptance thresholds.

## Boundaries

- Never store access tokens, API keys, passwords, cookies, or credential references in the profile.
- Use the user's already connected Notion, PostHog, and optional Jira tools. If a required connector is unavailable, explain which connection is missing and stop before saving an unverified profile.
- Jira is optional and is only used after verification when the user explicitly asks to create follow-up work.
- Do not change the Notion database schema during setup unless the user separately authorizes that change.

## First-run setup

1. Run `python3 ../../scripts/manage_profiles.py list --json` from this skill directory.
2. Ask for any missing essentials in one compact prompt:
   - profile name in lowercase hyphen-case;
   - squad name and product name;
   - Notion database/data-source URL or ID;
   - PostHog project name and ID;
   - optional Jira project key.
3. Fetch the Notion source and confirm that it is the database containing one row per tracking event. Inspect its schema and detect these roles:
   - event name;
   - App and/or Web status;
   - tracking platform/provider;
   - assignee, last verified, verification note, and PostHog reproduce link when present.
4. Confirm PostHog access to the selected project. Read the event schema once and inspect a real event's platform property. Prefer `$lib`, but use the verified property/value mapping if the project differs.
5. Show the detected mapping and the default thresholds before saving:
   - 90-day lookback;
   - last seen within 14 days;
   - at least 10 events for the standard Live verdict.
   Ask only about ambiguous mappings or requested threshold changes.
6. Save and activate the profile with `python3 ../../scripts/manage_profiles.py save ... --activate`, passing the confirmed field names. The command stores the profile at `~/.config/tracking-event-qa/profiles.json` with restrictive file permissions.
7. Run `python3 ../../scripts/manage_profiles.py validate`, then report the profile name, source, project, field mapping, thresholds, and whether Jira is configured.

## Multiple products or squads

Create one profile per product/squad combination. Use `list`, `show`, and `activate` to inspect or switch profiles. Do not overwrite another profile unless the user asks to update that named profile.

For the exact profile fields and command example, read [profile-schema.md](../../references/profile-schema.md).
