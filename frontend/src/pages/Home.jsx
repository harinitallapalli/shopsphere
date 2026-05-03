import { useEffect, useState } from "react";
import "./Home.css";

function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [cartMessage, setCartMessage] = useState("");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError("");
      const response = await fetch("http://127.0.0.1:8001/products");
      if (!response.ok) throw new Error("Fetch failed");
      const data = await response.json();
      setProducts(data || []);
    } catch (err) {
      setError("Failed to load products. Make sure product service is running.");
      console.log("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (product) => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("🔐 Please login first!");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8002/add-to-cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify(product)
      });
      const data = await response.json();
      setCartMessage(`✅ ${product.name} added to cart!`);
      setTimeout(() => setCartMessage(""), 3000);
    } catch (err) {
      setCartMessage("❌ Failed to add to cart");
      setTimeout(() => setCartMessage(""), 3000);
    }
  };

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (p.description && p.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="home-container">
      <div className="home-header">
        <h1>🏪 Shop Products</h1>
        <p>Discover our amazing collection</p>
      </div>

      {error && <div className="error-banner">{error}</div>}
      {cartMessage && <div className={`cart-message ${cartMessage.includes('✅') ? 'success' : 'error'}`}>{cartMessage}</div>}

      <div className="search-section">
        <input
          type="text"
          placeholder="🔍 Search products..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading products...</p>
        </div>
      ) : (
        <div className="products-grid">
          {filteredProducts && filteredProducts.length > 0 ? (
            filteredProducts.map((p, i) => (
              <div key={p.id || i} className="product-card">
                <div className="product-image">
                  <div className="product-placeholder">
                    📦
                  </div>
                </div>
                <div className="product-info">
                  <h3 className="product-name">{p.name}</h3>
                  {p.description && <p className="product-description">{p.description}</p>}
                  {p.category && <span className="product-category">{p.category}</span>}
                  <p className="product-price">₹{p.price}</p>
                  <button
                    onClick={() => addToCart(p)}
                    className="btn-add-to-cart"
                  >
                    🛒 Add to Cart
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="no-products">
              <p>😔 No products found</p>
              {searchTerm && <p>Try a different search term</p>}
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