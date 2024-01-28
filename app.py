import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler


# Function to read fundamental data from JSON files for the specified date range
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
                income_statement_df = data_df.filter(regex='^(?!BalanceSheet|CashFlow).*').sort_index()
                balance_sheet_df = data_df.filter(regex='^BalanceSheet.*').sort_index()
                cash_flow_df = data_df.filter(regex='^CashFlow.*').sort_index()

                # Display tables
                st.write("Income Statement Data (Ascending Order):")
                st.table(income_statement_df)

                st.write("Balance Sheet Data (Ascending Order):")
                st.table(balance_sheet_df)

                st.write("Cash Flow Data (Ascending Order):")
                st.table(cash_flow_df)

                st.write(f"Fundamental data for {stock_name} loaded successfully.")

                return fundamental_data
        except json.JSONDecodeError as e:
            st.write(f"Error decoding JSON for {stock_name}.json. Details: {str(e)}")
            return None
    else:
        st.write(f"Warning: Fundamental data not found for {stock_name}. Skipping. Path: {fundamental_file_path}")
        return None

# Function to normalize the data using Min-Max scaling
def normalize_data(data_df):
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data_df.values)
    normalized_df = pd.DataFrame(normalized_data, columns=data_df.columns, index=data_df.index)
    return normalized_df


# Streamlit UI
st.title("Stock Financial Statement Analysis for Date Range")

# User input for stock search
stock_to_search = st.text_input("Enter Stock Name to Search:")

# Given list of dates
given_dates = [
    "Dec-15", "Mar-16", "Jun-16", "Sep-16", "Dec-16", "Mar-17", "Jun-17", "Sep-17",
    "Dec-17", "Mar-18", "Jun-18", "Sep-18", "Dec-18", "Mar-19", "Jun-19", "Sep-19", "Dec-19",
    "Mar-20", "Jun-20", "Sep-20", "Dec-20", "Mar-21", "Jun-21", "Sep-21", "Dec-21", "Mar-22",
    "Jun-22", "Sep-22", "Dec-22", "Mar-23", "Jun-23", "Sep-23"
]

# Dropdown menu for start date
start_date = st.selectbox("Select Start Date:", given_dates)

# Dropdown menu for end date
end_date = st.selectbox("Select End Date:", given_dates)

# Financial folder path
financial_folder = "financial"

# Read fundamental data for the searched stock
if st.button("Fetch Financial Statements"):
    st.write(f"Fetching Financial Statements for {stock_to_search} for Date Range: {start_date} to {end_date}...")

    # Read fundamental data for the searched stock
    fundamental_data = read_fundamental_data(financial_folder, stock_to_search, start_date, end_date)

    if fundamental_data is not None:
        # Extract Income Statement data for the selected date range
        income_statements = fundamental_data.get('IncomeStatement', [])
        income_statement_df = pd.DataFrame(income_statements).set_index('Date').sort_index()
        income_statement_df = income_statement_df.loc[start_date:end_date]

        # Normalize the data for comparison
        normalized_income_statement_df = normalize_data(income_statement_df)

        # Create an interactive line chart for the normalized metrics
        fig_trends_normalized = px.line(normalized_income_statement_df,
                                        x=normalized_income_statement_df.index,
                                        y=normalized_income_statement_df.columns,
                                        title=f"Normalized Trends Analysis for {stock_to_search} from {start_date} to {end_date}",
                                        labels={'value': 'Normalized Amount'},
                                        line_shape="linear",
                                        markers=True)

        st.plotly_chart(fig_trends_normalized)

        # Display original data for reference
        st.write("Original Income Statement Data (Ascending Order) for Selected Date Range:")
        st.table(income_statement_df.sort_index(ascending=True))
