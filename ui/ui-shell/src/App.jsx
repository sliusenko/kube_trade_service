// src/App.jsx
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import { KCProvider } from "./auth";
import { Protected } from "./components/Protected";
import Home from "./pages/Home";
import Iframe from "./pages/Iframe";
import RootConfig from "./pages/RootConfig";
import { CONFIG } from "./config";

export default function App() {
  return (
    <KCProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<Protected allow={["viewer","trader","admin","root"]}><Home/></Protected>} />
            <Route path="/config" element={<Protected allow={["admin","root"]}><Iframe src={CONFIG.routes.adminUI} title="admin-ui" /></Protected>} />
            <Route path="/analytics" element={<Protected allow={["viewer","trader","admin","root"]}><Iframe src={CONFIG.routes.grafana} title="grafana" /></Protected>} />
            <Route path="/swagger" element={<Protected allow={["admin","root"]}><Iframe src={CONFIG.routes.swagger} title="swagger" /></Protected>} />
            <Route path="/auth-console" element={<Protected allow={["root"]}><Iframe src={CONFIG.routes.keycloak} title="keycloak" /></Protected>} />
            <Route path="/root-config" element={<Protected allow={["root"]}><RootConfig/></Protected>} />
            <Route path="*" element={<Navigate to="/home" replace />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </KCProvider>
  );
}
