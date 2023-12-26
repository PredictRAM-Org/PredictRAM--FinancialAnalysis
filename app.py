import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px

# Function to read fundamental data from JSON files for specified date range
def read_fundamental_data(financial_folder, stock_name, start_date, end_date):
    fundamental_file_path = os.path.join(financial_folder, f"{stock_name}.json")
    if os.path.exists(fundamental_file_path):
        try:
            with open(fundamental_file_path, 'r') as f:
                fundamental_data = json.load(f)
                st.write(f"Financial Data for {stock_name} for Selected Date Range:")
                
                # Check if 'IncomeStatement', 'BalanceSheet', and 'CashFlow' are lists
                income_statements = fundamental_data.get('IncomeStatement', [])
                balance_sheets = fundamental_data.get('BalanceSheet', [])
                cash_flows = fundamental_data.get('CashFlow', [])
                
                if not isinstance(income_statements, list) or not isinstance(balance_sheets, list) or not isinstance(cash_flows, list):
                    st.write("Error: 'IncomeStatement', 'BalanceSheet', or 'CashFlow' is not a list.")
                    return None
                
                # Create DataFrames for the tables
                data_for_date_range = []
                for statement in income_statements:
                    date = statement.get('Date', '')
                    if start_date <= date <= end_date:
                        balance_sheet_for_date = next((sheet for sheet in balance_sheets if sheet.get('Date', '') == date), {})
                        cash_flow_for_date = next((flow for flow in cash_flows if flow.get('Date', '') == date), {})
                        
                        data_for_date = {'Date': date, **statement, **balance_sheet_for_date, **cash_flow_for_date}
                        data_for_date_range.append(data_for_date)
                
                # Create DataFrames for the tables
                data_df = pd.DataFrame(data_for_date_range).set_index('Date')
                income_statement_df = data_df.filter(regex='^(?!BalanceSheet|CashFlow).*')
                balance_sheet_df = data_df.filter(regex='^BalanceSheet.*')
                cash_flow_df = data_df.filter(regex='^CashFlow.*')
                
                # Display tables
                st.write("Income Statement Data:")
                st.table(income_statement_df)
                
                st.write("Balance Sheet Data:")
                st.table(balance_sheet_df)
                
                st.write("Cash Flow Data:")
                st.table(cash_flow_df)
                
                st.write(f"Fundamental data for {stock_name} loaded successfully.")
                
                return fundamental_data
        except json.JSONDecodeError as e:
            st.write(f"Error decoding JSON for {stock_name}.json. Details: {str(e)}")
            return None
    else:
        st.write(f"Warning: Fundamental data not found for {stock_name}. Skipping. Path: {fundamental_file_path}")
        return None

# Streamlit UI
st.title("Stock Financial Statement Analysis for Date Range")

# User input for stock search
stock_to_search = st.text_input("Enter Stock Name to Search:")

# Date range input
start_date = st.date_input("Select Start Date:")
end_date = st.date_input("Select End Date:")

# Convert date format to match the input format
start_date_str = start_date.strftime("%b-%y")
end_date_str = end_date.strftime("%b-%y")

# Financial folder path
financial_folder = "financial"

# Read fundamental data for the searched stock
if st.button("Fetch Financial Statements"):
    st.write(f"Fetching Financial Statements for {stock_to_search} for Date Range: {start_date_str} to {end_date_str}...")
    
    # Read fundamental data for the searched stock
    fundamental_data = read_fundamental_data(financial_folder, stock_to_search, start_date_str, end_date_str)

    if fundamental_data is not None:
        # Extract Income Statement data
        income_statements = fundamental_data.get('IncomeStatement', [])
        income_statement_df = pd.DataFrame(income_statements).set_index('Date')

        # Perform horizontal analysis (changes over time)
        fig_horizontal = px.line(income_statement_df, x=income_statement_df.index, y=income_statement_df.columns,
                      title=f"Horizontal Analysis for {stock_to_search} from {start_date_str} to {end_date_str}",
                      labels={'value': 'Amount'},
                      line_shape="linear",
                      markers=True)

        st.plotly_chart(fig_horizontal)
