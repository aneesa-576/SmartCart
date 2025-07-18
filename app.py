'''import streamlit as st
import json
from pathlib import Path
DATA_PATH = "data/products.json"

def load_products():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def save_product(product):
    products = load_products()
    products.append(product)
    with open(DATA_PATH, "w") as f:
        json.dump(products, f, indent=2)

st.title("🛒 SmartCart - Your Smart Shopping Assistant")

st.set_page_config(page_title="SmartCart", layout="wide")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📦 Product Entry")
    name = st.text_input("Product Name")
    brand = st.text_input("Brand")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    if st.button("Add Product"):
        st.success("Added (for now, just fake it)")

    st.markdown("---")
    st.header("💰 Set Budget")
    budget = st.number_input("Your Budget", min_value=0.0, format="%.2f")

with col2:
    st.header("📊 Budget Tracker")
    st.write("Show current total vs budget here.")

    st.header("📈 Price Comparison")
    st.write("Later: Automatically fetch deals.")

# On Add Product button:
#if st.button("Add Product"):
if st.button("Add Product", key=f"add_product_main"):
    new_product = {"name": name, "brand": brand, "price": price}
    save_product(new_product)
    st.success(f"Added {name}")

products = load_products()
total_spent = sum(p["price"] for p in products)

st.metric("Total Spent", f"₹{total_spent:.2f}")
if budget:
    st.metric("Remaining", f"₹{budget - total_spent:.2f}")'''

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
