import apiClient from "./apiClient";

// отримати всі бінди (role ↔ permissions)
export const getRolePermissions = async () => {
  const response = await apiClient.get("/roles/bind");
  return response.data;
};

// додати прив'язку роль ↔ permission
export const createRolePermission = async (payload) => {
  const response = await apiClient.post("/roles/bind", payload);
  return response.data;
};

// видалити прив'язку роль ↔ permission
export const deleteRolePermission = async (roleName, permissionName) => {
  const response = await apiClient.delete(`/roles/bind/${roleName}/${permissionName}`);
  return response.data;
};
