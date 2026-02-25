Title: FSRA-006 YouTube Collector (recent videos + top comments + velocity proxy)
Target Version: 0.1.0
Priority: P1
Labels: pack:fear-signal-radar, fsra, mvp, collector, youtube, security
Owner:
Context:
YouTube commentary and creator output can signal rapidly spreading narratives. This collector gathers recent relevant videos, top comments, and velocity proxy indicators.
Scope:
- Implement YouTube collector for recent videos by keyword/topic.
- Fetch top comments and lightweight velocity proxy metrics.
- Submit normalized snippets and metrics to ingest API.
Non-Goals:
- Full transcript ingestion.
- Channel-level reputation scoring.
- Cross-platform trend modeling.
Security Requirements:
- Collector must use central egress proxy for all outbound calls.
- Collector is write-only to ingest API with no read endpoints.
- Enforce payload and request count caps from topic config.
- Sanitize title/description/comment text before ingest.
- Log each external fetch and ingest attempt for audit.
Acceptance Criteria (testable bullets):
- `services/collector-youtube/` exists with runnable collector entrypoint.
- Collector retrieves recent videos for configured keywords and ingests normalized items.
- Collector fetches top comments per video and enforces `max_comments_per_item` cap.
- Collector records velocity proxy fields (for example: view_count, like_count, comment_count, age_hours) in payload metadata.
- Network test confirms outbound requests route only through egress proxy and allowlisted domains.
- Collector logs include fetched counts, rejected counts, and ingest response summaries.
Implementation Notes:
- Keep source-specific mappers isolated from shared item normalization code.
- Treat velocity metrics as optional fields if provider data is missing.
- Use deterministic item hash inputs to improve dedupe.
Deliverables (file paths):
- services/collector-youtube/
- services/collector-youtube/README.md
- services/collector-youtube/config.example.yaml
Dependencies:
- FSRA-001
- FSRA-003
- FSRA-004
Definition of Done:
- Collector successfully ingests bounded YouTube-derived signal items.
- Velocity proxy metadata is present for supported items.
- Security and logging constraints are validated.
