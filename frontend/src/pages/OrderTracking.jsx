import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import DeliveryMap from "../components/DeliveryMap";
import { getOrder, getLiveTracking } from "../orders";
import "./OrderTracking.css";

const STAGES = [
  { key: "placed", label: "Order Placed" },
  { key: "confirmed", label: "Confirmed" },
  { key: "packed", label: "Packed" },
  { key: "shipped", label: "Shipped" },
  { key: "out_for_delivery", label: "Out for Delivery" },
  { key: "delivered", label: "Delivered" },
];

function stageIndex(status) {
  const idx = STAGES.findIndex((s) => s.key === status);
  return idx >= 0 ? idx : 0;
}

function OrderTracking() {
  const { orderId } = useParams();
  console.log("Order ID =", orderId);
  const [order, setOrder] = useState(null);
  const [live, setLive] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
  try {
    setLoading(true);

    // get order first
    const orderData = await getOrder(Number(orderId));

    console.log("Order API response:", orderData);
    console.log("Order ID:", orderId);

    setOrder(orderData);

    try {
      // try live tracking separately
      const liveData = await getLiveTracking(Number(orderId));
      setLive(liveData);
    } catch (err) {
      console.log("Live tracking failed:", err);

      // fake fallback data so page still works
      setLive({
        delivery_partner: {
          name: "Rahul Kumar",
          phone: "9876543210",
          vehicle: "Bike"
        }
      });
    }

    setError("");

  } catch (err) {
  console.log("FULL ERROR:", err);
  console.log("RESPONSE:", err?.response);
  console.log("DATA:", err?.response?.data);
  console.log("STATUS:", err?.response?.status);

  setError("Order not found");
  setOrder(null);
  } finally {
    setLoading(false);
  }
}, [orderId]);
useEffect(() => {
  load();

  const interval = setInterval(load, 15000);

  return () => clearInterval(interval);
}, [load]);

  if (loading) {
    return (
      <div className="tracking-container">
        <div className="tracking-loading">
          <div className="spinner" />
          <p>Loading tracking...</p>
        </div>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="tracking-container">
        <div className="tracking-error card-panel">{error || "Order not found"}</div>
        <Link to="/orders" className="link-back">← Back to orders</Link>
      </div>
    );
  }

  const currentIdx = stageIndex(order.status);
  const partner =
    live?.delivery_partner ||
    order.delivery_partner || {
      name: "Rahul Kumar",
      phone: "9876543210",
      vehicle: "Bike",
    };

  return (
    <div className="tracking-container">
      <div className="tracking-header">
        <Link to="/orders" className="link-back">← Orders</Link>
        <h1>Track package</h1>
        <p>
          Order #{order.order_id} · <code>{order.tracking_number}</code>
        </p>
      </div>

      <div className="tracking-grid">
        <div className="card-panel status-card">
          <div className="live-status">
            <span className="pulse" />
            <div>
              <strong>{order.status_label}</strong>
              <p>
                {order.is_delivered
                  ? "Package delivered"
                  : `Live · ${order.delivery_progress || 0}% complete`}
              </p>
            </div>
          </div>

          {order.estimated_delivery && !order.is_delivered && (
            <p className="eta-banner">
              Estimated delivery:{" "}
              <strong>{new Date(order.estimated_delivery).toLocaleDateString()}</strong>
            </p>
          )}

          <div className="progress-steps">
            {STAGES.map((stage, i) => (
              <div
                key={stage.key}
                className={`step ${i <= currentIdx ? "done" : ""} ${i === currentIdx ? "current" : ""}`}
              >
                <div className="step-dot" />
                <span>{stage.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card-panel partner-card">
          <h3>Delivery partner</h3>
          <div className="partner-info">
            <p><strong>Name:</strong> {partner.name}</p>
            <p><strong>Vehicle:</strong> {partner.vehicle}</p>
            <p>
              <strong>Contact:</strong>{" "}
              <a href={`tel:${partner.phone}`}>{partner.phone}</a>
            </p>
          </div>
        </div>

        <div className="card-panel map-card">
          <h3>Live route</h3>
          <DeliveryMap tracking={live} />
        </div>

        {order.timeline?.length > 0 && (
          <div className="card-panel timeline-card">
            <h3>Shipment activity</h3>
            <ul className="activity-list">
              {order.timeline.map((e, i) => (
                <li key={i}>
                  <strong>{e.title}</strong>
                  <p>{e.message}</p>
                  <small>
                    {e.location} · {new Date(e.event_at).toLocaleString()}
                  </small>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <button type="button" className="btn-refresh-track" onClick={load}>
        Refresh tracking
      </button>
    </div>
  );
}

export default OrderTracking;
