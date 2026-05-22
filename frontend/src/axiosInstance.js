import axios from "axios";

const AUTH_BASE_URL = process.env.REACT_APP_AUTH_URL || "http://127.0.0.1:5000";
const PRODUCT_BASE_URL = process.env.REACT_APP_PRODUCT_URL || "http://127.0.0.1:8001";
const ORDER_BASE_URL = process.env.REACT_APP_ORDER_URL || "http://127.0.0.1:8002";

export const authApi = axios.create({
  baseURL: AUTH_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export const productApi = axios.create({
  baseURL: PRODUCT_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export const orderApi = axios.create({
  baseURL: ORDER_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

const attachToken = (instance) => {
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
      }
      return Promise.reject(error);
    }
  );
};

attachToken(authApi);
attachToken(productApi);
attachToken(orderApi);

const apiInstances = { authApi, productApi, orderApi };
export default apiInstances;
