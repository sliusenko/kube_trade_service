//// src/api/schema.js
//import apiClient from "./apiClient";
//
//export const getSchema = () =>
//  apiClient.get("/openapi.json").then((r) => r.data);
import apiClient from "./apiClient";

// Отримати OpenAPI-схему (всі моделі)
export const getSchema = async () => {
  const res = await apiClient.get("/openapi.json");
  return res.data;
};
