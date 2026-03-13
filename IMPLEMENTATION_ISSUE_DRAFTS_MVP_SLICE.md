# IMPLEMENTATION_ISSUE_DRAFTS_MVP_SLICE.md

## Purpose

This document converts the smallest viable implementation slice into GitHub-ready implementation issue drafts.

The slice is intentionally narrow. It exists to prove:

- one Corestack desktop/control plane
- one registered Security/OSINT module
- one real Module 1 workflow
- policy-gated tool usage
- local-first model routing
- approvals/HITL
- evidence capture and review

## Issue 1

### Title

Implement the persistent Corestack shell and navigation skeleton

### Epic/group

Control plane shell and navigation foundation

### Why this issue exists

The product direction depends on one persistent control plane. This issue establishes the shell boundary before module-specific workflow work begins.

### Scope

Create the top-level shell, required navigation structure, and route scaffolding for core-owned surfaces.

### Explicit in-scope items

- persistent application shell
- top-level navigation structure
- route placeholders for Home, Launcher, Runs, Approvals, Cases / Evidence, Files / Artifacts, Logs / Audit, Agents, Policies, Models, Connectors, Modules, Settings, and Admin / Tenancy
- module-aware navigation hook points

### Explicit out-of-scope items

- workflow business logic
- detailed surface content
- module-specific views beyond route exposure
- advanced role customization

### Dependencies

- none

### Acceptance criteria

- a user can navigate between all required top-level surfaces without leaving one shell
- the shell clearly presents Corestack as one product
- modules are represented as part of the control plane, not as separate applications

### Test/validation expectations

- verify top-level routes resolve successfully
- verify navigation persists across route changes
- verify no route implies a separate-product module shell

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 2

### Title

Implement Home and Launcher as core-owned entry surfaces

### Epic/group

Control plane shell and navigation foundation

### Why this issue exists

The first slice needs clear user entry points for starting Module 1 work and returning to in-progress work.

### Scope

Add minimal Home and Launcher surfaces inside the shell.

### Explicit in-scope items

- Home surface skeleton
- Launcher surface skeleton
- placeholder sections for active work, approvals, recent work, and module workflow entry points
- Security/OSINT workflow launch entry path exposure

### Explicit out-of-scope items

- advanced dashboards
- role-tailored personalization
- rich analytics widgets

### Dependencies

- Issue 1

### Acceptance criteria

- Home exists as a stable landing surface
- Launcher exposes Security/OSINT workflow entry points
- both surfaces are core-owned and operate inside the shared shell

### Test/validation expectations

- verify Launcher can navigate into the first Module 1 workflow start path
- verify Home can display placeholder active work and approval sections

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 3

### Title

Define and implement the minimum run and workflow execution contract

### Epic/group

Core workflow, run, and case skeleton

### Why this issue exists

Module 1 workflows need a shared run model before any module-specific execution logic can be built safely.

### Scope

Create the minimum workflow/run contract and execution state model.

### Explicit in-scope items

- workflow registration shape
- run object
- step execution record shape
- run states such as created, running, blocked, failed, completed
- resumable/blocking semantics

### Explicit out-of-scope items

- full workflow builder
- advanced branching DSL
- multi-module workflow composition

### Dependencies

- Issue 1

### Acceptance criteria

- a workflow can be registered and launched as a run
- runs expose explicit state and step execution records
- runs support blocked and resumable execution states

### Test/validation expectations

- verify a stub workflow can start and persist run state
- verify state transitions persist correctly
- verify blocked runs can be resumed after an external state change

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 4

### Title

Define and implement the minimum case object and run-to-case linkage

### Epic/group

Core workflow, run, and case skeleton

### Why this issue exists

Module 1 needs a persistent investigation container that survives beyond one run and can hold evidence and approvals.

### Scope

Create the minimum case object and attach runs to cases.

### Explicit in-scope items

- case object shape
- case status and ownership fields
- case creation from run context
- attach existing case to run
- case timeline hook

### Explicit out-of-scope items

- advanced case collaboration
- rich case analytics
- export packaging

### Dependencies

- Issue 3

### Acceptance criteria

- a run can create a new case
- a run can attach to an existing case
- case identity and state are visible from linked run state

### Test/validation expectations

- verify case creation on workflow start
- verify run-to-case linkage persists
- verify basic case status updates persist

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 5

### Title

Define the policy decision contract for governed actions

### Epic/group

Policy-gated tool execution foundation

### Why this issue exists

The first slice must prove that tool use, model use, and later exports are governed by a reusable core policy contract rather than module-local logic.

### Scope

Define the common request/response shape for policy decisions.

### Explicit in-scope items

- policy decision request shape
- decision outcomes: allow, deny, approval-required
- reason codes
- limit/obligation fields
- reusable contract semantics for tools, models, and exports

### Explicit out-of-scope items

- full policy authoring UI
- complex inheritance model
- advanced admin tooling

### Dependencies

- Issue 3

### Acceptance criteria

- governed actions can request a policy decision through a shared contract
- decisions return stable effects and machine-readable reasons
- the contract is reusable across tools and model routing

### Test/validation expectations

- verify allow, deny, and approval-required decisions can be represented consistently
- verify reason codes are surfaced in a stable shape

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 6

### Title

Implement the `web.fetch` and `web.search` tool contracts and schemas

### Epic/group

Policy-gated tool execution foundation

### Why this issue exists

Security/OSINT Module 1 needs governed external collection through reusable tool contracts.

### Scope

Define request and response schemas for the first two tool classes.

### Explicit in-scope items

- `web.fetch` schema
- `web.search` schema
- normalized response envelope
- normalized error shape
- correlation metadata fields

### Explicit out-of-scope items

- gateway execution implementation
- broad connector catalog
- specialized OSINT connectors

### Dependencies

- Issue 5

### Acceptance criteria

- both tool contracts validate requests and responses
- failures return normalized error structures
- outputs contain the metadata needed for audit and evidence linkage

### Test/validation expectations

- schema validation tests for valid and invalid requests
- schema validation tests for normalized responses and errors

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 7

### Title

Implement a minimal tool gateway with policy enforcement and audit hooks

### Epic/group

Policy-gated tool execution foundation

### Why this issue exists

Tool execution must flow through one governed path to preserve the security model and avoid module-owned network behavior.

### Scope

Implement the minimum gateway path for executing `web.fetch` and `web.search`.

### Explicit in-scope items

- gateway execution path
- policy check before execution
- allowlist and limit enforcement hooks
- execution metadata capture
- audit emission on allow, deny, and failure

### Explicit out-of-scope items

- broad connector execution platform
- advanced sandbox hardening
- broad provider integrations

### Dependencies

- Issue 5
- Issue 6

### Acceptance criteria

- `web.fetch` and `web.search` only execute through the gateway
- denied actions return policy reasons
- allowed actions emit audit-ready metadata

### Test/validation expectations

- verify denied actions do not execute
- verify allowed actions emit audit events
- verify execution metadata includes correlation data

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 8

### Title

Define the minimum evidence, artifact, and finding objects

### Epic/group

Evidence, artifact, and audit backbone

### Why this issue exists

The first slice must produce evidence-bearing outputs that can be reviewed later. Without this, the workflow is not credible.

### Scope

Define the smallest evidence object set needed for the first workflow.

### Explicit in-scope items

- evidence item shape
- finding shape
- note shape
- artifact reference shape
- provenance fields
- supporting-evidence linkage fields

### Explicit out-of-scope items

- advanced graph relationships
- legal hold or retention automation
- evidence pack manifest design

### Dependencies

- Issue 4

### Acceptance criteria

- evidence items can link to a case
- findings can reference supporting evidence
- provenance fields exist on evidence-bearing objects

### Test/validation expectations

- verify object creation and linkage semantics
- verify required provenance fields are enforced

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 9

### Title

Implement artifact storage linkage and metadata persistence

### Epic/group

Evidence, artifact, and audit backbone

### Why this issue exists

The first slice needs file-like outputs for fetched data and normalized artifacts with persistent references back to runs and cases.

### Scope

Implement artifact reference persistence and storage linkage.

### Explicit in-scope items

- artifact storage reference model
- artifact metadata persistence
- content hash field where available
- linkage to run, case, and evidence objects

### Explicit out-of-scope items

- advanced file preview support
- report/export packaging
- bulk artifact operations

### Dependencies

- Issue 8

### Acceptance criteria

- artifacts can be stored and referenced from cases and evidence
- artifact metadata persists with relevant linkage and integrity fields

### Test/validation expectations

- verify artifact reference creation
- verify linkage to run/case/evidence persists
- verify integrity metadata persists when provided

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 10

### Title

Implement structured audit/event logging for runs, tools, evidence, and approvals

### Epic/group

Evidence, artifact, and audit backbone

### Why this issue exists

The first slice must be reconstructable. Audit cannot be added after the fact without costly retrofits.

### Scope

Implement the minimum structured audit/event logging needed for the slice.

### Explicit in-scope items

- event taxonomy for workflow, tool, policy, evidence, and approval actions
- correlation ids
- persistent event records
- object linkage in event metadata

### Explicit out-of-scope items

- full forensic export bundles
- advanced analytics dashboards
- complete tamper-evident chain implementation

### Dependencies

- Issue 3
- Issue 7
- Issue 8

### Acceptance criteria

- runs, tools, evidence, and approvals emit structured events
- events can be correlated to runs and cases
- the stored event shape can be surfaced in later UI work

### Test/validation expectations

- verify event emission on run state changes
- verify tool allow/deny/failure events are recorded
- verify evidence and approval events contain linked object references

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 11

### Title

Define and implement the approval object model and state machine

### Epic/group

Approvals and HITL flow

### Why this issue exists

Module 1 requires human review gates for escalation and similar actions, and those gates must be core-owned.

### Scope

Create the shared approval object and state model.

### Explicit in-scope items

- approval object shape
- states: pending, approved, denied, changes requested, escalated, expired, overridden
- linkage to run, case, and policy context
- rationale and scope fields

### Explicit out-of-scope items

- complex SLA routing
- advanced assignment workflows
- management reporting

### Dependencies

- Issue 3
- Issue 4

### Acceptance criteria

- approvals can be created and resolved
- approval states are explicit and persistent
- approvals link to relevant work objects and rationale

### Test/validation expectations

- verify valid state transitions
- verify invalid transitions are rejected
- verify linked case/run references persist

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 12

### Title

Add workflow approval checkpoints and approval queue/detail surfaces

### Epic/group

Approvals and HITL flow

### Why this issue exists

An approval object alone is insufficient. The first slice needs approvals to appear in the workflow and in the operator experience.

### Scope

Wire approval checkpoints into workflow execution and expose approval UI.

### Explicit in-scope items

- workflow pause/resume at approval checkpoints
- approvals queue surface
- approval detail surface
- approve, deny, request changes, escalate actions
- audit linkage from approval detail

### Explicit out-of-scope items

- complex escalation automation
- full approval analytics
- cross-tenant approval routing

### Dependencies

- Issue 1
- Issue 10
- Issue 11

### Acceptance criteria

- a workflow can block on an approval checkpoint
- an approver can act from the approval UI
- approval outcomes resume or terminate the gated path correctly

### Test/validation expectations

- verify blocked workflow resumes correctly after approval
- verify deny/request-changes/escalate states behave as expected
- verify approval actions emit audit events

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 13

### Title

Define and implement the model registry and local-first routing contract

### Epic/group

Model routing baseline

### Why this issue exists

The first workflow must prove that model use is routed through a core-owned local-first contract rather than vendor-specific module calls.

### Scope

Create the minimum model registry and capability-based routing path.

### Explicit in-scope items

- model registry
- capability tags
- local/open-weight default routing
- workflow capability request shape
- policy-aware provider selection hooks

### Explicit out-of-scope items

- fine-tuning
- advanced provider marketplace support
- optimization for cost/performance across many providers

### Dependencies

- Issue 3
- Issue 5

### Acceptance criteria

- workflows can request model capabilities instead of vendor-specific identifiers
- at least one local/open-weight path can be selected by the router
- routing decisions are explicit and inspectable

### Test/validation expectations

- verify capability-based routing selection
- verify local-first default behavior
- verify policy hook points exist in routing flow

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 14

### Title

Add model execution logging and external-provider restriction hooks

### Epic/group

Model routing baseline

### Why this issue exists

The first slice must show that model use is both auditable and policy-restricted from the start.

### Scope

Extend the baseline model routing path with logging and provider restriction enforcement hooks.

### Explicit in-scope items

- model execution event logging
- provider restriction enforcement points
- failure and fallback metadata

### Explicit out-of-scope items

- broad external provider support
- advanced evaluation harnesses
- cost reporting

### Dependencies

- Issue 10
- Issue 13

### Acceptance criteria

- model execution emits structured audit events
- disallowed external routes can be blocked by policy
- failures and fallbacks are recorded consistently

### Test/validation expectations

- verify model events are emitted with correlation ids
- verify restricted providers cannot be selected when blocked by policy

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Issue 15

### Title

Register Security/OSINT Module 1 through the core module contract

### Epic/group

Security/OSINT Module 1 workflow slice

### Why this issue exists

The first slice must prove that Module 1 is a true module on shared contracts rather than a private application surface.

### Scope

Register Module 1 and expose its first workflow through the control plane.

### Explicit in-scope items

- module registration
- module metadata
- workflow registration for Module 1
- module visibility in shell/Launcher

### Explicit out-of-scope items

- second and third Module 1 workflows
- separate module runtime
- module marketplace behavior

### Dependencies

- Issue 1
- Issue 3

### Acceptance criteria

- Security/OSINT appears in the control plane as a module
- Module 1 contributes workflows through core extension points
- no private shell or separate workflow runtime is introduced

### Test/validation expectations

- verify Module 1 registration is discoverable in the control plane
- verify registered workflow appears in Launcher

### Ownership

- module-owned content on a core-owned contract

### Slice status

- required for the smallest viable slice

## Issue 16

### Title

Implement the first end-to-end Module 1 workflow: Alert triage and investigation

### Epic/group

Security/OSINT Module 1 workflow slice

### Why this issue exists

This is the smallest real workflow that can validate shell, run, policy, tool, evidence, model, and approval contracts together.

### Scope

Implement the first working alert triage flow for Module 1.

### Explicit in-scope items

- alert-triggered or manual intake path
- run creation
- case creation/linkage
- governed tool usage where applicable
- model-assisted extraction and summary drafting
- evidence and finding creation
- at least one approval-gated path

### Explicit out-of-scope items

- OSINT entity investigation workflow
- incident evidence pack generation
- broad enrichment catalog
- advanced analyst collaboration

### Dependencies

- Issue 4
- Issue 7
- Issue 10
- Issue 12
- Issue 14
- Issue 15

### Acceptance criteria

- an operator can launch the workflow from the control plane
- the workflow creates a run and a case
- tool usage is policy-checked and logged
- model usage is routed through the core model path
- evidence and findings are attached to the case
- the workflow can exercise at least one approval checkpoint end to end

### Test/validation expectations

- validate successful workflow path from launch to case update
- validate denied or blocked policy path
- validate approval-gated path
- validate evidence and audit records are created

### Ownership

- module-owned workflow on core-owned contracts

### Slice status

- required for the smallest viable slice

## Issue 17

### Title

Implement run detail and case detail review surfaces

### Epic/group

MVP operator review surfaces

### Why this issue exists

The first slice is not validated until an operator can review run and case outputs in the control plane.

### Scope

Create the first review surfaces for runs and cases.

### Explicit in-scope items

- run detail surface
- case detail surface
- linked evidence/finding/timeline panels
- navigation pivots between run and case

### Explicit out-of-scope items

- advanced search and filtering
- relationship graph canvas
- management dashboarding

### Dependencies

- Issue 4
- Issue 8
- Issue 16

### Acceptance criteria

- operators can inspect run state and linked case data
- case detail shows findings, evidence, and timeline in one place
- operators can move between run and case without leaving the shared shell

### Test/validation expectations

- verify run detail renders step and state information
- verify case detail renders linked findings and evidence
- verify run-to-case navigation works

### Ownership

- core-owned surface with module-aware content

### Slice status

- required for the smallest viable slice

## Issue 18

### Title

Implement artifact/evidence detail and linked audit lookup

### Epic/group

MVP operator review surfaces

### Why this issue exists

Operators and reviewers need provenance and audit inspection to trust the first slice.

### Scope

Add detail views for evidence and artifacts, plus linked audit lookup.

### Explicit in-scope items

- evidence detail surface
- artifact metadata/detail surface
- linked audit lookup from run, case, and approval context
- provenance and integrity field display

### Explicit out-of-scope items

- rich binary preview support
- advanced audit analytics
- forensic export bundle UI

### Dependencies

- Issue 9
- Issue 10
- Issue 17

### Acceptance criteria

- evidence detail shows provenance fields
- artifact detail shows linkage and integrity metadata where available
- linked audit history can be inspected from core work surfaces

### Test/validation expectations

- verify evidence detail renders provenance data
- verify artifact detail renders integrity and linkage metadata
- verify audit lookup resolves linked events for run/case/approval context

### Ownership

- core-owned

### Slice status

- required for the smallest viable slice

## Recommended issue creation order

1. Issue 1: Implement the persistent Corestack shell and navigation skeleton
2. Issue 2: Implement Home and Launcher as core-owned entry surfaces
3. Issue 3: Define and implement the minimum run and workflow execution contract
4. Issue 4: Define and implement the minimum case object and run-to-case linkage
5. Issue 5: Define the policy decision contract for governed actions
6. Issue 6: Implement the `web.fetch` and `web.search` tool contracts and schemas
7. Issue 7: Implement a minimal tool gateway with policy enforcement and audit hooks
8. Issue 8: Define the minimum evidence, artifact, and finding objects
9. Issue 9: Implement artifact storage linkage and metadata persistence
10. Issue 10: Implement structured audit/event logging for runs, tools, evidence, and approvals
11. Issue 11: Define and implement the approval object model and state machine
12. Issue 12: Add workflow approval checkpoints and approval queue/detail surfaces
13. Issue 13: Define and implement the model registry and local-first routing contract
14. Issue 14: Add model execution logging and external-provider restriction hooks
15. Issue 15: Register Security/OSINT Module 1 through the core module contract
16. Issue 16: Implement the first end-to-end Module 1 workflow: Alert triage and investigation
17. Issue 17: Implement run detail and case detail review surfaces
18. Issue 18: Implement artifact/evidence detail and linked audit lookup

## Recommended execution order

1. Issue 1
2. Issue 3
3. Issue 4
4. Issue 5
5. Issue 6
6. Issue 7
7. Issue 8
8. Issue 9
9. Issue 10
10. Issue 11
11. Issue 13
12. Issue 14
13. Issue 15
14. Issue 16
15. Issue 2
16. Issue 12
17. Issue 17
18. Issue 18

Execution note:

- Issue 2 can be implemented early from a UX standpoint, but it is safe to delay some of its content until the first workflow path is real.
- Issue 12 should not land before Issue 11 and enough workflow state exists to block/resume correctly.
- Issue 16 is the first issue that proves the slice end to end and should arrive before broadening UI polish.

## First 5 issues only

If the team wants to start even narrower, begin with:

1. Issue 1: Implement the persistent Corestack shell and navigation skeleton
2. Issue 3: Define and implement the minimum run and workflow execution contract
3. Issue 4: Define and implement the minimum case object and run-to-case linkage
4. Issue 5: Define the policy decision contract for governed actions
5. Issue 6: Implement the `web.fetch` and `web.search` tool contracts and schemas

This subset creates the minimum structural base needed before gateway, evidence, approvals, and model routing are added.

## Issues that could be combined if fewer tickets are needed

- Issue 1 and Issue 2 can be combined into one shell-and-entry-surfaces ticket.
- Issue 5, Issue 6, and Issue 7 can be combined into one governed tool execution foundation ticket.
- Issue 8 and Issue 9 can be combined into one evidence-and-artifact-model ticket.
- Issue 13 and Issue 14 can be combined into one model routing baseline ticket.
- Issue 17 and Issue 18 can be combined into one review-surfaces ticket.

## Issues that should remain separate

- Issue 3 and Issue 4 should remain separate so workflow/run ownership does not get muddied with case model ownership.
- Issue 10 should remain separate so audit requirements are not hidden inside tool, model, or workflow tickets.
- Issue 11 and Issue 12 should remain separate so approval state semantics are defined before UI/workflow checkpoint behavior.
- Issue 15 and Issue 16 should remain separate so module registration stays distinct from workflow implementation.
- Issue 16 should remain separate from the second-pass Module 1 workflows to preserve a thin first slice.

## Alignment

This document is based on:

- [IMPLEMENTATION_ISSUE_BREAKDOWN_SECURITY_OSINT_MODULE_1.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/IMPLEMENTATION_ISSUE_BREAKDOWN_SECURITY_OSINT_MODULE_1.md)
- [ISSUES_ORDER.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/ISSUES_ORDER.md)
- [CORESTACK_REQUIREMENTS_SPEC.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/CORESTACK_REQUIREMENTS_SPEC.md)
- [SECURITY_OSINT_MODULE_1.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/SECURITY_OSINT_MODULE_1.md)
- [REFERENCE_ARCHITECTURE_SECURITY_OSINT_MODULE_1.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/REFERENCE_ARCHITECTURE_SECURITY_OSINT_MODULE_1.md)
- [UX_INFORMATION_ARCHITECTURE_CORESTACK_DESKTOP.md](/Users/leecuevas/Projects/corestack-bootstrap-kit/UX_INFORMATION_ARCHITECTURE_CORESTACK_DESKTOP.md)
