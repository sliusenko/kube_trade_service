import apiClient from "./apiClient";

// ================== CONFIG PARAMETERS ==================
export const getConfigs = async () => {
  const res = await apiClient.get("/config/settings/");
  return res.data;
};

export const createConfig = async (item) => {
  const res = await apiClient.post("/config/settings/", item);
  return res.data;
};

export const updateConfig = async (code, item) => {
  const res = await apiClient.put(`/config/settings/${code}`, item);
  return res.data;
};

export const deleteConfig = async (code) => {
  const res = await apiClient.delete(`/config/settings/${code}`);
  return res.data;
};

// ================== TIMEFRAMES ==================
export const getTimeframes = async () => {
  const res = await apiClient.get("/config/timeframes/");
  return res.data;
};

export const createTimeframe = async (item) => {
  const res = await apiClient.post("/config/timeframes/", item);
  return res.data;
};

export const updateTimeframe = async (code, item) => {
  const res = await apiClient.put(`/config/timeframes/${code}`, item);
  return res.data;
};

export const deleteTimeframe = async (code) => {
  const res = await apiClient.delete(`/config/timeframes/${code}`);
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
