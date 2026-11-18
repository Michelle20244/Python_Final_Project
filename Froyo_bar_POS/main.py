from datetime import datetime
from pathlib import Path

import streamlit as st
import read_menu


st.title("Welcome to the Froyo Bar!")

menu = read_menu.read_menu()

try:
    flavors = [item.strip() for item in menu["FLAVORS"].split(",")]
    toppings = [item.strip() for item in menu["TOPPINGS"].split(",")]
    sauces = [item.strip() for item in menu["SAUCES"].split(",")]
    price_per_ounce = float(menu["PRICES"])
except (KeyError, ValueError):
    st.error("Check that menu.txt has valid flavors, toppings, sauces, and price.")
    st.stop()

with st.form("order_form"):
    employee_id = st.number_input("Employee ID", min_value=1, step=1)
    first_name = st.text_input("First name")
    last_name = st.text_input("Last name")

    flavor = st.selectbox("Flavor", flavors)
    topping = st.selectbox("Topping", toppings)
    sauce = st.selectbox("Sauce", sauces)
    ounces = st.number_input("Ounces", min_value=0.1, value=1.0, step=0.1)

    submitted = st.form_submit_button("Place order")

if submitted:
    if not first_name.strip() or not last_name.strip():
        st.error("Enter the employee's first and last name.")
    else:
        total = round(ounces * price_per_ounce, 2)
        order_num = datetime.now().strftime("%Y%m%d%H%M%S%f")
        order = {
            "employee_id": int(employee_id),
            "flavor": flavor,
            "topping": topping,
            "sauce": sauce,
            "ounces": ounces,
            "price_per_ounce": price_per_ounce,
            "total": total,
        }

        orders_file = Path(__file__).with_name("all_orders.txt")
        with orders_file.open("a", encoding="utf-8") as file:
            file.write(f"{order_num}:{order}\n")

        st.success(f"Order {order_num} saved. Total: ${total:.2f}")
        st.write(order)
