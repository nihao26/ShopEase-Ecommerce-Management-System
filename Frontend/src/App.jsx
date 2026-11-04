
import { useEffect, useState } from "react";
import "./App.css";
const API_URL = "https://shopease-ecommerce-management-system.onrender.com/";
function App() {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState("home");
  const [message, setMessage] = useState("");
  const [customer, setCustomer] = useState(null);
  const [seller, setSeller] = useState(null);
  const [admin, setAdmin] = useState(null);
const [adminUsername, setAdminUsername] = useState("");
const [adminPassword, setAdminPassword] = useState("");

const [adminCustomers, setAdminCustomers] = useState([]);
const [adminSellers, setAdminSellers] = useState([]);
const [adminProducts, setAdminProducts] = useState([]);
const [adminOrders, setAdminOrders] = useState([]);
const [adminCategories, setAdminCategories] = useState([]);
const [categoryName, setCategoryName] = useState("");
const [categoryDescription, setCategoryDescription] = useState("");
const [sellerEmail, setSellerEmail] = useState("");
const [sellerPassword, setSellerPassword] = useState("");
const [sellerProducts, setSellerProducts] = useState([]);
const [productName, setProductName] = useState("");
const [productDescription, setProductDescription] = useState("");
const [productPrice, setProductPrice] = useState("");
const [productStock, setProductStock] = useState("");
const [productCategory, setProductCategory] = useState("");
const [editingProductId, setEditingProductId] = useState(null);
const [sellerOrders, setSellerOrders] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [cart, setCart] = useState([]);
const [cartTotal, setCartTotal] = useState(0);
const [orders, setOrders] = useState([]);
const [deliveryAddress, setDeliveryAddress] = useState("");
const [paymentMethod, setPaymentMethod] = useState("COD");

  useEffect(() => {
    fetch("${API_URL}/api/products")
      .then((response) => response.json())
      .then((data) => setProducts(data))
      .catch((error) => console.log(error));
  }, []);

  async function handleRegister(event) {
    event.preventDefault();

    const response = await fetch(
      "${API_URL}/api/customer/register",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          email,
          password,
          phone,
          address
        })
      }
    );

    const data = await response.json();
    setMessage(data.message);

    if (data.success) {
      setPage("login");
    }
  }

  async function handleLogin(event) {
    event.preventDefault();

    const response = await fetch(
      "${API_URL}/api/customer/login",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password })
      }
    );

    const data = await response.json();

    if (data.success) {
      setCustomer(data.customer);
      setMessage("Login successful!");
      setPage("home");
    } else {
      setMessage(data.message);
    }
  }
async function handleSellerLogin(event) {
  event.preventDefault();

  const response = await fetch(
    "${API_URL}/api/seller/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        email: sellerEmail,
        password: sellerPassword
      })
    }
  );

  const data = await response.json();

  if (data.success) {
    setSeller(data.seller);
    setMessage("Seller login successful!");
    setPage("seller");
  } else {
    setMessage(data.message);
  }
}
async function handleAdminLogin(event) {
  event.preventDefault();

  const response = await fetch(
    "${API_URL}/api/admin/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        username: adminUsername,
        password: adminPassword
      })
    }
  );

  const data = await response.json();

  if (response.ok && data.success) {
    setAdmin(data.admin);
    setMessage("Admin login successful!");
    setPage("admin");
  } else {
    setMessage(data.message);
  }
}
async function handleViewAdminCustomers() {
  const response = await fetch(
    "${API_URL}/api/admin/customers",
    { credentials: "include" }
  );

  const data = await response.json();

  if (response.ok) {
    setAdminCustomers(data);
  } else {
    setMessage(data.message);
  }
}

async function handleViewAdminSellers() {
  const response = await fetch(
    "${API_URL}/api/admin/sellers",
    { credentials: "include" }
  );

  const data = await response.json();

  if (response.ok) {
    setAdminSellers(data);
  } else {
    setMessage(data.message);
  }
}

async function handleViewAdminProducts() {
  const response = await fetch(
    "${API_URL}/api/admin/products",
    { credentials: "include" }
  );

  const data = await response.json();

  if (response.ok) {
    setAdminProducts(data);
  } else {
    setMessage(data.message);
  }
}

async function handleViewAdminOrders() {
  const response = await fetch(
    "${API_URL}/api/admin/orders",
    { credentials: "include" }
  );

  const data = await response.json();

  if (response.ok) {
    setAdminOrders(data);
  } else {
    setMessage(data.message);
  }
}async function handleViewAdminCategories() {
  const response = await fetch(
    "${API_URL}/api/admin/categories",
    { credentials: "include" }
  );

  const data = await response.json();

  if (response.ok) {
    setAdminCategories(data);
  } else {
    setMessage(data.message);
  }
}

async function handleAddCategory(event) {
  event.preventDefault();

  const response = await fetch(
    "${API_URL}/api/admin/categories",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        category_name: categoryName,
        description: categoryDescription
      })
    }
  );

  const data = await response.json();
  setMessage(data.message);

  if (response.ok) {
    setCategoryName("");
    setCategoryDescription("");
    handleViewAdminCategories();
  }
}

async function handleDeleteCategory(categoryId) {
  const response = await fetch(
    `${API_URL}/api/admin/categories/${categoryId}`,
    {
      method: "DELETE",
      credentials: "include"
    }
  );

  const data = await response.json();
  setMessage(data.message);

  if (response.ok) {
    handleViewAdminCategories();
  }
}
async function handleViewSellerProducts() {
  const response = await fetch(
    "${API_URL}/api/seller/products",
    {
      method: "GET",
      credentials: "include"
    }
  );

  const data = await response.json();

  if (response.ok) {
    setSellerProducts(data);
  } else {
    setMessage(data.message);
  }
}
async function handleAddProduct(event) {
  event.preventDefault();

  const response = await fetch(
    "${API_URL}/api/seller/products",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        category_id: Number(productCategory),
        name: productName,
        description: productDescription,
        price: Number(productPrice),
        stock: Number(productStock)
      })
    }
  );

  const data = await response.json();

  setMessage(data.message);

  if (response.ok && data.success) {
    setProductName("");
    setProductDescription("");
    setProductPrice("");
    setProductStock("");
    setProductCategory("");

    handleViewSellerProducts();
  }
}
async function handleUpdateProduct(event) {
  event.preventDefault();

  const response = await fetch(
    `${API_URL}/api/seller/products/${editingProductId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        category_id: Number(productCategory),
        name: productName,
        description: productDescription,
        price: Number(productPrice),
        stock: Number(productStock)
      })
    }
  );

  const data = await response.json();

  setMessage(data.message);

  if (response.ok && data.success) {
    setEditingProductId(null);
    setProductName("");
    setProductDescription("");
    setProductPrice("");
    setProductStock("");
    setProductCategory("");

    handleViewSellerProducts();
  }
}
async function handleDeleteProduct(productId) {
  const response = await fetch(
    `${API_URL}/api/seller/products/${productId}`,
    {
      method: "DELETE",
      credentials: "include"
    }
  );

  const data = await response.json();

  setMessage(data.message);

  if (response.ok && data.success) {
    handleViewSellerProducts();
  }
}
function handleEditProduct(product) {
  setEditingProductId(product.Product_id);
  setProductName(product.Product_name);
  setProductDescription(product.Description);
  setProductPrice(product.Price);
  setProductStock(product.Stock);
  setProductCategory(String(product.Category_id));
}
async function handleViewSellerOrders() {
  const response = await fetch(
    "${API_URL}/api/seller/orders",
    {
      method: "GET",
      credentials: "include"
    }
  );

  const data = await response.json();

  if (response.ok) {
    setSellerOrders(data);
  } else {
    setMessage(data.message);
  }
}
async function handleUpdateOrderStatus(orderId, status) {
  const response = await fetch(
    `${API_URL}/api/seller/orders/${orderId}/status`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({ status: status })
    }
  );

  const data = await response.json();

  setMessage(data.message);

  if (response.ok) {
    handleViewSellerOrders();
  }
}
async function handleAddToCart(productId) {
  const response = await fetch(
    "${API_URL}/api/cart/add",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        product_id: productId,
        quantity: 1
      })
    }
  );

  const data = await response.json();
  setMessage(data.message);
}

async function handleViewCart() {
  const response = await fetch(
    "${API_URL}/api/cart",
    {
      method: "GET",
      credentials: "include"
    }
  );

  const data = await response.json();

  if (response.ok) {
    setCart(data.items);
    setCartTotal(data.total);
    setPage("cart");
    setMessage("");
  } else {
    setMessage(data.message);
  }
}
async function handleViewOrders() {
  const response = await fetch(
    "${API_URL}/api/orders",
    {
      method: "GET",
      credentials: "include"
    }
  );

  const data = await response.json();

  if (response.ok) {
    setOrders(data);
    setPage("orders");
    setMessage("");
  } else {
    setMessage(data.message);
  }
}
async function handleUpdateCart(productId, quantity) {
  const response = await fetch(
    "${API_URL}/api/cart/update",
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        product_id: productId,
        quantity: quantity
      })
    }
  );

  const data = await response.json();
  setMessage(data.message);

  if (response.ok) {
    handleViewCart();
  }
}

async function handleRemoveCart(productId) {
  const response = await fetch(
    `${API_URL}/api/cart/remove/${productId}`,
    {
      method: "DELETE",
      credentials: "include"
    }
  );

  const data = await response.json();
  setMessage(data.message);

  if (response.ok) {
    handleViewCart();
  }
}
async function handlePlaceOrder(event) {
  event.preventDefault();

  const response = await fetch(
    "${API_URL}/api/orders",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        payment_method: paymentMethod,
        delivery_address: deliveryAddress
      })
    }
  );

  const data = await response.json();

  if (response.ok && data.success) {
    setMessage("Order placed successfully! Order ID: " + data.order_id);
    setCart([]);
    setCartTotal(0);
    setPage("home");
  } else {
    setMessage(data.message);
  }
}

  return (
    <div className="app">
      <header className="navbar">
        <h2 className="logo">ShopEase</h2>

        <nav>
          <a href="#home" onClick={() => setPage("home")}>Home</a>
          <a href="#products" onClick={() => setPage("home")}>Products</a>
          <a href="#cart" onClick={(e) => {
           e.preventDefault();
  handleViewCart();
}}>
  Cart
</a>
<a
  href="#orders"
  onClick={(e) => {
    e.preventDefault();
    handleViewOrders();
  }}
>
  My Orders
</a>
<a
  href="#seller-login"
  onClick={() => setPage("sellerLogin")}
>
  Seller Login
</a>
<a href="#admin-login" onClick={() => setPage("adminLogin")}>
  Admin Login
</a>
          {customer ? (
            <span>Welcome, {customer.Name}</span>
          ) : (
            <a href="#login" onClick={() => setPage("login")}>Login</a>
          )}
        </nav>
      </header>

      {page === "home" && (
        <>
          <section className="hero" id="home">
            <h1>Everything You Need, All in One Place.</h1>
            <p>Explore products across different categories.</p>
          </section>

          <section className="products" id="products">
            <h2>Our Products</h2>

            <div className="product-container">
              {products.map((product) => (
                <div className="product-card" key={product.Product_id}>
                  <h3>{product.Product_name}</h3>
                  <p>{product.Description}</p>
                  <p>Price: ₹{product.Price}</p>
                  <p>Stock: {product.Stock}</p>
                  <button onClick={() => handleAddToCart(product.Product_id)}>
  Add to Cart
</button>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
        {page === "cart" && (
  <section className="cart-section">
    <h2>My Shopping Cart</h2>

    {cart.length === 0 ? (
      <p>Your cart is empty.</p>
    ) : (
      cart.map((item) => (
        <div className="cart-item" key={item.Product_id}>
          <h3>{item.Product_name}</h3>
          <p>Price: ₹{item.Price}</p>
          <p>Quantity: {item.Quantity}</p>

<button
  disabled={item.Quantity <= 1}
  onClick={() =>
    handleUpdateCart(item.Product_id, item.Quantity - 1)
  }
>
  -
</button>

<button
  onClick={() =>
    handleUpdateCart(item.Product_id, item.Quantity + 1)
  }
>
  +
</button>

<button
  onClick={() => handleRemoveCart(item.Product_id)}
>
  Remove
</button>

<p>Subtotal: ₹{item.Subtotal}</p>
        </div>
      ))
    )}

    <h3>Total: ₹{cartTotal}</h3>

    <button onClick={() => setPage("home")}>
      Continue Shopping
    </button>
    <button onClick={() => setPage("checkout")}>
  Proceed to Checkout
</button>
  </section>
)}
{page === "orders" && (
  <section className="cart-section">
    <h2>My Orders</h2>

    {orders.length === 0 ? (
      <p>You have not placed any orders yet.</p>
    ) : (
      orders.map((order) => (
        <div className="cart-item" key={order.Order_id}>
          <h3>Order ID: {order.Order_id}</h3>

          <p>Total Amount: ₹{order.Total_amount}</p>

          <p>Payment Method: {order.Payment_method}</p>

          <p>Order Status: {order.Status}</p>

          <p>Delivery Address: {order.Delivery_address}</p>
        </div>
      ))
    )}

    <button onClick={() => setPage("home")}>
      Continue Shopping
    </button>
  </section>
)}
     {page === "checkout" && (
  <section className="auth-section">
    <h2>Checkout</h2>

    <h3>Order Total: ₹{cartTotal}</h3>

    <form onSubmit={handlePlaceOrder}>
      <label>Delivery Address</label>

      <textarea
        placeholder="Enter your delivery address"
        value={deliveryAddress}
        onChange={(e) => setDeliveryAddress(e.target.value)}
        required
      />

      <label>Payment Method</label>

      <select
        value={paymentMethod}
        onChange={(e) => setPaymentMethod(e.target.value)}
      >
        <option value="COD">Cash on Delivery</option>
        <option value="UPI">UPI</option>
        <option value="Card">Card</option>
      </select>

      <button type="submit">Place Order</button>
    </form>

    <button onClick={() => setPage("cart")}>
      Back to Cart
    </button>
  </section>
)}
      {page === "login" && (
        <section className="auth-section">
          <h2>Customer Login</h2>

          <form onSubmit={handleLogin}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit">Login</button>
          </form>

          <p>
            New customer?{" "}
            <button onClick={() => {
              setMessage("");
              setPage("register");
            }}>
              Register here
            </button>
          </p>
        </section>
      )}

     {page === "sellerLogin" && (
  <section className="auth-section">
    <h2>Seller Login</h2>

    <form onSubmit={handleSellerLogin}>
      <input
        type="email"
        placeholder="Seller Email"
        value={sellerEmail}
        onChange={(e) => setSellerEmail(e.target.value)}
        required
      />

      <input
        type="password"
        placeholder="Password"
        value={sellerPassword}
        onChange={(e) => setSellerPassword(e.target.value)}
        required
      />

      <button type="submit">Login as Seller</button>
    </form>
  </section>
)}
{page === "adminLogin" && (
  <section className="auth-section">
    <h2>Admin Login</h2>

    <form onSubmit={handleAdminLogin}>
      <input
        type="text"
        placeholder="Admin Username"
        value={adminUsername}
        onChange={(e) => setAdminUsername(e.target.value)}
        required
      />

      <input
        type="password"
        placeholder="Admin Password"
        value={adminPassword}
        onChange={(e) => setAdminPassword(e.target.value)}
        required
      />

      <button type="submit">Login as Admin</button>
    </form>
  </section>
)}
{page === "admin" && (
  <section className="cart-section">
    <h2>Admin Dashboard</h2>
    <h3>Welcome, Administrator!</h3>

    <div>
      <button onClick={handleViewAdminCustomers}>
        View Customers
      </button>

      <button onClick={handleViewAdminSellers}>
        View Sellers
      </button>

      <button onClick={handleViewAdminProducts}>
        View Products
      </button>

      <button onClick={handleViewAdminOrders}>
        View Orders
      </button>
    </div>

    <h3>Customers</h3>
    {adminCustomers.map((customer) => (
      <div className="cart-item" key={customer.Customer_id}>
        <p>Name: {customer.Name}</p>
        <p>Email: {customer.Email}</p>
      </div>
    ))}

    <h3>Sellers</h3>
    {adminSellers.map((seller) => (
      <div className="cart-item" key={seller.Seller_id}>
        <p>Name: {seller.Name}</p>
        <p>Email: {seller.Email}</p>
      </div>
    ))}

    <h3>Products</h3>
    {adminProducts.map((product) => (
      <div className="cart-item" key={product.Product_id}>
        <p>{product.Product_name}</p>
        <p>Price: ₹{product.Price}</p>
        <p>Stock: {product.Stock}</p>
      </div>
    ))}

    <h3>Orders</h3>
    {adminOrders.map((order) => (
      <div className="cart-item" key={order.Order_id}>
        <p>Order ID: {order.Order_id}</p>
        <p>Status: {order.Status}</p>
        <p>Total: ₹{order.Total_amount}</p>
      </div>
    ))}
    <h3>Category Management</h3>

<button onClick={handleViewAdminCategories}>
  View Categories
</button>

<form onSubmit={handleAddCategory}>
  <input
    type="text"
    placeholder="Category Name"
    value={categoryName}
    onChange={(e) => setCategoryName(e.target.value)}
    required
  />

  <input
    type="text"
    placeholder="Category Description"
    value={categoryDescription}
    onChange={(e) => setCategoryDescription(e.target.value)}
  />

  <button type="submit">Add Category</button>
</form>

{adminCategories.map((category) => (
  <div className="cart-item" key={category.Category_id}>
    <p>Name: {category.Category_name}</p>
    <p>Description: {category.Description}</p>

    <button
      onClick={() => handleDeleteCategory(category.Category_id)}
    >
      Delete
    </button>
  </div>
))}
  </section>
)}
{page === "seller" && (
  <section className="cart-section">
    <h2>Seller Dashboard</h2>

    <h3>Welcome to ShopEase, Seller!</h3>

    <div>
      <button onClick={handleViewSellerProducts}>
        My Products
      </button>

      <button onClick={handleViewSellerOrders}>
        My Orders
      </button>
    </div>

    <h3>My Products</h3>
    <h3>Add New Product</h3>

<form onSubmit={editingProductId ? handleUpdateProduct : handleAddProduct}>
  <input
    type="text"
    placeholder="Product Name"
    value={productName}
    onChange={(e) => setProductName(e.target.value)}
    required
  />

  <textarea
    placeholder="Product Description"
    value={productDescription}
    onChange={(e) => setProductDescription(e.target.value)}
    required
  />

  <input
    type="number"
    placeholder="Price"
    value={productPrice}
    onChange={(e) => setProductPrice(e.target.value)}
    min="0.01"
    step="0.01"
    required
  />

  <input
    type="number"
    placeholder="Stock"
    value={productStock}
    onChange={(e) => setProductStock(e.target.value)}
    min="0"
    required
  />

  <select
    value={productCategory}
    onChange={(e) => setProductCategory(e.target.value)}
    required
  >
    <option value="">Select Category</option>
    <option value="1">Electronics</option>
    <option value="2">Clothes</option>
    <option value="3">Beauty</option>
    <option value="4">Books</option>
    <option value="5">Home</option>
  </select>

<button type="submit">
  {editingProductId ? "Update Product" : "Add Product"}
</button>

{editingProductId && (
  <button
    type="button"
    onClick={() => {
      setEditingProductId(null);
      setProductName("");
      setProductDescription("");
      setProductPrice("");
      setProductStock("");
      setProductCategory("");
    }}
  >
    Cancel Editing
  </button>
)}
  
</form>

    {sellerProducts.length === 0 ? (
  <p>No products to display.</p>
) : (
  sellerProducts.map((product) => (
    <div className="cart-item" key={product.Product_id}>
      <h4>{product.Product_name}</h4>
      <p>Price: ₹{product.Price}</p>
      <p>Stock: {product.Stock}</p>

      <button onClick={() => handleEditProduct(product)}>
        Edit Product
      </button>
      <button onClick={() => handleDeleteProduct(product.Product_id)}>
  Delete Product
</button>
    </div>
  ))
)}

    <h3>Customer Orders</h3>

    {sellerOrders.length === 0 ? (
      <p>No orders to display.</p>
    ) : (
     sellerOrders.map((order) => (
  <div className="cart-item" key={order.Order_id}>
    <h4>Order ID: {order.Order_id}</h4>

    <p>Current Status: {order.Status}</p>

    <select
      value={order.Status}
      onChange={(e) =>
        handleUpdateOrderStatus(order.Order_id, e.target.value)
      }
    >
      <option value="Placed">Placed</option>
      <option value="Confirmed">Confirmed</option>
      <option value="Shipped">Shipped</option>
      <option value="Delivered">Delivered</option>
    </select>
  </div>
))  
    )}
  </section>
)}
      {page === "register" && (
        <section className="auth-section">
          <h2>Customer Registration</h2>

          <form onSubmit={handleRegister}>
            <input
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <input
              placeholder="Phone Number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />

            <input
              placeholder="Address"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              required
            />

            <button type="submit">Register</button>
          </form>

          <p>
            Already registered?{" "}
            <button onClick={() => {
              setMessage("");
              setPage("login");
            }}>
              Login here
            </button>
          </p>
        </section>
      )}

      {message && <p className="message">{message}</p>}

      <footer>
        <h3>ShopEase</h3>
        <p>Your one-stop destination for everyday shopping.</p>
      </footer>
    </div>
  );
}

export default App;
