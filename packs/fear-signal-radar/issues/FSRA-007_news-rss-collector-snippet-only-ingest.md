Title: FSRA-007 News/RSS Collector (snippet-only ingest)
Target Version: 0.1.0
Priority: P1
Labels: pack:fear-signal-radar, fsra, mvp, collector, news, rss, security
Owner:
Context:
News and RSS feeds provide structured signals but carry scraping/legal risk. MVP requires snippet-only ingestion from approved feeds with strict limits.
Scope:
- Implement collector for allowlisted news and RSS feeds.
- Ingest snippet-only records (headline, excerpt, metadata), not full article bodies.
- Enforce feed allowlist and per-run caps.
Non-Goals:
- Full-text paywalled scraping.
- Browser automation collectors.
- Citation verification workflow.
Security Requirements:
- No direct internet access except through egress proxy.
- Collector write-only to ingest API.
- Feed allowlist enforced before fetch.
- Snippet size and total payload caps enforced.
- Fetch and ingest logging required for each operation.
Acceptance Criteria (testable bullets):
- `services/collector-news/` exists with feed allowlist configuration.
- Collector ingests only snippet fields and excludes full page content/body HTML.
- Requests to non-allowlisted feeds are blocked and logged.
- Collector enforces per-feed and per-run max item caps from topic config.
- Network test verifies outbound requests go only through egress proxy.
- Ingest payload size remains under configured byte cap in integration tests.
Implementation Notes:
- Normalize RSS/Atom and JSON feed formats into one internal item structure.
- Include publication timestamp and canonical URL in every item.
- Keep parser strict; drop malformed entries with logged reason codes.
Deliverables (file paths):
- services/collector-news/
- services/collector-news/feed_allowlist.yaml
- services/collector-news/README.md
Dependencies:
- FSRA-001
- FSRA-003
- FSRA-004
Definition of Done:
- Collector performs snippet-only ingestion from approved feeds.
- Caps, allowlist, and logging requirements are tested.
- Security constraints are documented and enforced.
