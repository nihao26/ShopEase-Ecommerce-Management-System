from database import get_connection
from security import hash_password, verify_password


def login_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT * FROM ADMIN WHERE Username = %s
        """, (username,))

        admin = cursor.fetchone()

        if not admin or not verify_password(
            password, admin["Password"]
        ):
            return {"success": False, "message": "Invalid username or password"}

        if not admin["Password"].startswith("pbkdf2_sha256$"):
            cursor.execute("""
                UPDATE ADMIN SET Password = %s
                WHERE Admin_id = %s
            """, (hash_password(password), admin["Admin_id"]))
            conn.commit()

        admin.pop("Password", None)

        return {"success": True, "admin": admin}

    finally:
        cursor.close()
        conn.close()


def view_customers():
    return _get_all("CUSTOMER", "Customer_id, Name, Email, Phone, Address")


def view_sellers():
    return _get_all("SELLER", "Seller_id, Name, Email, Phone, Address")


def view_all_products():
    return _get_all("PRODUCT")


def view_all_orders():
    return _get_all("ORDERS")


def _get_all(table_name, columns="*"):
    # Only fixed table names used by the functions above are allowed.
    allowed_tables = {
        "CUSTOMER", "SELLER", "PRODUCT", "ORDERS"
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")
        cursor.execute(f"SELECT {columns} FROM {table_name}")
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def add_category(category_name, description=""):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            INSERT INTO CATEGORY (Category_name, Description)
            VALUES (%s, %s)
        """, (category_name, description))

        conn.commit()

        return {
            "success": True,
            "message": "Category added",
            "category_id": cursor.lastrowid
        }

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()


def view_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT * FROM CATEGORY ORDER BY Category_name
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            DELETE FROM CATEGORY WHERE Category_id = %s
        """, (category_id,))

        changed = cursor.rowcount
        conn.commit()

        if changed == 0:
            return {"success": False, "message": "Category not found"}

        return {"success": True, "message": "Category deleted"}

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": "Category could not be deleted. Products may still use it."
        }

    finally:
        cursor.close()
        conn.close()