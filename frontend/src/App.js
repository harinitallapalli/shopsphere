import { useEffect, useState } from "react";

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  // 🔹 Fetch products
  useEffect(() => {
    fetch("http://127.0.0.1:8001/products")
      .then(res => res.json())
      .then(data => setProducts(data));
  }, []);

  // 🔹 Add to cart
  const addToCart = (product) => {
    fetch("http://127.0.0.1:8002/add-to-cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(product)
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        setCart([...cart, product]);
      });
  };

  return (
    <div>
      <h1>ShopSphere</h1>

      <h2>Products</h2>
      {products.map((p, index) => (
        <div key={index}>
          {p.name} - ₹{p.price}
          <button onClick={() => addToCart(p)}>Add to Cart</button>
        </div>
      ))}

      <h2>Cart</h2>
      {cart.map((c, i) => (
        <div key={i}>{c.name}</div>
      ))}
    </div>
  );
}

export default App;