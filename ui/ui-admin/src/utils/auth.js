// src/utils/auth.js
export function signOut() {
  const keycloakUrl = window._env_.REACT_APP_KEYCLOAK_URL;
  const realm = window._env_.REACT_APP_KEYCLOAK_REALM;
  const portalUrl = window._env_.REACT_APP_PORTAL_URL || window.location.origin;

  const logoutUrl =
    `${keycloakUrl}/realms/${realm}/protocol/openid-connect/logout?` +
    `redirect_uri=${encodeURIComponent(portalUrl)}`;

  window.location.href = logoutUrl;
}
