// src/utils/auth.js
export function signOut() {
  const keycloakUrl = process.env.REACT_APP_KEYCLOAK_URL;
  const realm = process.env.REACT_APP_KEYCLOAK_REALM;
  const portalUrl = process.env.REACT_APP_PORTAL_URL;

  const logoutUrl =
    `${keycloakUrl}/realms/${realm}/protocol/openid-connect/logout` +
    `?redirect_uri=${encodeURIComponent(portalUrl)}`;

  window.location.href = logoutUrl;
}
