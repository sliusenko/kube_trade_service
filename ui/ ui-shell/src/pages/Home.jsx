import React from "react";
import { useKC } from "../auth";
export default function Home(){
  const { tokenParsed, roles } = useKC();
  return (
    <div style={{background:"#fff",border:"1px solid #eee",borderRadius:12,padding:16}}>
      <h2>Welcome</h2>
      <p>You are logged in as <b>{tokenParsed?.preferred_username}</b>.</p>
      <p>Roles: {[...roles].join(", ") || "none"}</p>
    </div>
  );
}
