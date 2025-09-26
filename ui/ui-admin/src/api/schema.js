import apiClient from "./apiClient";

// Отримати OpenAPI-схему (всі моделі)
export const getSchema = async () => {
  const res = await apiClient.get("/openapi.json");
  return res.data;
};
