import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px

# Function to read fundamental data from JSON files for specified dates
def read_fundamental_data(financial_folder, stock_name, selected_dates):
    fundamental_file_path = os.path.join(financial_folder, f"{stock_name}.json")
    if os.path.exists(fundamental_file_path):
        try:
            with open(fundamental_file_path, 'r') as f:
                fundamental_data = json.load(f)
                st.write(f"Financial Data for {stock_name} for Selected Dates:")
                
                # Check if 'IncomeStatement', 'BalanceSheet', and 'CashFlow' are lists
                income_statements = fundamental_data.get('IncomeStatement', [])
                balance_sheets = fundamental_data.get('BalanceSheet', [])
                cash_flows = fundamental_data.get('CashFlow', [])
                
                if not isinstance(income_statements, list) or not isinstance(balance_sheets, list) or not isinstance(cash_flows, list):
                    st.write("Error: 'IncomeStatement', 'BalanceSheet', or 'CashFlow' is not a list.")
                    return None
                
                # Create DataFrames for the tables
                data_for_dates = []
                for date in selected_dates:
                    income_statement_for_date = next((statement for statement in income_statements if statement.get('Date', '') == date), {})
                    balance_sheet_for_date = next((sheet for sheet in balance_sheets if sheet.get('Date', '') == date), {})
                    cash_flow_for_date = next((flow for flow in cash_flows if flow.get('Date', '') == date), {})
                    
                    data_for_date = {'Date': date, **income_statement_for_date, **balance_sheet_for_date, **cash_flow_for_date}
                    data_for_dates.append(data_for_date)
                
                # Create DataFrames for the tables
                data_df = pd.DataFrame(data_for_dates).set_index('Date')
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
st.title("Stock Financial Statement Analysis for Specific Dates")

# User input for stock search
stock_to_search = st.text_input("Enter Stock Name to Search:")

# Date range selection
start_date = st.date_input("Select Start Date:")
end_date = st.date_input("Select End Date:")

# Convert date inputs to the desired format
start_date_str = start_date.strftime("%b-%y")
end_date_str = end_date.strftime("%b-%y")

# Selected dates within the specified range
selected_dates = [
    "Dec-15", "Mar-16", "Jun-16", "Sep-16", "Dec-16", "Mar-17", "Jun-17", "Sep-17",
    "Dec-17", "Mar-18", "Jun-18", "Sep-18", "Dec-18", "Mar-19", "Jun-19", "Sep-19", "Dec-19",
    "Mar-20", "Jun-20", "Sep-20", "Dec-20", "Mar-21", "Jun-21", "Sep-21", "Dec-21", "Mar-22",
    "Jun-22", "Sep-22", "Dec-22", "Mar-23", "Jun-23", "Sep-23"
]

# Filter selected dates based on the date range
selected_dates = [date for date in selected_dates if start_date_str <= date <= end_date_str]

# Financial folder path
financial_folder = "financial"

# Read fundamental data for the searched stock
if st.button("Fetch Financial Statements"):
    st.write(f"Fetching Financial Statements for {stock_to_search} for Selected Dates...")
    
    # Read fundamental data for the searched stock
    fundamental_data = read_fundamental_data(financial_folder, stock_to_search, selected_dates)

    if fundamental_data is not None:
        # Extract Income Statement data
        income_statements = fundamental_data.get('IncomeStatement', [])
        income_statement_df = pd.DataFrame(income_statements).set_index('Date')

        # Perform horizontal analysis (changes over time)
        fig_horizontal = px.line(income_statement_df, x=income_statement_df.index, y=['Total Revenue/Income', 'Total Operating Expense', 'Operating Income/Profit', 'EBITDA', 'Net Income'],
                      title=f"Horizontal Analysis for {stock_to_search}",
                      labels={'value': 'Amount'},
                      line_shape="linear",
                      markers=True)

        st.plotly_chart(fig_horizontal)

        # Perform vertical analysis (percentage of total) for the latest date
        latest_date = income_statement_df.index[-1]
        latest_data = income_statement_df.loc[latest_date]
        total_revenue = latest_data['Total Revenue/Income']
        
        # Avoid division by zero
        if total_revenue != 0:
            percentages = latest_data[['Total Operating Expense', 'Operating Income/Profit', 'EBITDA', 'Net Income']] / total_revenue * 100

            # Create a bar chart for vertical analysis
            fig_vertical = px.bar(percentages, x=percentages.index, y=percentages.columns,
                          title=f"Vertical Analysis for {stock_to_search} on {latest_date}",
                          labels={'value': 'Percentage'},
                          barmode='stack')

            st.plotly_chart(fig_vertical)
