import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { getOrder } from "../orders";
import "./OrderSuccess.css";

function OrderSuccess() {
  const { orderId } = useParams();
  const location = useLocation();
  const [order, setOrder] = useState(location.state?.order || null);

  useEffect(() => {
    if (!order && orderId) {
      getOrder(Number(orderId))
        .then(setOrder)
        .catch(() => {});
    }
  }, [order, orderId]);

  if (!order) {
    return (
      <div className="success-container">
        <div className="success-card">
          <div className="success-icon">✅</div>
          <h1>Order placed successfully!</h1>
          <Link to="/orders" className="btn-primary">View orders</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="success-container">
      <div className="success-card">
        <div className="success-icon">✅</div>
        <h1>Payment successful!</h1>
        <p className="success-sub">Thank you for shopping with ShopSphere</p>

        <div className="success-details">
          <div className="detail-row">
            <span>Order ID</span>
            <strong>#{order.order_id}</strong>
          </div>
          <div className="detail-row">
            <span>Amount paid</span>
            <strong>₹{order.amount_paid || order.total}</strong>
          </div>
          {order.payment_id && (
            <div className="detail-row">
              <span>Payment ID</span>
              <code>{order.payment_id}</code>
            </div>
          )}
          {order.tracking_number && (
            <div className="detail-row">
              <span>Tracking</span>
              <code>{order.tracking_number}</code>
            </div>
          )}
          {order.estimated_delivery && (
            <div className="detail-row">
              <span>Estimated delivery</span>
              <strong>{new Date(order.estimated_delivery).toLocaleDateString()}</strong>
            </div>
          )}
        </div>

        <div className="success-actions">
          <Link to={`/track/${order.order_id}`} className="btn-primary">
            Track order
          </Link>
          <Link to="/orders" className="btn-secondary">
            All orders
          </Link>
          <Link to="/home" className="btn-secondary">
            Continue shopping
          </Link>
        </div>
      </div>
    </div>
  );
}

export default OrderSuccess;
