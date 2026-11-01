from database import get_connection
from security import hash_password, verify_password


def login_seller(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT * FROM SELLER WHERE Email = %s
        """, (email,))

        seller = cursor.fetchone()

        if not seller or not verify_password(
            password, seller["Password"]
        ):
            return {"success": False, "message": "Invalid email or password"}

        if not seller["Password"].startswith("pbkdf2_sha256$"):
            cursor.execute("""
                UPDATE SELLER SET Password = %s
                WHERE Seller_id = %s
            """, (
                hash_password(password),
                seller["Seller_id"]
            ))
            conn.commit()

        seller.pop("Password", None)

        return {"success": True, "seller": seller}

    finally:
        cursor.close()
        conn.close()


def get_seller_details(seller_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT Seller_id, Name, Email, Phone, Address
            FROM SELLER
            WHERE Seller_id = %s
        """, (seller_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def get_seller_products(seller_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT p.*, c.Category_name
            FROM PRODUCT p
            JOIN CATEGORY c ON p.Category_id = c.Category_id
            WHERE p.Seller_id = %s
            ORDER BY p.Product_id DESC
        """, (seller_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()