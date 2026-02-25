Title: FSRA-008 Synthesizer Agent (cluster + score + report JSON+MD export)
Target Version: 0.1.0
Priority: P1
Labels: pack:fear-signal-radar, fsra, mvp, synthesizer, reporting, security
Owner:
Context:
Collected snippets must be converted into operator-useful output. The synthesizer clusters items, scores threat/fear relevance, and exports machine/human-readable reports.
Scope:
- Implement synthesizer workflow for clustering and scoring.
- Generate radar report artifacts in JSON and Markdown.
- Include traceability from each cluster back to source evidence items.
Non-Goals:
- Advanced historical trend forecasting.
- Human-in-the-loop verification UI.
- Dashboard implementation.
Security Requirements:
- Synthesizer must not perform direct internet fetches.
- Reads only from internal DB/artifacts; writes report outputs locally.
- Preserve provenance for each claim/cluster to reduce hallucinated conclusions.
- Enforce output size caps to avoid oversized artifacts.
- Log run metadata and deterministic input set references.
Acceptance Criteria (testable bullets):
- `services/synthesizer/` exists with executable entrypoint.
- Running synthesizer for a topic writes both `outputs/{topic_id}/radar_report.json` and `outputs/{topic_id}/radar_report.md`.
- JSON report includes run id, topic id, generated_at timestamp, clusters array, and scored signals.
- Markdown report includes sectioned summary with at least: top signals, supporting evidence, and confidence notes.
- Every cluster references at least one source item id present in `signal_items`.
- Synthesizer logs include input row count, output file paths, and runtime duration.
Implementation Notes:
- Keep scoring heuristic deterministic in MVP for reproducibility.
- Use configurable thresholds via env vars or topic config overrides.
- Include clear markdown headings for downstream export tooling.
Deliverables (file paths):
- services/synthesizer/
- outputs/{topic_id}/radar_report.json
- outputs/{topic_id}/radar_report.md
Dependencies:
- FSRA-002
- FSRA-005
- FSRA-006
- FSRA-007
Definition of Done:
- Synthesizer produces both export formats from ingested data.
- Provenance mapping and scoring fields are present and test-verified.
- Output generation is documented for operations use.
