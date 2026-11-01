import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cart import add_to_cart, view_cart

print(add_to_cart(1, 1, 2))
print(view_cart(1))