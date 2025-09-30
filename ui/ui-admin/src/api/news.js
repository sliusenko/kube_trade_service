import apiClient from "./apiClient";

export const getNews = async () => {
  const res = await apiClient.get("/news/");
  return res.data;
};

export const createNews = async (data) => {
  const res = await apiClient.post("/news/", data);
  return res.data;
};

export const updateNews = async (id, data) => {
  const res = await apiClient.patch(`/news/${id}`, data);
  return res.data;
};

export const deleteNews = async (id) => {
  const res = await apiClient.delete(`/news/${id}`);
  return res.data;
};
