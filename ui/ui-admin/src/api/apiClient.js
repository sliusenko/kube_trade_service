// src/api/apiClient.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://kube-trade-bot-core-admin:8000", // або URL твого admin-core сервісу
});

export default apiClient;