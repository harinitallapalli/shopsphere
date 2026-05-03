import axios from "axios";

// Base URLs for each microservice
const AUTH_BASE_URL = "http://127.0.0.1:5000";
const PRODUCT_BASE_URL = "http://127.0.0.1:8001";
const ORDER_BASE_URL = "http://127.0.0.1:8002";

// Create axios instances for each service
export const authApi = axios.create({ 
  baseURL: AUTH_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

export const productApi = axios.create({ 
  baseURL: PRODUCT_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

export const orderApi = axios.create({ 
  baseURL: ORDER_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

// Attach JWT token to every request automatically
const attachToken = (instance) => {
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // If server returns 401 (token expired or invalid), log the user out
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
      return Promise.reject(error);
    }
  );
};

attachToken(authApi);
attachToken(productApi);
attachToken(orderApi);

export default { authApi, productApi, orderApi };
