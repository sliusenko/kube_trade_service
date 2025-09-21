import React from "react";
import Keycloak from "keycloak-js";
import { CONFIG } from "./config";

const KCContext = React.createContext(null);
export const useKC = () => React.useContext(KCContext);

export function KCProvider({ children }) {
  const [kc, setKc] = React.useState(null);
  const [ready, setReady] = React.useState(false);
  const [authenticated, setAuthenticated] = React.useState(false);
  const timerRef = React.useRef(null);

  React.useEffect(() => {
    const _kc = new Keycloak({
      url: CONFIG.keycloak.url,
      realm: CONFIG.keycloak.realm,
      clientId: CONFIG.keycloak.clientId,
    });

    _kc.init({ onLoad: "login-required", checkLoginIframe: false, pkceMethod: "S256" })
      .then((auth) => {
        setKc(_kc);
        setAuthenticated(auth);
        setReady(true);
        scheduleRefresh(_kc);
      })
      .catch((e) => {
        console.error("Keycloak init failed", e);
        setReady(true);
      });

    function scheduleRefresh(kc) {
      clearInterval(timerRef.current);
      timerRef.current = setInterval(async () => {
        try { await kc.updateToken(30); } catch { kc.login(); }
      }, 15000);
    }
    return () => clearInterval(timerRef.current);
  }, []);

  const tokenParsed = kc?.tokenParsed || {};
  const roles = new Set(
    (tokenParsed?.realm_access?.roles || []).concat(
      ...Object.values(tokenParsed?.resource_access || {}).map((r) => r.roles || [])
    )
  );
  const hasRole = (r) => roles.has(r);

  return (
    <KCContext.Provider value={{ kc, ready, authenticated, tokenParsed, roles, hasRole }}>
      {children}
    </KCContext.Provider>
  );
}
