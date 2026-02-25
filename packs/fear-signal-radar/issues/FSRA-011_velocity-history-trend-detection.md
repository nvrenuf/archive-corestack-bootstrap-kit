Title: FSRA-011 Velocity + history + trend detection
Target Version: 0.2.0
Priority: P2
Labels: pack:fear-signal-radar, fsra, backlog, analytics, trend, history
Owner:
Context:
After MVP, operators need trend context across runs to identify acceleration/deceleration and persistent narratives.
Scope:
- Add historical snapshots and trend computation layer.
- Compute velocity deltas by topic/source/cluster across defined windows.
- Expose trend flags for use in reports and future dashboard.
Non-Goals:
- Predictive forecasting with external models.
- Verification/citation adjudication.
- Dashboard rendering.
Security Requirements:
- No new direct internet paths; reuse existing collector/egress controls.
- Preserve collector write-only ingest boundary.
- Continue fetch logging, sanitization, and payload caps for all source data.
- Ensure historical storage does not include unsanitized raw payloads.
- Add retention bounds for history tables/artifacts.
Acceptance Criteria (testable bullets):
- New migration(s) define history/trend storage with indexes for time-window queries.
- Trend job computes velocity metrics for at least 3 windows (24h, 7d, 30d).
- Reports include trend direction field (`up`, `flat`, `down`) per major cluster.
- At least 3 deterministic test fixtures validate trend calculations.
- Trend generation runtime for 10k signal items completes within documented SLO threshold.
- Retention policy configuration exists and is enforced in cleanup job/tests.
Implementation Notes:
- Keep trend math deterministic and auditable.
- Reuse `radar_runs` identifiers for lineage.
- Prefer additive schema changes from 0.1.0.
Deliverables (file paths):
- migrations/002_velocity_history.sql
- services/synthesizer/trend/
- outputs/{topic_id}/trend_report.json
Dependencies:
- FSRA-008
- FSRA-009
Definition of Done:
- Trend metrics are persisted and exported.
- Tests verify correctness and performance targets.
- Retention and security controls remain enforced.
