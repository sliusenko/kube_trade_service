import apiClient from "./apiClient";

// Отримати всі біржі
export const getExchanges = async () => {
  const res = await apiClient.get("/exchanges/");
  return res.data;
};

// CRUD для бірж
export const createExchange = async (data) => {
  const res = await apiClient.post("/exchanges/", data);
  return res.data;
};

export const updateExchange = async (id, data) => {
  const res = await apiClient.put(`/exchanges/${id}`, data);
  return res.data;
};

export const deleteExchange = async (id) => {
  const res = await apiClient.delete(`/exchanges/${id}`);
  return res.data;
};

//// Отримати всі креденшіали для біржі
//export const getExchangeCredentials = async (exchangeId) => {
//  const res = await apiClient.get(`/exchanges/${exchangeId}/credentials`);
//  return res.data;
//};
//
//// Створити креденшіал
//export const createExchangeCredential = async (exchangeId, data) => {
//  const res = await apiClient.post(`/exchanges/${exchangeId}/credentials`, data);
//  return res.data;
//};
//
//// Оновити креденшіал
//export const updateExchangeCredential = async (exchangeId, id, data) => {
//  const res = await apiClient.put(`/exchanges/${exchangeId}/credentials/${id}`, data);
//  return res.data;
//};
//
//// Видалити креденшіал
//export const deleteExchangeCredential = async (exchangeId, id) => {
//  const res = await apiClient.delete(`/exchanges/${exchangeId}/credentials/${id}`);
//  return res.data;
//};
