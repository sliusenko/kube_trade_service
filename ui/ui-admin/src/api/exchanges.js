import apiClient from "./apiClient";

// --------------------
// Exchanges
// --------------------

// Отримати всі біржі
export const getExchanges = async () => {
  const res = await apiClient.get("/exchanges/");
  return res.data;
};

// Створити біржу
export const createExchange = async (payload) => {
  const res = await apiClient.post("/exchanges/", payload);
  return res.data;
};

// Оновити біржу
export const updateExchange = async (exchangeId, payload) => {
  const res = await apiClient.put(`/exchanges/${exchangeId}`, payload);
  return res.data;
};

// Видалити біржу
export const deleteExchange = async (exchangeId) => {
  const res = await apiClient.delete(`/exchanges/${exchangeId}`);
  return res.data;
};

// --------------------
// Symbols
// --------------------

// Отримати символи по біржі
export const getExchangeSymbols = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/symbols`);
  return res.data;
};

// --------------------
// Limits
// --------------------

// Отримати ліміти по біржі
export const getExchangeLimits = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/limits`);
  return res.data;
};

// --------------------
// Status History
// --------------------

// Отримати історію статусу біржі
export const getExchangeHistory = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/history`);
  return res.data;
};
