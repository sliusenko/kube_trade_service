import React, { useEffect, useState } from "react";
import Form from "@rjsf/mui"; // або @rjsf/bootstrap-5
import validator from "@rjsf/validator-ajv8";
import { getExchanges } from "../api/exchanges";
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

  // Завантажуємо список бірж і OpenAPI
  useEffect(() => {
    getExchanges().then(setExchanges);
    getSchema().then((schema) => {
      setSchemas(schema.components.schemas || {});
    });
  }, []);

  // Допоміжна функція для отримання схеми
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

      {/* Dropdown + кнопки */}
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

        <Button variant="contained" color="primary" startIcon={<Add />}>
          Create
        </Button>
        <Button
          variant="outlined"
          color="secondary"
          startIcon={<Edit />}
          disabled={!selectedExchange}
        >
          Update
        </Button>
        <Button
          variant="outlined"
          color="error"
          startIcon={<Delete />}
          disabled={!selectedExchange}
        >
          Delete
        </Button>
      </div>

      {/* Автоматично згенерована форма для активної вкладки */}
      {getCurrentSchema() && (
        <Form
          schema={getCurrentSchema()}
          validator={validator}
          onSubmit={({ formData }) => {
            console.log("Submit data:", formData);
          }}
        />
      )}
    </div>
  );
}
