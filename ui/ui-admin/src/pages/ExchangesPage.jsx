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
  const [selectedExchange, setSelectedExchange] = useState(""); // тільки id
  const [schemas, setSchemas] = useState({});
  const [formData, setFormData] = useState({});
  const [symbols, setSymbols] = useState([]);
  const [limits, setLimits] = useState([]);
  const [history, setHistory] = useState([]);
  const [credentials, setCredentials] = useState([]);

  useEffect(() => {
    reloadExchanges();
    getSchema().then((schema) => {
      setSchemas(schema.components.schemas || {});
    });
  }, []);

  useEffect(() => {
    if (!selectedExchange) return;

    if (activeTab === "SYMBOLS") {
      getExchangeSymbols(selectedExchange).then(setSymbols);
    }
    if (activeTab === "LIMITS") {
      getExchangeLimits(selectedExchange).then(setLimits);
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
        return schemas.ExchangeCreate;
      case "CREDENTIALS":
        return schemas.ExchangeCredentialCreate;
      default:
        return null;
    }
  };

  // UI Schema для правильного відображення форм
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
      await createExchange(formData);
      reloadExchanges();
      setFormData({});
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

  return (
    <div className="container mt-4">
      <h2>Exchanges</h2>

      {/* Вкладки */}
      <div style={{ marginBottom: "20px" }}>
        <TabButton
          label="EXCHANGES"
          active={activeTab === "EXCHANGES"}
          onClick={() => {
            setActiveTab("EXCHANGES");
            setFormData({});
          }}
        />
        <TabButton
          label="CREDENTIALS"
          active={activeTab === "CREDENTIALS"}
          onClick={() => {
            setActiveTab("CREDENTIALS");
            setFormData({});
          }}
        />
        <TabButton
          label="SYMBOLS"
          active={activeTab === "SYMBOLS"}
          onClick={() => {
            setActiveTab("SYMBOLS");
            setFormData({});
          }}
        />
        <TabButton
          label="LIMITS"
          active={activeTab === "LIMITS"}
          onClick={() => {
            setActiveTab("LIMITS");
            setFormData({});
          }}
        />
        <TabButton
          label="HISTORY"
          active={activeTab === "HISTORY"}
          onClick={() => {
            setActiveTab("HISTORY");
            setFormData({});
          }}
        />
      </div>

      {/* Dropdown + CRUD тільки для EXCHANGES/CREDENTIALS */}
      {(activeTab === "EXCHANGES" || activeTab === "CREDENTIALS") && (
        <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
          <select
            className="form-select"
            value={selectedExchange}
            onChange={(e) => {
              setSelectedExchange(e.target.value);
              setFormData({});
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

      {/* Форма з safe-guard */}
      {getCurrentSchema() ? (
        <Form
          schema={getCurrentSchema()}
          uiSchema={getUiSchema()}
          validator={validator}
          formData={formData}
          onChange={(e) => setFormData(e.formData)}
        />
      ) : (
        (activeTab === "EXCHANGES" || activeTab === "CREDENTIALS") && (
          <p style={{ color: "red", marginTop: "10px" }}>
            ❌ Schema for {activeTab} not found in /openapi.json
          </p>
        )
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
