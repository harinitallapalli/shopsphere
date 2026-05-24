import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { useCart } from "../CartContext";
import { useTheme } from "../ThemeContext";
import "./Navbar.css";

function Navbar() {
  const { user, logout } = useAuth();
  const { getTotalItems } = useCart();
  const { dark, toggle } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
    setMenuOpen(false);
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/home" className="navbar-logo">
          <div className="logo-mark">S</div>
          <span className="logo-text">ShopSphere</span>
        </Link>

        <div className={`navbar-menu ${menuOpen ? "open" : ""}`}>
          <Link to="/home" className={`navbar-link ${isActive("/home") ? "active" : ""}`} onClick={() => setMenuOpen(false)}>
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>
            Home
          </Link>

          <Link to="/cart" className={`navbar-link cart-link ${isActive("/cart") ? "active" : ""}`} onClick={() => setMenuOpen(false)}>
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
            Cart
            {getTotalItems() > 0 && (
              <span className="cart-badge">{getTotalItems()}</span>
            )}
          </Link>

          <Link to="/orders" className={`navbar-link ${isActive("/orders") ? "active" : ""}`} onClick={() => setMenuOpen(false)}>
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg>
            Orders
          </Link>

          {/* Dark/Light toggle */}
          <button className="theme-toggle" onClick={toggle} aria-label="Toggle dark mode" title={dark ? "Switch to light mode" : "Switch to dark mode"}>
            {dark ? (
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
            ) : (
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
              </svg>
            )}
          </button>

          {user ? (
            <div className="navbar-user-group">
              <div className="navbar-user">
                <div className="user-avatar">{user.username.charAt(0).toUpperCase()}</div>
                <span className="user-name">{user.username}</span>
              </div>
              <button onClick={handleLogout} className="btn-logout">
                Sign out
              </button>
            </div>
          ) : (
            <Link to="/login" className="btn-login-nav" onClick={() => setMenuOpen(false)}>
              Sign in
            </Link>
          )}
        </div>

        <div className="navbar-right-mobile">
          <button className="theme-toggle" onClick={toggle} aria-label="Toggle dark mode">
            {dark ? (
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
            ) : (
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
              </svg>
            )}
          </button>
          <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle menu">
            <span /><span /><span />
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
