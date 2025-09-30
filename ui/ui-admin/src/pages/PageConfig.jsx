import React, { useEffect, useState } from "react";
import {
  Button,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  TextField,
} from "@mui/material";
import { Add, Delete } from "@mui/icons-material";
import {
  getTimeframes,
  createTimeframe,
  updateTimeframe,
  deleteTimeframe,
} from "../api/config";

export default function PageConfig() {
  const [timeframes, setTimeframes] = useState([]);
  const [form, setForm] = useState({
    code: "",
    history_limit: "",
    min_len: "",
    hours: "",
    lookback: "",
  });

  async function fetchData() {
    const data = await getTimeframes();
    setTimeframes(data);
  }

  useEffect(() => {
    fetchData();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    await createTimeframe(form);
    setForm({ code: "", history_limit: "", min_len: "", hours: "", lookback: "" });
    fetchData();
  }

  async function handleDelete(code) {
    if (window.confirm("Видалити таймфрейм?")) {
      await deleteTimeframe(code);
      fetchData();
    }
  }

  return (
    <div className="p-6">
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Config: Timeframes</h1>

      {/* Форма створення */}
      <Paper style={{ padding: 16, marginBottom: 20 }}>
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", gap: 12, flexWrap: "wrap" }}
        >
          <TextField
            label="Code"
            value={form.code}
            onChange={(e) => setForm({ ...form, code: e.target.value })}
            required
            style={{ width: 120 }}
          />
          <TextField
            label="History Limit"
            type="number"
            value={form.history_limit}
            onChange={(e) => setForm({ ...form, history_limit: e.target.value })}
            style={{ width: 140 }}
          />
          <TextField
            label="Min Len"
            type="number"
            value={form.min_len}
            onChange={(e) => setForm({ ...form, min_len: e.target.value })}
            style={{ width: 120 }}
          />
          <TextField
            label="Hours"
            type="number"
            value={form.hours}
            onChange={(e) => setForm({ ...form, hours: e.target.value })}
            style={{ width: 120 }}
          />
          <TextField
            label="Lookback (ISO)"
            value={form.lookback}
            onChange={(e) => setForm({ ...form, lookback: e.target.value })}
            style={{ flex: 1 }}
          />

          <Button
            type="submit"
            variant="contained"
            startIcon={<Add />}
            color="primary"
          >
            Додати
          </Button>
        </form>
      </Paper>

      {/* Таблиця */}
      <Paper>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Code</TableCell>
              <TableCell>History Limit</TableCell>
              <TableCell>Min Len</TableCell>
              <TableCell>Hours</TableCell>
              <TableCell>Lookback</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {timeframes.map((tf) => (
              <TableRow key={tf.code}>
                <TableCell>{tf.code}</TableCell>
                <TableCell>{tf.history_limit}</TableCell>
                <TableCell>{tf.min_len}</TableCell>
                <TableCell>{tf.hours}</TableCell>
                <TableCell>{tf.lookback}</TableCell>
                <TableCell align="right">
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<Delete />}
                    onClick={() => handleDelete(tf.code)}
                  >
                    Видалити
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </div>
  );
}
