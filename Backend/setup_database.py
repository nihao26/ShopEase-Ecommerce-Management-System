from database import get_connection
conn = get_connection()
cursor = conn.cursor()

# Creating Database
cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")
cursor.execute("USE ecommerce_db")
print("Database created successfully!")

# Creating tables
# 1. Customer
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CUSTOMER(
        Customer_id int AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Email VARCHAR(100) NOT NULL UNIQUE,
        Password VARCHAR(250) NOT NULL,
        Phone VARCHAR(15) NOT NULL UNIQUE,
        Address VARCHAR(250)
    )
""")

# 2. Seller
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SELLER(
        Seller_id int AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Email VARCHAR(100) NOT NULL UNIQUE,
        Password VARCHAR(250) NOT NULL,
        Phone VARCHAR(15) NOT NULL UNIQUE,
        Address VARCHAR(250)
    )
""")

# 3. Admin
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ADMIN(
        Admin_id int AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Username VARCHAR(20) NOT NULL UNIQUE,
        Password VARCHAR(250) NOT NULL
    )
""")

# 4. Category
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CATEGORY(
        Category_id int AUTO_INCREMENT PRIMARY KEY,
        Category_name VARCHAR(50) NOT NULL UNIQUE,
        Description VARCHAR(250)
    )
""")

# 5. Product
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PRODUCT(
        Product_id int AUTO_INCREMENT PRIMARY KEY,
        Seller_id int NOT NULL,
        Category_id int NOT NULL,
        Product_name VARCHAR(100) NOT NULL,
        Description TEXT,
        Price DECIMAL(10,2) NOT NULL CHECK(Price>=0),
        Stock int NOT NULL CHECK(Stock>=0),
        Status VARCHAR(20) NOT NULL DEFAULT('Available'),
        CHECK(Status IN ('Available', 'Out of Stock', 'Discontinued')),
        FOREIGN KEY (Seller_id) REFERENCES SELLER(Seller_id),
        FOREIGN KEY (Category_id) REFERENCES CATEGORY(Category_id)
    )
""")

# 6. Cart
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CART(
        Cart_id int AUTO_INCREMENT PRIMARY KEY,
        Customer_id int NOT NULL UNIQUE,
        Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (Customer_id) REFERENCES CUSTOMER(Customer_id) ON DELETE CASCADE
    )
""")

# 7. Cart_item
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CART_ITEM(
        Cart_item_id int AUTO_INCREMENT PRIMARY KEY,
        Cart_id int NOT NULL,
        Product_id int NOT NULL,
        Quantity int NOT NULL CHECK(Quantity>0),
        UNIQUE(Cart_id, Product_id),
        FOREIGN KEY (Cart_id) REFERENCES CART(Cart_id) ON DELETE CASCADE,
        FOREIGN KEY (Product_id) REFERENCES PRODUCT(Product_id) ON DELETE CASCADE
    )
""")

# 8. Orders
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ORDERS(
        Order_id int AUTO_INCREMENT PRIMARY KEY,
        Customer_id int NOT NULL,
        Order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Total_amount DECIMAL(10,2) NOT NULL CHECK(Total_amount>=0),
        Payment_method VARCHAR(20) NOT NULL,
        CHECK(Payment_method IN ('COD', 'UPI', 'Card')),
        Status VARCHAR(20) NOT NULL DEFAULT 'Placed',
        CHECK(Status IN ('Placed', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled')),
        Delivery_address VARCHAR(250) NOT NULL,
        FOREIGN KEY (Customer_id) REFERENCES CUSTOMER(Customer_id)
    )
""")

# 9. Order_item
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ORDER_ITEM(
        Order_item_id int AUTO_INCREMENT PRIMARY KEY,
        Order_id int NOT NULL,
        Product_id int NOT NULL,
        Quantity int NOT NULL CHECK(Quantity>0),
        Price DECIMAL(10,2) NOT NULL CHECK(Price>=0),
        FOREIGN KEY (Order_id) REFERENCES ORDERS(Order_id) ON DELETE CASCADE,
        FOREIGN KEY (Product_id) REFERENCES PRODUCT(Product_id) ON DELETE RESTRICT
    )
""")

# 10. Review
cursor.execute("""
    CREATE TABLE IF NOT EXISTS REVIEW(
        Review_id int AUTO_INCREMENT PRIMARY KEY,
        Customer_id int NOT NULL,
        Product_id int NOT NULL,
        Rating int NOT NULL CHECK(Rating BETWEEN 1 AND 5),
        Comment VARCHAR(500),
        Review_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (Customer_id, Product_id),
        FOREIGN KEY (Customer_id) REFERENCES CUSTOMER(Customer_id),
        FOREIGN KEY (Product_id) REFERENCES PRODUCT(Product_id) ON DELETE CASCADE
    )
""")

conn.commit()
print("All tables created successfully!")

cursor.close()
conn.close()