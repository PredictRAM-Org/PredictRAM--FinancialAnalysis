import os
import json
import pandas as pd
import streamlit as st

# Function to read fundamental data from JSON files for specified dates
def read_fundamental_data(financial_folder, stock_name, selected_dates):
    fundamental_file_path = os.path.join(financial_folder, f"{stock_name}.json")
    if os.path.exists(fundamental_file_path):
        try:
            with open(fundamental_file_path, 'r') as f:
                fundamental_data = json.load(f)
                st.write(f"Income Statement for {stock_name} for Selected Dates:")
                
                # Filter Income Statement data for specified dates
                income_statement = fundamental_data.get('IncomeStatement', {})
                
                # Use a list comprehension to extract values for specified dates
                filtered_income_statement = [
                    {'Date': date, **(income_statement.get(date, {}) or {})}
                    for date in selected_dates
                ]
                
                # Create a DataFrame for the table
                income_statement_df = pd.DataFrame(filtered_income_statement).set_index('Date')
                
                st.table(income_statement_df)
                st.write(f"Fundamental data for {stock_name} loaded successfully.")
            return fundamental_data
        except json.JSONDecodeError as e:
            st.write(f"Error decoding JSON for {stock_name}.json. Details: {str(e)}")
            return None
    else:
        st.write(f"Warning: Fundamental data not found for {stock_name}. Skipping. Path: {fundamental_file_path}")
        return None

# Streamlit UI
st.title("Stock Income Statement Analysis for Specific Dates")

# User input for stock search
stock_to_search = st.text_input("Enter Stock Name to Search:")

# Selected dates
selected_dates = [
    "Dec-00", "Dec-15", "Mar-16", "Jun-16", "Sep-16", "Dec-16", "Mar-17", "Jun-17", "Sep-17",
    "Dec-17", "Mar-18", "Jun-18", "Sep-18", "Dec-18", "Mar-19", "Jun-19", "Sep-19", "Dec-19",
    "Mar-20", "Jun-20", "Sep-20", "Dec-20", "Mar-21", "Jun-21", "Sep-21", "Dec-21", "Mar-22",
    "Jun-22", "Sep-22", "Dec-22", "Mar-23", "Jun-23", "Sep-23"
]

# Financial folder path
financial_folder = "financial"

# Read fundamental data for the searched stock
if st.button("Fetch Income Statement"):
    st.write(f"Fetching Income Statement for {stock_to_search} for Selected Dates...")
    
    # Read fundamental data for the searched stock
    fundamental_data = read_fundamental_data(financial_folder, stock_to_search, selected_dates)

    if fundamental_data is not None:
        # Additional analysis or visualization based on the Income Statement can be added here.
        pass
