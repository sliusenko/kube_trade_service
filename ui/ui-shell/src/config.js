// Якщо є window.__APP_CONFIG__ (підкинутий з ConfigMap/nginx) — беремо звідти
const runtime = window.__APP_CONFIG__ || {};

export const CONFIG = {
  title: "dazhcore portal",
  keycloak: {
    url: (runtime.keycloak && runtime.keycloak.url) || "https://auth.dazhcore.com",
    realm: (runtime.keycloak && runtime.keycloak.realm) || "trade-realm",
    clientId: (runtime.keycloak && runtime.keycloak.clientId) || "portal",
  },
  routes: {
    adminUI: (runtime.routes && runtime.routes.adminUI) || "/",
    grafana: (runtime.routes && runtime.routes.grafana) || "/dashboards/",
    swagger: (runtime.routes && runtime.routes.swagger) || "/api/swagger-ui/",
    keycloak: (runtime.routes && runtime.routes.keycloak) || "/auth/",
  },
};
