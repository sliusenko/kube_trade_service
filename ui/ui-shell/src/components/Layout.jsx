import React from "react";
import { NavLink } from "react-router-dom";
import { useKC } from "../auth";

export default function Layout({ children }) {
  const { kc, tokenParsed, roles } = useKC();
  const username = tokenParsed?.preferred_username || "user";

  const menu = [
    { to: "/home", label: "Home", roles: ["viewer","trader","admin","root"] },
    { to: "/config", label: "Configs", roles: ["admin","root"] },
    { to: "/analytics", label: "Analytics", roles: ["viewer","trader","admin","root"] },
    { to: "/swagger", label: "API (Swagger)", roles: ["admin","root"] },
    { to: "/auth-console", label: "SSO Console", roles: ["root"] },
    { to: "/root-config", label: "Root Config", roles: ["root"] },
  ];
  const visible = menu.filter(m => m.roles.some(r => roles.has(r)));

  return (
    <div style={{minHeight:"100vh",background:"#f7f7fb"}}>
      <header style={{position:"sticky",top:0,background:"#fff",borderBottom:"1px solid #eee",padding:"10px 16px",display:"flex",justifyContent:"space-between"}}>
        <strong>dazhcore portal</strong>
        <div style={{display:"flex",gap:8,alignItems:"center"}}>
          <span style={{opacity:.7}}>{username}</span>
          <button onClick={() => kc?.accountManagement()}>Account</button>
          <button onClick={() => kc?.logout()}>Logout</button>
        </div>
      </header>
      <div style={{display:"grid",gridTemplateColumns:"220px 1fr",gap:16,padding:"16px",maxWidth:1200,margin:"0 auto"}}>
        <aside style={{display:"flex",flexDirection:"column",gap:6}}>
          {visible.map(m => (
            <NavLink key={m.to} to={m.to} style={({isActive})=>({
              padding:"8px 10px", borderRadius:8, textDecoration:"none",
              background:isActive?"#111":undefined, color:isActive?"#fff":"#111"
            })}>{m.label}</NavLink>
          ))}
        </aside>
        <main>{children}</main>
      </div>
    </div>
  );
}
