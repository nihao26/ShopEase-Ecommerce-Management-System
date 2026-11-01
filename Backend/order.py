from database import get_connection


def place_order(customer_id, payment_method, delivery_address):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")
        conn.start_transaction()

        if payment_method not in ("COD", "UPI", "Card"):
            conn.rollback()
            return {
                "success": False,
                "message": "Invalid payment method"
            }

        if not delivery_address or not delivery_address.strip():
            conn.rollback()
            return {
                "success": False,
                "message": "Delivery address is required"
            }

        # Find the customer's cart
        cursor.execute("""
            SELECT Cart_id
            FROM CART
            WHERE Customer_id = %s
        """, (customer_id,))

        cart = cursor.fetchone()

        if not cart:
            conn.rollback()
            return {
                "success": False,
                "message": "Cart not found"
            }

        # Get cart items and lock their product rows
        cursor.execute("""
            SELECT ci.Product_id, ci.Quantity,
                   p.Price, p.Stock, p.Status, p.Product_name
            FROM CART_ITEM ci
            JOIN PRODUCT p ON ci.Product_id = p.Product_id
            WHERE ci.Cart_id = %s
            FOR UPDATE
        """, (cart["Cart_id"],))

        items = cursor.fetchall()

        if not items:
            conn.rollback()
            return {
                "success": False,
                "message": "Cart is empty"
            }

        total = 0

        # Validate stock and calculate total
        for item in items:
            if (
                item["Status"] != "Available"
                or item["Stock"] < item["Quantity"]
            ):
                conn.rollback()
                return {
                    "success": False,
                    "message": (
                        "Insufficient stock for "
                        + item["Product_name"]
                    )
                }

            total += item["Price"] * item["Quantity"]

        # Create the order
        cursor.execute("""
            INSERT INTO ORDERS
            (Customer_id, Total_amount, Payment_method,
             Status, Delivery_address)
            VALUES (%s, %s, %s, 'Placed', %s)
        """, (
            customer_id,
            total,
            payment_method,
            delivery_address
        ))

        order_id = cursor.lastrowid

        # Create order items and reduce stock
        for item in items:
            cursor.execute("""
                INSERT INTO ORDER_ITEM
                (Order_id, Product_id, Quantity, Price)
                VALUES (%s, %s, %s, %s)
            """, (
                order_id,
                item["Product_id"],
                item["Quantity"],
                item["Price"]
            ))

            new_stock = item["Stock"] - item["Quantity"]

            new_status = (
                "Out of Stock" if new_stock == 0
                else "Available"
            )

            cursor.execute("""
                UPDATE PRODUCT
                SET Stock = %s, Status = %s
                WHERE Product_id = %s
            """, (
                new_stock,
                new_status,
                item["Product_id"]
            ))

        # Clear the cart only after creating the order
        cursor.execute("""
            DELETE FROM CART_ITEM
            WHERE Cart_id = %s
        """, (cart["Cart_id"],))

        conn.commit()

        return {
            "success": True,
            "message": "Order placed successfully",
            "order_id": order_id,
            "total_amount": float(total)
        }

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": str(e)
        }

    finally:
        cursor.close()
        conn.close()


def get_customer_orders(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT * FROM ORDERS
            WHERE Customer_id = %s
            ORDER BY Order_date DESC
        """, (customer_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_order_details(order_id, customer_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        query = "SELECT * FROM ORDERS WHERE Order_id = %s"
        values = [order_id]

        if customer_id is not None:
            query += " AND Customer_id = %s"
            values.append(customer_id)

        cursor.execute(query, tuple(values))
        order = cursor.fetchone()

        if not order:
            return None

        cursor.execute("""
            SELECT oi.Product_id, p.Product_name,
                   oi.Quantity, oi.Price,
                   (oi.Quantity * oi.Price) AS Subtotal
            FROM ORDER_ITEM oi
            JOIN PRODUCT p ON oi.Product_id = p.Product_id
            WHERE oi.Order_id = %s
        """, (order_id,))

        order["items"] = cursor.fetchall()
        return order

    finally:
        cursor.close()
        conn.close()


def get_seller_orders(seller_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT o.Order_id, o.Customer_id, o.Order_date,
                   o.Status, o.Delivery_address,
                   oi.Product_id, p.Product_name,
                   oi.Quantity, oi.Price
            FROM ORDERS o
            JOIN ORDER_ITEM oi ON o.Order_id = oi.Order_id
            JOIN PRODUCT p ON oi.Product_id = p.Product_id
            WHERE p.Seller_id = %s
            ORDER BY o.Order_date DESC
        """, (seller_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def update_order_status(seller_id, order_id, new_status):
    allowed_statuses = (
        "Placed",
        "Confirmed",
        "Shipped",
        "Delivered"
    )

    if new_status not in allowed_statuses:
        return {
            "success": False,
            "message": "Invalid status. Cancellation is not supported here."
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        # Confirm that the order exists and contains products
        # belonging exclusively to this seller.
        cursor.execute("""
            SELECT COUNT(*)
            FROM ORDER_ITEM oi
            JOIN PRODUCT p ON oi.Product_id = p.Product_id
            WHERE oi.Order_id = %s
        """, (order_id,))

        total_items = cursor.fetchone()[0]

        if total_items == 0:
            return {
                "success": False,
                "message": "Order not found or contains no items"
            }

        cursor.execute("""
            SELECT COUNT(*)
            FROM ORDER_ITEM oi
            JOIN PRODUCT p ON oi.Product_id = p.Product_id
            WHERE oi.Order_id = %s
              AND p.Seller_id = %s
        """, (order_id, seller_id))

        seller_items = cursor.fetchone()[0]

        if seller_items != total_items:
            return {
                "success": False,
                "message": (
                    "Order not found or it contains products "
                    "belonging to another seller"
                )
            }

        cursor.execute("""
            UPDATE ORDERS
            SET Status = %s
            WHERE Order_id = %s
        """, (new_status, order_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return {
                "success": False,
                "message": "Order status was not changed"
            }

        conn.commit()

        return {
            "success": True,
            "message": "Order status updated successfully"
        }

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": str(e)
        }

    finally:
        cursor.close()
        conn.close()