import streamlit as st

# --- Product class ---
class Product:
    def __init__(self, name, price, image_url):
        self.name = name
        self.price = price
        self.image_url = image_url

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
st.title("🛒 Simple Shopping Cart with Images")

# Define products
laptop = Product("Laptop", 1200, "https://cdn.pixabay.com/photo/2014/05/02/21/47/home-office-336377_1280.jpg")
mouse = Product("Mouse", 25, "https://cdn.pixabay.com/photo/2014/04/05/11/39/computer-mouse-316875_1280.jpg")
keyboard = Product("Keyboard", 50, "https://cdn.pixabay.com/photo/2016/11/18/12/43/keyboard-1837265_1280.jpg")

# Layout in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.image(laptop.image_url, caption="Laptop", use_column_width=True)
    qty_laptop = st.number_input("Laptops", min_value=0, max_value=10, step=1)

with col2:
    st.image(mouse.image_url, caption="Mouse", use_column_width=True)
    qty_mouse = st.number_input("Mice", min_value=0, max_value=10, step=1)

with col3:
    st.image(keyboard.image_url, caption="Keyboard", use_column_width=True)
    qty_keyboard = st.number_input("Keyboards", min_value=0, max_value=10, step=1)

# Discount code input
st.text_input("Discount Code (SAVE10, SAVE20, FREESHIP)", key="discount_code")

# Checkout button
if st.button("Checkout"):
    cart = ShoppingCart()
    cart.add_product(laptop, qty_laptop)
    cart.add_product(mouse, qty_mouse)
    cart.add_product(keyboard, qty_keyboard)

    discount_code = st.session_state.discount_code
    discount = cart.apply_discount_code(discount_code)
    if discount_code and discount == 0:
        st.warning("Invalid discount code.")

    st.subheader("🧾 Receipt")
    st.text(cart.generate_receipt())
