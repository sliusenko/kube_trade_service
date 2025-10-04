import apiClient from "./apiClient";

// ================== CONFIG PARAMETERS ==================
export const getSettings = async () => {
  const res = await apiClient.get("/config/settings/");
  return res.data;
};

export const createSetting = async (item) => {
  const res = await apiClient.post("/config/settings/", item);
  return res.data;
};

export const updateSetting = async (code, item) => {
  const res = await apiClient.put(`/config/settings/${code}`, item);
  return res.data;
};

export const deleteSetting = async (code) => {
  const res = await apiClient.delete(`/config/settings/${code}`);
  return res.data;
};

// ================== TIMEFRAMES ==================
export async function getTimeframes(exchangeId = null) {
  const url = exchangeId ? `/config/timeframes/?exchange_id=${exchangeId}` : "/config/timeframes/";
  const res = await apiClient.get(url);
  return res.data;
}

export const createTimeframe = async (item) => {
  const payload = {
    code: item.code,
    history_limit: item.history_limit ? parseInt(item.history_limit, 10) : null,
    min_len: item.min_len ? parseInt(item.min_len, 10) : null,
    hours: item.hours ? parseFloat(item.hours) : null
  };

  console.log("📤 Sending payload:", payload);
  const res = await apiClient.post(`/config/timeframes/?exchange_id=${item.exchange_id}`, payload);
  return res.data;
};

export const updateTimeframe = async (code, item) => {
  const res = await apiClient.put(`/config/timeframes/${code}?exchange_id=${item.exchange_id}`, item);
  return res.data;
};

export const deleteTimeframe = async (code, exchange_id) => {
  const res = await apiClient.delete(`/config/timeframes/${code}?exchange_id=${exchange_id}`);
  return res.data;
};

// ================== COMMANDS ==================
export const getCommands = async () => {
  const res = await apiClient.get("/config/commands/");
  return res.data;
};

export const createCommand = async (item) => {
  const res = await apiClient.post("/config/commands/", item);
  return res.data;
};

export const updateCommand = async (id, item) => {
  const res = await apiClient.put(`/config/commands/${id}`, item);
  return res.data;
};

export const deleteCommand = async (id) => {
  const res = await apiClient.delete(`/config/commands/${id}`);
  return res.data;
};

// ================== REASONS ==================
export const getReasons = async () => {
  const res = await apiClient.get("/config/reasons/");
  return res.data;
};

export const createReason = async (item) => {
  const res = await apiClient.post("/config/reasons/", item);
  return res.data;
};

export const updateReason = async (code, item) => {
  const res = await apiClient.put(`/config/reasons/${code}`, item);
  return res.data;
};

export const deleteReason = async (code) => {
  const res = await apiClient.delete(`/config/reasons/${code}`);
  return res.data;
};

// ================== TRADE PROFILES ==================
export const getTradeProfiles = async () => {
  const res = await apiClient.get("/config/trade-profiles/");
  return res.data;
};

export const createTradeProfile = async (item) => {
  const res = await apiClient.post("/config/trade-profiles/", item);
  return res.data;
};

export const updateTradeProfile = async (id, item) => {
  const res = await apiClient.put(`/config/trade-profiles/${id}`, item);
  return res.data;
};

export const deleteTradeProfile = async (id) => {
  const res = await apiClient.delete(`/config/trade-profiles/${id}`);
  return res.data;
};

// ================== TRADE CONDITIONS ==================
export const getTradeConditions = async () => {
  const res = await apiClient.get("/config/trade-conditions/");
  return res.data;
};

export const createTradeCondition = async (item) => {
  const res = await apiClient.post("/config/trade-conditions/", item);
  return res.data;
};

export const updateTradeCondition = async (id, item) => {
  const res = await apiClient.put(`/config/trade-conditions/${id}`, item);
  return res.data;
};

export const deleteTradeCondition = async (id) => {
  const res = await apiClient.delete(`/config/trade-conditions/${id}`);
  return res.data;
};

// ================== GROUP ICONS ==================
export const getGroupIcons = async () => {
  const res = await apiClient.get("/config/group-icons/");
  return res.data;
};

export const createGroupIcon = async (item) => {
  const res = await apiClient.post("/config/group-icons/", item);
  return res.data;
};

export const updateGroupIcon = async (groupName, item) => {
  const res = await apiClient.put(`/config/group-icons/${groupName}`, item);
  return res.data;
};

export const deleteGroupIcon = async (groupName) => {
  const res = await apiClient.delete(`/config/group-icons/${groupName}`);
  return res.data;
};
