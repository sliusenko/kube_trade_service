import React, { useEffect, useState } from "react";
import {
  getExchanges,
  getExchangeSymbols,
  getExchangeLimits,
  getExchangeHistory,
} from "../api/exchanges";

const TabButton = ({ label, active, onClick }) => (
  <button
    onClick={onClick}
    style={{
      padding: "8px 14px",
      borderBottom: active ? "2px solid #1e40af" : "2px solid transparent",
      fontWeight: active ? 700 : 500,
      color: active ? "#1e40af" : "#374151",
      background: "none",
      cursor: "pointer",
    }}
  >
    {label}
  </button>
);

export default function ExchangesPage() {
  const [activeTab, setActiveTab] = useState("EXCHANGES");
  const [exchanges, setExchanges] = useState([]);
  const [selectedExchange, setSelectedExchange] = useState(null);
  const [symbols, setSymbols] = useState([]);
  const [limits, setLimits] = useState([]);
  const [history, setHistory] = useState([]);

  // завантаження всіх бірж
  useEffect(() => {
    getExchanges().then(setExchanges).catch(console.error);
  }, []);

  // завантаження даних по вибраній біржі
  useEffect(() => {
    if (!selectedExchange) return;

    if (activeTab === "SYMBOLS") {
      getExchangeSymbols(selectedExchange).then(setSymbols).catch(console.error);
    } else if (activeTab === "LIMITS") {
      getExchangeLimits(selectedExchange).then(setLimits).catch(console.error);
    } else if (activeTab === "HISTORY") {
      getExchangeHistory(selectedExchange).then(setHistory).catch(console.error);
    }
  }, [activeTab, selectedExchange]);

  return (
    <div className="p-6">
      <h1 style={{ fontSize: 28, marginBottom: 16 }}>Exchanges</h1>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
        <TabButton label="EXCHANGES" active={activeTab === "EXCHANGES"} onClick={() => setActiveTab("EXCHANGES")} />
        <TabButton label="SYMBOLS" active={activeTab === "SYMBOLS"} onClick={() => setActiveTab("SYMBOLS")} />
        <TabButton label="LIMITS" active={activeTab === "LIMITS"} onClick={() => setActiveTab("LIMITS")} />
        <TabButton label="HISTORY" active={activeTab === "HISTORY"} onClick={() => setActiveTab("HISTORY")} />
      </div>

      {/* Dropdown для вибору біржі */}
      {activeTab !== "EXCHANGES" && (
        <div style={{ marginBottom: 20 }}>
          <label style={{ marginRight: 10 }}>Select Exchange:</label>
          <select
            value={selectedExchange || ""}
            onChange={(e) => setSelectedExchange(e.target.value)}
          >
            <option value="">-- choose exchange --</option>
            {exchanges.map((ex) => (
              <option key={ex.id} value={ex.id}>
                {ex.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* EXCHANGES */}
      {activeTab === "EXCHANGES" && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>ID</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Name</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Type</th>
            </tr>
          </thead>
          <tbody>
            {exchanges.map((ex) => (
              <tr key={ex.id}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{ex.id}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{ex.name}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{ex.type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* SYMBOLS */}
      {activeTab === "SYMBOLS" && selectedExchange && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Symbol</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Base</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Quote</th>
            </tr>
          </thead>
          <tbody>
            {symbols.map((s) => (
              <tr key={s.id}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{s.symbol}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{s.base_asset}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{s.quote_asset}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* LIMITS */}
      {activeTab === "LIMITS" && selectedExchange && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Symbol</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Min Qty</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Max Qty</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Step Size</th>
            </tr>
          </thead>
          <tbody>
            {limits.map((l, idx) => (
              <tr key={idx}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{l.symbol}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{l.min_qty}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{l.max_qty}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{l.step_size}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* HISTORY */}
      {activeTab === "HISTORY" && selectedExchange && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Timestamp</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Status</th>
              <th style={{ borderBottom: "1px solid #ddd", padding: 8 }}>Message</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h, idx) => (
              <tr key={idx}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{h.timestamp}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{h.status}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{h.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
