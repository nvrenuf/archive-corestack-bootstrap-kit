export const TOP_LEVEL_ROUTES = [
  { id: "home", label: "Home", scope: "core" },
  { id: "launcher", label: "Launcher", scope: "core" },
  { id: "runs", label: "Runs", scope: "core" },
  { id: "approvals", label: "Approvals", scope: "core" },
  { id: "cases-evidence", label: "Cases / Evidence", scope: "core" },
  { id: "files-artifacts", label: "Files / Artifacts", scope: "core" },
  { id: "logs-audit", label: "Logs / Audit", scope: "core" },
  { id: "agents", label: "Agents", scope: "core" },
  { id: "policies", label: "Policies", scope: "core" },
  { id: "models", label: "Models", scope: "core" },
  { id: "connectors", label: "Connectors", scope: "core" },
  { id: "modules", label: "Modules", scope: "core" },
  { id: "settings", label: "Settings", scope: "core" },
  { id: "admin-tenancy", label: "Admin / Tenancy", scope: "core" },
];

const ROUTE_IDS = new Set(TOP_LEVEL_ROUTES.map((route) => route.id));

export function normalizeRoute(hash = "") {
  const routeId = hash.replace(/^#\/?/, "").trim();
  return ROUTE_IDS.has(routeId) ? routeId : "home";
}

export function getRoute(routeId) {
  return TOP_LEVEL_ROUTES.find((route) => route.id === routeId) ?? TOP_LEVEL_ROUTES[0];
}

export function renderSurfacePlaceholder(route) {
  return `
    <section class="surface-placeholder" data-surface-id="${route.id}">
      <span class="surface-meta">${route.scope}-owned surface</span>
      <h3>${route.label}</h3>
      <p>This route is intentionally scaffolded inside the persistent Corestack shell.</p>
      <ul class="placeholder-list">
        <li>Shared control-plane route is active for ${route.label}.</li>
        <li>Module-specific content remains constrained to future slices.</li>
        <li>No separate product shell or module-owned navigation is introduced.</li>
      </ul>
    </section>
  `;
}

export function renderModuleHook() {
  return `
    <ul class="hook-list">
      <li>Module surfaces register content inside the shared shell.</li>
      <li>Security/OSINT remains a module, not a separate desktop.</li>
    </ul>
  `;
}
