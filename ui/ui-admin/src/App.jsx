import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import UsersPage from "./pages/UsersPage";
import ExchangesPage from "./pages/ExchangesPage";   // ✅ новий імпорт

// універсальний шаблон сторінки
const Page = ({ title, children }) => (
  <div className="p-6">
    <h1 style={{ fontSize: 28, marginBottom: 12 }}>{title}</h1>
    <div>{children}</div>
  </div>
);

// заглушки
const Dashboard = () => <Page title="Dashboard">Стартовий огляд.</Page>;
const Settings = () => <Page title="Settings">Загальні налаштування.</Page>;

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
      <aside style={{ borderRight: "1px solid #e5e7eb", padding: 16 }}>
        <div style={{ fontWeight: 800, marginBottom: 16 }}>Admin Panel</div>
        <nav style={{ display: "grid", gap: 6 }}>
          <NavLink to="/" style={navStyle} end>Dashboard</NavLink>
          <NavLink to="/users" style={navStyle}>Users</NavLink>
          <NavLink to="/exchanges" style={navStyle}>Exchanges</NavLink>
          <NavLink to="/pairs" style={navStyle}>Pairs</NavLink>
          <NavLink to="/settings" style={navStyle}>Settings</NavLink>
        </nav>
      </aside>

      {/* Main content */}
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/exchanges" element={<ExchangesPage />} /> {/* ✅ тепер справжня сторінка */}
          <Route path="/pairs" element={<Pairs />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Page title="404">Сторінку не знайдено.</Page>} />
        </Routes>
      </main>
    </div>
  );
}
