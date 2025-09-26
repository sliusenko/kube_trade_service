import React, { useEffect, useState } from "react";
import Form from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {
  getExchanges,
  createExchange,
  updateExchange,
  deleteExchange,
  getExchangeCredentials,
  createExchangeCredential,
  updateExchangeCredential,
  deleteExchangeCredential,
} from "../api/exchanges";
import {
  getExchangeSymbols,
  getExchangeLimits,
  getExchangeHistory,
} from "../api/exchange_service_tb";
import { getSchema } from "../api/schema";
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
  const [selectedExchange, setSelectedExchange] = useState(null);
  const [schemas, setSchemas] = useState({});
  const [formData, setFormData] = useState({});
  const [symbols, setSymbols] = useState([]);
  const [limits, setLimits] = useState([]);
  const [history, setHistory] = useState([]);
  const [credentials, setCredentials] = useState([]);

  // Завантажуємо список бірж і схеми
  useEffect(() => {
    reloadExchanges();
    getSchema().then((schema) => {
      setSchemas(schema.components.schemas || {});
    });
  }, []);

  // Коли змінюється вкладка або вибраний Exchange → тягнемо відповідні дані
  useEffect(() => {
    if (!selectedExchange) return;

    if (activeTab === "SYMBOLS") {
      getExchangeSymbols(selectedExchange.id).then(setSymbols);
    }
    if (activeTab === "LIMITS") {
      getExchangeLimits(selectedExchange.id).then(setLimits);
    }
    if (activeTab === "HISTORY") {
      getExchangeHistory(selectedExchange.id).then(setHistory);
    }
    if (activeTab === "CREDENTIALS") {
      getExchangeCredentials(selectedExchange.id).then(setCredentials);
    }
  }, [activeTab, selectedExchange]);

  const reloadExchanges = () => {
    getExchanges().then(setExchanges);
  };

  const getCurrentSchema = () => {
    switch (activeTab) {
      case "EXCHANGES":
        return schemas.ExchangeCreate;
      case "CREDENTIALS":
        return schemas.ExchangeCredentialCreate;
      default:
        return null;
    }
  };

  // -----------------------------
  // CRUD для Exchanges + Credentials
  // -----------------------------

  const handleCreate = async () => {
    if (activeTab === "EXCHANGES") {
      await createExchange(formData);
      reloadExchanges();
      setFormData({});
    }
    if (activeTab === "CREDENTIALS" && selectedExchange) {
      await createExchangeCredential(selectedExchange.id, formData);
      getExchangeCredentials(selectedExchange.id).then(setCredentials);
      setFormData({});
    }
  };

  const handleUpdate = async () => {
    if (activeTab === "EXCHANGES" && selectedExchange) {
      await updateExchange(selectedExchange.id, formData);
      reloadExchanges();
    }
    if (activeTab === "CREDENTIALS" && selectedExchange) {
      await updateExchangeCredential(selectedExchange.id, formData.id, formData);
      getExchangeCredentials(selectedExchange.id).then(setCredentials);
    }
  };

  const handleDelete = async () => {
    if (activeTab === "EXCHANGES" && selectedExchange) {
      await deleteExchange(selectedExchange.id);
      reloadExchanges();
      setSelectedExchange(null);
      setFormData({});
    }
    if (activeTab === "CREDENTIALS" && selectedExchange) {
      await deleteExchangeCredential(selectedExchange.id, formData.id);
      getExchangeCredentials(selectedExchange.id).then(setCredentials);
      setFormData({});
    }
  };

  return (
    <div className="container mt-4">
      <h2>Exchanges</h2>

      {/* Вкладки */}
      <div style={{ marginBottom: "20px" }}>
        <TabButton
          label="EXCHANGES"
          active={activeTab === "EXCHANGES"}
          onClick={() => setActiveTab("EXCHANGES")}
        />
        <TabButton
          label="CREDENTIALS"
          active={activeTab === "CREDENTIALS"}
          onClick={() => setActiveTab("CREDENTIALS")}
        />
        <TabButton
          label="SYMBOLS"
          active={activeTab === "SYMBOLS"}
          onClick={() => setActiveTab("SYMBOLS")}
        />
        <TabButton
          label="LIMITS"
          active={activeTab === "LIMITS"}
          onClick={() => setActiveTab("LIMITS")}
        />
        <TabButton
          label="HISTORY"
          active={activeTab === "HISTORY"}
          onClick={() => setActiveTab("HISTORY")}
        />
      </div>

      {/* Dropdown + CRUD тільки для EXCHANGES/CREDENTIALS */}
      {(activeTab === "EXCHANGES" || activeTab === "CREDENTIALS") && (
        <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
          <select
            className="form-select"
            value={selectedExchange?.id || ""}
            onChange={(e) => {
              const ex = exchanges.find((x) => x.id === e.target.value);
              setSelectedExchange(ex || null);
              setFormData(ex || {});
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

          <Button
            variant="contained"
            color="primary"
            startIcon={<Add />}
            onClick={handleCreate}
          >
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
      )}

      {/* Форма */}
      {getCurrentSchema() && (
        <Form
          schema={getCurrentSchema()}
          validator={validator}
          formData={formData}
          onChange={(e) => setFormData(e.formData)}
        />
      )}

      {/* CREDENTIALS таблиця */}
      {activeTab === "CREDENTIALS" && (
        <Paper style={{ marginTop: "20px" }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Label</TableCell>
                <TableCell>API Key</TableCell>
                <TableCell>Active</TableCell>
                <TableCell>Created At</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {credentials.map((c) => (
                <TableRow
                  key={c.id}
                  onClick={() => setFormData(c)} // вибір для редагування
                  style={{ cursor: "pointer" }}
                >
                  <TableCell>{c.id}</TableCell>
                  <TableCell>{c.label}</TableCell>
                  <TableCell>{c.api_key}</TableCell>
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
                <TableCell>ID</TableCell>
                <TableCell>Symbol</TableCell>
                <TableCell>Base Asset</TableCell>
                <TableCell>Quote Asset</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {symbols.map((s) => (
                <TableRow key={s.id}>
                  <TableCell>{s.id}</TableCell>
                  <TableCell>{s.symbol}</TableCell>
                  <TableCell>{s.base_asset}</TableCell>
                  <TableCell>{s.quote_asset}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}

      {/* LIMITS таблиця */}
      {activeTab === "LIMITS" && (
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
      )}

      {/* HISTORY таблиця */}
      {activeTab === "HISTORY" && (
        <Paper>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Message</TableCell>
                <TableCell>Created At</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {history.map((h) => (
                <TableRow key={h.id}>
                  <TableCell>{h.id}</TableCell>
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
