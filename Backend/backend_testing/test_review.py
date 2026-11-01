import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from review import add_review, get_product_reviews

# Add a review for Product ID 1 by Customer ID 1
print("\n--- ADD REVIEW ---")
result = add_review(
    1,
    1,
    5,
    "Good product, I am satisfied with the quality."
)
print(result)

# Display all reviews for Product ID 1
print("\n--- VIEW PRODUCT REVIEWS ---")
reviews = get_product_reviews(1)

for review in reviews:
    print(review)