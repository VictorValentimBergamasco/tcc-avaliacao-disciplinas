import axios from "axios";

const api = axios.create({ baseURL: "http://127.0.0.1:8000/api/" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export function getMediaUrl(pathOrUrl) {
  if (!pathOrUrl) return "";
  if (pathOrUrl.startsWith("http")) return pathOrUrl;
  return `http://127.0.0.1:8000${pathOrUrl}`;
}

export default api;
