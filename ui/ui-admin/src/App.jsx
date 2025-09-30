import React, { Suspense, lazy } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import { signOut } from "./utils/auth";

// 🔹 Lazy imports
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const UsersPage = lazy(() => import("./pages/UsersPage"));
const ExchangesPage = lazy(() => import("./pages/ExchangesPage"));
const NewsPage = lazy(() => import("./pages/NewsPage"));
const PageConfig = lazy(() => import("./pages/PageConfig"));

const Page = ({ title, children }) => (
  <div className="p-6">
    <h1 style={{ fontSize: 28, marginBottom: 12 }}>{title}</h1>
    <div>{children}</div>
  </div>
);

const navStyle = ({ isActive }) => ({
  padding: "10px 14px",
  borderRadius: 10,
  textDecoration: "none",
  fontWeight: 600,
  background: isActive ? "#eef2ff" : "transparent",
  color: isActive ? "#1e40af" : "#111827",
  display: "block",
});

export default function App() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "220px 1fr", minHeight: "100vh" }}>
      {/* Sidebar */}
      <aside style={{ borderRight: "1px solid #e5e7eb", padding: 16, display: "flex", flexDirection: "column", height: "100%" }}>
        <div style={{ fontWeight: 800, marginBottom: 16 }}>Admin Panel</div>
        <nav style={{ display: "grid", gap: 6 }}>
          <NavLink to="/" style={navStyle} end>Dashboard</NavLink>
          <NavLink to="/users" style={navStyle}>Users</NavLink>
          <NavLink to="/exchanges" style={navStyle}>Exchanges</NavLink>
          <NavLink to="/config" style={navStyle}>Config</NavLink>
          <NavLink to="/news" style={navStyle}>News</NavLink>
        </nav>
      </aside>

      {/* Main content */}
      <div style={{ display: "flex", flexDirection: "column" }}>
        {/* 🔑 Header */}
        <header style={{ borderBottom: "1px solid #e5e7eb", padding: "10px 16px", display: "flex", justifyContent: "flex-end" }}>
          <button
            onClick={signOut}
            style={{
              padding: "8px 14px",
              borderRadius: 8,
              fontWeight: 600,
              background: "#fee2e2",
              color: "#b91c1c",
              border: "none",
              cursor: "pointer",
            }}
          >
            Sign Out
          </button>
        </header>

        <main style={{ flex: 1 }}>
          <Suspense fallback={<div style={{ padding: 20 }}>Loading...</div>}>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/users" element={<UsersPage />} />
              <Route path="/exchanges" element={<ExchangesPage />} />
              <Route path="/config" element={<PageConfig />} />
              <Route path="/news" element={<NewsPage />} />
              <Route path="*" element={<Page title="404">Сторінку не знайдено.</Page>} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </div>
  );
}
