// src/api/permissions.js
import apiClient from "./apiClient";

export const getPermissions = () =>
  apiClient.get("/permissions/").then((r) => r.data);

export const createPermission = (permission) =>
  apiClient.post("/permissions/", permission).then((r) => r.data);

export const updatePermission = (name, permission) =>
  apiClient.put(`/permissions/${name}`, permission).then((r) => r.data);

export const deletePermission = (name) =>
  apiClient.delete(`/permissions/${name}`).then((r) => r.data);
