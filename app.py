import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px

# Function to read fundamental data from JSON files for specified dates
def read_fundamental_data(financial_folder, stock_name, selected_dates):
    # ... (previous code)

# Streamlit UI
st.title("Stock Financial Statement Analysis for Specific Dates")

# User input for stock search
stock_to_search = st.text_input("Enter Stock Name to Search:")

# Selected dates
selected_dates = [
    "Dec-15", "Mar-16", "Jun-16", "Sep-16", "Dec-16", "Mar-17", "Jun-17", "Sep-17",
    "Dec-17", "Mar-18", "Jun-18", "Sep-18", "Dec-18", "Mar-19", "Jun-19", "Sep-19", "Dec-19",
    "Mar-20", "Jun-20", "Sep-20", "Dec-20", "Mar-21", "Jun-21", "Sep-21", "Dec-21", "Mar-22",
    "Jun-22", "Sep-22", "Dec-22", "Mar-23", "Jun-23", "Sep-23"
]

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

        # Plot Total Revenue/Income, Total Operating Expense, Operating Income/Profit, EBITDA, and Net Income
        fig = px.line(income_statement_df, x=income_statement_df.index, y=['Total Revenue/Income', 'Total Operating Expense', 'Operating Income/Profit', 'EBITDA', 'Net Income'],
                      title=f"Financial Statement Analysis for {stock_to_search}",
                      labels={'value': 'Amount'},
                      line_shape="linear",
                      markers=True)

        st.plotly_chart(fig)

        # Perform vertical analysis (percentage of total) for the latest date
        latest_date = income_statement_df.index[-1]
        latest_data = income_statement_df.loc[latest_date]
        total_revenue = latest_data['Total Revenue/Income']
        
        # Calculate percentages
        percentages = latest_data[['Total Operating Expense', 'Operating Income/Profit', 'EBITDA', 'Net Income']] / total_revenue * 100

        # Plot vertical analysis as a bar chart
        fig_vertical = px.bar(percentages, x=percentages.index, y=percentages.columns,
                              title=f"Vertical Analysis for {stock_to_search} on {latest_date}",
                              labels={'value': 'Percentage'},
                              line_shape="linear",
                              markers=True)

        st.plotly_chart(fig_vertical)
