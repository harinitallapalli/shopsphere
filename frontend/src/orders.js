import { orderApi } from "./axiosInstance";

export const getCart = async () => {
  try {
    const response = await orderApi.get("/cart");
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const addToCart = async (product) => {
  try {
    const response = await orderApi.post("/add-to-cart", product);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const placeOrder = async () => {
  try {
    const response = await orderApi.post("/place-order");
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getOrders = async () => {
  try {
    const response = await orderApi.get("/orders");
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const removeFromCart = async (index) => {
  try {
    const response = await orderApi.delete(`/cart/${index}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const processPayment = async () => {
  try {
    const response = await orderApi.post("/pay");
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};
