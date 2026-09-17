# Channel verification

Many tracking plans route an event to more than one destination: product analytics for funnels and experiments, and a higher-volume **event stream** (a log-analytics dataset, warehouse table, or recommendation pipeline) for everything too expensive to keep in analytics. A cell is only verified when the event fires **on the channels the plan requires, and nowhere it was deliberately excluded from**.

This reference covers the stream channel. Product-analytics querying is unchanged.

## Why a stream channel changes the verdict

An event routed away from product analytics is **absent from PostHog by design**. Without channel awareness, a verifier reads that absence as "never fired" and flags a healthy event. The reverse is just as damaging: an event marked stream-only that still reaches product analytics is a live billing and double-counting problem that volume checks never surface.

So each cell carries two questions:

1. Does it fire at all, on the required channels, with enough recent volume?
2. Does it fire **only** on the channels the plan allows?

## Reading the plan's routing column

The tracking-platform column is the contract. Map each value to a channel with `plan_channel_value` in the profile (`posthog.plan_channel_value`, `stream.plan_channel_value`). Values that map to neither, such as a marketing tag manager or a CRM, stay `Unverifiable` — say which channel could not be proven rather than implying the row passed.

When the column and the code disagree, report both and let a human decide which is wrong. Do not silently rewrite the column to match observed traffic: the column is a decision record, and the traffic may be the bug.

## Querying a key/value stream

Streams often store one header row per event plus one row per property, rather than a column per property. Set `property_key_field` and `property_value_field` when that is the shape. Then:

- **Count events, not rows.** Use a distinct count of `event_id_field`. `count()` multiplies by the number of properties.
- **Property names can be prefixed per platform.** One client may send `attributes.section_key` while another sends `section_key`. Configure `property_key_prefixes` and filter on both spellings, or the platform with the other spelling silently returns zero.
- **Header rows carry the identifiers.** Organization, platform and user fields usually appear on the header row and are empty on property rows, so a filter such as `org != X` will drop property rows too. Filter on the header row when checking ownership.
- **Exclude non-production hosts.** Streams keyed by site or host collect staging, preview and local traffic. Put those values in `excluded_platform_values` and state the exclusion in the report.
- **Shared datasets hold other teams' traffic.** Confirm the events you count belong to the configured product before trusting any total.

## Value parity across platforms

Channel and volume checks pass while the payload is still unusable. For every event that ships on more than one platform, compare the values, not just the property names:

- **Same property, different vocabulary.** One client sends `ordersTab`, the other `orders`. Both are valid; grouping them is not. Report it as a value mismatch and name both spellings.
- **Same property, different field.** A readable key on one platform and an internal id on the other, or the same value in two different fields. Grouping across platforms silently returns two answers.
- **Same wrong value on both.** Sourced from a neighbouring field, hardcoded, or null on every event. Key-presence checks pass; the breakdown built on it is empty. A property that has exactly one distinct value across the whole window is the tell.
- **Different trigger for the same name.** A view counted before the section is on screen on one platform and at 50% visibility on the other makes any rate incomparable. Read the emitter when the counts disagree by an order of magnitude.

Value mismatches keep a cell at QA. They are not "Live with a note": a metric no one can group is not verified.

## What to put in the report

For every cell: required channels, observed per channel (count, users, last seen), leak check, and the value-parity result. State the exclusions applied and the window used, so the numbers can be reproduced and challenged.
