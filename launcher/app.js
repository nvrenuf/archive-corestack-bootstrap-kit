import {
  TOP_LEVEL_ROUTES,
  getRoute,
  normalizeRoute,
  renderModuleHook,
  renderRouteContent,
} from "./corestack-shell.mjs";

const navRoot = document.querySelector("[data-primary-nav]");
const contentRoot = document.querySelector("[data-route-content]");
const titleRoot = document.querySelector("[data-route-title]");
const moduleHookRoot = document.querySelector("[data-module-nav-hook]");

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

function renderRoute() {
  const routeId = normalizeRoute(window.location.hash);
  const route = getRoute(routeId);
  titleRoot.textContent = route.label;
  renderNav(route.id);
  moduleHookRoot.innerHTML = renderModuleHook();
  contentRoot.innerHTML = renderRouteContent(route);
}

window.addEventListener("hashchange", renderRoute);
renderRoute();
