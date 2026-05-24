import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { useCart } from "../CartContext";
import { getAllProducts } from "../products";
import { Toast, useToast } from "../components/Toast";
import "./Home.css";

function StarRating({ rating }) {
  return (
    <div className="star-rating">
      {[1, 2, 3, 4, 5].map((s) => (
        <svg key={s} width="13" height="13" viewBox="0 0 24 24"
          fill={s <= Math.round(rating) ? "#f59e0b" : "none"}
          stroke="#f59e0b" strokeWidth="2">
          <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
        </svg>
      ))}
      <span className="rating-val">{rating}</span>
    </div>
  );
}

function SkeletonCard() {
  return (
    <div className="product-card skeleton-card">
      <div className="skeleton skeleton-img" />
      <div className="product-info">
        <div className="skeleton skeleton-line w60" />
        <div className="skeleton skeleton-line w90" />
        <div className="skeleton skeleton-line w40" />
        <div className="skeleton skeleton-line w70" />
      </div>
    </div>
  );
}

const CATEGORY_ICONS = {
  All: "⊞",
  Electronics: "💻",
  Fashion: "👗",
  Beauty: "💄",
  Healthcare: "❤️",
  Peripherals: "🖱️",
  Audio: "🎧",
  Wearables: "⌚",
  Fitness: "🏋️",
};

export default function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [addingId, setAddingId] = useState(null);
  const [sortBy, setSortBy] = useState("default");
  const [quickView, setQuickView] = useState(null);
  const { user } = useAuth();
  const { addToCart } = useCart();
  const navigate = useNavigate();
  const { toasts, addToast, removeToast } = useToast();

  useEffect(() => { fetchProducts(); }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await getAllProducts();
      setProducts(data || []);
    } catch (err) {
      setError("Could not load products. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (product, fromModal = false) => {
    if (!user) {
      addToast("Please sign in to add items to cart", "info");
      navigate("/login");
      return;
    }
    setAddingId(product.id);
    try {
      await addToCart(product);
      addToast(`${product.name} added to cart!`, "success");
      if (fromModal) setQuickView(null);
    } catch {
      addToast("Failed to add item to cart", "error");
    } finally {
      setAddingId(null);
    }
  };

  const categories = ["All", ...Array.from(new Set(products.map((p) => p.category).filter(Boolean)))];

  const filteredProducts = products
    .filter((p) => {
      const q = searchTerm.toLowerCase();
      return (
        (p.name.toLowerCase().includes(q) || (p.description || "").toLowerCase().includes(q)) &&
        (selectedCategory === "All" || p.category === selectedCategory)
      );
    })
    .sort((a, b) => {
      if (sortBy === "price-asc") return a.price - b.price;
      if (sortBy === "price-desc") return b.price - a.price;
      if (sortBy === "rating") return b.rating - a.rating;
      return 0;
    });

  return (
    <div className="home-wrap">
      <Toast toasts={toasts} removeToast={removeToast} />

      {/* Hero */}
      <section className="hero">
        <div className="hero-inner">
          <div className="hero-text">
            <span className="hero-pill">✨ Fresh drops this week</span>
            <h1>Shop Everything<br /><span className="hero-gradient">You Love</span></h1>
            <p>Electronics, fashion, skincare &amp; more — all in one place.</p>
            <div className="hero-actions">
              <button className="btn-hero-primary" onClick={() => document.getElementById("products-section").scrollIntoView({ behavior: "smooth" })}>
                Browse Products
              </button>
              <button className="btn-hero-ghost" onClick={() => navigate("/orders")}>
                My Orders
              </button>
            </div>
          </div>
          <div className="hero-stats">
            <div className="stat-card"><span className="stat-num">500+</span><span className="stat-label">Products</span></div>
            <div className="stat-card"><span className="stat-num">4.8★</span><span className="stat-label">Avg Rating</span></div>
            <div className="stat-card"><span className="stat-num">Free</span><span className="stat-label">Shipping</span></div>
          </div>
        </div>
      </section>

      {/* Controls */}
      <section className="controls-bar" id="products-section">
        <div className="search-wrap">
          <svg className="search-icon" width="18" height="18" fill="none" stroke="#9ca3af" strokeWidth="2" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            type="text"
            placeholder="Search products…"
            value={searchTerm}
            className="search-input"
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <button className="search-clear" onClick={() => setSearchTerm("")}>×</button>
          )}
        </div>

        <select className="sort-select" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="default">Sort: Default</option>
          <option value="price-asc">Price: Low → High</option>
          <option value="price-desc">Price: High → Low</option>
          <option value="rating">Top Rated</option>
        </select>
      </section>

      {/* Category chips */}
      <div className="category-row">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`cat-chip ${selectedCategory === cat ? "active" : ""}`}
          >
            <span>{CATEGORY_ICONS[cat] || "•"}</span>
            {cat}
          </button>
        ))}
      </div>

      {error && (
        <div className="error-banner">
          <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {error}
          <button onClick={fetchProducts} className="retry-btn">Retry</button>
        </div>
      )}

      {/* Results count */}
      {!loading && (
        <div className="results-meta">
          <span>{filteredProducts.length} product{filteredProducts.length !== 1 ? "s" : ""}{selectedCategory !== "All" ? ` in ${selectedCategory}` : ""}</span>
        </div>
      )}

      {/* Grid */}
      <div className="products-grid">
        {loading
          ? Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)
          : filteredProducts.length > 0
          ? filteredProducts.map((p) => (
              <div key={p.id} className="product-card" onClick={() => setQuickView(p)}>
                <div className="product-image">
                  <img
                    src={p.image_url}
                    alt={p.name}
                    className="product-img"
                    onError={(e) => { e.target.src = "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500"; }}
                  />
                  {p.discount && <span className="discount-badge">{p.discount}</span>}
                  <span className="cat-badge">{p.category}</span>
                  <div className="card-overlay">
                    <button className="overlay-quick" onClick={(e) => { e.stopPropagation(); setQuickView(p); }}>
                      Quick View
                    </button>
                  </div>
                </div>

                <div className="product-info">
                  <h3 className="product-name">{p.name}</h3>
                  <p className="product-desc">{p.description}</p>
                  <StarRating rating={p.rating} />
                  <span className="review-count">({(p.reviews || 0).toLocaleString()} reviews)</span>

                  <div className="stock-bar">
                    <div className="stock-fill" style={{ width: `${Math.min(100, (p.stock / 30) * 100)}%` }} />
                  </div>
                  <span className="stock-label">Only {p.stock} left</span>

                  <div className="product-footer">
                    <span className="product-price">₹{p.price.toLocaleString()}</span>
                    <button
                      className={`btn-add ${addingId === p.id ? "adding" : ""}`}
                      onClick={(e) => { e.stopPropagation(); handleAddToCart(p); }}
                      disabled={addingId === p.id}
                    >
                      {addingId === p.id ? (
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="spin"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
                      ) : (
                        <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
                      )}
                      {addingId === p.id ? "Adding…" : "Add to Cart"}
                    </button>
                  </div>
                </div>
              </div>
            ))
          : (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <h3>No products found</h3>
              <p>Try adjusting your search or filters</p>
              <button onClick={() => { setSearchTerm(""); setSelectedCategory("All"); }} className="btn-reset">
                Clear filters
              </button>
            </div>
          )}
      </div>

      {/* Quick View Modal */}
      {quickView && (
        <div className="modal-overlay" onClick={() => setQuickView(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setQuickView(null)}>×</button>
            <div className="modal-body">
              <div className="modal-img-wrap">
                <img src={quickView.image_url} alt={quickView.name} className="modal-img"
                  onError={(e) => { e.target.src = "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500"; }} />
                {quickView.discount && <span className="discount-badge">{quickView.discount}</span>}
              </div>
              <div className="modal-info">
                <span className="modal-category">{quickView.category}</span>
                <h2 className="modal-name">{quickView.name}</h2>
                <StarRating rating={quickView.rating} />
                <span className="review-count">({(quickView.reviews || 0).toLocaleString()} reviews)</span>
                <p className="modal-desc">{quickView.description}</p>
                <div className="modal-meta">
                  <div><span className="meta-label">Stock</span><span className="meta-val">{quickView.stock} units</span></div>
                  <div><span className="meta-label">Category</span><span className="meta-val">{quickView.category}</span></div>
                </div>
                <div className="modal-footer">
                  <span className="modal-price">₹{quickView.price.toLocaleString()}</span>
                  <button
                    className={`btn-add modal-btn-add ${addingId === quickView.id ? "adding" : ""}`}
                    onClick={() => handleAddToCart(quickView, true)}
                    disabled={addingId === quickView.id}
                  >
                    {addingId === quickView.id ? "Adding…" : "Add to Cart"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
