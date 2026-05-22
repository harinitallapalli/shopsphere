import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { login as loginApi, register as registerApi } from "../auth";
import "./Login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await loginApi(username, password);

      if (data.token) {
        login(data.token, { username: data.username || username });
        navigate("/home");
      } else {
        setError("Invalid credentials");
      }
    } catch (err) {
      const msg = err?.message || "Connection error. Make sure auth service is running.";
      setError(msg.includes("Invalid") ? "Invalid credentials" : `Connection error. ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (demoUsername, demoPassword) => {
    setUsername(demoUsername);
    setPassword(demoPassword);
    // setShowDemoUsers(false);
    setTimeout(() => handleLogin(), 100);
  };

  const handleRegister = async () => {
    if (!username || !password) {
      setError("Please fill in all fields");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await registerApi(username, password);
      setError("Registration successful! Now login.");
      setUsername("");
      setPassword("");
    } catch (err) {
      setError(err?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleLogin();
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-hero">
          <div className="hero-badge">Welcome</div>
          <div className="hero-icon">🛍️</div>
          <p>Sign in to browse products, save your cart, and checkout faster.</p>
        </div>

        <div className="login-header">
          <div className="logo-icon">🛒</div>
          <h1>ShopSphere</h1>
          <p>Welcome back</p>
        </div>

        {error && (
          <div className={`error-message ${error.includes("successful") ? "success" : ""}`}>
            {error}
          </div>
        )}

        <div className="login-form">
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              className="form-input"
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading || !username || !password}
            className="btn-login"
          >
            {loading ? "Logging in..." : "Sign In"}
          </button>

          <div className="divider">OR</div>

          <button onClick={handleRegister} disabled={loading} className="btn-register">
            {loading ? "Registering..." : "Create Account"}
          </button>
        </div>

        </div>
      </div>
  );
}

export default Login;
