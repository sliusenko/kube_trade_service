import apiClient from "./apiClient";

// Fetch all users from backend
export const getUsers = async () => {
  const response = await apiClient.get("/users/");
  return response.data;
};

// Create a new user (expects { username, email, password, role? })
export const createUser = async (user) => {
  const response = await apiClient.post("/users/", user);
  return response.data;
};

// Update existing user by ID (userId is UUID, user is updated data)
export const updateUser = async (userId, user) => {
  const response = await apiClient.put(`/users/${userId}`, user);
  return response.data;
};

// Delete a user by ID
export const deleteUser = async (userId) => {
  const response = await apiClient.delete(`/users/${userId}`);
  return response.data;
};
