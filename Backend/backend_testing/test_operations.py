import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from customer import register_customer
from product import add_product, update_product
from cart import add_to_cart, update_cart_quantity, remove_from_cart
from review import add_review
from order import place_order, get_customer_orders

# 1. Register a new customer
print("\n1. Register Customer")
print(register_customer(
    "Test Customer",
    "testcustomer@example.com",
    "test123",
    "9000000001",
    "Test Address, Delhi"
))

# 2. Add a product for seller 1, category 1
print("\n2. Add Product")
print(add_product(
    1, 1, "Test Product",
    "Product created for backend testing",
    100, 10
))

# 3. Add product ID 11 to customer ID 1's cart
print("\n3. Add to Cart")
print(add_to_cart(1, 11, 2))

# 4. Update the cart quantity
print("\n4. Update Cart Quantity")
print(update_cart_quantity(1, 11, 3))

# 5. Place an order using the cart
print("\n5. Place Order")
print(place_order(
    1,
    "COD",
    "Test Delivery Address, Delhi"
))

# 6. View the customer's orders
print("\n6. Customer Orders")
print(get_customer_orders(1))