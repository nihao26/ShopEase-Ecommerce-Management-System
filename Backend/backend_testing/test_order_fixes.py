import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from order import place_order, update_order_status

# Test invalid payment method
print("\n--- INVALID PAYMENT TEST ---")
print(place_order(1, "Cash", "Delhi"))

# Test empty delivery address
print("\n--- EMPTY ADDRESS TEST ---")
print(place_order(1, "COD", ""))

# Test invalid order status
print("\n--- INVALID STATUS TEST ---")
print(update_order_status(1, 1, "Cancelled"))

print("\nTests completed.")