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
          {/* form (6x4 grid, larger font) */}
          <div
            style={{
              --pad: '10px',
              --gap: '14px',
              --radius: '10px',
              fontSize: 16,                 // ↑ більший шрифт
              lineHeight: 1.25,
            }}
          >
            {/* панель керування */}
            <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 14 }}>
              <select
                value={selectedId}
                onChange={(e) => setSelectedId(e.target.value)}
                style={{ padding: '8px 10px', borderRadius: 8 }}
              >
                <option value="">— select exchange —</option>
                {exchanges.map((ex) => (
                  <option key={ex.id} value={ex.id}>{ex.name}</option>
                ))}
              </select>

              <button className="btn btn-success">Create</button>
              <button className="btn btn-primary">Update</button>
              <button className="btn btn-danger">Delete</button>
            </div>

            {/* матриця 6x4 */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(6, minmax(0, 1fr))',
                gap: '14px',
                alignItems: 'start',
              }}
            >
              {/* helper стилі */}
              {/*
                Кожен "Cell" — це label + input з однаковим оформленням.
                Через style={{gridColumn: 'span N'}} керуємо шириною.
              */}
              {[
                // --- Row 1
                { label: 'ID', ro: true, value: formData.id || '', span: 2 },
                { label: 'Created At', ro: true, value: formData.created_at || '', span: 2 },
                { label: 'Updated At', ro: true, value: formData.updated_at || '', span: 2 },

                // --- Row 2
                { label: 'Code', key: 'code', value: formData.code || '', span: 2 },
                { label: 'Name', key: 'name', value: formData.name || '', span: 2 },
                {
                  label: 'Kind',
                  key: 'kind',
                  type: 'select',
                  options: ['spot', 'futures', 'margin'],
                  value: formData.kind || 'spot',
                  span: 1,
                },
                {
                  label: 'Environment',
                  key: 'environment',
                  type: 'select',
                  options: ['prod', 'dev', 'test'],
                  value: formData.environment || 'prod',
                  span: 1,
                },

                // --- Row 3
                { label: 'base url public', key: 'base_url_public', value: formData.base_url_public || '', span: 3 },
                { label: 'base url private', key: 'base_url_private', value: formData.base_url_private || '', span: 3 },

                // --- Row 4
                { label: 'ws public url', key: 'ws_public_url', value: formData.ws_public_url || '', span: 3 },
                { label: 'ws private url', key: 'ws_private_url', value: formData.ws_private_url || '', span: 3 },

                // --- Next row (поза 6×4; усе ще в одній грід-сітці)
                { label: 'data feed url', key: 'data_feed_url', value: formData.data_feed_url || '', span: 6 },

                { label: 'Fetch Symbols Interval (min)', key: 'fetch_symbols_interval_min', type: 'number', value: formData.fetch_symbols_interval_min ?? '', span: 2 },
                { label: 'Fetch Filters Interval (min)', key: 'fetch_filters_interval_min', type: 'number', value: formData.fetch_filters_interval_min ?? '', span: 2 },
                { label: 'Fetch Limits Interval (min)', key: 'fetch_limits_interval_min', type: 'number', value: formData.fetch_limits_interval_min ?? '', span: 2 },

                { label: 'Rate Limit per min', key: 'rate_limit_per_min', type: 'number', value: formData.rate_limit_per_min ?? '', span: 2 },
                { label: 'Recv Window (ms)', key: 'recv_window_ms', type: 'number', value: formData.recv_window_ms ?? '', span: 2 },
                { label: 'Request Timeout (ms)', key: 'request_timeout_ms', type: 'number', value: formData.request_timeout_ms ?? '', span: 2 },

                { label: 'Status', key: 'status', value: formData.status || '', span: 3 },
                { label: 'Status Msg', key: 'status_msg', value: formData.status_msg || '', span: 3 },
              ].map((f, i) => (
                <div key={i} style={{ gridColumn: `span ${f.span || 1}` }}>
                  <label style={{ display: 'block', fontWeight: 600, marginBottom: 6 }}>{f.label}</label>

                  {f.ro ? (
                    <input
                      type="text"
                      readOnly
                      value={f.value}
                      className="form-control"
                      style={{ padding: '10px 12px', borderRadius: '10px' }}
                    />
                  ) : f.type === 'select' ? (
                    <select
                      value={f.value}
                      onChange={(e) => setFormData({ ...formData, [f.key]: e.target.value })}
                      className="form-select"
                      style={{ padding: '10px 12px', borderRadius: '10px' }}
                    >
                      {f.options.map((opt) => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type={f.type || 'text'}
                      value={f.value}
                      onChange={(e) => setFormData({ ...formData, [f.key]: e.target.value })}
                      className="form-control"
                      style={{ padding: '10px 12px', borderRadius: '10px' }}
                    />
                  )}
                </div>
              ))}

              {/* JSON зручніше читати широкими — по 3 колонки кожен */}
              <div style={{ gridColumn: 'span 3' }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 6 }}>Features (JSON)</label>
                <textarea
                  rows={10}
                  value={JSON.stringify(formData.features || {}, null, 2)}
                  onChange={(e) => { try { setFormData({ ...formData, features: JSON.parse(e.target.value) }); } catch {} }}
                  className="form-control"
                  style={{ padding: '10px 12px', borderRadius: '10px', fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' }}
                />
              </div>

              <div style={{ gridColumn: 'span 3' }}>
                <label style={{ display: 'block', fontWeight: 600, marginBottom: 6 }}>Extra (JSON)</label>
                <textarea
                  rows={10}
                  value={JSON.stringify(formData.extra || {}, null, 2)}
                  onChange={(e) => { try { setFormData({ ...formData, extra: JSON.parse(e.target.value) }); } catch {} }}
                  className="form-control"
                  style={{ padding: '10px 12px', borderRadius: '10px', fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' }}
                />
              </div>

              {/* Checkbox + last refresh (read-only) */}
              <div style={{ gridColumn: 'span 1', display: 'flex', alignItems: 'center', gap: 8, marginTop: 8 }}>
                <input
                  type="checkbox"
                  className="form-check-input"
                  checked={formData.is_active || false}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                />
                <span style={{ fontWeight: 600 }}>Active</span>
              </div>

              {['last_symbols_refresh_at', 'last_filters_refresh_at', 'last_limits_refresh_at'].map((f) => (
                <div key={f} style={{ gridColumn: 'span 2' }}>
                  <label style={{ display: 'block', fontWeight: 600, marginBottom: 6 }}>{f.replace(/_/g, ' ')}</label>
                  <input
                    type="text"
                    readOnly
                    value={formData[f] || ''}
                    className="form-control"
                    style={{ padding: '10px 12px', borderRadius: '10px' }}
                  />
                </div>
              ))}
            </div>
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
