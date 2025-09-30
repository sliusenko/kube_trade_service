import apiClient from "./apiClient";

// Отримати статистику для Dashboard
export const getDashboardStats = async () => {
  const res = await apiClient.get("/dashboard/stats");
  return res.data;
};
