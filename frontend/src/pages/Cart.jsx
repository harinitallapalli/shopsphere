import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../CartContext";
import { placeOrder } from "../orders";
import "./Cart.css";

function Cart() {
  const { cart, loading, removeFromCart, clearCart, refreshCart, getTotalPrice } = useCart();
  const navigate = useNavigate();
  const [processing, setProcessing] = useState(false);

  const totalPrice = getTotalPrice();

  const handlePlaceOrder = async () => {
    try {
      setProcessing(true);
      const data = await placeOrder();
      await refreshCart();
      navigate(`/checkout?orderId=${data.order_id}`);
    } catch {
      setProcessing(false);
    }
  };

  return (
    <div className="cart-container">
      <div className="cart-header">
        <h1>🛒 Shopping Cart</h1>
        <p>{cart.length} item{cart.length !== 1 ? "s" : ""}</p>
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
          <button onClick={() => navigate("/home")} className="btn-continue-shopping">
            ← Continue Shopping
          </button>
        </div>
      ) : (
        <div className="cart-content">
          <div className="cart-items">
            {cart.map((item, index) => (
              <div key={`${item.id}-${index}`} className="cart-item">
                <div className="item-icon">🛍️</div>
                <div className="item-details">
                  <h3>{item.name}</h3>
                  <p className="item-price">
                    ₹{item.price}
                    {item.quantity > 1 ? ` × ${item.quantity}` : ""}
                  </p>
                </div>
                <button onClick={() => removeFromCart(index)} className="btn-remove">
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
              <span>Free</span>
            </div>
            <div className="summary-total">
              <span>Total</span>
              <span>₹{totalPrice}</span>
            </div>

            <button
              onClick={() => navigate("/checkout")}
              className="btn-pay-now"
            >
              💳 Proceed to Checkout
            </button>

            <button
              onClick={handlePlaceOrder}
              disabled={processing}
              className="btn-place-order"
            >
              {processing ? "Creating order..." : "📦 Place Order (Pay Later)"}
            </button>

            <button onClick={clearCart} className="btn-continue">
              Clear Cart
            </button>

            <button onClick={() => navigate("/home")} className="btn-continue">
              ← Continue Shopping
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Cart;
