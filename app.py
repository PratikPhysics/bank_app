import streamlit as st

# BankAccount Class (unchanged from your logic)
class BankAccount:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance

    def verify_pin(self, entered_pin):
        return self.pin == entered_pin

    def deposit(self, amount):
        self.balance += amount
        return f"✅ ₹{amount} deposited successfully. New balance is ₹{self.balance}"

    def withdraw(self, amount):
        if self.balance < amount:
            return "❌ Insufficient balance."
        else:
            self.balance -= amount
            return f"✅ ₹{amount} withdrawn successfully. New balance is ₹{self.balance}"

    def check_balance(self):
        return f"💰 {self.name}, your current balance is ₹{self.balance}"


# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = None
    st.session_state.step = 'create_account'  # Track app flow
    st.session_state.logged_in = False


# App Title
st.title("🏦 MyBank App")
st.subheader("Secure & Simple Banking")

# ---- Step 1: Create Account ----
if st.session_state.step == 'create_account':
    st.header("🔐 Create Your Bank Account")
    name = st.text_input("Enter your name")
    pin = st.text_input("Set a 4-digit PIN", type="password", max_chars=4)

    if st.button("Create Account"):
        if name.strip() == "":
            st.error("Please enter a valid name.")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be exactly 4 digits.")
        else:
            st.session_state.account = BankAccount(name, int(pin))
            st.session_state.step = 'menu'
            st.session_state.logged_in = False
            st.success(f"🎉 Account created for {name}! Now log in.")


# ---- Step 2: Login and Menu ----
elif st.session_state.step == 'menu':
    if not st.session_state.logged_in:
        st.header(f"👋 Welcome, {st.session_state.account.name}!")
        pin = st.text_input("Enter your PIN to continue", type="password")
        if st.button("Login"):
            if st.session_state.account.verify_pin(int(pin)):
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Incorrect PIN. Try again.")

    else:
        # Show Balance at top
        bal_msg = st.session_state.account.check_balance()
        st.markdown(f"### {bal_msg}")

        st.markdown("---")
        st.header("📋 Main Menu")

        choice = st.radio(
            "Select an option:",
            options=["1. Deposit 💰", "2. Withdraw 💸", "3. Check Balance 🧾", "4. Logout 🚪"]
        )

        if choice == "1. Deposit 💰":
            amt = st.number_input("Enter amount to deposit:", min_value=0, step=10)
            if st.button("Deposit"):
                if amt > 0:
                    msg = st.session_state.account.deposit(amt)
                    st.success(msg)
                else:
                    st.warning("Amount must be greater than zero.")

        elif choice == "2. Withdraw 💸":
            amt = st.number_input("Enter amount to withdraw:", min_value=0, step=10)
            if st.button("Withdraw"):
                if amt > 0:
                    msg = st.session_state.account.withdraw(amt)
                    if "✅" in msg:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Amount must be greater than zero.")

        elif choice == "3. Check Balance 🧾":
            if st.button("Refresh Balance"):
                bal_msg = st.session_state.account.check_balance()
                st.info(bal_msg)

        elif choice == "4. Logout 🚪":
            st.session_state.logged_in = False
            st.info("👋 You've been logged out. See you soon!")
