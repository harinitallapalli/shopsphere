import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useCart } from "../CartContext";
import {
  placeOrder,
  getOrder,
  processPayment,
  getEmiOptions,
} from "../orders";
import { validateUpi, validateCard, calcEmi } from "../utils/paymentValidation";
import "./Checkout.css";

const METHODS = [
  { id: "upi", label: "UPI", icon: "📱" },
  { id: "card", label: "Credit / Debit Card", icon: "💳" },
  { id: "wallet", label: "Wallet", icon: "👛" },
  { id: "emi", label: "EMI", icon: "📅" },
  { id: "cod", label: "Cash on Delivery", icon: "💵" },
];

const WALLETS = [
  { id: "phonepe", label: "PhonePe", balance: 2450 },
  { id: "paytm", label: "Paytm", balance: 1820 },
  { id: "amazonpay", label: "Amazon Pay", balance: 960 },
  { id: "googlepay", label: "Google Pay", balance: 3200 },
];

function Checkout() {
  const [searchParams] = useSearchParams();
  const orderIdParam = searchParams.get("orderId");
  const navigate = useNavigate();
  const { cart, getTotalPrice, refreshCart } = useCart();

  const [order, setOrder] = useState(null);
  const [method, setMethod] = useState("upi");
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  const [upiId, setUpiId] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [cardName, setCardName] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");
  const [walletProvider, setWalletProvider] = useState("phonepe");
  const [emiMonths, setEmiMonths] = useState(3);
  const [emiOptions, setEmiOptions] = useState([]);

  const total = order?.total ?? getTotalPrice();

  useEffect(() => {
    const load = async () => {
      if (orderIdParam) {
        try {
          const data = await getOrder(Number(orderIdParam));
          setOrder(data);
        } catch {
          setError("Could not load order");
        }
      }
    };
    load();
  }, [orderIdParam]);

  useEffect(() => {
    if (method === "emi" && total >= 3000) {
      getEmiOptions(total)
        .then((data) => setEmiOptions(data.options || []))
        .catch(() => {
          setEmiOptions([
            calcEmi(total, 3),
            calcEmi(total, 6),
            calcEmi(total, 12),
          ]);
        });
    }
  }, [method, total]);

  const ensureOrder = async () => {
    if (order?.order_id) return order;
    if (cart.length === 0) throw new Error("Cart is empty");
    const created = await placeOrder();
    await refreshCart();
    setOrder(created);
    return created;
  };

  const validateForm = () => {
    if (method === "upi") return validateUpi(upiId);
    if (method === "card") return validateCard({ cardNumber, cardName, expiry, cvv });
    if (method === "wallet" && !walletProvider) return "Select a wallet";
    if (method === "emi" && total < 3000) return "EMI available above ₹3,000";
    return null;
  };

  const handlePay = async () => {
    setError("");
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setProcessing(true);
    try {
      let currentOrder = order;
      if (!currentOrder?.order_id) {
        currentOrder = await ensureOrder();
      }
      const id = currentOrder.order_id;

      await new Promise((r) => setTimeout(r, 2200));

      const paymentData = {
        payment_method: method,
        upi_id: method === "upi" ? upiId.trim() : undefined,
        card_number: method === "card" ? cardNumber : undefined,
        card_name: method === "card" ? cardName : undefined,
        expiry: method === "card" ? expiry : undefined,
        cvv: method === "card" ? cvv : undefined,
        wallet_provider: method === "wallet" ? walletProvider : undefined,
        emi_months: method === "emi" ? emiMonths : undefined,
      };

      const result = await processPayment(id, paymentData);
      navigate(`/order-success/${id}`, { state: { order: result } });
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || "Payment failed");
      setProcessing(false);
    }
  };

  const localEmi = [
    calcEmi(total, 3),
    calcEmi(total, 6),
    calcEmi(total, 12),
  ];
  const emiList = emiOptions.length ? emiOptions : localEmi;

  return (
    <div className="checkout-container">
      {processing && (
        <div className="payment-overlay">
          <div className="payment-modal">
            <div className="pay-spinner" />
            <h3>Processing payment...</h3>
            <p>Please wait while we confirm with your bank</p>
          </div>
        </div>
      )}

      <div className="checkout-header">
        <h1>Secure Checkout</h1>
        <p>Total payable: <strong>₹{total}</strong></p>
      </div>

      <div className="checkout-grid">
        <div className="checkout-summary card-panel">
          <h3>Order summary</h3>
          {(order?.items || cart).map((item, i) => (
            <div key={i} className="checkout-line">
              <span>{item.name}</span>
              <span>₹{item.price}</span>
            </div>
          ))}
          <div className="checkout-total-row">
            <span>Total</span>
            <span>₹{total}</span>
          </div>
        </div>

        <div className="checkout-payment card-panel">
          <h3>Payment method</h3>
          <div className="method-tabs">
            {METHODS.map((m) => (
              <button
                key={m.id}
                type="button"
                className={`method-tab ${method === m.id ? "active" : ""}`}
                onClick={() => setMethod(m.id)}
              >
                <span>{m.icon}</span> {m.label}
              </button>
            ))}
          </div>

          {error && <div className="checkout-error">{error}</div>}

          {method === "upi" && (
            <div className="pay-form">
              <label>UPI ID</label>
              <input
                placeholder="yourname@paytm or yourname@ybl"
                value={upiId}
                onChange={(e) => setUpiId(e.target.value)}
              />
              <p className="hint">Examples: demo@paytm, demo@ybl, demo@gpay</p>
              <div className="qr-section">
                <div className="qr-box">
                  <div className="qr-fake" />
                  <p>Scan QR to pay ₹{total}</p>
                </div>
              </div>
            </div>
          )}

          {method === "card" && (
            <div className="pay-form">
              <label>Card number</label>
              <input
                placeholder="4111 1111 1111 1111"
                value={cardNumber}
                onChange={(e) => setCardNumber(e.target.value)}
                maxLength={19}
              />
              <label>Name on card</label>
              <input
                placeholder="As on card"
                value={cardName}
                onChange={(e) => setCardName(e.target.value)}
              />
              <div className="card-row">
                <div>
                  <label>Expiry</label>
                  <input
                    placeholder="MM/YY"
                    value={expiry}
                    onChange={(e) => setExpiry(e.target.value)}
                    maxLength={5}
                  />
                </div>
                <div>
                  <label>CVV</label>
                  <input
                    type="password"
                    placeholder="123"
                    value={cvv}
                    onChange={(e) => setCvv(e.target.value)}
                    maxLength={4}
                  />
                </div>
              </div>
            </div>
          )}

          {method === "wallet" && (
            <div className="pay-form wallet-grid">
              {WALLETS.map((w) => (
                <button
                  key={w.id}
                  type="button"
                  className={`wallet-card ${walletProvider === w.id ? "selected" : ""}`}
                  onClick={() => setWalletProvider(w.id)}
                >
                  <strong>{w.label}</strong>
                  <span>Balance: ₹{w.balance.toLocaleString()}</span>
                </button>
              ))}
            </div>
          )}

          {method === "emi" && (
            <div className="pay-form">
              {total < 3000 ? (
                <p className="hint">EMI available for orders above ₹3,000</p>
              ) : (
                <div className="emi-options">
                  {emiList.map((opt) => (
                    <button
                      key={opt.emi_months || opt.months}
                      type="button"
                      className={`emi-card ${
                        emiMonths === (opt.emi_months || opt.months) ? "selected" : ""
                      }`}
                      onClick={() => setEmiMonths(opt.emi_months || opt.months)}
                    >
                      <span>{opt.emi_months || opt.months} months</span>
                      <strong>
                        ₹{(opt.monthly_amount || opt.monthly).toLocaleString()}/month
                      </strong>
                      <small>Total ₹{total}</small>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {method === "cod" && (
            <div className="pay-form cod-info">
              <p>Pay ₹{total} in cash when your order arrives.</p>
            </div>
          )}

          <button type="button" className="btn-pay-submit" onClick={handlePay} disabled={processing}>
            Pay ₹{total}
          </button>
          <button type="button" className="btn-back" onClick={() => navigate(-1)}>
            ← Back
          </button>
        </div>
      </div>
    </div>
  );
}

export default Checkout;
