import pandas as pd
import sqlite3

def ingest_data(file_path):
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)
        print("Data ingestion successful!")
        return data
    except Exception as e:
        print(f"Error during data ingestion: {e}")
        return None
import pandas as pd

def transform_data(data):
    # Handling missing values with contextual rules
    data["Quantity"] = data.groupby("Product")["Quantity"].transform(lambda x: x.fillna(x.median()))
    data["Price"] = data.groupby("Product")["Price"].transform(lambda x: x.fillna(x.mean()))

    # Calculate TotalAmount if both Quantity and Price are available
    data["TotalAmount"] = data["Quantity"] * data["Price"]

    # Convert Date to datetime and handle invalid dates
    data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
    data = data.dropna(subset=["Date"])  # Remove rows with invalid or missing dates

    # Remove duplicates based on TransactionID to ensure data uniqueness
    data = data.drop_duplicates(subset="TransactionID", keep="first")

    # Enforce data type consistency
    data["Quantity"] = data["Quantity"].astype(int, errors='ignore')  # Convert to integer
    data["Price"] = pd.to_numeric(data["Price"], errors='coerce')  # Convert to numeric
    data = data.dropna(subset=["Price"])  # Remove rows where Price is still missing after conversion

    # Logical checks
    # Ensure Quantity and Price are non-negative
    data = data[(data["Quantity"] >= 0) & (data["Price"] >= 0)]

    # Handle Status values: Convert to lowercase and standardize common values
    data["Status"] = data["Status"].str.lower().str.strip()
    data["Status"] = data["Status"].replace({"completed": "complete"})  # Example standardization


    print("Data transformation successful with added quality checks!")
    return data


def load_data(data, db_path="output/transformed_data.db"):
    try:
        # Save the transformed data to a SQLite database
        conn = sqlite3.connect(db_path)
        data.to_sql("transactions", conn, if_exists="replace", index=False)
        conn.close()
        print("Data successfully saved to SQLite database!")
    except Exception as e:
        print(f"Error during data load: {e}")

def run_etl_pipeline():
    data = ingest_data("data/transactions_sample.csv")
    if data is None:
        return
    transformed_data = transform_data(data)
    load_data(transformed_data)

if __name__ == "__main__":
    run_etl_pipeline()
