import streamlit as st
import pandas as pd
import os

# Function to load financial data from JSON files
def load_data(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data[filename] = pd.read_json(file)
    return data

# Function to display tables for a given financial statement
def display_table(data, statement_name, dates):
    st.subheader(statement_name)
    for date in dates:
        st.write(f"## {date}")
        if date in data:
            st.table(data[date])
        else:
            st.warning(f"No data available for {date}")

def main():
    st.title("Financial Data Viewer")

    # Set the path to your financial folder
    financial_folder_path = "financial"

    # Load financial data
    financial_data = load_data(financial_folder_path)

    # Specify the dates
    statement_dates = ["Sep-15", "Dec-15", "Mar-16", "Jun-16", "Sep-16", "Dec-16", "Mar-17", "Jun-17", "Sep-17",
                       "Dec-17", "Mar-18", "Jun-18", "Sep-18", "Dec-18", "Mar-19", "Jun-19", "Sep-19", "Dec-19",
                       "Mar-20", "Jun-20", "Sep-20", "Dec-20", "Mar-21", "Jun-21", "Sep-21", "Dec-21", "Mar-22",
                       "Jun-22", "Sep-22", "Dec-22", "Mar-23", "Jun-23", "Sep-23"]

    # Display tables for each financial statement
    display_table(financial_data, "Income Statement", statement_dates)
    display_table(financial_data, "Balance Sheet", statement_dates)
    display_table(financial_data, "Cash Flow", statement_dates)

if __name__ == "__main__":
    main()
