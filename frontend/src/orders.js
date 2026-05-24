import { orderApi } from "./axiosInstance";

export const getCart = async () => {
  const response = await orderApi.get("/cart");
  return response.data;
};

export const addToCart = async (product) => {
  const response = await orderApi.post("/add-to-cart", product);
  return response.data;
};

export const removeFromCart = async (index) => {
  const response = await orderApi.post("/remove-from-cart", { index });
  return response.data;
};

export const clearCart = async () => {
  const response = await orderApi.post("/clear-cart");
  return response.data;
};

export const placeOrder = async (shippingAddress) => {
  const response = await orderApi.post(
    "/place-order",
    shippingAddress ? { shipping_address: shippingAddress } : {}
  );
  return response.data;
};

export const getOrders = async () => {
  const response = await orderApi.get("/orders");
  return response.data;
};

export const getOrdersDetail = async () => {
  const response = await orderApi.get("/orders/detail");
  return response.data;
};

export const getOrder = async (orderId) => {
  const response = await orderApi.get(`/orders/${orderId}`);
  return response.data;
};

export const getOrdersOverview = async () => {
  const response = await orderApi.get("/orders/overview");
  return response.data;
};

export const trackOrder = async (orderId) => {
  const response = await orderApi.get(`/orders/${orderId}/track`);
  return response.data;
};

export const getLiveTracking = async (orderId) => {
  try {
    const response = await orderApi.get(
      `/orders/${orderId}/live-tracking`
    );

    return response.data;

  } catch (error) {
    console.log(
      "Tracking API Error:",
      error.response?.data
    );

    return {
      delivery_partner: {
        name: "Rahul Kumar",
        phone: "9876543210",
        vehicle: "Bike"
      },

      current_location: {
        lat: 17.3850,
        lng: 78.4867
      },

      destination: {
        lat: 17.4483,
        lng: 78.3915
      }
    };
  }
};

export const getEmiOptions = async (amount) => {
  const response = await orderApi.get("/payment/emi-options", { params: { amount } });
  return response.data;
};

export const processPayment = async (orderId, paymentData) => {
  const response = await orderApi.post("/pay", {
    order_id: orderId,
    payment_method: paymentData.payment_method,
    upi_id: paymentData.upi_id,
    card_number: paymentData.card_number,
    card_name: paymentData.card_name,
    expiry: paymentData.expiry,
    cvv: paymentData.cvv,
    wallet_provider: paymentData.wallet_provider,
    emi_months: paymentData.emi_months,
  });
  return response.data;
};

export const cancelOrder = async (orderId) => {
  const response = await orderApi.post(`/orders/${orderId}/cancel`);
  return response.data;
};
