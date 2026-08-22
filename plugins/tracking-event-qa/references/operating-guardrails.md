# Operating guardrails

These boundaries are shared by profile setup and event verification.

## Data boundary

- Profiles contain routing, field mappings, platform values, and thresholds. Authentication stays in the connected provider.
- Reports and write-backs use aggregate evidence. Keep credentials, cookies, raw customer payloads, and credential references out of profiles, Notion, Jira, and chat output.
- When evidence must be shown, redact sensitive values and include only the fields needed to support the verdict.

## Authority boundary

- Setup authorizes reads from the named sources and a local non-secret profile write. A Notion schema change requires separate authorization.
- Verification authorizes reads and a report. Notion write-back requires an explicit request or confirmation after the change preview.
- Jira creation is a separate action and requires an explicit request.

## Scope boundary

- The active profile is the only routing source. A mismatched database or inaccessible project stops the run at the relevant gate.
- Write-back may change only the QA-marked platform status, last verified value, verification note, and reproduce link shown in the preview.
- Assignees and unrelated workflow states remain unchanged.
