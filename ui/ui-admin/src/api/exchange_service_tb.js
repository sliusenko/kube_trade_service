import apiClient from "./apiClient";

// Symbols
export const getExchangeSymbols = (exchangeId) =>
  apiClient.get(`/exchanges/${exchangeId}/symbols`).then(r => r.data);

// Limits
export const getExchangeLimits = (exchangeId) =>
  apiClient.get(`/exchanges/${exchangeId}/limits`).then(r => r.data);

// History
export const getExchangeHistory = (exchangeId) =>
  apiClient.get(`/exchanges/${exchangeId}/history`).then(r => r.data);
