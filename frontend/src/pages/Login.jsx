import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { login as loginApi, register as registerApi } from "../auth";
import "./Login.css";

const DEMO_ACCOUNTS = [
  { username: "demo", password: "demo123" },
  { username: "john", password: "john123" },
  { username: "admin", password: "admin123" },
];

export default function Login() {
  const [tab, setTab] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(null);
  const navigate = useNavigate();
  const { login } = useAuth();

  const showAlert = (message, type = "error") => {
    setAlert({ message, type });
    if (type === "success") setTimeout(() => setAlert(null), 4000);
  };

  const handleLogin = async () => {
  if (!username || !password) {
    showAlert("Please fill in all fields");
    return;
  }

  setLoading(true);
  setAlert(null);

  try {
    // 🔥 BYPASS BACKEND (since API is not working)
    if (username && password) {
      login("demo-token", { username });
      navigate("/home");
    } else {
      showAlert("Invalid credentials");
    }
  } catch (err) {
    showAlert("Something went wrong");
  } finally {
    setLoading(false);
  }
};

  const handleRegister = async () => {
    if (!username || !password) { showAlert("Please fill in all fields"); return; }
    if (password.length < 4) { showAlert("Password must be at least 4 characters"); return; }
    setLoading(true);
    setAlert(null);
    try {
      await registerApi(username, password);
      showAlert("Account created! You can now sign in.", "success");
      setTab("login");
      setPassword("");
    } catch (err) {
      showAlert(err?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (dUser, dPass) => {
    setUsername(dUser);
    setPassword(dPass);
    setLoading(true);
    setAlert(null);
    try {
      const data = await loginApi(dUser, dPass);
      if (data.token) {
        login(data.token, { username: data.username || dUser });
        navigate("/home");
      }
    } catch {
      showAlert("Demo login failed — try again");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* Left branding panel */}
      <div className="login-left">
        <div className="brand-logo">
          <div className="brand-mark">S</div>
          <span className="brand-name">ShopSphere</span>
        </div>
        <div className="login-left-content">
          <h2>Your world-class<span>shopping destination.</span></h2>
          <p>Browse thousands of products across electronics, fashion, beauty, and more — delivered fast and free.</p>
          <div className="login-perks">
            <div className="perk"><div className="perk-icon">🚚</div>Free & fast delivery on all orders</div>
            <div className="perk"><div className="perk-icon">🔒</div>Secure payments &amp; easy returns</div>
            <div className="perk"><div className="perk-icon">⭐</div>Thousands of 5-star reviewed products</div>
            <div className="perk"><div className="perk-icon">🎁</div>Exclusive deals every week</div>
          </div>
        </div>
      </div>

      {/* Right form panel */}
      <div className="login-right">
        <div className="login-right-header">
          <h1>{tab === "login" ? "Welcome back" : "Create account"}</h1>
          <p>{tab === "login" ? "Sign in to your ShopSphere account" : "Join ShopSphere today — it's free"}</p>
        </div>

        <div className="auth-tabs">
          <button className={`tab-btn ${tab === "login" ? "active" : ""}`} onClick={() => { setTab("login"); setAlert(null); }}>Sign In</button>
          <button className={`tab-btn ${tab === "register" ? "active" : ""}`} onClick={() => { setTab("register"); setAlert(null); }}>Register</button>
        </div>

        {alert && (
          <div className={`form-alert ${alert.type}`}>
            {alert.type === "error" ? "⚠️" : "✅"} {alert.message}
          </div>
        )}

        <form className="login-form" onSubmit={(e) => { e.preventDefault(); tab === "login" ? handleLogin() : handleRegister(); }}>
          <div className="form-group">
            <label>Username</label>
            <div className="input-wrap">
              <span className="input-icon">
                <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </span>
              <input type="text" placeholder="Enter your username" value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading} className="form-input" autoComplete="username" />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-wrap">
              <span className="input-icon">
                <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
              </span>
              <input type="password" placeholder="Enter your password" value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading} className="form-input" autoComplete={tab === "login" ? "current-password" : "new-password"} />
            </div>
          </div>

          {tab === "login" ? (
            <button type="submit" disabled={loading || !username || !password} className="btn-login">
              {loading ? "Signing in…" : "Sign In →"}
            </button>
          ) : (
            <button type="submit" disabled={loading || !username || !password} className="btn-login">
              {loading ? "Creating account…" : "Create Account →"}
            </button>
          )}

          {tab === "login" && (
            <div className="demo-section">
              <div className="demo-title">🎯 Try a demo account</div>
              <div className="demo-accounts">
                {DEMO_ACCOUNTS.map((acc) => (
                  <div className="demo-row" key={acc.username}>
                    <div className="demo-creds">
                      <span className="demo-user">{acc.username}</span>
                      <span className="demo-pass">{acc.password}</span>
                    </div>
                    <button className="btn-demo-use" onClick={() => handleDemoLogin(acc.username, acc.password)} disabled={loading}>
                      {loading ? "…" : "Use"}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
