
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os
from admin import (
    login_admin,
    view_customers,
    view_sellers,
    view_all_products,
    view_all_orders,
    add_category,
    view_categories,
    delete_category
)
from seller import (
    login_seller,
    get_seller_details,
    get_seller_products
)

from order import get_seller_orders, update_order_status

from product import add_product, update_product, delete_product
from review import add_review, get_product_reviews
from order import (
    place_order,
    get_customer_orders,
    get_order_details
)
from product import (
    get_all_products,
    get_product_details,
    search_products,
    filter_products
)
from cart import (
    add_to_cart,
    view_cart,
    update_cart_quantity,
    remove_from_cart
)
from customer import (
    register_customer,
    login_customer,
    get_customer_details,
    update_customer_details
)

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-key-change-later"
)

CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    supports_credentials=True
)


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "E-Commerce API is running!"
    })


# CUSTOMER REGISTRATION
@app.route("/api/customer/register", methods=["POST"])
def customer_register():
    data = request.get_json()

    result = register_customer(
        data.get("name"),
        data.get("email"),
        data.get("password"),
        data.get("phone"),
        data.get("address")
    )

    return jsonify(result)


# CUSTOMER LOGIN
@app.route("/api/customer/login", methods=["POST"])
def customer_login():
    data = request.get_json()

    result = login_customer(
        data.get("email"),
        data.get("password")
    )

    if result["success"]:
        customer = result["customer"]
        customer_id = customer.get(
            "Customer_id",
            customer.get("customer_id")
        )

        session["customer_id"] = customer_id
        session["role"] = "customer"

    return jsonify(result)


# CUSTOMER PROFILE
@app.route("/api/customer/profile", methods=["GET"])
def customer_profile():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    customer = get_customer_details(
        session["customer_id"]
    )

    return jsonify(customer)


# UPDATE CUSTOMER PROFILE
@app.route("/api/customer/profile", methods=["PUT"])
def update_customer_profile():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = update_customer_details(
        session["customer_id"],
        data.get("name"),
        data.get("phone"),
        data.get("address")
    )

    return jsonify(result)


# CUSTOMER LOGOUT
@app.route("/api/customer/logout", methods=["POST"])
def customer_logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })


# GET ALL PRODUCTS
@app.route("/api/products", methods=["GET"])
def products():
    result = get_all_products()
    return jsonify(result)


# GET PRODUCT DETAILS
@app.route("/api/products/<int:product_id>", methods=["GET"])
def product_details(product_id):
    result = get_product_details(product_id)
    return jsonify(result)


# SEARCH PRODUCTS
@app.route("/api/products/search", methods=["GET"])
def search_product_list():
    keyword = request.args.get("keyword", "")
    result = search_products(keyword)
    return jsonify(result)


# FILTER PRODUCTS
@app.route("/api/products/filter", methods=["GET"])
def filter_product_list():
    category_id = request.args.get("category_id")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    result = filter_products(
        category_id=int(category_id) if category_id else None,
        min_price=float(min_price) if min_price else None,
        max_price=float(max_price) if max_price else None
    )

    return jsonify(result)


# VIEW CART
@app.route("/api/cart", methods=["GET"])
def cart():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = view_cart(session["customer_id"])
    return jsonify(result)


# ADD TO CART
@app.route("/api/cart/add", methods=["POST"])
def cart_add():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = add_to_cart(
        session["customer_id"],
        data.get("product_id"),
        data.get("quantity", 1)
    )

    return jsonify(result)


# UPDATE CART QUANTITY
@app.route("/api/cart/update", methods=["PUT"])
def cart_update():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = update_cart_quantity(
        session["customer_id"],
        data.get("product_id"),
        data.get("quantity")
    )

    return jsonify(result)


# REMOVE FROM CART
@app.route("/api/cart/remove/<int:product_id>", methods=["DELETE"])
def cart_remove(product_id):
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = remove_from_cart(
        session["customer_id"],
        product_id
    )

    return jsonify(result)

# PLACE ORDER / CHECKOUT
@app.route("/api/orders", methods=["POST"])
def create_order():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = place_order(
        session["customer_id"],
        data.get("payment_method"),
        data.get("delivery_address")
    )

    return jsonify(result)


# CUSTOMER ORDER HISTORY
@app.route("/api/orders", methods=["GET"])
def customer_orders():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = get_customer_orders(session["customer_id"])
    return jsonify(result)


# ORDER DETAILS
@app.route("/api/orders/<int:order_id>", methods=["GET"])
def order_details(order_id):
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = get_order_details(
        order_id,
        session["customer_id"]
    )

    return jsonify(result)


# ADD PRODUCT REVIEW
@app.route("/api/reviews", methods=["POST"])
def create_review():
    if session.get("role") != "customer":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = add_review(
        session["customer_id"],
        data.get("product_id"),
        data.get("rating"),
        data.get("comment", "")
    )

    return jsonify(result)


# GET PRODUCT REVIEWS
@app.route("/api/reviews/<int:product_id>", methods=["GET"])
def product_reviews(product_id):
    result = get_product_reviews(product_id)
    return jsonify(result)

# SELLER LOGIN
@app.route("/api/seller/login", methods=["POST"])
def seller_login():
    data = request.get_json()

    result = login_seller(
        data.get("email"),
        data.get("password")
    )

    if result["success"]:
        seller = result["seller"]
        seller_id = seller.get(
            "Seller_id",
            seller.get("seller_id")
        )

        session.clear()
        session["seller_id"] = seller_id
        session["role"] = "seller"

    return jsonify(result)


# SELLER PROFILE
@app.route("/api/seller/profile", methods=["GET"])
def seller_profile():
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = get_seller_details(session["seller_id"])
    return jsonify(result)


# SELLER PRODUCTS
@app.route("/api/seller/products", methods=["GET"])
def seller_products():
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = get_seller_products(session["seller_id"])
    return jsonify(result)


# ADD PRODUCT
@app.route("/api/seller/products", methods=["POST"])
def seller_add_product():
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = add_product(
        session["seller_id"],
        data.get("category_id"),
        data.get("name"),
        data.get("description"),
        data.get("price"),
        data.get("stock")
    )

    return jsonify(result)


# UPDATE PRODUCT
@app.route("/api/seller/products/<int:product_id>", methods=["PUT"])
def seller_update_product(product_id):
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = update_product(
        session["seller_id"],
        product_id,
        data.get("category_id"),
        data.get("name"),
        data.get("description"),
        data.get("price"),
        data.get("stock")
    )

    return jsonify(result)


# DELETE PRODUCT
@app.route("/api/seller/products/<int:product_id>", methods=["DELETE"])
def seller_delete_product(product_id):
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = delete_product(
        session["seller_id"],
        product_id
    )

    return jsonify(result)


# SELLER ORDERS
@app.route("/api/seller/orders", methods=["GET"])
def seller_orders():
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    result = get_seller_orders(session["seller_id"])
    return jsonify(result)


# UPDATE ORDER STATUS
@app.route("/api/seller/orders/<int:order_id>/status", methods=["PUT"])
def seller_update_order_status(order_id):
    if session.get("role") != "seller":
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    result = update_order_status(
        session["seller_id"],
        order_id,
        data.get("status")
    )

    return jsonify(result)


# SELLER LOGOUT
@app.route("/api/seller/logout", methods=["POST"])
def seller_logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Seller logged out successfully"
    })


# ADMIN LOGIN
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    result = login_admin(
        data.get("username"),
        data.get("password")
    )

    if result["success"]:
        admin = result["admin"]
        admin_id = admin.get(
            "Admin_id",
            admin.get("admin_id")
        )

        session.clear()
        session["admin_id"] = admin_id
        session["role"] = "admin"

    return jsonify(result)


# VIEW CUSTOMERS
@app.route("/api/admin/customers", methods=["GET"])
def admin_customers():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    return jsonify(view_customers())


# VIEW SELLERS
@app.route("/api/admin/sellers", methods=["GET"])
def admin_sellers():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    return jsonify(view_sellers())


# VIEW ALL PRODUCTS
@app.route("/api/admin/products", methods=["GET"])
def admin_products():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    return jsonify(view_all_products())


# VIEW ALL ORDERS
@app.route("/api/admin/orders", methods=["GET"])
def admin_orders():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    return jsonify(view_all_orders())


# VIEW CATEGORIES
@app.route("/api/admin/categories", methods=["GET"])
def admin_categories():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    return jsonify(view_categories())


# ADD CATEGORY
@app.route("/api/admin/categories", methods=["POST"])
def admin_add_category():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    data = request.get_json()

    result = add_category(
        data.get("category_name"),
        data.get("description", "")
    )

    return jsonify(result)


# DELETE CATEGORY
@app.route("/api/admin/categories/<int:category_id>", methods=["DELETE"])
def admin_delete_category(category_id):
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Admin login required"}), 401

    result = delete_category(category_id)
    return jsonify(result)


# ADMIN LOGOUT
@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Admin logged out successfully"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
