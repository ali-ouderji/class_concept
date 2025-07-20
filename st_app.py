import streamlit as st

# --- Product class ---
class Product:
    def __init__(self, name, price, image_url):
        self.name = name
        self.price = price
        self.image_url = image_url

# --- Shopping Cart class ---
import pandas as pd

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

    def subtotal(self):
        return sum(product.price * qty for product, qty in self.items)

    def total_price(self):
        return round(self.subtotal() * (1 - self.discount / 100), 2)

    def get_receipt_data(self):
        data = []
        for product, qty in self.items:
            total = product.price * qty
            data.append({
                "Product": product.name,
                "Quantity": qty,
                "Unit Price": f"${product.price:.2f}",
                "Total": f"${total:.2f}"
            })
        return pd.DataFrame(data)


# --- App UI ---
st.title("🛒 Simple Shopping Cart with Images")

# Define products
laptop = Product("Laptop", 1200, "laptop_new.png")
mouse = Product("Mouse", 25, "mouse_new.png")
keyboard = Product("Keyboard", 50, "keyboard_3.jpg")

# Layout in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.image(laptop.image_url, caption="Laptop", use_container_width=True)
    qty_laptop = st.number_input("Laptops", min_value=0, max_value=10, step=1)

with col2:
    st.image(mouse.image_url, caption="Mouse", use_container_width=True)
    qty_mouse = st.number_input("Mice", min_value=0, max_value=10, step=1)

with col3:
    st.image(keyboard.image_url, caption="Keyboard", use_container_width=True)
    qty_keyboard = st.number_input("Keyboards", min_value=0, max_value=10, step=1)

# Discount code input
st.text_input("Discount Code (SAVE10, SAVE20, FREESHIP)", key="discount_code")

# Checkout button
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

    st.subheader("🧾 Receipt Summary")

    receipt_df = cart.get_receipt_data()
    if receipt_df.empty:
        st.info("Your cart is empty.")
    else:
        st.table(receipt_df)

        subtotal = cart.subtotal()
        total = cart.total_price()
        discount_amt = subtotal * (cart.discount / 100)

        # Show pricing summary
        st.markdown("---")
        st.markdown(f"**Subtotal:** ${subtotal:.2f}")
        if cart.discount:
            st.markdown(f"**Discount ({cart.discount}%):** -${discount_amt:.2f}")
        st.markdown(f"### ✅ Total: ${total:.2f}")

