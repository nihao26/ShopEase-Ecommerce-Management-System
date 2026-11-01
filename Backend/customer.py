from database import get_connection
from security import hash_password, verify_password
from mysql.connector import IntegrityError


def register_customer(name, email, password, phone, address):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            INSERT INTO CUSTOMER
            (Name, Email, Password, Phone, Address)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, hash_password(password), phone, address))

        customer_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO CART (Customer_id)
            VALUES (%s)
        """, (customer_id,))

        conn.commit()

        return {
            "success": True,
            "message": "Customer registered successfully",
            "customer_id": customer_id
        }

    except IntegrityError as e:
        conn.rollback()
        msg = str(e).lower()

        if e.errno == 1062 and "email" in msg:
            return {"success": False, "message": "Email is already registered"}
        if e.errno == 1062 and "phone" in msg:
            return {"success": False, "message": "Phone number is already registered"}
        return {"success": False, "message": "Could not register customer"}

    except Exception as e:
        conn.rollback()
        print("register_customer error:", e)
        return {"success": False, "message": "Could not register customer"}

    finally:
        cursor.close()
        conn.close()


def login_customer(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT * FROM CUSTOMER WHERE Email = %s
        """, (email,))

        customer = cursor.fetchone()

        if not customer or not verify_password(
            password, customer["Password"]
        ):
            return {"success": False, "message": "Invalid email or password"}

        if not customer["Password"].startswith("pbkdf2_sha256$"):
            cursor.execute("""
                UPDATE CUSTOMER SET Password = %s
                WHERE Customer_id = %s
            """, (
                hash_password(password),
                customer["Customer_id"]
            ))
            conn.commit()

        customer.pop("Password", None)

        return {"success": True, "customer": customer}

    finally:
        cursor.close()
        conn.close()


def get_customer_details(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")
        cursor.execute("""
            SELECT Customer_id, Name, Email, Phone, Address
            FROM CUSTOMER
            WHERE Customer_id = %s
        """, (customer_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def update_customer_details(customer_id, name, phone, address):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            UPDATE CUSTOMER
            SET Name = %s, Phone = %s, Address = %s
            WHERE Customer_id = %s
        """, (name, phone, address, customer_id))

        conn.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Customer not found"}

        return {"success": True, "message": "Profile updated"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()