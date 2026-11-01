from database import get_connection
conn = get_connection()
cursor = conn.cursor()

# Opening the database
cursor.execute("USE ecommerce_db")

# Inserting data
# Inserting Customers
customer_query="""
    INSERT INTO CUSTOMER
    (Name,Email,Password,Phone,Address)
    VALUES(%s,%s,%s,%s,%s)
"""
customers=[
    ("Rahul Sharma","rahul123@gmail.com","rahul123","9876543210","H.no. 123 sec-1, noida"),
    ("Priya Verma","priya123@gmail.com","priya123","9876543211","H.no. 124 sec-1, delhi")
]
cursor.executemany(customer_query,customers)

# Inserting Sellers
seller_query="""
    INSERT INTO SELLER
    (Name,Email,Password,Phone,Address)
    VALUES(%s,%s,%s,%s,%s)
"""
sellers=[
    ("Tech World","techworld123@gmail.com","tech123","9887654321","Tech pvt.ltd., noida"),
    ("Fashion Hub","fashionhub123@gmail.com","fashion123","9877654321","Fashion club, delhi")
]
cursor.executemany(seller_query,sellers)

# Inserting admin
admin_query="""
    INSERT INTO ADMIN
    (Name,Username,Password)
    VALUES(%s,%s,%s)
"""
admin=("Samay Rana","sam123","samay123")
cursor.execute(admin_query,admin)

# Inserting categories
category_query="""
    INSERT INTO CATEGORY
    (Category_name,Description)
    VALUES(%s,%s)
"""
categories=[
    ("Electronics","Electronic items and devices"),
    ("Clothes","Men and Women Clothing"),
    ("Beauty","Hair Care and Makeup products"),
    ("Books","Books and Study material"),
    ("Home","Home and Kitchen products")
]
cursor.executemany(category_query,categories)

# Inserting products
product_query="""
    INSERT INTO PRODUCT
    (Seller_id,Category_id,Product_name,Description,Price,Stock,Status)
    VALUES(%s,%s,%s,%s,%s,%s,%s)
"""
products=[
    (1,1,"Wireless Mouse","Wireless Optical Mouse",599.0,10,"Available"),
    (1,5,"Mixer-Grinder","Kitchen Mixer, Juicer, Grinder",1999.0,5,"Available"),
    (1,1,"Headphones","Wireless Bluetooth Headphones",399.0,20,"Available"),
    (1,5,"Table Lamp","Table Lamp for Study tables",199.0,0,"Out of Stock"),
    (1,1,"Smartwatch","Smart Wearable watch with new features",999.0,10,"Available"),
    (2,3,"Foundation","Long-lasting Matte Foundation",199.0,50,"Available"),
    (2,3,"Hair dryer","Strong Blow Hair Dryer",599.0,0,"Out of Stock"),
    (2,2,"Denim Jeans","Regular fit denim jeans for boys",299.0,15,"Available"),
    (2,3,"Face Wash","Daily Use Anti-Tan Facewash",99.0,100,"Available"),
    (2,2,"Crop top","Cute Crop Top for Girls",499.0,5,"Available")
]
cursor.executemany(product_query,products)

conn.commit()
print("All data inserted successfully!")

cursor.close()
conn.close()