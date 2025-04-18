import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date

# CSV file path
DATA_FILE = "expenses.csv"

# Create CSV file if not exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv(DATA_FILE, index=False)

# Title
st.title("🎓 Student Expense Tracker")

# --- Add Expense Form ---
st.header("Add a New Expense")
with st.form(key="expense_form"):
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Study", "Others"])
    amount = st.number_input("Amount (₹)", min_value=1.0, format="%.2f")
    submit = st.form_submit_button("Add Expense")

# Save to CSV
if submit:
    new_data = pd.DataFrame([[expense_date, category, amount]], columns=["Date", "Category", "Amount"])
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success("Expense added successfully!")

# --- Load Data ---
df = pd.read_csv(DATA_FILE)

if not df.empty:
    st.header("📊 Summary")
    total_expense = df["Amount"].sum()
    daily_expense = df.groupby("Date")["Amount"].sum()
    category_expense = df.groupby("Category")["Amount"].sum()

    st.write(f"**Total Spent:** ₹{total_expense:.2f}")

    # --- Charts ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category-wise Spending")
        fig1, ax1 = plt.subplots()
        ax1.pie(category_expense, labels=category_expense.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        st.subheader("Daily Spending")
        fig2, ax2 = plt.subplots()
        daily_expense.plot(kind='bar', ax=ax2, color='skyblue')
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    st.subheader("📁 Expense Records")
    st.dataframe(df.sort_values(by="Date", ascending=False))

else:
    st.info("No expenses added yet.")

