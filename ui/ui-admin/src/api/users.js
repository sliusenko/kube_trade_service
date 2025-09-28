import apiClient from "./apiClient";

// Отримати всіх користувачів
export const getUsers = async () => {
  const response = await apiClient.get("/users/");
  return response.data;
};

// Створити користувача
export const createUser = async (user) => {
  const response = await apiClient.post("/users/", user);
  return response.data;
};

// Оновити користувача
export const updateUser = async (userId, user) => {
  const response = await apiClient.put(`/users/${userId}`, user);
  return response.data;
};

// Видалити користувача
export const deleteUser = async (userId) => {
  const response = await apiClient.delete(`/users/${userId}`);
  return response.data;
};
