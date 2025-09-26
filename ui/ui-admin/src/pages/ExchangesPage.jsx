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

import {
  getExchangeCredentials,
  createExchangeCredential,
  updateExchangeCredential,
  deleteExchangeCredential,
} from "../api/exchange_credentials";

const TabButton = ({ label, active, onClick }) => (
  <button
    onClick={onClick}
    className={`btn ${active ? "btn-primary" : "btn-outline-secondary"}`}
    style={{ marginRight: 8 }}
  >
    {label}
  </button>
);

export default function ExchangesPage() {
  const [activeTab, setActiveTab] = useState("EXCHANGES");
  const [exchanges, setExchanges] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [formData, setFormData] = useState({});

  const [symbols, setSymbols] = useState([]);
  const [limits, setLimits] = useState([]);
  const [history, setHistory] = useState([]);

  const [credentials, setCredentials] = useState([]);
  const [selectedCredId, setSelectedCredId] = useState("");
  const [credForm, setCredForm] = useState({});

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
      setFormData({});
      return;
    }
    const ex = exchanges.find((e) => e.id === selectedId);
    if (ex) setFormData(ex);
  }, [selectedId, exchanges]);

  // load symbols/limits/history/credentials
  useEffect(() => {
    if (!selectedId) return;

    if (activeTab === "SYMBOLS") {
      getExchangeSymbols(selectedId).then(setSymbols).catch(console.error);
    } else if (activeTab === "LIMITS") {
      getExchangeLimits(selectedId).then(setLimits).catch(console.error);
    } else if (activeTab === "HISTORY") {
      getExchangeHistory(selectedId).then(setHistory).catch(console.error);
    } else if (activeTab === "CREDENTIALS") {
      getExchangeCredentials(selectedId).then(setCredentials).catch(console.error);
    }
  }, [activeTab, selectedId]);

  // handlers exchanges
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

  // handlers credentials
  const handleCredCreate = async () => {
    await createExchangeCredential(selectedId, credForm);
    getExchangeCredentials(selectedId).then(setCredentials);
  };

  const handleCredUpdate = async () => {
    if (!selectedCredId) return;
    await updateExchangeCredential(selectedId, selectedCredId, credForm);
    getExchangeCredentials(selectedId).then(setCredentials);
  };

  const handleCredDelete = async () => {
    if (!selectedCredId) return;
    await deleteExchangeCredential(selectedId, selectedCredId);
    setSelectedCredId("");
    getExchangeCredentials(selectedId).then(setCredentials);
  };

  return (
    <div className="container py-4">
      <h1 className="mb-4">Exchanges</h1>

      {/* Tabs */}
      <div className="mb-3">
        {["EXCHANGES", "CREDENTIALS", "SYMBOLS", "LIMITS", "HISTORY"].map((tab) => (
          <TabButton
            key={tab}
            label={tab}
            active={activeTab === tab}
            onClick={() => setActiveTab(tab)}
          />
        ))}
      </div>

      {/* --- EXCHANGES TAB --- */}
      {activeTab === "EXCHANGES" && (
        <>
          {/* dropdown + buttons */}
          <div className="d-flex gap-2 mb-3">
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="form-select"
              style={{ maxWidth: 300 }}
            >
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

          {/* form grid */}
          <div className="row g-3">
            <div className="col-md-4">
              <label className="form-label">Code</label>
              <input
                type="text"
                className="form-control"
                value={formData.code || ""}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Name</label>
              <input
                type="text"
                className="form-control"
                value={formData.name || ""}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div className="col-md-2">
              <label className="form-label">Kind</label>
              <select
                className="form-select"
                value={formData.kind || "spot"}
                onChange={(e) => setFormData({ ...formData, kind: e.target.value })}
              >
                <option>spot</option>
                <option>futures</option>
                <option>margin</option>
              </select>
            </div>
            <div className="col-md-2">
              <label className="form-label">Environment</label>
              <select
                className="form-select"
                value={formData.environment || "prod"}
                onChange={(e) => setFormData({ ...formData, environment: e.target.value })}
              >
                <option>prod</option>
                <option>dev</option>
                <option>test</option>
              </select>
            </div>

            <div className="col-md-6">
              <label className="form-label">Base URL Public</label>
              <input
                type="text"
                className="form-control"
                value={formData.base_url_public || ""}
                onChange={(e) => setFormData({ ...formData, base_url_public: e.target.value })}
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">Base URL Private</label>
              <input
                type="text"
                className="form-control"
                value={formData.base_url_private || ""}
                onChange={(e) => setFormData({ ...formData, base_url_private: e.target.value })}
              />
            </div>

            <div className="col-md-6">
              <label className="form-label">WS Public URL</label>
              <input
                type="text"
                className="form-control"
                value={formData.ws_public_url || ""}
                onChange={(e) => setFormData({ ...formData, ws_public_url: e.target.value })}
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">WS Private URL</label>
              <input
                type="text"
                className="form-control"
                value={formData.ws_private_url || ""}
                onChange={(e) => setFormData({ ...formData, ws_private_url: e.target.value })}
              />
            </div>

            <div className="col-md-12">
              <label className="form-label">Data Feed URL</label>
              <input
                type="text"
                className="form-control"
                value={formData.data_feed_url || ""}
                onChange={(e) => setFormData({ ...formData, data_feed_url: e.target.value })}
              />
            </div>

            <div className="col-md-4">
              <label className="form-label">Features (JSON)</label>
              <textarea
                rows={6}
                className="form-control font-monospace"
                value={JSON.stringify(formData.features || {}, null, 2)}
                onChange={(e) => {
                  try {
                    setFormData({ ...formData, features: JSON.parse(e.target.value) });
                  } catch {}
                }}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Extra (JSON)</label>
              <textarea
                rows={6}
                className="form-control font-monospace"
                value={JSON.stringify(formData.extra || {}, null, 2)}
                onChange={(e) => {
                  try {
                    setFormData({ ...formData, extra: JSON.parse(e.target.value) });
                  } catch {}
                }}
              />
            </div>
            <div className="col-md-4 d-flex align-items-center">
              <div className="form-check mt-4">
                <input
                  type="checkbox"
                  className="form-check-input"
                  checked={formData.is_active || false}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                />
                <label className="form-check-label">Active</label>
              </div>
            </div>
          </div>
        </>
      )}

      {/* --- CREDENTIALS TAB --- */}
      {activeTab === "CREDENTIALS" && selectedId && (
        <>
          <div className="d-flex gap-2 mb-3">
            <select
              value={selectedCredId}
              onChange={(e) => {
                setSelectedCredId(e.target.value);
                const c = credentials.find((cc) => cc.id === e.target.value);
                setCredForm(c || {});
              }}
              className="form-select"
              style={{ maxWidth: 300 }}
            >
              <option value="">-- select credential --</option>
              {credentials.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.label}
                </option>
              ))}
            </select>

            <button onClick={handleCredCreate} className="btn btn-success">Create</button>
            <button onClick={handleCredUpdate} className="btn btn-primary">Update</button>
            <button onClick={handleCredDelete} className="btn btn-danger">Delete</button>
          </div>

          <div className="row g-3">
            <div className="col-md-4">
              <label className="form-label">Label</label>
              <input
                type="text"
                className="form-control"
                value={credForm.label || ""}
                onChange={(e) => setCredForm({ ...credForm, label: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">API Key</label>
              <input
                type="text"
                className="form-control"
                value={credForm.api_key || ""}
                onChange={(e) => setCredForm({ ...credForm, api_key: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">API Secret</label>
              <input
                type="password"
                className="form-control"
                value={credForm.api_secret || ""}
                onChange={(e) => setCredForm({ ...credForm, api_secret: e.target.value })}
              />
            </div>

            <div className="col-md-4">
              <label className="form-label">Passphrase</label>
              <input
                type="text"
                className="form-control"
                value={credForm.api_passphrase || ""}
                onChange={(e) => setCredForm({ ...credForm, api_passphrase: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Subaccount</label>
              <input
                type="text"
                className="form-control"
                value={credForm.subaccount || ""}
                onChange={(e) => setCredForm({ ...credForm, subaccount: e.target.value })}
              />
            </div>
            <div className="col-md-4">
              <label className="form-label">Scopes (JSON)</label>
              <textarea
                rows={3}
                className="form-control font-monospace"
                value={JSON.stringify(credForm.scopes || [], null, 2)}
                onChange={(e) => {
                  try {
                    setCredForm({ ...credForm, scopes: JSON.parse(e.target.value) });
                  } catch {}
                }}
              />
            </div>
          </div>
        </>
      )}

      {/* --- SYMBOLS TAB --- */}
      {activeTab === "SYMBOLS" && selectedId && (
        <table className="table table-striped">
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
        <table className="table table-bordered">
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
        <table className="table table-hover">
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
