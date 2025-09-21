import React from "react";
export default function Iframe({ src, title="iframe" }) {
  return (
    <div style={{height:"75vh",background:"#fff",border:"1px solid #eee",borderRadius:12,overflow:"hidden"}}>
      <iframe title={title} src={src} style={{width:"100%",height:"100%",border:0}} />
    </div>
  );
}
