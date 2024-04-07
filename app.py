import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import re

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
        password TEXT,
        email TEXT UNIQUE,
        state TEXT,
        country TEXT,
        phone_number TEXT
    )
''')
conn.commit()

# Initialize session state variables
if 'login_state' not in st.session_state:
    st.session_state.login_state = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Page functions
def validate_username(username):
    if len(username) < 4:
        return "Username must be at least 4 characters long"
    return ""

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search("[A-Z]", password) or not re.search("[0-9]", password):
        return "Password must contain at least one capital letter and one number"
    return ""

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format"
    return ""

def validate_state(state):
    if len(state) < 2:
        return "State must be at least 2 characters long"
    return ""

def validate_country(country):
    if len(country) < 2:
        return "Country must be at least 2 characters long"
    return ""

def validate_phone_number(phone_number):
    if not re.match(r"^\+?[0-9]{10,15}$", phone_number):
        return "Invalid phone number format"
    return ""

def signup():
    st.title("Sign Up")
    new_username = st.text_input("Username")
    username_error = validate_username(new_username)
    if username_error:
        st.markdown(f'<p style="color:red">{username_error}</p>', unsafe_allow_html=True)

    new_password = st.text_input("Password", type="password")
    password_error = validate_password(new_password)
    if password_error:
        st.markdown(f'<p style="color:red">{password_error}</p>', unsafe_allow_html=True)

    email = st.text_input("Email")
    email_error = validate_email(email)
    if email_error:
        st.markdown(f'<p style="color:red">{email_error}</p>', unsafe_allow_html=True)

    state = st.text_input("State")
    state_error = validate_state(state)
    if state_error:
        st.markdown(f'<p style="color:red">{state_error}</p>', unsafe_allow_html=True)

    country = st.text_input("Country")
    country_error = validate_country(country)
    if country_error:
        st.markdown(f'<p style="color:red">{country_error}</p>', unsafe_allow_html=True)

    phone_number = st.text_input("Phone Number")
    phone_number_error = validate_phone_number(phone_number)
    if phone_number_error:
        st.markdown(f'<p style="color:red">{phone_number_error}</p>', unsafe_allow_html=True)

    # Check if any error exists to disable the register button
    error_exists = bool(username_error or password_error or email_error or state_error or country_error or phone_number_error)
    
    # Create an empty element to hold the button
    register_button_placeholder = st.empty()
    register_button = register_button_placeholder.button("Register", disabled=error_exists)

    if register_button:
        cur.execute('INSERT INTO users (username, password, email, state, country, phone_number) VALUES (?, ?, ?, ?, ?, ?)', 
                    (new_username, new_password, email, state, country, phone_number))
        conn.commit()
        st.success("User registered successfully")
        st.session_state.login_state = True


def login():
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Check if username and password match the records in the database
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username_input, password_input))
        user = cur.fetchone()
        if user:
            st.session_state.login_state = True
            st.session_state.username = username_input  # Initialize username
            st.query_params.update(logged_in=True)  # Set query parameter to indicate login state  
            st.success("Login Successful")
        else:
            st.error("Invalid username or password")

# import numpy as np

# def calculate_rating(sales_data, items_report):

    # print(sales_data)
    # print(items_report)
    # # Calculate total sales
    # total_sales = sales_data['Total Sales'].sum()

    # # Calculate average sales per bill
    # avg_sales_per_bill = total_sales / sales_data['Total no. of bills'].sum()

    # # Calculate percentage of cash payments
    # cash_percentage = (sales_data['Cash'].sum() / total_sales) * 100

    # # Calculate percentage of card payments
    # card_percentage = (sales_data['Card'].sum() / total_sales) * 100

    # # Calculate percentage of due payments
    # due_percentage = (sales_data['Due Payment'].sum() / total_sales) * 100

    # # Calculate total revenue from extras category items
    # extras_revenue = items_report[items_report['Category'] == 'Extras']['Total (₹)'].sum()

    # # Calculate total revenue from hot category items
    # hot_revenue = items_report[items_report['Category'] == 'Hot']['Total (₹)'].sum()

    # # Calculate total revenue from Indian Bread category items
    # indian_bread_revenue = items_report[items_report['Category'] == 'Indian Bread']['Total (₹)'].sum()

    # # Normalize statistical measures
    # sales_std_norm = np.std(sales_data['Total Sales']) / total_sales
    # sales_mean_norm = np.mean(sales_data['Total Sales']) / total_sales
    # cash_std_norm = np.std(sales_data['Cash']) / total_sales
    # card_std_norm = np.std(sales_data['Card']) / total_sales
    # due_std_norm = np.std(sales_data['Due Payment']) / total_sales

    # # Calculate the rating using normalized statistical variables
    # rating = (total_sales * 0.5) + (avg_sales_per_bill * 0.2) + (cash_percentage * 0.1) + \
    #          (card_percentage * 0.1) + (due_percentage * 0.05) + (extras_revenue * 0.025) + \
    #          (hot_revenue * 0.025) + (indian_bread_revenue * 0.025) + (sales_std_norm * 0.01) + \
    #          (sales_mean_norm * 0.01) + (cash_std_norm * 0.01) + (card_std_norm * 0.01) + (due_std_norm * 0.01)
    
    # print(rating)

    # # Normalize the rating to ensure it remains within the range of 0 to 5
    # max_possible_rating = 5
    # normalized_rating = min(rating, max_possible_rating)

    # return round(normalized_rating, 2)

import numpy as np

def calculate_rating(sales_data, items_report):
     # Extracting relevant columns from sales data
    total_sales = sales_data['Total Sales'].sum()
    total_bills = sales_data['Total no. of bills'].sum()

    # Extracting relevant columns from items report
    total_items_sold = items_report['Qty.'].sum()
    unique_items_sold = len(items_report['Item'].unique())
    total_categories = len(items_report['Category'].unique())

    # Weight factors for different components
    weight_sales = 0.65
    weight_items_sold = 0.2
    weight_unique_items = 0.05
    weight_categories = 0.1

    # Calculate component scores
    score_sales = total_sales / total_bills
    score_items_sold = total_items_sold / total_bills
    score_unique_items = unique_items_sold / total_items_sold if total_items_sold > 0 else 0
    score_categories = total_categories / total_items_sold if total_items_sold > 0 else 0

    # Normalize scores
    max_score = max(score_sales, score_items_sold, score_unique_items, score_categories)
    min_score = min(score_sales, score_items_sold, score_unique_items, score_categories)

    if max_score != min_score:
        score_sales = (score_sales - min_score) / (max_score - min_score)
        score_items_sold = (score_items_sold - min_score) / (max_score - min_score)
        score_unique_items = (score_unique_items - min_score) / (max_score - min_score)
        score_categories = (score_categories - min_score) / (max_score - min_score)

    # Calculate weighted average rating
    rating = (weight_sales * score_sales) + (weight_items_sold * score_items_sold) + \
             (weight_unique_items * score_unique_items) + (weight_categories * score_categories)

    # Ensure rating is between 0 and 5
    rating = min(max(rating * 5, 0), 5)

    # Limiting rating to two decimal places
    rating = round(rating, 2)

    return rating
# Example usage:
# rating = calculate_rating(sales_data, items_report)


def main():
    st.sidebar.markdown(f"Welcome, {st.session_state.username}!")
    st.sidebar.title("Select Data File for Analysis")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.login_state = False
        st.session_state.username = ""
        st.query_params.pop("logged_in", None)
        st.rerun()

    # Upload sales report
    uploaded_sales_file = st.sidebar.file_uploader("Upload Sales Report (CSV)", type=["csv"])
    uploaded_items_file = st.sidebar.file_uploader("Upload Items Report (CSV)", type=["csv"])

    analyze_button_enabled = uploaded_sales_file is not None and uploaded_items_file is not None
    analyze_button = st.sidebar.button("Analyze", disabled=not analyze_button_enabled)

    if analyze_button:
        try:
            superSales = pd.read_csv(uploaded_sales_file)  # Attempt to read sales report as CSV
            items_report = pd.read_csv(uploaded_items_file)  # Attempt to read items report as CSV

            # Convert numeric values to strings in the 'Total (₹)' column
            items_report['Total (₹)'] = items_report['Total (₹)'].astype(str)

            # Remove commas from the 'Total (₹)' column and convert it to float
            items_report['Total (₹)'] = items_report['Total (₹)'].str.replace(',', '').astype(float)

            
            # Calculate rating
            rating = calculate_rating(superSales, items_report)

            # Display data and charts
            st.title("Sales Analysis Dashboard")
            
            # Display rating on the sidebar
            st.subheader("Restaurant Rating")

            # Convert numerical rating to stars format with partial star coloring
            stars = int(rating)
            fractional_part = rating - stars
            full_stars = "★" * stars
            partial_star = "★" if fractional_part >= 0.75 else "☆" if fractional_part >= 0.25 else "☆"
            empty_stars = "☆" * (5 - stars - 1)

            # Create HTML with CSS to style the stars
            stars_html = f"""
                    <span style="font-size: 20px; color: gold;">{full_stars}{partial_star}{empty_stars}</span>
            """

            # Display rating in numerical format and stars format
            st.write(f"Rating: {stars_html} {rating:.2f}/5", unsafe_allow_html=True)

            # Display rating formula on the sidebar
            st.subheader("Rating Formula")
            st.markdown(
                """
                The formula for calculating the restaurant rating is as follows:

                1. **Component Scores Calculation:**
                    - **Sales Score:** $$\\text{Score}_{\\text{sales}} = \\frac{\\text{Total Sales}}{\\text{Total Number of Bills}} $$
                    - **Items Sold Score:** $$ \\text{Score}_{\\text{items\_sold}} = \\frac{\\text{Total Items Sold}}{\\text{Total Number of Bills}} $$
                    - **Unique Items Score:** $$ \\text{Score}_{\\text{unique\_items}} = \\frac{\\text{Number of Unique Items Sold}}{\\text{Total Items Sold}} $$ (if Total Items Sold > 0, else 0)
                    - **Categories Score:** $$ \\text{Score}_{\\text{categories}} = \\frac{\\text{Number of Unique Categories}}{\\text{Total Items Sold}} $$ (if Total Items Sold > 0, else 0)


                2. **Normalization:**
                    - Normalize all scores to ensure they are on the same scale by subtracting the minimum score and dividing by the range (maximum score - minimum score).

                3. **Weighted Average Rating:**
                    - The weighted average rating is calculated as follows:
                        $$
                        \\text{Rating} = (0.65 \\times \\text{Score}_{\\text{sales}}) + (0.2 \\times \\text{Score}_{\\text{items\_sold}}) + (0.05 \\times \\text{Score}_{\\text{unique\_items}}) + (0.1 \\times \\text{Score}_{\\text{categories}})
                        $$

                4. **Rating Adjustment:**
                    - Ensure the rating is between 0 and 5 by multiplying by 5 and taking the minimum of the maximum of the rating and 0.

                5. **Limiting Decimal Places:**
                    - Round the rating to two decimal places.
                """
            )

            # Statistics from items report
            st.subheader("Sales Analysis")

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

            # Statistics from items report
            st.title("Items Report Statistics")

            # Bar graph to show top 10 items by quantity
            top_items_qty = items_report.sort_values(by='Qty.', ascending=False).head(10)
            fig_top_items_qty = px.bar(top_items_qty, x='Item', y='Qty.', title='Top 10 Items by Quantity')
            st.plotly_chart(fig_top_items_qty)

            # Bar graph to show top 10 items by total revenue
            top_items_revenue = items_report.sort_values(by='Total (₹)', ascending=False).head(10)
            fig_top_items_revenue = px.bar(top_items_revenue, x='Item', y='Total (₹)', title='Top 10 Items by Total Revenue')
            st.plotly_chart(fig_top_items_revenue)

            # Heading for Category-wise Analysis
            st.title("Category-wise Analysis")

            # # Category-wise Analysis using Sunburst Chart
            # st.subheader("Category-wise Analysis using Sunburst Chart")
            fig_category_sunburst = px.sunburst(items_report, path=['Category', 'Item'], values='Qty.', title='Category-wise Item Distribution')
            st.plotly_chart(fig_category_sunburst)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.title("Welcome to the Sales Analysis Dashboard!")
        st.markdown("Please upload the sales report and items report on the left side to perform the analysis.")
        st.markdown("Make sure to click the 'Analyze' button after uploading the files.")


# Render pages
if st.query_params.get("logged_in"):
    main()
else:
    st.title("Sales Analysis Dashboard")
    option = st.radio("Choose an option:", ["Login", "Register"])

    if option == "Login":
        login()
    elif option == "Register":
        signup()
