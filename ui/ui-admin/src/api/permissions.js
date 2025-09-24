import apiClient from "./apiClient";

// Отримати всі permissions
export async function getPermissions() {
  const res = await apiClient.get("/permissions/");
  return res.data;
}

// Створити новий permission
export async function createPermission(permission) {
  const res = await apiClient.post("/permissions/", permission);
  return res.data;
}

// Оновити permission
export async function updatePermission(name, permission) {
  const res = await apiClient.put(`/permissions/${name}`, permission);
  return res.data;
}

// Видалити permission
export async function deletePermission(name) {
  const res = await apiClient.delete(`/permissions/${name}`);
  return res.data;
}