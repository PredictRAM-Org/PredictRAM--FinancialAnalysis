import os
import json
import pandas as pd
import streamlit as st

# Function to read fundamental data from JSON files
def read_fundamental_data(financial_folder, stock_name):
    fundamental_file_path = os.path.join(financial_folder, f"{stock_name}.json")
    if os.path.exists(fundamental_file_path):
        try:
            with open(fundamental_file_path, 'r') as f:
                fundamental_data = json.load(f)
                st.write(f"Income Statement for {stock_name}:")
                income_statement = fundamental_data.get('IncomeStatement', {})
                st.table(pd.DataFrame(income_statement))
                st.write(f"Fundamental data for {stock_name} loaded successfully.")
            return fundamental_data
        except json.JSONDecodeError as e:
            st.write(f"Error decoding JSON for {stock_name}.json. Details: {str(e)}")
            return None
    else:
        st.write(f"Warning: Fundamental data not found for {stock_name}. Skipping. Path: {fundamental_file_path}")
        return None

# Streamlit UI
st.title("Stock Income Statement Analysis")

# User input for stock search
stock_to_search = st.text_input("Enter Stock Name to Search:")

# Financial folder path
financial_folder = "financial"

# Read fundamental data for the searched stock
if st.button("Fetch Income Statement"):
    st.write(f"Fetching Income Statement for {stock_to_search}...")
    
    # Read fundamental data for the searched stock
    fundamental_data = read_fundamental_data(financial_folder, stock_to_search)

    if fundamental_data is not None:
        # Additional analysis or visualization based on the Income Statement can be added here.
        pass
