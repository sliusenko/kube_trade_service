import apiClient from "./apiClient";

export const getDashboardStats = async () => {
  const res = await apiClient.get("/dashboard/stats");
  return res.data;
};
