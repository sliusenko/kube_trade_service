import React, { useEffect, useState } from "react";
import Form from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {
  getExchanges,
  createExchange,
  updateExchange,
  deleteExchange,
} from "../api/exchanges";
import {
  getExchangeCredentials,
  createExchangeCredential,
  updateExchangeCredential,
  deleteExchangeCredential,
} from "../api/exchange_credentials";
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
      getExchangeSymbols(selectedExchange).then(setSymbols);
    }
    if (activeTab === "LIMITS") {
      getExchangeLimits(selectedExchange).then(setLimits);
    }
    if (activeTab === "HISTORY") {
      getExchangeHistory(selectedExchange).then(setHistory);
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

  // CRUD для Exchanges + Credentials
  const handleCreate = async () => {
    if (activeTab === "EXCHANGES") {
      await createExchange(formData);
      reloadExchanges();
    }
    if (activeTab === "CREDENTIALS") {
      await createExchangeCredential(selectedExchange, formData);
    }
  };

  const handleUpdate = async () => {
    if (activeTab === "EXCHANGES") {
      await updateExchange(selectedExchange, formData);
      reloadExchanges();
    }
    if (activeTab === "CREDENTIALS") {
      await updateExchangeCredential(selectedExchange, formData.id, formData);
    }
  };

  const handleDelete = async () => {
    if (activeTab === "EXCHANGES") {
      await deleteExchange(selectedExchange);
      reloadExchanges();
      setSelectedExchange(null);
    }
    if (activeTab === "CREDENTIALS") {
      await deleteExchangeCredential(selectedExchange, formData.id);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Exchanges</h2>

      {/* Вкладки */}
      <div style={{ marginBottom: "20px" }}>
        <TabButton label="EXCHANGES" active={activeTab === "EXCHANGES"} onClick={() => setActiveTab("EXCHANGES")} />
        <TabButton label="CREDENTIALS" active={activeTab === "CREDENTIALS"} onClick={() => setActiveTab("CREDENTIALS")} />
        <TabButton label="SYMBOLS" active={activeTab === "SYMBOLS"} onClick={() => setActiveTab("SYMBOLS")} />
        <TabButton label="LIMITS" active={activeTab === "LIMITS"} onClick={() => setActiveTab("LIMITS")} />
        <TabButton label="HISTORY" active={activeTab === "HISTORY"} onClick={() => setActiveTab("HISTORY")} />
      </div>

      {/* Dropdown + CRUD тільки для EXCHANGES/CREDENTIALS */}
      {(activeTab === "EXCHANGES" || activeTab === "CREDENTIALS") && (
        <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
          <select
            className="form-select"
            value={selectedExchange || ""}
            onChange={(e) => setSelectedExchange(e.target.value)}
            style={{ maxWidth: "250px" }}
          >
            <option value="">-- select exchange --</option>
            {exchanges.map((ex) => (
              <option key={ex.id} value={ex.id}>
                {ex.name}
              </option>
            ))}
          </select>

          <Button variant="contained" color="primary" startIcon={<Add />} onClick={handleCreate}>
            Create
          </Button>
          <Button variant="outlined" color="secondary" startIcon={<Edit />} disabled={!selectedExchange} onClick={handleUpdate}>
            Update
          </Button>
          <Button variant="outlined" color="error" startIcon={<Delete />} disabled={!selectedExchange} onClick={handleDelete}>
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
                  <TableCell>{h.status_msg}</TableCell>
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
