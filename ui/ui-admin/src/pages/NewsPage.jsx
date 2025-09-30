import React, { useEffect, useState } from "react";
import { getNews, createNews, updateNews, deleteNews } from "../api/news";

export default function NewsPage() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // форма для створення новини
  const [form, setForm] = useState({
    title: "",
    summary: "",
    symbol: "",
    url: "",
  });

  useEffect(() => {
    fetchNews();
  }, []);

  async function fetchNews() {
    try {
      setLoading(true);
      const data = await getNews();
      setNews(data);
    } catch (err) {
      console.error(err);
      setError("Не вдалося завантажити новини");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await createNews(form);
      setForm({ title: "", summary: "", symbol: "", url: "" });
      fetchNews();
    } catch (err) {
      console.error(err);
      setError("Помилка при створенні новини");
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Видалити новину?")) return;
    try {
      await deleteNews(id);
      fetchNews();
    } catch (err) {
      console.error(err);
      setError("Помилка при видаленні новини");
    }
  }

  return (
    <div className="p-6">
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>News</h1>

      {error && <div style={{ color: "red" }}>{error}</div>}

      {/* форма */}
      <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Summary"
          value={form.summary}
          onChange={(e) => setForm({ ...form, summary: e.target.value })}
        />
        <input
          type="text"
          placeholder="Symbol"
          value={form.symbol}
          onChange={(e) => setForm({ ...form, symbol: e.target.value })}
        />
        <input
          type="url"
          placeholder="URL"
          value={form.url}
          onChange={(e) => setForm({ ...form, url: e.target.value })}
        />
        <button type="submit">Додати новину</button>
      </form>

      {/* список */}
      {loading ? (
        <div>Завантаження...</div>
      ) : (
        <table border="1" cellPadding="6" style={{ width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Published</th>
              <th>Title</th>
              <th>Symbol</th>
              <th>Sentiment</th>
              <th>URL</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {news.map((n) => (
              <tr key={n.id}>
                <td>{n.id}</td>
                <td>{n.published_at}</td>
                <td>{n.title}</td>
                <td>{n.symbol}</td>
                <td>{n.sentiment}</td>
                <td>
                  {n.url && (
                    <a href={n.url} target="_blank" rel="noopener noreferrer">
                      Link
                    </a>
                  )}
                </td>
                <td>
                  <button onClick={() => handleDelete(n.id)}>Видалити</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
