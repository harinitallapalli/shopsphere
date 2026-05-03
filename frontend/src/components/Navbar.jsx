import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { useCart } from "../CartContext";
import "./Navbar.css";

function Navbar() {
  const { user, logout } = useAuth();
  const { getTotalItems } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/home" className="navbar-logo">
          <span className="logo-icon">🛒</span>
          <span className="logo-text">ShopSphere</span>
        </Link>

        <div className="navbar-menu">
          <Link to="/home" className="navbar-link">
            🏠 Home
          </Link>

          <Link to="/cart" className="navbar-link">
            🛍️ Cart
            {getTotalItems() > 0 && (
              <span className="cart-badge">{getTotalItems()}</span>
            )}
          </Link>

          <Link to="/orders" className="navbar-link">
            📦 Orders
          </Link>

          {user ? (
            <>
              <div className="navbar-user">
                <span className="user-avatar">{user.username.charAt(0).toUpperCase()}</span>
                <span className="user-name">{user.username}</span>
              </div>
              <button onClick={handleLogout} className="btn-logout">
                Logout
              </button>
            </>
          ) : (
            <Link to="/login" className="btn-login-nav">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;