Title: FSRA-012 Verification layer (evidence vs speculation; citations workflow)
Target Version: 0.3.0
Priority: P2
Labels: pack:fear-signal-radar, fsra, backlog, verification, citations, trust
Owner:
Context:
Operators need explicit differentiation between evidence-backed signals and speculative claims before decision-making.
Scope:
- Add verification classifier/heuristics for evidence vs speculation.
- Add citation workflow and confidence annotation in outputs.
- Track verification decisions and reviewer notes.
Non-Goals:
- Full legal/compliance review workflow.
- Human moderation UI.
- External fact-check provider integration.
Security Requirements:
- No direct internet expansion beyond existing egress controls.
- Collectors remain write-only and source ingest remains sanitized/capped.
- Verification outputs must preserve source provenance and immutable evidence references.
- Log verification decisions for auditability.
- Prevent unsafe claim promotion by requiring evidence references for high-confidence labels.
Acceptance Criteria (testable bullets):
- Verification module labels each synthesized claim as `evidence`, `mixed`, or `speculation`.
- `radar_report.json` includes citations list per claim with source item ids and URLs.
- Claims marked high-confidence without citations are rejected in validation tests.
- Verification audit log captures claim id, label, confidence, citation count, and reviewer/system actor.
- At least 20 fixture claims are evaluated in tests with expected labels.
- Markdown export displays a separate section for speculation with warning text.
Implementation Notes:
- Start with deterministic rule set before model-based verification.
- Keep label thresholds configurable.
- Track transformation lineage from raw signal item to final claim.
Deliverables (file paths):
- services/synthesizer/verification/
- schemas/verification_result.schema.json
- outputs/{topic_id}/verification_report.md
Dependencies:
- FSRA-011
Definition of Done:
- Verification labels and citations are enforced in exports.
- Validation rejects uncited high-confidence claims.
- Audit trail supports post-run review.
