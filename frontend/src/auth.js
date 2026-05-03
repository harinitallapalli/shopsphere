import { authApi } from "./axiosInstance";

export const register = async (username, password) => {
  try {
    const response = await authApi.post("/register", { username, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const login = async (username, password) => {
  try {
    const response = await authApi.post("/login", { username, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getMe = async () => {
  try {
    const response = await authApi.get("/me");
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};
