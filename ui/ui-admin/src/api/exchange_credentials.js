// src/api/exchange_credentials.js
import axios from "axios";

const API_BASE = "/api"; // 👈 підлаштуй під свій бекенд (наприклад, http://localhost:8000/api)

export async function getExchangeCredentials(exchangeId) {
  const res = await axios.get(`${API_BASE}/exchanges/${exchangeId}/credentials`);
  return res.data;
}

export async function createExchangeCredential(exchangeId, payload) {
  const res = await axios.post(`${API_BASE}/exchanges/${exchangeId}/credentials`, payload);
  return res.data;
}

export async function updateExchangeCredential(exchangeId, credId, payload) {
  const res = await axios.put(`${API_BASE}/exchanges/${exchangeId}/credentials/${credId}`, payload);
  return res.data;
}

export async function deleteExchangeCredential(exchangeId, credId) {
  const res = await axios.delete(`${API_BASE}/exchanges/${exchangeId}/credentials/${credId}`);
  return res.data;
}
