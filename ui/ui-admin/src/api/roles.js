import apiClient from "./apiClient";

// Отримати всі ролі
export async function getRoles() {
  const res = await apiClient.get("/roles/");
  return res.data;
}

// Створити нову роль
export async function createRole(role) {
  const res = await apiClient.post("/roles/", role);
  return res.data;
}

// Оновити роль
export async function updateRole(name, role) {
  const res = await apiClient.put(`/roles/${name}`, role);
  return res.data;
}

// Видалити роль
export async function deleteRole(name) {
  const res = await apiClient.delete(`/roles/${name}`);
  return res.data;
}
