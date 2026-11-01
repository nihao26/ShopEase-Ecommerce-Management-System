import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from customer import login_customer, get_customer_details
from seller import login_seller, get_seller_products
from product import get_all_products, search_products
from cart import add_to_cart, view_cart
from admin import login_admin, view_categories
from review import get_product_reviews


print("\n--- CUSTOMER LOGIN ---")
print(login_customer("rahul123@gmail.com", "rahul123"))

print("\n--- SELLER LOGIN ---")
print(login_seller("techworld123@gmail.com", "tech123"))

print("\n--- ALL PRODUCTS ---")
print(get_all_products())

print("\n--- SEARCH PRODUCTS ---")
print(search_products("Mouse"))

print("\n--- CUSTOMER PROFILE ---")
print(get_customer_details(1))

print("\n--- SELLER PRODUCTS ---")
print(get_seller_products(1))

print("\n--- CUSTOMER CART ---")
print(view_cart(1))

print("\n--- PRODUCT REVIEWS ---")
print(get_product_reviews(1))

print("\n--- ADMIN LOGIN ---")
print(login_admin("sam123", "samay123"))

print("\n--- CATEGORIES ---")
print(view_categories())

print("\nBackend tests completed.")