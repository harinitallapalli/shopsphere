import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { login as apiLogin, register as apiRegister } from "../auth";
import "./Login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showDemoUsers, setShowDemoUsers] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const demoUsers = [
    { username: "demo", password: "demo123" },
    { username: "john", password: "john123" },
    { username: "sarah", password: "sarah123" },
    { username: "admin", password: "admin123" },
  ];

  const handleLogin = async () => {
    setLoading(true);
    setError("");
    
    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();
      
      if (data.token) {
        login(data.token, { username });
        alert("✅ Login successful!");
        navigate("/home");
      } else {
        setError("❌ Invalid credentials");
      }
    } catch (err) {
      setError("❌ Connection error. Make sure auth service is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (demoUsername, demoPassword) => {
    setUsername(demoUsername);
    setPassword(demoPassword);
    setShowDemoUsers(false);
    
    setTimeout(() => {
      handleLogin();
    }, 100);
  };

  const handleRegister = async () => {
    if (!username || !password) {
      setError("❌ Please fill in all fields");
      return;
    }
    
    setLoading(true);
    setError("");
    
    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();
      setError("✅ Registration successful! Now login.");
      setUsername("");
      setPassword("");
    } catch (err) {
      setError("❌ Registration failed");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleLogin();
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="logo-icon">🛒</div>
          <h1>ShopSphere</h1>
          <p>Welcome back</p>
        </div>

        {error && <div className={`error-message ${error.includes('✅') ? 'success' : ''}`}>{error}</div>}

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

          <button
            onClick={handleRegister}
            disabled={loading}
            className="btn-register"
          >
            {loading ? "Registering..." : "Create Account"}
          </button>
        </div>

        <div className="login-footer">
          <button 
            onClick={() => setShowDemoUsers(!showDemoUsers)}
            className="btn-demo-toggle"
          >
            {showDemoUsers ? "Hide Demo Users ▲" : "Show Demo Users ▼"}
          </button>

          {showDemoUsers && (
            <div className="demo-users-list">
              <h3>📝 Demo Accounts</h3>
              {demoUsers.map((user, index) => (
                <div key={index} className="demo-user-card">
                  <div className="demo-user-info">
                    <span className="demo-username">👤 {user.username}</span>
                    <span className="demo-password">🔑 {user.password}</span>
                  </div>
                  <button
                    onClick={() => handleDemoLogin(user.username, user.password)}
                    disabled={loading}
                    className="btn-quick-login"
                  >
                    Login
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;