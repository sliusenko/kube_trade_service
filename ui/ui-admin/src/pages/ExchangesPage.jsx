import React, { useEffect, useState } from "react";
import {
  getExchanges,
  createExchange,
  updateExchange,
  deleteExchange,
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
  const [selectedId, setSelectedId] = useState("");
  const [formData, setFormData] = useState({ name: "", type: "", is_active: false });

  const [symbols, setSymbols] = useState([]);
  const [limits, setLimits] = useState([]);
  const [history, setHistory] = useState([]);

  // load all exchanges
  const fetchExchanges = async () => {
    try {
      const data = await getExchanges();
      setExchanges(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchExchanges();
  }, []);

  // when user selects exchange
  useEffect(() => {
    if (!selectedId) {
      setFormData({ name: "", type: "", is_active: false });
      return;
    }
    const ex = exchanges.find((e) => e.id === selectedId);
    if (ex) setFormData(ex);
  }, [selectedId, exchanges]);

  // load symbols/limits/history for selected exchange
  useEffect(() => {
    if (!selectedId) return;
    if (activeTab === "SYMBOLS") {
      getExchangeSymbols(selectedId).then(setSymbols).catch(console.error);
    } else if (activeTab === "LIMITS") {
      getExchangeLimits(selectedId).then(setLimits).catch(console.error);
    } else if (activeTab === "HISTORY") {
      getExchangeHistory(selectedId).then(setHistory).catch(console.error);
    }
  }, [activeTab, selectedId]);

  // handlers
  const handleCreate = async () => {
    await createExchange(formData);
    fetchExchanges();
  };

  const handleUpdate = async () => {
    if (!selectedId) return;
    await updateExchange(selectedId, formData);
    fetchExchanges();
  };

  const handleDelete = async () => {
    if (!selectedId) return;
    await deleteExchange(selectedId);
    setSelectedId("");
    fetchExchanges();
  };

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

      {/* --- EXCHANGES TAB --- */}
      {activeTab === "EXCHANGES" && (
        <>
          {/* dropdown + buttons */}
          <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
            <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)}>
              <option value="">-- select exchange --</option>
              {exchanges.map((ex) => (
                <option key={ex.id} value={ex.id}>
                  {ex.name}
                </option>
              ))}
            </select>

            <button onClick={handleCreate} className="btn btn-success">Create</button>
            <button onClick={handleUpdate} className="btn btn-primary">Update</button>
            <button onClick={handleDelete} className="btn btn-danger">Delete</button>
          </div>

          {/* form */}
          <div style={{ maxWidth: 800 }}>
            {/* Read-only */}
            <div className="row">
              <div className="col-md-4 mb-3">
                <label>ID</label>
                <input type="text" value={formData.id || ""} readOnly className="form-control" />
              </div>
              <div className="col-md-4 mb-3">
                <label>Created At</label>
                <input type="text" value={formData.created_at || ""} readOnly className="form-control" />
              </div>
              <div className="col-md-4 mb-3">
                <label>Updated At</label>
                <input type="text" value={formData.updated_at || ""} readOnly className="form-control" />
              </div>
            </div>

             {/* Editable core */}
            <div className="row">
              <div className="col-md-6 mb-3">
                <label>Code</label>
                <input type="text" value={formData.code || ""}
                  onChange={(e) => setFormData({ ...formData, code: e.target.value })} className="form-control" />
              </div>
              <div className="col-md-6 mb-3">
                <label>Name</label>
                <input type="text" value={formData.name || ""}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="form-control" />
              </div>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <label>Kind</label>
                <select value={formData.kind || "spot"}
                  onChange={(e) => setFormData({ ...formData, kind: e.target.value })} className="form-select">
                  <option value="spot">spot</option>
                  <option value="futures">futures</option>
                  <option value="margin">margin</option>
                </select>
              </div>
              <div className="col-md-6 mb-3">
                <label>Environment</label>
                <select value={formData.environment || "prod"}
                  onChange={(e) => setFormData({ ...formData, environment: e.target.value })} className="form-select">
                  <option value="prod">prod</option>
                  <option value="test">test</option>
                  <option value="dev">dev</option>
                </select>
              </div>
            </div>

            {/* URLs */}
            {["base_url_public", "base_url_private", "ws_public_url", "ws_private_url", "data_feed_url"].map((f) => (
              <div className="mb-3" key={f}>
                <label>{f.replace(/_/g, " ")}</label>
                <input type="text" value={formData[f] || ""}
                  onChange={(e) => setFormData({ ...formData, [f]: e.target.value })} className="form-control" />
              </div>
            ))}

            {/* Intervals */}
            <div className="row">
              <div className="col-md-4 mb-3">
                <label>Fetch Symbols Interval (min)</label>
                <input type="number" value={formData.fetch_symbols_interval_min || ""}
                  onChange={(e) => setFormData({ ...formData, fetch_symbols_interval_min: e.target.value })} className="form-control" />
              </div>
              <div className="col-md-4 mb-3">
                <label>Fetch Filters Interval (min)</label>
                <input type="number" value={formData.fetch_filters_interval_min || ""}
                  onChange={(e) => setFormData({ ...formData, fetch_filters_interval_min: e.target.value })} className="form-control" />
              </div>
              <div className="col-md-4 mb-3">
                <label>Fetch Limits Interval (min)</label>
                <input type="number" value={formData.fetch_limits_interval_min || ""}
                  onChange={(e) => setFormData({ ...formData, fetch_limits_interval_min: e.target.value })} className="form-control" />
              </div>
            </div>

            {/* Limits */}
            <div className="row">
              <div className="col-md-4 mb-3">
                <label>Rate Limit per min</label>
                <input type="number" value={formData.rate_limit_per_min || ""}
                  onChange={(e) => setFormData({ ...formData, rate_limit_per_min: e.target.value })} className="form-control" />
              </div>
              <div className="col-md-4 mb-3">
                <label>Recv Window (ms)</label>
                <input type="number" value={formData.recv_window_ms || ""}
                  onChange={(e) => setFormData({ ...formData, recv_window_ms: e.target.value })} className="form-control" />
              </div>
              <div className="col-md-4 mb-3">
                <label>Request Timeout (ms)</label>
                <input type="number" value={formData.request_timeout_ms || ""}
                  onChange={(e) => setFormData({ ...formData, request_timeout_ms: e.target.value })} className="form-control" />
              </div>
            </div>

            {/* Status */}
            <div className="row">
              <div className="col-md-6 mb-3">
                <label>Status</label>
                <input type="text" value={formData.status || ""}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })} className="form-control" />
              </div>
              <div className="col-md-6 mb-3">
                <label>Status Msg</label>
                <input type="text" value={formData.status_msg || ""}
                  onChange={(e) => setFormData({ ...formData, status_msg: e.target.value })} className="form-control" />
              </div>
            </div>

            {/* JSON */}
            <div className="mb-3">
              <label>Features (JSON)</label>
              <textarea value={JSON.stringify(formData.features || {}, null, 2)}
                onChange={(e) => { try { setFormData({ ...formData, features: JSON.parse(e.target.value) }); } catch {} }}
                className="form-control" rows={3} />
            </div>

            <div className="mb-3">
              <label>Extra (JSON)</label>
              <textarea value={JSON.stringify(formData.extra || {}, null, 2)}
                onChange={(e) => { try { setFormData({ ...formData, extra: JSON.parse(e.target.value) }); } catch {} }}
                className="form-control" rows={3} />
            </div>

            {/* Active */}
            <div className="mb-3 form-check">
              <input type="checkbox" className="form-check-input" checked={formData.is_active || false}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })} />
              <label className="form-check-label">Active</label>
            </div>

            {/* Last refresh times */}
            {["last_symbols_refresh_at", "last_filters_refresh_at", "last_limits_refresh_at"].map((f) => (
              <div className="mb-3" key={f}>
                <label>{f.replace(/_/g, " ")}</label>
                <input type="text" value={formData[f] || ""} readOnly className="form-control" />
              </div>
            ))}
          </div>
        </>
      )}


      {/* --- SYMBOLS TAB --- */}
      {activeTab === "SYMBOLS" && selectedId && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Base</th>
              <th>Quote</th>
            </tr>
          </thead>
          <tbody>
            {symbols.map((s) => (
              <tr key={s.id}>
                <td>{s.symbol}</td>
                <td>{s.base_asset}</td>
                <td>{s.quote_asset}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* --- LIMITS TAB --- */}
      {activeTab === "LIMITS" && selectedId && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Min Qty</th>
              <th>Max Qty</th>
              <th>Step Size</th>
            </tr>
          </thead>
          <tbody>
            {limits.map((l, idx) => (
              <tr key={idx}>
                <td>{l.symbol}</td>
                <td>{l.min_qty}</td>
                <td>{l.max_qty}</td>
                <td>{l.step_size}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* --- HISTORY TAB --- */}
      {activeTab === "HISTORY" && selectedId && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Status</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h, idx) => (
              <tr key={idx}>
                <td>{h.timestamp}</td>
                <td>{h.status}</td>
                <td>{h.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
