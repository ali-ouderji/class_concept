import streamlit as st

# --- Product class ---
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# --- Shopping Cart class ---
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount = 0  # percent

    def add_product(self, product, quantity):
        if quantity > 0:
            self.items.append((product, quantity))

    def apply_discount_code(self, code):
        codes = {"SAVE10": 10, "SAVE20": 20, "FREESHIP": 5}
        self.discount = codes.get(code.upper(), 0)
        return self.discount

    def total_price(self):
        subtotal = sum(product.price * qty for product, qty in self.items)
        discount_amount = subtotal * (self.discount / 100)
        return round(subtotal - discount_amount, 2)

    def generate_receipt(self):
        receipt_lines = []
        subtotal = 0
        for product, qty in self.items:
            line = f"{product.name} x{qty} = ${product.price * qty:.2f}"
            receipt_lines.append(line)
            subtotal += product.price * qty
        receipt_lines.append(f"\nSubtotal: ${subtotal:.2f}")
        if self.discount:
            discount_amount = subtotal * (self.discount / 100)
            receipt_lines.append(f"Discount: {self.discount}% (-${discount_amount:.2f})")
        receipt_lines.append(f"Total: ${self.total_price():.2f}")
        return "\n".join(receipt_lines)

# --- App UI ---
st.title("🛒 Simple Shopping Cart")

# Product catalog
laptop = Product("Laptop", 1200)
mouse = Product("Mouse", 25)
keyboard = Product("Keyboard", 50)

# Quantities
qty_laptop = st.number_input("Quantity of Laptops", min_value=0, max_value=10, step=1)
qty_mouse = st.number_input("Quantity of Mice", min_value=0, max_value=10, step=1)
qty_keyboard = st.number_input("Quantity of Keyboards", min_value=0, max_value=10, step=1)

# Discount code input
discount_code = st.text_input("Enter Discount Code (e.g., SAVE10, SAVE20, FREESHIP)")

# Checkout button
if st.button("Checkout"):
    cart = ShoppingCart()
    cart.add_product(laptop, qty_laptop)
    cart.add_product(mouse, qty_mouse)
    cart.add_product(keyboard, qty_keyboard)

    discount = cart.apply_discount_code(discount_code)
    if discount_code and discount == 0:
        st.warning("Invalid discount code.")

    st.subheader("🧾 Receipt")
    st.text(cart.generate_receipt())
