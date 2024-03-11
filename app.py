import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Set page configuration and layout variables
st.set_page_config(
    page_title="Sales Analysis Dashboard",
    initial_sidebar_state="expanded"
)

# Database connection
conn = sqlite3.connect('user_data.db')
cur = conn.cursor()

# Create users table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

# Page functions
def validate_username(username):
    if len(username) < 4:
        return False
    return True

def validate_password(password):
    if len(password) < 6:
        return False
    return True

def login():
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_button = st.button("Login", disabled=not (validate_username(username_input) and validate_password(password_input)))

    if login_button:
        # Check if username and password match the records in the database
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username_input, password_input))
        user = cur.fetchone()
        if user:
            st.session_state.login_state = True
            st.session_state.username = username_input
            st.query_params.update(logged_in = True)  # Set query parameter to indicate login state  
            st.success("Login Successful")
            st.rerun() # Rerun the app to reflect the changes
        else:
            st.error("Invalid username or password")
    

def register():
    st.title("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    register_button = st.button("Register", disabled=not (validate_username(new_username) and validate_password(new_password) and new_password == confirm_password))

    if register_button:
        # Insert new user into the database
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_username, new_password))
        conn.commit()
        st.success("User registered successfully")

def main():
    st.sidebar.markdown(f"Welcome, {st.session_state.username}!")
    st.sidebar.markdown("---")
    st.sidebar.title("Select Data File for Analysis")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.login_state = False
        st.rerun()

    # Load the data
    selected_file = st.sidebar.selectbox('Select File', ["January Sales", "February Sales", "March Sales", "April Sales", "May Sales", "June Sales", "July Sales", "August Sales", "September Sales", "October Sales", "November Sales", "December Sales"])
    superSales = pd.read_csv(f'Data/{selected_file}.csv')

    # Display data and charts if logged in and data is uploaded
    st.title("Sales Analysis Dashboard")

    # Overall Sales Analysis
    fig_sales = px.line(superSales, x='Date', y='Total Sales', title='Overall Sales Analysis')
    st.plotly_chart(fig_sales)

    # Category-wise Sales Analysis for Cash Payments
    category_sales_cash = superSales.groupby('Cash')['Total Sales'].sum().reset_index()
    fig_category_sales_cash = px.pie(category_sales_cash, values='Total Sales', names='Cash', title='Cash Payments Sales Analysis')
    st.plotly_chart(fig_category_sales_cash)

    # Category-wise Sales Analysis for Card Payments
    category_sales_card = superSales.groupby('Card')['Total Sales'].sum().reset_index()
    fig_category_sales_card = px.pie(category_sales_card, values='Total Sales', names='Card', title='Card Payments Sales Analysis')
    st.plotly_chart(fig_category_sales_card)

# Render pages
if st.query_params.get("logged_in"):
    main()
else:
    st.title("Sales Analysis Dashboard")
    option = st.radio("Choose an option:", ["Login", "Register"])

    if option == "Login":
        login()
    elif option == "Register":
        register()
