from fastapi import FastAPI, Query, HTTPException
import sqlite3
import pandas as pd
from typing import Optional
import logging
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI(
    title="Transaction Data API",
    description="An API for retrieving transaction data from the transformed dataset",
    version="1.0"
)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Log all INFO-level and above messages
    format="%(asctime)s - %(levelname)s - %(message)s",  # Include timestamp, level, and message
)

# Helper function to connect to the SQLite database
def get_database_connection():
    try:
        conn = sqlite3.connect("output/transformed_data.db")
        logging.info("Database connection successful")  # Log successful connection
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")  # Log the error
        raise Exception(f"Error connecting to the database: {e}")

# Root endpoint
@app.get("/", summary="Root Endpoint")
async def root():
    return {"message": "Welcome to the Transaction Data API :) Visit /docs for API documentation."}

# Endpoint to fetch all transformed data
@app.get("/data/all", summary="Fetch All Transformed Data")
async def fetch_all_data():
    try:
        # Connect to the database and fetch all data
        conn = get_database_connection()
        query = "SELECT * FROM transactions"
        data = pd.read_sql_query(query, conn)
        conn.close()
        logging.info("Fetched all data successfully")  # Log successful data fetch
        # Return the data as a list of dictionaries (JSON format)
        return data.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Error fetching all data: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error fetching all data: {e}")  # Return a 500 error

# Endpoint to fetch filtered data based on query parameters
@app.get("/data/filter", summary="Fetch Filtered Data")
async def fetch_filtered_data(
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    status: Optional[str] = Query(None, description="Transaction status")
):
    try:
        # Validate date formats
        if start_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")  # Check if start_date is in the correct format
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")
        if end_date:
            try:
                datetime.strptime(end_date, "%Y-%m-%d")  # Check if end_date is in the correct format
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

        # Connect to the database
        conn = get_database_connection()
        # Start building the SQL query
        query = "SELECT * FROM transactions WHERE 1=1"

        # Apply filters based on query parameters
        if start_date:
            query += f" AND Date >= '{start_date}'"
        if end_date:
            query += f" AND Date <= '{end_date}'"
        if status:
            query += f" AND Status = '{status}'"

        # Execute the query and fetch data
        data = pd.read_sql_query(query, conn)
        conn.close()
        logging.info("Fetched filtered data successfully")  # Log successful data fetch
        # Return the filtered data as a list of dictionaries (JSON format)
        return data.to_dict(orient="records")
    except HTTPException as http_exc:
        raise http_exc  # Re-raise HTTP exceptions
    except Exception as e:
        logging.error(f"Error fetching filtered data: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error fetching filtered data: {e}")  # Return a 500 error
