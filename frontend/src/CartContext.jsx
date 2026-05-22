import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { useAuth } from "./AuthContext";
import { getCart, addToCart as addToCartApi, removeFromCart as removeFromCartApi, clearCart as clearCartApi } from "./orders";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const { user } = useAuth();
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(false);

  const refreshCart = useCallback(async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setCart([]);
      return;
    }
    try {
      setLoading(true);
      const data = await getCart();
      setCart(Array.isArray(data) ? data : []);
    } catch {
      setCart([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshCart();
  }, [user, refreshCart]);

  const addToCart = async (product) => {
    await addToCartApi(product);
    await refreshCart();
    return true;
  };

  const removeFromCart = async (index) => {
    await removeFromCartApi(index);
    await refreshCart();
  };

  const clearCart = async () => {
    await clearCartApi();
    setCart([]);
  };

  const getTotalPrice = () => {
    return cart.reduce((sum, item) => sum + (item.price || 0) * (item.quantity || 1), 0);
  };

  const getTotalItems = () => {
    return cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        loading,
        addToCart,
        removeFromCart,
        clearCart,
        refreshCart,
        getTotalPrice,
        getTotalItems,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within CartProvider");
  }
  return context;
}
