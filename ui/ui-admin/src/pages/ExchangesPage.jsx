import React, { useEffect, useState } from "react";
import Form from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {
  getExchanges,
  createExchange,
  updateExchange,
  deleteExchange,
} from "../api/exchanges";
import { getSchema } from "../api/schema";
import { Button } from "@mui/material";
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

  // Завантаження даних
  useEffect(() => {
    reloadExchanges();
    getSchema().then((schema) => {
      setSchemas(schema.components.schemas || {});
    });
  }, []);

  const reloadExchanges = () => {
    getExchanges().then(setExchanges);
  };

  const getCurrentSchema = () => {
    switch (activeTab) {
      case "EXCHANGES":
        return schemas.ExchangeSchema;
      case "CREDENTIALS":
        return schemas.ExchangeCredentialSchema;
      case "SYMBOLS":
        return schemas.ExchangeSymbolRead;
      case "LIMITS":
        return schemas.ExchangeLimitRead;
      case "HISTORY":
        return schemas.ExchangeStatusHistoryRead;
      default:
        return null;
    }
  };

  // CRUD-обробники
  const handleCreate = async () => {
    try {
      await createExchange(formData);
      reloadExchanges();
      alert("Exchange created successfully!");
    } catch (err) {
      console.error(err);
      alert("Error creating exchange");
    }
  };

  const handleUpdate = async () => {
    try {
      await updateExchange(selectedExchange, formData);
      reloadExchanges();
      alert("Exchange updated successfully!");
    } catch (err) {
      console.error(err);
      alert("Error updating exchange");
    }
  };

  const handleDelete = async () => {
    try {
      await deleteExchange(selectedExchange);
      reloadExchanges();
      setSelectedExchange(null);
      alert("Exchange deleted successfully!");
    } catch (err) {
      console.error(err);
      alert("Error deleting exchange");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Exchanges</h2>

      {/* Tabs */}
      <div style={{ marginBottom: "20px" }}>
        <TabButton label="EXCHANGES" active={activeTab === "EXCHANGES"} onClick={() => setActiveTab("EXCHANGES")} />
        <TabButton label="CREDENTIALS" active={activeTab === "CREDENTIALS"} onClick={() => setActiveTab("CREDENTIALS")} />
        <TabButton label="SYMBOLS" active={activeTab === "SYMBOLS"} onClick={() => setActiveTab("SYMBOLS")} />
        <TabButton label="LIMITS" active={activeTab === "LIMITS"} onClick={() => setActiveTab("LIMITS")} />
        <TabButton label="HISTORY" active={activeTab === "HISTORY"} onClick={() => setActiveTab("HISTORY")} />
      </div>

      {/* Dropdown + CRUD buttons */}
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

      {/* Форма */}
      {getCurrentSchema() && (
        <Form
          schema={getCurrentSchema()}
          validator={validator}
          formData={formData}
          onChange={(e) => setFormData(e.formData)}
          onSubmit={({ formData }) => {
            console.log("Form submitted:", formData);
          }}
        />
      )}
    </div>
  );
}
