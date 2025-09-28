// src/api/role_permissions.js
import apiClient from "./apiClient";

export const getRolePermissions = () =>
  apiClient.get("/role-permissions/").then((r) => r.data);

export const createRolePermission = (payload) =>
  apiClient.post("/role-permissions/", payload).then((r) => r.data);

export const deleteRolePermission = (roleName, permissionName) =>
  apiClient.delete(`/role-permissions/${roleName}/${permissionName}`).then((r) => r.data);
