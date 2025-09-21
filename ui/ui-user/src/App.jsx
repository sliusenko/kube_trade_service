import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";

const Page = ({ title, children }) => (
  <div className="p-6">
    <h1 style={{ fontSize: 28, marginBottom: 12 }}>{title}</h1>
    <div>{children}</div>
  </div>
);

const Overview = () => <Page title="Shell Overview">Огляд стратегії/бота.</Page>;
const Logs = () => <Page title="Logs">Логи роботи Shell.</Page>;
const Health = () => <Page title="Health">Моніторинг / життєздатність.</Page>;

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
      <aside style={{ borderRight: "1px solid #e5e7eb", padding: 16 }}>
        <div style={{ fontWeight: 800, marginBottom: 16 }}>Shell UI</div>
        <nav style={{ display: "grid", gap: 6 }}>
          <NavLink to="/" style={navStyle} end>Overview</NavLink>
          <NavLink to="/logs" style={navStyle}>Logs</NavLink>
          <NavLink to="/health" style={navStyle}>Health</NavLink>
        </nav>
      </aside>

      <main>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/health" element={<Health />} />
          <Route path="*" element={<Page title="404">Сторінку не знайдено.</Page>} />
        </Routes>
      </main>
    </div>
  );
}
