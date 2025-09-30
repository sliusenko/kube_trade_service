import apiClient from "./apiClient";

// отримати всі новини
export const getNews = async () => {
  const res = await apiClient.get("/news/");
  return res.data;
};

// створити новину
export const createNews = async (data) => {
  const res = await apiClient.post("/news/", data);
  return res.data;
};

// оновити новину
export const updateNews = async (id, data) => {
  const res = await apiClient.patch(`/news/${id}`, data);
  return res.data;
};

// видалити новину
export const deleteNews = async (id) => {
  const res = await apiClient.delete(`/news/${id}`);
  return res.data;
};
