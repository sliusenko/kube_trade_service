import apiClient from "./apiClient";

export const getUsers = () => apiClient.get("/users/").then(r => r.data);
export const createUser = (user) => apiClient.post("/users/users/", user).then(r => r.data);
export const updateUser = (id, user) => apiClient.put(`/users/${id}`, user).then(r => r.data);
export const deleteUser = (id) => apiClient.delete(`/users/${id}`).then(r => r.data);
