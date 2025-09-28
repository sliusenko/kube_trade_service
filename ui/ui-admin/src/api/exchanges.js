import apiClient from "./apiClient";

// -----------------------------
// Exchanges CRUD
// -----------------------------

// Отримати всі біржі
export const getExchanges = async () => {
  const res = await apiClient.get("/exchanges/");
  return res.data;
};

// Створити біржу
export const createExchange = async (data) => {
  const res = await apiClient.post("/exchanges/", data);
  return res.data;
};

// Оновити біржу
export const updateExchange = async (id, data) => {
  const res = await apiClient.put(`/exchanges/${id}`, data);
  return res.data;
};

// Видалити біржу
export const deleteExchange = async (id) => {
  const res = await apiClient.delete(`/exchanges/${id}`);
  return res.data;
};

// -----------------------------
// Exchange Credentials CRUD
// -----------------------------

// Отримати всі креденшали для конкретної біржі
export const getExchangeCredentials = async (exchangeId) => {
  const res = await apiClient.get(`/exchanges/${exchangeId}/credentials`);
  return res.data;
};

// Створити креденшал
export const createExchangeCredential = async (exchangeId, data) => {
  const res = await apiClient.post(`/exchanges/${exchangeId}/credentials`, data);
  return res.data;
};

// Оновити креденшал
export const updateExchangeCredential = async (exchangeId, credId, data) => {
  const res = await apiClient.put(
    `/exchanges/${exchangeId}/credentials/${credId}`,
    data
  );
  return res.data;
};

// Видалити креденшал
export const deleteExchangeCredential = async (exchangeId, credId) => {
  const res = await apiClient.delete(
    `/exchanges/${exchangeId}/credentials/${credId}`
  );
  return res.data;
};

// additional functions
export async function getExchange(id) {
  const res = await fetch(`/api/exchanges/${id}`);
  if (!res.ok) throw new Error("Failed to load exchange");
  return res.json();
}

export async function getExchangeCredential(exchangeId, credentialId) {
  const res = await fetch(`/api/exchanges/${exchangeId}/credentials/${credentialId}`);
  if (!res.ok) throw new Error("Failed to load credential");
  return res.json();
}
