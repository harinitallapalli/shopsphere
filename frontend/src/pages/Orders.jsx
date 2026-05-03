import { useEffect, useState } from "react";
import "./Orders.css";

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8002/orders");
      const data = await response.json();
      setOrders(data);
    } catch (err) {
      console.error("Error fetching orders:", err);
    } finally {
      setLoading(false);
    }
  };

  const calculateTotal = (items) => {
    return items.reduce((sum, item) => sum + (item.price || 0), 0);
  };

  return (
    <div className="orders-container">
      <div className="orders-header">
        <h1>📦 Order History</h1>
        <p>Your past orders</p>
      </div>

      {loading ? (
        <div className="orders-loading">
          <div className="spinner"></div>
          <p>Loading orders...</p>
        </div>
      ) : orders.length === 0 ? (
        <div className="no-orders">
          <div className="empty-icon">📭</div>
          <h2>No orders yet</h2>
          <p>You haven't placed any orders</p>
          <button onClick={() => window.location.href = "/"} className="btn-shop-now">
            🛒 Start Shopping
          </button>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order, orderIndex) => (
            <div key={orderIndex} className="order-card">
              <div className="order-header">
                <h3>Order #{orderIndex + 1}</h3>
                <span className="order-status">✅ Completed</span>
              </div>

              <div className="order-items">
                {order.map((item, itemIndex) => (
                  <div key={itemIndex} className="order-item">
                    <span className="item-name">{item.name}</span>
                    <span className="item-price">₹{item.price}</span>
                  </div>
                ))}
              </div>

              <div className="order-footer">
                <div className="order-total">
                  <span>Total:</span>
                  <span className="total-price">₹{calculateTotal(order)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <button onClick={fetchOrders} className="btn-refresh-orders">
        🔄 Refresh Orders
      </button>
    </div>
  );
}

export default Orders;