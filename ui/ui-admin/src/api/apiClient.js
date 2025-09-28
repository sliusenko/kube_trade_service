//// apiClient.js
//import axios from "axios";
//
//const apiClient = axios.create({
//  baseURL: "/core-admin",
//  withCredentials: true,
//});
//
//apiClient.interceptors.response.use(
//  (response) => {
//
//    if (response.request?.responseURL?.includes("/oauth2/start")) {
//      return Promise.reject(new Error("Not authenticated"));
//    }
//    return response;
//  },
//  (error) => Promise.reject(error)
//);
//
//export default apiClient;

// src/api/apiClient.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: "/core-admin",
});

export default apiClient;