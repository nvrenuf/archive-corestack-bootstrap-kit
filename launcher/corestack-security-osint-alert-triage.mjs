import { buildRunPolicyReference, createPolicyDecision } from "./corestack-policy.mjs";
import { launchWorkflowRun } from "./corestack-runtime.mjs";

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function assertNonEmptyString(value, label) {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${label} must be a non-empty string`);
  }
}

export function validateAlertTriageInput(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new Error("alert triage input must be an object");
  }

  const alert = input.alert;
  if (!alert || typeof alert !== "object" || Array.isArray(alert)) {
    throw new Error("alert triage input.alert must be an object");
  }

  assertNonEmptyString(alert.alertId, "alert.alertId");
  assertNonEmptyString(alert.title, "alert.title");
  assertNonEmptyString(alert.severity, "alert.severity");
  assertNonEmptyString(alert.source, "alert.source");

  return clone({
    alert: {
      alertId: alert.alertId,
      title: alert.title,
      severity: alert.severity,
      source: alert.source,
      description: alert.description ?? null,
      indicators: Array.isArray(alert.indicators) ? alert.indicators : [],
      observedAt: alert.observedAt ?? null,
    },
    policy: {
      requireApproval: input.policy?.requireApproval !== false,
      allowExternalProviders: Boolean(input.policy?.allowExternalProviders),
      disallowedModelIds: input.policy?.disallowedModelIds ?? [],
    },
  });
}

export function createAlertTriageWorkflowService({
  workflowRegistry,
  runStore,
  caseStore,
  approvalStore,
  evidenceStore,
  modelRouter,
  modelExecutionHooks,
  auditStore,
  now = () => new Date().toISOString(),
} = {}) {
  function resolveCaseForRun({ run, actor, caseMode, requestedCaseId }) {
    if (caseMode === "attach") {
      const targetCase = caseStore.getCase(requestedCaseId);
      if (!targetCase) {
        throw new Error(`case not found: ${requestedCaseId}`);
      }
      caseStore.attachRun(requestedCaseId, run, "Alert triage run attached to existing case");
      runStore.linkCase(run.runId, requestedCaseId);
      return caseStore.getCase(requestedCaseId);
    }

    const createdCase = caseStore.createCaseFromRun({
      run,
      title: `Security / OSINT triage: ${run.input.alert.title}`,
      owner: actor,
    });
    runStore.linkCase(run.runId, createdCase.caseId);
    return createdCase;
  }

  async function executeInvestigation({ run, workflow, actor, linkedCase, policyDecision }) {
    const routeResult = modelRouter.route({
      target: { kind: "llm", capability: "summarize" },
      policy: {
        allowExternalProviders: run.input.policy.allowExternalProviders,
        disallowedModelIds: run.input.policy.disallowedModelIds,
        decisionId: policyDecision.decision_id,
      },
      context: {
        runId: run.runId,
        workflowId: workflow.id,
        caseId: linkedCase.caseId,
        actorId: actor.actorId,
        correlationId: run.policyContext?.correlation_id,
      },
    });

    auditStore.recordEvent({
      eventType: routeResult.audit.event_type,
      correlation: routeResult.audit.correlation,
      payload: routeResult.audit.payload,
    });

    if (!routeResult.ok) {
      runStore.failRun(run.runId, {
        stepId: "review",
        error: {
          code: routeResult.error.code,
          message: routeResult.error.message,
        },
      });
      caseStore.updateCaseStatus(linkedCase.caseId, "in-review");
      return {
        run: runStore.getRun(run.runId),
        caseRecord: caseStore.getCase(linkedCase.caseId),
        status: "failed",
        error: routeResult.error,
      };
    }

    const executionRequest = {
      routeResult,
      context: {
        runId: run.runId,
        workflowId: workflow.id,
        caseId: linkedCase.caseId,
        actorId: actor.actorId,
        correlationId: run.policyContext?.correlation_id,
        decisionId: policyDecision.decision_id,
        requestId: `model-request-${run.runId}`,
      },
      restrictions: {
        localOnly: !run.input.policy.allowExternalProviders,
      },
      invocation: {
        operation: "triage.summarize",
        inputShape: {
          alert_id: run.input.alert.alertId,
          severity: run.input.alert.severity,
        },
      },
    };

    const before = await modelExecutionHooks.beforeExecute(executionRequest);
    if (!before.ok) {
      runStore.failRun(run.runId, {
        stepId: "review",
        error: before.error,
      });
      caseStore.updateCaseStatus(linkedCase.caseId, "in-review");
      return {
        run: runStore.getRun(run.runId),
        caseRecord: caseStore.getCase(linkedCase.caseId),
        status: "failed",
        error: before.error,
      };
    }

    const triageSummary = `Alert ${run.input.alert.alertId} (${run.input.alert.severity}) from ${run.input.alert.source} triaged with ${routeResult.route.modelId}.`;

    await modelExecutionHooks.afterExecute(executionRequest, {
      ok: true,
      responseShape: {
        summary: triageSummary,
      },
    });

    const artifact = evidenceStore.createArtifact({
      type: "triage-report",
      classification: "osint.supporting",
      storageRef: {
        uri: `memory://triage/${run.runId}/summary.json`,
      },
      runId: run.runId,
      caseId: linkedCase.caseId,
      source: {
        kind: "workflow",
        workflowId: workflow.id,
      },
      provenance: {
        collectedAt: now(),
        collectorType: "security-osint.alert-triage",
      },
      metadata: {
        summary: triageSummary,
        modelId: routeResult.route.modelId,
      },
    });

    const evidence = evidenceStore.createEvidenceItem({
      type: "triage-summary",
      classification: "osint.supporting",
      summary: triageSummary,
      runId: run.runId,
      caseId: linkedCase.caseId,
      source: {
        kind: "workflow",
        workflowId: workflow.id,
      },
      provenance: {
        collectedAt: now(),
        collectorType: "security-osint.alert-triage",
      },
      artifactIds: [artifact.artifactId],
    });

    const finding = evidenceStore.createFinding({
      type: "alert-triage",
      severity: run.input.alert.severity,
      summary: `Triage finding for ${run.input.alert.title}`,
      runId: run.runId,
      caseId: linkedCase.caseId,
      evidenceIds: [evidence.evidenceId],
      artifactIds: [artifact.artifactId],
      provenance: {
        collectedAt: now(),
        collectorType: "security-osint.alert-triage",
      },
      metadata: {
        alertId: run.input.alert.alertId,
      },
    });

    runStore.completeRun(run.runId, {
      stepId: "review",
      output: {
        summary: triageSummary,
        findingId: finding.findingId,
      },
    });
    caseStore.updateCaseStatus(linkedCase.caseId, "in-review");

    return {
      run: runStore.getRun(run.runId),
      caseRecord: caseStore.getCase(linkedCase.caseId),
      status: "completed",
      output: {
        summary: triageSummary,
        artifactId: artifact.artifactId,
        evidenceId: evidence.evidenceId,
        findingId: finding.findingId,
      },
    };
  }

  return {
    startAlertTriage({ workflowId, actor, input, caseMode = "new", requestedCaseId = null }) {
      const workflow = workflowRegistry.get(workflowId);
      if (!workflow) {
        throw new Error(`workflow not registered: ${workflowId}`);
      }

      const normalizedInput = validateAlertTriageInput(input);
      const run = launchWorkflowRun({
        registry: workflowRegistry,
        runStore,
        workflowId,
        actor,
        input: {
          ...normalizedInput,
          source: "launcher",
          ...buildRunPolicyReference({
            workflow,
            actor,
            caseRecord: requestedCaseId ? caseStore.getCase(requestedCaseId) : null,
          }),
        },
      });

      const linkedCase = resolveCaseForRun({ run, actor, caseMode, requestedCaseId });
      const policyDecision = createPolicyDecision({
        decisionId: `policy-${run.runId}`,
        requestId: `request-${run.runId}`,
        outcome: normalizedInput.policy.requireApproval ? "require_approval" : "allow",
        reasons: normalizedInput.policy.requireApproval
          ? [{ code: "HUMAN_REVIEW_REQUIRED", message: "Analyst checkpoint requires explicit approval before continuation." }]
          : [{ code: "AUTO_TRIAGE_ALLOWED", message: "Policy allows this triage workflow to continue automatically." }],
        approval: normalizedInput.policy.requireApproval
          ? {
              required: true,
              subject_ref: `run:${run.runId}:review`,
              approver_role: "analyst",
            }
          : null,
        audit: {
          correlation_id: run.policyContext?.correlation_id ?? `${workflow.id}:${run.runId}`,
        },
      });

      runStore.appendPolicyDecision(run.runId, policyDecision);

      if (normalizedInput.policy.requireApproval) {
        const approval = approvalStore.createApproval({
          governedAction: {
            type: "workflow_step",
            id: `${run.runId}:review`,
            summary: "Proceed from analyst review checkpoint",
            correlationId: policyDecision.audit.correlation_id,
          },
          links: {
            runId: run.runId,
            workflowId: workflow.id,
            caseId: linkedCase.caseId,
            policyDecisionId: policyDecision.decision_id,
          },
          policyDecision,
          subject: {
            summary: "Alert triage review checkpoint",
            targetType: "workflow_step",
            targetId: "review",
          },
          reasonContext: {
            rationale: "Require analyst confirmation before advancing governed action.",
          },
          requestedBy: actor,
        });

        runStore.markPendingApproval(run.runId, {
          stepId: "review",
          approvalId: approval.approvalId,
          reason: "policy.require_approval",
        });

        return {
          status: "pending_approval",
          run: runStore.getRun(run.runId),
          caseRecord: caseStore.getCase(linkedCase.caseId),
          approval,
        };
      }

      return executeInvestigation({ run, workflow, actor, linkedCase, policyDecision });
    },
    resolveAlertTriageApproval({ approvalId, action, actor }) {
      const approval = approvalStore.getApproval(approvalId);
      if (!approval) {
        throw new Error(`approval not found: ${approvalId}`);
      }

      if (action === "deny") {
        approvalStore.denyApproval(approvalId, { actor, rationale: "Denied in MVP queue" });
        runStore.resolveApprovalCheckpoint(approval.links.runId, {
          stepId: "review",
          approvalId,
          outcome: "denied",
        });
        return {
          status: "denied",
          run: runStore.getRun(approval.links.runId),
          caseRecord: caseStore.getCase(approval.links.caseId),
        };
      }

      approvalStore.approveApproval(approvalId, { actor, rationale: "Approved in MVP queue" });
      runStore.resolveApprovalCheckpoint(approval.links.runId, {
        stepId: "review",
        approvalId,
        outcome: "approved",
      });

      const run = runStore.getRun(approval.links.runId);
      const workflow = workflowRegistry.get(approval.links.workflowId);
      const linkedCase = caseStore.getCase(approval.links.caseId);
      const policyDecision = run.policyDecisions.at(-1);
      return executeInvestigation({ run, workflow, actor, linkedCase, policyDecision });
    },
  };
}
