import apiClient from "./apiClient";

// Отримати OpenAPI-схему (JSON опис всіх моделей)
export const getSchema = async () => {
  const res = await apiClient.get("/openapi.json");
  return res.data;
};
