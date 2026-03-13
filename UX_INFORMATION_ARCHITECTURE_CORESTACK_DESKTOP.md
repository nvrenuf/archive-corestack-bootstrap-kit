# UX_INFORMATION_ARCHITECTURE_CORESTACK_DESKTOP.md

## 1. UX intent

Corestack is one desktop/control plane. The UX must present one coherent operator workspace for workflows, cases, evidence, approvals, policies, connectors, models, modules, and administration.

The UX must feel like a professional operator workspace:

- task-oriented instead of shell-switching-oriented
- evidence-aware instead of chat-centric
- stateful instead of ephemeral
- reviewable and auditable instead of opaque

Modules extend the experience without fragmenting the product. Module-aware content may add workflows, panels, views, and object facets, but modules must not create separate top-level shells or replace core-owned product surfaces.

Security/OSINT Module 1 is the first real vertical surface. It should shape the first analyst-facing experience while validating shared control-plane UX patterns for runs, cases, evidence, approvals, logs, policies, connectors, and exports.

If packs are mentioned, they should be treated as implementation or runtime details rather than product identity. The operator-facing experience remains Corestack.

## 2. Primary personas

### SOC analyst

#### Primary goals

- triage alerts quickly
- determine whether escalation is needed
- create defensible findings and attach evidence

#### Top actions

- open alert-driven investigations
- review run output and enrichment
- inspect and attach evidence
- disposition or escalate cases

#### What they need visible

- assigned or priority work
- current run and case status
- evidence-linked findings
- blockers, denials, and pending approvals

#### What they should not need to touch often

- model configuration
- connector secrets
- policy authoring
- tenancy or deep admin settings

### IR lead

#### Primary goals

- oversee high-severity investigations
- maintain review discipline and evidence quality
- approve escalations and exports

#### Top actions

- review cases and timelines
- inspect findings and evidence coverage
- approve or deny gated actions
- direct and reassign work

#### What they need visible

- case severity and status
- pending approvals
- export readiness and unresolved gaps
- audit trail for high-risk actions

#### What they should not need to touch often

- low-level connector configuration
- routine model selection
- module lifecycle controls

### Threat hunter

#### Primary goals

- pursue hypotheses
- correlate signals across entities and prior investigations
- turn weak indicators into supported findings

#### Top actions

- initiate entity investigations
- pivot across entities, evidence, and artifacts
- save notes, hypotheses, and findings

#### What they need visible

- related entities and relationships
- source provenance
- prior runs and linked cases
- safe enrichment and collection paths

#### What they should not need to touch often

- approval administration
- export configuration
- deep system health settings

### OSINT investigator

#### Primary goals

- investigate external entities and infrastructure using governed sources
- preserve provenance
- separate supported observations from unresolved hypotheses

#### Top actions

- launch manual investigations
- collect source material
- review artifacts and extracted entities
- produce findings and exportable summaries

#### What they need visible

- search scope and policy constraints
- source records and artifact provenance
- evidence/finding linkage
- export readiness

#### What they should not need to touch often

- core workflow administration
- model registry details
- tenancy controls

### Security manager

#### Primary goals

- understand case status and investigation quality
- review high-risk approvals and exceptions
- consume exports and summaries without re-running technical workflows

#### Top actions

- review case summaries
- inspect approvals and overrides
- review evidence pack outputs

#### What they need visible

- concise case and run status
- high-risk approvals
- exports and review outcomes
- policy exception activity

#### What they should not need to touch often

- detailed evidence editing
- connector configuration
- workflow step-level operation

### Platform admin

#### Primary goals

- keep the control plane healthy
- manage models, connectors, policies, modules, and operational settings
- support secure self-hosted operation

#### Top actions

- manage connectors and secrets
- manage policies and model availability
- inspect system health, logs, and audit streams
- enable or disable modules

#### What they need visible

- system health and warnings
- connector status
- model availability and routing defaults
- policy status and enforcement impact
- module lifecycle state

#### What they should not need to touch often

- day-to-day investigation notes
- low-risk case handling
- routine analyst decisions

## 3. Top-level navigation

Recommended order:

1. Home
2. Launcher
3. Runs
4. Approvals
5. Cases / Evidence
6. Files / Artifacts
7. Logs / Audit
8. Agents
9. Policies
10. Models
11. Connectors
12. Modules
13. Settings
14. Admin / Tenancy

The order prioritizes operator work first, then governance surfaces, then administration.

### Home

#### Purpose

Provide a role-aware overview of active work, blocked work, recent investigations, approvals, and system signals relevant to the user.

#### Primary users

- SOC analyst
- IR lead
- threat hunter
- OSINT investigator
- security manager
- platform admin

#### Core objects shown there

- runs
- cases
- approvals
- exports
- major warnings or blockers

#### Key actions

- resume work
- open a case
- open a pending approval
- jump into a workflow start path

#### Core-wide or module-aware

- Core-wide with module-aware widgets

### Launcher

#### Purpose

Provide a stable entry surface for available modules and workflow start paths without becoming a generic app catalog.

#### Primary users

- SOC analyst
- threat hunter
- OSINT investigator
- platform admin

#### Core objects shown there

- modules
- workflow entry points
- saved or recent launch paths

#### Key actions

- launch Security/OSINT workflows
- inspect module capabilities
- jump to recent module-aware work

#### Core-wide or module-aware

- Core-owned shell with module-aware content

### Agents

#### Purpose

Expose reusable agent or assistant definitions, capability boundaries, and linked policy/model context.

#### Primary users

- platform admin
- IR lead
- advanced operators

#### Core objects shown there

- agents
- allowed tools
- model defaults
- policy associations

#### Key actions

- inspect
- enable/disable
- review capability boundaries

#### Core-wide or module-aware

- Core-wide with module-aware usage context

### Runs

#### Purpose

Provide the execution-centric view of in-progress, blocked, failed, queued, and completed workflow runs.

#### Primary users

- SOC analyst
- IR lead
- threat hunter
- OSINT investigator

#### Core objects shown there

- runs
- workflow steps
- statuses
- blockers
- linked approvals
- linked cases

#### Key actions

- open run details
- resume or retry
- inspect step outputs
- pivot to linked case or evidence

#### Core-wide or module-aware

- Core-wide with strong module awareness

### Approvals

#### Purpose

Provide the queue and detail views for all approval-gated actions, denials, requested changes, escalations, expirations, and overrides.

#### Primary users

- IR lead
- security manager
- platform admin

#### Core objects shown there

- approvals
- approval state
- requester and approver
- linked case/run/policy/export references

#### Key actions

- approve
- deny
- request changes
- escalate
- inspect approval history

#### Core-wide or module-aware

- Core-wide with module-specific context panes

### Cases / Evidence

#### Purpose

Provide the primary investigative workspace for cases, evidence, findings, notes, entities, relationships, and timelines.

#### Primary users

- SOC analyst
- IR lead
- threat hunter
- OSINT investigator
- security manager

#### Core objects shown there

- cases
- evidence items
- findings
- notes
- entities
- relationships
- timeline events

#### Key actions

- open a case
- inspect evidence and provenance
- create or revise findings
- review timeline
- initiate export

#### Core-wide or module-aware

- Core-wide with strong module-aware layouts and panels

### Files / Artifacts

#### Purpose

Provide direct access to stored artifacts, snapshots, manifests, reports, and export bundles.

#### Primary users

- SOC analyst
- IR lead
- OSINT investigator
- platform admin

#### Core objects shown there

- artifacts
- reports
- manifests
- source snapshots
- export bundles

#### Key actions

- preview
- inspect provenance and integrity metadata
- link to cases or evidence
- export or download where allowed

#### Core-wide or module-aware

- Core-wide with module-derived artifact types

### Logs / Audit

#### Purpose

Expose operational and forensic records for workflows, tools, policies, models, approvals, evidence changes, and user actions.

#### Primary users

- platform admin
- IR lead
- security manager

#### Core objects shown there

- audit events
- workflow events
- tool/policy/model events
- user action events

#### Key actions

- search by correlation id
- filter by object id
- reconstruct an action path
- inspect failures, denials, and overrides

#### Core-wide or module-aware

- Core-wide

### Policies

#### Purpose

Expose and manage execution rules for tools, connectors, models, exports, and selected workflow actions.

#### Primary users

- platform admin
- security manager

#### Core objects shown there

- policies
- policy scopes
- allow/deny rules
- approval-required rules
- recent denials or exception context

#### Key actions

- inspect
- edit
- review impact on workflows or modules
- inspect recent decision outcomes

#### Core-wide or module-aware

- Core-wide with module-level scope views

### Models

#### Purpose

Expose local and external model entries, capabilities, routing defaults, and policy constraints.

#### Primary users

- platform admin
- advanced operators

#### Core objects shown there

- models
- providers
- capability tags
- routing defaults
- availability status

#### Key actions

- inspect
- enable/disable
- review routing role and restrictions

#### Core-wide or module-aware

- Core-wide with module-aware usage context

### Connectors

#### Purpose

Manage ingestion, enrichment, and export connectors together with their status, restrictions, and secret bindings.

#### Primary users

- platform admin
- advanced operators

#### Core objects shown there

- connectors
- status
- policy scope
- secret binding references
- module usage context

#### Key actions

- configure
- enable/disable
- inspect restrictions
- test

#### Core-wide or module-aware

- Core-wide with module-aware assignments

### Modules

#### Purpose

Expose installed modules, contributed workflows, views, connectors, and lifecycle state.

#### Primary users

- platform admin
- security manager
- advanced operators

#### Core objects shown there

- modules
- lifecycle state
- contributed workflows
- contributed views/connectors

#### Key actions

- inspect
- enable/disable
- review contributed content

#### Core-wide or module-aware

- Core-wide

### Settings

#### Purpose

Provide user and workspace preferences that are not deep platform administration.

#### Primary users

- all personas, lightly

#### Core objects shown there

- profile settings
- notifications
- workspace preferences

#### Key actions

- adjust preferences
- update user-level defaults

#### Core-wide or module-aware

- Core-wide

### Admin / Tenancy

#### Purpose

Provide hardened administration for deployment-level settings, system health, access boundaries, retention, and future tenancy controls.

#### Primary users

- platform admin

#### Core objects shown there

- system health
- retention settings
- access or boundary settings
- storage status
- tenancy controls if later implemented

#### Key actions

- inspect health
- update admin settings
- inspect warnings

#### Core-wide or module-aware

- Core-wide

## 4. Core object model in the UX

### Agent

#### What it is

A reusable assistant or execution profile with defined capabilities, tools, models, and policies.

#### Where users see it

- Agents
- workflow launch context
- run details

#### What actions users can take on it

- inspect
- enable/disable
- review capability boundaries

#### What relationships matter most

- workflows
- tools
- models
- policies

### Run

#### What it is

A concrete execution instance of a workflow.

#### Where users see it

- Home
- Runs
- Cases / Evidence
- Approvals

#### What actions users can take on it

- open
- resume
- retry
- inspect steps
- pivot to linked objects

#### What relationships matter most

- workflow
- case
- approvals
- artifacts
- audit events

### Workflow

#### What it is

A reusable procedure definition that drives runs.

#### Where users see it

- Launcher
- Modules
- Runs

#### What actions users can take on it

- launch
- inspect prerequisites
- review recent run history

#### What relationships matter most

- module
- agent
- runs
- policies

### Approval

#### What it is

A human decision object for a gated action.

#### Where users see it

- Approvals
- Runs
- Cases / Evidence
- Logs / Audit

#### What actions users can take on it

- approve
- deny
- request changes
- escalate
- inspect history

#### What relationships matter most

- case
- run
- policy
- requester
- approver

### Case

#### What it is

The primary investigative container for a unit of work, incident, or investigation.

#### Where users see it

- Home
- Cases / Evidence
- Runs
- Approvals

#### What actions users can take on it

- open
- update status
- assign
- review timeline
- initiate export

#### What relationships matter most

- evidence items
- findings
- artifacts
- runs
- approvals

### Evidence item

#### What it is

A structured evidentiary object linked to a case and supported by provenance.

#### Where users see it

- Cases / Evidence
- Runs
- Files / Artifacts

#### What actions users can take on it

- inspect
- attach/detach
- review provenance
- link to findings

#### What relationships matter most

- case
- source
- artifact
- finding
- derived-from chain

### Artifact

#### What it is

A stored file-like or payload snapshot object such as a fetched page, normalized payload, report, or manifest.

#### Where users see it

- Files / Artifacts
- Cases / Evidence
- Runs

#### What actions users can take on it

- preview
- inspect integrity metadata
- link to case or evidence
- export where allowed

#### What relationships matter most

- evidence item
- source
- export package
- run

### Finding

#### What it is

A supported observation or conclusion produced by a workflow or analyst.

#### Where users see it

- Cases / Evidence
- Runs
- exports

#### What actions users can take on it

- create
- edit
- review support
- mark state or confidence

#### What relationships matter most

- case
- supporting evidence
- notes
- approvals

### Policy

#### What it is

A reusable rule set controlling access, routing, limits, and approval requirements.

#### Where users see it

- Policies
- Approvals
- Runs
- Models
- Connectors

#### What actions users can take on it

- inspect
- edit
- review impact and recent denials

#### What relationships matter most

- tools
- connectors
- models
- modules
- approvals

### Model

#### What it is

A registered local or external model path with known capability tags and restrictions.

#### Where users see it

- Models
- Runs
- Policies

#### What actions users can take on it

- inspect
- enable/disable
- review routing role

#### What relationships matter most

- provider
- policies
- workflows
- runs

### Connector

#### What it is

A configured integration path for ingestion, enrichment, or export.

#### Where users see it

- Connectors
- Policies
- Runs
- Modules

#### What actions users can take on it

- configure
- enable/disable
- test
- inspect restrictions

#### What relationships matter most

- policies
- workflows
- modules
- secrets

### Module

#### What it is

A domain extension that adds workflows, views, connectors, and object facets to the Corestack control plane.

#### Where users see it

- Launcher
- Modules
- Home

#### What actions users can take on it

- inspect
- enable/disable
- launch workflows
- review contributed content

#### What relationships matter most

- workflows
- views
- connectors
- policies

## 5. Primary user flows

### Alert triage and investigation

#### Entry point

- Home priority work list
- Launcher workflow entry
- direct alert intake path

#### Screens/surfaces touched

- Home
- Launcher
- Runs
- Cases / Evidence
- Approvals
- Files / Artifacts
- Logs / Audit when needed

#### User actions

- open the alert-driven run
- inspect normalized alert and extracted entities
- review enrichment and findings
- add notes or adjust case linkage
- disposition or escalate

#### Agent/system actions

- create run and case linkage
- normalize alert
- execute governed search/fetch/enrichment
- draft summaries and findings
- create evidence, artifacts, and timeline entries
- request approval when required

#### Approval points

- escalation
- scope exception
- final disposition where policy requires review
- external export or handoff

#### Outputs

- triage summary
- updated case state
- linked evidence and findings

### OSINT entity investigation

#### Entry point

- Launcher workflow entry
- Home quick action
- pivot from a case, entity, or evidence item

#### Screens/surfaces touched

- Home
- Launcher
- Runs
- Cases / Evidence
- Files / Artifacts
- Approvals when required

#### User actions

- define seed entity and scope
- review sources, artifacts, and extracted entities
- refine direction of investigation
- save findings and notes
- initiate export if needed

#### Agent/system actions

- create run and case context
- enforce policy on requested scope
- execute governed search/fetch/enrichment
- generate relationship suggestions and draft summaries
- persist findings, notes, sources, and artifacts

#### Approval points

- broadened scope where policy requires it
- higher-risk collection categories if later supported
- export or closure where policy requires it

#### Outputs

- entity profile
- supporting evidence set
- exportable investigation summary

### Incident evidence pack generation

#### Entry point

- case detail action
- approval follow-up action
- completed run action

#### Screens/surfaces touched

- Cases / Evidence
- Files / Artifacts
- Approvals
- Logs / Audit for review and verification

#### User actions

- choose report scope and output type
- review included evidence and unresolved gaps
- inspect manifest and draft outputs
- approve release or request changes

#### Agent/system actions

- assemble evidence set
- draft chronology and summaries
- generate manifest and report artifacts
- write export bundle
- record release and handoff events

#### Approval points

- redactions where required
- final release
- external handoff/export

#### Outputs

- evidence pack manifest
- analyst report
- management summary
- export bundle reference

## 6. Approval and HITL UX

### Where approvals appear

- global Approvals surface
- Home widgets for relevant personas
- run detail pages
- case detail pages

### What information the approver sees

Each approval detail should show:

- requested action
- requester
- linked case and run
- relevant policy reason
- evidence and finding summary
- impact of approve versus deny
- deadline, escalation path, and related prior approvals

### Approve / deny / request changes / escalate states

The UX should support:

- pending
- approved
- denied
- changes requested
- escalated
- expired
- overridden

The UI should distinguish terminal states from states that return work to the analyst.

### How overrides are shown

- overrides must be visually distinct from ordinary approvals
- the UI should show who overrode, why, what authority applied, and what scope changed
- override history must remain visible from the approval detail, linked case/run, and Logs / Audit

### How auditability is exposed in the UI

- approval detail includes a decision-history panel
- linked audit events are directly accessible
- users can pivot from approval to case, run, policy, and export
- approval state changes should also appear in the case timeline

## 7. Evidence and case UX

### How evidence is collected and attached

- workflows should attach evidence by default as outputs are produced
- analysts can attach existing artifacts or findings to a case
- evidence creation should not require manual filing for routine workflow outputs

### How provenance is shown

Each evidence detail should expose:

- source
- acquisition method
- tool or connector used
- collection time
- parent/derived-from references
- integrity metadata where present
- linked run and case

### How cases are reviewed

Case review should center:

- summary and status
- findings
- evidence list
- timeline
- related runs
- approvals
- export readiness

The review model should feel chronological and evidence-first rather than document-first.

### How exports are initiated

- from case detail
- from approved workflow outputs
- from evidence-pack preparation panels

Export initiation should show scope, policy implications, and approval requirements before submission.

### What makes the experience analyst-friendly

- clear separation between draft system output and approved findings
- one-click pivots between run, case, evidence, artifact, and approval
- visible blockers such as denied tools or pending approvals
- evidence support shown near findings rather than hidden in separate flows
- timeline and provenance accessible from the active work context

## 8. Module UX extension rules

### What navigation can be extended

Modules may extend:

- Launcher entries
- Home widgets
- module-aware tabs or panels inside Runs and Cases / Evidence
- module-specific saved views under Modules

### What objects can be added

Modules may add:

- domain-specific object facets
- domain-specific relationship labels
- domain-specific workflow types
- module-specific summary panels

### What module-specific panels are allowed

Allowed module-specific panels include:

- workflow-specific input panels
- domain-specific evidence views
- investigation summary panels
- module-specific dashboards within the module context

### What must remain core-owned

- desktop shell and top-level navigation structure
- Home and Launcher shell behavior
- Runs
- Approvals
- Cases / Evidence base model
- Files / Artifacts base model
- Logs / Audit
- Policies
- Models
- Connectors
- Modules
- Settings
- Admin / Tenancy

Modules may specialize these surfaces but may not replace them.

## 9. MVP UX scope

### Minimum viable UI

Desktop shell:

- persistent shell and top-level navigation
- one coherent control-plane layout

Home and launcher:

- Home overview with active work and blockers
- Launcher for module and workflow entry points

Module 1 workflows:

- run detail view with steps, blockers, and linked objects
- case detail view with findings, evidence, timeline, and related runs
- workflow launch paths for the first three Security/OSINT workflows

Approvals:

- approvals queue
- approval detail with approve/deny/request changes/escalate

Evidence/cases:

- case list
- case detail
- evidence detail
- artifact preview or metadata detail

Logs/audit:

- searchable audit list
- event detail with correlation ids and linked object references

Admin essentials:

- connector list/detail
- policy list/detail
- model list/detail
- module list/detail
- basic health/admin status

### Explicitly deferred

- advanced visual analytics
- graph-native investigation canvas
- broad personalization
- full workflow designer
- deep tenancy UX
- extensive executive dashboarding
- collaboration/chat surfaces

## 10. Open UX questions

- Should Home be heavily role-tailored or mostly consistent across personas?
- After intake, should analysts work primarily from Runs or Cases / Evidence?
- What is the best first-class entry point for alert-driven work: Home queue, Launcher shortcut, or direct case/run intake?
- How much entity/relationship visualization is required in MVP?
- Should approvals remain a top-level destination for all personas or mainly for reviewers/admins?
- What is the minimum artifact preview experience needed for analyst confidence?
- How should module-specific panels be visually distinct without fragmenting the product?
- What is the right balance between timeline-first and evidence-grid-first case review?

## Alignment

This document is intended to align:

- [ISSUES_ORDER.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/ISSUES_ORDER.md)
- [docs/roadmap/CORESTACK_ISSUE_DRAFTS.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/docs/roadmap/CORESTACK_ISSUE_DRAFTS.md)
- [SECURITY_OSINT_MODULE_1.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/SECURITY_OSINT_MODULE_1.md)
- [REFERENCE_ARCHITECTURE_SECURITY_OSINT_MODULE_1.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/REFERENCE_ARCHITECTURE_SECURITY_OSINT_MODULE_1.md)

It should guide:

- control-plane UX surface definition
- Module 1 operator workflows
- approval and HITL UX
- evidence/case review UX
- module extension rules
