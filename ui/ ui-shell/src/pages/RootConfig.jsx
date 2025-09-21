import React from "react";
export default function RootConfig(){
  return (
    <div style={{display:"grid",gap:16,gridTemplateColumns:"1fr 1fr"}}>
      <section style={{background:"#fff",border:"1px solid #eee",borderRadius:12,padding:16}}>
        <h3>Bot Parameters</h3>
        <ul>
          <li>Maps / exchange bindings</li>
          <li>User & roles management</li>
          <li>Global feature flags</li>
        </ul>
      </section>
      <section style={{background:"#fff",border:"1px solid #eee",borderRadius:12,padding:16}}>
        <h3>Shortcuts</h3>
        <ul>
          <li><a href="/api/swagger-ui/" target="_blank" rel="noreferrer">Swagger</a></li>
          <li><a href="/auth/" target="_blank" rel="noreferrer">Keycloak</a></li>
        </ul>
      </section>
    </div>
  );
}
