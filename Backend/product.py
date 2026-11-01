from database import get_connection


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT p.Product_id, p.Seller_id, p.Category_id,
                   p.Product_name, p.Description, p.Price,
                   p.Stock, p.Status, c.Category_name,
                   s.Name AS Seller_name
            FROM PRODUCT p
            JOIN CATEGORY c ON p.Category_id = c.Category_id
            JOIN SELLER s ON p.Seller_id = s.Seller_id
            ORDER BY p.Product_id DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_product_details(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT p.*, c.Category_name, s.Name AS Seller_name
            FROM PRODUCT p
            JOIN CATEGORY c ON p.Category_id = c.Category_id
            JOIN SELLER s ON p.Seller_id = s.Seller_id
            WHERE p.Product_id = %s
        """, (product_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def search_products(keyword):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")
        pattern = "%" + keyword + "%"

        cursor.execute("""
            SELECT p.*, c.Category_name
            FROM PRODUCT p
            JOIN CATEGORY c ON p.Category_id = c.Category_id
            WHERE p.Product_name LIKE %s
               OR p.Description LIKE %s
               OR c.Category_name LIKE %s
        """, (pattern, pattern, pattern))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def filter_products(category_id=None, min_price=None, max_price=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        query = """
            SELECT p.*, c.Category_name
            FROM PRODUCT p
            JOIN CATEGORY c ON p.Category_id = c.Category_id
            WHERE 1 = 1
        """
        values = []

        if category_id is not None:
            query += " AND p.Category_id = %s"
            values.append(category_id)

        if min_price is not None:
            query += " AND p.Price >= %s"
            values.append(min_price)

        if max_price is not None:
            query += " AND p.Price <= %s"
            values.append(max_price)

        cursor.execute(query, tuple(values))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def add_product(seller_id, category_id, name, description,
                price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        status = "Available" if stock > 0 else "Out of Stock"

        cursor.execute("""
            INSERT INTO PRODUCT
            (Seller_id, Category_id, Product_name, Description,
             Price, Stock, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            seller_id, category_id, name, description,
            price, stock, status
        ))

        conn.commit()

        return {
            "success": True,
            "message": "Product added",
            "product_id": cursor.lastrowid
        }

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()


def update_product(seller_id, product_id, category_id, name,
                   description, price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        # A Discontinued product stays Discontinued; otherwise the
        # status follows the stock.
        cursor.execute("""
            UPDATE PRODUCT
            SET Category_id = %s,
                Product_name = %s,
                Description = %s,
                Price = %s,
                Stock = %s,
                Status = CASE
                    WHEN Status = 'Discontinued' THEN 'Discontinued'
                    WHEN %s > 0 THEN 'Available'
                    ELSE 'Out of Stock'
                END
            WHERE Product_id = %s AND Seller_id = %s
        """, (
            category_id, name, description, price,
            stock, stock, product_id, seller_id
        ))

        changed = cursor.rowcount
        conn.commit()

        if changed == 0:
            return {
                "success": False,
                "message": "Product not found or no changes made"
            }

        return {"success": True, "message": "Product updated"}

    except Exception as e:
        conn.rollback()
        print("update_product error:", e)
        return {"success": False, "message": "Could not update product"}

    finally:
        cursor.close()
        conn.close()


def delete_product(seller_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            DELETE FROM PRODUCT
            WHERE Product_id = %s AND Seller_id = %s
        """, (product_id, seller_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return {
                "success": False,
                "message": "Product not found or not owned by this seller"
            }

        conn.commit()
        return {"success": True, "message": "Product deleted"}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()