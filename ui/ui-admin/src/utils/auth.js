// src/utils/auth.js

/**
 * Виконує повний вихід із Keycloak (SSO).
 * Після виклику користувача редіректить на портал,
 * де його змусить знову залогінитися.
 */
export function signOut() {
  const keycloakLogoutUrl =
    "https://auth.dazhcore.com/realms/trade-realm/protocol/openid-connect/logout" +
    "?redirect_uri=" + encodeURIComponent("https://portal.dazhcore.com/");

  window.location.href = keycloakLogoutUrl;
}
