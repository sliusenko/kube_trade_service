// src/api/roles.js
import apiClient from "./apiClient";

export const getRoles = () => apiClient.get("/roles/").then(r => r.data);
export const createRole = (role) => apiClient.post("/roles/", role).then(r => r.data);
export const updateRole = (name, role) => apiClient.put(`/roles/${name}`, role).then(r => r.data);
export const deleteRole = (name) => apiClient.delete(`/roles/${name}`).then(r => r.data);
