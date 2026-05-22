import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { useCart } from "../CartContext";
import { getAllProducts } from "../products";
import "./Home.css";

function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [cartMessage, setCartMessage] = useState("");
  const { user } = useAuth();
  const { addToCart } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await getAllProducts();
      setProducts(data || []);
    } catch (err) {
      setError("Failed to load products. Make sure the product service is running on port 8001.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (product) => {
    if (!user) {
      alert("Please login first");
      navigate("/login");
      return;
    }

    try {
      await addToCart(product);
      setCartMessage(`${product.name} added to cart`);
      setTimeout(() => setCartMessage(""), 3000);
    } catch {
      setCartMessage("Failed to add to cart");
      setTimeout(() => setCartMessage(""), 3000);
    }
  };

  const categories = [
    "All",
    ...Array.from(new Set(products.map((p) => p.category).filter(Boolean))),
  ];

  const filteredProducts = products.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (p.description && p.description.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory =
      selectedCategory === "All" || p.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="home-container">
      <div className="home-hero">
        <div className="hero-copy">
          <span className="hero-badge">Fresh drops this week</span>
          <h1>ShopSphere</h1>
          <p>Electronics, fashion, skincare, beauty and healthcare products.</p>
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {cartMessage && (
        <div className={`cart-message ${cartMessage.includes("added") ? "success" : "error"}`}>
          {cartMessage}
        </div>
      )}

      <div className="search-controls">
        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          className="search-input"
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <div className="category-chips">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`category-chip ${selectedCategory === category ? "active" : ""}`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading products...</p>
        </div>
      ) : (
        <div className="products-grid">
          {filteredProducts.length > 0 ? (
            filteredProducts.map((p) => (
              <div key={p.id} className="product-card">
                <div className="product-image">
                  <img
                    src={p.image_url}
                    alt={p.name}
                    className="product-img"
                    onError={(e) => {
                      e.target.src =
                        "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500";
                    }}
                  />
                  <span className="product-category-badge">{p.category}</span>
                </div>

                <div className="product-info">
                  <h3 className="product-name">{p.name}</h3>
                  <p className="product-description">{p.description}</p>
                  <div className="product-extra">
                    <p>⭐ {p.rating} ({p.reviews} reviews)</p>
                    <p>🔥 {p.discount}</p>
                    <p>📦 Only {p.stock} left</p>
                  </div>
                  <div className="product-meta">
                    <p className="product-price">₹{p.price}</p>
                    <button onClick={() => handleAddToCart(p)} className="btn-add-to-cart">
                      🛒 Add To Cart
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="no-products">
              <p>No products found</p>
            </div>
          )}
        </div>
      )}

      <button onClick={fetchProducts} className="btn-refresh">
        🔄 Refresh Products
      </button>
    </div>
  );
}

export default Home;
