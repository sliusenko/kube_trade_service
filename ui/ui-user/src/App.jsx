import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";

const Page = ({ title, children }) => (
  <div className="p-6">
    <h1 style={{ fontSize: 28, marginBottom: 12 }}>{title}</h1>
    <div>{children}</div>
  </div>
);

const Home = () => <Page title="Home">Мій акаунт / баланс.</Page>;
const Strategies = () => <Page title="Strategies">Мої стратегії.</Page>;
const Activity = () => <Page title="Activity">Історія угод / активність.</Page>;

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
        <div style={{ fontWeight: 800, marginBottom: 16 }}>User UI</div>
        <nav style={{ display: "grid", gap: 6 }}>
          <NavLink to="/" style={navStyle} end>Home</NavLink>
          <NavLink to="/strategies" style={navStyle}>Strategies</NavLink>
          <NavLink to="/activity" style={navStyle}>Activity</NavLink>
        </nav>
      </aside>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/strategies" element={<Strategies />} />
          <Route path="/activity" element={<Activity />} />
          <Route path="*" element={<Page title="404">Сторінку не знайдено.</Page>} />
        </Routes>
      </main>
    </div>
  );
}
