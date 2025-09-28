import apiClient from "./apiClient";

// ---------------------------
// Додаткові API для бірж
// ---------------------------

// Symbols
export const getExchangeSymbols = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/symbols`);
  return res.data;
};

// Limits
export const getExchangeLimits = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/limits`);
  return res.data;
};

// History
export const getExchangeHistory = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/history`);
  return res.data;
};
