import streamlit as st

# BankAccount Class
class BankAccount:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance

    def verify_pin(self, entered_pin):
        return self.pin == entered_pin

    def deposit(self, amount):
        self.balance += amount
        return f"✅ ₹{amount} deposited successfully. New balance: ₹{self.balance}"

    def withdraw(self, amount):
        if self.balance < amount:
            return "❌ Insufficient balance."
        else:
            self.balance -= amount
            return f"✅ ₹{amount} withdrawn successfully. New balance: ₹{self.balance}"

    def check_balance(self):
        return f"💰 {self.name}, your current balance is ₹{self.balance}"


# --- Initialize session state ---
if 'account' not in st.session_state:
    st.session_state.account = None
if 'page' not in st.session_state:
    st.session_state.page = 'create'  # 'create', 'login', 'menu'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# App Title
st.title("🏦 Harshal Co. Bank")
st.subheader("Simple & Secure Banking")

# --- Page 1: Create Account ---
if st.session_state.page == 'create' and st.session_state.account is None:
    st.header("🔐 Create Your Account")
    name = st.text_input("Enter your full name")
    pin = st.text_input("Set a 4-digit PIN", type="password", max_chars=4)

    if st.button("Create Account"):
        if not name.strip():
            st.error("Name cannot be empty.")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be exactly 4 digits.")
        else:
            st.session_state.account = BankAccount(name, int(pin))
            st.session_state.page = 'login'
            st.success(f"✅ Account created for {name}!")
            st.info("Please log in to continue.")
            st.rerun()  # Ensures immediate page switch

# --- Page 2: Login ---
elif st.session_state.page == 'login' or not st.session_state.logged_in:
    if not st.session_state.logged_in:
        st.header(f"👋 Welcome, {st.session_state.account.name}!")
        st.write("Please enter your PIN to continue.")
        pin = st.text_input("PIN", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                if pin.isdigit() and st.session_state.account.verify_pin(int(pin)):
                    st.session_state.logged_in = True
                    st.session_state.page = 'menu'
                    st.success("🔓 Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect PIN. Try again.")
        with col2:
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()

# --- Page 3: Main Menu ---
elif st.session_state.logged_in and st.session_state.page == 'menu':
    acc = st.session_state.account

    # Display balance at top
    bal_msg = acc.check_balance()
    st.markdown(f"### {bal_msg}")
    st.markdown("---")

    st.header("📋 Banking Menu")
    choice = st.radio("What would you like to do?", [
        "1. Deposit 💰",
        "2. Withdraw 💸",
        "3. Check Balance 🧾",
        "4. Logout 🚪"
    ])

    if choice == "1. Deposit 💰":
        amt = st.number_input("Enter amount to deposit:", min_value=0, step=10)
        if st.button("Deposit"):
            if amt > 0:
                msg = acc.deposit(amt)
                st.success(msg)
            else:
                st.warning("Enter a valid amount.")

    elif choice == "2. Withdraw 💸":
        amt = st.number_input("Enter amount to withdraw:", min_value=0, step=10)
        if st.button("Withdraw"):
            if amt > 0:
                msg = acc.withdraw(amt)
                if "✅" in msg:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Enter a valid amount.")

    elif choice == "3. Check Balance 🧾":
        if st.button("Refresh Balance"):
            st.info(acc.check_balance())

    elif choice == "4. Logout 🚪":
        if st.button("Confirm Logout"):
            st.session_state.clear()
            st.success("👋 You've been logged out. Thank you!")
            st.rerun()
