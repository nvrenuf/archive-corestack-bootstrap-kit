Title: FSRA-013 Dashboard + angle picker + exports
Target Version: 0.4.0
Priority: P2
Labels: pack:fear-signal-radar, fsra, backlog, dashboard, exports, ux
Owner:
Context:
Once synthesis and verification mature, operators need a focused dashboard to triage signals, choose narrative angles, and export stakeholder-ready outputs.
Scope:
- Build dashboard view for current run, trends, and verification status.
- Add angle picker workflow to compose report framing.
- Add export options for JSON, Markdown, and CSV summaries.
Non-Goals:
- Public multi-tenant portal.
- Mobile native app.
- Role-based enterprise permission matrix.
Security Requirements:
- Dashboard backend must not introduce unrestricted outbound internet access.
- Display-only path cannot mutate ingest records except through approved actions.
- Continue collector write-only contract and egress/fetch logging controls.
- Enforce output sanitization and size limits for downloadable artifacts.
- Audit log user export actions with timestamps and artifact ids.
Acceptance Criteria (testable bullets):
- Dashboard route renders latest run summary, top clusters, trend direction, and verification status.
- Angle picker supports at least 3 saved angle presets per topic.
- Export action produces JSON, Markdown, and CSV files under `outputs/{topic_id}/exports/`.
- Export files are generated with deterministic naming including run id and timestamp.
- Access controls prevent unauthenticated users from viewing dashboard/export endpoints.
- Audit logs record each export event with actor, format, topic id, and output path.
Implementation Notes:
- Reuse existing report schemas for backend responses.
- Keep UI state minimal and driven by server APIs.
- Include pagination for high-volume signal lists.
Deliverables (file paths):
- services/dashboard/
- services/dashboard/README.md
- outputs/{topic_id}/exports/
Dependencies:
- FSRA-011
- FSRA-012
Definition of Done:
- Dashboard and exports are functional for verified radar runs.
- Authentication and audit requirements are validated.
- Operator workflow for angle selection is documented.
