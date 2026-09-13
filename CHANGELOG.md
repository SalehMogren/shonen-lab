# Marketplace changelog

## 0.3.0 — 2026-09-13

- Added multi-channel verification: a tracking plan can route an event to product analytics, to a second event stream, or to both.
- Added a channel gate that resolves required and excluded channels from the plan's routing column before any volume query.
- Added wrong-channel and value-mismatch verdicts, and made channel evidence outrank volume evidence.
- Added optional stream-channel configuration for key/value datasets, per-platform property prefixes, and excluded staging hosts.
- Added value-parity checks across platforms, so matching property names alone no longer qualify a cell for Live.
- Added a privacy boundary for raw stream rows and a rule against rewriting the plan's routing column to match observed traffic.

## 0.2.0 — 2026-08-22

- Added source, evidence, save, and write completion gates.
- Centralized shared data, authority, and scope boundaries.
- Added observed PostHog platform mappings to profile setup.
- Added overwrite protection and profile-manager tests.
- Clarified verdict precedence and low-volume handling.

## 0.1.0 — 2026-08-22

- Created a generic multi-plugin marketplace structure.
- Named the marketplace Shonen Lab.
- Added Tracking Event QA as the first reusable plugin.
- Added contribution and security guidance for cross-functional teams.
