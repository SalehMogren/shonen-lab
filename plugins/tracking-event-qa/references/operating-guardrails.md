# Operating guardrails

These boundaries are shared by profile setup and event verification.

## Data boundary

- Profiles contain routing, field mappings, platform values, channel routing, and thresholds. Authentication stays in the connected provider.
- Reports and write-backs use aggregate evidence. Keep credentials, cookies, raw customer payloads, and credential references out of profiles, Notion, Jira, and chat output.
- When evidence must be shown, redact sensitive values and include only the fields needed to support the verdict.
- Event-stream rows hold raw property values, including page URLs with query strings, contact details, and discount codes. Summarize them; never paste raw rows into a report. When a query surfaces a property that should not be collected at all, report the finding as a privacy defect rather than quoting the values.

## Channel boundary

- The tracking plan's routing column is the contract for which channels an event belongs to. Observed traffic proves compliance; it does not redefine the requirement.
- When the column and the observed channels disagree, report both and stop. Changing the column is a human decision, and the traffic may be the defect.
- A channel the plugin cannot query leaves the cell partially verified. Say which channel is unproven instead of implying the whole row passed.

## Authority boundary

- Setup authorizes reads from the named sources and a local non-secret profile write. A Notion schema change requires separate authorization.
- Verification authorizes reads and a report. Notion write-back requires an explicit request or confirmation after the change preview.
- Jira creation is a separate action and requires an explicit request.

## Scope boundary

- The active profile is the only routing source. A mismatched database or inaccessible project stops the run at the relevant gate.
- Write-back may change only the QA-marked platform status, last verified value, verification note, and reproduce link shown in the preview.
- Assignees and unrelated workflow states remain unchanged.
