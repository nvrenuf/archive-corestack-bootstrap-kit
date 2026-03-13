import {
  TOP_LEVEL_ROUTES,
  getRoute,
  normalizeRoute,
  renderModuleHook,
  renderRouteContent,
} from "./corestack-shell.mjs";
import {
  createBrowserStorage,
  createRunStore,
  createWorkflowRegistry,
  launchWorkflowRun,
} from "./corestack-runtime.mjs";

const navRoot = document.querySelector("[data-primary-nav]");
const contentRoot = document.querySelector("[data-route-content]");
const titleRoot = document.querySelector("[data-route-title]");
const moduleHookRoot = document.querySelector("[data-module-nav-hook]");

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

const runStore = createRunStore({ storage: createBrowserStorage() });

function renderNav(activeRouteId) {
  navRoot.innerHTML = TOP_LEVEL_ROUTES.map((route, index) => `
    <a
      class="nav-link ${route.id === activeRouteId ? "active" : ""}"
      href="#/${route.id}"
      data-route-link="${route.id}"
    >
      <span>${route.label}</span>
      <span class="nav-index">${String(index + 1).padStart(2, "0")}</span>
    </a>
  `).join("");
}

function getRouteContext(routeId) {
  const runs = runStore.listRuns();

  if (routeId === "home") {
    return {
      activeRuns: runs.filter((run) => run.status === "running" || run.status === "blocked").slice(0, 3),
      recentRuns: runs.slice(0, 3),
    };
  }

  if (routeId === "launcher") {
    return {
      startPathLabel: "Launch alert triage run",
    };
  }

  return {};
}

function renderRoute() {
  const routeId = normalizeRoute(window.location.hash);
  const route = getRoute(routeId);
  titleRoot.textContent = route.label;
  renderNav(route.id);
  moduleHookRoot.innerHTML = renderModuleHook();
  contentRoot.innerHTML = renderRouteContent(route, getRouteContext(route.id));
}

contentRoot.addEventListener("click", (event) => {
  const trigger = event.target.closest("[data-start-workflow]");
  if (!trigger) {
    return;
  }

  const workflowId = trigger.getAttribute("data-start-workflow");
  launchWorkflowRun({
    registry: workflowRegistry,
    runStore,
    workflowId,
    actor: { actorId: "local-operator", actorType: "user" },
    input: { source: "launcher" },
  });
  window.location.hash = "#/home";
  renderRoute();
});

window.addEventListener("hashchange", renderRoute);
renderRoute();
