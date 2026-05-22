import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../CartContext";
import { getCart, placeOrder, removeFromCart as removeFromCartApi, processPayment } from "../orders";
import "./Cart.css";

function Cart() {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { clearCart } = useCart();

  useEffect(() => {
    const user = localStorage.getItem("user");

    if (!user) {
      alert("Please login first");
      navigate("/login");
      return;
    }

    fetchCart();
  }, [navigate]);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const data = await getCart();
      setCart(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error fetching cart:", err);
      setCart([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePlaceOrder = async () => {
    try {
      const data = await placeOrder();
      alert(data.message || "Order placed!");
      setCart([]);
      clearCart();
    } catch (err) {
      alert("Failed to place order");
    }
  };

  const payNow = async () => {
    try {
      const data = await processPayment();
      alert(data.message || "Payment successful");
    } catch (err) {
      alert("Payment failed");
    }
  };

  const handleRemoveFromCart = async (index) => {
    try {
      await removeFromCartApi(index);
      await fetchCart();
    } catch (err) {
      console.error("Error removing item:", err);
    }
  };

  const totalPrice = cart.reduce((sum, item) => sum + (item.price || 0), 0);

  return (
    <div className="cart-container">
      <div className="cart-header">
        <h1>🛒 Shopping Cart</h1>
        <p>{cart.length} item{cart.length !== 1 ? 's' : ''}</p>
      </div>

      {loading ? (
        <div className="cart-loading">
          <div className="spinner"></div>
          <p>Loading cart...</p>
        </div>
      ) : cart.length === 0 ? (
        <div className="empty-cart">
          <div className="empty-icon">🛍️</div>
          <h2>Your cart is empty</h2>
          <p>Start shopping to add items!</p>
          <button onClick={() => navigate("/")} className="btn-continue-shopping">
            ← Continue Shopping
          </button>
        </div>
      ) : (
        <div className="cart-content">
          <div className="cart-items">
            {cart.map((item, index) => (
              <div key={index} className="cart-item">
                <div className="item-icon">🛍️</div>
                <div className="item-details">
                  <h3>{item.name}</h3>
                  <p className="item-price">₹{item.price}</p>
                </div>
                <button
                  onClick={() => handleRemoveFromCart(index)}
                  className="btn-remove"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <div className="summary-row">
              <span>Subtotal</span>
              <span>₹{totalPrice}</span>
            </div>
            <div className="summary-row">
              <span>Shipping</span>
              <span>₹0</span>
            </div>
            <div className="summary-row">
              <span>Tax</span>
              <span>₹0</span>
            </div>
            <div className="summary-total">
              <span>Total</span>
              <span>₹{totalPrice}</span>
            </div>

            <button onClick={handlePlaceOrder} className="btn-place-order">
              📦 Place Order
            </button>

            <button onClick={payNow} className="btn-pay-now">
              💳 Pay Now
            </button>

            <button onClick={() => navigate("/")} className="btn-continue">
              ← Continue Shopping
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Cart;
