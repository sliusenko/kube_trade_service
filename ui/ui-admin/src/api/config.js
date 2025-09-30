import apiClient from "./apiClient";

// ---- Timeframes ----
export const getTimeframes = async () => {
  const res = await apiClient.get("/core-config/timeframes/");
  return res.data;
};

export const createTimeframe = async (item) => {
  const res = await apiClient.post("/core-config/timeframes/", item);
  return res.data;
};

export const updateTimeframe = async (code, item) => {
  const res = await apiClient.put(`/core-config/timeframes/${code}`, item);
  return res.data;
};

export const deleteTimeframe = async (code) => {
  const res = await apiClient.delete(`/core-config/timeframes/${code}`);
  return res.data;
};
