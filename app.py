
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Tracker")
st.write("Track your income, expenses and savings.")

# Add income
st.header("Add Your Income")

income = st.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    value=30000.0,
    step=1000.0
)

# Add expense
st.header("Add Your Expenses")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.form("expense_form"):
    category = st.selectbox(
        "Expense Category",
        ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]
    )

    amount = st.number_input(
        "Expense Amount (₹)",
        min_value=1.0,
        step=100.0
    )

    note = st.text_input("Description")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        st.session_state.expenses.append({
            "Category": category,
            "Amount": amount,
            "Description": note
        })
        st.success("Expense added successfully!")

# Display expenses
df = pd.DataFrame(st.session_state.expenses)

total_expenses = df["Amount"].sum() if not df.empty else 0
savings = income - total_expenses
savings_percentage = (savings / income * 100) if income > 0 else 0

st.header("Financial Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Monthly Income", f"₹{income:,.2f}")
col2.metric("Total Expenses", f"₹{total_expenses:,.2f}")
col3.metric("Remaining Savings", f"₹{savings:,.2f}")
col4.metric("Savings Rate", f"{savings_percentage:.2f}%")
st.subheader("Monthly Savings Progress")

progress = max(0.0, min(savings_percentage / 100, 1.0))

st.progress(progress)

st.write(f"You are saving {savings_percentage:.2f}% of your income.")

if not df.empty:
    st.header("Expense Breakdown")

    st.subheader("Expense History")

for index, expense in df.iterrows():
    col1, col2, col3, col4 = st.columns([2, 2, 3, 1])

    col1.write(expense["Category"])
    col2.write(f"₹{expense['Amount']:,.2f}")
    col3.write(expense["Description"])

    if col4.button("Delete", key=f"delete_{index}"):
        st.session_state.expenses.pop(index)
        st.rerun()

    category_totals = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    category_totals.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")

    st.pyplot(fig)
else:
    st.info("Add your first expense to see your financial dashboard.")

# Download Expenses as CSV
if not df.empty:
    st.header("Download Your Expenses")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Expenses as CSV",
        data=csv,
        file_name="my_expenses.csv",
        mime="text/csv"
    )

