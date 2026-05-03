import { productApi } from "./axiosInstance";

export const getAllProducts = async () => {
  try {
    const response = await productApi.get("/products");
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getProduct = async (productId) => {
  try {
    const response = await productApi.get(`/products/${productId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const addProduct = async (product) => {
  try {
    const response = await productApi.post("/add-product", product);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const searchProducts = async (query) => {
  try {
    const response = await productApi.get("/products");
    const products = response.data;
    return products.filter(p => 
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      (p.description && p.description.toLowerCase().includes(query.toLowerCase()))
    );
  } catch (error) {
    throw error.response?.data || error.message;
  }
};
