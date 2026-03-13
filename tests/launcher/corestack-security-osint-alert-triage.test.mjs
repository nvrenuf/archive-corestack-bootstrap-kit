import test from "node:test";
import assert from "node:assert/strict";

import { createApprovalStore } from "../../launcher/corestack-approvals.mjs";
import { createAuditEventStore } from "../../launcher/corestack-audit.mjs";
import { createCaseStore } from "../../launcher/corestack-cases.mjs";
import { createEvidenceStore } from "../../launcher/corestack-evidence.mjs";
import { createModelExecutionHooks } from "../../launcher/corestack-model-execution.mjs";
import { createModelRegistry, createModelRouter } from "../../launcher/corestack-model-routing.mjs";
import { createAlertTriageWorkflowService } from "../../launcher/corestack-security-osint-alert-triage.mjs";
import { createMemoryStorage, createRunStore, createWorkflowRegistry } from "../../launcher/corestack-runtime.mjs";

function createHarness() {
  let runCounter = 0;
  let caseCounter = 0;
  let approvalCounter = 0;
  let eventCounter = 0;
  let artifactCounter = 0;
  let evidenceCounter = 0;
  let findingCounter = 0;
  const storage = createMemoryStorage();
  const workflowRegistry = createWorkflowRegistry([
    {
      id: "security-osint.alert-triage",
      moduleId: "security-osint-module-1",
      name: "Alert triage and investigation",
      version: "0.1.0",
      steps: [
        { id: "intake", title: "Intake and normalize alert", kind: "ingest" },
        { id: "review", title: "Analyst review checkpoint", kind: "review" },
      ],
    },
  ]);
  const auditStore = createAuditEventStore({
    storage,
    now: () => "2026-03-13T00:00:00.000Z",
    createEventId: () => `event-${++eventCounter}`,
  });
  const runStore = createRunStore({
    storage,
    now: () => "2026-03-13T00:00:00.000Z",
    createId: () => `run-${++runCounter}`,
    emitEvent: ({ event_type, timestamp, correlation, payload }) =>
      auditStore.recordEvent({ eventType: event_type, timestamp, correlation, payload }),
  });
  const caseStore = createCaseStore({
    storage,
    now: () => "2026-03-13T00:00:00.000Z",
    createId: () => `case-${++caseCounter}`,
  });
  const approvalStore = createApprovalStore({
    storage,
    now: () => "2026-03-13T00:00:00.000Z",
    createApprovalId: () => `approval-${++approvalCounter}`,
    emitEvent: ({ event_type, timestamp, correlation, payload }) =>
      auditStore.recordEvent({ eventType: event_type, timestamp, correlation, payload }),
  });
  const evidenceStore = createEvidenceStore({
    storage,
    runStore,
    caseStore,
    now: () => "2026-03-13T00:00:00.000Z",
    createArtifactId: () => `artifact-${++artifactCounter}`,
    createEvidenceId: () => `evidence-${++evidenceCounter}`,
    createFindingId: () => `finding-${++findingCounter}`,
    emitEvent: ({ event_type, timestamp, correlation, payload }) =>
      auditStore.recordEvent({ eventType: event_type, timestamp, correlation, payload }),
  });

  const modelRegistry = createModelRegistry([
    {
      id: "local.mistral-small",
      kind: "llm",
      providerType: "local",
      localFirst: true,
      status: { available: true },
      trustTags: ["self_hosted"],
      capabilities: ["summarize"],
    },
  ]);
  const modelRouter = createModelRouter({ registry: modelRegistry });
  const modelExecutionHooks = createModelExecutionHooks({
    now: () => "2026-03-13T00:00:00.000Z",
    emitEvent: ({ event_type, timestamp, correlation, payload }) =>
      auditStore.recordEvent({ eventType: event_type, timestamp, correlation, payload }),
  });

  const service = createAlertTriageWorkflowService({
    workflowRegistry,
    runStore,
    caseStore,
    approvalStore,
    evidenceStore,
    modelRouter,
    modelExecutionHooks,
    auditStore,
    now: () => "2026-03-13T00:00:00.000Z",
  });

  return { service, runStore, caseStore, approvalStore, evidenceStore, auditStore };
}

const actor = { actorId: "analyst-1", actorType: "user" };
const alertInput = {
  alert: {
    alertId: "alert-1",
    title: "Suspicious DNS pattern",
    severity: "high",
    source: "sensor-a",
  },
};

test("alert triage workflow initiation creates run, links case, and enters pending approval", () => {
  const { service, runStore, caseStore, approvalStore } = createHarness();
  const result = service.startAlertTriage({
    workflowId: "security-osint.alert-triage",
    actor,
    input: alertInput,
  });

  assert.equal(result.status, "pending_approval");
  assert.equal(result.run.status, "pending_approval");
  assert.equal(result.caseRecord.caseId, "case-1");
  assert.equal(runStore.getRun("run-1").caseId, "case-1");
  assert.equal(caseStore.getCase("case-1").runIds[0], "run-1");
  assert.equal(approvalStore.projectQueueItems()[0].approvalId, "approval-1");
});

test("approval path executes model routing and creates evidence-bearing output", async () => {
  const { service, evidenceStore, auditStore } = createHarness();
  const started = service.startAlertTriage({
    workflowId: "security-osint.alert-triage",
    actor,
    input: alertInput,
  });

  const resolved = await service.resolveAlertTriageApproval({
    approvalId: started.approval.approvalId,
    action: "approve",
    actor,
  });

  assert.equal(resolved.status, "completed");
  assert.equal(resolved.run.status, "completed");
  assert.equal(evidenceStore.listArtifacts().length, 1);
  assert.equal(evidenceStore.listEvidenceItems().length, 1);
  assert.equal(evidenceStore.listFindings().length, 1);
  assert.ok(auditStore.listEvents({ eventType: "model.routing.decision" }).length >= 1);
  assert.ok(auditStore.listEvents({ eventType: "model.execution.requested" }).length >= 1);
  assert.ok(auditStore.listEvents({ eventType: "evidence.object.mutated" }).length >= 3);
});

test("auto-allowed triage can execute without approval", async () => {
  const { service } = createHarness();
  const result = await service.startAlertTriage({
    workflowId: "security-osint.alert-triage",
    actor,
    input: {
      ...alertInput,
      policy: { requireApproval: false },
    },
  });

  assert.equal(result.status, "completed");
  assert.equal(result.run.policyDecisions[0].outcome, "allow");
});

test("invalid alert input and blocked routing path produce safe failures", async () => {
  const { service } = createHarness();

  assert.throws(
    () => service.startAlertTriage({ workflowId: "security-osint.alert-triage", actor, input: { alert: { title: "missing" } } }),
    /alert\.alertId must be a non-empty string/,
  );

  const started = service.startAlertTriage({
    workflowId: "security-osint.alert-triage",
    actor,
    input: {
      ...alertInput,
      policy: { requireApproval: false, disallowedModelIds: ["local.mistral-small"] },
    },
  });

  const failed = await started;
  assert.equal(failed.status, "failed");
  assert.equal(failed.run.status, "failed");
  assert.equal(failed.error.code, "NO_ROUTE");
});
