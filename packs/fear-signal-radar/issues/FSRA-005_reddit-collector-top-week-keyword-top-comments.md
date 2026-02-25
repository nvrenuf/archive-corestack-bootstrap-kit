Title: FSRA-005 Reddit Collector (top/week + keyword + top comments)
Target Version: 0.1.0
Priority: P1
Labels: pack:fear-signal-radar, fsra, mvp, collector, reddit, security
Owner:
Context:
Reddit is a primary channel for early fear signal detection. The collector must gather weekly top posts and top comments by topic keywords under strict caps.
Scope:
- Implement Reddit collector with keyword query support.
- Fetch top/week posts and top comments per post under configured limits.
- Submit normalized snippets to ingest API.
Non-Goals:
- Full Reddit archive scraping.
- Sentiment model training.
- Historical trend analytics.
Security Requirements:
- Collector cannot directly call arbitrary domains; outbound requests go through egress proxy only.
- Collector remains write-only to ingest API.
- Fetch logging is required for each API call and ingest submission.
- Enforce per-run/per-post caps from topic config.
- Sanitize and bound text prior to ingest submission.
Acceptance Criteria (testable bullets):
- `services/collector-reddit/` exists with runnable collector entrypoint.
- Collector fetches top/week posts for configured keywords and ingests at least one normalized item in integration test.
- Collector fetches comments and respects `max_comments_per_item` cap.
- Collector emits structured fetch logs with request target, count fetched, and duration.
- Collector sends payloads to ingest API and handles dedupe responses without retries that exceed configured limit.
- Network test confirms only egress proxy host is contacted for outbound requests.
Implementation Notes:
- Normalize Reddit post/comment fields into common signal item schema.
- Include source provenance fields (`subreddit`, `post_id`, `comment_id`).
- Add retry with exponential backoff bounded by topic config.
Deliverables (file paths):
- services/collector-reddit/
- services/collector-reddit/README.md
- services/collector-reddit/config.example.yaml
Dependencies:
- FSRA-001
- FSRA-003
- FSRA-004
Definition of Done:
- Collector ingests bounded Reddit snippets through ingest API.
- Logs and caps are validated in test run.
- Security constraints (egress-only/write-only) are verified.
