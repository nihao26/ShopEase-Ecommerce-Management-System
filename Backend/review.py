from database import get_connection
from mysql.connector import IntegrityError


def add_review(customer_id, product_id, rating, comment=""):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("USE ecommerce_db")

        if not isinstance(rating, int) or not 1 <= rating <= 5:
            return {"success": False, "message": "Rating must be between 1 and 5"}

        cursor.execute("""
            SELECT Product_id FROM PRODUCT WHERE Product_id = %s
        """, (product_id,))

        if not cursor.fetchone():
            return {"success": False, "message": "Product not found"}

        cursor.execute("""
            INSERT INTO REVIEW
            (Customer_id, Product_id, Rating, Comment)
            VALUES (%s, %s, %s, %s)
        """, (customer_id, product_id, rating, comment))

        conn.commit()

        return {
            "success": True,
            "message": "Review added",
            "review_id": cursor.lastrowid
        }

    except IntegrityError as e:
        conn.rollback()

        if e.errno == 1062:
            return {
                "success": False,
                "message": "You have already reviewed this product"
            }
        return {"success": False, "message": "Could not add review"}

    except Exception as e:
        conn.rollback()
        print("add_review error:", e)
        return {"success": False, "message": "Could not add review"}

    finally:
        cursor.close()
        conn.close()


def get_product_reviews(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("USE ecommerce_db")

        cursor.execute("""
            SELECT r.Review_id, r.Rating, r.Comment,
                   r.Review_date, c.Name AS Customer_name
            FROM REVIEW r
            JOIN CUSTOMER c ON r.Customer_id = c.Customer_id
            WHERE r.Product_id = %s
            ORDER BY r.Review_date DESC
        """, (product_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()