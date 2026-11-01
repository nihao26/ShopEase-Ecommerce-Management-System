from database import get_connection


def create_cart(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            INSERT IGNORE INTO CART (Customer_id)
            VALUES (%s)
        """, (customer_id,))

        conn.commit()

        cursor.execute("""
            SELECT Cart_id FROM CART WHERE Customer_id = %s
        """, (customer_id,))

        result = cursor.fetchone()

        if result:
            return {"success": True, "cart_id": result[0]}

        return {"success": False, "message": "Customer not found"}

    finally:
        cursor.close()
        conn.close()


def add_to_cart(customer_id, product_id, quantity=1):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        if quantity <= 0:
            return {"success": False, "message": "Quantity must be positive"}

        cursor.execute("""
            SELECT Stock, Status FROM PRODUCT
            WHERE Product_id = %s
        """, (product_id,))
        product = cursor.fetchone()

        if not product:
            return {"success": False, "message": "Product not found"}

        if product["Status"] != "Available" or product["Stock"] < quantity:
            return {"success": False, "message": "Insufficient stock"}

        cursor.execute("""
            INSERT IGNORE INTO CART (Customer_id)
            VALUES (%s)
        """, (customer_id,))

        cursor.execute("""
            SELECT Cart_id FROM CART WHERE Customer_id = %s
        """, (customer_id,))
        cart = cursor.fetchone()

        if not cart:
            return {"success": False, "message": "Customer not found"}

        cart_id = cart["Cart_id"]

        cursor.execute("""
            SELECT Quantity FROM CART_ITEM
            WHERE Cart_id = %s AND Product_id = %s
        """, (cart_id, product_id))

        existing = cursor.fetchone()
        new_quantity = quantity

        if existing:
            new_quantity += existing["Quantity"]

        if new_quantity > product["Stock"]:
            return {"success": False, "message": "Insufficient stock"}

        cursor.execute("""
            INSERT INTO CART_ITEM (Cart_id, Product_id, Quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE Quantity = %s
        """, (cart_id, product_id, new_quantity, new_quantity))

        conn.commit()
        return {"success": True, "message": "Cart updated"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()


def view_cart(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT Cart_id FROM CART WHERE Customer_id = %s
        """, (customer_id,))
        cart = cursor.fetchone()

        if not cart:
            return {"items": [], "total": 0}

        cursor.execute("""
            SELECT ci.Product_id, p.Product_name, p.Price,
                   ci.Quantity, p.Stock,
                   (p.Price * ci.Quantity) AS Subtotal
            FROM CART_ITEM ci
            JOIN PRODUCT p ON ci.Product_id = p.Product_id
            WHERE ci.Cart_id = %s
        """, (cart["Cart_id"],))

        items = cursor.fetchall()
        total = sum(float(item["Subtotal"]) for item in items)

        return {"items": items, "total": round(total, 2)}

    finally:
        cursor.close()
        conn.close()


def update_cart_quantity(customer_id, product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        if quantity <= 0:
            return {
                "success": False,
                "message": "Quantity must be positive; use remove_from_cart to remove an item"
            }

        cursor.execute("""
            SELECT c.Cart_id
            FROM CART c
            JOIN CART_ITEM ci ON c.Cart_id = ci.Cart_id
            WHERE c.Customer_id = %s AND ci.Product_id = %s
        """, (customer_id, product_id))
        cart_item = cursor.fetchone()

        if not cart_item:
            return {"success": False, "message": "Cart item not found"}

        cursor.execute("""
            SELECT Stock, Status FROM PRODUCT WHERE Product_id = %s
        """, (product_id,))
        product = cursor.fetchone()

        if not product or product["Status"] != "Available" or quantity > product["Stock"]:
            return {"success": False, "message": "Insufficient stock"}

        cursor.execute("""
            UPDATE CART_ITEM
            SET Quantity = %s
            WHERE Cart_id = %s AND Product_id = %s
        """, (quantity, cart_item["Cart_id"], product_id))

        conn.commit()
        return {"success": True, "message": "Quantity updated"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()


def remove_from_cart(customer_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            DELETE ci FROM CART_ITEM ci
            JOIN CART c ON ci.Cart_id = c.Cart_id
            WHERE c.Customer_id = %s AND ci.Product_id = %s
        """, (customer_id, product_id))

        changed = cursor.rowcount
        conn.commit()

        if changed == 0:
            return {"success": False, "message": "Cart item not found"}

        return {"success": True, "message": "Item removed from cart"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()