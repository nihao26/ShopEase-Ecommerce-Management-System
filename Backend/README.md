# E-Commerce Management System (Backend)

A DBMS course project built with **Python** and **MySQL**. It covers the complete backend logic of a small online shop: customer and seller accounts, product catalogue, cart, orders with stock handling, reviews, and basic admin controls.

The frontend and API layer (Flask) are developed separately and call the functions in this backend.

---

## Features

**Customer**
- Register and log in (passwords stored as salted PBKDF2 hashes)
- View and update profile
- Browse, search and filter products
- Add to cart, change quantity, remove items, view cart total
- Place orders (COD / UPI / Card) and view order history
- Review products (rating 1-5 with a comment)

**Seller**
- Log in and view profile
- Add, update and delete own products
- View orders for own products and update order status

**Admin**
- Log in
- View all customers, sellers, products and orders
- Add, view and delete product categories

---

## Tech Stack

| Part      | Technology                        |
| --------- | --------------------------------- |
| Language  | Python 3.10+                      |
| Database  | MySQL 8                           |
| Connector | `mysql-connector-python`          |
| Security  | `hashlib` (PBKDF2-HMAC-SHA256)    |

---

## Folder Structure

```
Backend/
├── database.py          # MySQL connection (get_connection)
├── security.py          # hash_password / verify_password
├── setup_database.py    # creates the database and all 10 tables
├── insert_data.py       # inserts sample data
├── customer.py          # register, login, profile
├── seller.py            # login, profile, seller's products
├── product.py           # list, details, search, filter, add, update, delete
├── cart.py              # cart operations
├── order.py             # place order, order history, seller orders, status
├── review.py            # add and view reviews
├── admin.py             # admin login, views, category management
├── backend_testing/     # simple test scripts
└── Documentation/       # relational schema and screenshots
```

---

## Database Tables

`CUSTOMER`, `SELLER`, `ADMIN`, `CATEGORY`, `PRODUCT`, `CART`, `CART_ITEM`, `ORDERS`, `ORDER_ITEM`, `REVIEW`

The relational schema is in `Documentation/`.

---

## Setup

### 1. Requirements
- Python 3.10 or newer
- MySQL Server running on your computer

### 2. Install the connector
```bash
pip install mysql-connector-python
```

### 3. Set your MySQL password
Open `database.py` and write your own MySQL username and password in the `get_connection()` function (the `user` and `password` fields).

### 4. Create the database and tables
Run these from inside the `Backend` folder, **in this order**:
```bash
python setup_database.py
python insert_data.py
```

> Run `insert_data.py` only **once**. Running it again causes duplicate-entry errors. To start fresh, run `DROP DATABASE ecommerce_db;` in MySQL, then repeat step 4.

---

## Sample Logins

| Role     | Login                          | Password     |
| -------- | ------------------------------ | ------------ |
| Customer | `rahul123@gmail.com`           | `rahul123`   |
| Customer | `priya123@gmail.com`           | `priya123`   |
| Seller   | `techworld123@gmail.com`       | `tech123`    |
| Seller   | `fashionhub123@gmail.com`      | `fashion123` |
| Admin    | username `sam123`              | `samay123`   |

The sample passwords are inserted as plain text. Each account is converted to a secure hash automatically the first time it logs in.

---

## Running the Tests

Run from inside the `Backend` folder:
```bash
python -m backend_testing.test_backend
python -m backend_testing.test_review
python -m backend_testing.test_order_fixes
```

Notes:
- These are print-based scripts: read the output to check the results.
- `test_operations.py` registers a customer and uses product ID 11, so it works only **once** on a fresh database.
- `test_review.py` fails with "already reviewed" if run a second time, which is expected.

---

## How the Backend Is Used (for API / Frontend Integration)

**Return format.** Action functions (register, add to cart, place order, ...) return a dictionary:
```python
{"success": True,  "message": "..."}      # success
{"success": False, "message": "..."}      # failure
```
Read functions (get products, view orders, ...) return a list or dictionary of rows.

**Important notes for the API layer**
- Prices and totals come from MySQL as `Decimal`, and dates as `datetime`. Flask's `jsonify` turns prices into strings such as `"599.00"`, so the frontend should convert them (for example `parseFloat`) before doing math.
- `customer_id`, `seller_id` and the admin identity must come from the **logged-in session**, never from the request body. Otherwise one user could act as another.
- `add_review` needs `rating` as an integer. Convert it with `int()` if it arrives as a string in the request.
- Login functions never return the password.

**Main functions per module**

| Module        | Functions |
| ------------- | --------- |
| `customer.py` | `register_customer`, `login_customer`, `get_customer_details`, `update_customer_details` |
| `seller.py`   | `login_seller`, `get_seller_details`, `get_seller_products` |
| `product.py`  | `get_all_products`, `get_product_details`, `search_products`, `filter_products`, `add_product`, `update_product`, `delete_product` |
| `cart.py`     | `create_cart`, `add_to_cart`, `view_cart`, `update_cart_quantity`, `remove_from_cart` |
| `order.py`    | `place_order`, `get_customer_orders`, `get_order_details`, `get_seller_orders`, `update_order_status` |
| `review.py`   | `add_review`, `get_product_reviews` |
| `admin.py`    | `login_admin`, `view_customers`, `view_sellers`, `view_all_products`, `view_all_orders`, `add_category`, `view_categories`, `delete_category` |

---

## Key Design Points

- **Parameterized queries** (`%s` placeholders) are used for all user input to prevent SQL injection.
- **Password hashing** with a random salt and 200,000 PBKDF2 iterations.
- **Transactions** in `place_order`: the order, order items, stock update and cart clearing are committed together, or rolled back if anything fails.
- **Row locking** (`SELECT ... FOR UPDATE`) while checking stock to avoid overselling.
- **Price snapshot**: `ORDER_ITEM` stores the price at purchase time, so later price changes do not alter old orders.
- **Ownership checks**: a seller can only update or delete their own products.
- **Constraints**: unique email/phone, `CHECK` constraints on price, stock, rating, status and payment method, plus foreign keys.

---

## Known Limitations / Future Scope

- No real payment gateway: the payment method is only recorded.
- Order cancellation with stock restoration is not implemented.
- Order status is stored per order, so an order containing products from several sellers cannot be updated by a single seller.
- Reviews are not restricted to customers who bought the product.
- A product that has been ordered cannot be deleted (foreign key restriction); it should be marked `Discontinued` instead.
- Test scripts are print-based and not automated.

---

## Author

Shrishti Aggarwal