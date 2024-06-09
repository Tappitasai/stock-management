import streamlit as st
import pandas as pd
import os

# Function to load or create an Excel file
def load_excel(file_path):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        if 'Date' in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.date  # Ensure 'Date' is in date format without time
        else:
            df = pd.DataFrame(columns=["Date", "S.No.", "Birds", "Weight", "Rate", "Value", "Collection", "Balance"])
    else:
        columns = ["Date", "S.No.", "Birds", "Weight", "Rate", "Value", "Collection", "Balance"]
        df = pd.DataFrame(columns=columns)
        df.to_excel(file_path, index=False)
    return df

# Ensure the directory exists
directory = "E:/chicken_stock"
os.makedirs(directory, exist_ok=True)

# Streamlit UI
company = st.selectbox('Select company:', options=["sneha", "vhsl", "satyanarayana"])

st.title("Daily Values Entry")

# Define the Excel file path based on selected company
excel_file = f"{company}_daily_values.xlsx"
file_path = os.path.join(directory, excel_file)

# Load the existing data for the selected company
df = load_excel(file_path)

# Input fields
date = st.date_input("Date")
serial_no = st.number_input("S.No.", min_value=1)
birds = st.number_input("Birds", min_value=0)
weight = st.number_input("Weight (in kg)", min_value=0.0)
rate = st.number_input("Rate (per kg)", min_value=0.0)
value = weight * rate
collection = st.number_input("Collection", min_value=0)
# balance = collection - value
# Calculate the balance
if not df.empty:
    previous_balance = df.iloc[-1]["Balance"]
else:
    previous_balance = 0

balance = collection - value + previous_balance

# Display calculated value and balance
st.write(f"Calculated Value: {value}")
st.write(f"Calculated Balance: {balance}")

# Add new entry to DataFrame
if st.button("Add Entry"):
    # Convert date input to date (without time)
    date = date.strftime('%Y-%m-%d')
    
    # Check for duplicate entries
    if not ((df["Date"] == date) & (df["S.No."] == serial_no)).any():
        new_entry = pd.DataFrame({
            "Date": [date],
            "S.No.": [serial_no],
            "Birds": [birds],
            "Weight": [weight],
            "Rate": [rate],
            "Value": [value],
            "Collection": [collection],
            "Balance": [balance]
        })
        df = pd.concat([df, new_entry], ignore_index=True)
        try:
            df.to_excel(file_path, index=False)
            st.success("Entry added successfully!")
        except PermissionError:
            st.error(f"Permission denied: Ensure '{file_path}' is not open in another program.")
        except Exception as e:
            st.error(f"Error saving to Excel: {e}")
    else:
        st.warning("An entry with the same date and serial number already exists.")

# Delete selected rows
rows_to_delete = st.multiselect("Select rows to delete", df.index)
if st.button("Delete Selected"):
    if rows_to_delete:
        df = df.drop(rows_to_delete, axis=0).reset_index(drop=True)
        try:
            df.to_excel(file_path, index=False)
            st.success("Selected rows deleted successfully.")
        except PermissionError:
            st.error(f"Permission denied: Ensure '{file_path}' is not open in another program.")
        except Exception as e:
            st.error(f"Error saving to Excel: {e}")
    else:
        st.warning("No rows selected for deletion.")

# Display the DataFrame
st.write(df)

