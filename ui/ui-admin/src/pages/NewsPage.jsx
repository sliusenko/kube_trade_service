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
  getNews,
  createNews,
  updateNews,
  deleteNews,
} from "../api/news";

export default function NewsPage() {
  const [news, setNews] = useState([]);
  const [form, setForm] = useState({
    title: "",
    summary: "",
    symbol: "",
    url: "",
  });

  async function fetchNews() {
    const data = await getNews();
    setNews(data);
  }

  useEffect(() => {
    fetchNews();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    await createNews(form);
    setForm({ title: "", summary: "", symbol: "", url: "" });
    fetchNews();
  }

  async function handleDelete(id) {
    if (window.confirm("Видалити новину?")) {
      await deleteNews(id);
      fetchNews();
    }
  }

  return (
    <div className="p-6">
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>News</h1>

      {/* Форма створення */}
      <Paper style={{ padding: 16, marginBottom: 20 }}>
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", gap: 12, flexWrap: "wrap" }}
        >
          <TextField
            label="Title"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            required
            style={{ flex: 1 }}
          />
          <TextField
            label="Summary"
            value={form.summary}
            onChange={(e) => setForm({ ...form, summary: e.target.value })}
            style={{ flex: 1 }}
          />
          <TextField
            label="Symbol"
            value={form.symbol}
            onChange={(e) => setForm({ ...form, symbol: e.target.value })}
            style={{ width: 120 }}
          />
          <TextField
            label="URL"
            value={form.url}
            onChange={(e) => setForm({ ...form, url: e.target.value })}
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
              <TableCell>ID</TableCell>
              <TableCell>Published</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Symbol</TableCell>
              <TableCell>Sentiment</TableCell>
              <TableCell>URL</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {news.map((n) => (
              <TableRow key={n.id}>
                <TableCell>{n.id}</TableCell>
                <TableCell>{n.published_at}</TableCell>
                <TableCell>{n.title}</TableCell>
                <TableCell>{n.symbol}</TableCell>
                <TableCell>{n.sentiment}</TableCell>
                <TableCell>
                  {n.url && (
                    <a
                      href={n.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Link
                    </a>
                  )}
                </TableCell>
                <TableCell align="right">
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<Delete />}
                    onClick={() => handleDelete(n.id)}
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
