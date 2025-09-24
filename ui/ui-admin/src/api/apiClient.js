// src/api/apiClient.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: "/core-admin",
});

export default apiClient;