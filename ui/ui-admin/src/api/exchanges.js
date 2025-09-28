// -----------------------------
// Exchanges CRUD
// -----------------------------

export const getExchanges = () =>
  apiClient.get("/exchanges/").then((r) => r.data);

export const createExchange = (data) =>
  apiClient.post("/exchanges/", data).then((r) => r.data);

export const updateExchange = (id, data) =>
  apiClient.put(`/exchanges/${id}`, data).then((r) => r.data);

export const deleteExchange = (id) =>
  apiClient.delete(`/exchanges/${id}`).then((r) => r.data);

// -----------------------------
// Exchange Credentials CRUD
// -----------------------------

export const getExchangeCredentials = (exchangeId) =>
  apiClient.get(`/exchanges/${exchangeId}/credentials`).then((r) => r.data);

export const createExchangeCredential = (exchangeId, data) =>
  apiClient.post(`/exchanges/${exchangeId}/credentials`, data).then((r) => r.data);

export const updateExchangeCredential = (exchangeId, credId, data) =>
  apiClient.put(`/exchanges/${exchangeId}/credentials/${credId}`, data).then((r) => r.data);

export const deleteExchangeCredential = (exchangeId, credId) =>
  apiClient.delete(`/exchanges/${exchangeId}/credentials/${credId}`).then((r) => r.data);

// -----------------------------
// Допоміжні функції
// -----------------------------

export const getExchange = (id) =>
  apiClient.get(`/exchanges/${id}`).then((r) => r.data);

export const getExchangeCredential = (exchangeId, credentialId) =>
  apiClient.get(`/exchanges/${exchangeId}/credentials/${credentialId}`).then((r) => r.data);
