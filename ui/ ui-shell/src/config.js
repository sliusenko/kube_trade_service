// Якщо є window.__APP_CONFIG__ (підкинутий з ConfigMap/nginx) — беремо звідти
const runtime = window.__APP_CONFIG__ || {};

export const CONFIG = {
  title: "dazhcore portal",
  keycloak: {
    url: (runtime.keycloak && runtime.keycloak.url) || "https://auth.dazhcore.com",
    realm: (runtime.keycloak && runtime.keycloak.realm) || "kube-trade-bot",
    clientId: (runtime.keycloak && runtime.keycloak.clientId) || "admin-core",
  },
  routes: {
    adminUI: (runtime.routes && runtime.routes.adminUI) || "/",
    grafana: (runtime.routes && runtime.routes.grafana) || "/dashboards/",
    swagger: (runtime.routes && runtime.routes.swagger) || "/api/swagger-ui/",
    keycloak: (runtime.routes && runtime.routes.keycloak) || "/auth/",
  },
};
