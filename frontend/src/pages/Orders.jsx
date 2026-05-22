import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { getOrdersDetail, getOrdersOverview, cancelOrder } from "../orders";
import "./Orders.css";

function statusBadgeClass(order) {
  if (order.payment_status === "pending") return "badge-pending";
  if (order.is_delivered) return "badge-delivered";
  if (order.status === "cancelled") return "badge-cancelled";
  if (order.status === "out_for_delivery") return "badge-out";
  return "badge-active";
}

function statusLabel(order) {
  if (order.payment_status === "pending") return "Payment Pending";
  return order.status_label || order.status;
}

function Orders() {
  const [orders, setOrders] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);
  const [actionError, setActionError] = useState("");
  const navigate = useNavigate();

  const fetchAll = useCallback(async () => {
    try {
      setLoading(true);
      const [detail, overview] = await Promise.all([
        getOrdersDetail(),
        getOrdersOverview().catch(() => null),
      ]);
      setOrders(Array.isArray(detail) ? detail : []);
      setSummary(overview?.summary || null);
    } catch (err) {
      console.error("Error fetching orders:", err);
      setOrders([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 30000);
    return () => clearInterval(interval);
  }, [fetchAll]);

  const handleCancel = async (orderId) => {
    if (!window.confirm("Cancel this order?")) return;
    try {
      setActionError("");
      await cancelOrder(orderId);
      await fetchAll();
    } catch {
      setActionError("Could not cancel order.");
    }
  };

  return (
    <div className="orders-container">
      <div className="orders-header">
        <h1>📦 Your Orders</h1>
        <p>Track packages, pay pending orders, and view delivery status</p>
      </div>

      {actionError && <div className="orders-action-error">{actionError}</div>}

      {summary && (
        <div className="orders-overview">
          <div className="overview-card">
            <span className="overview-num">{summary.total_orders}</span>
            <span className="overview-label">Total Orders</span>
          </div>
          <div className="overview-card highlight-pending">
            <span className="overview-num">{summary.pending_payment}</span>
            <span className="overview-label">Awaiting Payment</span>
          </div>
          <div className="overview-card highlight-active">
            <span className="overview-num">{summary.active_deliveries}</span>
            <span className="overview-label">On the Way</span>
          </div>
          <div className="overview-card highlight-delivered">
            <span className="overview-num">{summary.delivered}</span>
            <span className="overview-label">Delivered</span>
          </div>
        </div>
      )}

      {loading ? (
        <div className="orders-loading">
          <div className="spinner"></div>
          <p>Loading orders...</p>
        </div>
      ) : orders.length === 0 ? (
        <div className="no-orders">
          <div className="empty-icon">📭</div>
          <h2>No orders yet</h2>
          <p>Place an order from your cart to see it here</p>
          <button onClick={() => navigate("/home")} className="btn-shop-now">
            🛒 Start Shopping
          </button>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order) => (
            <div key={order.order_id} className="order-card">
              <div className="order-header">
                <div>
                  <h3>Order #{order.order_id}</h3>
                  {order.created_at && (
                    <p className="order-date">
                      Placed {new Date(order.created_at).toLocaleString()}
                    </p>
                  )}
                </div>
                <span className={`order-status ${statusBadgeClass(order)}`}>
                  {statusLabel(order)}
                </span>
              </div>

              {order.tracking_number && order.payment_status === "paid" && (
                <div className="tracking-bar">
                  <span className="tracking-label">Tracking</span>
                  <code className="tracking-code">{order.tracking_number}</code>
                  <span className="carrier">{order.carrier}</span>
                </div>
              )}

              {order.payment_status === "paid" && (
                <div className="delivery-progress-wrap">
                  <div className="delivery-progress-header">
                    <span>Delivery progress</span>
                    <span>{order.delivery_progress || 0}%</span>
                  </div>
                  <div className="delivery-progress-track">
                    <div
                      className="delivery-progress-fill"
                      style={{ width: `${order.delivery_progress || 0}%` }}
                    />
                  </div>
                  {order.estimated_delivery && !order.is_delivered && (
                    <p className="eta-text">
                      Est. delivery:{" "}
                      {new Date(order.estimated_delivery).toLocaleDateString()}
                    </p>
                  )}
                  {order.is_delivered && order.delivered_at && (
                    <p className="eta-text delivered-text">
                      Delivered {new Date(order.delivered_at).toLocaleString()}
                    </p>
                  )}
                </div>
              )}

              <div className="order-items">
                {order.items.map((item, itemIndex) => (
                  <div key={itemIndex} className="order-item">
                    <span className="item-name">
                      {item.name}
                      {item.quantity > 1 ? ` × ${item.quantity}` : ""}
                    </span>
                    <span className="item-price">₹{item.price}</span>
                  </div>
                ))}
              </div>

              <div className="order-footer">
                <div className="order-total">
                  <span>Total</span>
                  <span className="total-price">₹{order.total}</span>
                </div>

                <div className="order-actions">
                  {order.can_pay && (
                    <Link
                      to={`/checkout?orderId=${order.order_id}`}
                      className="btn-pay-order"
                    >
                      💳 Pay Now
                    </Link>
                  )}
                  {order.payment_status === "paid" && (
                    <Link
                      to={`/track/${order.order_id}`}
                      className="btn-track-toggle"
                    >
                      📍 Track package
                    </Link>
                  )}
                  {order.timeline?.length > 0 && (
                    <button
                      type="button"
                      className="btn-track-toggle"
                      onClick={() =>
                        setExpandedId(
                          expandedId === order.order_id ? null : order.order_id
                        )
                      }
                    >
                      {expandedId === order.order_id ? "Hide activity" : "View activity"}
                    </button>
                  )}
                  {order.can_pay && order.status === "placed" && (
                    <button
                      type="button"
                      className="btn-cancel-order"
                      onClick={() => handleCancel(order.order_id)}
                    >
                      Cancel
                    </button>
                  )}
                </div>
              </div>

              {expandedId === order.order_id && order.timeline?.length > 0 && (
                <div className="order-timeline">
                  <h4>Shipment activity</h4>
                  <ul>
                    {order.timeline.map((event, i) => (
                      <li key={i} className="timeline-event">
                        <div className="timeline-dot" />
                        <div className="timeline-body">
                          <strong>{event.title}</strong>
                          <p>{event.message}</p>
                          <span className="timeline-meta">
                            {event.location} ·{" "}
                            {new Date(event.event_at).toLocaleString()}
                          </span>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <button onClick={fetchAll} className="btn-refresh-orders">
        🔄 Refresh Orders
      </button>
    </div>
  );
}

export default Orders;
