// src/pages/ExchangesPage.jsx
import React, { useEffect, useState } from "react";
import Form from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import { ExchangeFormSchema, ExchangeCredentialFormSchema } from "../forms/schemas";
import {
  getExchanges,
  getExchange,
  createExchange,
  updateExchange,
  deleteExchange,
  getExchangeCredentials,
  getExchangeCredential,
  createExchangeCredential,
  updateExchangeCredential,
  deleteExchangeCredential,
} from "../api/exchanges";
import {
  getExchangeSymbols,
  getExchangeLimits,
  getExchangeFees,
  getExchangeHistory,
} from "../api/exchange_service_tb";
import {
  Button,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
} from "@mui/material";
import { Add, Edit, Delete } from "@mui/icons-material";

const TabButton = ({ label, active, onClick }) => (
  <Button
    variant={active ? "contained" : "outlined"}
    color={active ? "primary" : "secondary"}
    onClick={onClick}
    style={{ marginRight: "10px" }}
  >
    {label}
  </Button>
);

export default function ExchangesPage() {
  const [activeTab, setActiveTab] = useState("EXCHANGES");
  const [exchanges, setExchanges] = useState([]);
  const [selectedExchange, setSelectedExchange] = useState(""); // тільки id
  const [formData, setFormData] = useState({});
  const [symbols, setSymbols] = useState([]);
  const [limits, setLimits] = useState([]);
  const [fees, setFees] = useState([]);
  const [history, setHistory] = useState([]);
  const [credentials, setCredentials] = useState([]);

  useEffect(() => {
    reloadExchanges();
  }, []);

  useEffect(() => {
    if (!selectedExchange) return;

    if (activeTab === "SYMBOLS") {
      getExchangeSymbols(selectedExchange).then(setSymbols);
    }
    if (activeTab === "LIMITS&FEES") {
      getExchangeLimits(selectedExchange).then(setLimits);
      getExchangeFees(selectedExchange).then(setFees);
    }
    if (activeTab === "HISTORY") {
      getExchangeHistory(selectedExchange).then(setHistory);
    }
    if (activeTab === "CREDENTIALS") {
      getExchangeCredentials(selectedExchange).then(setCredentials);
    }
  }, [activeTab, selectedExchange]);

  const reloadExchanges = () => {
    getExchanges().then(setExchanges);
  };

  const getCurrentSchema = () => {
    switch (activeTab) {
      case "EXCHANGES":
        return ExchangeFormSchema;
      case "CREDENTIALS":
        return ExchangeCredentialFormSchema;
      default:
        return null;
    }
  };

  const getUiSchema = () => {
    if (activeTab === "CREDENTIALS") {
      return {
        api_key: { "ui:widget": "password" },
        api_secret: { "ui:widget": "password" },
        api_passphrase: { "ui:widget": "password" },
        subaccount: { "ui:widget": "text" },
        label: { "ui:widget": "text" },
        is_service: { "ui:widget": "checkbox" },
        is_active: { "ui:widget": "checkbox" },
      };
    }
    return {};
  };

  // -----------------------------
  // CRUD для Exchanges + Credentials
  // -----------------------------
  const handleCreate = async () => {
    if (activeTab === "EXCHANGES") {
      const newEx = await createExchange(formData);
      reloadExchanges();
      setSelectedExchange(newEx.id);
      setFormData(newEx);
    }
    if (activeTab === "CREDENTIALS" && selectedExchange) {
      await createExchangeCredential(selectedExchange, formData);
      getExchangeCredentials(selectedExchange).then(setCredentials);
      setFormData({});
    }
  };

  const handleUpdate = async () => {
    if (activeTab === "EXCHANGES" && selectedExchange) {
      await updateExchange(selectedExchange, formData);
      reloadExchanges();
    }
    if (activeTab === "CREDENTIALS" && selectedExchange && formData.id) {
      await updateExchangeCredential(selectedExchange, formData.id, formData);
      getExchangeCredentials(selectedExchange).then(setCredentials);
    }
  };

  const handleDelete = async () => {
    if (activeTab === "EXCHANGES" && selectedExchange) {
      await deleteExchange(selectedExchange);
      reloadExchanges();
      setSelectedExchange("");
      setFormData({});
    }
    if (activeTab === "CREDENTIALS" && selectedExchange && formData.id) {
      await deleteExchangeCredential(selectedExchange, formData.id);
      getExchangeCredentials(selectedExchange).then(setCredentials);
      setFormData({});
    }
  };

  // -----------------------------
  // Handlers для кліків по таблиці
  // -----------------------------
  const handleExchangeClick = async (id) => {
    setSelectedExchange(id);
    const full = await getExchange(id);
    setFormData(full);
  };

  const handleCredentialClick = async (id) => {
    const full = await getExchangeCredential(selectedExchange, id);
    setFormData(full);
  };

  return (
    <div className="container mt-4">
      <h2>Exchanges</h2>

      {/* Вкладки */}
      <div style={{ marginBottom: "20px" }}>
        {["EXCHANGES", "CREDENTIALS", "SYMBOLS", "LIMITS&FEES", "HISTORY"].map((tab) => (
          <TabButton
            key={tab}
            label={tab}
            active={activeTab === tab}
            onClick={() => {
              setActiveTab(tab);
              setFormData({});
            }}
          />
        ))}
      </div>

      {/* Dropdown для вибору біржі */}
      {(activeTab === "EXCHANGES" || activeTab === "CREDENTIALS") && (
        <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
          <select
            className="form-select"
            value={selectedExchange}
            onChange={(e) => {
              setSelectedExchange(e.target.value);
              const found = exchanges.find((ex) => ex.id === e.target.value);
              setFormData(found || {});
            }}
            style={{ maxWidth: "250px" }}
          >
            <option value="">-- select exchange --</option>
            {exchanges.map((ex) => (
              <option key={ex.id} value={ex.id}>
                {ex.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Форма + кнопки CRUD */}
      {getCurrentSchema() ? (
        <Form
          schema={getCurrentSchema()}
          uiSchema={getUiSchema()}
          validator={validator}
          formData={formData}
          onChange={(e) => setFormData(e.formData)}
          noHtml5Validate
        >
          <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
            <Button variant="contained" color="primary" startIcon={<Add />} onClick={handleCreate}>
              Create
            </Button>
            <Button
              variant="outlined"
              color="secondary"
              startIcon={<Edit />}
              disabled={!selectedExchange}
              onClick={handleUpdate}
            >
              Update
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<Delete />}
              disabled={!selectedExchange}
              onClick={handleDelete}
            >
              Delete
            </Button>
          </div>
        </Form>
      ) : (
        (activeTab === "EXCHANGES" || activeTab === "CREDENTIALS") && (
          <p style={{ color: "red", marginTop: "10px" }}>❌ Schema for {activeTab} not found</p>
        )
      )}

      {/* EXCHANGES таблиця */}
      {activeTab === "EXCHANGES" && (
        <Paper style={{ marginTop: "20px" }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Code</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Kind</TableCell>
                <TableCell>Environment</TableCell>
                <TableCell>Rate Limit</TableCell>
                <TableCell>Active</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {exchanges.map((ex) => (
                <TableRow
                  key={ex.id}
                  onClick={() => handleExchangeClick(ex.id)}
                  style={{ cursor: "pointer" }}
                >
                  <TableCell>{ex.code}</TableCell>
                  <TableCell>{ex.name}</TableCell>
                  <TableCell>{ex.kind}</TableCell>
                  <TableCell>{ex.environment}</TableCell>
                  <TableCell>{ex.rate_limit_per_min || "-"}</TableCell>
                  <TableCell>{ex.is_active ? "Yes" : "No"}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}

      {/* CREDENTIALS таблиця */}
      {activeTab === "CREDENTIALS" && (
        <Paper style={{ marginTop: "20px" }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Label</TableCell>
                <TableCell>Valid From</TableCell>
                <TableCell>Valid To</TableCell>
                <TableCell>Active</TableCell>
                <TableCell>Created At</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {credentials.map((c) => (
                <TableRow
                  key={c.id}
                  onClick={() => handleCredentialClick(c.id)}
                  style={{ cursor: "pointer" }}
                >
                  <TableCell>{c.label}</TableCell>
                  <TableCell>{c.valid_from || "-"}</TableCell>
                  <TableCell>{c.valid_to || "-"}</TableCell>
                  <TableCell>{c.is_active ? "Yes" : "No"}</TableCell>
                  <TableCell>{c.created_at}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}

      {/* SYMBOLS таблиця */}
      {activeTab === "SYMBOLS" && (
        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Exchange ID</TableCell>
                <TableCell>Symbol</TableCell>
                <TableCell>Active</TableCell>
                <TableCell>Base Asset</TableCell>
                <TableCell>Quote Asset</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {symbols.map((s) => (
                <TableRow key={s.id}>
                  <TableCell>{s.exchange_id}</TableCell>
                  <TableCell>{s.symbol}</TableCell>
                  <TableCell>{s.is_active ? "Yes" : "No"}</TableCell>
                  <TableCell>{s.base_asset}</TableCell>
                  <TableCell>{s.quote_asset}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}

      {/* LIMITS&FEES таблиці */}
      {activeTab === "LIMITS&FEES" && (
        <div>
          {/* LIMITS */}
          <Paper>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Limit Type</TableCell>
                  <TableCell>Interval Unit</TableCell>
                  <TableCell>Interval Num</TableCell>
                  <TableCell>Limit</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {limits.map((l) => (
                  <TableRow key={l.id}>
                    <TableCell>{l.id}</TableCell>
                    <TableCell>{l.limit_type}</TableCell>
                    <TableCell>{l.interval_unit}</TableCell>
                    <TableCell>{l.interval_num}</TableCell>
                    <TableCell>{l.limit}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
  
          {/* FEES */}
          <Paper>
            <h3 style={{ padding: "10px" }}>Fees</h3>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Volume Threshold</TableCell>
                  <TableCell>Maker Fee</TableCell>
                  <TableCell>Taker Fee</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {fees.map((f) => (
                  <TableRow key={f.id}>
                    <TableCell>{f.id}</TableCell>
                    <TableCell>{f.volume_threshold}</TableCell>
                    <TableCell>{f.maker_fee}</TableCell>
                    <TableCell>{f.taker_fee}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </div>
      )}

      {/* HISTORY таблиця */}
      {activeTab === "HISTORY" && (
        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Event</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Message</TableCell>
                <TableCell>Created At</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {history.map((h) => (
                <TableRow key={h.id}>
                  <TableCell>{h.id}</TableCell>
                  <TableCell>{h.event}</TableCell>
                  <TableCell>{h.status}</TableCell>
                  <TableCell>{h.message}</TableCell>
                  <TableCell>{h.created_at}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </div>
  );
}
