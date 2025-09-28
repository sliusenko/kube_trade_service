// src/api/schema.js
import apiClient from "./apiClient";

export const getSchema = () =>
  apiClient.get("/openapi.json").then((r) => r.data);
