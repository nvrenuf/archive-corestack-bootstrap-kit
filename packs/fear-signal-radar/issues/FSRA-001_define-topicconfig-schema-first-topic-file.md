Title: FSRA-001 Define TopicConfig schema + first topic file
Target Version: 0.1.0
Priority: P0
Labels: pack:fear-signal-radar, fsra, mvp, schema, config, security
Owner:
Context:
Fear Signal Radar requires a strict topic definition contract before collectors, storage, and synthesis can run safely. This issue defines the JSON schema and an initial topic config for work/money entry-level collapse monitoring.
Scope:
- Create JSON Schema for TopicConfig with required fields for topic identity, source toggles, keyword lists, collector caps, and egress constraints.
- Create first production-ready topic config aligned to that schema.
- Add schema validation examples in issue notes for downstream services.
Non-Goals:
- Implement collector runtime.
- Implement ingest API or DB writes.
- Add multiple topic configs beyond the first seed file.
Security Requirements:
- Corestack services must not make direct internet calls outside the controlled egress proxy.
- Collectors must remain write-only to ingest and cannot read Corestack internal data stores.
- Topic config must define explicit caps (per source/per run/per payload) to bound ingestion volume.
- Inputs and fetched text assumptions must support sanitization before persistence.
- Fetch logging requirements must be preserved by including fields needed for traceability (source, URL, fetch time, collector id).
Acceptance Criteria (testable bullets):
- `schemas/topic_config.schema.json` exists and is valid JSON.
- Schema declares required keys: `topic_id`, `display_name`, `keywords`, `sources`, `caps`, `egress`.
- Schema enforces `topic_id` pattern `^[a-z0-9-]{3,64}$`.
- Schema enforces numeric caps with minimums greater than 0 for `max_items_per_run`, `max_comments_per_item`, and `max_payload_bytes`.
- `configs/topics/work-money_entry-level-collapse.yaml` exists and validates against the schema using repository validation tooling.
- Topic config includes at least 10 keywords, at least 2 enabled sources, and explicit collector caps.
Implementation Notes:
- Use JSON Schema Draft 2020-12 for compatibility with existing toolchain.
- Keep source-specific options nested under `sources.<source_name>`.
- Include a static `allowed_domains` list reference in topic config to support egress policy generation.
Deliverables (file paths):
- schemas/topic_config.schema.json
- configs/topics/work-money_entry-level-collapse.yaml
Dependencies:
- None
Definition of Done:
- Schema and topic file are committed.
- Validation command is documented in issue comments or README update task.
- Downstream teams can consume this schema without guessing field semantics.
