import React from "react";
import { useKC } from "../auth";

export function Protected({ allow = [], children }) {
  const { ready, authenticated, hasRole } = useKC();
  if (!ready) return <Centered label="Loading auth..." />;
  if (!authenticated) return <Centered label="Redirecting to login..." />;
  if (allow.length && !allow.some(hasRole)) return <Denied />;
  return children;
}

function Centered({ label }) {
  return (
    <div style={{minHeight:"70vh",display:"grid",placeItems:"center"}}>
      <div style={{opacity:.8}}>{label}</div>
    </div>
  );
}

function Denied() {
  const { kc } = useKC();
  return (
    <div style={{minHeight:"70vh",display:"grid",placeItems:"center"}}>
      <div style={{textAlign:"center"}}>
        <h2>Access denied</h2>
        <p>You do not have permissions to view this page.</p>
        <button onClick={() => kc?.accountManagement()}>Account</button>{" "}
        <button onClick={() => kc?.logout()}>Logout</button>
      </div>
    </div>
  );
}
