import unittest
import pandas as pd
from etl import ingest_data, transform_data

class TestETL(unittest.TestCase):

    def setUp(self):
        # Sample data to use in tests
        self.sample_data = pd.DataFrame({
            "TransactionID": [1001, 1002, 1003, 1003],  # Duplicate to test removal
            "Date": ["2023-10-01", "invalid_date", "2023-10-03", "2023-10-04"],
            "Product": ["Widget A", "Widget B", "Widget A", "Widget C"],
            "Quantity": [5, None, 10, -1],  # None and negative value to test validation
            "Price": [100.0, 200.0, None, 50.0],  # None to test filling
            "Status": ["Complete", "completed", "Pending", "complete"]
        })

    def test_ingest_data(self):
        # Test that the data ingestion function loads data correctly
        data = ingest_data("data/transactions_sample.csv")
        self.assertIsNotNone(data, "Data ingestion should not return None")

    def test_transform_data(self):
        # Test the data transformation function
        transformed_data = transform_data(self.sample_data)

        # Check if invalid dates were removed
        self.assertNotIn("invalid_date", transformed_data["Date"].astype(str).values, "Invalid dates should be removed")

        # Check if duplicates were removed
        self.assertEqual(len(transformed_data["TransactionID"].unique()), len(transformed_data), "Duplicates should be removed")

        # Check if missing Quantity was filled
        self.assertFalse(transformed_data["Quantity"].isnull().any(), "Missing Quantity values should be filled")

        # Check if negative Quantity values were filtered out
        self.assertTrue((transformed_data["Quantity"] >= 0).all(), "Quantity values should be non-negative")

        # Check if Status values were standardized
        self.assertTrue(all(transformed_data["Status"].isin(["complete", "pending"])), "Status values should be standardized")

if __name__ == "__main__":
    unittest.main()
