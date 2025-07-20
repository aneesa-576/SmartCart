import streamlit as st
import json
from pathlib import Path

# File path
PRODUCTS_FILE = Path("data/products.json")
PRODUCTS_FILE.parent.mkdir(parents=True, exist_ok=True)  # ensure "data" folder exists

# Load products
def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save product
def save_product(product):
    products = load_products()
    products.append(product)
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)

# --- Streamlit UI ---
st.title("🛒 SmartCart – Budget Tracker")

# Form inputs
product_name = st.text_input("Product Name")
price = st.number_input("Price", min_value=0.0, step=1.0)
category = st.selectbox("Category", ["Groceries", "Electronics", "Clothing", "Other"])

# Add button
if st.button("Add Product", key="add_product_button"):
    if product_name and price:
        product = {
            "name": product_name,
            "price": price,
            "category": category
        }
        save_product(product)
        st.success("✅ Product added!")
        products = load_products()
        for product in products:
            name = product.get("name", "Unnamed")
            price = product.get("price", "N/A")
            category = product.get("category", "Uncategorized")
            st.write(f"- {name} | ₹{price} | {category}") 
    else:
        st.warning("Please fill all fields.")

# Show saved products
st.subheader("📦 Saved Products")
for product in load_products():
    st.write(f"- {product['name']} | ₹{product['price']} | {product['category']}")

# Load products (again or reuse if already loaded)
products = load_products()

# 💸 Budget Summary
st.subheader("💸 Budget Summary")

if products:
    total_spent = sum(p.get("price", 0) for p in products)
    st.write(f"**Total Spent:** ₹{total_spent}")

    # 📊 Breakdown by Category
    category_totals = {}
    for p in products:
        category = p.get("category", "Uncategorized")
        category_totals[category] = category_totals.get(category, 0) + p.get("price", 0)

    st.write("**Spending by Category:**")
    for cat, amt in category_totals.items():
        st.write(f"- {cat}: ₹{amt}")
else:
    st.write("No products added yet.")
