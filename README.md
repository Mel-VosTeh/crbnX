# crbnX-Project

**Overview**
This project implements an ETL (Extract, Transform, Load) pipeline and a RESTful API using Python and FastAPI.

**Project Structure**
```
crbnX-Project/
├── data/
│   ├── transactions_sample.csv    # Sample data file for ingestion
├── etl.py                         # ETL pipeline implementation
├── tests/
│   ├── test_etl.py                # Unit tests for ETL pipeline
│   ├── test_api.py                # Unit tests for API endpoints
├── api.py                         # Script to run the FastAPI server
├── requirements.txt              
├── README.md                      # Project documentation (this file)
```

**Clone the Repository**
git clone https://github.com/Mel-VosTeh/crbnX.git
cd crbnX-Project


**Install Dependencies**
pip install -r requirements.txt

**ETL Pipeline**
The ETL pipeline consists of three main steps:
1-Ingest: Reads the CSV file using Pandas.
2-Transform: Cleans and transforms the data by:
   - Handling missing values
   - Removing duplicates
   - Standardizing data types and values
   - Ensuring data integrity through logical checks
3-Load: Saves the transformed data to a SQLite database.
   
**API**
- Start the FastAPI Server: uvicorn main:app --reload
- The API will be available at: http://127.0.0.1:8000
- API documentation can be accessed at: http://127.0.0.1:8000/docs



**API Endpoints**
```
1. Root Endpoint
URL: /
Method: GET
Description: Returns a welcome message.
Response:
Status: 200 OK
Body: {"message": "Welcome to the Transaction Data API :) Visit /docs for API documentation."}

2. Fetch All Transformed Data
URL: /data/all
Method: GET
Description: Retrieves all transaction records.
Response:
Status: 200 OK
Body: List of all transaction records in JSON format.
Example: GET /data/all

3. Fetch Filtered Data
URL: /data/filter
Method: GET
Description: Fetches transaction data filtered by:
start_date: YYYY-MM-DD (optional)
end_date: YYYY-MM-DD (optional)
status: Transaction status (optional)
Response:
Status: 200 OK
Body: Filtered records in JSON format.
Errors: 400: Invalid date format / 500: Server error
Example: GET /data/filter?start_date=2023-08-25&status=complete
```

**Unit Tests**
- Located in the `tests` directory, covering both the ETL pipeline and API.
- Run etl test: ```python -m unittest test-etl.py```
- Run api test: ```python -m unittest test-api.py```

**Author**
Melissa Vosough (Mel-VosTeh) / melissa.v.tehrani@gmail.com

---
