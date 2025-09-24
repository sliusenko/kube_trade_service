import apiClient from "./apiClient";

// Отримати всі біржі
export const getExchanges = async () => {
  const res = await apiClient.get("/exchanges");
  return res.data;
};

// Отримати символи по біржі
export const getExchangeSymbols = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/symbols`);
  return res.data;
};

// Отримати ліміти по біржі
export const getExchangeLimits = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/limits`);
  return res.data;
};

// Отримати історію статусу біржі
export const getExchangeHistory = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/history`);
  return res.data;
};
